---
name: "bounded-experiments"
description: "Run a finite sequence of measurable candidate changes with a fixed baseline, explicit editable boundary and resource budget; use for controlled optimization and hypothesis testing."
---

# Run a controlled experiment

1. Establish a measurable hypothesis and an independent success contract. Read
   the existing baseline command, workload, evaluator and relevant decisions.
   Use [ai-evaluation](../ai-evaluation/SKILL.md) for AI behavior or
   [performance-analysis](../performance-analysis/SKILL.md) for resource claims.
2. Complete [the experiment record](assets/experiment-record.md): baseline
   identity, allowed edits, invariant inputs/evaluator, metric direction and
   acceptance tolerances. Set finite attempt and total wall-time limits, plus
   tokens, money, storage or compute limits where relevant. Count setup, warmup,
   evaluation and cleanup in the total budget even if the metric excludes them.
3. Preserve existing work. Use a task-owned branch or isolated worktree when
   changes would conflict; record the starting state. Run the baseline before
   modifying the candidate. If the baseline cannot be reproduced, resolve the
   cause or record an inconclusive experiment rather than claiming improvement.
4. Change one coherent hypothesis per trial within the declared boundary. Run
   its focused correctness check and measurement; append the command, revision,
   outcome and evidence to [the trial log](assets/trials.tsv). Preserve failed
   and interrupted trials rather than reporting only the winning run.
5. Keep a candidate only when the agreed behavior and measurement criteria are
   met. Discard only task-owned changes through a reviewed diff or isolated
   branch. Do not reset a shared working tree or alter the evaluator/holdout to
   reward the current candidate. A justified evaluator correction starts a new
   comparison with the affected baseline and candidate rerun.
6. Stop at the budget, a verified result or a recorded blocking condition.
   Report the best verified candidate, consumed budget, rejected hypotheses and
   uncertainty. Further attempts need a concrete new reason within the task's
   authorization; an instruction to keep questioning is not an endless loop.

For code edits, apply [clean-code](../clean-code/SKILL.md). A log entry is
evidence provenance, not proof that the command executed or produced the result.
Do not provision a paid runtime merely because an experiment record has a cost
field.

This adapts the baseline/editable-boundary separation in
[Karpathy's experiment protocol](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/program.md).
The finite stopping rules and preservation of unrelated work are deliberate
adaptations; no unbounded agent loop or runtime setup is imported.
