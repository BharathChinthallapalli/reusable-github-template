#!/usr/bin/env python3
"""Bounded, read-only agent checks; a deny list is not a shell sandbox.

Only recognized shell forms and structured file arguments can be inspected.
Computed commands, opaque tools, host bypasses, and concurrent changes remain
outside this guard's guarantees. Nothing here executes or approves a tool call.
"""

import argparse
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
MAX_INPUT_BYTES = 4 * 1024 * 1024
MAX_SCAN_BYTES = 64 * 1024 * 1024
EXCLUDED_DIRECTORIES = {
    ".git", ".venv", "venv", ".tools", "node_modules", "__pycache__",
    ".ruff_cache", ".pytest_cache",
}
SHELL_TOOLS = {
    "bash", "shell", "powershell", "execcommand", "runinterminal",
    "runterminalcommand", "terminal",
}
EDIT_TOOLS = {
    "applypatch", "write", "edit", "create", "createfile", "writefile",
    "editfiles", "strreplaceeditor", "replacestringinfile",
    "multireplacestringinfile", "inserteditintofile", "multiedit",
}
PATH_FIELDS = {
    "path", "paths", "filepath", "filepaths", "filename", "filenames",
    "oldpath", "newpath", "uri",
}
PATCH_HEADER = re.compile(r"^\*\*\* (?:(?:Add|Update|Delete) File:|Move to:) (.+)$", re.MULTILINE)


class CheckFailure(Exception):
    """A safe diagnostic that never embeds arguments or scanner output."""


def remaining_seconds(deadline):
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise CheckFailure("Agent check timed out; the operation was not verified.")
    return remaining


def run_check(arguments, root, deadline, *, input_text=None, environment=None):
    try:
        return subprocess.run(
            arguments,
            cwd=root,
            input=input_text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=environment,
            timeout=remaining_seconds(deadline),
            check=False,
        )
    except subprocess.TimeoutExpired:
        raise CheckFailure("Agent check timed out; the operation was not verified.") from None
    except OSError:
        raise CheckFailure("Required check executable is unavailable; run hook setup.") from None


def gitleaks_binary(root):
    binary = root / ".tools" / "bin" / ("gitleaks.exe" if os.name == "nt" else "gitleaks")
    if not binary.is_file():
        raise CheckFailure("Gitleaks is unavailable; run hook setup before continuing.")
    return str(binary)


def scan_secrets(root, deadline, *, input_text=None, directory=None):
    executable = gitleaks_binary(root)
    with tempfile.TemporaryDirectory(prefix="agent-secret-rules-") as temporary:
        config = Path(temporary) / "gitleaks.toml"
        config.write_text("[extend]\nuseDefault = true\n", encoding="utf-8")
        ignore = Path(temporary) / "empty.ignore"
        ignore.touch()
        arguments = [
            executable, "stdin" if directory is None else "dir",
            "--config", str(config), "--gitleaks-ignore-path", str(ignore),
            "--redact=100", "--no-banner", "--no-color", "--exit-code=10", "--log-level=error",
            "--ignore-gitleaks-allow",
        ]
        if directory is not None:
            arguments.extend(["--", str(directory)])
        environment = {
            key: value for key, value in os.environ.items()
            if not key.startswith("GITLEAKS_")
        }
        result = run_check(arguments, root, deadline, input_text=input_text, environment=environment)
    if result.returncode == 10:
        raise CheckFailure("Secret scan found a potential secret; remove it before continuing.")
    if result.returncode != 0:
        raise CheckFailure("Gitleaks failed; the operation was not verified.")


def normalized_name(name):
    return name.rsplit(".", 1)[-1].replace("_", "").replace("-", "").lower()


def tool_call(payload):
    if "toolName" in payload:
        name, arguments = payload.get("toolName"), payload.get("toolArgs")
    else:
        name, arguments = payload.get("tool_name"), payload.get("tool_input")
    if isinstance(arguments, str):
        try:
            arguments = json.loads(arguments)
        except json.JSONDecodeError:
            raise CheckFailure("Invalid tool arguments; the operation was not verified.") from None
    if not isinstance(name, str) or not name or not isinstance(arguments, dict):
        raise CheckFailure("Invalid tool event; the operation was not verified.")
    return normalized_name(name), arguments


