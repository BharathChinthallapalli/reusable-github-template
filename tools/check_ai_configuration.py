"""Read-only static checks for repository skills and custom-agent metadata."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys

try:
    import yaml
    from yaml.constructor import ConstructorError
except ModuleNotFoundError as exc:
    if exc.name != "yaml":
        raise
    if __name__ == "__main__":
        raise SystemExit("PyYAML is missing. Install dependencies with: python3 -m pip install -r requirements-dev.txt") from None
    raise


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
HOST_LIMITATION = "Host discovery and invocation: NOT CHECKED. Static validity does not establish host support or actual tool access."


@dataclass(frozen=True)
class Definition:
    path: Path
    kind: str
    name: str
    metadata: dict


class UniqueKeySafeLoader(yaml.SafeLoader):
    """Keep SafeLoader's constructors and reject repeated explicit YAML keys."""

    def construct_document(self, node):
        # Inspect the original node graph before SafeLoader expands YAML merges.
        pending = [node]
        visited = set()
        merge_key = object()
        while pending:
            current = pending.pop()
            if id(current) in visited:
                continue
            visited.add(id(current))
            if isinstance(current, yaml.SequenceNode):
                pending.extend(current.value)
            elif isinstance(current, yaml.MappingNode):
                keys = set()
                for key_node, value_node in current.value:
                    key = merge_key if key_node.tag == "tag:yaml.org,2002:merge" else self.construct_object(key_node)
                    try:
                        if key in keys:
                            raise ConstructorError(None, None, "duplicate YAML key", key_node.start_mark)
                        keys.add(key)
                    except TypeError as exc:
                        raise ConstructorError(None, None, "unhashable YAML key", key_node.start_mark) from exc
                    pending.extend((key_node, value_node))
        return super().construct_document(node)


def read_frontmatter(path: Path, relative: str, errors: list[str]) -> dict | None:
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeError) as exc:
        errors.append(f"{relative}: could not read UTF-8 frontmatter: {exc}")
        return None
    if not lines or lines[0].rstrip() != "---":
        errors.append(f"{relative}: missing opening YAML frontmatter delimiter")
        return None
    end = next((index for index in range(1, len(lines)) if lines[index].rstrip() == "---"), None)
    if end is None:
        errors.append(f"{relative}: missing closing YAML frontmatter delimiter")
        return None
    try:
        metadata = yaml.load("\n".join(lines[1:end]), Loader=UniqueKeySafeLoader)
    except (RecursionError, ValueError) as exc:
        errors.append(f"{relative}: YAML could not be parsed: {type(exc).__name__}: {exc}")
        return None
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        location = f" at line {mark.line + 2}" if mark else ""
        reason = getattr(exc, "problem", None) or "invalid document"
        errors.append(f"{relative}: invalid YAML{location}: {reason}")
        return None
    if not isinstance(metadata, dict):
        errors.append(f"{relative}: YAML frontmatter must be a mapping")
        return None
    return metadata


def validate_metadata(path: Path, kind: str, metadata: dict, errors: list[str]) -> str | None:
    relative = path.as_posix()
    default_name = path.name.removesuffix(".agent.md").removesuffix(".md") if kind == "agent" else None
    name = metadata.get("name", default_name)
    description = metadata.get("description")
    if not isinstance(name, str) or not name.strip():
        errors.append(f"{relative}: name must be a nonempty string")
        name = None
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{relative}: description must be a nonempty string")
    elif kind == "skill" and len(description) > 1024:
        errors.append(f"{relative}: description must not exceed 1024 characters")
    if kind == "skill" and name is not None:
        if len(name) > 64 or SKILL_NAME.fullmatch(name) is None:
            errors.append(f"{relative}: name must be 1-64 lowercase letters/digits with single separating hyphens")
        if name != path.parent.name:
            errors.append(f"{relative}: name must match its skill directory {path.parent.name!r}")
    for field in ("user-invocable", "disable-model-invocation"):
        if field in metadata and type(metadata[field]) is not bool:
            errors.append(f"{relative}: {field} must be a boolean")
    if kind == "agent":
        if "infer" in metadata and type(metadata["infer"]) is not bool:
            errors.append(f"{relative}: infer must be a boolean")
        if "tools" in metadata:
            tools = metadata["tools"]
            if isinstance(tools, str):
                tools = [tool.strip() for tool in tools.split(",")]
            if not isinstance(tools, list) or any(not isinstance(tool, str) or not tool.strip() for tool in tools):
                errors.append(f"{relative}: tools must contain nonempty strings in a YAML list or comma-separated string")
    return name


