# From a request to a supported solution

Start at the task the user actually needs. An agreed bug fix can go straight to
implementation; a wording correction can go straight to the documentation writer.
The stages below are available procedures, not a required approval chain.

## Choose the task route

Match the requested outcome to a route, then start at the first unresolved step.
Research means inspecting the relevant repository and evidence; external research
is needed when the question depends on information outside that evidence.
An agreed feature does not require another approval of its intent. Reuse sufficient
existing tests, current decisions and still-applicable validation results.

| Request | Working sequence and relevant procedures | Evidence to finish |
| --- | --- | --- |
| Explore an idea or compare approaches | [Discover the need](../.agents/skills/solution-discovery/SKILL.md), research unknowns, then [compare feasible plans](../.agents/skills/implementation-planning/SKILL.md). Implement only when the request includes implementation. | A recommendation tied to the user outcome, meaningful alternatives and explicit remaining questions. |
| Implement a feature | [Trace affected behavior](../.agents/skills/repo-discovery/SKILL.md), plan material unknowns, implement with [clean-code](../.agents/skills/clean-code/SKILL.md), then [verify](../.agents/skills/verify-change/SKILL.md). | The requested behavior works through its consumer and relevant existing contracts still hold. |
| Fix a reported bug | [Reproduce and isolate the cause](../.agents/skills/systematic-debugging/SKILL.md), make a focused correction, then verify the reproducer and affected behavior. Use [Actions debugging](../.agents/skills/github-actions-debug/SKILL.md) for a workflow-run failure. | Evidence connects the reported failure to the correction; an unreproduced report remains an uncertainty, not a verified fix. |
| Refactor existing code | Identify behavior to preserve, inspect coverage with [test-design](../.agents/skills/test-design/SKILL.md), fill meaningful gaps, then [refactor in checked increments](../.agents/skills/clean-code/references/safe-changes.md). | Relevant behavior checks pass before and after; necessary behavior changes are identified separately. |
| Explain a system or decision | Trace the relevant code or sources, then use [documentation-writing](../.agents/skills/documentation-writing/SKILL.md) for the reader's question. | A traceable explanation with a concrete example; a diagram or interactive example when it improves understanding. |
| Make a routine prose or configuration correction | Inspect the affected contract, edit directly, and run the relevant link, parser or other focused check. | The correction is usable and verified without an unrelated design or test exercise. |

