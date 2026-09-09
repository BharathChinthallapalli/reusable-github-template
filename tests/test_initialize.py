"""Behavior and safety checks for the repository template initializer."""

from contextlib import redirect_stderr, redirect_stdout
import errno
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).absolute().parents[1] / "tools" / "initialize.py"
SPEC = importlib.util.spec_from_file_location("initialize", SCRIPT)
initialize = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(initialize)


class InitializeTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name) / "template"
        self.root.mkdir()
        self.values = {
            "name": "Policy Assistant",
            "slug": "policy-assistant",
            "owner": "example-org",
            "codeowner": "@example-org/maintainers",
            "security_contact": "mailto:security@example.com",
            "description": "Internal policy Q&A service.",
        }
        self.config = {
            "schema_version": 1,
            "template_version": "1.0.0",
            "initialized": False,
            "project": dict(initialize.TOKENS),
            "customize_files": sorted(initialize.CUSTOMIZE_FILES),
            "license_decision": "unselected",
        }
        self.write_config()
        for relative in self.config["customize_files"]:
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("\n".join(initialize.TOKENS.values()) + "\nKeep this content.\n", encoding="utf-8")
        (self.root / "unrelated.txt").write_text("@@PROJECT_NAME@@ stays unchanged\n", encoding="utf-8")

    def write_config(self):
        (self.root / "template.json").write_text(json.dumps(self.config, indent=2) + "\n", encoding="utf-8")

    def snapshot(self):
        return {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def run_initializer(self, write=False, root=None, **overrides):
        values = {**self.values, **overrides}
        arguments = ["--root", str(self.root if root is None else root)]
        for key, value in values.items():
            arguments.extend(["--" + key.replace("_", "-"), value])
        if write:
            arguments.append("--write")
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = initialize.main(arguments)
        return code, stdout.getvalue(), stderr.getvalue()

    def create_symlink(self, link, target, directory=False):
        try:
            link.symlink_to(target, target_is_directory=directory)
        except OSError as error:
            if error.errno in {errno.EACCES, errno.EPERM} or getattr(error, "winerror", None) == 1314:
                self.skipTest("The operating system denied permission to create a symlink")
            raise

    def test_preview_leaves_every_file_unchanged(self):
        before = self.snapshot()
        code, stdout, stderr = self.run_initializer()
        self.assertEqual(code, 0, stderr)
        self.assertIn("Preview only", stdout)
        self.assertEqual(before, self.snapshot())

    def test_write_expands_only_declared_files_and_serializes_config(self):
        code, _, stderr = self.run_initializer(write=True)
        self.assertEqual(code, 0, stderr)
        for relative in self.config["customize_files"]:
            actual = (self.root / relative).read_text(encoding="utf-8")
            self.assertEqual(actual, "\n".join(self.values.values()) + "\nKeep this content.\n")
        config = json.loads((self.root / "template.json").read_text(encoding="utf-8"))
        self.assertIs(config["initialized"], True)
        self.assertEqual(config["project"], self.values)
        self.assertEqual(config["license_decision"], "unselected")
        self.assertEqual((self.root / "unrelated.txt").read_text(), "@@PROJECT_NAME@@ stays unchanged\n")

    def test_same_inputs_preserve_customized_files_and_modification_times(self):
        self.assertEqual(self.run_initializer(write=True)[0], 0)
        readme = self.root / "README.md"
        readme.write_text("User edits, including @@PROJECT_NAME@@, are preserved.\n", encoding="utf-8")
        before = self.snapshot()
        mtimes = {p: p.stat().st_mtime_ns for p in self.root.rglob("*") if p.is_file()}
        code, stdout, stderr = self.run_initializer(write=True)
        self.assertEqual(code, 0, stderr)
        self.assertIn("no files changed", stdout)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(mtimes, {p: p.stat().st_mtime_ns for p in mtimes})

    def test_codeowners_activates_only_commented_template_owner_lines(self):
        codeowners = self.root / ".github/CODEOWNERS"
        codeowners.write_text(
            "# Repository ownership\n# * @@CODEOWNER@@\n# /.github/ @@CODEOWNER@@\n"
            "# Keep @example-org/other-team commented.\n", encoding="utf-8"
        )
        code, _, stderr = self.run_initializer(write=True)
        self.assertEqual(code, 0, stderr)
        self.assertEqual(codeowners.read_text(encoding="utf-8"),
                         "# Repository ownership\n* @example-org/maintainers\n"
                         "/.github/ @example-org/maintainers\n# Keep @example-org/other-team commented.\n")

    def test_different_reinitialization_is_rejected_without_writes(self):
        self.assertEqual(self.run_initializer(write=True)[0], 0)
        before = self.snapshot()
        code, _, stderr = self.run_initializer(write=True, name="Different Project")
        self.assertEqual(code, 2)
        self.assertIn("already initialized", stderr)
        self.assertEqual(before, self.snapshot())

    def test_missing_target_prevents_all_writes(self):
        (self.root / "SUPPORT.md").unlink()
        before = self.snapshot()
        code, _, stderr = self.run_initializer(write=True)
        self.assertEqual(code, 2)
        self.assertIn("missing", stderr)
        self.assertEqual(before, self.snapshot())

    def test_bad_inputs_prevent_all_writes(self):
        cases = [
            {"name": "Title\n# injected heading"},
            {"name": "Title\u2028injected heading"},
            {"description": "hidden\u202edirection change"},
            {"description": "[unexpected link](https://example.com)"},
            {"description": "@@PROJECT_NAME@@"},
            {"description": "hidden\x00control"},
            {"name": " padded "},
            {"slug": "../outside"},
            {"owner": "bad--owner"},
            {"codeowner": "@example-org/team @another-owner"},
            {"codeowner": "@example-org/team/extra"},
            {"security_contact": "javascript:alert(1)"},
            {"security_contact": "https://example.com/) [link](https://evil.example)"},
            {"security_contact": "https://example.com/%0Ainjected"},
            {"security_contact": "https://user:password@example.com"},
            {"security_contact": "mailto:not-an-email"},
            {"security_contact": "mailto:.bad..name@example.com"},
            {"security_contact": "mailto:security@example.com?subject=example"},
        ]
        before = self.snapshot()
        for values in cases:
            with self.subTest(values=values):
                code, _, stderr = self.run_initializer(write=True, **values)
                self.assertEqual(code, 2)
                self.assertTrue(stderr.startswith("Error:"))
                self.assertEqual(before, self.snapshot())

    def test_plain_punctuation_unicode_and_https_contact_are_supported(self):
        values = {"name": "Équipe's Policy Assistant (EU)", "description": 'Internal Q&A: "policy", support and access.',
                  "security_contact": "https://example.com/security?source=github&team=platform"}
        code, _, stderr = self.run_initializer(write=True, **values)
        self.assertEqual(code, 0, stderr)
        actual = json.loads((self.root / "template.json").read_text(encoding="utf-8"))
        self.assertEqual(actual["project"], {**self.values, **values})

    def test_managed_user_can_own_repository_and_be_codeowner(self):
        code, _, stderr = self.run_initializer(write=True, owner="mona-cat_octo", codeowner="@mona-cat_octo")
        self.assertEqual(code, 0, stderr)
        actual = json.loads((self.root / "template.json").read_text(encoding="utf-8"))
        self.assertEqual(actual["project"]["owner"], "mona-cat_octo")
        self.assertEqual(actual["project"]["codeowner"], "@mona-cat_octo")

    def test_managed_username_limits_and_organization_boundary(self):
        maximum = "a" * 30 + "_abc12345"
        code, _, stderr = self.run_initializer(owner=maximum, codeowner="@" + maximum)
        self.assertEqual(code, 0, stderr)
        before = self.snapshot()
        for values in (
            {"owner": "a" + maximum},
            {"codeowner": "@a" + maximum},
            {"owner": "mona_ab"},
            {"owner": "mona_abcdefghi"},
            {"owner": "mona_abc_def"},
            {"codeowner": "@mona-cat_octo/team"},
        ):
            with self.subTest(values=values):
                code, _, stderr = self.run_initializer(write=True, **values)
                self.assertEqual(code, 2)
                self.assertTrue(stderr.startswith("Error:"))
                self.assertEqual(before, self.snapshot())

    def test_symlink_target_is_rejected_without_touching_destination(self):
        external = Path(self.directory.name) / "external.md"
        external.write_text("External content", encoding="utf-8")
        readme = self.root / "README.md"
        readme.unlink()
        self.create_symlink(readme, external)
        before = self.snapshot()
        code, _, stderr = self.run_initializer(write=True)
        self.assertEqual(code, 2)
        self.assertIn("Symlinks", stderr)
        self.assertEqual(external.read_text(), "External content")
        self.assertEqual(before, self.snapshot())

    def test_symlink_parent_directory_is_rejected(self):
        original = self.root / "docs"
        external = Path(self.directory.name) / "external-docs"
        original.rename(external)
        self.create_symlink(original, external, directory=True)
        before = (external / "project.md").read_bytes()
        code, _, stderr = self.run_initializer(write=True)
        self.assertEqual(code, 2)
        self.assertIn("Symlinks", stderr)
        self.assertEqual(before, (external / "project.md").read_bytes())

    def test_system_ancestor_symlink_allows_preview_and_initialization(self):
        alias = Path(self.directory.name) / "system-parent-alias"
        self.create_symlink(alias, self.root.parent, directory=True)
        aliased_root = alias / self.root.name
        before = self.snapshot()
        code, stdout, stderr = self.run_initializer(root=aliased_root)
        self.assertEqual(code, 0, stderr)
        self.assertIn("  README.md\n", stdout)
        self.assertEqual(before, self.snapshot())
        code, stdout, stderr = self.run_initializer(write=True, root=aliased_root)
        self.assertEqual(code, 0, stderr)
        self.assertIn("  template.json\n", stdout)
        actual = json.loads((self.root / "template.json").read_text(encoding="utf-8"))
        self.assertIs(actual["initialized"], True)

    def test_symlink_at_selected_project_root_is_rejected(self):
        alias = Path(self.directory.name) / "project-alias"
        self.create_symlink(alias, self.root, directory=True)
        before = self.snapshot()
        code, _, stderr = self.run_initializer(write=True, root=alias)
        self.assertEqual(code, 2)
        self.assertIn("root must not itself be a symlink", stderr)
        self.assertEqual(before, self.snapshot())

    def test_traversal_in_configuration_is_rejected_without_writes(self):
        self.config["customize_files"][-1] = "../outside.md"
        self.write_config()
        before = self.snapshot()
        code, _, stderr = self.run_initializer(write=True)
        self.assertEqual(code, 2)
        self.assertIn("Unsafe template path", stderr)
        self.assertEqual(before, self.snapshot())

    def test_malformed_configuration_is_a_friendly_error(self):
        (self.root / "template.json").write_text("{not json", encoding="utf-8")
        before = self.snapshot()
        code, _, stderr = self.run_initializer(write=True)
        self.assertEqual(code, 2)
        self.assertTrue(stderr.startswith("Error:"))
        self.assertNotIn("Traceback", stderr)
        self.assertEqual(before, self.snapshot())


if __name__ == "__main__":
    unittest.main()
