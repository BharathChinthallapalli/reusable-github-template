"""Exercise host contracts through the CLI and controlled scanner processes."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import venv


ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "hooks" / "agent_hooks.py"


@unittest.skipIf(os.name == "nt", "Scanner process fixtures use a POSIX executable")
class AgentHookTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.root = self.directory / "repo"
        self.root.mkdir()
        self.log = self.directory / "scanner.json"
        scanner = self.root / ".tools" / "bin" / "gitleaks"
        scanner.parent.mkdir(parents=True)
        scanner.write_text(
            f"#!{sys.executable}\n"
            "import json, os, pathlib, sys, time\n"
            "args = sys.argv[1:]\n"
            "data = sys.stdin.read() if 'stdin' in args else ''\n"
            "if 'dir' in args:\n"
            "    data = '\\n'.join(p.read_text(errors='replace') "
            "for p in pathlib.Path(args[-1]).rglob('*') if p.is_file())\n"
            "pathlib.Path(os.environ['SCAN_LOG']).write_text("
            "json.dumps({'args':args,'data':data}))\n"
            "mode = os.environ.get('SCAN_MODE', '')\n"
            "if mode == 'timeout': time.sleep(2)\n"
            "print('sensitive-scanner-output', file=sys.stderr)\n"
            "sys.exit(3 if mode == 'error' else "
            "10 if 'HOOK_TEST_SECRET' in data else 0)\n",
            encoding="utf-8",
        )
        scanner.chmod(0o755)
        tools = self.root / "tools"
        tools.mkdir()
        (tools / "check_design.py").write_text(
            "import json, os, pathlib, sys\n"
            "pathlib.Path(os.environ['DESIGN_LOG']).write_text(json.dumps(sys.argv))\n"
            "sys.exit(int(os.environ.get('DESIGN_EXIT', '0')))\n",
            encoding="utf-8",
        )
        environment = self.directory / "python"
        venv.EnvBuilder(with_pip=False, symlinks=True).create(environment)
        self.python = environment / "bin" / "python"
        modules = environment / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
        (modules / "ruff.py").write_text(
            "import json, os, pathlib, sys\n"
            "pathlib.Path(os.environ['RUFF_LOG']).write_text(json.dumps(sys.argv))\n"
            "print('sensitive-linter-output', file=sys.stderr)\n"
            "sys.exit(int(os.environ.get('RUFF_EXIT', '0')))\n",
            encoding="utf-8",
        )
        self.environment = {
            **os.environ,
            "SCAN_LOG": str(self.log),
            "DESIGN_LOG": str(self.directory / "design.json"),
            "RUFF_LOG": str(self.directory / "ruff.json"),
        }

    def invoke(self, payload, event="pre", host=None, timeout=None):
        arguments = [str(self.python), str(HOOK), "--root", str(self.root), "--event", event]
        if host:
            arguments.extend(["--host", host])
        if timeout:
            arguments.extend(["--timeout-seconds", str(timeout)])
        return subprocess.run(
            arguments,
            input=payload if isinstance(payload, str) else json.dumps(payload),
            capture_output=True,
            text=True,
            env=self.environment,
            timeout=5,
            check=False,
        )

    def deny_reason(self, result, github=False):
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        decision = output if github else output["hookSpecificOutput"]
        self.assertEqual(decision["permissionDecision"], "deny")
        self.assertNotIn("sensitive", result.stdout + result.stderr)
        return decision["permissionDecisionReason"]

    def test_clean_github_string_arguments_pass_without_granting_permission(self):
        arguments = {"command": "git status", "nested": {"text": "hello"}}
        result = self.invoke({"toolName": "bash", "toolArgs": json.dumps(arguments)})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {})
        scanned = json.loads(self.log.read_text())
        self.assertEqual(json.loads(scanned["data"]), arguments)
        self.assertIn("--redact=100", scanned["args"])
        self.assertIn("--ignore-gitleaks-allow", scanned["args"])

    def test_secret_in_nested_non_shell_arguments_is_denied_without_echo(self):
        result = self.invoke(
            {"toolName": "custom", "toolArgs": {"nested": [{"value": "HOOK_TEST_SECRET"}]}}
        )
        self.assertIn("secret", self.deny_reason(result, github=True).lower())
        self.assertNotIn("HOOK_TEST_SECRET", result.stdout + result.stderr)

    def test_recognized_destructive_commands_are_denied(self):
        commands = [
            "rm -rf build", "rm --recursive --force build", "r''m -r\\f build",
            "sudo env X=1 /bin/rm -f -R build", "bash -lc 'git reset --hard HEAD'",
            "git -C . clean -xfd", "git push origin +main:main", "git push --force-with-lease",
            "pwsh -Command 'Remove-Item build -Recurse -Force'", "echo hi; git reset --hard",
            "git push -uf origin main", "cmd /c rmdir build /s /q",
            "bash -xec 'rm -rf build'", "env -S 'rm -rf build'",
        ]
        for command in commands:
            with self.subTest(command=command):
                self.deny_reason(self.invoke({"tool_name": "Bash", "tool_input": {"command": command}}))

    def test_credential_file_tools_and_shell_reads_are_denied(self):
        for path in [".env", ".env.production", "~/.ssh/id_ed25519", "~/.aws/credentials", "key.pem"]:
            with self.subTest(path=path):
                self.deny_reason(self.invoke({"toolName": "view", "toolArgs": {"path": path}}), github=True)
                self.deny_reason(self.invoke({"tool_name": "Bash", "tool_input": {"command": "cat " + path}}))

    def test_windows_credential_paths_and_symlinks_are_denied(self):
        (self.root / "harmless").symlink_to(self.root / ".env")
        for command in [r"Get-Content C:\Users\alice\.aws\credentials", "cat harmless"]:
            with self.subTest(command=command):
                self.deny_reason(self.invoke({"tool_name": "Bash", "tool_input": {"command": command}}))

    def test_sanitized_environment_example_is_allowed(self):
        for filename in [".env.example", ".env.local.example"]:
            with self.subTest(filename=filename):
                result = self.invoke({"tool_name": "create_file", "tool_input": {"filePath": filename, "content": "URL=http://localhost"}})
                self.assertEqual(json.loads(result.stdout), {})

    def test_candidate_command_is_never_executed(self):
        marker = self.directory / "executed"
        command = f"touch '{marker}'"
        result = self.invoke({"tool_name": "Bash", "tool_input": {"command": command}})
        self.assertEqual(json.loads(result.stdout), {})
        self.assertFalse(marker.exists())

    def test_invalid_pre_input_is_structured_denial(self):
        for payload in ["{", "[]", "{}", '{"tool_name":"Bash","tool_input":null}']:
            with self.subTest(payload=payload):
                self.deny_reason(self.invoke(payload, host="vscode"))

    def test_invalid_input_without_host_uses_shared_blocking_exit_code(self):
        for payload in ["{", "[]", "{}"]:
            with self.subTest(payload=payload):
                result = self.invoke(payload)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(json.loads(result.stdout), {})

    def test_missing_failing_and_timed_out_scanner_deny(self):
        payload = {"tool_name": "Bash", "tool_input": {"command": "git status"}}
        self.environment["SCAN_MODE"] = "error"
        self.assertIn("failed", self.deny_reason(self.invoke(payload)))
        self.environment["SCAN_MODE"] = "timeout"
        self.assertIn("timed out", self.deny_reason(self.invoke(payload, timeout=0.2)))
        (self.root / ".tools/bin/gitleaks").unlink()
        self.assertIn("unavailable", self.deny_reason(self.invoke(payload)))

    def test_apply_patch_move_paths_reach_design_gate(self):
        patch = "*** Begin Patch\n*** Update File: src/old.py\n*** Move to: src/new.py\n@@\n-old\n+new\n*** End Patch"
        result = self.invoke({"tool_name": "apply_patch", "tool_input": {"command": patch}})
        self.assertEqual(json.loads(result.stdout), {})
        arguments = json.loads((self.directory / "design.json").read_text())
        self.assertIn("src/old.py", arguments)
        self.assertIn("src/new.py", arguments)

    def test_design_failure_blocks_structured_edit_with_safe_reason(self):
        self.environment["DESIGN_EXIT"] = "1"
        result = self.invoke({"tool_name": "replace_string_in_file", "tool_input": {"filePath": "src/app.py", "newString": "safe"}})
        self.assertIn("design", self.deny_reason(result).lower())

    def test_absolute_editor_paths_and_nested_working_directory_reach_design_gate(self):
        for path in [str(self.root / "src" / "app.py"), "app.py"]:
            with self.subTest(path=path):
                result = self.invoke({"cwd": str(self.root / "src"), "tool_name": "create_file", "tool_input": {"filePath": path, "content": "value = 1"}})
                self.assertEqual(json.loads(result.stdout), {})
                arguments = json.loads((self.directory / "design.json").read_text())
                self.assertEqual(arguments[-1], "src/app.py")

    def test_multi_replace_checks_every_file_and_rejects_outside_target(self):
        payload = {"tool_name": "multi_replace_string_in_file", "tool_input": {"replacements": [{"filePath": "src/a.py", "newString": "one"}, {"filePath": "src/b.py", "newString": "two"}]}}
        result = self.invoke(payload)
        self.assertEqual(json.loads(result.stdout), {})
        arguments = json.loads((self.directory / "design.json").read_text())
        self.assertEqual(arguments[-2:], ["src/a.py", "src/b.py"])
        payload["tool_input"]["replacements"][1]["filePath"] = "../outside.py"
        self.assertIn("outside", self.deny_reason(self.invoke(payload)))

    def test_remote_file_uri_and_invalid_path_are_structured_denials(self):
        for path in ["file://remote-host" + str(self.root / "app.py"), "src/invalid\0.py"]:
            with self.subTest(path=path):
                result = self.invoke({"tool_name": "create_file", "tool_input": {"filePath": path, "content": "value = 1"}}, host="vscode")
                self.deny_reason(result)
                self.assertNotIn("Traceback", result.stderr)

    def test_editor_without_known_path_contract_is_denied(self):
        result = self.invoke({"tool_name": "edit", "tool_input": {"opaque": "some edit"}})
        self.assertIn("paths", self.deny_reason(result))

    def test_patch_cannot_hide_a_credential_target(self):
        patch = "*** Begin Patch\n*** Add File: .env\n+URL=local\n*** End Patch"
        result = self.invoke({"tool_name": "apply_patch", "tool_input": {"input": patch}})
        self.assertIn("credential", self.deny_reason(result).lower())

    def test_post_scans_existing_files_and_lints_without_mutating_them(self):
        source = self.root / "app.py"
        source.write_text("value = 1\n")
        result = self.invoke({"tool_name": "Bash", "tool_input": {"command": "echo done"}}, event="post")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {})
        self.assertEqual(source.read_text(), "value = 1\n")
        self.assertIn("value = 1", json.loads(self.log.read_text())["data"])
        ruff = json.loads((self.directory / "ruff.json").read_text())
        self.assertIn("check", ruff)
        self.assertNotIn("--fix", ruff)

    def test_post_secret_and_lint_failure_are_nonzero_and_redacted(self):
        (self.root / "app.py").write_text("# HOOK_TEST_SECRET\n")
        payload = {"toolName": "edit", "toolArgs": {"path": "app.py"}}
        result = self.invoke(payload, event="post")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("secret", json.loads(result.stdout)["additionalContext"].lower())
        self.assertNotIn("HOOK_TEST_SECRET", result.stdout + result.stderr)
        (self.root / "app.py").write_text("value = 1\n")
        self.environment["RUFF_EXIT"] = "1"
        result = self.invoke(payload, event="post")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Ruff", result.stderr)
        self.assertNotIn("sensitive-linter-output", result.stdout + result.stderr)

    def test_post_symlinks_are_rejected_without_reading_external_target(self):
        (self.root / "external.py").symlink_to(self.directory / "outside.py")
        result = self.invoke({"tool_name": "apply_patch", "tool_input": {}}, event="post")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symlink", result.stderr)

    def test_local_ruff_module_cannot_execute_as_the_installed_scanner(self):
        marker = self.directory / "executed"
        (self.root / "ruff.py").write_text(f"from pathlib import Path\nPath({str(marker)!r}).touch()\n")
        self.environment["PYTHONPATH"] = str(self.root)
        result = self.invoke({"tool_name": "apply_patch", "tool_input": {}}, event="post")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(marker.exists())

    def test_check_and_session_modes_verify_dependencies(self):
        (self.root / "app.py").write_text("value = 1\n")
        self.assertEqual(self.invoke("", event="check").returncode, 0)
        self.assertEqual(self.invoke("", event="session").returncode, 0)
        result = self.invoke({"sessionId": "test", "source": "startup"}, event="session", host="github")
        self.assertEqual(result.returncode, 0, result.stderr)
        (self.root / ".tools/bin/gitleaks").unlink()
        result = self.invoke({"sessionId": "test", "source": "startup"}, event="session", host="github")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unavailable", json.loads(result.stdout)["additionalContext"])

    def test_post_non_edit_does_not_claim_a_repository_scan(self):
        result = self.invoke({"tool_name": "read_file", "tool_input": {"path": "README.md"}}, event="post")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), {})
        self.assertFalse(self.log.exists())

    def test_git_post_scans_tracked_and_untracked_but_lints_only_changed_python(self):
        def git(*arguments):
            return subprocess.run(["git", *arguments], cwd=self.root, capture_output=True, check=True)

        git("init", "--quiet")
        (self.root / ".gitignore").write_text(".tools/\nignored.txt\n")
        (self.root / "clean.py").write_text("clean = 1\n")
        (self.root / "changed.py").write_text("changed = 1\n")
        git("add", ".")
        git("-c", "user.name=Hook Tests", "-c", "user.email=hooks@example.invalid", "commit", "--quiet", "-m", "baseline")
        (self.root / "changed.py").write_text("changed = 2\n")
        (self.root / "staged.py").write_text("staged = 1\n")
        git("add", "staged.py")
        (self.root / "new.py").write_text("new = 1\n")
        (self.root / "ignored.txt").write_text("HOOK_TEST_SECRET\n")
        result = self.invoke({"tool_name": "Bash", "tool_input": {"command": "echo edited"}}, event="post")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(self.log.read_text())["data"]
        self.assertIn("clean = 1", data)
        self.assertIn("new = 1", data)
        ruff = json.loads((self.directory / "ruff.json").read_text())
        self.assertNotIn(str(self.root / "clean.py"), ruff)
        for name in ["changed.py", "staged.py", "new.py"]:
            self.assertIn(str(self.root / name), ruff)


if __name__ == "__main__":
    unittest.main()
