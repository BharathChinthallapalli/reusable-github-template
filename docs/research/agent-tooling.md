# Agent tooling: sources and validation

Reviewed 13 September 2026 for the user's requested template-wide defaults:
ripgrep, fd, fzf, jq, lazygit and Hack Nerd Font. The implementation extends
template 3.2.0 as version 3.3.0, based on main commit
`4e83258f721da42adddb538bc960160669bb3d6d` (the merged Kun adaptation), through
[ADR 0008](../adr/0008-efficient-agent-tooling.md) and
[the shared policy](../agent-tooling.md).

## Source review and choices

| Primary source inspected | Adopted behavior |
| --- | --- |
| [ripgrep guide](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md) and local help | Scoped text search, filenames/counts when sufficient, explicit hidden-file handling and preservation of ignore rules |
| [fd README](https://github.com/sharkdp/fd) and [manual](https://github.com/sharkdp/fd/blob/master/doc/fd.1) | Filename/glob/type/root filtering, NUL output, `--quiet` presence checks and Ubuntu's `fdfind` executable name |
| [fzf README](https://github.com/junegunn/fzf) and [manual](https://github.com/junegunn/fzf/blob/master/man/man1/fzf.1) | Separate fuzzy filtering from filesystem traversal; bounded stdin plus `--filter`, `--read0` and `--print0` in unattended work |
| [jq manual](https://jqlang.org/manual/) | Structured selectors, `--arg` values and predicate-aware interpretation of `-e` |
| [lazygit README and installation](https://github.com/jesseduffield/lazygit) | Interactive Git interface for a person; explicit Git CLI for unattended work. Package availability depends on distribution |
| [Hack Nerd Font documentation](https://github.com/ryanoasis/nerd-fonts/tree/master/patched-fonts/Hack), [Homebrew cask](https://formulae.brew.sh/cask/font-hack-nerd-font), [VS Code terminal appearance](https://code.visualstudio.com/docs/terminal/appearance) | Workstation install guidance and terminal font-family selection with fallback; no font dependency in headless jobs |
| [GitHub Copilot environment setup](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-environment) | Extend the existing correctly named setup job, then verify its actual run; the default branch is needed for normal cloud-agent setup discovery |

This is a review of the relevant documented interfaces, not a benchmark or a
complete upstream source audit. No upstream installer script, font binary,
global shell alias or personal tool configuration is bundled. Ubuntu setup uses
its configured package sources and logs resolved versions; it is not a fully
pinned environment. No claim of measured speedup or universal agent compliance
is made.

## Implementation boundaries

AGENTS.md owns the brief defaults and links to one canonical policy. All 13
bundled profiles already reference the shared root instructions. Copilot has a
direct reminder; Claude uses its existing AGENTS import. The discovery skill
links to the policy. Read/search-only profiles retain their declared tools.

Copilot setup installs ripgrep, fd-find, fzf and jq, prints their versions, then
checks content lookup, hidden workflow discovery, a NUL-delimited fuzzy match
containing a space, and a JSON predicate. Shell failure and pipeline failure
propagate to the setup job. Lazygit and Hack Nerd Font apply to interactive
workstations; `.vscode/settings.json` selects the font without installing it.

## Verification record

This section records the initial tool-default change delivered as
`7ef30d93e522b7833f7214938181e238a78d338c`. The later uv, ast-grep and review-skill
follow-up has its own [evidence record](native-tooling.md).

Foundation/link validation, AI metadata, catalog freshness, the changed skill's
format, complete design coverage/bindings and Ruff/Gitleaks checks passed.
All 136 offline tests passed using Python 3.12 and `TMPDIR=/private/tmp`, with an
interpreter path without spaces. The [existing macOS alias and fixture-path
limits](kun-validation.md#existing-platform-failures) remain unchanged.

A disposable version 3.3.0 copy passed foundation, metadata, catalog and design
checks after initialization. Preview changed no content, writing customized the
six declared files, and repeating the same inputs preserved deliverable bytes.

Final local command checks found ripgrep 15.2.0, fd 10.5.0, fzf 0.74.4,
jq 1.8.2 and lazygit 0.65.1. Version commands succeeded. fd presence/no-match
checks, jq predicates, and fzf's NUL preservation for synthetic names containing
spaces and embedded newlines passed, including no-match termination. Lazygit
was not opened interactively. Ubuntu's `fdfind` name and package setup are
checked separately in the modified Copilot workflow.

An independent review found no functional issue with the policy or setup
commands. Four prospective tasks exercised headless Copilot, a read/search-only
review profile, missing-tool fallback, and interactive Git with an absent font.
The review corrected an outdated local tool-availability statement. These are
bounded qualitative exercises, not a measured benchmark or a host invocation
test. Workstation installation and font rendering remain unverified.

The PR records applicable pre-commit checks and the observed results of the
modified Copilot setup workflow and `Repository checks` at the delivered
revision. Normal cloud-agent setup requires the workflow on the default branch;
a successful PR run is not evidence that a native agent followed the policy.

Semgrep 1.177.0 previously ran 200 applicable Python/security rules and 11 Actions
rules on the Kun parent revision with no findings or scan errors. A fresh
`p/github-actions` scan of both workflows after this change ran 11 applicable
rules with **zero findings and zero scan errors**. It used the local OSS engine
with metrics disabled. Python implementation files were unchanged in this update.
