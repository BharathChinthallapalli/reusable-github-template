---
name: "performance-analysis"
description: "Diagnose and verify latency, throughput, memory, token or cost improvements using a reproducible workload and valid measurements; use for bottlenecks and performance regressions."
---

# Measure and improve performance

1. Establish the user-visible requirement or observed regression. Trace the
   relevant request/job and inspect existing telemetry or benchmark commands.
   Identify what must remain behaviorally correct; do not optimize an invented
   load or impose a universal latency target.
2. Record the baseline, workload, environment and metric semantics in
   [the measurement record](assets/measurement-record.md). State units, included
   and excluded work, warm/cold state, concurrency and relevant input sizes.
   Define the acceptance tolerance and total measurement budget before running.
3. Reproduce the baseline and profile enough to locate the bottleneck. Separate
   local processing, queueing, external latency and retries when the system uses
   them. Confirm sample completeness and finite values; a parser that drops slow
   failures cannot substantiate a speed improvement.
4. Make a focused change using [clean-code](../clean-code/SKILL.md). For repeated
   trials, use [bounded-experiments](../bounded-experiments/SKILL.md). Preserve a
   meaningful behavior oracle while measuring performance; independent reference
   checks are useful where the domain supports them.
5. Compare baseline and candidate under comparable workload and resource limits.
   Use repetitions and distributions/percentiles when they answer the task;
   record counts, variability and failures. Account for shifted cost, memory,
   quality or background work instead of reporting only the improved metric.
6. Report measured improvement, regression or inconclusive evidence with exact
   code/configuration identities, commands, raw-evidence location and limits of
   generalization. Stop when the required behavior and measurement are verified
   or the experiment budget is exhausted.

A billing estimate is distinct from measured spend, and an alert is distinct
from an enforced budget. Use [operations](../../../docs/operations.md) for
operational limits and [ai-evaluation](../ai-evaluation/SKILL.md) when an AI
optimization can change answer or tool quality. No load infrastructure or paid
benchmark is provisioned merely because this skill is selected.

This adapts [nanochat's measurement-boundary documentation](https://github.com/karpathy/nanochat/blob/92d63d4e8bb4df75c3b71618f31ddde2378b2bcd/dev/LEADERBOARD.md)
and [micrograd's independent reference checks](https://github.com/karpathy/micrograd/blob/7bc720e951fe422b8f8814aa5aa1b64121d26b4c/test/test_engine.py).
See [the llm.c review](../../../docs/research/repository-inventory/karpathy-notes.md)
for why complete measurements and machine-detectable failures matter.

For Azure spending, resource utilization or model-service costs, read
[the Azure procedure](references/azure.md) before selecting tools or evidence.
