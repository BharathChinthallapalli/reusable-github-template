# Validation record

Template version: 1.0.0. Prepared 9 September 2026.

## Results

- Linux with Python 3.12.14: repository checker passed.
- All 25 unit tests passed in the uninitialized template.
- A disposable project initialized successfully; its checker and all 25 tests passed.
- Repeating initialization with identical inputs left every deliverable file unchanged.
- Six YAML files and both JSON files parsed; local workflow and issue-form structure checks passed.
- Action commit references and ruleset fields were checked against current first-party sources.

Tests exercise macOS-style ancestor symlinks and managed enterprise usernames.
Native macOS and Windows runs were not performed in this environment.

## Scope

This record concerns the delivered repository foundation. No application,
GitHub-hosted CI run, ruleset import, remote team permissions, or Azure deployment
has been exercised. The repository must be uploaded and configured to verify
those surfaces.

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
