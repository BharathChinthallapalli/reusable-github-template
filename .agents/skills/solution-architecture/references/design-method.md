# Workload design and interface specification

## Build the smallest sufficient packet

Start with the task's outcome, affected users, hard constraints, existing domain
rules, and significant uncertainty. Trace one real operation from entrypoint
through state and side effects before proposing boundaries. An application's
language is established by manifests and execution paths, not a repository's
maintenance scripts. An example folder may be independent from the application.

Choose a context view to explain ownership and external dependencies, a container
view for deployable/runtime boundaries, and a sequence or state view when order,
retries, or transitions matter. Add a deployment view when environment topology
changes the decision. Do not require all diagram types or equate C4 containers
with Docker containers. Mark observed and proposed components distinctly.

Connect each significant requirement to the boundary responsible for meeting it,
the design choice, and an observable test. Include failure and change scenarios
that distinguish alternatives. For a critical data flow, consider authorization,
validation, consistency, retry identity, cancellation, and recovery only to the
depth demanded by its consequences. Delegating a call does not transfer ownership
of the business outcome or imply that retries are safe.

Reject options that violate established hard constraints. For remaining choices,
compare compatibility, build/change effort, operating cost, support burden,
failure modes, and reversibility. Estimate with ranges and assumptions when
measurement is unavailable. Avoid choosing a pattern from familiarity alone.

## Specify an interface or agent contract

State the scope and consumers of the specification. Give each consequential
requirement an identifier and a verifiable outcome. If using MUST or SHOULD,
define what those words mean within this project and distinguish an obligation
from a recommendation. Do not claim RFC or standards conformance from typography.

Describe valid inputs and outputs, required/optional fields, invariants, invalid
input behavior, side effects, permission checks, timeout/cancellation, and version
compatibility as relevant. Identify conformance classes only if different kinds
of consumers or implementations truly have different obligations. Scope each
requirement to the correct class instead of making every rule global.

Trace requirements through the implementation, schema/parser, examples, public
documentation, and behavioral checks. Investigate disagreement: a schema accepting
an input does not establish that the runtime handles it correctly. Include an
invalid example and an older-client case when they exercise actual supported
behavior. Label pseudocode and unexecuted examples; do not invent test results.

## Review a shared strategy

For cross-workload work, extract repeated problems and decisions from actual
designs, incidents, or integration contracts. State which workloads share the
constraint, who owns the shared capability, and where an exception is justified.
Recommend exception scope and reconsideration criteria; do not grant exceptions
or change another owner's policy. A single local implementation detail rarely
requires organization-wide strategy.

Sequence a migration around dependencies and reversible slices, with transition
compatibility and a clear retirement condition. Describe the observation that
would make the proposed standard inappropriate. Return local decisions to local
owners instead of turning this skill into compulsory central governance.

## Sources and scope

Reviewed 2026-09-09. Original synthesis; no source templates or book chapters are
bundled. Consult current source documents when platform behavior matters.

- [Microsoft: architecture design specification](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-design-specification).
  Read technical specification, recovery, and consistency guidance; apply linked
  contracts, rollout, monitoring, and evidence rather than a diagram-only design.
- [C4 diagrams](https://c4model.com/diagrams) and
  [arc42 overview](https://arc42.org/overview/). Read the short overview pages;
  select views that resolve the actual reader's question rather than copying
  every framework section.
- [Will Larson: writing engineering strategy](https://staffeng.com/guides/engineering-strategy/).
  Read the author-hosted introduction, when/why, and design-document guidance;
  infer shared direction from specific decisions and keep documentation modest.
- [Software Architecture in Practice publisher sample](https://www.informit.com/articles/article.aspx?p=3131593).
  Read sample page 1 on mobile-system constraints and energy, not the full book.
  Platform resource and lifecycle differences can invalidate assumed boundaries.
- [W3C QA Framework: Specification Guidelines](https://www.w3.org/TR/qaframe-spec/).
  Read the introduction and requirements/good-practice overview covering scope,
  consumers, normative language, test assertions, and error handling. Verify the
  full applicable requirements before making a standards claim. This interface
  mode is project guidance, not claimed conformance to that specification.
