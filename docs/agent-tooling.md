# Efficient tools for repository agents

This is the shared tool-use policy for assistants following this template.
For shell-based repository work, agents **must use the applicable available tool
below**. Choose by the operation; invoking every tool on every task wastes work.
Check availability once per environment, then reuse that knowledge. Built-in
read/search tools remain the route for hosts or profiles without shell execution.
Do not change a profile's permissions just to run a preferred command.

## Choose the tool by the operation

| Operation | Required default when available | Noninteractive use and limits |
| --- | --- | --- |
| Search source or instructions | **ripgrep (`rg`)** | Scope paths first. Use `rg -n -F -- 'literal' PATH` for literal content, `rg -l` for matching filenames, or `rg --files` for a search-file inventory |
| Locate files or directories | **fd (`fd`, packaged as `fdfind` on Ubuntu/Debian)** | Use filename/glob/type filters and a root, such as `fd --type f --glob '*.py' tools`. Both executable names satisfy this policy |
| Narrow a candidate list by approximate name | **fzf** | Feed a bounded list and use `--filter` for unattended work. Inspect the matches before acting; fuzzy ranking is not proof that a file is the intended target |
| Inspect or filter JSON | **jq** | Use selectors, `-r` for string output and `-e` for assertions. Pass external values with `--arg`/`--argjson`; do not interpolate them into jq source or parse JSON with regex |
| Search code by syntax | **ast-grep** | Use an explicit language, quoted pattern, scoped input and JSON output; use `ast-grep`, since Linux's `sg` can mean a different program |
| Install this template's Python validation dependencies | **uv** | Use `uv pip install --python python -r requirements-dev.txt` in the prepared virtual environment; retain the application's chosen package manager |
| Lint this template's Python | **Ruff** | Use the existing hook/check commands and pinned rules. Formatting changes require a project formatting contract |
| Inspect Git interactively with a person | **lazygit** | Use in a human-driven terminal. Automated agents use `git status --short`, `git --no-pager diff` and other explicit Git commands; do not open a TUI that waits for input |
| Render terminal text and icons | **Hack Nerd Font Mono** | Select the installed font in the local terminal. The VS Code workspace selects it with `monospace` fallback. Fonts do not change agent parsing or headless execution |

These defaults apply to exploration and command use, not the application's
runtime implementation. Keep existing application libraries and test commands.
Use [repository checks](repository-tools.md) for validation. For a security/code
scan, use the project's Semgrep rules when present; otherwise select relevant
reviewed rules, disable metrics for a local scan, and record rule/tool versions
and coverage. A Semgrep finding needs a code-path review; zero findings do not
prove the absence of defects. Semgrep is not a dependency of routine searches.

For syntax-aware investigations, use ast-grep's scoped `run` command. For example,
`ast-grep run --lang python --pattern 'subprocess.run($$$ARGS)' --json=compact tools`
lists matching calls, not vulnerabilities. Inspect arguments and affected callers
before drawing conclusions. Quote metavariables to prevent shell expansion and
avoid rewrite/interactive options during searches. JSON `[]` is no result, not a
policy pass. Check command failures separately from a no-match result.

When a project has `sgconfig.yml` and tested policy rules, use its documented
`ast-grep test` and `ast-grep scan` commands. Add rules only for an explicit
project contract, with violating and allowed examples, then verify the failure
exit before making them a CI gate. This template ships tool availability, not
a blanket structural rule pack. Keep Gitleaks for secret detection; a fast
regex search is not a replacement. TODOs and debug output need project-specific
scope and exceptions, not a universal ban. See [native tool research](research/native-tooling.md).

## Keep searches useful and automation finite

Start in the relevant directory, then widen only when evidence calls for it.
Keep ignore rules enabled. This template's `.agents` and `.github` directories
need explicit roots or `--hidden`; exclude `.git` when including hidden files.
Do not default to unrestricted scans of caches, generated output or credentials.
If an expected file is absent, inspect path, case, hidden-file and ignore rules
before concluding it does not exist. Use `git ls-files` when tracked-file status,
rather than search visibility, is the actual question.

Request filenames or counts when sufficient, then read bounded matching context.
Do not truncate a result and claim it was exhaustive. Use NUL-delimited paths
(`rg --files -0`, `fd --print0`, `fzf --read0 --print0`) between tools; quote
individual paths and use `--` where supported. Treat filenames and JSON values
as data, never shell source. Avoid parallel mutation through fd execution flags.

