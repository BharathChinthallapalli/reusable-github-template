# Validation record

Template version: 1.1.0. Prepared 9 September 2026.

## Results

- Linux with Python 3.12.14: repository checker passed.
- All 26 unit tests passed in the uninitialized template.
- A disposable project initialized successfully; its checker and all 26 tests passed.
- Repeating initialization with identical inputs left every deliverable file unchanged.
- YAML and JSON configuration parsed; workflow, issue-form, and AI frontmatter checks passed.
- Action commit references and ruleset fields were checked against current first-party sources.
- All five skills passed the skill format validator; five agent profiles use documented fields and explicit tool scopes.
- A new regression test first demonstrated missing checks for broken agent/skill references, then passed after extending the existing link checker.
- An independent static review checked discovery, routing, clean-code scope, and host limitations. Its reviewer-evidence handoff finding was corrected.

Tests exercise macOS-style ancestor symlinks and managed enterprise usernames.
Native macOS and Windows runs were not performed in this environment.

## Scope

This record concerns local preparation of the repository foundation. Published
v1.0.0 passed [GitHub CI](https://github.com/BharathChinthallapalli/reusable-github-template/actions/runs/34393922313).
For later commits, inspect [their CI runs](https://github.com/BharathChinthallapalli/reusable-github-template/actions/workflows/ci.yml)
for evidence tied to that exact revision. No application, ruleset import,
remote team permissions, or Azure deployment has been exercised.

Custom-agent and skill invocation inside VS Code or Copilot cloud was not
executed in this environment. Static validation establishes file format and
links, not host activation or model compliance. Follow the discovery check in
[AI assistance](docs/ai-assistance.md) in the actual client.

## Local commands

```bash
python3 tools/check_repository.py
python3 -m unittest discover -s tests -v
```

The tooling tests cover preview behavior, successful initialization, preservation
of subsequent edits, invalid input, missing targets, unsafe paths and symlinks,
CODEOWNERS activation, mutable Action references, stale check names, broken local
links, unresolved project markers, and invalid Python syntax.

The delivery process also parses all YAML/JSON files and checks GitHub workflow,
issue form, and ruleset structure locally. YAML parsing is an extra delivery check
using the available environment; PyYAML is not required by the included tools.
The local structure checks do not replace validation by GitHub's services.

## Boundaries of the repository checker

`tools/check_repository.py` checks the foundation's expected files, project markers,
local Markdown links, basic workflow properties, check-name agreement, and Python
syntax. Its workflow checks are deliberately limited textual checks. It is not
a full YAML/schema validator, a secret scanner, or a security analyzer.

Add application-specific lint, type checking, behavior tests, dependency review,
and security tooling when the application exists. These repository tools do not
establish the application's correctness. Review GitHub Actions runs before
activating the included ruleset.
