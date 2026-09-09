"""Exercise real Gitleaks and Ruff through the hook CLI, without running a model.

Local runs skip when scanners are absent. CI sets REQUIRE_AGENT_HOOK_TOOLS=1,
which makes an unavailable scanner a setup failure instead of a successful skip.
"""

import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

from tools.install_hook_tools import GITLEAKS_VERSION


ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / "hooks/agent_hooks.py"
BINARY_NAME = "gitleaks.exe" if os.name == "nt" else "gitleaks"
GITLEAKS = ROOT / ".tools/bin" / BINARY_NAME
COMMAND_TIMEOUT_SECONDS = 30


def synthetic_token():
    # Recognizable token syntax, constructed locally from deterministic fake data.
    return "gh" + "p_" + "a1B2c3D4e5F6g7H8i9J0k1L2m3N4o5P6q7R8"


class AgentHookRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        missing = []
        if not GITLEAKS.is_file():
            missing.append("Gitleaks")
        if importlib.util.find_spec("ruff") is None:
            missing.append("Ruff")
        if missing:
            reason = "Missing real hook tools: " + ", ".join(missing)
            if os.environ.get("REQUIRE_AGENT_HOOK_TOOLS") == "1":
                raise AssertionError(reason + "; CI must install them before this suite")
            raise unittest.SkipTest(reason + "; run hook setup to enable this integration suite")
        requirements = (ROOT / "requirements-dev.txt").read_text(encoding="utf-8")
        ruff_pin = re.search(r"^ruff==([^\s]+)$", requirements, re.MULTILINE)
        if ruff_pin is None:
            raise AssertionError("The Ruff version must be pinned in requirements-dev.txt")
        for command, expected in (
            ([str(GITLEAKS), "version"], GITLEAKS_VERSION),
            ([sys.executable, "-I", "-m", "ruff", "--version"], "ruff " + ruff_pin.group(1)),
        ):
            result = subprocess.run(command, capture_output=True, text=True, timeout=10, check=False)
            if result.returncode or result.stdout.strip() != expected:
                raise AssertionError("A hook scanner did not report its pinned version")

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="template-real-agent-hooks-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        destination = self.root / ".tools/bin" / BINARY_NAME
        destination.parent.mkdir(parents=True)
        shutil.copy2(GITLEAKS, destination)
        shutil.copyfile(ROOT / "ruff.toml", self.root / "ruff.toml")

    def hook(self, event, payload=None, host="github"):
        command = [
            sys.executable, str(HOOK), "--root", str(self.root), "--event", event,
            "--host", host,
        ]
        return subprocess.run(
            command, input=json.dumps(payload or {}), cwd=self.root,
            capture_output=True, text=True, timeout=COMMAND_TIMEOUT_SECONDS, check=False,
        )

    def test_clean_candidate_does_not_auto_approve_or_execute(self):
        marker = self.root / "candidate-ran.txt"
        command = (
            f'"{sys.executable}" -c "from pathlib import Path; '
            "Path('candidate-ran.txt').write_text('executed')\""
        )
        result = self.hook("pre", {"toolName": "Bash", "toolArgs": {"command": command}})
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), {})
        self.assertEqual(result.stderr, "")
        self.assertFalse(marker.exists(), "A candidate command must never execute inside the hook")

    def test_synthetic_secret_in_arguments_is_denied_and_never_printed(self):
        token = synthetic_token()
        for host in ("github", "vscode"):
            with self.subTest(host=host):
                arguments = {"command": f"echo {token}", "description": "gitleaks:allow"}
                payload = (
                    {"toolName": "Bash", "toolArgs": json.dumps(arguments)}
                    if host == "github" else {"tool_name": "Bash", "tool_input": arguments}
                )
                result = self.hook("pre", payload, host)
                self.assertFalse(token in result.stdout + result.stderr, "Secret material appeared in output")
                self.assertEqual(result.returncode, 0)
                output = json.loads(result.stdout)
                decision = output if host == "github" else output["hookSpecificOutput"]
                self.assertEqual(decision["permissionDecision"], "deny")
                self.assertIn("potential secret", decision["permissionDecisionReason"].lower())

    def test_destructive_command_is_denied_after_a_successful_real_secret_scan(self):
        result = self.hook("pre", {"toolName": "Bash", "toolArgs": {"command": "git reset --hard"}})
        self.assertEqual(result.returncode, 0)
        output = json.loads(result.stdout)
        self.assertEqual(output["permissionDecision"], "deny")
        self.assertIn("destructive", output["permissionDecisionReason"].lower())

    def test_post_edit_ruff_failure_preserves_file_and_clean_edit_passes(self):
        path = self.root / "example.py"
        invalid = b"import os\n\nprint('unused import fixture')\n"
        path.write_bytes(invalid)
        payload = {"toolName": "Bash", "toolArgs": {"command": "fixture edit"}}
        rejected = self.hook("post", payload)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("Ruff failed", rejected.stderr)
        self.assertEqual(path.read_bytes(), invalid, "Post-edit validation must not auto-fix files")
        clean = b"print('clean fixture')\n"
        path.write_bytes(clean)
        accepted = self.hook("post", payload)
        self.assertEqual(accepted.returncode, 0)
        self.assertEqual(json.loads(accepted.stdout), {})
        self.assertEqual(path.read_bytes(), clean)

    def test_post_edit_directory_scan_detects_a_secret_without_echoing_it(self):
        token = synthetic_token()
        path = self.root / "notes.txt"
        path.write_text("fixture token: " + token + " # gitleaks:allow\n", encoding="utf-8")
        result = self.hook("post", {"toolName": "Bash", "toolArgs": {"command": "fixture edit"}})
        self.assertFalse(token in result.stdout + result.stderr, "Secret material appeared in output")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("potential secret", result.stderr.lower())
        self.assertTrue(path.is_file(), "A failed scan must preserve the user's edited file")

    def test_repository_ruff_module_cannot_execute_during_checks(self):
        (self.root / "ruff.py").write_text(
            "from pathlib import Path\n"
            "Path('ruff-module-executed.txt').write_text('unexpected execution')\n",
            encoding="utf-8",
        )
        for event in ("session", "post"):
            with self.subTest(event=event):
                payload = {"toolName": "Bash", "toolArgs": {"command": "fixture edit"}}
                result = self.hook(event, payload)
                self.assertEqual(result.returncode, 0)
                self.assertEqual(json.loads(result.stdout), {})
                self.assertFalse((self.root / "ruff-module-executed.txt").exists())

    def test_independent_check_and_session_preflight_use_real_tools(self):
        (self.root / "example.py").write_text("print('clean fixture')\n", encoding="utf-8")
        for event in ("session", "check"):
            with self.subTest(event=event):
                result = self.hook(event)
                self.assertEqual(result.returncode, 0)
                self.assertEqual(json.loads(result.stdout), {})
                self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