def describe_metadata(relative: str, kind: str, name: str, metadata: dict) -> str:
    user_invocable = metadata.get("user-invocable", True)
    model_eligible = not metadata.get("disable-model-invocation", False)
    description = (f"{relative}: {kind} name={json.dumps(name)}; "
                   f"current flags: user_invocable={json.dumps(user_invocable)}; "
                   f"model_invocation_eligible={json.dumps(model_eligible)}")
    if kind == "agent":
        tools = metadata.get("tools")
        if isinstance(tools, str):
            tools = [tool.strip() for tool in tools.split(",")]
        scopes = json.dumps(tools) if "tools" in metadata else "not declared (host defaults apply)"
        description += f"; declared tools={scopes}"
        if "infer" in metadata:
            description += "; deprecated infer present: effective legacy invocation eligibility=unverified"
    return description


def within_root(path: Path, root: Path, errors: list[str]) -> bool:
    relative = path.relative_to(root).as_posix()
    try:
        if path.resolve().is_relative_to(root):
            return True
        errors.append(f"{relative}: refuses to inspect a path outside selected root")
    except (OSError, RuntimeError) as exc:
        errors.append(f"{relative}: could not resolve path: {exc}")
    return False


def directory_entries(folder: Path, root: Path, errors: list[str]) -> list[Path]:
    if not within_root(folder, root, errors):
        return []
    try:
        return sorted(folder.iterdir())
    except FileNotFoundError:
        return []
    except OSError as exc:
        errors.append(f"{folder.relative_to(root).as_posix()}: could not inspect directory: {exc}")
        return []


def inspect_definitions(root: Path) -> tuple[list[Definition], list[str], list[str]]:
    """Load validated definitions and diagnostics without executing their content."""
    errors: list[str] = []
    notes = [HOST_LIMITATION]
    try:
        root = root.resolve(strict=True)
        if not root.is_dir():
            return [], [f"Invalid root: not a directory: {root}"], notes
    except (OSError, RuntimeError) as exc:
        return [], [f"Invalid root: {exc}"], notes

    definitions: list[tuple[str, Path]] = []
    for skill_root in (".agents/skills", ".github/skills"):
        for folder in directory_entries(root / skill_root, root, errors):
            if within_root(folder, root, errors) and folder.is_dir():
                definitions.append(("skill", folder / "SKILL.md"))
    for path in directory_entries(root / ".github/agents", root, errors):
        if path.name.endswith(".md"):
            definitions.append(("agent", path))

    validated: list[Definition] = []
    names: dict[str, dict[str, str]] = {"skill": {}, "agent": {}}
    for kind, path in definitions:
        relative = path.relative_to(root).as_posix()
        if not within_root(path, root, errors):
            continue
        metadata = read_frontmatter(path, relative, errors)
        if metadata is None:
            continue
        previous_errors = len(errors)
        name = validate_metadata(Path(relative), kind, metadata, errors)
        if name is not None:
            if name in names[kind]:
                errors.append(f"{relative}: duplicate {kind} name {name!r}; also declared in {names[kind][name]}")
            else:
                names[kind][name] = relative
            if len(errors) == previous_errors:
                notes.append(describe_metadata(relative, kind, name, metadata))
                validated.append(Definition(Path(relative), kind, name, metadata))
    notes.append(f"Inspected {sum(kind == 'skill' for kind, _ in definitions)} skill and "
                 f"{sum(kind == 'agent' for kind, _ in definitions)} agent definitions.")
    return validated, errors, notes


def check(root: Path) -> tuple[list[str], list[str]]:
    """Return invalid metadata and declared configuration; never run file content."""
    _, errors, notes = inspect_definitions(root)
    return errors, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true", help="emit a machine-readable report")
    args = parser.parse_args()
    errors, notes = check(args.root)
    if args.json:
        print(json.dumps({"root": str(args.root), "static_validation": "failed" if errors else "passed",
                          "host_discovery": "not_checked", "host_invocation": "not_checked",
                          "errors": errors, "notes": notes}, indent=2))
    else:
        for note in notes:
            print(f"Note: {note}")
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Static AI configuration validation {'failed' if errors else 'passed'}.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
