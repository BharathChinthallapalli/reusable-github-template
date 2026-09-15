# 0010: Prepare hook dependencies before the first tool call

Status: Accepted
Date: 2026-09-14

## Context

The WorkBoard Copilot desktop trial reproduced a bootstrap deadlock: a new
worktree omitted ignored `.tools/bin/gitleaks`, while the pre-tool hook denied
both normal operations and the command to install that scanner. The desktop's
Python also lacked Ruff. The cloud setup workflow does not prepare local
desktop worktrees. Native retesting also found that desktop hooks resolved an
older system Python even when a supported Homebrew Python was installed. The
launcher therefore discovers and verifies an installed supported interpreter
before consuming hook input; it does not install Python or change global PATH.

Skill files were valid; live skill loading must be retested
after setup to distinguish a blocked invocation from a discovery defect.

## Decision

Use a small standard-library hook launcher for configured local host events.
Only session start may create `.tools/venv`, install the existing pinned Python
requirements, and run the existing checksum-pinned Gitleaks installer. It must
complete the original session preflight before recording a requirements digest.
The environment belongs to one worktree and does not replace application
environments, alter global packages or change Git configuration.

Pre-tool and post-tool events use the prepared interpreter and original policy.
They perform no installation or network requests. Missing or stale setup fails
closed with a direct terminal recovery command. Setup failures cannot produce
a readiness marker. Retain bounded subprocesses, sanitized output, no execution
of proposed commands, and all existing secret, credential and design checks.
Repository trust must precede running these repository-controlled commands.

## Alternatives and consequences

Allowing unscanned setup commands or read tools would weaken the existing
argument-scanning contract. Installing inside pre-tool hooks risks host
timeouts that allow execution. Sharing mutable environments between worktrees
couples unrelated revisions and package versions. A manual-only prerequisite
leaves ordinary desktop worktree creation broken. A session-only bootstrap
keeps installation separate from tool decisions, at the cost of a bounded
network-dependent first start and a small environment per worktree.

The cloud setup workflow and manual diagnostics remain supported. Existing
projects must port the launcher and host configuration explicitly. Test a
fresh setup, reuse, changed requirements, failed/timeout setup, clean and denied
tool requests, and actual Copilot skill loading. Record untested hosts honestly.

## Sources

[GitHub hook reference](https://docs.github.com/en/copilot/reference/hooks-reference)
documents session-start command hooks and notes that pre-tool command timeouts
fall through to normal host permission checks. Checked 2026-09-14.

## Review repair, 2026-09-15

The readiness receipt now binds the resolved interpreter, scanner and venv
configuration bytes to the setup inputs. Every dispatch checks these without
executing an unverified candidate. Scanner paths reject symlinks and junctions;
external interpreter links must resolve to the launcher's actual base runtime.
A missing base-runtime link may be cleared only during session recovery.
Malformed, oversized and non-UTF8 receipts require setup again. Windows uses
`py -3` at the configured entrypoint, and failures infer VS Code's snake_case
payload to return its structured denial.

This detects stale or replaced executables relative to a local receipt. A writer
can still modify that receipt, the hook code or installed Python modules, or race
a check with execution. It is not an authenticated trust anchor or OS sandbox.

Official references fetched with the web tool on 2026-09-15:

- [Python venv](https://docs.python.org/3/library/venv.html): base environments,
  interpreter copies/symlinks and explicit environment interpreter execution.
- [Python pathlib](https://docs.python.org/3/library/pathlib.html): path resolution,
  symlink and junction checks.
- [Python on Windows](https://docs.python.org/3/using/windows.html): `py` launcher.
- [VS Code hook reference](https://code.visualstudio.com/docs/agents/reference/hooks-reference):
  snake_case event fields and structured pre-tool output.
- [GitHub hook reference](https://docs.github.com/en/copilot/reference/hooks-reference):
  platform commands and GitHub event/output fields. Host fallthrough on failures
  remains a host limitation; the launcher emits explicit denial when callable.
