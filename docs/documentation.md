# Documentation work

Use `documentation-writer` for developer guides, onboarding, references and
explanations. The
[documentation-writing skill](../.agents/skills/documentation-writing/SKILL.md)
also works from a normal engineering session; selecting a profile is optional.

A useful request supplies the reader and outcome:

> Rewrite the onboarding guide so a new maintainer can run the repository checks
> from a clean checkout. Derive commands from this repository, test the supported
> local steps, and record anything you could not execute.

The writer checks source claims and the reader's path. It uses the existing
documentation system and does not introduce Astro, MkDocs or a new hosted site
unless the task needs one. For this foundation,
`python3 tools/check_repository.py` verifies structure and local documentation
links; it does not run every example or render the pages.

Keep decision rationale in [ADRs](adr/README.md), protected agent behavior in
[ADDs](add/README.md), and operational recovery in [runbooks](runbooks/README.md).
A tutorial teaches a first outcome, a how-to solves a task, a reference describes
a contract, and an explanation develops understanding. Link between them where
useful rather than repeat the same contract.

For ongoing documentation automation, start with the bounded recipe in
[agentic workflows](agentic-workflows.md). Its design is included; an engine,
scheduled job or external output is not automatically activated.
