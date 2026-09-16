"""Check all seven DoR structural signals; accepted labels cannot enable dispatch."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from sdlc_contracts import Invalid, document, spec_check  # noqa: E402
from sdlc_governance import dor_task  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("change")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        _, spec = spec_check(args.root, args.change)
        tasks, _ = document(args.root, f"specs/{args.change}/tasks.md", "tasks")
        identifiers = {task["id"] for task in tasks["tasks"]}
        reports = {task["id"]: dor_task(args.root, task, identifiers) for task in tasks["tasks"]}
        print(json.dumps({"spec": spec, "tasks": reports, "dispatch": "BLOCKED_PENDING_AUTHENTICATED_ACCEPTANCE"}, indent=2))
        return 1 if any(report["result"] == "BLOCKED" for report in reports.values()) else 0
    except (Invalid, OSError, UnicodeError, TypeError, RuntimeError) as exc:
        print(json.dumps({"result": "BLOCKED", "reason": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
