# Harness opinions

These are revisable design judgments for the [vision](vision.md), not new
permissions, mandatory tools or overrides of accepted decisions. Apply the
current project contract first. A material change to it uses the
[ADR process](../adr/README.md).

| Default judgment | Why it fits this harness | Evidence that would justify reconsidering it |
| --- | --- | --- |
| Begin with local versioned Markdown | It keeps context reviewable alongside the change without a new service. | Repeated retrieval or collaboration failures that a small indexed view demonstrably resolves. |
| Prefer one maintained term and one contract owner | Duplicated definitions make implementation and review disagree. | Distinct bounded domains require different meanings; qualify the terms instead of forcing a false universal definition. |
| Prefer deterministic checks to repeated model review | Repeatable rules should have reproducible outcomes and bounded cost. | A documented judgment cannot be reduced to a reliable rule; use a bounded review with evidence. |
| Keep host-specific integration thin | Shared semantics reduce drift while native envelopes still differ. | An installed host requires distinct behavior; preserve and test that difference explicitly. |
| Start with a bounded task and add help selectively | Coordination, context transfer and conflicting edits cost time. | Independent tasks with clear ownership can progress usefully in parallel. |
| Measure before optimizing context or hooks | Smaller prompts and faster tools matter only if task success and coverage survive. | Representative baseline/candidate results identify a specific bottleneck and a safe improvement. |
| Prefer a working vertical feature increment | It exposes interface mistakes before many disconnected components accumulate. | A shared interface or infrastructure prerequisite genuinely blocks the first useful path. |
| Prioritize Azure/M365 delivery examples for the owner | They match the intended work described in the supplied master prompt. | A project's accepted scope selects another environment; the reusable base need not impose a provider. |

Further Rust tool replacements, signed scope compilation and broader automated
lifecycle services are proposed in the owner's 2026-09-16 master prompt. The
current [tool policy](../agent-tooling.md) already prefers suitable Rust tools
while retaining tools that fit. This page does not replace that policy, accepted ADRs or
[Guardian contract](../guardian.md) with those proposals. Evaluate them through
the [roadmap](roadmap.md), against useful behavior and measurable maintenance cost.

Maintain an opinion when its evidence changes; record an accepted architectural
decision separately. A preference should never masquerade as a runtime guarantee.
