---
name: task-orchestration
description: Coordinate independent engineering subtasks with explicit dependencies, file ownership, bounded work and evidence-bearing handoffs. Use when parallel research, implementation or review can resolve a concrete uncertainty; do simple work directly.
---

# Coordinate useful parallel work

Identify the integration result and dependencies before delegating. Split by
independent question or file area, not by an arbitrary list of agent titles.
Keep dependent edits sequential and assign one writer to each shared file area.
Research and read-only review can overlap implementation when they do not depend
on its final output. If the host has no delegation capability, do the same work
locally without claiming that specialists ran.

Use the [assignment and handoff record](assets/task-handoff.md) for a substantial
subtask. Give the worker the desired result, minimum source context, owned paths,
integration contract, permitted side effects, budget/stop condition and evidence
required. Do not assume task delegation grants credentials, publication or a
different tool permission level.

For an independent review, supply the request and raw artifact rather than your
preferred conclusion. Keep implementation and reviewer findings distinguishable.
For a dependency failure, report failed or blocked explicitly; silence, an empty
answer or another worker's success cannot satisfy the missing dependency.

At handoff, inspect the actual artifact and changed files. Resolve conflicting
assumptions against code, requirements and current decisions. Do not choose the
majority view merely because more agents repeat it. Preserve unrelated work;
avoid reset-based integration or having multiple workers repair the same file.

The integrating worker owns the final outcome: check interface compatibility,
run the required gates on the combined state and report what was verified.
Use [code-review](../code-review/SKILL.md) for findings and
[verify-change](../verify-change/SKILL.md) for the integrated verification.
Stop or reassign a stalled subtask when its bounded result cannot be obtained;
do not create an indefinite retry or delegation chain.
