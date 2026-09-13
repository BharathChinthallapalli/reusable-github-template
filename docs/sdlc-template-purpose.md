# Purpose: support the SDLC through bounded features and specifications

Owner requirements recorded: 13 September 2026.

This repository is intended to help a person take a business idea through the
software development lifecycle (SDLC): requirements, design, implementation,
review, delivery, operations and feedback. The maintainer may own that entire
lifecycle while still learning Git, CI/CD and Azure infrastructure. The template
should supply reusable procedures, working automation and understandable evidence
without assuming the maintainer is already a platform engineer.

This document records the owner's intended direction and the current gap. The
[lifecycle research](research/ai-sdlc-lifecycles.md) compares AI-assisted software
development, AI application delivery, LLMOps, machine-learning development and
specification-driven development. Proposed mechanisms in these documents are
not claims that those mechanisms have been implemented or enabled.

## The unit of delivery is a bounded feature or specification

**Supporting an entire project's lifecycle does not mean asking one agent to
build the entire project in one pass. Development proceeds feature by feature,
against explicit specifications and acceptance evidence.**

A project-level direction provides shared constraints and interfaces. It is then
decomposed into outcomes small enough to implement, review and integrate:

1. **Initiative:** the business problem and expected outcome.
2. **Feature:** one useful behavior, with an explicit scope and specification.
3. **Task:** a bounded piece of that feature with inputs, dependencies and an
   expected result. Investigation can be a task; its result can be inconclusive.
4. **Change/PR:** a reviewable implementation increment linked to its feature and
   acceptance cases. A feature may need several dependent PRs.
5. **Release:** identified artifacts and configuration deployed to a known
   environment, followed by verification and an operational handoff.

Prefer a small working path through the layers the feature needs. Avoid building
every screen, service and data pipeline separately before attempting integration.
Do enough shared design to establish interfaces and dependencies, then refine it
as feature evidence changes. A roadmap is not a request to implement every item.

One agent may complete a bounded task. Independent work can be delegated when
it resolves a real uncertainty or permits useful parallel progress. More agents
do not make an oversized or ambiguous task safe. Each assignment needs a clear
scope, relevant source context, file ownership, dependencies, acceptance evidence
and a stopping condition. Keep one writer per shared file area, integrate in
dependency order and verify the combined result. Independent review examines
both implementation and tests against the feature's accepted behavior.

Existing [task orchestration](../.agents/skills/task-orchestration/SKILL.md) and
[implementation planning](../.agents/skills/implementation-planning/SKILL.md)
provide the underlying procedures. Small fixes retain proportionate checks;
neither a fixed agent chain nor a full new design packet is required for every edit.

## The six phases and their intended GitHub support

| Phase | Intended support | Evidence that the phase produced something useful |
| --- | --- | --- |
| Planning and requirements | Issues for problems/features; Projects for work ordering, ownership and dependencies; discovery and feature specifications | A real user problem, observable acceptance criteria, scope, constraints and the next bounded feature |
| Design and architecture | Markdown contracts, ADRs and optional Discussions for collaborative exploration | A justified design connected to the feature; resolved interfaces and explicit consequential unknowns |
| Development | Git branches, reproducible local/Codespaces setup and bounded agent tasks | A working feature increment with preserved existing behavior and reproducible commands |
| Review and testing | PR review, application CI and configured security/dependency checks | Tests exercise the accepted behavior; relevant findings are resolved; evidence identifies the checked revision |
| Delivery | Application build/package workflows, Releases/Packages where appropriate, environment-specific deployment | Identified artifact and target, successful deployment, critical-path verification and usable recovery instructions |
| Maintenance and feedback | Dependency updates, production signals, bug reports, incident/recovery procedures and feature feedback | An operated service with an owner; observed problems become actionable issues and verified repairs |

CI means automatic checks. CD means automated delivery/deployment steps. Neither
term implies that GitHub has already configured a deployment target or proved an
application meets its requirements. Repository files, platform settings and live
runtime evidence are separate. Security and license-policy checks require the
appropriate rules, configuration and available platform features.

## What this template should make easier for a beginner

- Begin with the business idea and existing facts. The agent should identify the
  first unresolved decision and ask understandable questions instead of expecting
  the maintainer to select unfamiliar cloud services or name specialist agents.
- Explain unfamiliar concepts when they affect a decision. State what a proposed
  command changes, where it runs, the expected result and a relevant recovery step.
- Inspect the company's existing repositories, access boundaries, supported
  services, deployment process and ownership before proposing another toolchain.
- Maintain one connected project record with current facts, decisions, feature
  state, verified commands, evidence and the next action. Link existing issues,
  specs, ADRs, PRs and runbooks instead of copying the same facts everywhere.
- Keep business acceptance and consequential deployment/access/cost decisions
  visible. Reuse authorization already supplied; routine progress should not
  create a new approval request at each procedural stage.
- Distinguish prepared, checked, deployed and observed working. Explain a real
  blocker and continue independent useful work rather than presenting uncertainty
  as a passing check.

## Current implementation versus intended coverage

The inspected source baseline is `a94e2a5995803653a5b993c56bd82bb450b130c6`.
The repository already contains issue/PR forms, a safe project initializer,
34 skills, 13 agent profiles, design/context records, template CI, Copilot setup,
Ruff/Gitleaks checks, dependency-update configuration and lifecycle procedures.

It does not yet ship Projects setup automation, a custom Codespaces development
container, application CI, application infrastructure, a deployment/publication
workflow, or working application monitoring and recovery commands. Its release
configuration categorizes generated notes; it does not publish a release. The
operations worksheet and deployment procedures must be instantiated against an
actual project. This missing project configuration is distinct from missing
template knowledge.

The next implementation work should therefore be separate, reviewable features:
guided repository/project setup; reproducible development setup; feature/spec
traceability; application validation; one selected delivery path; and operational
feedback. Their detailed scope and order belong in individual specifications,
not a single request to generate a whole application or platform.

## Completion criteria for the intended approach

A representative project should demonstrate one feature moving from an issue
and specification to implementation, review, tests, an identified release and
verified operation. A subsequent bug or change should reuse the same path with
proportionate scope. Relevant documentation should let the maintainer identify
what is running, what was checked, where failures appear and how recovery works.

For AI/ML features, ordinary code checks are supplemented by the model/data/eval
evidence described in the research. A green scaffold workflow, a filled template,
a model's confident answer or a successful demo is insufficient to establish
production readiness.
