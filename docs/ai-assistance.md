# Default agents, skills, and clean code

Version 3.0.0 bundles **24 skills and 10 agents**. New repositories receive the
files, routing instructions and VS Code settings automatically. The
[generated catalog](ai-catalog.md) lists every capability, its trigger, declared
tools and invocation flags. [Working examples](working-with-agents.md) show how
to use them for ordinary engineering and AI projects.

## Default behavior and host support

Use a normal task request: repository instructions route an active assistant to
relevant skills. Skill names and descriptions are discoverable in supported
hosts; full procedures load when selected. All skills remain eligible for
automatic and explicit invocation. All agent profiles declare
`user-invocable: true` and `disable-model-invocation: false`, and inherit the
host's selected model. No skill grants tool preapproval. The new `/triage-issue`, `/write-adr` and
`/release-notes` procedures are discoverable skills, with shared task text under
`hooks/prompts`. That directory is not itself a native host command location.

| Host | Shared instructions | Skills | Specialist profiles |
| --- | --- | --- | --- |
| GitHub Copilot cloud agent and supported Copilot clients | `AGENTS.md`, `.github/copilot-instructions.md` and supported scoped instructions | Native discovery from `.agents/skills` | `.github/agents`; selection and available tools depend on the client |
| Current VS Code Copilot agent sessions | Repository settings enable instructions, AGENTS.md, matching instructions and skills | Native `.agents/skills`; verify in Chat customizations | Native `.github/agents`; profile menus and delegation depend on the chat surface |
| Codex | `AGENTS.md` | Native `.agents/skills` within its documented repository scope | Copilot profiles are reference procedures, not native Codex subagent configuration |
| Claude Code | Root `CLAUDE.md` imports `AGENTS.md` | Shared procedures can be read through instruction links; native skill menus require Claude's documented skill locations | Copilot profiles are reference procedures, not native Claude subagents |

The canonical skill folder appears once. Do not also copy it into `.github/skills`
or `.claude/skills` in this repository: duplicate names can create ambiguous
selection. Native host agents and tool availability are separate from shared
procedures. GitHub's cloud reference, for example, marks the `web` tool alias as
inapplicable there. An `execute` tool can run arbitrary available commands; a
profile asking for read-only investigation is not an operating-system sandbox.

These defaults guide a running session. They do not launch background agents,
schedule work, consume model usage on their own, or override workspace trust,
account access, tool permissions or organization policy. A repository cannot
force every client to load every skill or guarantee a particular automatic
selection. Keep procedures concise and load only the relevant references.

## Agent hooks and design gate

[Agent hooks](../hooks/README.md) use `.github/hooks` for Copilot/VS Code and a
separate `.codex/hooks.json` for current Codex. Native hook support is different
from agent-profile discovery in the table above. Codex requires trusted project
configuration and explicit hook review in `/hooks`; repository files cannot bypass
that review. No native hook execution trace was captured in this delivery.

[Agent Design Documents](add/README.md) declare protected implementation scope,
accepted ADRs and observable behavior. The final design gate detects content drift
from the reviewed binding, while the pre-edit check permits work in progress.
It is an engineering completeness/integrity gate; semantic correctness remains a
review responsibility. [Runbooks](runbooks/README.md) describe actual operation and
recovery, including durable state, action identity and bounded retry decisions.

## Copilot environment setup

The bundled [setup workflow](../.github/workflows/copilot-setup-steps.yml) uses
GitHub's reserved `copilot-setup-steps` job to prepare Python 3.12, the pinned
validation dependencies and the checksum-pinned Gitleaks executable. It also runs on relevant setup-file changes and can be
started manually. Extend it with actual project prerequisites after choosing
the stack; keep commands aligned with [project context](project.md).

A setup failure does **not** prevent Copilot's cloud agent from starting. Inspect
its logs and run the validation commands before relying on that environment.
Successful setup proves prerequisite commands worked, not that a skill was
selected or a coding task succeeded. The separate `Repository checks` CI job
remains the foundation gate. Git hook installation is per clone through the
[hook preflight](git-hooks.md).

## Diagnose configuration and catalog drift

Prepare [the validation environment](using-the-template.md), then run:

```bash
python tools/check_ai_configuration.py --json
python tools/ai_catalog.py
python tools/check_design.py
python tools/check_repository.py
```

The AI checker safely parses metadata, checks entrypoints, names, descriptions,
flag types, tools and duplicate definitions, and reports paths and counts. It
recognizes the previous `.github/skills` location for migration diagnostics and
rejects duplicate names across roots. The catalog command checks that its
committed page matches valid metadata without changing files. After a deliberate
metadata change, run `python tools/ai_catalog.py --write` and review the diff.
The foundation checker separately checks local Markdown links.

| Evidence level | How to establish it | What remains unknown |
| --- | --- | --- |
| Files and metadata | Run diagnostics and catalog check at the recorded revision | Whether a client discovered the files |
| Host discovery | Inspect workspace customizations in the actual client | Whether a request selected the skill |
| Invocation | Inspect the host's skill/tool trace for a controlled request | Whether the output met task acceptance criteria |
| Task behavior | Compare outputs and checks against independent expected results | Behavior on other tasks or clients |

Static diagnostics always leave host discovery and invocation **not checked**.
An assistant's claim that it used a skill or model is not invocation evidence.
Use [the validation record](../VALIDATION.md) for the exact tested boundaries.

## Confirm discovery and useful behavior

1. Open the repository root in the client you actually use. In current VS Code,
   run **Chat: Open Customizations** and compare the visible skills and profiles
   against [the catalog](ai-catalog.md). Start a fresh chat after syncing if needed.
2. Select `engineer` where supported. Confirm the displayed tools match your
   intended work. The `reviewer` profile declares only read/search tools; any
   mismatch needs host/version diagnosis before relying on that profile.
3. Try a controlled request: “Trace the initializer entrypoint, its declared
   customization files and its refusal to overwrite different project values.
   Cite the code and make no edits.” Check the answer against
   `tools/initialize.py`, `template.json` and `tests/test_initialize.py`.
4. Inspect the invocation trace where available. Record unavailable trace access
   as unverified. For a behavioral check, use a [working example](working-with-agents.md)
   with explicit expected outcomes and examine the actual result.
5. Record client/runtime versions, repository revision, workspace root, chat
   surface, selected profile, trace evidence and outcome in the
   [troubleshooting record](troubleshooting.md). Remove confidential content.

If discovery fails, check root selection, standard paths, names, frontmatter,
duplicate installations and host versions first. A parent folder, nested Git
repository or different chat surface can change discovery. Avoid deprecated
custom skill-location settings or prompt files as a portability workaround.
Inline completion, editor agent chat, CLI and cloud sessions are separate
surfaces. Forum workarounds require verification on your actual version; see
[community lessons](research/community-lessons.md).

## Sources and maintenance

Checked 9 September 2026:
[GitHub skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills),
[GitHub custom-agent fields](https://docs.github.com/en/copilot/reference/custom-agents-configuration),
[Copilot environment setup](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-environment),
[VS Code skills](https://code.visualstudio.com/docs/agent-customization/agent-skills),
[VS Code custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents),
[VS Code prompt-file migration](https://code.visualstudio.com/docs/agent-customization/prompt-files),
[Codex skills](https://learn.chatgpt.com/docs/build-skills),
[Claude instruction imports](https://code.claude.com/docs/en/memory#agentsmd).

CI checks metadata, catalog freshness, links and tooling behavior. It does not
validate every host-specific field or activate these capabilities in your
editor. Follow [version 3 migration](maintenance.md) for existing generated
projects, which do not inherit template updates automatically.
