"""Exercise the shipped pre-commit configuration through disposable Git repos.

Run explicitly with ``python -m unittest discover -s tests/integration -v``.
The first setup may download the pinned hook environment; later cases share
the normal pre-commit cache. No hook source is imported or mocked.
"""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
COMMAND_TIMEOUT_SECONDS = 120
ONE_MIB = 1024 * 1024


def isolated_environment() -> dict[str, str]:
    """Ignore ambient Git overrides without changing the user's configuration."""
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }
    environment.update(
        GIT_CONFIG_NOSYSTEM="1",
        GIT_CONFIG_GLOBAL=os.devnull,
        GIT_TERMINAL_PROMPT="0",
    )
    environment.pop("SKIP", None)
    environment.pop("PRE_COMMIT_ALLOW_NO_CONFIG", None)
    return environment


def command(
    directory: Path, environment: dict[str, str], *arguments: str
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            arguments,
            cwd=directory,
            env=environment,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise AssertionError(
            f"Command exceeded {COMMAND_TIMEOUT_SECONDS}s in {directory}: "
            f"{arguments!r}\nstdout: {error.stdout!r}\nstderr: {error.stderr!r}"
        ) from error


def require_success(result: subprocess.CompletedProcess[str]) -> None:
    if result.returncode:
        raise AssertionError(
            f"Command failed ({result.returncode}): {result.args!r}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


def prepare_repository(directory: Path, environment: dict[str, str]) -> None:
    directory.mkdir(parents=True)
    require_success(
        command(directory, environment, "git", "-c", "init.templateDir=", "init", "--initial-branch=main")
    )
    for name, value in (
        ("user.name", "Template Integration"),
        ("user.email", "template-integration@example.invalid"),
        ("commit.gpgsign", "false"),
        ("core.autocrlf", "false"),
    ):
        require_success(command(directory, environment, "git", "config", "--local", name, value))
    for filename in (".pre-commit-config.yaml", ".gitignore"):
        shutil.copyfile(ROOT / filename, directory / filename)
    (directory / "README.md").write_text("Disposable hook integration fixture.\n")
    require_success(command(directory, environment, "git", "add", "--all"))
    require_success(command(directory, environment, "git", "commit", "-m", "Fixture baseline"))


def synthetic_private_key_marker() -> str:
    # Assemble a recognisable marker without embedding a key header in source.
    return "-----" + "BEGIN " + "PRIVATE KEY" + "-----\nsynthetic fixture only\n"


class GitHookIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.environment = isolated_environment()
        require_success(command(ROOT, cls.environment, "git", "--version"))
        require_success(command(ROOT, cls.environment, sys.executable, "-m", "pre_commit", "--version"))
        cls.temporary = tempfile.TemporaryDirectory(prefix="template-hook-integration-")
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.workspace = Path(cls.temporary.name)
        warmup = cls.workspace / "warmup"
        prepare_repository(warmup, cls.environment)
        require_success(
            command(
                warmup, cls.environment, sys.executable, "-m", "pre_commit",
                "install", "--install-hooks",
            )
        )
        # A green warmup proves dependency/setup failures are not policy results.
        require_success(
            command(warmup, cls.environment, sys.executable, "-m", "pre_commit", "run", "--all-files")
        )

    def setUp(self) -> None:
        self.repository = self.workspace / self.id().rsplit(".", 1)[-1]
        prepare_repository(self.repository, self.environment)
        self.pre_commit("install", succeeds=True)

    def git(self, *arguments: str, succeeds: bool = True) -> subprocess.CompletedProcess[str]:
        result = command(self.repository, self.environment, "git", *arguments)
        if succeeds:
            require_success(result)
        return result

    def pre_commit(self, *arguments: str, succeeds: bool = False) -> subprocess.CompletedProcess[str]:
        result = command(self.repository, self.environment, sys.executable, "-m", "pre_commit", *arguments)
        if succeeds:
            require_success(result)
        return result

    def write(self, filename: str, content: str | bytes) -> Path:
        path = self.repository / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode("utf-8") if isinstance(content, str) else content)
        return path

    def stage(self, *filenames: str) -> None:
        self.git("add", "-f", "--", *filenames)

    def commit_rejected(self, *hook_ids: str) -> None:
        before = self.git("rev-parse", "HEAD").stdout
        result = self.git("commit", "-m", "Rejected synthetic fixture", succeeds=False)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        output = result.stdout + result.stderr
        for hook_id in hook_ids:
            self.assertIn(f"- hook id: {hook_id}", output)
        self.assertEqual(self.git("rev-parse", "HEAD").stdout, before)

    def unstage_and_remove(self, filename: str) -> None:
        self.git("reset", "HEAD", "--", filename)
        (self.repository / filename).unlink()

    def test_forced_environment_files_are_rejected_including_paths_with_spaces(self) -> None:
        for filename in (".env", "deployment notes/.env.local", "config/.env.example.backup"):
            self.write(filename, "APP_MODE=synthetic\n")
        self.stage(".env", "deployment notes/.env.local", "config/.env.example.backup")
        self.commit_rejected("protect-env-files")

    def test_sanitized_environment_examples_are_accepted(self) -> None:
        for filename in (".env.example", "config/.env.production.example"):
            self.write(filename, "APP_MODE=replace-with-local-value\n")
        self.stage(".env.example", "config/.env.production.example")
        self.git("commit", "-m", "Add sanitized configuration examples")
        self.assertIn("config/.env.production.example", self.git("ls-files").stdout)

    def test_environment_symlinks_and_broken_symlinks_are_rejected(self) -> None:
        link = self.repository / ".env"
        try:
            link.symlink_to("README.md")
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"This platform cannot create test symlinks: {error}")
        self.stage(".env")
        self.commit_rejected("protect-env-files")
        self.unstage_and_remove(".env")
        (self.repository / "broken-link").symlink_to("missing-fixture-target")
        self.stage("broken-link")
        self.commit_rejected("check-symlinks")

    @unittest.skipIf(os.name == "nt", "Requires case-sensitive POSIX symlink filenames")
    def test_symlink_case_collision_is_rejected_locally_and_in_a_clean_clone(self) -> None:
        upper = self.repository / "CaseLink"
        lower = self.repository / "caselink"
        try:
            upper.symlink_to("README.md")
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"This platform cannot create test symlinks: {error}")
        if lower.exists():
            self.skipTest("This filesystem treats the two case variants as the same filename")
        lower.symlink_to("README.md")
        self.stage("CaseLink", "caselink")
        self.commit_rejected("check-case-conflict")
        self.git("commit", "--no-verify", "-m", "Bypass local case-collision check")
        clone = self.workspace / "case-collision-clone"
        require_success(command(self.workspace, self.environment, "git", "clone", str(self.repository), str(clone)))
        result = command(clone, self.environment, sys.executable, "-m", "pre_commit", "run", "--all-files")
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("- hook id: check-case-conflict", result.stdout + result.stderr)

    def test_malformed_json_yaml_and_toml_are_rejected(self) -> None:
        cases = (
            ("fixture.json", '{"value":', "check-json"),
            ("fixture.yaml", "value: [unterminated\n", "check-yaml"),
            ("fixture.toml", "value = [unterminated\n", "check-toml"),
        )
        for filename, content, hook_id in cases:
            with self.subTest(format=filename):
                self.write(filename, content)
                self.stage(filename)
                self.commit_rejected(hook_id)
                self.unstage_and_remove(filename)

    def test_conflict_markers_are_rejected_outside_a_merge(self) -> None:
        self.assertNotEqual(
            self.git("rev-parse", "--verify", "MERGE_HEAD", succeeds=False).returncode, 0
        )
        self.write("conflict.txt", "<<<<<<< branch-a\nfirst\n=======\nsecond\n>>>>>>> branch-b\n")
        self.stage("conflict.txt")
        self.commit_rejected("check-merge-conflict")

    def test_synthetic_private_key_marker_is_rejected(self) -> None:
        self.write("synthetic-key.txt", synthetic_private_key_marker())
        self.stage("synthetic-key.txt")
        self.commit_rejected("detect-private-key")

    def test_modified_tracked_file_accepts_one_mib_and_rejects_one_byte_more(self) -> None:
        self.write("asset.dat", b"small fixture\n")
        self.stage("asset.dat")
        self.git("commit", "-m", "Track size-boundary fixture")
        self.write("asset.dat", b"x" * ONE_MIB)
        self.stage("asset.dat")
        self.git("commit", "-m", "Accept exact size boundary")
        self.write("asset.dat", b"x" * (ONE_MIB + 1))
        self.stage("asset.dat")
        self.commit_rejected("check-added-large-files")

    def test_lfs_attribute_exempts_size_without_proving_lfs_storage(self) -> None:
        # This records the hook's exemption; no LFS clean filter is installed.
        self.write(".gitattributes", "weights.dat filter=lfs\n")
        self.write("weights.dat", b"x" * (ONE_MIB + 1))
        self.stage(".gitattributes", "weights.dat")
        self.git("commit", "-m", "Document the LFS attribute size exemption")
        self.assertEqual(
            int(self.git("cat-file", "-s", "HEAD:weights.dat").stdout), ONE_MIB + 1
        )

    def test_option_like_filename_does_not_hide_other_content_violations(self) -> None:
        self.write("--help", "Ordinary filename, not a command-line option.\n")
        self.write("conflict.txt", "<<<<<<< left\nfirst\n=======\nsecond\n>>>>>>> right\n")
        self.write("synthetic-key.txt", synthetic_private_key_marker())
        self.stage("--help", "conflict.txt", "synthetic-key.txt")
        self.commit_rejected("check-merge-conflict", "detect-private-key")
        self.unstage_and_remove("conflict.txt")
        self.unstage_and_remove("synthetic-key.txt")
        self.git("commit", "-m", "Accept ordinary option-like filename")

    @unittest.skipIf(os.name == "nt", "Windows cannot create a filename containing a newline")
    def test_control_character_filename_is_rejected(self) -> None:
        filename = "notes\nsecond-line.txt"
        self.write(filename, "synthetic fixture\n")
        self.stage(filename)
        self.commit_rejected("check-illegal-windows-names")

    def test_invalid_index_cannot_be_hidden_by_a_repaired_worktree(self) -> None:
        self.write("fixture.json", '{"value": "baseline"}\n')
        self.stage("fixture.json")
        self.git("commit", "-m", "Track partial-staging fixture")
        invalid = b'{"value":'
        repaired = b'{"value": "repaired but unstaged"}\n'
        self.write("fixture.json", invalid)
        self.stage("fixture.json")
        self.write("fixture.json", repaired)
        self.commit_rejected("check-json")
        self.assertEqual((self.repository / "fixture.json").read_bytes(), repaired)
        self.assertEqual(self.git("show", ":fixture.json").stdout.encode(), invalid)

    def test_valid_index_commits_and_restores_an_invalid_unstaged_worktree(self) -> None:
        self.write("fixture.json", '{"value": "baseline"}\n')
        self.stage("fixture.json")
        self.git("commit", "-m", "Track partial-staging fixture")
        staged = b'{"value": "staged update"}\n'
        unstaged = b'{"value": "unfinished'
        self.write("fixture.json", staged)
        self.stage("fixture.json")
        self.write("fixture.json", unstaged)
        self.git("commit", "-m", "Commit only valid staged bytes")
        self.assertEqual(self.git("show", "HEAD:fixture.json").stdout.encode(), staged)
        self.assertEqual(self.git("show", ":fixture.json").stdout.encode(), staged)
        self.assertEqual((self.repository / "fixture.json").read_bytes(), unstaged)

    def test_clean_clone_all_files_check_catches_a_bypassed_local_hook(self) -> None:
        self.write(".env", "APP_MODE=synthetic\n")
        self.stage(".env")
        self.git("commit", "--no-verify", "-m", "Bypass local hook")
        clone = self.workspace / "clean-clone"
        require_success(command(self.workspace, self.environment, "git", "clone", str(self.repository), str(clone)))
        result = command(clone, self.environment, sys.executable, "-m", "pre_commit", "run", "--all-files")
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("- hook id: protect-env-files", result.stdout + result.stderr)
        self.assertEqual(command(clone, self.environment, "git", "status", "--porcelain").stdout, "")

    def test_existing_hook_survives_install_uninstall_and_custom_hooks_path_is_respected(self) -> None:
        self.pre_commit("uninstall", succeeds=True)
        hook = self.repository / ".git/hooks/pre-commit"
        original = b"#!/bin/sh\nprintf 'legacy hook ran\\n' >> .git/legacy-hook-runs\nexit 0\n"
        hook.write_bytes(original)
        hook.chmod(0o755)
        self.pre_commit("install", succeeds=True)
        self.assertNotEqual(hook.read_bytes(), original)
        self.write("README.md", "Exercise the installed hook chain.\n")
        self.stage("README.md")
        self.git("commit", "-m", "Exercise existing hook alongside pre-commit")
        self.assertEqual(
            (self.repository / ".git/legacy-hook-runs").read_bytes(), b"legacy hook ran\n"
        )
        self.pre_commit("uninstall", succeeds=True)
        self.assertEqual(hook.read_bytes(), original)

        custom = self.write("custom-hooks/pre-commit", original)
        self.git("config", "--local", "core.hooksPath", "custom-hooks")
        config_before = (self.repository / ".git/config").read_bytes()
        result = self.pre_commit("install")
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("core.hooksPath", result.stdout + result.stderr)
        self.assertEqual(self.git("config", "--local", "--get", "core.hooksPath").stdout.strip(), "custom-hooks")
        self.assertEqual((self.repository / ".git/config").read_bytes(), config_before)
        self.assertEqual(hook.read_bytes(), original)
        self.assertEqual(custom.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
