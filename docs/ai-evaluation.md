# Evaluate AI changes

Use this optional worksheet when a change affects a model, prompt, retrieval,
agent tool behavior, training data or evaluation logic. Link the completed
record from the change or decision. Ordinary repository checks do not establish
AI quality. This template supplies guidance; it has no model runner or sample
evaluation result. Record actual commands in [project context](project.md).

## Agree on the comparison before running

| Record | Required project evidence |
| --- | --- |
| Outcome and acceptance | User task, observable success and failure, relevant permissions, tolerances and owner of the decision |
| Baseline and candidate | Frozen baseline; candidate change; code commits, effective model/provider revisions, prompt/configuration versions and dependency environment |
| Cases and provenance | Stable case IDs, dataset/corpus revision or content hashes, source and labeling method, usage rights, split and case-selection rationale |
| Independence | Hold-out cases kept separate from tuning; independent expected outcomes or rubric; evaluator/judge version and configuration |
| Boundaries | Where inputs, retrieved content, embeddings, memory, outputs and telemetry go; allowed recipients, retention and access controls |
| Method | Exact command, environment, seed where applicable, planned repetitions, assertions/metrics, slices and sample counts |
| Budget and stopping | Maximum trials, wall time, tokens and cost as relevant; timeout/retry limits; conditions for stopping or declaring inconclusive |
| Evidence location | Report/artifact identity, protected storage for sensitive evidence, reviewed commit and responsible maintainer |

Use synthetic or approved data. A software repository's license does not prove
rights to its external datasets or model weights. Record effective runtime
settings, including separate embedding and judge providers; a model label in a
report is insufficient. Keep credentials and sensitive raw content out of
committed reports. Use [the threat model](threat-model.md) for access boundaries.

Freeze acceptance criteria and comparison inputs before candidate evaluation.
Do not change labels or tune on held-out failures solely to make the candidate
pass. If a case or label is wrong, correct it with evidence, version the change
and repeat the affected baseline and candidate checks within an agreed budget.

## Report what happened

For each case, record its ID, expected outcome or label status, observed result,
supporting evidence, outcome below, and any applicable score, latency and cost.
These are reporting meanings, not a required file format.

| Outcome | Meaning |
| --- | --- |
| Not run | No execution evidence; no quality conclusion |
| Skipped | Deliberately omitted, with reason and effect on coverage |
| Missing label | An expected outcome is unavailable; do not invent one |
| Execution error | Setup, provider, timeout, parsing or evaluator failure; retain the error and separate it from quality |
| Quality failure | Execution completed, but the result missed an agreed behavioral requirement |
| Pass | Execution completed and the applicable requirement was checked and met |

A labeled unanswerable question can correctly expect no answer; it is different
from a question whose answer has not been labeled. Include grounded-answer,
retrieval, refusal, permission or tool-side-effect cases when they matter to the
task. Verify actual effects and evidence rather than trusting a fluent answer.

Compare baseline and candidate on the same cases and information budget.
Report per-case failures, relevant slices, counts and metric denominators.
Do not turn missing labels or infrastructure errors into fabricated quality
scores or silently discard them; report coverage and availability separately.
For stochastic results, state repetitions and uncertainty. Record budget used,
early stopping and untested cases alongside any aggregate score.

## Decide and preserve the result

Choose accept, reject or inconclusive against the agreed criteria. An incomplete
required evaluation is not a passing gate. When a project automates a gate, its
command must propagate failures with a nonzero exit status and preserve a report;
later successful cleanup or upload commands must not mask that failure.

Tie the decision to the exact evaluated code, configuration, data and artifact.
Any later deployment should consume that artifact and use the project's smoke
check and rollback plan in [operations](operations.md). Evaluation alone does
not authorize deployment.

Stop review when acceptance behavior is verified, blocking findings are resolved
and remaining limits are recorded. Repeat only for new evidence, a changed
boundary or a failed acceptance case; stop an experiment at its budget and
report an inconclusive result when needed.

## Source lessons

This original guidance draws on Made With ML's
[data contracts](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/tests/data/test_dataset.py),
[behavioral tests](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/tests/model/test_behavioral.py)
and [slice evaluation](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/madewithml/evaluate.py),
plus AI Engineering Hub's
[question/answer/context cases](https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/eval-and-observability/data/test.csv)
and [artifact manifest](https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/kitops-mcp/ml-project/Kitfile).
These are inspected educational examples, not required dependencies or evidence
that their current deployments or benchmarks were reproduced.
