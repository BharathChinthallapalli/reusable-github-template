"""Validate an offline evaluation report and apply its declared acceptance gate."""

import argparse
import json
import math
from pathlib import Path


OUTCOMES = ("pass", "quality_failure", "execution_error", "missing_label", "not_run", "skipped")
QUALITY_OUTCOMES = {"pass", "quality_failure"}
PROVENANCE_FIELDS = {"code", "config", "data", "model", "evaluator", "environment"}


class InvalidReport(ValueError):
    """The report cannot be interpreted under the versioned contract."""


def object_fields(value, required, context, optional=()):
    if not isinstance(value, dict):
        raise InvalidReport(f"{context} must be an object")
    missing = set(required) - value.keys()
    unknown = value.keys() - set(required) - set(optional)
    if missing or unknown:
        raise InvalidReport(f"{context} has missing fields {sorted(missing)} or unknown fields {sorted(unknown)}")


def nonempty_text(value, context):
    if not isinstance(value, str) or not value.strip():
        raise InvalidReport(f"{context} must be a nonempty string")


def unique_ids(values, context):
    if not isinstance(values, list) or not values:
        raise InvalidReport(f"{context} must be a nonempty array")
    seen = set()
    for value in values:
        nonempty_text(value, context)
        if value in seen:
            raise InvalidReport(f"{context} contains a duplicate ID")
        seen.add(value)
    return seen


def validate_case(case, context):
    object_fields(case, {"id", "expected", "outcome", "evidence"}, context, {"measurements"})
    for field in ("id", "outcome", "evidence"):
        nonempty_text(case[field], f"{context}.{field}")
    if case["outcome"] not in OUTCOMES:
        raise InvalidReport(f"{context}.outcome is not a supported outcome")
    expected = case["expected"]
    object_fields(expected, {"status"}, f"{context}.expected", {"label"})
    if expected["status"] == "labeled":
        nonempty_text(expected.get("label"), f"{context}.expected.label")
        if case["outcome"] == "missing_label":
            raise InvalidReport(f"{context} declares a label and a missing_label outcome")
    elif expected["status"] == "missing_label":
        if "label" in expected or case["outcome"] in QUALITY_OUTCOMES:
            raise InvalidReport(f"{context} cannot label or assess quality without an expected label")
    else:
        raise InvalidReport(f"{context}.expected.status must be labeled or missing_label")
    measurements = case.get("measurements", {})
    if not isinstance(measurements, dict):
        raise InvalidReport(f"{context}.measurements must be an object")
    for name, value in measurements.items():
        nonempty_text(name, f"{context}.measurement name")
        if type(value) not in (int, float):
            raise InvalidReport(f"{context}.measurements values must be finite numbers, not booleans")
        if isinstance(value, float) and not math.isfinite(value):
            raise InvalidReport(f"{context}.measurements values must be finite numbers")


def validate_run(run, context):
    object_fields(run, {"provenance", "cases"}, context)
    object_fields(run["provenance"], PROVENANCE_FIELDS, f"{context}.provenance")
    for field, value in run["provenance"].items():
        nonempty_text(value, f"{context}.provenance.{field}")
    cases = run["cases"]
    if not isinstance(cases, list) or not cases:
        raise InvalidReport(f"{context}.cases must be a nonempty array")
    for index, case in enumerate(cases):
        validate_case(case, f"{context}.cases[{index}]")
    unique_ids([case["id"] for case in cases], f"{context}.cases")
    return {case["id"]: case for case in cases}


