# Agent hooks and task commands

This directory contains executable lifecycle checks and shared task procedures.
The native registrations live in [Copilot/VS Code configuration](../.github/hooks/agent-checks.json)
and [Codex configuration](../.codex/hooks.json). They are distinct from the
[Git commit hooks](../docs/git-hooks.md), which remain independently configured.

## Prepare the tools

From the repository root, in the [prepared Python environment](../docs/using-the-template.md):

```bash
python -m pip install -r requirements-dev.txt
python tools/install_hook_tools.py
python hooks/agent_hooks.py --event session
python hooks/agent_hooks.py --event check
python tools/check_design.py
```

Ruff is pinned to 0.16.6. The installer obtains Gitleaks 8.30.1 for a supported
Linux, macOS or Windows x64/ARM64 platform, verifies the reviewed archive SHA-256,
and extracts its executable into the ignored `.tools/bin` directory. It does not
install a global executable or run an upstream install script. Pin updates need
source verification, archive-digest review and the scanner integration tests.

Activate the same environment before starting a local coding client so `python`
or `python3` resolves to the prepared interpreter. The GitHub setup workflow
prepares these prerequisites for Copilot cloud sessions. A session diagnostic
failure is a setup failure, not evidence that scanning succeeded. Use the
installer's help for supported invocation details.

## What the checks do

| Event | Behavior | Result |
| --- | --- | --- |
| Session start | Check that the required scanner tools are usable | Sanitized setup diagnostics; this event alone is not a host security gate |
| Pre-tool | Parse the host envelope, scan proposed arguments for detected secrets, reject known destructive command forms and credential-file access, and check declared ADD coverage for recognized structured edits | A denial stops the attempted call in a supporting host; clean checks return no automatic approval |
| Post-edit or covered shell tool | Run read-only Ruff and Gitleaks checks on the selected repository files | Failures report repair feedback after the edit; they cannot undo the completed tool call |
| Standalone `--event check` | Run the working-tree Ruff/Gitleaks checks without a model session | Nonzero exit on findings or unavailable/failed checks; used in CI |

The dispatcher never executes a candidate command to decide whether it is safe.
Scanner invocations use argument arrays, bounded deadlines and sanitized outputs.
It does not persist raw prompts, tool arguments, scanner matches or transcripts.
Gitleaks output is redacted and suppressed at the hook boundary; diagnostics identify
the failed check without printing its potential secret. Ruff runs in isolated Python mode so a repository `ruff.py` cannot replace the
installed scanner. Inline `gitleaks:allow` comments cannot suppress findings.
Ruff checks run without silently rewriting files or applying broad formatting changes.

The working-tree scan includes Git-tracked files and untracked files selected by
Git's ignore rules. A ZIP uses a filesystem fallback without Git ignore selection, so local
environment files can be scanned too.
Tool caches, dependency directories and other excluded paths are outside that
snapshot; repository history is not scanned. Symlinks are handled without copying
content outside the repository. Read the implementation and its tests for the
exact supported paths, command forms and event aliases.

## Host behavior and trust

| Host | Discovery and input | Limits to verify in the actual client |
| --- | --- | --- |
| Copilot CLI/cloud | `.github/hooks/*.json`; camelCase events and tool fields | Cloud uses its default-branch files and Unix command. CLI should restart after hook changes. A host-level timeout can allow a call to continue. |
| VS Code Copilot | Reads the same configuration and supplies snake_case event fields | Preview behavior and organizational settings apply; matchers are currently ignored, so the script filters tools itself. Inspect agent debug logs. |
| Current Codex | `.codex/hooks.json`; nested handler groups and snake_case fields | Trust the project and review the exact hooks through `/hooks`. The launcher resolves Git root, with `python3` on Unix and an explicit PowerShell/`python` override on Windows. Hosted tools and later `write_stdin` input are outside pre-tool coverage. |

