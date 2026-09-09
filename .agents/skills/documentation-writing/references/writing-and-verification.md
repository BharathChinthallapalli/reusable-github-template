# Writing and verification decisions

## Select the document job

| Reader need | Organize around | Completion evidence |
| --- | --- | --- |
| Learn through a first successful task | One concrete outcome, minimal prerequisites and a continuous path | A fresh reader environment reaches the stated result |
| Complete a known task | Starting state, actions, expected state and relevant failure recovery | The task works under the documented conditions |
| Look up a contract | Actual commands, fields, types, defaults, limits, outputs and errors | Entries agree with parser/runtime and supported examples |
| Understand a design | Problem, boundaries, alternatives, consequences and links to decisions | Claims trace to actual code or clearly marked proposals |

Use the project's domain terms. Keep rationales in explanations or decisions
rather than interrupt every tutorial step. Do not remove a necessary constraint
just to shorten prose.

## Resolve evidence before drafting

Record exact repository revision or local snapshot, supported environment and
the implementation that establishes each consequential claim. Prefer actual CLI
help, schemas, manifests, tests and callers over an old README. Tests establish
intended assertions; record whether they ran. Read current primary documentation
for version-sensitive platform behavior.

For a reference, inspect both accepted input and actual runtime behavior: required
versus optional, default versus example, omitted versus null, retryable versus
permanent error. Flag missing contract evidence rather than fill it from intuition.
For a migration, document old and new behavior, affected users, necessary action
and how to tell whether migration succeeded.

## Verify as a reader

Use a temporary checkout or directory when the procedure changes files. Start
from the prerequisites stated on the page, not the author's warm environment.
Capture command, working directory, relevant tool version, expected result,
observed result and failure location. Use sanitized sample configuration.

Do not automatically run an instruction that publishes, changes access, spends
on cloud resources or removes user data. Existing task authorization governs
those operations. When unavailable, verify the preparatory steps and clearly
mark the unexecuted boundary; do not replace it with a claimed success.

Run the existing link/build checks that cover the change. For this foundation,
`python3 tools/check_repository.py` checks repository structure and local
documentation links; it does not execute every example or render Markdown.
Discover application documentation commands from project manifests and CI;
`make build-docs` from another repository is not a universal command.

For rendered pages, review the actual output where navigation, diagrams, long
code samples or responsive behavior changed. A clean build cannot prove a diagram
renders correctly or the text matches the code. Avoid a browser requirement for
a plain text procedure with no hosted site.

Stop when the changed claims have proportionate evidence. Report a pre-existing
failure separately and repair it only when it blocks the authorized task or
falls within scope. Do not repeatedly rebuild unrelated material.

## Sources and adaptation

Original procedure informed by the pinned gh-aw
[writer profile](https://github.com/asw101/gh-aw/blob/bc153047bde1afe62da5cd4bf03a9dc607d79c7d/.github/agents/technical-doc-writer.agent.md),
[documentation skill](https://github.com/asw101/gh-aw/blob/bc153047bde1afe62da5cd4bf03a9dc607d79c7d/skills/documentation/SKILL.md)
and [new-user walkthrough](https://github.com/asw101/gh-aw/blob/bc153047bde1afe62da5cd4bf03a9dc607d79c7d/.github/workflows/docs-noob-tester.md).
The sources use an Astro site and project-specific commands. This procedure
adapts their reader-task and verification ideas without requiring that stack.
