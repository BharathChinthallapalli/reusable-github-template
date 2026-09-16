"""Compute metrics from explicit observed events; unavailable data is never zero."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from sdlc_contracts import Invalid, object_keys, read_text, load_json, require, utc_time
from sdlc_monitor import number

KINDS = {"conversation", "intent", "accepted", "rejected", "spec", "tasks", "breach", "fix",
         "pr_opened", "pr_merged", "eval", "cost", "success", "gate_wait", "production_violation", "incident"}


def average(values: list[float]) -> float | None:
    return round(number(sum(values), "aggregate") / len(values), 6) if values else None


def compute(events: list[dict]) -> dict:
    require(isinstance(events, list) and len(events) <= 10000, "Invalid event batch")
    by_change = {}
    seen = set()
    amounts = {name: [] for name in ("eval", "cost", "gate_wait")}
    for event in events:
        object_keys(event, {"event_id", "change", "kind", "timestamp", "value"})
        require(all(isinstance(event[k], str) and event[k] for k in ("event_id", "change", "kind")), "Invalid event identity")
        require(event["event_id"] not in seen, "Duplicate event ID")
        seen.add(event["event_id"])
        kind = event["kind"]
        require(kind in KINDS, "Unknown metric event")
        at = utc_time(event["timestamp"])
        if kind in amounts:
            value = number(event["value"], kind)
            require(value >= 0 and (kind != "eval" or value in {0, 1}), "Invalid metric value")
            amounts[kind].append(value)
        else:
            require(event["value"] is None, "Non-measurement events require null value")
        by_change.setdefault(event["change"], {}).setdefault(kind, []).append(at)

    def elapsed(start: str, end: str) -> float | None:
        values = []
        for change in by_change.values():
            if start in change and end in change:
                seconds = (min(change[end]) - min(change[start])).total_seconds()
                require(seconds >= 0, "Inconsistent event chronology: " + start + " -> " + end)
                values.append(seconds)
        return average(values)

    def count(kind: str) -> int:
        return sum(kind in change for change in by_change.values())

    require(all(not ({"accepted", "rejected"} <= c.keys()) for c in by_change.values()), "Conflicting acceptance outcomes; use versioned change IDs")
    successes = count("success")
    decided = count("accepted") + count("rejected")
    return {
        "evidence": {"events": len(events), "changes": len(by_change), "authority": "CALLER_SUPPLIED_NOT_AUTHENTICATED"},
        "conversation_to_intent_seconds": elapsed("conversation", "intent"),
        "intent_survival_rate": count("accepted") / decided if decided else None,
        "intent_to_spec_seconds": elapsed("intent", "spec"),
        "breach_to_intent_seconds": elapsed("breach", "intent"),
        "pr_cycle_seconds": elapsed("pr_opened", "pr_merged"),
        "eval_pass_rate": average(amounts["eval"]),
        "gate_wait_seconds": average(amounts["gate_wait"]),
        "cost_per_successful_task": number(sum(amounts["cost"]), "aggregate cost") / successes if successes and amounts["cost"] else None,
        "spec_rework_after_first_tasks": None,
        "gate_violations_reaching_production": count("production_violation") if count("production_violation") else None,
        "findings_to_merged_fixes": None,
        "repeat_incidents_per_class": None,
        "unavailable_reason": "No complete inventory, class taxonomy, Git revision adapter or production denominator supplied; null is not zero.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("events", help="Project-relative JSON array of observed events")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        print(json.dumps(compute(load_json(read_text(args.root, args.events))), indent=2))
        return 0
    except (Invalid, OSError, UnicodeError, TypeError, RuntimeError) as exc:
        print(json.dumps({"result": "BLOCKED", "reason": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
