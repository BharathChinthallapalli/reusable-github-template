# Validation record

Template version: 1.2.0. Prepared 9 September 2026.

## Results

- Linux with Python 3.12.14: repository checker passed.
- All 51 unit tests passed in the uninitialized template, including 25 AI-diagnostic tests.
- A disposable project initialized successfully; preview left its files unchanged, both checkers passed, and all 51 tests passed.
- Repeating initialization with identical inputs left every deliverable file unchanged.
- YAML and JSON configuration parsed; workflow, issue-form, and AI frontmatter checks passed.
- Action commit references and ruleset fields were checked against current first-party sources.
- All five skills passed the skill format validator; five agent profiles use documented fields and explicit tool scopes.
- A new regression test first demonstrated missing checks for broken agent/skill references, then passed after extending the existing link checker.
- Independent static reviews checked metadata diagnostics, discovery, routing, decision status, Git recovery, and host limitations.
- All JSON/YAML configuration and Markdown frontmatter parsed; ADR 0001/0002 statuses, index and reciprocal supersession links agreed.
- Static AI diagnostics passed for five skills and five agents, with host discovery/invocation explicitly unverified.
- Review regressions cover valid alternate tool syntax and agent filenames, duplicate YAML keys, invalid timestamps, deep YAML, description length, and external symlink boundaries.

Tests exercise macOS-style ancestor symlinks and managed enterprise usernames.
Native macOS and Windows runs were not performed in this environment.

## Scope

This record concerns local preparation of the repository foundation. Published
v1.1.0 passed [GitHub CI](https://github.com/BharathChinthallapalli/reusable-github-template/actions/runs/34395756576).
For later commits, inspect [their CI runs](https://github.com/BharathChinthallapalli/reusable-github-template/actions/workflows/ci.yml)
for evidence tied to that exact revision. No application, ruleset import,
remote team permissions, or Azure deployment has been exercised.

Custom-agent and skill invocation inside VS Code or Copilot cloud was not
executed in this environment. Static validation establishes file format and
links, not host activation or model compliance. Follow the discovery check in
[AI assistance](docs/ai-assistance.md) in the actual client.

## Local commands

```bash
python3 -m pip install -r requirements-dev.txt
python3 tools/check_repository.py
python3 tools/check_ai_configuration.py --json
python3 -m unittest discover -s tests -v
```

Use the prepared environment described in [local setup](docs/using-the-template.md).
The tested YAML parser is PyYAML 6.0.3, pinned as a development dependency.

The tooling tests cover preview behavior, successful initialization, preservation
of subsequent edits, invalid input, missing targets, unsafe paths and symlinks,
CODEOWNERS activation, mutable Action references, stale check names, broken local
links, unresolved project markers, and invalid Python syntax.
AI diagnostics additionally exercise valid and invalid metadata, unsupported
YAML constructors, parser failure reporting, and a CLI that preserves input files.

The delivery process also parses all YAML/JSON files and checks GitHub workflow,
issue form, and ruleset structure locally. AI metadata parsing is now an included
CI check using PyYAML. Other YAML/schema checks remain additional delivery checks.
The local structure checks do not replace validation by GitHub's services.

## Boundaries of the repository checker

`tools/check_repository.py` checks the foundation's expected files, project markers,
local Markdown links, basic workflow properties, check-name agreement, and Python
syntax. Its workflow checks are deliberately limited textual checks. It is not
a full YAML/schema validator, a secret scanner, or a security analyzer.

`tools/check_ai_configuration.py` safely parses agent/skill frontmatter and checks
core names, descriptions, invocation flag types, tool declarations and duplicate
metadata. It is a bounded static check of repository files, not a validator for
all optional fields or all coding hosts. JSON output reports host discovery and
invocation as `not_checked`; verify those separately in the actual client.

Add application-specific lint, type checking, behavior tests, dependency review,
and security tooling when the application exists. These repository tools do not
establish the application's correctness. Review GitHub Actions runs before
activating the included ruleset.
