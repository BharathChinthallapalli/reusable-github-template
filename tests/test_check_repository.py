"""Behavioral checks for baseline regressions using isolated repository copies."""

import json
from pathlib import Path
import shutil
import tempfile
import unittest

from tools.check_repository import check


SOURCE = Path(__file__).resolve().parents[1]


class RepositoryCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        shutil.copytree(SOURCE, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv"))

    def test_current_foundation_passes(self):
        errors, _ = check(self.root)
        self.assertEqual(errors, [])

    def test_missing_file_fails(self):
        (self.root / "SECURITY.md").unlink()
        errors, _ = check(self.root)
        self.assertTrue(any("SECURITY.md" in error for error in errors))

    def test_mutable_action_reference_fails(self):
        workflow = self.root / ".github/workflows/ci.yml"
        source = workflow.read_text(encoding="utf-8")
        import re
        source = re.sub(r"(actions/checkout@)[a-f0-9]{40}", r"\g<1>main", source)
        workflow.write_text(source, encoding="utf-8")
        errors, _ = check(self.root)
        self.assertTrue(any("full commit SHA" in error for error in errors))

    def test_mismatched_required_check_fails(self):
        path = self.root / ".github/rulesets/main.json"
        path.write_text(path.read_text(encoding="utf-8").replace("Repository checks", "Retired check"), encoding="utf-8")
        errors, _ = check(self.root)
        self.assertTrue(any("required check" in error for error in errors))

    def test_broken_document_link_fails(self):
        path = self.root / "docs/project.md"
        path.write_text(path.read_text(encoding="utf-8") + "\n[Runbook](missing-runbook.md)\n", encoding="utf-8")
        errors, _ = check(self.root)
        self.assertTrue(any("broken local link" in error for error in errors))

    def test_broken_ai_reference_fails(self):
        for relative in (".github/agents/probe.agent.md", ".github/skills/probe/SKILL.md",
                         ".agents/skills/probe/SKILL.md", "CLAUDE.md"):
            with self.subTest(path=relative):
                path = self.root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                original = path.read_bytes() if path.exists() else None
                path.write_text("[Required procedure](missing-procedure.md)\n", encoding="utf-8")
                errors, _ = check(self.root)
                self.assertTrue(any(relative in error and "broken local link" in error for error in errors))
                if original is None:
                    path.unlink()
                else:
                    path.write_bytes(original)

    def test_initialized_markers_fail(self):
        path = self.root / "template.json"
        config = json.loads(path.read_text(encoding="utf-8"))
        config["initialized"] = True
        config["project"]["name"] = "@@PROJECT_NAME@@"
        path.write_text(json.dumps(config), encoding="utf-8")
        errors, _ = check(self.root)
        self.assertTrue(any("unresolved markers" in error for error in errors))

    def test_invalid_project_shape_returns_a_clear_error(self):
        path = self.root / "template.json"
        config = json.loads(path.read_text(encoding="utf-8"))
        config["initialized"] = True
        config["project"] = []
        path.write_text(json.dumps(config), encoding="utf-8")
        errors, _ = check(self.root)
        self.assertTrue(any("project must be an object" in error for error in errors))

    def test_initialized_commented_ownership_fails(self):
        path = self.root / "template.json"
        config = json.loads(path.read_text(encoding="utf-8"))
        config["initialized"] = True
        config["project"]["codeowner"] = "@example-owner"
        path.write_text(json.dumps(config), encoding="utf-8")
        (self.root / ".github/CODEOWNERS").write_text("# * @example-owner\n", encoding="utf-8")
        errors, _ = check(self.root)
        self.assertTrue(any("missing active default entry" in error for error in errors))

    def test_invalid_tool_python_fails(self):
        (self.root / "tools/broken.py").write_text("def broken(:\n", encoding="utf-8")
        errors, _ = check(self.root)
        self.assertTrue(any("tools/broken.py" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
