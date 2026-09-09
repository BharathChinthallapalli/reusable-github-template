# Repository context for Copilot

This repository starts as a reusable foundation. Read `docs/project.md` for the
actual project's purpose, architecture, commands, and operational constraints.
Follow `AGENTS.md` for repository work and validation. There is no application
stack until its manifests and code are added.

Prepare the validation environment described in `docs/using-the-template.md`.
Use the command map and required checks in `AGENTS.md`, including the skill
catalog and separate Git integration lane. These checks exercise
the template tools, not application behavior. State what was actually tested.

Use the existing design and dependencies. Keep patches focused, preserve user
edits, and add behavioral regression coverage for meaningful failures. Never
invent resource names, configuration, test results, or supported features.
Keep private data and secrets out of source and generated examples.

## Default workflow and clean code

Use the bundled skills automatically when relevant; follow the task routing in
`AGENTS.md`. Before changing code, read `.agents/skills/clean-code/SKILL.md` and
its applicable references. Use `.agents/skills/verify-change/SKILL.md` to choose
meaningful evidence. For a review, use `.agents/skills/code-review/SKILL.md`.

Prefer expressive names, cohesive responsibilities, clear control flow, visible
side effects, and the existing error contract. Extract an abstraction only for
a present concept, shared rule, or real boundary. Refactor in small verified
steps that preserve observable behavior. Avoid arbitrary line limits and
speculative interfaces, factories, wrappers, or reorganizations.

The generated inventory in `docs/ai-catalog.md` lists specialist agents and the
shared `.agents/skills` procedures. When delegation is supported, use specialists
for bounded independent work that improves the result. Otherwise perform the
relevant procedure directly. Keep the user's selected model and host approvals.
Do not claim that installing these files guarantees invocation or starts a
background process. Discovery checks are in `docs/ai-assistance.md`.
