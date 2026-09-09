---
name: architecture-review
description: Evaluate a proposed or implemented architecture against business constraints and measurable quality scenarios. Use for consequential design tradeoffs, shared-platform choices, or migration risks; use code-review for ordinary diff defects.
---

# Review architecture through evidence and counterexamples

Establish the decision under review, its current revision, relevant Accepted ADRs,
stakeholders, hard constraints, and claimed improvement. Inspect real contracts
and implementation evidence; distinguish an observed system from a proposed
design. Missing evidence is an uncertainty, not an automatic defect or pass.

Read [tradeoff review](references/tradeoff-review.md) and adapt the
[review record](assets/architecture-review.md). Select the runtime, failure, and
change scenarios that could alter the decision. Compare feasible alternatives
against these scenarios, including the simplest extension where credible.

Trace concrete counterexamples, quality interactions, migration dependencies, and
operational ownership. Tie each finding to an affected boundary, consequence, and
evidence or a specific next check. Use
[bounded experiments](../bounded-experiments/SKILL.md) if an authorized experiment
can resolve a consequential uncertainty; avoid speculative benchmarking.

Return the justified recommendation, unresolved risks, and decision-reversal
conditions. Recommendations do not approve a design, waive requirements, or grant
execution authority. Stop when the decision has sufficient evidence; reopen for
new information or failed validation, not to accumulate repeated agreement.
