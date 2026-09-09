"""Exercise static AI configuration diagnostics through files and the CLI."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools.check_ai_configuration import check


SCRIPT = Path(__file__).resolve().parents[1] / "tools/check_ai_configuration.py"


class AIConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write_definition(self, relative, frontmatter, body="Use repository evidence."):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\n{frontmatter}\n---\n{body}\n", encoding="utf-8")
        return path

    def skill(self, frontmatter="name: inspect\ndescription: Inspect a repository.", folder="inspect"):
        return self.write_definition(f".github/skills/{folder}/SKILL.md", frontmatter)

    def agent(self, frontmatter, filename="review"):
        return self.write_definition(f".github/agents/{filename}.agent.md", frontmatter)

    def assert_invalid(self, expected):
        errors, _ = check(self.root)
        self.assertTrue(any(expected in error for error in errors), errors)

    def test_bom_crlf_multiline_and_custom_tool_names_are_supported(self):
        path = self.skill("name: inspect\ndescription: >-\n  Inspect code\n  and trace callers.")
        path.write_bytes(b"\xef\xbb\xbf" + path.read_bytes().replace(b"\n", b"\r\n"))
        self.agent("name: Domain reviewer\ndescription: |\n  Review domain rules.\n  Check actual callers.\ntools: [read, 'my-server/query']")
        errors, notes = check(self.root)
        self.assertEqual(errors, [])
        self.assertTrue(any('my-server/query' in note for note in notes))
        self.assertTrue(any('model_invocation_eligible=true' in note for note in notes))

    def test_manual_only_hidden_and_empty_tools_are_valid_choices(self):
        self.skill("name: inspect\ndescription: Inspect code.\ndisable-model-invocation: true")
        self.agent("name: reviewer\ndescription: Review code.\ntools: []\nuser-invocable: false")
        errors, notes = check(self.root)
        self.assertEqual(errors, [])
        self.assertTrue(any('model_invocation_eligible=false' in note for note in notes))
        self.assertTrue(any('user_invocable=false' in note and 'tools=[]' in note for note in notes))

    def test_agent_name_defaults_to_filename_and_omitted_tools_are_distinct(self):
        self.agent("description: Review code.")
        errors, notes = check(self.root)
        self.assertEqual(errors, [])
        self.assertTrue(any('name="review"' in note and 'tools=not declared' in note for note in notes))

    def test_plain_markdown_agent_definitions_are_inspected(self):
        path = self.write_definition(".github/agents/helper.md", "description: Help review code.")
        errors, notes = check(self.root)
        self.assertEqual(errors, [])
        self.assertTrue(any('name="helper"' in note for note in notes))
        path.write_text("broken metadata", encoding="utf-8")
        self.assert_invalid(".github/agents/helper.md")

    def test_missing_skill_entrypoint_is_reported(self):
        (self.root / ".github/skills/empty").mkdir(parents=True)
        self.assert_invalid(".github/skills/empty/SKILL.md")

    def test_canonical_skills_are_discovered_and_validated(self):
        path = self.write_definition(".agents/skills/inspect/SKILL.md",
                                     "name: inspect\ndescription: Inspect canonical skills.")
        errors, notes = check(self.root)
        self.assertEqual(errors, [])
        self.assertTrue(any(".agents/skills/inspect/SKILL.md" in note for note in notes))
        path.write_text("missing metadata", encoding="utf-8")
        self.assert_invalid(".agents/skills/inspect/SKILL.md")

    def test_same_skill_in_canonical_and_legacy_roots_is_rejected(self):
        self.skill()
        self.write_definition(".agents/skills/inspect/SKILL.md",
                              "name: inspect\ndescription: Duplicated discovery.")
        errors, _ = check(self.root)
        self.assertTrue(any("duplicate skill name" in error
                            and ".agents/skills/inspect/SKILL.md" in error
                            and ".github/skills/inspect/SKILL.md" in error for error in errors), errors)

    def test_invalid_frontmatter_is_reported_with_file_context(self):
        path = self.skill()
        for content in ("No header", "---\nname: inspect", "---\n---", "---\n[]\n---", "---\nname: [\n---"):
            with self.subTest(content=content):
                path.write_text(content, encoding="utf-8")
                self.assert_invalid(".github/skills/inspect/SKILL.md")

    def test_duplicate_fields_are_rejected_including_nested_mappings(self):
        for metadata in (
            "name: inspect\nname: other\ndescription: Inspect code.",
            "name: inspect\ndescription: Inspect code.\nmetadata:\n  owner: one\n  owner: two",
            "name: inspect\n<<: {description: first, description: second}",
        ):
            with self.subTest(metadata=metadata):
                self.skill(metadata)
                self.assert_invalid("duplicate YAML key")

    def test_yaml_merge_overrides_and_alias_cycles_remain_valid(self):
        self.skill("name: inspect\n<<: {description: Default description.}\ndescription: Specific description.\nextra: &cycle [*cycle]")
        self.assertEqual(check(self.root)[0], [])

    def test_deep_yaml_returns_a_diagnostic_instead_of_crashing(self):
        self.skill("name: inspect\ndescription: Inspect code.\nextra: " + "[" * 1500 + "0" + "]" * 1500)
        self.assert_invalid("YAML")

    def test_invalid_yaml_timestamp_returns_json_failure(self):
        self.skill("name: inspect\ndescription: Inspect code.\nmetadata: {date: 2026-99-99}")
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), "--json"],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1)
        report = json.loads(result.stdout)
        self.assertTrue(any(".github/skills/inspect/SKILL.md" in error for error in report["errors"]))

    def test_unsafe_yaml_tags_cannot_execute_code(self):
        marker = self.root / "executed"
        self.skill(f"name: inspect\ndescription: Inspect code.\nextra: !!python/object/apply:pathlib.Path.touch [!!python/object/apply:pathlib.Path ['{marker.as_posix()}']]")
        self.assert_invalid("YAML")
        self.assertFalse(marker.exists())

    def test_skill_name_grammar_length_and_directory_match(self):
        for name in ("Wrong", "has_space", "-start", "end-", "two--dashes", "a" * 65):
            with self.subTest(name=name):
                self.skill(f"name: {name}\ndescription: Inspect code.")
                self.assert_invalid("name")
        self.skill("name: elsewhere\ndescription: Inspect code.")
        self.assert_invalid("directory")

    def test_empty_or_nonstring_identity_fields_are_rejected(self):
        for field, value in (("name", "null"), ("name", "true"), ("name", "' '"),
                             ("description", "[]"), ("description", "null"), ("description", "' '")):
            with self.subTest(field=field, value=value):
                values = {"name": "inspect", "description": "Inspect code."}
                values[field] = value
                self.skill("\n".join(f"{key}: {item}" for key, item in values.items()))
                self.assert_invalid(field)

    def test_skill_description_accepts_documented_limit_and_rejects_overflow(self):
        self.skill("name: inspect\ndescription: " + "a" * 1024)
        self.assertEqual(check(self.root)[0], [])
        self.skill("name: inspect\ndescription: " + "a" * 1025)
        self.assert_invalid("description must not exceed 1024 characters")

    def test_invocation_flags_require_boolean_values(self):
        for field in ("user-invocable", "disable-model-invocation"):
            for value in ("0", "1", "'false'", "null", "[]"):
                with self.subTest(field=field, value=value):
                    self.skill(f"name: inspect\ndescription: Inspect code.\n{field}: {value}")
                    self.assert_invalid(f"{field} must be a boolean")

    def test_agent_tools_reject_invalid_list_or_string_entries(self):
        for value in ("null", "[read, null]", "['']", "[' ']", "[[read]]", "[false]", "''", "read, ,search"):
            with self.subTest(value=value):
                self.agent(f"name: reviewer\ndescription: Review code.\ntools: {value}")
                self.assert_invalid("tools must contain nonempty strings")

    def test_comma_separated_and_single_tool_strings_are_supported(self):
        for value, expected in (("read", '["read"]'), ("read, my-server/query", '["read", "my-server/query"]')):
            with self.subTest(value=value):
                self.agent(f"name: reviewer\ndescription: Review code.\ntools: {value}")
                errors, notes = check(self.root)
                self.assertEqual(errors, [])
                self.assertTrue(any(f"declared tools={expected}" in note for note in notes))

    def test_legacy_infer_does_not_claim_portable_invocation_behavior(self):
        self.agent("name: reviewer\ndescription: Review code.\ninfer: false")
        errors, notes = check(self.root)
        self.assertEqual(errors, [])
        self.assertTrue(any("legacy invocation eligibility=unverified" in note for note in notes))

    def test_duplicate_names_are_checked_within_each_category(self):
        self.skill()
        self.agent("name: inspect\ndescription: Review code.")
        self.assertEqual(check(self.root)[0], [])
        self.agent("name: inspect\ndescription: Second reviewer.", filename="second")
        self.assert_invalid("duplicate agent name")
        self.skill(folder="second")
        self.assert_invalid("duplicate skill name")

    def test_unreadable_and_invalid_utf8_files_fail_clearly(self):
        path = self.skill()
        with patch.object(Path, "read_text", side_effect=PermissionError("permission denied")):
            self.assert_invalid("could not read")
        path.write_bytes(b"\xff\xfe\x00")
        self.assert_invalid("could not read")

    def test_invalid_roots_and_nondirectory_configuration_are_reported(self):
        missing = self.root / "missing"
        self.assertTrue(check(missing)[0])
        regular = self.root / "file"
        regular.write_text("content", encoding="utf-8")
        self.assertTrue(check(regular)[0])
        (self.root / ".github").write_text("not a directory", encoding="utf-8")
        self.assert_invalid("could not inspect")

    def test_external_definition_symlinks_are_not_read(self):
        with tempfile.TemporaryDirectory() as external:
            outside = Path(external) / "private.agent.md"
            outside.write_text("---\nname: PRIVATE-MARKER\ndescription: External data.\n---", encoding="utf-8")
            link = self.root / ".github/agents/external.agent.md"
            link.parent.mkdir(parents=True)
            link.symlink_to(outside)
            errors, notes = check(self.root)
            self.assertTrue(any("outside selected root" in error for error in errors))
            self.assertNotIn("PRIVATE-MARKER", "\n".join(errors + notes))

    def test_external_discovery_directory_symlink_is_not_traversed(self):
        with tempfile.TemporaryDirectory() as external:
            outside = Path(external)
            (outside / "PRIVATE-MARKER.agent.md").write_text("not metadata", encoding="utf-8")
            link = self.root / ".github/agents"
            link.parent.mkdir()
            link.symlink_to(outside, target_is_directory=True)
            errors, notes = check(self.root)
            self.assertTrue(any("outside selected root" in error for error in errors))
            self.assertNotIn("PRIVATE-MARKER", "\n".join(errors + notes))

    def test_external_canonical_skill_directory_is_not_traversed(self):
        with tempfile.TemporaryDirectory() as external:
            outside = Path(external)
            (outside / "PRIVATE-MARKER").mkdir()
            link = self.root / ".agents/skills"
            link.parent.mkdir()
            link.symlink_to(outside, target_is_directory=True)
            errors, notes = check(self.root)
            self.assertTrue(any("outside selected root" in error for error in errors))
            self.assertNotIn("PRIVATE-MARKER", "\n".join(errors + notes))

    def test_cli_reports_static_result_without_mutating_input_files(self):
        self.skill()
        self.agent("name: reviewer\ndescription: Review code.\ntools: [read]")
        before = {path.relative_to(self.root): (path.read_bytes(), path.stat().st_mtime_ns)
                  for path in self.root.rglob("*") if path.is_file()}
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), "--json"],
                                capture_output=True, text=True, check=False)
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["static_validation"], "passed")
        self.assertEqual(report["host_discovery"], "not_checked")
        self.assertEqual(report["host_invocation"], "not_checked")
        after = {path.relative_to(self.root): (path.read_bytes(), path.stat().st_mtime_ns)
                 for path in self.root.rglob("*") if path.is_file()}
        self.assertEqual(after, before)

    def test_cli_invalid_root_has_json_failure_and_nonzero_exit(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root / "missing"), "--json"],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1)
        report = json.loads(result.stdout)
        self.assertEqual(report["static_validation"], "failed")
        self.assertTrue(report["errors"])
        self.assertEqual(report["host_discovery"], "not_checked")


if __name__ == "__main__":
    unittest.main()