The dispatcher distinguishes the GitHub denial schema from the VS Code/Codex
schema. Malformed input with an unknown host uses exit 2 and a generic diagnostic
so it is not mistaken for a clean pass. Valid clean checks return `{}` and leave
ordinary host permissions in force. Internal deadlines are shorter than the
configured host timeout so failures can be returned before the host times out.

These repository-controlled checks provide a tested early rejection layer. They
cannot make arbitrary shell code safe, exhaustively detect secrets, enforce an
administrative policy against someone who can edit the hooks, or intercept tools
a host does not expose. Encoded/dynamic programs, undisclosed file effects and
interactive input require the host's execution isolation and permission controls.
A post-edit failure does not prevent the preceding write or disclosure.

No Claude-native hook configuration is installed here; `CLAUDE.md` continues to
share instructions. Native Codex hooks are configured, but trust and live invocation
must be verified in the user's actual client. Static JSON validity and replayed
hook inputs do not establish native host activation.

## Work with the ADD gate

Read [Agent Design Documents](../docs/add/README.md) before editing protected agent,
skill or hook paths. Declare a path in a ready design before a recognized edit.
The pre-edit `--paths` check permits fingerprint drift during an implementation.
The final gate requires current scope, accepted ADR references and matching bound
contents after review and explicit sealing. A missing or outdated design must be
repaired from actual behavior and evidence, not bypassed or blindly resealed.

The gate binds the declared implementation and design record; it does not infer
semantic correctness, authenticate business approval or authorize new side effects.
Existing task authorization remains applicable. CI checks this gate independently
of whether a particular editor intercepted the edit.

## Task commands

| Command | Shared procedure | Discoverable skill |
| --- | --- | --- |
| `/triage-issue` | [Trace impact, reproduction and next action](prompts/triage-issue.md) | [triage-issue](../.agents/skills/triage-issue/SKILL.md) |
| `/write-adr` | [Record evidence, alternatives and decision status](prompts/write-adr.md) | [write-adr](../.agents/skills/write-adr/SKILL.md) |
| `/release-notes` | [Describe verified changes over an explicit revision range](prompts/release-notes.md) | [release-notes](../.agents/skills/release-notes/SKILL.md) |

The `hooks/prompts` folder holds shared text; it is not automatically a native
slash-command location. Thin skills expose these names through supported skill
menus and default routing. Other hosts can read the same procedures directly.
The commands do not post issue comments or publish a release without the task's
authorization. ADRs use [the canonical decision template](../docs/adr/template.md).

## Troubleshoot a failed hook

1. Preserve the attempted task and sanitized check name. Do not copy a secret-bearing
   payload into an issue or terminal log. Confirm the interpreter and exact repository
   root used by the host.
2. Run the session diagnostic and standalone check in that environment. If tools are
   missing, repair setup with the pinned installer; a skipped scan is not a passing scan.
3. For a design rejection, check explicit path coverage and accepted ADR status. Complete
   the design, implement the authorized change, review and seal it before the final gate.
4. For lint or secret findings, inspect only the affected local files, correct the issue,
   and repeat the relevant check. If a real credential was exposed, use the project's
   security response process; deleting text does not revoke it.
5. Verify recovery through the original operation. Use [the agent recovery runbook](../docs/runbooks/agent-recovery.md)
   when state, tool side effects or interrupted approvals are involved.

Current primary sources, checked 9 September 2026:
[GitHub hook reference](https://docs.github.com/en/copilot/reference/hooks-reference),
[VS Code hooks](https://code.visualstudio.com/docs/agent-customization/hooks),
[VS Code hook events](https://code.visualstudio.com/docs/agents/reference/hooks-reference),
[Codex hooks](https://learn.chatgpt.com/docs/hooks),
[Ruff configuration](https://docs.astral.sh/ruff/configuration/),
[Gitleaks 8.30.1](https://github.com/gitleaks/gitleaks/tree/v8.30.1),
and [Cloudflare source lessons](../docs/research/cloudflare-agents.md).