def validate_report(report):
    object_fields(report, {"version", "task", "acceptance", "baseline", "candidate"}, "report")
    if type(report["version"]) is not int or report["version"] != 1:
        raise InvalidReport("report.version must be the integer 1")
    object_fields(report["task"], {"id", "case_set_id"}, "task")
    for field, value in report["task"].items():
        nonempty_text(value, f"task.{field}")
    acceptance = report["acceptance"]
    object_fields(acceptance, {"required_cases", "max_regressions"}, "acceptance")
    required = unique_ids(acceptance["required_cases"], "acceptance.required_cases")
    if type(acceptance["max_regressions"]) is not int or acceptance["max_regressions"] < 0:
        raise InvalidReport("acceptance.max_regressions must be a nonnegative integer")
    baseline = validate_run(report["baseline"], "baseline")
    candidate = validate_run(report["candidate"], "candidate")
    if baseline.keys() != candidate.keys():
        raise InvalidReport("baseline and candidate must contain exactly the same case IDs")
    if not required <= candidate.keys():
        raise InvalidReport("acceptance.required_cases contains IDs absent from the case set")
    for case_id in baseline:
        if baseline[case_id]["expected"] != candidate[case_id]["expected"]:
            raise InvalidReport("baseline and candidate expected labels must match for every case ID")
    return baseline, candidate


def run_counts(cases):
    counts = {outcome: 0 for outcome in OUTCOMES}
    for case in cases.values():
        counts[case["outcome"]] += 1
    return {"total_cases": len(cases), "outcomes": counts,
            "quality_passes": {"numerator": counts["pass"],
                               "denominator": counts["pass"] + counts["quality_failure"]}}


def evaluate(report, baseline, candidate):
    required = report["acceptance"]["required_cases"]
    comparable = [case_id for case_id in baseline
                  if baseline[case_id]["outcome"] in QUALITY_OUTCOMES
                  and candidate[case_id]["outcome"] in QUALITY_OUTCOMES]
    regressions = sorted(case_id for case_id in comparable
                         if baseline[case_id]["outcome"] == "pass"
                         and candidate[case_id]["outcome"] == "quality_failure")
    required_failures = sorted(case_id for case_id in required
                               if candidate[case_id]["outcome"] == "quality_failure")
    reasons = []
    if required_failures:
        reasons.append("Required candidate cases have quality failures")
    if len(regressions) > report["acceptance"]["max_regressions"]:
        reasons.append("Quality regressions exceed the declared maximum")
    status = "failed" if reasons else "passed"
    if len(comparable) != len(baseline):
        reasons.append("The baseline/candidate comparison contains incomplete outcomes")
        if status != "failed":
            status = "inconclusive"
    return {"version": 1, "status": status, "task": report["task"], "acceptance": report["acceptance"],
            "provenance": {"baseline": report["baseline"]["provenance"],
                           "candidate": report["candidate"]["provenance"]},
            "baseline": run_counts(baseline), "candidate": run_counts(candidate),
            "comparison": {"total_cases": len(baseline), "comparable_cases": len(comparable),
                           "regressions": regressions, "required_cases": len(required),
                           "required_passes": sum(candidate[case_id]["outcome"] == "pass" for case_id in required),
                           "required_quality_failures": required_failures},
            "reasons": reasons, "errors": []}


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InvalidReport("JSON object contains a duplicate key")
        result[key] = value
    return result


def reject_nonfinite_constant(value):
    raise InvalidReport("JSON contains a nonfinite numeric constant")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     epilog="Exit codes: 0 passed; 1 failed or inconclusive; 2 invalid input. "
                                            "Prints JSON; never runs a model or changes the input report. "
                                            "See docs/evaluation-reports.md for version 1.")
    parser.add_argument("report", type=Path, help="Local version 1 JSON evidence report")
    args = parser.parse_args()
    try:
        report = json.loads(args.report.read_text(encoding="utf-8"),
                            object_pairs_hook=reject_duplicate_keys,
                            parse_constant=reject_nonfinite_constant)
        baseline, candidate = validate_report(report)
        summary = evaluate(report, baseline, candidate)
    except (OSError, UnicodeError, ValueError, RecursionError) as error:
        summary = {"status": "invalid", "errors": [f"Cannot validate report: {error}"], "reasons": []}
    print(json.dumps(summary, indent=2, allow_nan=False))
    if summary["status"] == "invalid":
        return 2
    return 0 if summary["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
