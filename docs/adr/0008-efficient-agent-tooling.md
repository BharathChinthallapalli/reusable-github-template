# 0008: Use the requested tools through shared agent defaults

Status: Accepted
Date: 2026-09-13

## Context

The user requested ripgrep, fd, fzf, jq, lazygit and Hack Nerd Font as defaults
for agents working from this template. Shared instructions already reach the
bundled profiles, Copilot instructions and the Claude import. Most of these
tools are not installed by the current Copilot setup workflow. A terminal UI or
font cannot supply a noninteractive command interface to an unattended agent.

## Decision

Add one canonical tool-use policy in `docs/agent-tooling.md`, referenced by
AGENTS.md, Copilot and repository discovery. An agent with shell execution must
use the applicable available tool: ripgrep for content, fd/fdfind for paths,
jq for JSON, and fzf for bounded fuzzy selection with a noninteractive filter.
Preserve ignore rules, handle filenames as data, check exit status and keep
results scoped. A host without shell execution uses its available read/search
tools without claiming it ran a CLI. Document a missing-tool fallback once.

Install the four noninteractive tools from Ubuntu's configured package sources
in the existing Copilot setup job and smoke-test their actual behavior. Log
resolved versions; this package-manager setup is not a fully pinned environment.
Keep Python validation dependencies and required CI job names unchanged.

Use lazygit for human-driven interactive Git review. Unattended agents use Git's
noninteractive commands for the same operations; a terminal UI must not leave an
automated task waiting for input. Select Hack Nerd Font Mono for the VS Code
terminal, with a monospace fallback, and document workstation installation.
Do not install a font or start a terminal UI in headless setup.

This extends ADR 0007's local-reference design with the user's explicit tooling
choice. It does not add tool permissions, a new agent, a shell alias, a hosted
service or a mechanism that forces clients to obey instructions. Existing
host permissions and project authorization continue to govern actions.

## Validation and consequences

Verify shared links, skill format, metadata and ADD bindings. Run bounded command
examples, a forward exercise for missing tools/noninteractive use, and the
modified Copilot setup workflow. A passing setup run proves package availability
and smoke behavior in that runner; native agent selection and workstation font
rendering require separate observation. Recheck commands when their interfaces,
Ubuntu image, package sources or host instruction behavior change.
