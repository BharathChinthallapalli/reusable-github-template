# Repository context for Copilot

This repository starts as a reusable foundation. Read `docs/project.md` for the
actual project's purpose, architecture, commands, and operational constraints.
Follow `AGENTS.md` for repository work and validation. There is no application
stack until its manifests and code are added.

For tooling changes run `python3 tools/check_repository.py` and
`python3 -m unittest discover -s tests -v` from the root. These checks exercise
the template tools, not application behavior. State what was actually tested.

Use the existing design and dependencies. Keep patches focused, preserve user
edits, and add behavioral regression coverage for meaningful failures. Never
invent resource names, configuration, test results, or supported features.
Keep private data and secrets out of source and generated examples.
