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

## Default workflow and clean code

Use the bundled skills automatically when relevant; follow the task routing in
`AGENTS.md`. Before changing code, read `.github/skills/clean-code/SKILL.md` and
its applicable references. Use `.github/skills/verify-change/SKILL.md` to choose
meaningful evidence. For a review, use `.github/skills/code-review/SKILL.md`.

Prefer expressive names, cohesive responsibilities, clear control flow, visible
side effects, and the existing error contract. Extract an abstraction only for
a present concept, shared rule, or real boundary. Refactor in small verified
steps that preserve observable behavior. Avoid arbitrary line limits and
speculative interfaces, factories, wrappers, or reorganizations.

The repository supplies `engineer`, `architect`, `reviewer`, `debugger`, and
`security-reviewer` custom agents. When delegation is supported, use specialists
for bounded independent work that improves the result. Otherwise perform the
relevant procedure directly. Keep the user's selected model and host approvals.
Do not claim that installing these files guarantees invocation or starts a
background process. Discovery checks are in `docs/ai-assistance.md`.
