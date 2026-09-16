"""Inert artifact/governance tests, not real model, approval or deployment evidence."""

import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import yaml
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from sdlc_contracts import (  # noqa: E402
    LIMIT, Invalid, compliance, document, load_json, reference,
    relative_name, requirements_check, sections, spec_check, tasks_check,
)
from sdlc_governance import (  # noqa: E402
    change_gate, dor_task, failure_action, finding_check, posture_check, review_independence,
)
from sdlc_metrics import compute  # noqa: E402
from sdlc_monitor import evaluate  # noqa: E402
from initialize import apply_changes, plan_changes  # noqa: E402


def artifact(meta, body):
    return "---\n" + json.dumps(meta, indent=2) + "\n---\n" + body


class ArtifactTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="sdlc-fixture-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for parent in ("intent", "specs"):
            shutil.copytree(ROOT / parent / "monitor-smoke", self.root / parent / "monitor-smoke")
        (self.root / "tests").mkdir()
        (self.root / "tests/test_sdlc.py").write_text("# Verification reference, not an executed test result.\n")
        self.task_meta, _ = document(self.root, "specs/monitor-smoke/tasks.md", "tasks")
        self.task = self.task_meta["tasks"][0]

    def change_document(self, kind, mutate):
        name = f"{'intent' if kind == 'intent' else 'specs'}/monitor-smoke/{kind}.md"
        meta, body = document(self.root, name, kind)
        mutate(meta)
        (self.root / name).write_text(artifact(meta, body))

    def test_example_instantiates_and_renders_without_authorizing(self):
        rendered, report = spec_check(self.root, "monitor-smoke")
        self.assertIn("source-sha256", rendered)
        self.assertIn("Synthetic requirements", rendered)
        self.assertEqual(report["result"], "STRUCTURALLY_READY")
        self.assertEqual(report["authorization"], "UNVERIFIED")
        self.assertTrue(report["dispatch"].startswith("BLOCKED"))

    def test_changed_source_invalidates_render_hash(self):
        _, before = spec_check(self.root, "monitor-smoke")
        path = self.root / "specs/monitor-smoke/design.md"
        path.write_text(path.read_text() + "\nAn additional reviewed constraint.\n")
        _, after = spec_check(self.root, "monitor-smoke")
        self.assertNotEqual(before["source_hashes"], after["source_hashes"])

    def test_declaring_accepted_does_not_authenticate(self):
        self.change_document("tasks", lambda m: m.update(status="accepted"))
        _, report = spec_check(self.root, "monitor-smoke")
        self.assertEqual(report["authorization"], "UNVERIFIED")

    def test_archetypes_required(self):
        self.change_document("intent", lambda m: m.update(archetypes=[]))
        with self.assertRaises(Invalid):
            spec_check(self.root, "monitor-smoke")

    def test_all_declared_archetype_sections_required(self):
        self.change_document("intent", lambda m: m.update(archetypes=["A", "B"]))
        with self.assertRaisesRegex(Invalid, "section"):
            spec_check(self.root, "monitor-smoke")

    def test_compliance_unassessed_blocks_render(self):
        self.change_document("intent", lambda m: m["compliance"]["gdpr"].update(applicability="requires_assessment"))
        with self.assertRaisesRegex(Invalid, "unresolved"):
            spec_check(self.root, "monitor-smoke")

    def test_na_without_reason_rejected(self):
        meta, _ = document(self.root, "intent/monitor-smoke/intent.md", "intent")
        meta["compliance"]["gdpr"]["reason"] = ""
        with self.assertRaises(Invalid):
            compliance(meta["compliance"])

    def test_intent_design_drift_requires_review(self):
        self.change_document("design", lambda m: m["compliance"]["gdpr"].update(reason="Changed assessment"))
        with self.assertRaisesRegex(Invalid, "drift"):
            spec_check(self.root, "monitor-smoke")

    def test_flagged_concern_blocks_render(self):
        self.change_document("design", lambda m: m.update(concerns=["Legal owner has not resolved the issue"]))
        with self.assertRaisesRegex(Invalid, "concerns"):
            spec_check(self.root, "monitor-smoke")

    def test_every_requirement_needs_resolvable_test(self):
        meta, _ = document(self.root, "specs/monitor-smoke/requirements.md", "requirements")
        for verification in ([], ["tests/missing.py"], ["docs/statement.md"]):
            with self.subTest(verification=verification):
                bad = copy.deepcopy(meta)
                bad["requirements"][0]["verification"] = verification
                with self.assertRaises(Invalid):
                    requirements_check(self.root, bad)

    def test_unknown_requirement_or_cycle_blocks(self):
        for mutation in (lambda t: t.update(requirements=["R-2"]), lambda t: t.update(depends_on=["T-1"])):
            with self.subTest(mutation=mutation):
                bad = copy.deepcopy(self.task_meta)
                mutation(bad["tasks"][0])
                with self.assertRaises(Invalid):
                    tasks_check(self.root, bad, {"R-1"})

    def test_dependency_must_be_earlier_wave(self):
        bad = copy.deepcopy(self.task_meta)
        second = copy.deepcopy(self.task)
        second.update(id="T-2", depends_on=["T-1"])
        bad["tasks"].append(second)
        with self.assertRaisesRegex(Invalid, "earlier wave"):
            tasks_check(self.root, bad, {"R-1"})
        second["wave"] = 2
        tasks_check(self.root, bad, {"R-1"})

    def test_duplicate_keys_and_nan_rejected(self):
        for value in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'):
            with self.subTest(value=value), self.assertRaises(Invalid):
                load_json(value)

    def test_oversize_json_rejected(self):
        with self.assertRaises(Invalid):
            load_json(" " * (LIMIT + 1))

    def test_unsafe_paths_rejected(self):
        for value in ("../secret", "/etc/passwd", "C:/Users/user", "docs/../file", "docs\\file", "docs/file:stream", "docs/file.", "docs//x", "docs/*.md"):
            with self.subTest(value=value), self.assertRaises(Invalid):
                relative_name(value)

    def test_private_references_rejected(self):
        for value in (".env", ".ssh/id_rsa", "docs/.env", "docs/mail.ost"):
            with self.subTest(value=value), self.assertRaises(Invalid):
                reference(self.root, value)

    def test_symlink_reference_rejected(self):
        target = self.root / "tests/link.py"
        try:
            target.symlink_to(self.root / "tests/test_sdlc.py")
        except OSError:
            self.skipTest("Platform cannot create fixture symlinks")
        with self.assertRaises(Invalid):
            reference(self.root, "tests/link.py")

    def test_code_fence_cannot_supply_section(self):
        result = sections("## Real\nContent\n```text\n## Fake\n```\n")
        self.assertNotIn("Fake", result)

    def test_dor_tbd_rejected(self):
        self.task["done"] = "TBD"
        report = dor_task(self.root, self.task, {"T-1"})
        self.assertEqual(report["result"], "BLOCKED")
        self.assertEqual(report["gates"]["2"]["result"], "FAIL")

    def test_monitor_shortcut_retains_structural_gates(self):
        # In-memory test stands in for a trusted caller, NOT real CI authentication.
        self.task.update(acceptance="", done="", surface=[])
        report = dor_task(self.root, self.task, {"T-1"}, verified_source="monitor")
        self.assertEqual(report["result"], "STRUCTURALLY_READY")
        self.assertEqual({k for k, v in report["gates"].items() if v["result"] == "SKIPPED"}, {"1", "4", "5", "6"})
        self.assertTrue(report["dispatch"].startswith("BLOCKED"))
        self.task["done"] = "TBD"
        self.assertEqual(dor_task(self.root, self.task, {"T-1"}, verified_source="monitor")["result"], "BLOCKED")

    def test_forged_source_cannot_request_shortcut(self):
        self.task["source"] = "monitor"
        with self.assertRaises(Invalid):
            dor_task(self.root, self.task, {"T-1"})

    def test_cli_in_scratch_project(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/dor-check.py"), "monitor-smoke", "--root", str(self.root)], capture_output=True, text=True, timeout=10, check=False)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertTrue(json.loads(result.stdout)["dispatch"].startswith("BLOCKED"))

    def test_template_initializer_then_example_in_scratch(self):
        # Copy only the explicit initializer contract and example, not any home,
        # environment, credential store, ledger, tool cache or source checkout.
        for name in ("template.json", "README.md", "SECURITY.md", "SUPPORT.md", ".github/CODEOWNERS", "docs/project.md"):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        values = {"name": "SDLC scratch fixture", "slug": "sdlc-scratch", "owner": "example-org",
                  "codeowner": "@example-org/maintainers", "security_contact": "mailto:security@example.com",
                  "description": "Synthetic offline template instantiation."}
        apply_changes(plan_changes(self.root, values))
        self.assertTrue(json.loads((self.root / "template.json").read_text())["initialized"])
        self.assertIn("SDLC scratch fixture", (self.root / "README.md").read_text())
        self.assertEqual(spec_check(self.root, "monitor-smoke")[1]["result"], "STRUCTURALLY_READY")
        self.assertEqual(plan_changes(self.root, values), [])

    def test_full_repository_template_snapshot_in_scratch(self):
        listing = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True, timeout=10)
        names = set(listing.stdout.decode().strip("\0").split("\0"))
        add = (ROOT / "docs/add/0005-ai-native-sdlc.md").read_text().split("---", 2)[1]
        names.update(yaml.safe_load(add)["scope"])
        names.add("docs/add/0005-ai-native-sdlc.md")
        snapshot = self.root / "full-template"
        snapshot.mkdir()
        for name in sorted(names):
            relative_name(name)
            source = ROOT / name
            self.assertFalse(source.is_symlink(), "Fixture snapshot must not follow links")
            if source.is_file():
                destination = snapshot / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, destination)
        values = {"name": "SDLC full scratch", "slug": "sdlc-scratch", "owner": "example-org",
                  "codeowner": "@example-org/maintainers", "security_contact": "mailto:security@example.com",
                  "description": "Synthetic full template instantiation."}
        apply_changes(plan_changes(snapshot, values))
        rendered, report = spec_check(snapshot, "monitor-smoke")
        self.assertEqual(report["result"], "STRUCTURALLY_READY")
        (snapshot / "specs/monitor-smoke/spec.md").write_text(rendered)
        for command in ([sys.executable, str(snapshot / "tools/check_repository.py"), "--root", str(snapshot)],
                        [sys.executable, str(snapshot / "scripts/monitor.py"), "docs/sdlc/fixtures/samples.json", "--root", str(snapshot), "--now", "2026-09-16T10:01:00Z"]):
            result = subprocess.run(command, cwd=snapshot, capture_output=True, text=True, timeout=10, check=False)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)