def path_arguments(value):
    paths = []
    if isinstance(value, dict):
        for key, item in value.items():
            if normalized_name(key) in PATH_FIELDS:
                candidates = item if isinstance(item, list) else [item]
                paths.extend(candidate for candidate in candidates if isinstance(candidate, str))
            else:
                paths.extend(path_arguments(item))
    elif isinstance(value, list):
        for item in value:
            paths.extend(path_arguments(item))
    return paths


def credential_path(path):
    normalized = unquote(path).replace("\\", "/").lower().strip("\"'`")
    components = normalized.split("/")
    filename = components[-1]
    if ".ssh" in components:
        return True
    if ".aws" in components and filename in {"credentials", "config"}:
        return True
    sanitized_example = filename.endswith((".example", ".sample", ".template"))
    if filename.startswith(".env") and not sanitized_example:
        return True
    return filename in {"id_rsa", "id_dsa", "id_ecdsa", "id_ed25519"} or filename.endswith(
        (".pem", ".key", ".p12", ".pfx")
    )


def command_segments(command):
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|()<>")
        lexer.whitespace_split = True
        lexer.commenters = ""
        tokens = list(lexer)
    except ValueError:
        raise CheckFailure("Shell quoting could not be inspected; the operation was not verified.") from None
    segment = []
    for token in tokens:
        if token and all(character in ";&|()<>" for character in token):
            if segment:
                yield segment
                segment = []
        else:
            segment.append(token)
    if segment:
        yield segment


def has_short_flag(arguments, flag):
    return any(
        item.startswith("-") and not item.startswith("--") and flag in item[1:]
        for item in arguments
    )


def recursive_forced_removal(executable, arguments):
    powershell_flags = executable == "remove-item" or any(
        item.startswith(("-recurse", "-force")) for item in arguments
    )
    if powershell_flags:
        recursive = any(item.startswith("-recurse") or item == "-r" for item in arguments)
        force = any(item.startswith("-force") or item == "-f" for item in arguments)
    else:
        recursive = "--recursive" in arguments or has_short_flag(arguments, "r")
        force = "--force" in arguments or has_short_flag(arguments, "f")
    windows_quiet_tree = (
        executable in {"rmdir", "rd", "del", "erase"}
        and "/s" in arguments and "/q" in arguments
    )
    return (recursive and force) or windows_quiet_tree


def destructive_segment(tokens):
    # Search literal command words so common sudo/env wrappers are covered.
    # This is conservative and deliberately does not evaluate shell expressions.
    for index, token in enumerate(tokens):
        executable = token.replace("\\", "/").rsplit("/", 1)[-1].strip("`").lower()
        arguments = [item.lower() for item in tokens[index + 1:]]
        if executable in {"rm", "rmdir", "rd", "del", "erase", "remove-item"}:
            if recursive_forced_removal(executable, arguments):
                return True
        if executable in {"git", "git.exe"}:
            if "reset" in arguments and "--hard" in arguments:
                return True
            if "clean" in arguments and ("--force" in arguments or has_short_flag(arguments, "f")):
                return True
            force_push = has_short_flag(arguments, "f") or any(
                item.startswith(("--force", "+")) for item in arguments
            )
            if "push" in arguments and force_push:
                return True
    return False


def inspect_command(command, cwd, depth=0):
    if depth > 4:
        raise CheckFailure("Nested shell command exceeds the inspection limit.")
    # The POSIX tokenizer removes Windows path separators. Inspect a separate
    # normalized view for credential paths without changing command parsing.
    for token in re.split(r"[\s\"'`;&|()<>=]+", command.replace("\\", "/")):
        if credential_path(token):
            raise CheckFailure("Credential path access blocked; use sanitized examples.")
    for tokens in command_segments(command):
        if destructive_segment(tokens):
            raise CheckFailure("Recognized destructive command blocked; use a reviewed safer operation.")
        for token in tokens:
            if (
                credential_path(token)
                or credential_path(str((cwd / token).resolve()))
                or any(credential_path(part) for part in token.split("="))
            ):
                raise CheckFailure("Credential path access blocked; use sanitized examples.")
        for index, token in enumerate(tokens[:-1]):
            shell_words = {item.rsplit("/", 1)[-1].lower() for item in tokens[:index]}
            clustered_shell_flag = (
                bool(shell_words & {"sh", "bash", "dash", "zsh", "ksh"})
                and bool(re.fullmatch(r"-[a-zA-Z]*c[a-zA-Z]*", token))
            )
            if (
                token.lower() in {"-c", "-lc", "/c", "-command", "-commandwithargs"}
                or clustered_shell_flag or (token == "-S" and "env" in shell_words)
            ):
                inspect_command(tokens[index + 1], cwd, depth + 1)


