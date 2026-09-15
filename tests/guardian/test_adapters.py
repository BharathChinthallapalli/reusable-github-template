"""Host-wire fixture checks; no installed agent or prohibited command executes."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "guardian_dispatch", ROOT / ".guardian/adapters/dispatch.py"
)
dispatch = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dispatch)


class AdapterTests(unittest.TestCase):
    def invoke(self, runtime, payload, result=None, failure=None, event="PreToolUse"):
        def decide(*args, **kwargs):
            self.assertEqual(args[0]["_guardian_event"], event)
            if failure:
                raise failure
            return result

        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.dict(sys.modules, {"gate": types.SimpleNamespace(decide=decide)}):
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                code = dispatch.main(["--runtime", runtime, "--event", event], io.StringIO(payload))
        return code, json.loads(stdout.getvalue()), stderr.getvalue()

    def test_copilot_native_denies_with_reason(self):
        code, output, error = self.invoke("copilot", '{"toolName":"bash"}',
                                          {"decision": "IN_SCOPE", "rationale": "Route through guardian"})
        self.assertEqual(code, 2)
        self.assertEqual(output["permissionDecision"], "deny")
        self.assertIn("Route through guardian", error)

    def test_snake_case_nested_denial_all_hosts(self):
        for runtime in ["copilot", "claude", "codex"]:
            with self.subTest(runtime=runtime):
                code, output, _ = self.invoke(runtime, '{"tool_name":"Bash"}',
                                               {"decision": "HARD_DENY", "rationale": "Blocked"})
                self.assertEqual(code, 2)
                self.assertEqual(output["hookSpecificOutput"]["permissionDecision"], "deny")
                self.assertNotIn("continue", output)

    def test_review_success_preserves_normal_permissions(self):
        for runtime in ["copilot", "claude", "codex"]:
            for decision in ["APPROVED", "AUTO_ALLOW"]:
                code, output, _ = self.invoke(runtime, '{}', {"decision": decision})
                self.assertEqual((code, output), (0, {}))

    def test_permission_request_is_deny_not_ask(self):
        code, output, _ = self.invoke("copilot", '{"hook_event_name":"permissionRequest"}',
                                       {"decision": "PIVOT_ATTEMPT", "rationale": "Pivot"},
                                       event="permissionRequest")
        self.assertEqual((code, output["behavior"]), (2, "deny"))

    def test_engine_crash_blocks_without_secret_disclosure(self):
        for runtime in ["copilot", "claude", "codex"]:
            code, _, error = self.invoke(runtime, '{}', failure=RuntimeError("SENSITIVE"))
            self.assertEqual(code, 2)
            self.assertNotIn("SENSITIVE", error)

    def test_invalid_and_oversized_input_blocks(self):
        for payload in ['[]', '{', 'x' * (dispatch.MAX_INPUT + 1)]:
            code, _, _ = self.invoke("codex", payload)
            self.assertEqual(code, 2)

    def test_unknown_decision_blocks(self):
        code, _, _ = self.invoke("claude", '{}', {"decision": "ALLOW"})
        self.assertEqual(code, 2)

    def test_payload_cannot_change_trusted_event(self):
        code, output, _ = self.invoke("copilot", '{"hook_event_name":"permissionRequest", "_guardian_event":"permissionRequest"}',
                                      {"decision": "IN_SCOPE", "rationale": "Review required"})
        self.assertEqual(code, 2)
        self.assertEqual(output["permissionDecision"], "deny")

    def test_permission_success_never_preapproves(self):
        code, output, _ = self.invoke("copilot", '{}', {"decision": "AUTO_ALLOW"},
                                      event="permissionRequest")
        self.assertEqual((code, output), (0, {}))

    def test_copilot_snake_case_crash_retains_protocol(self):
        code, output, _ = self.invoke("copilot", '{"tool_name":"Bash"}', failure=ValueError())
        self.assertEqual(code, 2)
        self.assertEqual(output["hookSpecificOutput"]["permissionDecision"], "deny")


if __name__ == "__main__":
    unittest.main()
