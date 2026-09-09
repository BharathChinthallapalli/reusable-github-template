---
name: implementation-planning
description: Plan a material implementation or redesign by comparing feasible alternatives, tracing dependencies, challenging failure modes and defining observable acceptance evidence. Skip a formal plan for a routine edit with an obvious verification path.
---

# Plan a change that can be checked

Start from the user's outcome and the repository's actual contracts. Read current
decision status through the [decision index](../../../docs/decisions/README.md).
Use [repo-discovery](../repo-discovery/SKILL.md) if the affected behavior is unclear.
Record important unknowns instead of selecting a stack, workload or service target
without evidence.

For material work, adapt the [change plan](assets/change-plan.md). Compare the
simplest viable change with a credible alternative; include leaving behavior
unchanged when that is a real option. Evaluate compatibility, migration effort,
operating cost, maintainability and reversibility only where they affect this task.

Challenge the candidate through different questions:

- **Counterexample:** Which valid input, existing caller or supported environment
  contradicts the proposal?
- **Premortem:** Suppose this change fails after release. Trace a plausible cause
  through a real dependency, state transition or trust boundary.
- **Cost of simplicity:** What could be removed while preserving the user's
  outcome? What concrete failure would the removed element allow?
- **Verification:** What independent observable result would falsify the claimed
  improvement? Can the test command actually report failure?

Resolve findings by changing the plan, supplying evidence, or recording a bounded
remaining risk. Independent review is useful for an unresolved consequential
decision; different agent names or repeated agreement do not establish correctness.
Stop challenging when acceptance evidence is sufficient. Reopen only for a new
finding, changed requirement or failed gate.

Sequence the work around dependencies and reviewable behavior changes. Name
shared-file ownership if delegating, using
[task-orchestration](../task-orchestration/SKILL.md). Separate preparation from a
deployment or other external action that requires its own authorization.
Proceed with authorized implementation using [clean-code](../clean-code/SKILL.md)
and [verify-change](../verify-change/SKILL.md); a plan alone does not complete a
request to make the change.