class GovernanceTests(unittest.TestCase):
    def change(self, path="src/app.py", lines=1):
        return {"path": path, "old_path": None, "added": ["line"] * lines, "deleted": [], "binary": False, "linked": False}

    def test_junior_budget_boundary(self):
        self.assertEqual(change_gate([self.change(lines=200)], actor="engineer", tests_present=True)["result"], "DIFF_POLICY_PASS")
        self.assertEqual(change_gate([self.change(lines=201)], actor="engineer", tests_present=True)["result"], "BLOCKED")

    def test_missing_path_and_non_lock_filename(self):
        bad = self.change()
        bad["path"] = None
        with self.assertRaises(Invalid):
            change_gate([bad], actor="engineer", tests_present=True)
        self.assertEqual(change_gate([self.change("src/clock.py")], actor="engineer", tests_present=True)["result"], "DIFF_POLICY_PASS")

    def test_deletions_count_and_file_cap(self):
        item = self.change(lines=1)
        item["deleted"] = ["deleted"] * 200
        self.assertEqual(change_gate([item], actor="engineer", tests_present=True)["result"], "BLOCKED")
        self.assertEqual(change_gate([self.change(f"src/{i}.py") for i in range(6)], actor="engineer", tests_present=True)["result"], "BLOCKED")

    def test_protected_paths_deny_even_docs(self):
        for path in ("tests/test_app.py", "evals/prompt.md", ".guardian/policy.json", ".CoDeX/hooks.json", "docs/add/policy.md", "AGENTS.md", "src/package-lock.json"):
            with self.subTest(path=path):
                self.assertEqual(change_gate([self.change(path)], actor="untrusted", tests_present=True)["result"], "BLOCKED")

    def test_rename_cannot_hide_protected_source(self):
        item = self.change("docs/moved.md")
        item["old_path"] = ".github/workflows/ci.yml"
        self.assertEqual(change_gate([item], actor="untrusted", tests_present=True)["result"], "BLOCKED")

    def test_new_uses_detected_even_in_allowed_path(self):
        item = self.change("docs/example.md")
        item["added"] = ["  - uses: attacker/action@main"]
        self.assertEqual(change_gate([item], actor="untrusted", tests_present=True)["result"], "BLOCKED")

    def test_vision_lint(self):
        item = self.change("specs/example/design.md")
        item["added"] = ["we'll document after implementation"]
        self.assertEqual(change_gate([item], actor="untrusted", tests_present=True)["result"], "BLOCKED")

    def test_docs_bypass_does_not_bypass_denials(self):
        self.assertTrue(change_gate([self.change("docs/guide.md")], actor="untrusted", tests_present=False)["docs_only"])
        self.assertEqual(change_gate([self.change()], actor="engineer", tests_present=False)["result"], "BLOCKED")

    def reviews(self, harness):
        return [{"stage": stage, "harness": harness, "verdict": "approved", "transcript_sha256": "a" * 64} for stage in ("code-review", "test-review", "security-review")]

    def test_same_harness_rejected(self):
        with self.assertRaisesRegex(Invalid, "differ"):
            review_independence("claude", self.reviews("claude"))

    def test_different_harness_shape_pass_not_attestation(self):
        report = review_independence("codex", self.reviews("claude"))
        self.assertEqual(report["result"], "INDEPENDENCE_SHAPE_PASS")
        self.assertEqual(report["signature"], "UNVERIFIED")
        self.assertTrue(report["release"].startswith("BLOCKED"))

    def test_missing_or_duplicate_reviews_rejected(self):
        for reviews in ([], self.reviews("claude")[:2], self.reviews("claude") * 2):
            with self.subTest(reviews=reviews), self.assertRaises(Invalid):
                review_independence("codex", reviews)

    def test_immediate_and_unknown_failures_escalate(self):
        for mode in ("GuardianDenied", "PivotAttempt", "HookTimeoutFailOpen"):
            self.assertEqual(failure_action(mode, 0)["action"], "ESCALATE_IMMEDIATELY")
        self.assertEqual(failure_action("Unrecognized", 0)["action"], "ESCALATE_UNKNOWN_FAILURE")

    def test_override_requires_notes_and_cannot_weaken_hard_gate(self):
        base = {"schema_version": 1, "regimes": [], "overrides": {}, "retention": []}
        posture_check(base)
        for override in ({"soft_quality_threshold": {"value": 1, "owner": "owner"}}, {"guardian": {"value": False, "owner": "owner", "_notes": "urgent"}}):
            with self.subTest(override=override), self.assertRaises(Invalid):
                posture_check(base | {"overrides": override})

    def test_major_finding_requires_failure_scenario(self):
        with self.assertRaises(Invalid):
            finding_check({"severity": "major", "summary": "A concern", "failureScenario": ""})


class MonitorMetricsTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((ROOT / "monitoring/bands.yaml").read_text())
        self.samples = json.loads((ROOT / "docs/sdlc/fixtures/samples.json").read_text())
        self.now = datetime(2026, 9, 16, 10, 1, tzinfo=timezone.utc)

    def test_control_band_boundaries(self):
        for value, tier in ((99, 0), (109.9, 0), (110, 1), (120, 2), (130, 3)):
            with self.subTest(value=value):
                self.samples["p95-latency"]["value"] = value
                report = evaluate(self.config, self.samples, self.now)[0]
                self.assertEqual(report["tier"], tier)
                self.assertEqual(report["allowed_tools"], [])
                self.assertEqual(report["runbook_execution"], "DISABLED")

    def test_lower_is_worse_and_two_sided(self):
        self.samples["p95-latency"]["value"] = 70
        for direction in ("low", "both"):
            self.config["metrics"][0]["direction"] = direction
            self.assertEqual(evaluate(self.config, self.samples, self.now)[0]["tier"], 3)

    def test_same_sample_has_stable_id_and_changed_baseline_does_not(self):
        first = evaluate(self.config, self.samples, self.now)[0]
        self.assertEqual(first, evaluate(self.config, self.samples, self.now)[0])
        self.config["metrics"][0]["baseline_version"] = "new-baseline"
        self.assertNotEqual(first["evidence_id"], evaluate(self.config, self.samples, self.now)[0]["evidence_id"])

    def test_bad_samples_and_baselines_escalate(self):
        for value in (float("nan"), float("inf"), True, "130"):
            with self.subTest(value=value), self.assertRaises(Invalid):
                self.samples["p95-latency"]["value"] = value
                evaluate(self.config, self.samples, self.now)
        self.samples["p95-latency"]["value"] = 130
        for timestamp in ("2026-09-16T09:00:00Z", "2026-09-16T11:00:00Z", "2026-09-16T10:00:00"):
            with self.subTest(timestamp=timestamp), self.assertRaises(Invalid):
                self.samples["p95-latency"]["timestamp"] = timestamp
                evaluate(self.config, self.samples, self.now)

    def test_zero_variance_and_unknown_metric_rejected(self):
        self.config["metrics"][0]["stddev"] = 0
        with self.assertRaises(Invalid):
            evaluate(self.config, self.samples, self.now)
        self.config["metrics"][0]["stddev"] = 10
        self.samples["unknown"] = self.samples["p95-latency"]
        with self.assertRaises(Invalid):
            evaluate(self.config, self.samples, self.now)

    def test_synthetic_metrics_known_values(self):
        report = compute(json.loads((ROOT / "docs/sdlc/fixtures/events.json").read_text()))
        self.assertEqual(report["conversation_to_intent_seconds"], 300)
        self.assertEqual(report["intent_to_spec_seconds"], 600)
        self.assertEqual(report["pr_cycle_seconds"], 600)
        self.assertEqual(report["breach_to_intent_seconds"], 120)
        self.assertEqual(report["cost_per_successful_task"], 0.2)
        self.assertIsNone(report["repeat_incidents_per_class"])

    def test_empty_metrics_unknown_not_zero(self):
        report = compute([])
        self.assertIsNone(report["eval_pass_rate"])
        self.assertIsNone(report["gate_violations_reaching_production"])

    def test_numeric_overflow_rejected(self):
        self.samples["p95-latency"]["value"] = 10 ** 400
        with self.assertRaises(Invalid):
            evaluate(self.config, self.samples, self.now)
        events = [{"event_id": str(i), "change": "example", "kind": "gate_wait", "timestamp": "2026-09-16T10:00:00Z", "value": 1e308} for i in range(2)]
        with self.assertRaises(Invalid):
            compute(events)

    def test_duplicate_or_inconsistent_metric_events_rejected(self):
        events = json.loads((ROOT / "docs/sdlc/fixtures/events.json").read_text())
        with self.assertRaises(Invalid):
            compute(events + [events[0]])
        events[1]["timestamp"] = "2026-09-16T08:00:00Z"
        with self.assertRaises(Invalid):
            compute(events)


if __name__ == "__main__":
    unittest.main()