Use the existing [role map](#select-a-responsibility-by-its-output) if specialist
help resolves a concrete uncertainty. Review substantial completed changes against
the original intent and raw diff; the implementer's summary alone is insufficient.
Available tools and authorization govern execution. No route requires a named
external product, a fixed agent chain or loading the whole reference library.

For tradeoffs, read the relevant [engineering principle](engineering-principles.md)
and follow its link to the current decision or procedure. Choose executable checks
with the [repository tool guide](repository-tools.md); application commands still
come from [project context](project.md) and actual manifests.

## Select a responsibility by its output

| Need | Profile when supported | Procedure and useful output |
| --- | --- | --- |
| Understand an unclear need or evaluate a solution | `solutions-engineer` | [Solution discovery](../.agents/skills/solution-discovery/SKILL.md): concrete user task, baseline, constraints and bounded proof |
| Design a workload or integration | `architect` | [Solution architecture](../.agents/skills/solution-architecture/SKILL.md): actual/proposed boundaries, testable contracts, quality scenarios and delivery implications |
| Review shared strategy or consequential tradeoffs | `principal-architect` | [Architecture review](../.agents/skills/architecture-review/SKILL.md): risks, alternatives, scoped exception recommendations, migration and reconsideration evidence |
| Implement an agreed change | `engineer` | Existing clean-code, test and verification procedures; a working slice in the actual stack |
| Write material that a reader can use | `documentation-writer` | [Documentation writing](../.agents/skills/documentation-writing/SKILL.md): audience-specific material with factual checks and a reader walkthrough |
| Deliver and hand off | `release-engineer` or `solutions-engineer` | Existing release procedure plus [operational readiness](../.agents/skills/operational-readiness/SKILL.md): artifact, observed outcomes, owner and remaining work |
| Author GitHub Agentic Workflows | `engineer` or `release-engineer` | [Workflow development](../.agents/skills/agentic-workflow-development/SKILL.md): source, compiler/version, generated workflow, bounded effects and run evidence |

All skills also work as procedures in the current session. A missing native
profile does not require installing another host. Profile tool lists and source
instructions are not a sandbox or organizational authority. Preserve existing
authorization; a principal title cannot approve another team's exception.

## Maintain one connected set of records

Use the [solution brief](../.agents/skills/solution-discovery/assets/solution-brief.md)
for an unclear problem and the
[design packet](../.agents/skills/solution-architecture/assets/design-packet.md)
for a consequential solution. Keep working records in the project's existing
location, such as an issue or `docs/architecture/`, and link to their source
revision. Do not create empty records for work that does not need them.

- `docs/project.md` describes the actual system and commands.
- `docs/adr/` preserves decisions, alternatives and status.
- `docs/add/` binds the existing protected agent/skill/hook changes.
- The design packet connects requirements, boundaries and evidence without
  repeating every ADR or ADD.
- `docs/runbooks/` contains repeatable operational actions and recovery.
- Test reports, traces and deployment records show what was observed on a
  particular revision and environment. A summary status cannot replace them.

For an API or other formal contract, separate normative requirements from
rationale, identify the relevant consumer, and map requirement IDs to observable
checks. Do not label an ordinary design note as an external standard or claim
conformance from headings alone.

## Apply Azure procedures only to Azure work

The [Azure capability map](azure-capabilities.md) explains service-family routes
and source coverage. Keep the existing repository toolchain: Terraform remains
Terraform; Bicep remains Bicep; azd is used when the project selects it.

Preparation produces missing or changed source/configuration and a target plan.
Validation records checks that actually ran against that plan, artifact and
environment. Deployment consumes current evidence and executes the authorized
change. Reuse still-applicable evidence instead of repeating the whole sequence
for every request. A changed target, artifact, dependency or significant setting
invalidates the affected evidence and identifies what needs rechecking.

Resource discovery, troubleshooting, costs and AI evaluation can run independently
of deployment. Missing permissions mean incomplete evidence, not an empty account
or a successful readiness check. An installed skill does not connect Azure or
Foundry; inspect actual tools and credentials in the chosen host.

## Examples of useful requests

> Write a first-run guide for this repository. Derive prerequisites and commands
> from its files, try the documented local path in a disposable copy, and record
> exactly which step fails or cannot be tested. Keep setup instructions separate
> from architecture explanation.

> Design an internal approval service using the existing stack. Trace the request,
> identity, data and failure paths. Compare a small extension with a separate
> service against our known access and recovery requirements. Leave unknown
> traffic and availability targets open; define the next useful measurement.

> Two applications propose incompatible shared identity conventions. Review their
> current ADRs and actual consumers. Explain whether a shared standard is justified,
> what migration would cost, where a scoped exception is needed, and which owner
> must decide. Return recommendations without changing access or accepted policy.

> Prove that the existing integration solves the support team's search task using
> representative permitted data. Agree measurable criteria, compare the baseline,
> build the smallest working slice, and hand over observed results plus the
> remaining production work. A demo that looks correct is insufficient evidence.

> This Azure app already uses Terraform and a release pipeline. Validate the
> current candidate and deploy to the already-authorized staging environment if
> its required evidence is current. Preserve the existing toolchain and show
> deployment outcome separately from critical user-path and recovery checks.

## Research behind these procedures

The [implementation map](research/engineering-expansion.md) ties source observations
to additions. [Architecture references](research/architecture-practice.md) include
Microsoft workload guidance, SEI tradeoff analysis, C4/arc42, author-hosted Staff
Engineer and Cosmic Python material, and a publisher's architecture book sample.
The research record states exactly what was read; it does not claim whole-book
coverage or that adopting a method certifies the design.
