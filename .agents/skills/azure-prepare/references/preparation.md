# Repository to Azure preparation

## Establish readiness

Build a component inventory from manifests, lockfiles, entrypoints, Dockerfiles,
IaC, runtime configuration and actual call paths. For each deployable component,
record language/runtime version, build and start commands, port/health route,
configuration names, native dependencies, external dependencies, persisted data,
background work and network access. A local emulator, in-memory session store or
filesystem write is an explicit deployment assumption, not automatically a bug.

Run proportionate authorized build/tests using the project's commands. Record
the result and revision. Static inspection can establish that a command is
configured; it cannot establish that the build succeeded. Evaluate framework and
SDK compatibility against current official documentation for installed versions.
Do not classify non-Azure SDK imports as requiring migration without tracing
whether that external integration must remain part of the solution.

## Map components to services

Choose from requirements rather than a default cloud template. Compare the
simplest viable option with alternatives where latency, operations, portability,
scale, identity, data residency, or cost changes the decision. Existing resource
IDs and ownership matter: reference resources intentionally instead of
recreating them. Incremental deployment mode alone does not prevent updates to
existing resources; inspect the proposed resource-level changes.

Resolve tenant, subscription, cloud, environment, target region and resource
group from explicit task context and project configuration. If sources disagree,
identify the conflict before a live operation. Never silently select another
region or subscription to work around quota. Available quota is not a reservation
of physical capacity. Pricing estimates include currency, region/SKU, usage units,
period, price source/date and assumptions; no catalog quote proves the actual bill.

Record deployment and runtime identities separately, required role/action/scope,
secret references, ingress/egress, private DNS dependencies, data retention and
recovery. Select zone/region redundancy from recovery requirements and service
support, not from a universal production checklist. Budget or permissions can
leave a live check unknown without invalidating a useful local design.

## Load only relevant service guidance

| Detected need | Research before implementation |
| --- | --- |
| Web app, container, function | Runtime/hosting limits, startup contract, probes, scale and supported identity for the chosen service |
| Storage, queue, database | Data-plane permissions, durability, consistency, retry/idempotency, lifecycle and migration semantics |
| AKS or VM requirement | Actual workload need, operating ownership, networking, supported versions, quota and capacity; do not add a cluster for an ordinary app by default |
| AI/Foundry model or agent | Version, deployment SKU, region/data processing boundary, quota unit, input/output contract, evaluation and telemetry destinations |
| API Management or MCP | Authentication, per-caller authorization, tool schema, caching isolation and measured rate/cost controls |
| Existing cloud/SDK migration | Compatibility assessment, data movement, coexistence/cutover, rollback and current source/target documentation |

Use the selected service's Microsoft Learn documentation and existing module
source. Preserve lockfiles and supported versions. Do not copy an upstream sample
without reconciling its resource scope, identities, API versions and cost.

## Deliverable and handoff

Record all generated artifact paths and configuration inputs. Reference the
accepted ADR for material tradeoffs. Identify local versus live validation and
which outcomes remain blocked. See [Azure delivery](../../../../docs/azure-delivery.md)
for OIDC and environment setup. A plan or ready ADD is not an Azure approval token.

Sources: [Microsoft preparation](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-prepare/SKILL.md),
[onboarding architecture rubric](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-app-onboard/prepare/references/validation-rubric.md),
[enterprise infrastructure planner](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-enterprise-infra-planner/SKILL.md).
These inform original procedures; upstream defaults do not override project requirements.
