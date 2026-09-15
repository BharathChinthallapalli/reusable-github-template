"""Real adapter subprocesses with inert commands and isolated audit files."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[2]


class ProcessTests(unittest.TestCase):
    def test_real_adapter_process_denial_and_diagnostic_all_protocols(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            guardian = root / ".guardian"
            shutil.copytree(ROOT / ".guardian/engine", guardian / "engine", ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copytree(ROOT / ".guardian/adapters", guardian / "adapters", ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copyfile(ROOT / ".guardian/policy.json", guardian / "policy.json")
            (guardian / "ledger.jsonl").touch()
            timings = []
            for runtime in ("copilot", "claude", "codex"):
                for command, expected in (("pwd", 0), ("cmdkey /list", 2)):
                    payload = {"session_id": runtime, "cwd": str(root), "tool_name": "Bash",
                               "tool_input": {"command": command}}
                    started = time.monotonic()
                    result = subprocess.run([sys.executable, "-I", str(guardian / "adapters/dispatch.py"),
                                             "--runtime", runtime, "--surface", "cli"],
                                            input=json.dumps(payload), text=True, capture_output=True,
                                            timeout=3, check=False)
                    timings.append(time.monotonic() - started)
                    self.assertEqual(result.returncode, expected, result.stderr)
                    output = json.loads(result.stdout)
                    self.assertEqual(output, {} if expected == 0 else {
                        "hookSpecificOutput": {"hookEventName": "PreToolUse",
                                               "permissionDecision": "deny",
                                               "permissionDecisionReason": result.stderr.strip()}})
            self.assertEqual(len((guardian / "ledger.jsonl").read_text().splitlines()), 6)
            print(f"Adapter subprocess latency: n={len(timings)}, max={max(timings):.3f}s")


if __name__ == "__main__":
    unittest.main()
