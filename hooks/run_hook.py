#!/usr/bin/env python3
"""Prepare trusted worktree tools at session start, then run the read-only policy."""

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

if __package__:
    from . import agent_hooks as policy
else:
    import agent_hooks as policy


ROOT = Path(__file__).resolve().parents[1]
SETUP_TIMEOUT = 150
RECOVERY = "Run python3 hooks/run_hook.py --event session in this worktree's terminal, then retry."


def supported_runtime():
    """Desktop launch environments can resolve Apple's older system Python."""
    candidates = []
    for name in ("python3.14", "python3.13", "python3.12", "python3", "python"):
        executable = shutil.which(name)
        if executable:
            candidates.append([executable])
    if sys.platform == "darwin":
        for path in (
            "/opt/homebrew/bin/python3",
            "/usr/local/bin/python3",
            "/Library/Frameworks/Python.framework/Versions/Current/bin/python3",
        ):
            if Path(path).is_file():
                candidates.append([path])
    if os.name == "nt" and (launcher := shutil.which("py")):
        candidates.append([launcher, "-3"])
    seen = set()
    for candidate in candidates:
        identity = tuple(candidate)
        if identity in seen:
            continue
        seen.add(identity)
        try:
            result = subprocess.run(
                [
                    *candidate,
                    "-I",
                    "-c",
                    "import sys; sys.exit(sys.version_info < (3, 12))",
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=1,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):
            continue
        if result.returncode == 0:
            return candidate
    return None


def environment_paths(root):
    tools = root / ".tools"
    environment = tools / "venv"
    receipt = tools / "hook-environment.sha256"
    lock = tools / "hook-bootstrap.lock"
    for path in (tools, environment, receipt, lock):
        if path.is_symlink() or path.is_junction():
            raise policy.CheckFailure("Hook setup path uses a symlink or junction.")
        if path.exists() and not (
            path.is_dir() if path in (tools, environment) else path.is_file()
        ):
            raise policy.CheckFailure("Hook setup path has an unexpected file type.")
    python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    return tools, environment, python, receipt, lock


def environment_fingerprint(root):
    digest = hashlib.sha256()
    digest.update(f"v1:{sys.platform}:{sys.implementation.cache_tag}\0".encode())
    for relative in ("requirements-dev.txt", "tools/install_hook_tools.py"):
        digest.update(
            relative.encode() + b"\0" + (root / relative).read_bytes() + b"\0"
        )
    return digest.hexdigest()


def validate_environment_tree(environment):
    """Do not let a partially prepared environment redirect package writes."""
    if not environment.exists():
        return
    for directory, folders, files in os.walk(environment, followlinks=False):
        for name in folders + files:
            path = Path(directory) / name
            if not (path.is_symlink() or path.is_junction()):
                continue
            interpreter = (
                path.parent == environment / "bin"
                and (re.fullmatch(r"python(?:3(?:\.\d+)?)?", name) or name == "𝜋thon")
                and not path.is_dir()
            )
            if not interpreter and not path.resolve().is_relative_to(environment):
                raise policy.CheckFailure(
                    "Hook environment contains a path redirected outside the worktree."
                )


def environment_ready(root):
    _, _, python, receipt, _ = environment_paths(root)
    scanner = root / ".tools/bin" / ("gitleaks.exe" if os.name == "nt" else "gitleaks")
    return (
        python.is_file()
        and scanner.is_file()
        and receipt.is_file()
        and receipt.read_text(encoding="utf-8").strip() == environment_fingerprint(root)
    )


@contextmanager
def setup_lock(path, deadline):
    """OS releases the lock on process exit, including an interrupted startup."""
    with path.open("a+b") as handle:
        if os.name == "nt":
            import msvcrt

            handle.write(b"\0")
            handle.flush()

            def acquire():
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)

            def release():
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            def acquire():
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)

            def release():
                fcntl.flock(handle, fcntl.LOCK_UN)

        while True:
            policy.remaining_seconds(deadline)
            try:
                acquire()
                break
            except BlockingIOError:
                time.sleep(min(0.1, policy.remaining_seconds(deadline)))
            except OSError as error:
                if os.name != "nt" or error.errno not in (13, 36):
                    raise
                time.sleep(min(0.1, policy.remaining_seconds(deadline)))
        try:
            yield
        finally:
            release()