def edited_paths(name, arguments):
    paths = path_arguments(arguments)
    if name == "applypatch":
        patch = arguments.get("input", arguments.get("command", arguments.get("patch", "")))
        if not isinstance(patch, str):
            raise CheckFailure("Patch arguments could not be inspected.")
        paths.extend(PATCH_HEADER.findall(patch))
    return list(dict.fromkeys(paths))


def edit_path_relative_to_root(path, cwd, root):
    parsed = urlparse(path)
    if parsed.scheme == "file":
        if parsed.netloc not in {"", "localhost"}:
            raise CheckFailure("Remote editor file URI cannot be verified against repository design coverage.")
        path = unquote(parsed.path)
    if linked_path(cwd / path):
        raise CheckFailure("Editor path uses a symlink or junction; design coverage cannot be verified.")
    candidate = (cwd / path).resolve()
    try:
        return candidate.relative_to(root).as_posix()
    except ValueError:
        raise CheckFailure("Editor path is outside the repository; design coverage cannot be verified.") from None


def linked_path(path):
    return any(candidate.is_symlink() or candidate.is_junction() for candidate in [path, *path.parents])


def inspect_pre_tool(payload, root, deadline):
    name, arguments = tool_call(payload)
    scan_secrets(root, deadline, input_text=json.dumps(arguments, ensure_ascii=False))
    cwd = payload.get("cwd", str(root))
    if not isinstance(cwd, str):
        raise CheckFailure("Invalid tool working directory; the operation was not verified.")
    cwd = (root / cwd).resolve()
    paths = edited_paths(name, arguments)
    for path in paths:
        if credential_path(path) or credential_path(str((cwd / path).resolve())):
            raise CheckFailure("Credential path access blocked; use sanitized examples.")
    if name in SHELL_TOOLS:
        command = arguments.get("command", arguments.get("cmd", arguments.get("script")))
        if not isinstance(command, str) or not command:
            raise CheckFailure("Shell command arguments could not be inspected.")
        inspect_command(command, cwd)
    if name in EDIT_TOOLS:
        if not paths:
            raise CheckFailure("Editor paths could not be inspected; use a supported structured editor.")
        paths = [edit_path_relative_to_root(path, cwd, root) for path in paths]
        result = run_check(
            [sys.executable, str(root / "tools" / "check_design.py"), "--root", str(root), "--paths", *paths],
            root, deadline,
        )
        if result.returncode != 0:
            raise CheckFailure("Design check failed; complete ready design coverage for the proposed paths.")


