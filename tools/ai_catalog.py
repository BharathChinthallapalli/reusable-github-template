"""Check the generated AI catalog, or regenerate it explicitly with --write."""

from __future__ import annotations

import argparse
import html
from pathlib import Path
import re
import sys
from urllib.parse import quote

if __package__:
    from .check_ai_configuration import Definition, ROOT, inspect_definitions, within_root
else:
    from check_ai_configuration import Definition, ROOT, inspect_definitions, within_root


CATALOG_PATH = Path("docs/ai-catalog.md")


def markdown_text(value: str) -> str:
    text = html.escape(" ".join(value.split()), quote=False)
    text = re.sub(r"([\\`*_\[\]])", r"\\\1", text)
    return text.replace("|", "&#124;")


def invocation_flags(metadata: dict) -> list[str]:
    user_invocable = metadata.get("user-invocable", True)
    model_eligible = not metadata.get("disable-model-invocation", False)
    user_source = "declared" if "user-invocable" in metadata else "default"
    model_source = "declared" if "disable-model-invocation" in metadata else "default"
    return [f"{str(user_invocable).lower()} ({user_source})",
            f"{str(model_eligible).lower()} ({model_source})"]


def agent_tools(metadata: dict) -> str:
    if "tools" not in metadata:
        return "Not declared; host defaults apply"
    tools = metadata["tools"]
    if isinstance(tools, str):
        tools = [tool.strip() for tool in tools.split(",")]
    return markdown_text(", ".join(tools)) if tools else "None declared (empty list)"


def render_catalog(definitions: list[Definition]) -> str:
    lines = [
        "# AI catalog", "",
        "Generated from repository metadata by `python3 tools/ai_catalog.py --write`.",
        "Run `python3 tools/ai_catalog.py` to check freshness without changing files.", "",
        "This is a static catalog. Host discovery and invocation are not checked.",
        "Eligibility and tool scopes describe metadata, not actual host support,",
        "permissions, running agents, or guaranteed automatic selection. Default flags",
        "mean user invocation is allowed and model invocation is eligible unless",
        "disabled in metadata. Deprecated `infer` flags do not establish legacy host behavior.",
        "Skills describe procedures; the invoking host and agent control their tools.", "",
    ]
    for kind, title in (("agent", "Agents"), ("skill", "Skills")):
        entries = sorted((item for item in definitions if item.kind == kind),
                         key=lambda item: (item.name.casefold(), item.name, item.path.as_posix()))
        lines.extend([f"## {title} ({len(entries)})", ""])
        columns = ["Name", "When to use"]
        if kind == "agent":
            columns.append("Declared tools")
        columns.extend(["User invocable", "Model invocation eligible"])
        lines.append("| " + " | ".join(columns) + " |")
        lines.append("| " + " | ".join("---" for _ in columns) + " |")
        for definition in entries:
            destination = quote("../" + definition.path.as_posix(), safe="/.")
            cells = [f"[{markdown_text(definition.name)}]({destination})",
                     markdown_text(definition.metadata["description"])]
            if kind == "agent":
                cells.append(agent_tools(definition.metadata))
            cells.extend(invocation_flags(definition.metadata))
            lines.append("| " + " | ".join(cells) + " |")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--write", action="store_true", help="regenerate docs/ai-catalog.md after validation")
    args = parser.parse_args()
    definitions, errors, _ = inspect_definitions(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    root = args.root.resolve()
    output = root / CATALOG_PATH
    if not within_root(output, root, errors):
        print(f"ERROR: {errors[0]}", file=sys.stderr)
        return 1
    if output.is_symlink():
        print(f"ERROR: {CATALOG_PATH}: refuses a symlink catalog file", file=sys.stderr)
        return 1
    expected = render_catalog(definitions)
    try:
        if args.write:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(expected, encoding="utf-8")
            print(f"Generated {CATALOG_PATH} from validated metadata.")
            return 0
        if not output.is_file():
            print(f"ERROR: {CATALOG_PATH} is missing. Run python3 tools/ai_catalog.py --write.", file=sys.stderr)
            return 1
        if output.read_text(encoding="utf-8") != expected:
            print(f"ERROR: {CATALOG_PATH} is stale. Run python3 tools/ai_catalog.py --write.", file=sys.stderr)
            return 1
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: {CATALOG_PATH}: {exc}", file=sys.stderr)
        return 1
    print("AI catalog matches validated metadata. Host discovery and invocation are not checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
