# Performance measurement record

Status: Not run. The record makes no performance claim until evidence is added.

| Comparison contract | Project value |
| --- | --- |
| User requirement or regression evidence | |
| Baseline and candidate code/configuration identities | |
| Behavior oracle and correctness command | |
| Workload/data revision, input sizes, concurrency and duration | |
| Runtime, dependencies, hardware/provider and resource limits | |
| Metric definition, units, direction and acceptance tolerance | |
| Timing includes / excludes | |
| Warmup, cache state and cold-start treatment | |
| Repetitions, sample-count requirements and uncertainty method | |
| Exact command, working directory and instrumentation | |
| Maximum attempts, wall time and applicable resource/cost budget | |
| Raw measurement/report location | |

## Measurement comparison

Choose statistics suitable for the actual workload. Do not populate unmeasured
percentiles, costs or sample counts from guesses.

| Measure and unit | Baseline | Candidate | Samples / variation | Evidence |
| --- | --- | --- | --- | --- |

## Interpretation

| Evidence | Recorded result |
| --- | --- |
| Profiling result and demonstrated bottleneck | |
| Correctness and failure-rate comparison | |
| Completeness, nonfinite/missing samples and exclusions | |
| Shifted memory, compute, background work, quality or cost | |
| Included setup, warmup, evaluation and total elapsed time | |
| Improvement, regression or inconclusive decision | |
| Applicable workload range and remaining uncertainty | |

Keep timeouts and failed requests visible. If the setup or workload changed,
explain comparability or rerun the affected baseline. Label cost estimates as
estimates and record their pricing assumptions separately from measured usage.