For unattended fzf calls, provide input and `--filter`; clear inherited
`FZF_DEFAULT_OPTS` and `FZF_DEFAULT_OPTS_FILE` for that invocation. Do not add
interactive preview, reload or execute bindings. Reuse a saved candidate list
when trying another query instead of repeatedly traversing the repository.

Read exit status as well as output. For ordinary `rg` searches, 1 means no match
and 2 means an error. `fd` can return success with an empty list; use `--quiet`
for a presence assertion. fzf's filter can return 1 for no match. `jq -e` returns
nonzero for false/null/no-result or an error; inspect stderr and the intended
predicate before labeling that a parser failure. A failed search is not evidence
that the task succeeded.

If a tool is missing, state the limitation once and use the closest available
equivalent: `rg --files` or native file search for fd, native text search or
scoped grep for rg, exact filtering for fzf, the existing JSON parser for jq,
and Git CLI for lazygit. Use the setup below when environment preparation is
authorized. Do not repeatedly install tools during investigation or edit global
shell aliases, key bindings, Git configuration or fonts as a side effect of a
routine task.

If ast-grep is unavailable, use scoped rg results plus manual syntax inspection
and report that structural matching was not run. For uv, use the documented pip
fallback in [local setup](using-the-template.md#prepare-local-validation). Missing
Ruff in a required check is a setup failure; do not silently skip that gate.

## Command examples

Run from the repository root. These are reads; replace the query/root with the
current task. On Ubuntu/Debian use `fdfind` in place of `fd` if that is installed.

```bash
rg -n -F -- 'check_design' tools hooks
fd --hidden --exclude .git --type f --glob '*.agent.md' .github/agents
jq -r '.template_version' template.json
jq -e --arg key 'schema_version' 'has($key)' template.json
rg --files --hidden -g '!.git' -0 docs | FZF_DEFAULT_OPTS= FZF_DEFAULT_OPTS_FILE= fzf --read0 --print0 --filter='tool'
git --no-pager diff --stat
```

The fzf example emits NUL-separated candidates, not executable commands. Use a
NUL-aware consumer if passing its results onward. Run `lazygit` from a repository
only when a person is interacting with the terminal.

## Prepare an environment

Copilot's [setup workflow](../.github/workflows/copilot-setup-steps.yml) installs
`ripgrep`, `fd-find`, `fzf` and `jq` on its Ubuntu runner and smoke-tests them.
It records resolved versions. These OS packages follow the configured Ubuntu
repositories; this is not a completely pinned toolchain. Lazygit and fonts are
workstation tools and are not installed by the headless job. The workflow must
be on the default branch for normal Copilot cloud-agent setup discovery.

Both hosted setup jobs pin uv 0.12.13 and retain Python 3.12. Copilot also installs
the ast-grep-cli 0.45.3 binary wheel and checks a real call against comment/string
lookalikes. Only the hosted runners use `uv pip install --system`; local setup stays in
a virtual environment. Ruff is already pinned in `requirements-dev.txt`.
Install ast-grep locally with `uv pip install --python python --only-binary :all:
ast-grep-cli==0.45.3` in that environment, or use the upstream platform packages.
Neither workflow installs frontend frameworks or changes an application's lockfile.

For an authorized macOS workstation setup with Homebrew already installed:

```bash
brew install ripgrep fd fzf jq lazygit
brew install --cask font-hack-nerd-font
```

For Ubuntu/Debian's noninteractive tools:

```bash
sudo apt-get update
sudo apt-get install -y --no-install-recommends ripgrep fd-find fzf jq
```

Use [lazygit's platform instructions](https://github.com/jesseduffield/lazygit#installation)
for its package availability on your distribution. For Windows or another
platform, use the upstream installation instructions linked in the
[source and validation record](research/agent-tooling.md). Avoid assuming a
package name from a different OS exists locally.

Install the [Hack font package](https://github.com/ryanoasis/nerd-fonts/tree/master/patched-fonts/Hack)
using the workstation's font installer and select **Hack Nerd Font Mono** in its
terminal preferences. The [VS Code setting](../.vscode/settings.json) requests
that family but does not install it. Reopen the terminal after installation and
check text/icons visually; headless CI cannot verify font rendering.

Check installed commands with `rg --version`, `fd --version` (or
`fdfind --version`), `fzf --version`, `jq --version` and `lazygit --version`.
Keep versions and failures in the task's validation record. Shared instructions
express the required defaults; actual use still depends on the client loading
them and exposing the necessary tools.
