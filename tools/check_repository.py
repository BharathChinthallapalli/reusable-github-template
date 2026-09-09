"""Check this repository foundation, not arbitrary YAML or application security."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
MARKER = re.compile(r"@@[A-Z_]+@@")
REQUIRED = (
    "README.md", "AGENTS.md", "CONTRIBUTING.md", "SECURITY.md", "SUPPORT.md",
    "template.json", ".github/CODEOWNERS", ".github/workflows/ci.yml",
    ".github/dependabot.yml", ".github/rulesets/main.json",
    ".github/pull_request_template.md", ".github/ISSUE_TEMPLATE/bug.yml",
    ".github/ISSUE_TEMPLATE/change.yml", ".github/copilot-instructions.md",
    "docs/project.md", "tools/initialize.py", "tools/check_repository.py",
)


def read_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError("expected a JSON object")
        return value
    except (OSError, ValueError) as exc:
        errors.append(f"{path.name}: {exc}")
        return {}


def check_customization(root: Path, config: dict, errors: list[str], notes: list[str]) -> None:
    if type(config.get("schema_version")) is not int or config.get("schema_version") != 1:
        errors.append("template.json: unsupported schema_version")
    if type(config.get("initialized")) is not bool:
        errors.append("template.json: initialized must be a boolean")
    if not isinstance(config.get("project"), dict):
        errors.append("template.json: project must be an object")
        return
    targets = config.get("customize_files", [])
    if not isinstance(targets, list) or not targets:
        errors.append("template.json: customize_files must be a nonempty list")
        return
    for relative in targets:
        if not isinstance(relative, str):
            errors.append("template.json: customization paths must be strings")
            continue
        path = root / relative
        if Path(relative).is_absolute() or ".." in Path(relative).parts:
            errors.append(f"Unsafe customization path: {relative}")
            continue
        if not path.resolve().is_relative_to(root.resolve()) or path.is_symlink():
            errors.append(f"Customization path escapes the repository or is a symlink: {relative}")
            continue
        if not path.is_file():
            errors.append(f"Missing customization file: {relative}")
        elif config.get("initialized") and MARKER.search(path.read_text(encoding="utf-8")):
            errors.append(f"Unresolved project markers: {relative}")
    if config.get("initialized"):
        if MARKER.search(json.dumps(config.get("project", {}))):
            errors.append("template.json: initialized project contains unresolved markers")
        owner = config.get("project", {}).get("codeowner")
        owners_path = root / ".github/CODEOWNERS"
        if owners_path.is_file():
            entries = [line.split() for line in owners_path.read_text(encoding="utf-8").splitlines()
                       if line.strip() and not line.lstrip().startswith("#")]
            if not any(len(entry) >= 2 and entry[0] == "*" and owner in entry[1:] for entry in entries):
                errors.append("CODEOWNERS: missing active default entry for the configured owner")
    else:
        notes.append("Shared template mode: run the initializer in each generated project.")
    if config.get("license_decision") == "unselected":
        notes.append("Project license is unselected; complete docs/licensing.md before distribution.")


def check_workflow(root: Path, errors: list[str]) -> None:
    path = root / ".github/workflows/ci.yml"
    if not path.is_file():
        return
    source = path.read_text(encoding="utf-8")
    # These checks guard the intentionally small baseline. They are not a YAML parser.
    required_patterns = {
        "read-only contents permission": r"(?m)^  contents: read\s*$",
        "stable required job name": r"(?m)^    name: Repository checks\s*$",
        "pull-request trigger": r"(?m)^  pull_request:\s*$",
        "merge-group trigger": r"(?m)^  merge_group:\s*$",
        "checkout credential removal": r"(?m)^          persist-credentials: false\s*$",
        "job timeout": r"(?m)^    timeout-minutes: [1-9][0-9]*\s*$",
    }
    for label, pattern in required_patterns.items():
        if not re.search(pattern, source):
            errors.append(f"ci.yml: missing {label}")
    for number, line in enumerate(source.splitlines(), 1):
        active = line.strip()
        if active.startswith("#"):
            continue
        match = re.search(r"\buses:\s*['\"]?([^\s'\"#]+)", active)
        if match and not re.fullmatch(r"[\w.-]+/[\w./-]+@[a-f0-9]{40}", match.group(1)):
            errors.append(f"ci.yml:{number}: external baseline action must use a full commit SHA")
    if re.search(r"(?m)^\s+pull_request_target:", source):
        errors.append("ci.yml: the baseline must not run under pull_request_target")
    if re.search(r"(?m)^\s+paths(?:-ignore)?:", source):
        errors.append("ci.yml: required baseline check must not have path filters")


def check_ruleset(root: Path, errors: list[str]) -> None:
    path = root / ".github/rulesets/main.json"
    if not path.is_file():
        return
    ruleset = read_json(path, errors)
    if ruleset.get("enforcement") not in {"disabled", "active", "evaluate"}:
        errors.append("Ruleset: invalid enforcement state")
    if ruleset.get("target") != "branch":
        errors.append("Ruleset: baseline must target branches")
    rules = ruleset.get("rules")
    if not isinstance(rules, list):
        errors.append("Ruleset: rules must be an array")
        return
    contexts = []
    for rule in rules:
        if not isinstance(rule, dict):
            errors.append("Ruleset: each rule must be an object")
            continue
        if rule.get("type") == "required_status_checks":
            parameters = rule.get("parameters", {})
            checks = parameters.get("required_status_checks", []) if isinstance(parameters, dict) else []
            if isinstance(checks, list):
                contexts.extend(check.get("context") for check in checks if isinstance(check, dict))
    if "Repository checks" not in contexts:
        errors.append("Ruleset: required check must include Repository checks")


def check_docs(root: Path, errors: list[str]) -> None:
    files = [root / name for name in ("README.md", "AGENTS.md", "CONTRIBUTING.md", "SECURITY.md", "SUPPORT.md")]
    for folder in ("docs", ".github/agents", ".github/skills", ".github/instructions"):
        files.extend((root / folder).rglob("*.md"))
    files.append(root / ".github/copilot-instructions.md")
    for path in files:
        if not path.is_file():
            continue
        # Ignore fenced code; validate simple relative Markdown links in our docs.
        source = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", source):
            if target.startswith(("http:", "https:", "mailto:", "#")) or MARKER.search(target):
                continue
            relative = unquote(target.split("#", 1)[0])
            if relative and not (path.parent / relative).exists():
                errors.append(f"{path.relative_to(root)}: broken local link {target}")


def check(root: Path) -> tuple[list[str], list[str]]:
    root = root.resolve()
    errors: list[str] = []
    notes: list[str] = []
    for relative in REQUIRED:
        if not (root / relative).is_file():
            errors.append(f"Missing required foundation file: {relative}")
    config = read_json(root / "template.json", errors)
    if config:
        check_customization(root, config, errors, notes)
    check_workflow(root, errors)
    check_ruleset(root, errors)
    check_docs(root, errors)
    for folder in ("tools", "tests"):
        for path in (root / folder).rglob("*.py"):
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except SyntaxError as exc:
                errors.append(f"{path.relative_to(root)}: {exc.msg}, line {exc.lineno}")
    return errors, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        errors, notes = check(args.root)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"Repository check failed: {exc}", file=sys.stderr)
        return 1
    for note in notes:
        print(f"Note: {note}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    print("Repository foundation checks passed. Application tests and GitHub settings are separate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
