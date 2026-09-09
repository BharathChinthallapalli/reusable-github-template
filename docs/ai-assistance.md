# Default agents, skills, and clean code

Template version 1.3.0 includes five custom agents and five skills. Every new
repository created from this version receives their files and VS Code settings.
The project initializer keeps them generic and ready for the new project.

## What is on by default

| Layer | Behavior in a supported Copilot session |
| --- | --- |
| `.github/copilot-instructions.md` and `AGENTS.md` | Repository guidance is included automatically; code edits are routed to clean-code and verification procedures |
| `.github/instructions/` | Existing Python and workflow guidance applies to matching paths |
| `.github/skills/` | Names and descriptions are discoverable; the relevant procedure and references load when selected |
| `.github/agents/` | Agents are visible for selection and eligible for automatic invocation where the host supports it |
| `.vscode/settings.json` | Explicitly enables repository instructions, AGENTS.md, matching instructions, and skills in VS Code |

These files guide an active session. They do not start processes, schedule jobs,
or generate usage by themselves. Model selection, account entitlement, tool
availability, workspace trust, and organization policy remain host controls.
The template cannot force every host to load every skill or select one agent for
all new chats. Copilot chooses relevant skills; instructions request their use.

## Agents

| Agent | Responsibility | Declared tools |
| --- | --- | --- |
| `engineer` | Implement and verify the requested change; coordinate useful specialist work | Read, search, edit, execute, delegate, web |
| `architect` | Investigate design choices and real system boundaries | Read, search, web |
| `reviewer` | Review a diff for evidenced defects and regressions | Read, search |
| `debugger` | Reproduce and fix a failure | Read, search, edit, execute, web |
| `security-reviewer` | Inspect identity, data, and privileged-action boundaries | Read, search, web |

All profiles set `user-invocable: true` and `disable-model-invocation: false`.
They inherit the selected model. A tool alias is useful only when the host
provides it; for example GitHub's cloud-agent reference currently marks the
`web` alias as inapplicable there. A read-only reviewer reports findings for an
implementing agent; it does not execute tests or approve a PR.

## Skills

| Skill | Use |
| --- | --- |
| [repo-discovery](../.github/skills/repo-discovery/SKILL.md) | Trace instructions, manifests, entrypoints, callers, and verified commands |
| [clean-code](../.github/skills/clean-code/SKILL.md) | Implement or refactor with clear names, justified abstractions, stable contracts, and useful tests |
| [verify-change](../.github/skills/verify-change/SKILL.md) | Choose checks that demonstrate the actual change and distinguish failure from missing evidence |
| [code-review](../.github/skills/code-review/SKILL.md) | Find consequential defects in a specified change and support findings with evidence |
| [github-actions-debug](../.github/skills/github-actions-debug/SKILL.md) | Diagnose the exact failing run and revision before proposing a correction |

Each skill has a linked reference with task-specific detail. No manual-only
invocation flags are set. Clean-code guidance uses Cocca's handbook, Martin's
*Clean Code*, and Fowler's *Refactoring*, with original synthesis and source
links in that skill. It rejects arbitrary size limits and speculative structure.

## Diagnose configuration before changing instructions

Prepare [the validation environment](using-the-template.md), then run:

```bash
python tools/check_ai_configuration.py
python tools/check_ai_configuration.py --json
python tools/check_repository.py
```

The first command reads agent and skill frontmatter with a safe YAML parser.
It checks names, required descriptions, invocation flag types, declared tools,
duplicate metadata, and skill entrypoints. It reports the configured profiles;
the foundation checker separately checks Markdown links. Neither command starts
an agent, reads editor settings outside this repository, or proves host activation.
The JSON result is for inspection or a local report; it is not a host telemetry feed.

| Evidence level | How to establish it | What remains unknown |
| --- | --- | --- |
| Files and metadata | Run both local checkers at the recorded revision | Whether the client discovered those files |
| Host discovery | Inspect workspace customizations in the actual client | Whether a specific request selected the skill |
| Invocation | Inspect the host's skill/tool trace for a controlled request | Whether the result met the task's acceptance criteria |
| Task behavior | Compare actual output and checks with a known expected result | Performance on other tasks or clients |

The static diagnostic always leaves host discovery and invocation **not checked**.
An assistant's claim that it used a skill or model is not invocation evidence.
Record the client, extension and agent runtime versions, workspace root, revision,
chat surface, selected profile, evidence, and outcome with the
[troubleshooting record](troubleshooting.md). Keep confidential prompts and logs out.

## Confirm discovery in your editor

1. Pull this template version or create a new repository from it. Open the
   repository root in a current VS Code with Copilot available.
2. Run **Chat: Open Customizations**. Confirm the five agents and five skills
   appear as workspace customizations. If needed, open a fresh chat after syncing.
3. Select a profile and inspect its description and available tools. For example,
   `reviewer` declares only read/search tools. If actual tools differ, investigate
   the host's metadata loading before using the profile for its intended boundary.
4. Select `engineer` for a coordinated coding task. For direct skill use, type
   `/clean-code` or `/repo-discovery` and provide the task. Automatic routing also
   applies in ordinary supported agent sessions through the repository instructions.
5. Try a read-only request: `/repo-discovery trace the initializer entrypoint,
   its declared customization targets, and the refusal to overwrite a project
   initialized with different values. Cite the code and do not modify files.`
   Inspect the host's invocation trace and check its answer against
   `tools/initialize.py`, `template.json`, and `tests/test_initialize.py`.
   Record missing trace access as unverified rather than inferring invocation.

GitHub Copilot cloud agent and CLI have their own agent selection surfaces.
The `.vscode` settings apply to VS Code; they are not GitHub account settings.
For another coding host, follow its discovery rules. `AGENTS.md` includes direct
skill links so a host can read the same procedures without duplicating folders.

If custom agents are missing from a Copilot CLI session launched inside VS Code,
check whether that editor version exposes
`github.copilot.chat.cli.customAgents.enabled` and enable it if available.
The setting is listed in the current documentation but absent from the current
development extension manifest, so this template does not require that
version-specific setting. See the [settings reference](https://code.visualstudio.com/docs/agents/reference/ai-settings)
and [extension manifest](https://github.com/microsoft/vscode/blob/main/extensions/copilot/package.json).

If files are missing from discovery, first check the workspace root, names,
frontmatter, duplicate installations, and actual host/version. Supported standard
folders avoid dependence on deprecated custom-path settings. Opening the parent
repository, a subfolder, or a Git submodule can produce different discovery results.
Test the chat surface you actually use; editor inline suggestions are distinct
from Chat. A reported workaround or an Insiders patch does not prove your stable
build is fixed. See [the community evidence](research/community-lessons.md).

## Verification and maintenance

CI runs metadata diagnostics and the existing repository checks. These validate
the documented static fields and local Markdown links; they do not validate every
host-specific metadata field or prove invocation in your editor. Keep names distinct
and references near
their entrypoint. Do not add all skills to every prompt or create a mandatory
multi-agent chain for routine edits. Existing generated repositories need a
reviewed update to inherit new defaults.

Current sources, checked 9 September 2026:
[GitHub skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills),
[GitHub custom-agent fields and tool aliases](https://docs.github.com/en/copilot/reference/custom-agents-configuration),
[VS Code skills](https://code.visualstudio.com/docs/agent-customization/agent-skills),
[VS Code custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents),
[VS Code settings](https://code.visualstudio.com/docs/agents/reference/ai-settings).