def setup_command(command, root, deadline, phase, *, environment=None):
    timeout = policy.remaining_seconds(deadline)
    options = (
        {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
        if os.name == "nt"
        else {"start_new_session": True}
    )
    process = subprocess.Popen(
        command,
        cwd=root,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        **options,
    )
    try:
        try:
            process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            if os.name == "nt":
                try:
                    subprocess.run(
                        [
                            str(
                                Path(os.environ["SystemRoot"]) / "System32/taskkill.exe"
                            ),
                            "/PID",
                            str(process.pid),
                            "/T",
                            "/F",
                        ],
                        capture_output=True,
                        timeout=5,
                        check=True,
                    )
                except (OSError, subprocess.SubprocessError):
                    process.kill()
                    process.wait(timeout=5)
                    raise policy.CheckFailure(
                        "Hook setup process-tree cleanup failed. Stop remaining setup "
                        "processes in this worktree before retrying."
                    ) from None
            else:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            process.communicate(timeout=5)
            raise policy.CheckFailure(
                "Hook setup timed out; the environment was not verified. " + RECOVERY
            ) from None
    finally:
        process.stdout.close()
        process.stderr.close()
    if process.returncode:
        raise policy.CheckFailure(f"Hook setup failed during {phase}. {RECOVERY}")


def verify_environment(root, python, deadline):
    setup_command(
        [str(python), "-I", "-c", "import yaml, ruff"],
        root,
        deadline,
        "Python dependency verification",
    )
    setup_command(
        [str(python), str(root / "hooks/agent_hooks.py"), "--event", "session"],
        root,
        deadline,
        "scanner verification",
    )


def prepare_environment(root, deadline):
    tools, environment, python, receipt, lock = environment_paths(root)
    tools.mkdir(exist_ok=True)
    with setup_lock(lock, deadline):
        environment_paths(root)
        validate_environment_tree(environment)
        if environment_ready(root):
            try:
                verify_environment(root, python, deadline)
                return
            except policy.CheckFailure:
                pass
        receipt.unlink(missing_ok=True)
        setup_command(
            [sys.executable, "-I", "-m", "venv", "--clear", str(environment)],
            root,
            deadline,
            "Python environment creation",
        )
        uv = shutil.which("uv")
        if uv:
            command = [
                uv,
                "pip",
                "install",
                "--python",
                str(python),
                "--no-config",
                "--no-cache",
                "-r",
                str(root / "requirements-dev.txt"),
            ]
        else:
            command = [
                str(python),
                "-I",
                "-m",
                "pip",
                "--isolated",
                "install",
                "--disable-pip-version-check",
                "--no-input",
                "--no-cache-dir",
                "-r",
                str(root / "requirements-dev.txt"),
            ]
        setup_command(command, root, deadline, "validation dependency installation")
        setup_command(
            [str(python), str(root / "tools/install_hook_tools.py")],
            root,
            deadline,
            "verified Gitleaks installation",
        )
        verify_environment(root, python, deadline)
        environment_paths(root)
        with tempfile.NamedTemporaryFile(
            mode="w", dir=tools, delete=False, encoding="utf-8"
        ) as temporary:
            temporary.write(environment_fingerprint(root) + "\n")
        try:
            os.replace(temporary.name, receipt)
        finally:
            Path(temporary.name).unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--event", required=True, choices=["session", "pre", "post", "check"]
    )
    parser.add_argument("--host", choices=["github", "vscode", "codex"])
    parser.add_argument("--root", type=Path, default=ROOT)
    options = parser.parse_args(argv)
    host = options.host
    try:
        if sys.version_info < (3, 12):
            runtime = supported_runtime()
            if runtime:
                os.execv(
                    runtime[0], [*runtime, str(Path(__file__).resolve()), *sys.argv[1:]]
                )
        interactive_setup = options.event == "session" and sys.stdin.isatty()
        raw = (
            b""
            if options.event == "check" or interactive_setup
            else sys.stdin.buffer.read(policy.MAX_INPUT_BYTES + 1)
        )
        if len(raw) > policy.MAX_INPUT_BYTES:
            raise policy.CheckFailure("Hook input exceeds the inspection limit.")
        if raw and host is None:
            try:
                payload = json.loads(raw)
                if isinstance(payload, dict):
                    host = (
                        "github"
                        if "toolName" in payload or "sessionId" in payload
                        else None
                    )
            except (ValueError, RecursionError):
                pass  # The original policy rejects malformed tool envelopes.
        if sys.version_info < (3, 12):
            raise policy.CheckFailure(
                "Hook setup requires an installed Python 3.12 or newer; "
                "make it available to the desktop host and retry."
            )
        root = options.root.resolve(strict=True)
        deadline = time.monotonic() + (
            SETUP_TIMEOUT if options.event == "session" else 20
        )
        if options.event == "session":
            prepare_environment(root, deadline)
        if not environment_ready(root):
            raise policy.CheckFailure(
                "Hook environment is missing or stale. " + RECOVERY
            )
        _, _, python, _, _ = environment_paths(root)
        command = [
            str(python),
            str(root / "hooks/agent_hooks.py"),
            "--event",
            options.event,
            "--root",
            str(root),
            "--timeout-seconds",
            str(min(20, policy.remaining_seconds(deadline))),
        ]
        if host:
            command.extend(["--host", host])
        result = subprocess.run(
            command,
            input=raw,
            capture_output=True,
            timeout=policy.remaining_seconds(deadline),
            check=False,
            cwd=root,
        )
        sys.stdout.buffer.write(result.stdout)
        sys.stderr.buffer.write(result.stderr)
        return result.returncode
    except (
        policy.CheckFailure,
        OSError,
        ValueError,
        RuntimeError,
        subprocess.SubprocessError,
    ) as error:
        reason = (
            str(error)
            if isinstance(error, policy.CheckFailure)
            else "Hook environment could not be prepared or verified. " + RECOVERY
        )
        print(reason, file=sys.stderr)
        if options.event == "pre" and host is None:
            print("{}")
            return 2
        print(json.dumps(policy.failure_output(options.event, host, reason)))
        return 0 if options.event == "pre" else 2


if __name__ == "__main__":
    raise SystemExit(main())
