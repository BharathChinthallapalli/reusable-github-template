"""Verify the evaluation report contract through its offline command line."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/check_evaluation.py"


def synthetic_report():
    cases = [
        {"id": "answer", "expected": {"status": "labeled", "label": "answer grounded in source"},
         "outcome": "pass", "evidence": "synthetic:answer-observation", "measurements": {"latency_ms": 12.5}},
        {"id": "unanswerable", "expected": {"status": "labeled", "label": "decline unsupported answer"},
         "outcome": "pass", "evidence": "synthetic:unanswerable-observation"},
    ]
    run = {"provenance": {name: "synthetic:" + name for name in
                          ("code", "config", "data", "model", "evaluator", "environment")}, "cases": cases}
    return {"version": 1, "task": {"id": "synthetic-task", "case_set_id": "synthetic-cases-v1"},
            "acceptance": {"required_cases": ["answer"], "max_regressions": 0},
            "baseline": copy.deepcopy(run), "candidate": copy.deepcopy(run)}


class EvaluationTests(unittest.TestCase):
    def run_report(self, report=None, raw=None):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            original = (raw if raw is not None else json.dumps(report)).encode("utf-8")
            path.write_bytes(original)
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)],
                                    capture_output=True, text=True, check=False)
            self.assertEqual(path.read_bytes(), original, "The report must remain unchanged")
        self.assertNotIn("Traceback", result.stderr)
        return result.returncode, json.loads(result.stdout)

    def test_complete_labeled_unanswerable_case_can_pass(self):
        code, summary = self.run_report(synthetic_report())
        self.assertEqual((code, summary["status"]), (0, "passed"))
        self.assertEqual(summary["candidate"]["quality_passes"], {"numerator": 2, "denominator": 2})
        self.assertEqual(summary["comparison"]["comparable_cases"], 2)

    def test_declared_regression_budget_applies_only_to_nonrequired_cases(self):
        report = synthetic_report()
        report["candidate"]["cases"][1]["outcome"] = "quality_failure"
        self.assertEqual(self.run_report(report)[0], 1)
        report["acceptance"]["max_regressions"] = 1
        self.assertEqual(self.run_report(report)[0], 0)
        report["candidate"]["cases"][0]["outcome"] = "quality_failure"
        report["acceptance"]["max_regressions"] = 2
        code, summary = self.run_report(report)
        self.assertEqual((code, summary["status"]), (1, "failed"))
        self.assertEqual(summary["comparison"]["required_quality_failures"], ["answer"])

    def test_existing_nonrequired_failure_is_visible_without_consuming_regression_budget(self):
        report = synthetic_report()
        for run in ("baseline", "candidate"):
            report[run]["cases"][1]["outcome"] = "quality_failure"
        code, summary = self.run_report(report)
        self.assertEqual((code, summary["status"]), (0, "passed"))
        self.assertEqual(summary["comparison"]["regressions"], [])
        self.assertEqual(summary["candidate"]["outcomes"]["quality_failure"], 1)
        report["acceptance"]["required_cases"].append("unanswerable")
        code, summary = self.run_report(report)
        self.assertEqual((code, summary["status"]), (1, "failed"))
        self.assertEqual(summary["comparison"]["regressions"], [])
        self.assertEqual(summary["comparison"]["required_quality_failures"], ["unanswerable"])

    def test_incomplete_outcomes_cannot_be_reported_as_quality_failures_or_pass(self):
        for outcome in ("execution_error", "missing_label", "not_run", "skipped"):
            with self.subTest(outcome=outcome):
                report = synthetic_report()
                report["candidate"]["cases"][0]["outcome"] = outcome
                if outcome == "missing_label":
                    for run in ("baseline", "candidate"):
                        report[run]["cases"][0]["expected"] = {"status": "missing_label"}
                        report[run]["cases"][0]["outcome"] = "missing_label"
                code, summary = self.run_report(report)
                self.assertEqual((code, summary["status"]), (1, "inconclusive"))
                self.assertEqual(summary["candidate"]["quality_passes"], {"numerator": 1, "denominator": 1})
                self.assertEqual(summary["candidate"]["outcomes"][outcome], 1)
                self.assertEqual(summary["comparison"]["total_cases"], 2)

    def test_incomplete_baseline_or_optional_case_prevents_passing_comparison(self):
        for run, index in (("baseline", 0), ("candidate", 1)):
            report = synthetic_report()
            report[run]["cases"][index]["outcome"] = "not_run"
            self.assertEqual(self.run_report(report)[1]["status"], "inconclusive")

    def test_decisive_quality_failure_and_incomplete_evidence_are_both_reported(self):
        report = synthetic_report()
        report["candidate"]["cases"][0]["outcome"] = "quality_failure"
        report["baseline"]["cases"][1]["outcome"] = "execution_error"
        code, summary = self.run_report(report)
        self.assertEqual((code, summary["status"]), (1, "failed"))
        self.assertEqual(summary["comparison"]["required_quality_failures"], ["answer"])
        self.assertEqual(summary["baseline"]["outcomes"]["execution_error"], 1)
        self.assertTrue(any("incomplete" in reason for reason in summary["reasons"]))

    def test_case_order_does_not_change_comparison(self):
        report = synthetic_report()
        report["candidate"]["cases"].reverse()
        self.assertEqual(self.run_report(report)[0], 0)

    def test_missing_duplicate_or_changed_case_identity_is_invalid(self):
        for change in ("missing", "duplicate", "renamed", "changed_label"):
            report = synthetic_report()
            cases = report["candidate"]["cases"]
            if change == "missing":
                cases.pop()
            elif change == "duplicate":
                cases.append(copy.deepcopy(cases[0]))
            elif change == "renamed":
                cases[0]["id"] = "different"
            else:
                cases[0]["expected"]["label"] = "changed after evaluation"
            with self.subTest(change=change):
                self.assertEqual(self.run_report(report)[0], 2)

    def test_acceptance_must_be_explicit_nonempty_and_refer_to_real_cases(self):
        for acceptance in ({}, {"required_cases": [], "max_regressions": 0},
                           {"required_cases": ["absent"], "max_regressions": 0},
                           {"required_cases": ["answer", "answer"], "max_regressions": 0},
                           {"required_cases": ["answer"], "max_regressions": True},
                           {"required_cases": ["answer"], "max_regressions": -1}):
            report = synthetic_report()
            report["acceptance"] = acceptance
            with self.subTest(acceptance=acceptance):
                self.assertEqual(self.run_report(report)[0], 2)

    def test_wrong_types_empty_provenance_and_unknown_fields_are_invalid(self):
        for field, value in (("version", True), ("task", []), ("baseline", None),
                             ("unexpected", "ignored?")):
            report = synthetic_report()
            report[field] = value
            with self.subTest(field=field):
                self.assertEqual(self.run_report(report)[0], 2)
        report = synthetic_report()
        report["candidate"]["provenance"]["model"] = "  "
        self.assertEqual(self.run_report(report)[0], 2)

    def test_quality_result_requires_an_evidence_reference_or_observation(self):
        report = synthetic_report()
        report["candidate"]["cases"][0]["evidence"] = ""
        self.assertEqual(self.run_report(report)[0], 2)

    def test_measurements_require_finite_numbers_and_reject_boolean(self):
        for value in (True, "1", None, float("nan"), float("inf"), -float("inf"), 1e309):
            report = synthetic_report()
            report["candidate"]["cases"][0]["measurements"] = {"score": value}
            with self.subTest(value=value):
                self.assertEqual(self.run_report(report)[0], 2)
        raw = json.dumps(synthetic_report()).replace('12.5', '1e999')
        self.assertEqual(self.run_report(raw=raw)[0], 2)

    def test_missing_label_cannot_claim_a_measured_quality_outcome(self):
        report = synthetic_report()
        for run in ("baseline", "candidate"):
            report[run]["cases"][0]["expected"] = {"status": "missing_label"}
        self.assertEqual(self.run_report(report)[0], 2)

    def test_duplicate_keys_invalid_json_and_excessive_nesting_return_json_errors(self):
        for raw in ('{"version":1,"version":1}', '{"nested":{"id":1,"id":2}}',
                    '{', '[' * 1500 + '0' + ']' * 1500):
            with self.subTest(raw=raw[:40]):
                code, summary = self.run_report(raw=raw)
                self.assertEqual((code, summary["status"]), (2, "invalid"))
                self.assertTrue(summary["errors"])

    def test_missing_input_returns_json_diagnostic(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, str(SCRIPT), str(Path(directory) / "missing.json")],
                                    capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["status"], "invalid")

    def test_bundled_examples_have_the_documented_exit_status(self):
        for name, expected in (("passing.json", 0), ("incomplete.json", 1)):
            result = subprocess.run([sys.executable, str(SCRIPT), str(ROOT / "examples/evaluation" / name)],
                                    capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
            self.assertTrue(json.loads(result.stdout)["task"]["id"].startswith("synthetic"))


if __name__ == "__main__":
    unittest.main()
