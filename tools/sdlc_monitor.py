"""Evaluate calibrated control bands; emit proposals only, never remediation commands."""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path

from sdlc_contracts import Invalid, SLUG, canonical, digest, load_json, object_keys, read_text, require, utc_time


def number(value: object, label: str) -> float:
    require(type(value) in {int, float}, "Invalid number type: " + label)
    try:
        converted = float(value)
    except OverflowError as exc:
        raise Invalid("Numeric overflow: " + label) from exc
    require(math.isfinite(converted), "Invalid finite number: " + label)
    return converted


def evaluate(config: dict, samples: dict, now: datetime) -> list[dict]:
    object_keys(config, {"schema_version", "metrics"})
    require(type(config["schema_version"]) is int and config["schema_version"] == 1, "Unknown bands schema")
    require(isinstance(samples, dict), "Samples must be a metric map")
    require(now.tzinfo is not None, "Evaluation clock requires timezone")
    require(isinstance(config["metrics"], list) and 0 < len(config["metrics"]) <= 100, "Expected one to 100 metrics")
    names = set()
    results = []
    for metric in config["metrics"]:
        object_keys(metric, {"name", "mean", "stddev", "direction", "max_age_seconds", "owner", "baseline_version", "archetypes"})
        name = metric["name"]
        require(isinstance(name, str) and SLUG.fullmatch(name) and name not in names, "Invalid or duplicate metric name")
        names.add(name)
        require(isinstance(metric["owner"], str) and metric["owner"].strip(), "Metric owner required")
        require(isinstance(metric["baseline_version"], str) and metric["baseline_version"].strip(), "Baseline version required")
        require(isinstance(metric["archetypes"], list) and metric["archetypes"] and all(a in {"A", "B", "C", "D", "E"} for a in metric["archetypes"]), "Metric archetypes required")
        mean = number(metric["mean"], name + " mean")
        stddev = number(metric["stddev"], name + " stddev")
        age_limit = number(metric["max_age_seconds"], name + " age")
        require(stddev > 0 and age_limit > 0, "Standard deviation and freshness limit must be positive")
        require(metric["direction"] in {"high", "low", "both"}, "Unknown metric direction")
        require(name in samples, "Missing metric: " + name)
        sample = samples[name]
        object_keys(sample, {"value", "timestamp", "sample_id"})
        require(isinstance(sample["sample_id"], str) and sample["sample_id"].strip(), "Sample ID required")
        at = utc_time(sample["timestamp"])
        require(0 <= (now - at).total_seconds() <= age_limit, "Stale or future sample: " + name)
        value = number(sample["value"], name)
        z = (value - mean) / stddev
        require(math.isfinite(z), "Control-band calculation overflow")
        if metric["direction"] == "low":
            z = -z
        elif metric["direction"] == "both":
            z = abs(z)
        tier = 3 if z >= 3 else 2 if z >= 2 else 1 if z >= 1 else 0
        action = ("OBSERVE", "LOG", "REQUEST_READ_ONLY_DIAGNOSIS", "PROPOSE_INTENT_PR")[tier]
        key = digest(canonical({"metric": metric, "sample": sample}))[:20]
        result = {"metric": name, "sigma": round(z, 6), "tier": tier, "action": action,
                  "owner": metric["owner"], "evidence_id": key, "sample_timestamp": sample["timestamp"],
                  "allowed_tools": [], "authorization": "NONE", "runbook_execution": "DISABLED"}
        if tier >= 2:
            result["intent_proposal"] = {
                "id": "breach-" + name + "-" + key,
                "source": "monitor", "status": "proposed", "archetypes": metric["archetypes"],
                "problem": "Calibrated " + name + " control band breached",
                "evidence_id": key, "owner": metric["owner"],
                "required_before_spec": ["Human triage", "Complete compliance assessment", "Product-owner acceptance"],
            }
        results.append(result)
    require(set(samples) == names, "Unknown metrics in sample payload")
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("samples", help="Explicit project-relative JSON file")
    parser.add_argument("--bands", default="monitoring/bands.yaml", help="Strict JSON (YAML subset) configuration")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--now", help="Explicit clock for replay tests; production uses UTC clock")
    args = parser.parse_args()
    try:
        now = utc_time(args.now) if args.now else datetime.now(timezone.utc)
        results = evaluate(load_json(read_text(args.root, args.bands)), load_json(read_text(args.root, args.samples)), now)
        print(json.dumps({"result": "EVALUATED", "observations": results}, indent=2))
        return 0
    except (Invalid, OSError, UnicodeError, TypeError, RuntimeError) as exc:
        print(json.dumps({"result": "ESCALATE", "reason": str(exc), "runbook_execution": "DISABLED"}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
