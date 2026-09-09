---
schema_version: 1
id: ADD-0002
status: ready
scope:
- .agents/skills/documentation-writing/SKILL.md
- .agents/skills/documentation-writing/references/writing-and-verification.md
- .agents/skills/documentation-writing/assets/documentation-plan.md
- .agents/skills/agentic-workflow-development/SKILL.md
- .agents/skills/agentic-workflow-development/references/workflow-contract.md
- .agents/skills/agentic-workflow-development/assets/workflow-design.md
- .agents/skills/solution-discovery/SKILL.md
- .agents/skills/solution-discovery/references/discovery-and-proof.md
- .agents/skills/solution-discovery/assets/solution-brief.md
- .agents/skills/solution-architecture/SKILL.md
- .agents/skills/solution-architecture/references/design-method.md
- .agents/skills/solution-architecture/assets/design-packet.md
- .agents/skills/architecture-review/SKILL.md
- .agents/skills/architecture-review/references/tradeoff-review.md
- .agents/skills/architecture-review/assets/architecture-review.md
- .agents/skills/operational-readiness/SKILL.md
- .agents/skills/operational-readiness/references/readiness-evidence.md
- .agents/skills/operational-readiness/assets/readiness-record.md
- .agents/skills/azure-prepare/SKILL.md
- .agents/skills/azure-prepare/references/preparation.md
- .agents/skills/azure-prepare/assets/azure-plan.md
- .agents/skills/azure-validate/SKILL.md
- .agents/skills/azure-validate/references/validation.md
- .agents/skills/azure-validate/assets/validation-record.md
- .agents/skills/azure-deploy/SKILL.md
- .agents/skills/azure-deploy/references/delivery.md
- .agents/skills/azure-deploy/assets/deployment-record.md
- .agents/skills/azure-resource-discovery/SKILL.md
- .agents/skills/azure-resource-discovery/references/discovery.md
- .agents/skills/azure-resource-discovery/assets/resource-inventory.md
- .github/agents/documentation-writer.agent.md
- .github/agents/principal-architect.agent.md
- .github/agents/solutions-engineer.agent.md
- .agents/skills/systematic-debugging/references/azure.md
- .agents/skills/security-review/references/azure.md
- .agents/skills/performance-analysis/references/azure.md
- .agents/skills/ai-evaluation/references/azure.md
- .agents/skills/data-contracts/references/azure.md
- .agents/skills/tool-integration/references/azure.md
adrs:
- docs/adr/0004-portable-engineering-capabilities.md
- docs/adr/0005-scoped-agent-design-gate.md
- docs/adr/0006-evidence-based-engineering-workflows.md
binding_sha256: 52073d982dee10152a8c7defceab57dd3ed927df0ff099ebe9023bbd620f1ef5
---
# Evidence-based engineering workflows

## Purpose

Expand the reusable template beyond hooks with the user's requested documentation,
architecture, solutions engineering, Azure and agentic-workflow capabilities. Use
selected-source evidence from gh-aw and Azure Skills plus primary architecture
references. New procedures must improve a concrete engineering task and produce
reviewable outputs using actual project facts.

## Scope and non-goals

The explicit scope covers ten new skill entrypoints, their task references and
assets, three distinct profiles, and Azure references extending existing skills.
Existing routing and profile edits remain owned by ADD-0001. No runtime, cloud
subscription, model engine, external MCP server or scheduled paid workflow is
installed or enabled by these documentation and profile additions.

## Inputs and outputs

Inputs are the user task, repository code and manifests, accepted decisions,
selected current official sources, and authorized live evidence when available.
Outputs include reader-tested docs, a solution brief, a design packet, review
findings, readiness evidence, Azure preparation/validation/delivery records,
resource inventory, or a bounded workflow design according to the task.
Unverified assumptions and inaccessible resources remain explicit unknowns.

## Capabilities and permissions

The user authorizes research, template changes and publication in the named GitHub
repository. Profiles inherit available tools and the session's actual authority.
The principal architect reads and advises; the solutions engineer may implement
and run authorized checks; documentation writing edits relevant prose and uses
available verification tools. A ready document, selected profile or validation
record cannot grant access, authorize spending, approve a design on behalf of a
person or prove a deployed workload healthy.

## Behavior and failure modes

Descriptions route precise tasks and keep code maintenance separate from new
solution discovery. Entry points load only relevant references. Existing project
tools and constraints take precedence over upstream defaults. Evidence is tied
to environment, configuration and revision; stale or incomplete validation must
be repeated only for affected checks, with gaps reported instead of fabricated.
Workflow authoring distinguishes Markdown intent, compiled workflow, run result
and observed external effects. No model engine or schedule is activated merely
because its design is present. Cloud diagnosis is read-only until remediation is
authorized, and retry/cost/operation limits belong to the actual task contract.

## Validation

Run the foundation, metadata, catalog and default ADD checks after reconciling the
implementation, followed by source and initialized-project regression lanes.
Run skill-format validation for the complete bundle. Independently exercise
reader onboarding, partial Azure validation, architecture tradeoffs and workflow
failure/no-change scenarios using synthetic or repository-local inputs. Record
actual outcomes and fix concrete failures. Native host discovery, live cloud
execution and compiled gh-aw execution require separate evidence and must not be
claimed from prose review or metadata validation.

## Risks and alternatives

A larger catalog can misroute tasks or inflate context. Distinct descriptions,
progressive references and extensions to existing procedures reduce overlap.
Copying upstream rules can introduce incompatible tooling and new approval loops;
original task-focused guidance preserves existing authorization and code contracts.
Passive checklists cannot enforce runtime outcomes, so each record distinguishes
observed checks from intended policy. Full framework or cloud SDK installation
would impose unrelated maintenance and cost without a project requirement.
