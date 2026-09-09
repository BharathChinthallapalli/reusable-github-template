# Review a consequential architecture decision

## Form falsifiable scenarios

Replace qualities such as scalable, secure, or maintainable with an observable
situation: source and trigger, operating condition, affected boundary, expected
response, and measurement. Obtain targets from requirements or measured evidence.
If a threshold is unknown, record who can establish it and why it matters rather
than assigning a convenient number.

Include the differentiating case rather than an exhaustive taxonomy. A normal
request, a dependency failure, and a schema or deployment change may expose very
different properties. For example, a cache can improve latency while making
permission revocation or freshness harder; the acceptable delay is a requirement
to establish, not a universal default.

Prioritize scenarios by consequence and uncertainty. Check hard constraints first.
Preference scores cannot compensate for violating a required access boundary or
compatibility contract. Weighted scores are useful only when weights and evidence
have an explicit basis and uncertainty is visible.

## Challenge options from different directions

| Lens | Question | Evidence worth seeking |
| --- | --- | --- |
| Counterexample | Which supported input, consumer, or operating condition breaks the claim? | Contract case or trace with the concrete failure |
| Failure and recovery | What state remains after a partial failure or repeated operation? | Recovery mechanism, idempotency identity, restoration result |
| Quality interaction | Does improving one goal worsen another? | Measured or reasoned effect on cost, freshness, latency, isolation, or change effort |
| Change and migration | Can current consumers operate during the transition? | Version coexistence, data migration, deployment order, rollback limits |
| Organizational fit | Who owns and can support each boundary? | Actual responsibilities, skills, constraints, and escalation path |
| Simplicity | What can be removed while preserving the outcome? | A smaller feasible option and the failure it would or would not introduce |

Different lenses should produce distinct observations. Additional agents or
repeated rounds do not establish correctness by voting. Use independent review
only when it can examine a real unresolved uncertainty within the task's scope.

## Make findings actionable

For a risk, identify the affected scenario, source evidence, causal path to harm,
severity rationale, and bounded remediation or verification. Separate observed
defects from hypotheses. A sensitivity is a choice whose variation changes an
important result; identify its range or unknown threshold. A tradeoff affects
multiple goals, so record who accepts the consequence under existing authority.

Recommend proceed, revise, or gather specific evidence. Record remaining risks
with owners and review conditions, without creating a new approval process.
For the selected option, name the observation that would reverse the decision.
Reconcile implementation differences with the design rather than silently
reviewing an obsolete diagram.

## Sources and scope

Reviewed 2026-09-09. Original practical review guidance, not a full or certified
Architecture Tradeoff Analysis Method evaluation and not copied templates.

- [SEI ATAM collection](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/).
  Read the overview, method steps, and results; it supports connecting quality
  scenarios and interacting decisions to business risks. Linked reports were
  not all read.
- [arc42 quality requirements](https://docs.arc42.org/section-10/).
  Read quality overview and scenario forms, including usage and change scenarios;
  use measurable acceptance rather than broad quality adjectives.
- [Microsoft ISE design reviews](https://microsoft.github.io/code-with-engineering-playbook/design/design-reviews/).
  Read the substantive article; apply its balance between early risk reduction
  and time to decision, with traceable design artifacts near the implementation.
- [Will Larson: staff archetypes](https://staffeng.com/guides/staff-archetypes/).
  Read the author-hosted guide, especially the architect's domain responsibility;
  this is selected book-related material, not the full Staff Engineer book.
  A title does not supply authority or replace knowledge of the actual system.
