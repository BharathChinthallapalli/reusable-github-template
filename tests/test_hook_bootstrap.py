"""Exercise fresh-worktree startup and fail-closed recovery without network calls."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

from hooks import run_hook


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipIf(os.name == "nt", "Controlled package-manager executable is POSIX")
class HookBootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="hook-bootstrap-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve() / "repo with spaces"
        (self.root / "hooks").mkdir(parents=True)
        (self.root / "tools").mkdir()
        for name in ("agent_hooks.py", "run_hook.py"):
            shutil.copyfile(ROOT / "hooks" / name, self.root / "hooks" / name)
        (self.root / "requirements-dev.txt").write_text(
            "# offline fixture requirements\n"
        )
        self.installer = self.root / "tools/install_hook_tools.py"
        scanner = (
            f"#!{sys.executable}\nimport sys\n"
            "data = sys.stdin.read() if 'stdin' in sys.argv else ''\n"
            "sys.exit(10 if 'HOOK_TEST_SECRET' in data else 0)\n"
        )
        self.installer.write_text(
            "from pathlib import Path\n"
            "binary = Path(__file__).resolve().parents[1] / '.tools/bin/gitleaks'\n"
            "binary.parent.mkdir(parents=True, exist_ok=True)\n"
            f"binary.write_text({scanner!r})\n"
            "binary.chmod(0o755)\n"
        )
        binaries = self.root.parent / "bin"
        binaries.mkdir()
        uv = binaries / "uv"
        uv.write_text(
            f"#!{sys.executable}\nimport os, pathlib, subprocess, sys\n"
            "if os.environ.get('FIXTURE_SETUP_FAIL'):\n"
            "    print('sensitive-package-output', file=sys.stderr)\n"
            "    sys.exit(7)\n"
            "python = sys.argv[sys.argv.index('--python') + 1]\n"
            "site = subprocess.check_output([python, '-I', '-c', 'import sysconfig; print(sysconfig.get_path(\"purelib\"))'], text=True).strip()\n"
            "for module in ('ruff', 'yaml'):\n"
            "    pathlib.Path(site, module + '.py').write_text('')\n"
            "with pathlib.Path(os.environ['FIXTURE_SETUP_LOG']).open('a') as log: log.write('install\\n')\n"
        )
        uv.chmod(0o755)
        self.log = self.root.parent / "installs.log"
        self.environment = {
            **os.environ,
            "PATH": str(binaries) + os.pathsep + os.environ["PATH"],
            "FIXTURE_SETUP_LOG": str(self.log),
        }

    def invoke(self, event, payload=None, host="github", executable=None):
        return subprocess.run(
            [
                executable or sys.executable,
                str(self.root / "hooks/run_hook.py"),
                "--event",
                event,
                "--host",
                host,
            ],
            input=json.dumps(payload or {}),
            cwd=self.root,
            env=self.environment,
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
        )

    def test_fresh_start_allows_clean_read_and_keeps_secret_denial(self):
        blocked = self.invoke(
            "pre", {"toolName": "view", "toolArgs": {"path": "README.md"}}
        )
        self.assertEqual(json.loads(blocked.stdout)["permissionDecision"], "deny")
        self.assertFalse((self.root / ".tools").exists())
        started = self.invoke("session")
        self.assertEqual(started.returncode, 0, started.stderr)
        self.assertEqual(json.loads(started.stdout), {})
        clean = self.invoke(
            "pre", {"toolName": "view", "toolArgs": {"path": "README.md"}}
        )
        self.assertEqual(json.loads(clean.stdout), {})
        denied = self.invoke(
            "pre", {"toolName": "custom", "toolArgs": {"text": "HOOK_TEST_SECRET"}}
        )
        self.assertEqual(json.loads(denied.stdout)["permissionDecision"], "deny")
        self.assertNotIn("HOOK_TEST_SECRET", denied.stdout + denied.stderr)
        destructive = self.invoke(
            "pre", {"toolName": "bash", "toolArgs": {"command": "git reset --hard"}}
        )
        self.assertIn(
            "destructive",
            json.loads(destructive.stdout)["permissionDecisionReason"].lower(),
        )

    def test_resume_reuses_environment_and_scanner_update_invalidates_it(self):
        self.assertEqual(self.invoke("session").returncode, 0)
        self.assertEqual(self.invoke("session").returncode, 0)
        self.assertEqual(self.log.read_text().splitlines(), ["install"])
        self.installer.write_text(
            self.installer.read_text() + "# changed release pin\n"
        )
        blocked = self.invoke(
            "pre", {"toolName": "view", "toolArgs": {"path": "README.md"}}
        )
        self.assertEqual(json.loads(blocked.stdout)["permissionDecision"], "deny")
        self.assertEqual(self.invoke("session").returncode, 0)
        self.assertEqual(self.log.read_text().splitlines(), ["install", "install"])

    def test_corrupt_receipt_denies_pre_and_session_recovers(self):
        self.assertEqual(self.invoke("session").returncode, 0)
        receipt = self.root / ".tools/hook-environment.sha256"
        for content in (b"\xff\xfe", b'{"partial":', b"a" * 9000, b"[" * 1100, receipt.read_bytes() + b" " * 9000):
            with self.subTest(content=content[:10]):
                receipt.write_bytes(content)
                denied = self.invoke("pre", {"toolName": "view", "toolArgs": {"path": "README.md"}})
                self.assertEqual(json.loads(denied.stdout)["permissionDecision"], "deny")
                self.assertEqual(self.invoke("session").returncode, 0)

    def test_replaced_scanner_denied_without_executing_replacement(self):
        self.assertEqual(self.invoke("session").returncode, 0)
        scanner = self.root / ".tools/bin/gitleaks"
        marker = self.root / "untrusted-ran"
        scanner.write_text(f"#!{sys.executable}\nfrom pathlib import Path\nPath({str(marker)!r}).touch()\n")
        denied = self.invoke("pre", {"toolName": "view", "toolArgs": {"path": "README.md"}})
        self.assertEqual(json.loads(denied.stdout)["permissionDecision"], "deny")
        self.assertFalse(marker.exists())
        self.assertEqual(self.invoke("session").returncode, 0)
        self.assertFalse(marker.exists())

    def test_interpreter_link_to_arbitrary_executable_is_rejected(self):
        self.assertEqual(self.invoke("session").returncode, 0)
        interpreter = self.root / ".tools/venv/bin/python"
        interpreter.unlink()
        replacement = self.root / "untrusted-python"
        marker = self.root / "untrusted-ran"
        replacement.write_text(f"#!{sys.executable}\nfrom pathlib import Path\nPath({str(marker)!r}).touch()\n")
        replacement.chmod(0o755)
        interpreter.symlink_to(replacement)
        denied = self.invoke("pre", {"toolName": "view", "toolArgs": {"path": "README.md"}})
        self.assertEqual(json.loads(denied.stdout)["permissionDecision"], "deny")
        self.assertEqual(self.invoke("session").returncode, 2)
        self.assertFalse(marker.exists())
        # An in-environment replacement is not a legitimate base interpreter either.
        interpreter.unlink()
        internal = interpreter.parent / "alternate"
        shutil.copyfile(replacement, internal)
        internal.chmod(0o755)
        interpreter.symlink_to(internal)
        denied = self.invoke("pre", {"toolName": "view", "toolArgs": {"path": "README.md"}})
        self.assertEqual(json.loads(denied.stdout)["permissionDecision"], "deny")
        self.assertFalse(marker.exists())
        # Replacing a copied interpreter also invalidates its recorded digest.
        interpreter.unlink()
        shutil.copyfile(replacement, interpreter)
        interpreter.chmod(0o755)
        denied = self.invoke("pre", {"toolName": "view", "toolArgs": {"path": "README.md"}})
        self.assertEqual(json.loads(denied.stdout)["permissionDecision"], "deny")
        self.assertFalse(marker.exists())

    def test_scanner_symlink_and_parent_symlink_are_rejected(self):
        self.assertEqual(self.invoke("session").returncode, 0)
        scanner = self.root / ".tools/bin/gitleaks"
        target = self.root.parent / "external-scanner"
        shutil.copyfile(scanner, target)
        scanner.unlink()
        scanner.symlink_to(target)
        with self.assertRaisesRegex(run_hook.policy.CheckFailure, "scanner path"):
            run_hook.environment_ready(self.root)
        scanner.unlink()
        scanner.parent.rmdir()
        scanner.parent.symlink_to(self.root.parent, target_is_directory=True)
        with self.assertRaisesRegex(run_hook.policy.CheckFailure, "scanner path"):
            run_hook.environment_ready(self.root)

    def test_snake_case_missing_setup_returns_vscode_denial(self):
        result = subprocess.run(
            [sys.executable, str(self.root / "hooks/run_hook.py"), "--event", "pre"],
            input=json.dumps({"tool_name": "Read", "tool_input": {"path": "README.md"}}),
            cwd=self.root, env=self.environment, capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_failed_install_leaves_no_receipt_and_recovers_on_next_start(self):
        self.environment["FIXTURE_SETUP_FAIL"] = "1"
        failed = self.invoke("session")
        self.assertEqual(failed.returncode, 2)
        self.assertIn(
            "dependency installation", json.loads(failed.stdout)["additionalContext"]
        )
        self.assertNotIn("sensitive-package-output", failed.stdout + failed.stderr)
        self.assertFalse((self.root / ".tools/hook-environment.sha256").exists())
        blocked = self.invoke(
            "pre",
            {"tool_name": "Read", "tool_input": {"path": "README.md"}},
            host="codex",
        )
        self.assertEqual(
            json.loads(blocked.stdout)["hookSpecificOutput"]["permissionDecision"],
            "deny",
        )
        del self.environment["FIXTURE_SETUP_FAIL"]
        self.assertEqual(self.invoke("session").returncode, 0)

    def test_changed_requirements_and_missing_scanner_are_not_ready(self):
        self.assertEqual(self.invoke("session").returncode, 0)
        self.assertTrue(run_hook.environment_ready(self.root))
        requirements = self.root / "requirements-dev.txt"
        requirements.write_text(requirements.read_text() + "# updated\n")
        self.assertFalse(run_hook.environment_ready(self.root))
        self.assertEqual(self.invoke("session").returncode, 0)
        (self.root / ".tools/bin/gitleaks").unlink()
        self.assertFalse(run_hook.environment_ready(self.root))

    def test_setup_rejects_redirected_environment_without_touching_target(self):
        external = self.root.parent / "external"
        external.mkdir()
        (self.root / ".tools").symlink_to(external, target_is_directory=True)
        result = self.invoke("session")
        self.assertEqual(result.returncode, 2)
        self.assertIn("symlink", result.stderr)
        self.assertEqual(list(external.iterdir()), [])

    def test_expired_setup_deadline_does_not_mark_ready(self):
        with self.assertRaisesRegex(run_hook.policy.CheckFailure, "timed out"):
            run_hook.prepare_environment(self.root, time.monotonic() - 1)
        self.assertFalse((self.root / ".tools/hook-environment.sha256").exists())

    def test_removed_base_interpreter_is_repaired_on_next_start(self):
        self.assertEqual(self.invoke("session").returncode, 0)
        interpreter = self.root / ".tools/venv/bin/python"
        interpreter.unlink()
        interpreter.symlink_to(self.root.parent / "removed-python")
        self.assertFalse(interpreter.exists())
        repaired = self.invoke("session")
        self.assertEqual(repaired.returncode, 0, repaired.stderr)
        self.assertTrue(interpreter.is_file())
        self.assertEqual(self.log.read_text().splitlines(), ["install", "install"])

    def test_nested_environment_redirect_cannot_receive_package_writes(self):
        external = self.root.parent / "external-packages"
        external.mkdir()
        environment = self.root / ".tools/venv"
        environment.mkdir(parents=True)
        (environment / "lib").symlink_to(external, target_is_directory=True)
        result = self.invoke("session")
        self.assertEqual(result.returncode, 2)
        self.assertIn("redirected outside", result.stderr)
        self.assertEqual(list(external.iterdir()), [])
        self.assertFalse(self.log.exists())

    def test_python_314_interpreter_alias_does_not_redirect_package_writes(self):
        environment = self.root / ".tools/venv"
        binaries = environment / "bin"
        binaries.mkdir(parents=True)
        (binaries / "𝜋thon").symlink_to(sys.executable)
        run_hook.validate_environment_tree(environment)

    @unittest.skipUnless(
        sys.platform == "darwin", "Apple system Python is macOS-specific"
    )
    def test_apple_system_python_discovers_supported_runtime_and_reuses_it(self):
        system_python = "/usr/bin/python3"
        if not Path(system_python).is_file():
            self.skipTest("Apple developer tools Python is not installed")
        started = self.invoke("session", executable=system_python)
        self.assertEqual(started.returncode, 0, started.stderr)
        resumed = self.invoke("session", executable=system_python)
        self.assertEqual(resumed.returncode, 0, resumed.stderr)
        self.assertEqual(self.log.read_text().splitlines(), ["install"])
        clean = self.invoke(
            "pre",
            {"toolName": "view", "toolArgs": {"path": "README.md"}},
            executable=system_python,
        )
        self.assertEqual(json.loads(clean.stdout), {})

    def test_concurrent_setup_wait_is_bounded_and_lock_is_released(self):
        lock = self.root / "setup.lock"
        with run_hook.setup_lock(lock, time.monotonic() + 2):
            with self.assertRaisesRegex(run_hook.policy.CheckFailure, "timed out"):
                with run_hook.setup_lock(lock, time.monotonic() + 0.1):
                    self.fail("A second setup acquired the same lock")
        with run_hook.setup_lock(lock, time.monotonic() + 2):
            pass

    def test_setup_timeout_stops_descendant_writes_before_retry(self):
        marker = self.root / "late-installer-write"
        child = (
            "import pathlib, time; time.sleep(0.7); "
            f"pathlib.Path({str(marker)!r}).write_text('unexpected')"
        )
        parent = (
            "import subprocess, sys, time; "
            f"subprocess.Popen([sys.executable, '-c', {child!r}]); time.sleep(10)"
        )
        with self.assertRaisesRegex(run_hook.policy.CheckFailure, "timed out"):
            run_hook.setup_command(
                [sys.executable, "-c", parent],
                self.root,
                time.monotonic() + 0.2,
                "controlled timeout",
            )
        time.sleep(0.8)
        self.assertFalse(marker.exists())

    def test_post_cannot_bootstrap_and_malformed_pre_fails_closed(self):
        self.assertEqual(self.invoke("post").returncode, 2)
        self.assertFalse((self.root / ".tools").exists())
        result = self.invoke("pre", ["invalid"], host="vscode")
        self.assertEqual(
            json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"],
            "deny",
        )

@unittest.skipUnless(os.name == "nt", "Requires native Windows executables and PowerShell")
class WindowsHookBootstrapTests(unittest.TestCase):
    def test_configured_launcher_bootstrap_recovery_and_denial(self):
        with tempfile.TemporaryDirectory(prefix="hook-windows-") as directory:
            root = Path(directory) / "repo with spaces"
            (root / "hooks").mkdir(parents=True)
            (root / "tools").mkdir()
            for relative in ("hooks/run_hook.py", "hooks/agent_hooks.py", "tools/install_hook_tools.py", "requirements-dev.txt", ".gitleaks.toml"):
                shutil.copyfile(ROOT / relative, root / relative)
            configuration = json.loads((ROOT / ".github/hooks/agent-checks.json").read_text())
            commands = configuration["hooks"]
            # Execute the shipped PowerShell command with no python command on PATH.
            launcher = shutil.which("py")
            self.assertIsNotNone(launcher, "Windows CI must provide the Python launcher")
            path = root / "launcher-only"
            path.mkdir()
            shutil.copyfile(launcher, path / "py.exe")
            environment = {**os.environ, "PATH": str(path)}
            shell = str(Path(os.environ["SystemRoot"]) / "System32/WindowsPowerShell/v1.0/powershell.exe")

            def invoke(event, payload):
                return subprocess.run(
                    [shell, "-NoProfile", "-NonInteractive", "-Command", commands[event][0]["powershell"]],
                    cwd=root, env=environment, input=json.dumps(payload), capture_output=True,
                    text=True, timeout=180, check=False,
                )

            started = invoke("sessionStart", {})
            self.assertEqual(started.returncode, 0, started.stderr)
            clean = invoke("preToolUse", {"toolName": "view", "toolArgs": {"path": "README.md"}})
            self.assertEqual(json.loads(clean.stdout), {})
            receipt = root / ".tools/hook-environment.sha256"
            receipt.write_bytes(b"\xff\xfe")
            denied = invoke("preToolUse", {"tool_name": "Read", "tool_input": {"path": "README.md"}})
            self.assertEqual(json.loads(denied.stdout)["hookSpecificOutput"]["permissionDecision"], "deny")
            self.assertIn("py -3", denied.stderr)
            repaired = invoke("sessionStart", {})
            self.assertEqual(repaired.returncode, 0, repaired.stderr)
            scanner = root / ".tools/bin/gitleaks.exe"
            scanner.write_bytes(b"invalid executable, must never launch")
            denied = invoke("preToolUse", {"toolName": "view", "toolArgs": {"path": "README.md"}})
            self.assertEqual(json.loads(denied.stdout)["permissionDecision"], "deny")


if __name__ == "__main__":
    unittest.main()
