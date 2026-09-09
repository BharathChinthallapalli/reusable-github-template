"""Exercise catalog freshness, deterministic rendering, and safe CLI writes."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml


SCRIPT = Path(__file__).resolve().parents[1] / "tools/ai_catalog.py"


class AICatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / "docs/ai-catalog.md"

    def definition(self, relative, metadata):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("---\n" + yaml.safe_dump(metadata) + "---\nUse repository evidence.\n",
                        encoding="utf-8")
        return path

    def skill(self, name="inspect", description="Inspect repository evidence."):
        return self.definition(f".agents/skills/{name}/SKILL.md",
                               {"name": name, "description": description})

    def run_catalog(self, *arguments):
        return subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), *arguments],
                              cwd=self.root, capture_output=True, text=True, check=False)

    def write_catalog(self):
        result = self.run_catalog("--write")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return self.output.read_text(encoding="utf-8")

    def test_missing_catalog_fails_without_creating_files(self):
        self.skill()
        result = self.run_catalog()
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing", result.stderr.lower())
        self.assertFalse(self.output.exists())

    def test_rendered_catalog_contains_actual_configuration_and_static_limits(self):
        self.skill()
        self.definition(".github/skills/legacy/SKILL.md",
                        {"name": "legacy", "description": "Inspect a legacy skill."})
        self.definition(".github/agents/Read only.agent.md",
                        {"description": "Review the actual diff.", "tools": "read, search",
                         "user-invocable": False, "disable-model-invocation": True})
        self.definition(".github/agents/defaults.agent.md", {"description": "Use host defaults."})
        text = self.write_catalog()
        self.assertIn("../.agents/skills/inspect/SKILL.md", text)
        self.assertIn("../.github/skills/legacy/SKILL.md", text)
        self.assertIn("../.github/agents/Read%20only.agent.md", text)
        self.assertIn("Review the actual diff.", text)
        self.assertIn("read, search", text)
        self.assertIn("false (declared)", text)
        self.assertIn("true (default)", text)
        self.assertIn("Not declared; host defaults apply", text)
        self.assertIn("Host discovery and invocation are not checked", text)
        before = (self.output.read_bytes(), self.output.stat().st_mtime_ns)
        result = self.run_catalog()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.output.read_bytes(), self.output.stat().st_mtime_ns), before)

    def test_added_skill_changed_description_and_deleted_definition_make_catalog_stale(self):
        self.skill()
        self.write_catalog()
        second = self.skill("trace")
        self.assertEqual(self.run_catalog().returncode, 1)
        self.write_catalog()
        self.skill(description="Inspect changed behavior.")
        self.assertEqual(self.run_catalog().returncode, 1)
        self.write_catalog()
        second.unlink()
        second.parent.rmdir()
        result = self.run_catalog()
        self.assertEqual(result.returncode, 1)
        self.assertIn("stale", result.stderr.lower())
        text = self.write_catalog()
        self.assertNotIn("skills/trace/", text)

    def test_regeneration_is_deterministic_across_creation_order(self):
        zulu = self.skill("zulu")
        alpha = self.skill("alpha")
        expected = self.write_catalog()
        zulu.unlink()
        alpha.unlink()
        self.skill("alpha")
        self.skill("zulu")
        self.assertEqual(self.write_catalog(), expected)

    def test_invalid_metadata_preserves_existing_catalog(self):
        skill = self.skill()
        self.write_catalog()
        before = (self.output.read_bytes(), self.output.stat().st_mtime_ns)
        skill.write_text("---\nname: [\n---\n", encoding="utf-8")
        result = self.run_catalog("--write")
        self.assertEqual(result.returncode, 1)
        self.assertIn("SKILL.md", result.stderr)
        self.assertEqual((self.output.read_bytes(), self.output.stat().st_mtime_ns), before)

    def test_duplicate_skill_roots_do_not_create_catalog(self):
        self.skill()
        self.definition(".github/skills/inspect/SKILL.md",
                        {"name": "inspect", "description": "Duplicated skill."})
        result = self.run_catalog("--write")
        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate skill name", result.stderr)
        self.assertFalse(self.output.exists())

    def test_metadata_cannot_inject_table_rows_links_or_html(self):
        self.skill(description="Review | safety\n\n[remote](https://example.com) <script>bad</script> `code` \\")
        self.definition(".github/agents/unusual (draft).agent.md",
                        {"name": "[injected](https://example.com) | name\nnext",
                         "description": "Useful <b>description</b>.", "tools": ["read|write\nnext"]})
        text = self.write_catalog()
        self.assertIn("Review &#124; safety", text)
        self.assertIn(r"\[remote\](https://example.com)", text)
        self.assertIn("&lt;script&gt;", text)
        self.assertNotIn("<script>", text)
        self.assertNotIn("\nnext", text)
        self.assertIn("../.github/agents/unusual%20%28draft%29.agent.md", text)
        for line in text.splitlines():
            if line.startswith("| "):
                self.assertIn(line.count("|"), (5, 6))

    def test_external_catalog_symlink_is_not_read_or_written(self):
        self.skill()
        with tempfile.TemporaryDirectory() as external:
            outside = Path(external) / "catalog.md"
            outside.write_text("PRIVATE-MARKER", encoding="utf-8")
            self.output.parent.mkdir()
            self.output.symlink_to(outside)
            for arguments in ((), ("--write",)):
                result = self.run_catalog(*arguments)
                self.assertEqual(result.returncode, 1)
                self.assertNotIn("PRIVATE-MARKER", result.stdout + result.stderr)
                self.assertIn("outside selected root", result.stderr)
                self.assertEqual(outside.read_text(encoding="utf-8"), "PRIVATE-MARKER")

    def test_external_docs_directory_is_not_created_or_written(self):
        self.skill()
        with tempfile.TemporaryDirectory() as external:
            outside = Path(external)
            self.output.parent.symlink_to(outside, target_is_directory=True)
            result = self.run_catalog("--write")
            self.assertEqual(result.returncode, 1)
            self.assertIn("outside selected root", result.stderr)
            self.assertFalse((outside / "ai-catalog.md").exists())

    def test_invalid_root_returns_nonzero_without_traceback(self):
        self.root = self.root / "missing"
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), "--write"],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Invalid root", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
