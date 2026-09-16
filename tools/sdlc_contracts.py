"""Bounded local artifact checks. Structural readiness is never execution authority."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import sys
from datetime import datetime
from pathlib import Path, PurePosixPath

LIMIT = 512 * 1024
MARKER = re.compile(r"\b(?:TBD|TODO|FIXME|TBC)\b|\[\s*insert\b", re.I)
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
RID = re.compile(r"R-[1-9][0-9]*")
TID = re.compile(r"T-[1-9][0-9]*")
ARCHETYPES = {
    "A": ("API contract", "Data model and migrations", "Auth matrix", "Performance budgets", "Accessibility and i18n"),
    "B": ("Trigger catalogue", "Idempotency and retries", "Connector inventory", "Tenant and region flows", "Run retention and DLP"),
    "C": ("Model choice and pinning", "Grounding and data cards", "Prompt versions", "Eval plan", "Human oversight", "Fallback and deprecation"),
    "D": ("Agent roster", "Orchestration and termination", "Inter-agent trust", "State and checkpoints", "Human oversight", "Containment and budgets"),
    "E": ("Data lineage", "Feature definitions", "Training and eval splits", "Bias and fairness", "Retraining and retirement"),
}
COMMON_DESIGN = ("Architecture", "Data flows", "Threat model", "Compliance", "Cost model", "Well-Architected")
ARCHETYPES["D"] = ARCHETYPES["C"] + ARCHETYPES["D"]
AI_DESIGN = ("AI supply chain", "AI threat model", "Data governance", "Eval plan", "Human oversight")
COMMON_INTENT = ("Problem", "Proposed outcome", "Affected users and systems", "Constraints", "Open questions", "Compliance")


class Invalid(ValueError):
    """Invalid or incomplete untrusted artifact; safe to report without its contents."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Invalid(message)


def object_keys(value: object, required: set[str], optional: set[str] | None = None) -> None:
    require(isinstance(value, dict), "Expected an object")
    require(required <= value.keys(), "Required fields missing: " + ", ".join(sorted(required - value.keys())))
    require(not (value.keys() - required - (optional or set())), "Unknown fields are not accepted")


