"""Exercise the design gate through repository files and its command line."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml

from tools.check_design import seal


SCRIPT = Path(__file__).resolve().parents[1] / "tools/check_design.py"
SECTIONS = {
    "Purpose": "Make repository agents respect the task's design before editing.",
    "Scope and non-goals": "Change the review agent; application permissions stay project-owned.",
    "Inputs and outputs": "Read task context and emit a review with concrete file evidence.",
    "Capabilities and permissions": "Use the running host's existing read permissions.",
    "Behavior and failure modes": "Report missing evidence without claiming a successful review.",
    "Validation": "Exercise a covered edit and reject an uncovered protected path.",
    "Risks and alternatives": "Instructions remain editable and require ordinary code review.",
}


class DesignGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.scope = [".github/agents/reviewer.agent.md"]
        self.document = "docs/add/0001-review-agent.md"
        self.write("docs/adr/0001-agents.md", "# Agents\n\nStatus: Accepted\n")
        self.write(self.scope[0], "Review the requested change using repository evidence.\n")
        self.write_design()

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def write_design(self, status="ready", scope=None, adrs=None, sections=None,
                     relative=None, design_id="ADD-0001"):
        metadata = {"schema_version": 1, "id": design_id, "status": status,
                    "scope": self.scope if scope is None else scope,
                    "adrs": ["docs/adr/0001-agents.md"] if adrs is None else adrs,
                    "binding_sha256": ""}
        body = "# Review agent design\n\n" + "\n\n".join(
            f"## {name}\n\n{value}" for name, value in
            (SECTIONS if sections is None else sections).items()) + "\n"
        return self.write(relative or self.document,
                          "---\n" + yaml.safe_dump(metadata, sort_keys=False) + "---\n" + body)

    def run_gate(self, *arguments):
        return subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root),
                               *arguments], capture_output=True, text=True, check=False)

    def seal(self, document=None):
        result = self.run_gate("--seal", document or self.document)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_ready_design_covers_edit_and_sealed_snapshot_passes(self):
        planning = self.run_gate("--paths", self.scope[0])
        self.assertEqual(planning.returncode, 0, planning.stderr)
        self.seal()
        delivered = self.run_gate()
        self.assertEqual(delivered.returncode, 0, delivered.stderr)

    def test_content_drift_blocks_delivery_but_allows_in_progress_edit(self):
        self.seal()
        self.write(self.scope[0], "Request evidence and report unresolved findings.\n")
        self.assertEqual(self.run_gate("--paths", self.scope[0]).returncode, 0)
        result = self.run_gate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("binding does not match", result.stderr)
        self.seal()
        self.assertEqual(self.run_gate().returncode, 0)

    def test_design_prose_drift_also_requires_resealing(self):
        self.seal()
        path = self.root / self.document
        path.write_text(path.read_text().replace("Make repository", "Require repository"))
        self.assertIn("binding does not match", self.run_gate().stderr)

    def test_accepted_decision_content_drift_also_requires_resealing(self):
        self.seal()
        self.write("docs/adr/0001-agents.md", "# Agents\n\nStatus: Accepted\n\nRetain evidence for every claim.\n")
        result = self.run_gate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("binding does not match", result.stderr)
        self.assertEqual(self.run_gate("--paths", self.scope[0]).returncode, 0)

    def test_new_protected_path_requires_explicit_coverage_before_creation(self):
        future = ".github/agents/new.agent.md"
        result = self.run_gate("--paths", future)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no ready ADD covers", result.stderr)
        self.write_design(scope=self.scope + [future])
        self.assertEqual(self.run_gate("--paths", future).returncode, 0)
        self.seal()
        self.write(future, "Explain the requested design.\n")
        self.assertIn("binding does not match", self.run_gate().stderr)

    def test_full_check_discovers_uncovered_skill_assets(self):
        self.seal()
        self.write(".agents/skills/review/assets/cases.json", "{}\n")
        self.assertIn("no ready ADD covers", self.run_gate().stderr)

    def test_imported_hook_bytecode_does_not_invalidate_the_delivery_gate(self):
        self.write("hooks/sample.py", "VALUE = 1\n")
        self.write_design(scope=self.scope + ["hooks/sample.py"])
        self.seal()
        imported = subprocess.run(
            [sys.executable, "-c", "import sys\nsys.dont_write_bytecode = False\nimport hooks.sample\n"],
            cwd=self.root, capture_output=True, text=True, check=False)
        self.assertEqual(imported.returncode, 0, imported.stderr)
        self.assertTrue(list((self.root / "hooks/__pycache__").glob("*.pyc")))
        self.write("hooks/__pycache__/sample.pyo", "generated optimized bytecode fixture")
        result = self.run_gate()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.seal()
        self.assertEqual(self.run_gate().returncode, 0)

    def test_cache_folder_does_not_hide_source_or_bytecode_symlinks(self):
        self.seal()
        for relative in ("hooks/__pycache__/hidden.py", "hooks/standalone.pyc"):
            with self.subTest(relative=relative):
                path = self.write(relative, "unplanned implementation")
                result = self.run_gate()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("no ready ADD covers", result.stderr)
                path.unlink()
        link = self.root / "hooks/__pycache__/hidden.pyc"
        link.symlink_to(self.root / self.scope[0])
        result = self.run_gate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symlink", result.stderr)

    def test_deleted_bound_path_has_a_distinct_sealable_state(self):
        self.seal()
        (self.root / self.scope[0]).unlink()
        self.assertIn("binding does not match", self.run_gate().stderr)
        self.seal()
        self.assertEqual(self.run_gate().returncode, 0)

    def test_draft_and_retired_designs_never_cover_edits(self):
        for status in ("draft", "retired"):
            with self.subTest(status=status):
                self.write_design(status=status)
                self.seal()
                source = (self.root / self.document).read_text()
                self.assertIn(f"status: {status}", source)
                self.assertIn("no ready ADD covers", self.run_gate("--paths", self.scope[0]).stderr)

    def test_ready_sections_must_be_filled_and_placeholders_do_not_count(self):
        for content in ("", "TODO", "[Describe the failure behavior.]", "<!-- filled later -->",
                        "~~~text\npytest tests/\n~~~", "    pytest tests/", "```sh\npytest tests/\n```"):
            with self.subTest(content=content):
                self.write_design(sections=SECTIONS | {"Validation": content})
                result = self.run_gate("--paths", self.scope[0])
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Validation", result.stderr)

    def test_ready_design_requires_current_accepted_decision(self):
        for status in ("Proposed", "Superseded", "Rejected"):
            with self.subTest(status=status):
                self.write("docs/adr/0001-agents.md", f"# Agents\n\nStatus: {status}\n")
                self.assertIn("Accepted ADR", self.run_gate("--paths", self.scope[0]).stderr)
        self.write_design(adrs=["docs/adr/missing.md"])
        self.assertIn("ADR", self.run_gate("--paths", self.scope[0]).stderr)

    def test_scope_rejects_globs_traversal_directories_and_symlinks(self):
        for path in (".github/**", "../outside", "/tmp/outside", ".github/agents", "C:\\outside"):
            with self.subTest(path=path):
                self.write_design(scope=[path])
                self.assertNotEqual(self.run_gate("--seal", self.document).returncode, 0)
        self.write_design(scope=[".github/agents/link.md"])
        (self.root / ".github/agents/link.md").symlink_to(self.root / self.scope[0])
        self.assertIn("symlink", self.run_gate("--seal", self.document).stderr)

    def test_unsafe_selected_path_is_rejected_and_routine_path_needs_no_add(self):
        self.assertNotEqual(self.run_gate("--paths", "../escape").returncode, 0)
        self.assertEqual(self.run_gate("--paths", "src/application.py").returncode, 0)

    def test_duplicate_ready_scope_and_ids_are_reported(self):
        self.write_design(relative="docs/add/0002-other.md", design_id="ADD-0002")
        self.assertIn("multiple ready ADDs", self.run_gate("--paths", self.scope[0]).stderr)
        self.write_design(relative="docs/add/0002-other.md")
        self.assertIn("duplicate ADD id", self.run_gate("--paths", self.scope[0]).stderr)

    def test_invalid_yaml_or_failed_seal_never_overwrites_document(self):
        for source in ("---\nid: one\nid: two\n---\n# Design\n", "---\n[]\n---\n", "no frontmatter"):
            with self.subTest(source=source):
                path = self.write(self.document, source)
                result = self.run_gate("--seal", self.document)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(path.read_text(), source)

    def test_digest_is_stable_across_text_checkout_line_endings(self):
        self.seal()
        path = self.root / self.scope[0]
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        self.assertEqual(self.run_gate().returncode, 0)

    def test_failed_atomic_replacement_preserves_the_original_record(self):
        path = self.root / self.document
        original = path.read_bytes()
        with patch("tools.check_design.Path.replace", side_effect=OSError("simulated write failure")):
            with self.assertRaisesRegex(OSError, "simulated write failure"):
                seal(self.root, self.document)
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual(list(path.parent.iterdir()), [path])


if __name__ == "__main__":
    unittest.main()
