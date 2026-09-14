# 0010: Prepare hook dependencies before the first tool call

Status: Accepted
Date: 2026-09-14

## Context

The WorkBoard Copilot desktop trial reproduced a bootstrap deadlock: a new
worktree omitted ignored `.tools/bin/gitleaks`, while the pre-tool hook denied
both normal operations and the command to install that scanner. The desktop's
Python also lacked Ruff. The cloud setup workflow does not prepare local
desktop worktrees. Skill files were valid; live skill loading must be retested
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
