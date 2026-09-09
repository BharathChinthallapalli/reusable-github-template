#!/usr/bin/env python3
"""Preview or initialize this template using only the Python standard library."""

import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile
import unicodedata
from urllib.parse import unquote, urlsplit


TOKENS = {
    "name": "@@PROJECT_NAME@@",
    "slug": "@@PROJECT_SLUG@@",
    "owner": "@@GITHUB_OWNER@@",
    "codeowner": "@@CODEOWNER@@",
    "security_contact": "@@SECURITY_CONTACT@@",
    "description": "@@PROJECT_DESCRIPTION@@",
}
CUSTOMIZE_FILES = {
    "README.md", "SECURITY.md", "SUPPORT.md", ".github/CODEOWNERS", "docs/project.md"
}


def github_owner(value, allow_managed=True):
    name, separator, shortcode = value.partition("_")
    if separator and (not allow_managed or not re.fullmatch(r"[A-Za-z0-9]{3,8}", shortcode)):
        return False
    return len(value) <= 39 and re.fullmatch(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*", name)


def has_controls(value):
    return any(unicodedata.category(c).startswith("C") or c in "\u2028\u2029" for c in value)


def hostname(value):
    return bool(value) and len(value) <= 253 and all(
        re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?", label)
        for label in value.split(".")
    )


def validate_values(values):
    for key, value in values.items():
        if not value or value != value.strip() or has_controls(value):
            raise ValueError(f"{key} must be nonempty, single-line text without surrounding whitespace")
    for key, limit in (("name", 100), ("description", 500)):
        value = values[key]
        if len(value) > limit or re.search(r"[`*_\[\]<>#|\\]", value) or "@@" in value:
            raise ValueError(f"{key} must be plain text (up to {limit} characters, without Markdown markup or @@ tokens)")
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,100}", values["slug"]) or values["slug"] in {".", ".."}:
        raise ValueError("slug must be a GitHub repository name: 1–100 letters, digits, dots, underscores or hyphens")
    if not github_owner(values["owner"]):
        raise ValueError("owner must be a GitHub username or organization name (up to 39 characters)")
    codeowner = values["codeowner"]
    parts = codeowner[1:].split("/") if codeowner.startswith("@") else []
    if not (1 <= len(parts) <= 2 and github_owner(parts[0], allow_managed=len(parts) == 1)):
        raise ValueError("codeowner must be @username or @organization/team")
    if len(parts) == 2 and not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,99}", parts[1]):
        raise ValueError("codeowner must contain a valid GitHub team slug")
    contact = values["security_contact"]
    if re.search(r"[\s\\<>\[\]()`\"']", contact) or has_controls(unquote(contact)):
        raise ValueError("security_contact must be a safe HTTPS or mailto link without whitespace, control characters or Markdown delimiters")
    parsed = urlsplit(contact)
    if parsed.scheme == "mailto":
        local, separator, domain = parsed.path.partition("@")
        if (parsed.netloc or parsed.query or parsed.fragment or not separator or not hostname(domain)
                or "." not in domain or len(local) > 64
                or not re.fullmatch(r"[A-Za-z0-9_%+-]+(?:\.[A-Za-z0-9_%+-]+)*", local)):
            raise ValueError("security_contact must contain one mailto email address without headers")
    elif parsed.scheme == "https":
        if not hostname(parsed.hostname) or parsed.username is not None or parsed.password is not None:
            raise ValueError("security_contact must have a valid HTTPS hostname without credentials")
        parsed.port  # Validate a supplied port before any files are written.
    else:
        raise ValueError("security_contact must use HTTPS or mailto")


def regular_file(root, relative):
    if (not isinstance(relative, str) or not relative or "\\" in relative
            or PurePosixPath(relative).is_absolute() or any(part in {"", ".", ".."} for part in relative.split("/"))):
        raise ValueError(f"Unsafe template path: {relative!r}")
    path = root
    for part in PurePosixPath(relative).parts:
        path /= part
        if path.is_symlink():
            raise ValueError(f"Symlinks are not supported: {relative}")
    if not path.is_file():
        raise ValueError(f"Required template file is missing or is not a regular file: {relative}")
    return path


def plan_changes(root, values):
    if root.is_symlink():
        raise ValueError("Template root must not itself be a symlink")
    root = root.resolve(strict=True)  # Allow system ancestors such as macOS /var -> /private/var.
    config_path = regular_file(root, "template.json")
    original_config = config_path.read_text(encoding="utf-8")
    config = json.loads(original_config)
    if not isinstance(config, dict) or type(config.get("schema_version")) is not int or config["schema_version"] != 1:
        raise ValueError("template.json must use schema_version 1")
    if type(config.get("initialized")) is not bool:
        raise ValueError("template.json initialized must be true or false")
    files = config.get("customize_files")
    if not isinstance(files, list) or not files or any(not isinstance(item, str) for item in files):
        raise ValueError("template.json customize_files must be a list of file paths")
    paths = [regular_file(root, item) for item in files]
    if len(files) != len(CUSTOMIZE_FILES) or set(files) != CUSTOMIZE_FILES:
        raise ValueError("customize_files must contain exactly the five supported documentation and CODEOWNERS files")
    if config["initialized"]:
        if config.get("project") != values:
            raise ValueError("Template is already initialized with different values; edit project files manually instead of reinitializing")
        return []
    if config.get("project") != TOKENS:
        raise ValueError("Uninitialized template.json project must contain the original six template tokens")
    changes = []
    for path in paths:
        before = path.read_text(encoding="utf-8")
        after = before
        if path.relative_to(root).as_posix() == ".github/CODEOWNERS":
            after = "".join(
                line[2:] if line.startswith("# ") and TOKENS["codeowner"] in line else line
                for line in after.splitlines(keepends=True)
            )
        for key, token in TOKENS.items():
            after = after.replace(token, values[key])
        if before != after:
            changes.append((path, after))
    config["initialized"] = True
    config["project"] = values
    changes.append((config_path, json.dumps(config, indent=2, ensure_ascii=False) + "\n"))
    return changes


def apply_changes(changes):
    """Stage all writes first; atomically replace each file, with template.json last."""
    staged = []
    try:
        for path, content in changes:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="", dir=path.parent,
                                             prefix=f".{path.name}.", delete=False) as temporary:
                staged.append((path, Path(temporary.name)))
                os.chmod(temporary.name, stat.S_IMODE(path.stat().st_mode))
                temporary.write(content)
                temporary.flush()
                os.fsync(temporary.fileno())
        for path, temporary in staged:
            os.replace(temporary, path)
    finally:
        for _, temporary in staged:
            temporary.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for key in TOKENS:
        parser.add_argument("--" + key.replace("_", "-"), required=True)
    parser.add_argument("--write", action="store_true", help="apply changes; the default is a preview")
    parser.add_argument("--root", type=Path, default=Path(__file__).absolute().parents[1], help="template root directory")
    args = parser.parse_args(argv)
    values = {key: getattr(args, key) for key in TOKENS}
    try:
        validate_values(values)
        changes = plan_changes(args.root, values)
        display_root = args.root.resolve(strict=True)
        if not changes:
            print("Already initialized with these values; no files changed.")
            return 0
        if args.write:
            apply_changes(changes)
        print("Initialized:" if args.write else "Preview only; run again with --write to apply:")
        for path, _ in changes:
            print(f"  {path.relative_to(display_root)}")
        return 0
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
