"""Gate protected edits against explicit ADD scope and check delivered design bindings."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile

if __package__:
    from .check_ai_configuration import ROOT, read_frontmatter, yaml
else:
    from check_ai_configuration import ROOT, read_frontmatter, yaml


PROTECTED_FOLDERS = (
    ".agents/skills", ".github/agents", ".github/instructions", ".github/hooks", "hooks",
)
PROTECTED_FILES = (
    "AGENTS.md", "CLAUDE.md", ".github/copilot-instructions.md", ".codex/hooks.json",
    "tools/check_design.py", "tools/install_hook_tools.py", ".pre-commit-config.yaml",
    "ruff.toml", ".gitleaks.toml", ".github/workflows/ci.yml",
    ".github/workflows/copilot-setup-steps.yml",
    "tools/check_ai_configuration.py", "requirements-dev.txt", ".gitignore",
)
REQUIRED_SECTIONS = (
    "Purpose", "Scope and non-goals", "Inputs and outputs", "Capabilities and permissions",
    "Behavior and failure modes", "Validation", "Risks and alternatives",
)
FIELDS = {"schema_version", "id", "status", "scope", "adrs", "binding_sha256"}
LIMITATION = ("Design readiness is a structural planning gate, not permission or human approval. "
              "Reviewers remain responsible for design accuracy and task authorization.")


@dataclass(frozen=True)
class Design:
    path: Path
    metadata: dict
    body: str


def protected(relative: str) -> bool:
    return relative in PROTECTED_FILES or any(
        relative.startswith(folder + "/") for folder in PROTECTED_FOLDERS)


def safe_file(root: Path, relative: object, errors: list[str], label: str) -> Path | None:
    if (not isinstance(relative, str) or not relative or
            any(character in relative for character in "\\:*?[]\x00\n\r") or
            relative.startswith("/") or
            any(part in {"", ".", ".."} for part in relative.split("/"))):
        errors.append(f"{label}: expected an explicit repository-relative file path without globs")
        return None
    path = root / relative
    if any((root / parent).is_symlink() for parent in (PurePosixPath(relative), *PurePosixPath(relative).parents)):
        errors.append(f"{label}: symlink paths are not allowed")
        return None
    if not path.resolve().is_relative_to(root):
        errors.append(f"{label}: path escapes the repository")
        return None
    if path.exists() and not path.is_file():
        errors.append(f"{label}: scope must name a file, not a directory or special file")
        return None
    return path


def validate_sections(body: str, label: str, errors: list[str]) -> None:
    # Comments and code fences cannot supply the explanatory design narrative.
    narrative = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    sections: dict[str, str] = {}
    current = None
    fence = ""
    for line in narrative.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                fence = ""
            continue
        if marker:
            fence = marker[1]
            continue
        if line.startswith(("    ", "\t")):
            continue
        if line.startswith("## "):
            current = line[3:].strip()
            if current in sections:
                errors.append(f"{label}: duplicate section {current}")
            sections[current] = ""
        elif line.startswith("# "):
            current = None
        elif current is not None:
            sections[current] += line + "\n"
    for heading in REQUIRED_SECTIONS:
        text = sections.get(heading, "").strip()
        placeholder = (not text or not re.search(r"[A-Za-z0-9]", text) or
                       re.search(r"\b(?:TODO|TBD|FIXME)\b|\[Describe\b|Replace this\b", text, re.I))
        if placeholder:
            errors.append(f"{label}: ready ADD needs a filled '{heading}' section without placeholders")


def read_design(root: Path, path: Path, errors: list[str]) -> Design | None:
    label = path.relative_to(root).as_posix()
    before = len(errors)
    if safe_file(root, label, errors, label) is None:
        return None
    metadata = read_frontmatter(path, label, errors)
    if metadata is None:
        return None
    unknown = set(metadata) - FIELDS
    if unknown:
        errors.append(f"{label}: unknown frontmatter fields: {', '.join(sorted(map(str, unknown)))}")
    if type(metadata.get("schema_version")) is not int or metadata["schema_version"] != 1:
        errors.append(f"{label}: schema_version must be 1")
    identifier = metadata.get("id")
    if not isinstance(identifier, str) or re.fullmatch(r"ADD-[0-9]{4}", identifier) is None:
        errors.append(f"{label}: id must use ADD-0001 format")
    status = metadata.get("status")
    if not isinstance(status, str) or status not in {"draft", "ready", "retired"}:
        errors.append(f"{label}: status must be draft, ready, or retired")
    for field in ("scope", "adrs"):
        values = metadata.get(field)
        if not isinstance(values, list) or any(not isinstance(value, str) for value in values):
            errors.append(f"{label}: {field} must be a list of explicit file paths")
            continue
        if status == "ready" and not values:
            errors.append(f"{label}: ready ADD requires a nonempty {field}")
        if len(values) != len(set(values)):
            errors.append(f"{label}: duplicate {field} paths")
        for relative in values:
            dependency = safe_file(root, relative, errors, f"{label} {field}")
            if field == "scope" and relative.startswith("docs/add/"):
                errors.append(f"{label}: ADD records bind their own design; do not include docs/add in scope")
            if field == "adrs" and dependency is not None:
                if (PurePosixPath(relative).parent != PurePosixPath("docs/adr") or
                        re.fullmatch(r"[0-9]{4}-.+\.md", dependency.name) is None or
                        not dependency.is_file()):
                    errors.append(f"{label}: ADR must name an existing numbered file under docs/adr")
                elif status == "ready":
                    statuses = re.findall(r"^Status: (.+)$", dependency.read_text(encoding="utf-8"), re.M)
                    if statuses != ["Accepted"]:
                        errors.append(f"{label}: ready ADD must reference a current Accepted ADR: {relative}")
    binding = metadata.get("binding_sha256", "")
    if not isinstance(binding, str) or (binding and re.fullmatch(r"[0-9a-f]{64}", binding) is None):
        errors.append(f"{label}: binding_sha256 must be empty or a SHA-256 hex digest")
    lines = path.read_text(encoding="utf-8-sig").splitlines(keepends=True)
    end = next(index for index in range(1, len(lines)) if lines[index].rstrip() == "---")
    body = "".join(lines[end + 1:])
    if status == "ready":
        validate_sections(body, label, errors)
    if len(errors) != before:
        return None
    return Design(path, metadata, body)


def designs(root: Path, errors: list[str]) -> list[Design]:
    records = []
    identifiers = set()
    folder = root / "docs/add"
    if folder.is_symlink():
        errors.append("docs/add: design directory must not be a symlink")
        return records
    for path in sorted(folder.glob("*.md")):
        if path.name in {"README.md", "template.md"}:
            continue
        record = read_design(root, path, errors)
        if record is None:
            continue
        if record.metadata["id"] in identifiers:
            errors.append(f"{path.relative_to(root)}: duplicate ADD id {record.metadata['id']}")
        identifiers.add(record.metadata["id"])
        records.append(record)
    return records


def file_digest(path: Path) -> dict[str, str]:
    if not path.exists():
        return {"state": "absent"}
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeError:
        state = "binary"
    else:
        state = "utf8"
        data = text.replace("\r\n", "\n").encode("utf-8")
    return {"state": state, "sha256": hashlib.sha256(data).hexdigest()}


def binding(root: Path, record: Design) -> str:
    metadata = {key: value for key, value in record.metadata.items() if key != "binding_sha256"}
    dependencies = sorted(set(metadata["scope"] + metadata["adrs"]))
    payload = {"metadata": metadata, "body": record.body.replace("\r\n", "\n"),
               "files": {relative: file_digest(root / relative) for relative in dependencies}}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def generated_bytecode(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return ("__pycache__" in relative.parts[:-1] and path.suffix in {".pyc", ".pyo"}
            and not any((root / part).is_symlink() for part in (relative, *relative.parents))
            and path.is_file())


def current_protected_paths(root: Path) -> list[str]:
    paths = {relative for relative in PROTECTED_FILES
             if (root / relative).exists() or (root / relative).is_symlink()}
    for relative in PROTECTED_FOLDERS:
        folder = root / relative
        if folder.is_symlink():
            paths.add(relative)
        else:
            paths.update(path.relative_to(root).as_posix() for path in folder.rglob("*")
                         if (path.is_file() or path.is_symlink()) and not generated_bytecode(path, root))
    return sorted(paths)


def check(root: Path, paths: list[str] | None = None) -> tuple[list[str], list[str]]:
    root = root.resolve(strict=True)
    errors: list[str] = []
    records = designs(root, errors)
    owners: dict[str, list[str]] = {}
    for record in records:
        if record.metadata["status"] != "ready":
            continue
        for relative in record.metadata["scope"]:
            owners.setdefault(relative, []).append(record.path.relative_to(root).as_posix())
        if paths is None and record.metadata.get("binding_sha256") != binding(root, record):
            errors.append(f"{record.path.relative_to(root)}: binding does not match the current design and files; "
                          "review the change, then run --seal for this ADD")
    for relative, covering in owners.items():
        if protected(relative) and len(covering) > 1:
            errors.append(f"{relative}: multiple ready ADDs cover the same protected path")
    selected = current_protected_paths(root) if paths is None else paths
    for relative in selected:
        if safe_file(root, relative, errors, "selected path") is None:
            continue
        if protected(relative) and not owners.get(relative):
            errors.append(f"{relative}: no ready ADD covers this protected path; complete explicit scope before editing")
    return errors, [LIMITATION]


def seal(root: Path, relative: str) -> list[str]:
    root = root.resolve(strict=True)
    errors, _ = check(root, paths=[])
    path = safe_file(root, relative, errors, "--seal")
    if (path is None or path.parent != root / "docs/add" or
            path.suffix != ".md" or path.name in {"README.md", "template.md"}):
        errors.append("--seal must name one ADD record directly under docs/add")
    if errors:
        return errors
    record = read_design(root, path, errors)
    if record is None:
        return errors
    metadata = record.metadata | {"binding_sha256": binding(root, record)}
    source = "---\n" + yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True) + "---\n" + record.body
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(source)
        temporary.chmod(path.stat().st_mode)
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--paths", nargs="+", metavar="PATH",
                      help="gate planned paths using scope and structure; allow in-progress content drift")
    mode.add_argument("--seal", metavar="ADD", help="record one ADD's current binding without changing status")
    args = parser.parse_args()
    try:
        if args.seal:
            errors = seal(args.root, args.seal)
            notes = [LIMITATION]
        else:
            errors, notes = check(args.root, args.paths)
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        print(f"Design check failed: {exc}", file=sys.stderr)
        return 1
    for note in notes:
        print(f"Note: {note}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    if args.seal:
        print(f"Recorded binding for {args.seal}; design status was preserved.")
    elif args.paths is not None:
        print("Planned-path design gate passed. Delivery bindings were not checked.")
    else:
        print("Design records, protected-path coverage, and delivery bindings passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