def repository_files(root, deadline, changed_only=False):
    if (root / ".git").exists():
        options = ["--modified" if changed_only else "--cached", "--others", "--exclude-standard"]
        result = run_check(["git", "ls-files", "-z", *options], root, deadline)
        if result.returncode != 0:
            raise CheckFailure("Git file enumeration failed; repository checks were not completed.")
        names = result.stdout.split("\0")
        if changed_only:
            staged = run_check(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"], root, deadline)
            if staged.returncode != 0:
                raise CheckFailure("Git change enumeration failed; repository checks were not completed.")
            names.extend(staged.stdout.split("\0"))
        paths = {Path(name) for name in names if name}
    else:
        paths = set()
        for directory, folders, filenames in os.walk(root, followlinks=False):
            remaining_seconds(deadline)
            folders[:] = [name for name in folders if name not in EXCLUDED_DIRECTORIES]
            for name in folders:
                if linked_path(Path(directory) / name):
                    raise CheckFailure("Repository scan cannot verify a symlink or junction; remove or review it separately.")
            paths.update((Path(directory) / name).relative_to(root) for name in filenames)
    selected = []
    for path in sorted(paths):
        remaining_seconds(deadline)
        if any(part in EXCLUDED_DIRECTORIES for part in path.parts):
            continue
        full_path = root / path
        if linked_path(full_path):
            raise CheckFailure("Repository scan cannot verify a symlink or junction; remove or review it separately.")
        if path.is_absolute() or ".." in path.parts:
            raise CheckFailure("Repository scan received an unsafe file path.")
        if full_path.is_file():
            selected.append(path)
    return selected


def inspect_repository(root, deadline, *, all_python=False):
    files = repository_files(root, deadline)
    with tempfile.TemporaryDirectory(prefix="agent-scan-") as temporary:
        snapshot = Path(temporary)
        total_bytes = 0
        for path in files:
            remaining_seconds(deadline)
            total_bytes += (root / path).stat().st_size
            if total_bytes > MAX_SCAN_BYTES:
                raise CheckFailure("Repository exceeds the bounded scan size; run a reviewed external scan.")
            destination = snapshot / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / path, destination)
        scan_secrets(root, deadline, directory=snapshot)
    changed = files if all_python else repository_files(root, deadline, changed_only=True)
    python_files = [str(root / path) for path in changed if path.suffix == ".py"]
    if python_files:
        result = run_check(
            [
                sys.executable, "-I", "-m", "ruff", "check", "--no-fix",
                "--no-fix-only", "--no-cache", "--output-format=json", "--", *python_files,
            ],
            root, deadline,
        )
        if result.returncode != 0:
            raise CheckFailure("Ruff failed; run python -I -m ruff check locally for diagnostics.")


def session_preflight(root, deadline):
    for arguments in [[gitleaks_binary(root), "version"], [sys.executable, "-I", "-m", "ruff", "--version"]]:
        if run_check(arguments, root, deadline).returncode != 0:
            raise CheckFailure("Hook tools are unavailable or failed; run hook setup.")


def failure_output(event, host, reason):
    if event == "pre":
        decision = {"permissionDecision": "deny", "permissionDecisionReason": reason}
        if host == "github":
            return decision
        return {"hookSpecificOutput": {"hookEventName": "PreToolUse", **decision}}
    if host == "github":
        return {"additionalContext": reason}
    if event == "session":
        return {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": reason}}
    return {
        "decision": "block", "reason": reason,
        "hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": reason},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event", required=True, choices=["session", "pre", "post", "check"])
    parser.add_argument("--host", choices=["github", "vscode", "codex"])
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--timeout-seconds", type=float, default=20)
    options = parser.parse_args(argv)
    if not 0 < options.timeout_seconds <= 20:
        parser.error("--timeout-seconds must be greater than 0 and at most 20")
    deadline = time.monotonic() + options.timeout_seconds
    host = options.host
    try:
        payload = {}
        if options.event not in {"check", "session"}:
            raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
            if len(raw) > MAX_INPUT_BYTES:
                raise CheckFailure("Hook input exceeds the inspection limit.")
            try:
                payload = json.loads(raw)
            except (json.JSONDecodeError, UnicodeDecodeError, RecursionError):
                raise CheckFailure("Invalid hook JSON; the operation was not verified.") from None
            if not isinstance(payload, dict):
                raise CheckFailure("Invalid hook envelope; the operation was not verified.")
            if host is None:
                if "toolName" in payload or "sessionId" in payload:
                    host = "github"
                elif "tool_name" in payload or "session_id" in payload:
                    host = "vscode"
        root = options.root.resolve()
        if options.event == "pre":
            inspect_pre_tool(payload, root, deadline)
        elif options.event == "session":
            session_preflight(root, deadline)
        elif options.event == "check":
            inspect_repository(root, deadline, all_python=True)
        else:
            name, _ = tool_call(payload)
            if name in EDIT_TOOLS | SHELL_TOOLS:
                inspect_repository(root, deadline)
        print("{}")
        return 0
    except (CheckFailure, OSError, ValueError, RuntimeError) as error:
        reason = str(error) if isinstance(error, CheckFailure) else "Repository check could not read its inputs safely."
        print(reason, file=sys.stderr)
        if options.event == "pre" and host is None:
            # Exit 2 is the shared fail-closed fallback when JSON cannot identify a host.
            print("{}")
            return 2
        print(json.dumps(failure_output(options.event, host, reason)))
        return 0 if options.event == "pre" else 2


if __name__ == "__main__":
    raise SystemExit(main())
