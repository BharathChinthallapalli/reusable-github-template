---
name: solution-architecture
description: Produce a code-grounded workload design or interface specification for a material integration, migration, or new capability. Connect constraints, boundaries, contracts, quality scenarios, and delivery evidence; skip routine implementation planning that changes no architectural contract.
---

# Design a solution that can be implemented and checked

Use [repository discovery](../repo-discovery/SKILL.md) to establish real entrypoints,
interfaces, versions, state, and deployment evidence. Read relevant Accepted ADRs
through [the decision index](../../../docs/adr/README.md). Separate current
architecture from the proposal and recorded requirements from assumptions.

Read [the design method](references/design-method.md) for workload, interface, or
shared-strategy work. Adapt the [design packet](assets/design-packet.md) to the
decision's scope. Compare feasible alternatives, including extending the current
system, against hard constraints before preferences. Trace significant quality
requirements to observable scenarios and verification; do not invent targets.

Show only useful views of the system and name trust and ownership boundaries.
Document contracts, failure behavior, compatibility, migration, and operational
consequences where they distinguish the options. Use actual resource names only
when repository or authorized live evidence supplies them; a configured name is
not proof of an existing deployment. Verify version-dependent platform facts with
current official documentation and label access or knowledge gaps.

Use [architecture review](../architecture-review/SKILL.md) for consequential
tradeoffs and [implementation planning](../implementation-planning/SKILL.md) to
sequence delivery. Link a durable decision to an ADR through
[write-adr](../write-adr/SKILL.md); an Agent Design Document serves the separate
[agent-change gate](../../../docs/add/README.md), not every workload design.

Return the selected option, evidence, unresolved risks, and implementable next
slice. For an authorized implementation request, continue beyond the packet into
delivery and update the design when observed behavior changes its assumptions.
