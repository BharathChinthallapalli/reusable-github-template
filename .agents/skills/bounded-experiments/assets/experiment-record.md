# Experiment record

Status: Planned; no execution evidence recorded.

| Contract | Value agreed before trials |
| --- | --- |
| Experiment ID, owner and user outcome | |
| Hypothesis and reason it is plausible | |
| Baseline code/artifact and starting worktree state | |
| Allowed editable files/components | |
| Fixed evaluator, data/workload revision and holdout boundary | |
| Correctness invariants and verification command | |
| Metric, direction, tolerance and acceptance criterion | |
| Exact baseline/candidate command and working directory | |
| Runtime, dependency, hardware/provider and seed context | |
| Maximum trials and total elapsed time | |
| Applicable compute, token, cost and storage limits | |
| Per-attempt timeout, retry policy and budget enforcement | |
| Stop conditions and inconclusive conditions | |
| Task-owned rollback method and evidence location | |

Append one row per attempt to a copy of `trials.tsv`. Use explicit trial statuses:
completed, failed, timed out, interrupted or not run. Keep metric cells empty
when measurement is unavailable; do not substitute zero. `disposition` records
keep, discard or inconclusive after evaluating the evidence.

## Decision after stopping

| Result | Recorded evidence |
| --- | --- |
| Chosen candidate identity or no candidate | |
| Correctness check and metric evidence | |
| Comparison uncertainty and untested boundaries | |
| Attempts, total elapsed time and other budget actually used | |
| Stopping reason and state of task-owned changes | |
| Rejected hypotheses and any evidence-backed follow-up | |

A blank record or a best observed metric without its correctness evidence does
not establish improvement. Keep raw evidence associated with each trial's
revision so later code changes do not silently inherit an earlier result.
