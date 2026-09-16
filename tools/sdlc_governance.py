# SPDX-License-Identifier: Apache-2.0
# Modified adaptation of AI-SDLC governance concepts; see NOTICE for exact sources.
"""Deterministic governance evidence. No result grants execution or merge authority."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
from pathlib import Path

from sdlc_contracts import (
    Invalid, MARKER, ears, load_json, object_keys, read_text, reference,
    relative_name, require, string_list, text_value,
)

PROTECTED = (
    ".guardian/**", ".github/**", ".claude/**", ".codex/**", ".agents/**", ".ai-sdlc/**",
    "hooks/**", "rules/**", "tests/**", "evals/**", "scripts/**", "tools/**",
    "AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md", "CODEOWNERS", "docs/add/**",
    ".pre-commit-config.*", "*.lock", "*.lockb", "package-lock.json", "**/package-lock.json",
    "pnpm-lock.yaml", "**/pnpm-lock.yaml", "npm-shrinkwrap.json", "**/npm-shrinkwrap.json",
    "Pipfile.lock", "requirements*.txt", "compliance/**", "monitoring/**",
)
ALLOWED_MUTATIONS = ("src/**", "app/**", "docs/**", "intent/**", "specs/**", "mlops/**", "llmops/**")
USES = re.compile(r"\buses\s*:", re.I)
VISION_ANTI_PATTERN = re.compile(r"\bwe(?:'|’)ll\s+document\s+(?:it\s+)?after\b", re.I)
IMMEDIATE = {"GuardianDenied", "PivotAttempt", "HookTimeoutFailOpen"}
RETRY_BUDGETS = {"TransientReadFailure": 2, "ValidationFailure": 1, "ReviewFailure": 1, "Conflict": 0}
HARNESSES = {"codex", "claude", "copilot"}


def dor_task(root: Path, task: dict, task_ids: set[str], *, verified_source: str | None = None) -> dict:
    """verified_source belongs to an external trusted caller, never task JSON.

    No CLI in this repository supplies it. Fixture use exercises the intended
    shortcut, not source authentication. Even passing results cannot dispatch.
    """
    object_keys(task, {"id", "requirements", "depends_on", "wave", "surface", "acceptance", "done", "verification"})
    require(verified_source in {None, "spec-job", "monitor"}, "Unknown verified source")
    checks = {}

    def gate(number: int, check) -> None:
        try:
            check()
            checks[str(number)] = {"result": "PASS", "basis": "deterministic structural check"}
        except (Invalid, OSError, TypeError) as exc:
            checks[str(number)] = {"result": "FAIL", "reason": str(exc)}

    def no_markers() -> None:
        require(not MARKER.search(json.dumps(task)), "Unresolved marker: request clarification")

    def refs() -> None:
        for path in string_list(task["verification"], "verification"):
            reference(root, path)
        require(bool(string_list(task["requirements"], "requirements")), "Requirement reference required")

    def scope() -> None:
        require(1 <= len(string_list(task["surface"], "surface")) <= 5, "Junior task exceeds five named files")

    def surface() -> None:
        for path in string_list(task["surface"], "surface"):
            relative_name(path)

    def dependencies() -> None:
        for dep in string_list(task["depends_on"], "dependencies", nonempty=False):
            require(dep in task_ids and dep != task["id"], "Unknown or self dependency")

    functions = {1: lambda: ears(task["acceptance"]), 2: no_markers, 3: refs,
                 4: scope, 5: surface, 6: lambda: text_value(task["done"], "done-state"), 7: dependencies}
    skipped = {1, 4, 5, 6} if verified_source else set()
    for number, function in functions.items():
        if number in skipped:
            checks[str(number)] = {"result": "SKIPPED", "basis": "caller-verified " + verified_source}
        else:
            gate(number, function)
    failed = any(v["result"] == "FAIL" for v in checks.values())
    return {"result": "BLOCKED" if failed else "STRUCTURALLY_READY", "gates": checks,
            "semantic_review": "REQUIRED" if not verified_source else "SHORTCUT_POLICY",
            "authorization": "NOT_EVALUATED", "dispatch": "BLOCKED_PENDING_AUTHENTICATED_ACCEPTANCE"}


def path_matches(path: str, patterns: tuple[str, ...]) -> bool:
    return any(fnmatch.fnmatchcase(path.casefold(), pattern.casefold()) for pattern in patterns)


def change_gate(changes: list[dict], *, actor: str, tests_present: bool) -> dict:
    """Check a caller-supplied diff; caller must independently bind it to head/base.

    A contributor-provided manifest is not authenticated Git evidence. Both rename
    endpoints count and deletion lines count toward the total change budget.
    """
    require(actor in {"untrusted", "engineer"}, "Unknown contribution class")
    require(isinstance(changes, list) and changes, "Empty change evidence")
    violations = []
    paths = set()
    total = 0
    for change in changes:
        object_keys(change, {"path", "old_path", "added", "deleted", "binary", "linked"})
        require(isinstance(change["path"], str) and bool(change["path"]), "Change path is required")
        require(type(change["binary"]) is bool and type(change["linked"]) is bool, "Invalid change flags")
        require(change["old_path"] is None or isinstance(change["old_path"], str), "Invalid rename origin")
        for path in (change["path"], change["old_path"]):
            if path is None:
                continue
            relative_name(path)
            paths.add(path.casefold())
            if path_matches(path, PROTECTED):
                violations.append("Protected path: " + path)
            elif not path_matches(path, ALLOWED_MUTATIONS):
                violations.append("Path outside mutation allowlist: " + path)
        if change["binary"] or change["linked"]:
            violations.append("Binary or linked mutation needs human review")
        for field in ("added", "deleted"):
            require(isinstance(change[field], list) and all(isinstance(line, str) for line in change[field]), "Diff lines must be strings")
            total += len(change[field])
        if any(USES.search(line) for line in change["added"]):
            violations.append("New Actions uses reference requires trusted review")
        if change["path"].endswith("design.md") and VISION_ANTI_PATTERN.search("\n".join(change["added"])):
            violations.append("Design defers documentation: record it before build")
    if total > 200:
        violations.append("Change exceeds 200 added/deleted lines")
    if len(paths) > 5:
        violations.append("Change exceeds five paths (including rename origins)")
    docs_only = all(path.endswith(".md") and path.startswith(("docs/", "intent/", "specs/")) for path in paths)
    if not docs_only and tests_present is not True:
        violations.append("Non-docs change requires independently verified test evidence")
    return {"result": "BLOCKED" if violations else "DIFF_POLICY_PASS", "violations": violations,
            "changed_lines": total, "changed_paths": len(paths), "docs_only": docs_only,
            "evidence_authenticity": "CALLER_RESPONSIBILITY", "authorization": "NOT_EVALUATED",
            "dispatch": "BLOCKED_PENDING_AUTHENTICATED_DIFF_AND_APPROVAL"}


def review_independence(implementer: str, reviews: list[dict], *, docs_only: bool = False) -> dict:
    """Semantic precheck only; this is not an upstream v6 signature verifier."""
    require(implementer in HARNESSES, "Unknown implementation harness")
    require(type(docs_only) is bool, "Invalid docs-only classification")
    if docs_only:
        return {"result": "DOCS_ONLY_BYPASS", "authorization": "NOT_EVALUATED"}
    required = {"code-review", "test-review", "security-review"}
    seen = set()
    require(isinstance(reviews, list), "Reviews must be a list")
    for review in reviews:
        object_keys(review, {"stage", "harness", "verdict", "transcript_sha256"})
        require(review["stage"] in required and review["stage"] not in seen, "Unknown or duplicate review stage")
        seen.add(review["stage"])
        require(review["harness"] in HARNESSES and review["harness"] != implementer, "Reviewer harness must differ from implementer")
        require(review["verdict"] == "approved", "Review did not approve")
        require(isinstance(review["transcript_sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", review["transcript_sha256"]), "Invalid transcript hash")
    require(seen == required, "Missing required independent review")
    return {"result": "INDEPENDENCE_SHAPE_PASS", "signature": "UNVERIFIED",
            "authorization": "UNVERIFIED", "release": "BLOCKED_PENDING_TRUSTED_CI_ATTESTATION"}


def failure_action(mode: str, attempts: int) -> dict:
    require(isinstance(mode, str) and type(attempts) is int and attempts >= 0, "Invalid failure event")
    if mode in IMMEDIATE:
        return {"action": "ESCALATE_IMMEDIATELY", "mode": mode, "retry_budget": 0}
    if mode not in RETRY_BUDGETS:
        return {"action": "ESCALATE_UNKNOWN_FAILURE", "mode": mode, "retry_budget": 0}
    budget = RETRY_BUDGETS[mode]
    return {"action": "RETRY_READ_ONLY" if mode == "TransientReadFailure" and attempts < budget else "ESCALATE",
            "mode": mode, "retry_budget": budget}


def posture_check(posture: dict) -> dict:
    object_keys(posture, {"schema_version", "regimes", "overrides", "retention"})
    require(type(posture["schema_version"]) is int and posture["schema_version"] == 1, "Unknown posture version")
    regimes = string_list(posture["regimes"], "regimes", nonempty=False)
    require(set(regimes) <= {"EU-AI-Act", "GDPR", "NIS2", "BetrVG", "NIST-AI-RMF", "OWASP-LLM"}, "Unknown regime")
    require(isinstance(posture["overrides"], dict), "Overrides must be an object")
    for key, override in posture["overrides"].items():
        require(key in {"advisory_review", "soft_quality_threshold"}, "Hard controls cannot be overridden")
        object_keys(override, {"value", "_notes", "owner"})
        text_value(override["_notes"], "override _notes")
        text_value(override["owner"], "override owner")
    require(isinstance(posture["retention"], list), "Retention must be record-specific")
    for item in posture["retention"]:
        object_keys(item, {"record_class", "duration", "basis", "owner"})
        for key, value in item.items():
            text_value(value, "retention " + key)
    return {"result": "POSTURE_SHAPE_PASS", "attestation_required": bool(set(regimes) & {"EU-AI-Act", "NIS2", "BetrVG"}),
            "legal_assessment": "HUMAN_REQUIRED", "override_authority": "UNVERIFIED"}


def finding_check(finding: dict) -> None:
    object_keys(finding, {"severity", "summary", "failureScenario"})
    require(finding["severity"] in {"critical", "major", "minor", "info"}, "Unknown finding severity")
    text_value(finding["summary"], "finding summary")
    if finding["severity"] in {"critical", "major"}:
        text_value(finding["failureScenario"], "failureScenario")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("check", choices=["change", "review", "failure", "posture", "finding"])
    parser.add_argument("input", help="Explicit project-relative JSON file")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        value = load_json(read_text(args.root, args.input))
        if args.check == "change":
            object_keys(value, {"changes", "actor", "tests_present"})
            report = change_gate(**value)
        elif args.check == "review":
            object_keys(value, {"implementer", "reviews"})
            report = review_independence(**value)
        elif args.check == "failure":
            object_keys(value, {"mode", "attempts"})
            report = failure_action(**value)
        elif args.check == "finding":
            finding_check(value)
            report = {"result": "FINDING_SHAPE_PASS"}
        else:
            report = posture_check(value)
        print(json.dumps(report, indent=2))
        return 1 if report.get("result") == "BLOCKED" or report.get("action", "").startswith("ESCALATE") else 0
    except (Invalid, OSError, UnicodeError, TypeError, RuntimeError) as exc:
        print(json.dumps({"result": "BLOCKED", "reason": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
