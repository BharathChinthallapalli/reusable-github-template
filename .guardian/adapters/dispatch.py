"""Translate native hook envelopes without granting host permissions."""

import argparse
import json
from pathlib import Path
import sys

MAX_INPUT = 1_048_576
WORKSPACE = Path(__file__).resolve().parents[2]


def response(runtime, surface, event, decision):
    """An accepted review resumes normal permissions; it never auto-approves."""
    if decision.get("decision") in {"AUTO_ALLOW", "APPROVED"}:
        return {}, 0
    reason = decision.get("rationale") or "Guardian denied this operation."
    if event.lower() == "permissionrequest":
        if runtime == "copilot":
            return {"behavior": "deny", "message": reason}, 2
        return {"hookSpecificOutput": {
            "hookEventName": "PermissionRequest",
            "decision": {"behavior": "deny", "message": reason},
        }}, 2
    body = {"permissionDecision": "deny", "permissionDecisionReason": reason}
    if runtime == "copilot" and surface != "vscode":
        return body, 2
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", **body}}, 2


def resolve_surface(runtime, requested, payload):
    if requested != "auto":
        return requested
    # Snake-case is shared by multiple hosts: an envelope alone cannot prove VS Code.
    if runtime == "copilot" and "toolName" in payload:
        return "unknown"
    return "unknown"


def main(argv=None, stream=None):
    runtime, surface, event = "copilot", "unknown", "PreToolUse"
    wire_surface = surface
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--runtime", choices=["copilot", "claude", "codex"], required=True)
        parser.add_argument("--surface", choices=["cli", "vscode", "cloud", "auto", "unknown"], default="auto")
        parser.add_argument("--event", default="PreToolUse")
        args = parser.parse_args(argv)
        runtime, surface, event = args.runtime, args.surface, args.event
        raw = (stream or sys.stdin).read(MAX_INPUT + 1)
        if len(raw) > MAX_INPUT:
            raise ValueError("oversized hook input")
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            raise ValueError("hook input must be an object")
        surface = resolve_surface(runtime, surface, payload)
        # The trusted configured invocation selects the gate event, never tool input.
        payload["_guardian_event"] = event
        wire_surface = "vscode" if runtime == "copilot" and "tool_name" in payload else surface
        sys.path.insert(0, str(WORKSPACE / ".guardian" / "engine"))
        from gate import decide

        decision = decide(payload, runtime=runtime, surface=surface, workspace=WORKSPACE)
        # Copilot's PascalCase protocol needs nested output even when surface is unknown.
        output, code = response(runtime, wire_surface, event, decision)
    except BaseException as exc:
        # Do not print raw exceptions: tool input can contain secrets.
        decision = {"decision": "HARD_DENY", "rationale":
                    f"Guardian unavailable ({type(exc).__name__}); operation denied."}
        output, code = response(runtime, wire_surface, event, decision)
    print(json.dumps(output, separators=(",", ":")))
    if code:
        print(decision.get("rationale") or "Guardian denied this operation.", file=sys.stderr)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