def pairs(items: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in items:
        require(key not in result, "Duplicate JSON key")
        result[key] = value
    return result


def reject_constant(_: str) -> None:
    raise Invalid("Non-finite JSON numbers are not accepted")


def load_json(source: str) -> object:
    require(len(source.encode("utf-8")) <= LIMIT, "Input exceeds 512 KiB")
    try:
        return json.loads(source, object_pairs_hook=pairs, parse_constant=reject_constant)
    except Invalid:
        raise
    except (ValueError, RecursionError) as exc:
        raise Invalid("Malformed or excessively nested JSON") from exc


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode()


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def relative_name(name: str) -> str:
    require(isinstance(name, str) and 0 < len(name) <= 240, "Invalid relative path length")
    require(not any(ord(c) < 32 for c in name), "Control character in path")
    require(not any(c in name for c in "\\:*?[]%"), "Ambiguous or non-literal path")
    parts = name.split("/")
    require(all(p not in {"", ".", ".."} and p == p.rstrip(" .") for p in parts), "Unsafe path components")
    require(not PurePosixPath(name).is_absolute(), "Absolute path refused")
    return name


def scoped_path(root: Path, name: str) -> Path:
    relative_name(name)
    root = root.resolve(strict=True)
    path = root
    for component in name.split("/"):
        path /= component
        require(not path.is_symlink() and not path.is_junction(), "Linked path refused")
    require(path.resolve(strict=False).is_relative_to(root), "Path escapes project")
    return path


def read_text(root: Path, name: str) -> str:
    relative_name(name)
    private = {".ssh", ".aws", ".azure", ".kube", "appdata", "credentials", "vault", "protect", "login data", "cookies", "local state", "consolehost_history.txt"}
    require(not any(p.casefold() in private or p.casefold().startswith(".env") for p in name.split("/")), "Sensitive input path refused")
    require(Path(name).suffix.lower() not in {".ost", ".pst", ".pem", ".key", ".pfx"}, "Sensitive input file refused")
    path = scoped_path(root, name)
    require(stat.S_ISREG(path.stat().st_mode), "Input must be a regular file")
    require(path.stat().st_size <= LIMIT, "Input exceeds 512 KiB")
    with path.open("rb") as stream:
        data = stream.read(LIMIT + 1)
    require(len(data) <= LIMIT, "Input exceeds 512 KiB")
    return data.decode("utf-8").replace("\r\n", "\n")


def parse_document(text: str, kind: str) -> tuple[dict, str]:
    require(text.startswith("---\n"), "Strict JSON frontmatter is required")
    header, separator, body = text[4:].partition("\n---\n")
    require(bool(separator), "Frontmatter terminator missing")
    metadata = load_json(header)
    require(isinstance(metadata, dict), "Frontmatter must be an object")
    require(type(metadata.get("schema_version")) is int and metadata["schema_version"] == 1, "Unsupported schema version")
    require(metadata.get("kind") == kind, "Artifact kind mismatch")
    require(bool(SLUG.fullmatch(metadata.get("id", ""))), "Invalid change identifier")
    return metadata, body


def document(root: Path, name: str, kind: str) -> tuple[dict, str]:
    return parse_document(read_text(root, name), kind)


def sections(body: str) -> dict[str, str]:
    result = {}
    current = None
    fence = None
    for line in body.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            fence = None if fence == marker else (marker if fence is None else fence)
        if fence is None and line.startswith("## "):
            current = line[3:].strip()
            require(current not in result, "Duplicate section heading")
            result[current] = ""
        elif current is not None:
            result[current] += line + "\n"
    require(fence is None, "Unclosed Markdown code fence")
    return result


def section_check(body: str, names: tuple[str, ...]) -> None:
    found = sections(body)
    for name in names:
        require(name in found and bool(found[name].strip()), "Missing or empty section: " + name)
    require(not MARKER.search(body), "Unresolved placeholder requires clarification")


def text_value(value: object, field: str) -> None:
    require(isinstance(value, str) and bool(value.strip()) and len(value) <= 10000, "Missing or invalid " + field)
    require(not MARKER.search(value), "Unresolved marker in " + field)


def utc_time(value: str) -> datetime:
    require(isinstance(value, str), "Timestamp must be a string")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise Invalid("Invalid ISO timestamp") from exc
    require(result.tzinfo is not None, "Timestamp needs timezone")
    return result


def compliance(value: object) -> None:
    required = {"ai_act", "gdpr", "betrvg", "nis2"}
    object_keys(value, required)
    for framework, assessment in value.items():
        object_keys(assessment, {"applicability", "reason", "owner"})
        require(assessment["applicability"] in {"applicable", "not_applicable", "requires_assessment"}, "Unknown compliance applicability")
        text_value(assessment["reason"], framework + " reason")
        text_value(assessment["owner"], framework + " owner")
        require(assessment["applicability"] != "requires_assessment", framework + " assessment is unresolved")


def intent_check(meta: dict, body: str) -> None:
    object_keys(meta, {"schema_version", "kind", "id", "author", "created_at", "source", "priority", "archetypes", "compliance"})
    text_value(meta["author"], "author")
    utc_time(meta["created_at"])
    require(meta["source"] in {"human", "ticket", "researcher", "reviewer", "monitor"}, "Unknown intent source")
    require(meta["priority"] in {"normal", "urgent"}, "Unknown priority")
    archetypes = meta["archetypes"]
    require(isinstance(archetypes, list) and archetypes and all(isinstance(x, str) for x in archetypes), "Archetypes required")
    require(len(set(archetypes)) == len(archetypes) and set(archetypes) <= ARCHETYPES.keys(), "Unknown or duplicate archetype")
    compliance(meta["compliance"])
    required = COMMON_INTENT
    if set(archetypes) & {"C", "D", "E"}:
        required += ("Feasibility", "Measurable KPIs", "Ethical impact", "Regulatory review")
    section_check(body, required)


def reference(root: Path, value: object) -> None:
    require(isinstance(value, str), "Reference must be an explicit project path")
    relative_name(value)
    # Reference discovery never reads user profiles, credentials or environment files.
    require(value.split("/")[0] in {"intent", "specs", "docs", "src", "app", "tests", "evals", "mlops", "llmops", "runbooks"}, "Reference outside artifact/source scope")
    require(not any(p.startswith(".") for p in value.split("/")), "Private reference path refused")
    require(Path(value).suffix.lower() not in {".ost", ".pst", ".pem", ".key", ".pfx"}, "Sensitive reference refused")
    require(scoped_path(root, value).is_file(), "Reference does not resolve: " + value)


def string_list(value: object, label: str, nonempty: bool = True) -> list[str]:
    require(isinstance(value, list) and (not nonempty or value), label + " must be a list")
    require(all(isinstance(x, str) and x for x in value), label + " entries must be strings")
    require(len(set(value)) == len(value), "Duplicate " + label)
    return value


def ears(value: object) -> None:
    text_value(value, "acceptance criterion")
    patterns = (
        r"The .+ shall .+\.",
        r"(?:When|While|Where) .+, the .+ shall .+\.",
        r"If .+, then the .+ shall .+\.",
    )
    require(any(re.fullmatch(p, value) for p in patterns), "Acceptance criterion must use supported EARS form")


def requirements_check(root: Path, meta: dict) -> set[str]:
    object_keys(meta, {"schema_version", "kind", "id", "requirements"})
    require(isinstance(meta["requirements"], list) and meta["requirements"], "Requirements cannot be empty")
    identifiers = set()
    for item in meta["requirements"]:
        object_keys(item, {"id", "story", "acceptance", "verification"})
        require(isinstance(item["id"], str) and RID.fullmatch(item["id"]) and item["id"] not in identifiers, "Invalid or duplicate requirement ID")
        identifiers.add(item["id"])
        text_value(item["story"], "user story")
        ears(item["acceptance"])
        for ref in string_list(item["verification"], "verification"):
            require(ref.startswith(("tests/", "evals/")), "Requirement needs a test or eval reference")
            reference(root, ref)
    return identifiers


def tasks_check(root: Path, meta: dict, requirements: set[str]) -> None:
    object_keys(meta, {"schema_version", "kind", "id", "status", "tasks"})
    require(meta["status"] in {"proposed", "accepted"}, "Tasks status must be proposed or accepted")
    require(isinstance(meta["tasks"], list) and meta["tasks"], "Tasks cannot be empty")
    tasks = {}
    covered = set()
    for task in meta["tasks"]:
        object_keys(task, {"id", "requirements", "depends_on", "wave", "surface", "acceptance", "done", "verification"})
        identifier = task["id"]
        require(isinstance(identifier, str) and TID.fullmatch(identifier) and identifier not in tasks, "Invalid or duplicate task ID")
        tasks[identifier] = task
        refs = string_list(task["requirements"], "task requirements")
        require(set(refs) <= requirements, "Unknown task requirement")
        covered.update(refs)
        require(type(task["wave"]) is int and 1 <= task["wave"] <= 1000, "Wave must be a positive bounded integer")
        string_list(task["depends_on"], "dependencies", nonempty=False)
        for name in string_list(task["surface"], "surface"):
            scoped_path(root, name)  # Future target files may not exist yet.
        ears(task["acceptance"])
        text_value(task["done"], "done-state")
        for name in string_list(task["verification"], "task verification"):
            require(name.startswith(("tests/", "evals/")), "Task verification must cite tests or evals")
            reference(root, name)
    require(covered == requirements, "Every requirement needs an implementing task")
    for task in tasks.values():
        for dependency in task["depends_on"]:
            require(dependency in tasks, "Unknown task dependency")
            require(tasks[dependency]["wave"] < task["wave"], "Dependency must be in an earlier wave; cycles refused")


def spec_check(root: Path, change: str) -> tuple[str, dict]:
    require(isinstance(change, str) and SLUG.fullmatch(change), "Invalid change ID")
    sources = {}
    data = {}
    for kind, path in (("intent", f"intent/{change}/intent.md"), *[(k, f"specs/{change}/{k}.md") for k in ("requirements", "design", "tasks")]):
        source = read_text(root, path)
        meta, body = parse_document(source, kind)
        require(meta["id"] == change, "Change ID mismatch")
        sources[path] = source
        data[kind] = (meta, body)
    intent_check(*data["intent"])
    reqs = requirements_check(root, data["requirements"][0])
    design, body = data["design"]
    object_keys(design, {"schema_version", "kind", "id", "compliance", "concerns"})
    compliance(design["compliance"])
    require(design["compliance"] == data["intent"][0]["compliance"], "Intent/design compliance drift requires review")
    require(design["concerns"] == [], "Flagged design concerns must be resolved before rendering")
    names = set(COMMON_DESIGN)
    for archetype in data["intent"][0]["archetypes"]:
        names.update(ARCHETYPES[archetype])
    if set(data["intent"][0]["archetypes"]) & {"C", "D", "E"}:
        names.update(AI_DESIGN)
    section_check(body, tuple(sorted(names)))
    tasks_check(root, data["tasks"][0], reqs)
    rendered = "# Rendered specification: " + change + "\n\n"
    hashes = {path: digest(text.encode()) for path, text in sources.items()}
    rendered += "<!-- source-sha256: " + canonical(hashes).decode() + " -->\n\n"
    for kind in ("requirements", "design"):
        rendered += sources[f"specs/{change}/{kind}.md"] + "\n\n"
    return rendered, {"result": "STRUCTURALLY_READY", "change": change, "source_hashes": hashes,
                      "authorization": "UNVERIFIED", "dispatch": "BLOCKED_PENDING_AUTHENTICATED_ACCEPTANCE"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("change")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--render", action="store_true", help="Print validated spec to stdout; does not write or accept it")
    args = parser.parse_args()
    try:
        rendered, report = spec_check(args.root, args.change)
        print(rendered if args.render else json.dumps(report, indent=2))
        return 0
    except (Invalid, OSError, UnicodeError, TypeError, RuntimeError) as exc:
        print(json.dumps({"result": "BLOCKED", "reason": str(exc), "dispatch": "BLOCKED"}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
