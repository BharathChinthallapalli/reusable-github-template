# Offline evaluation evidence gate

`tools/check_evaluation.py` checks a local evidence report and applies its
declared acceptance criteria. It uses Python's standard library, reads one JSON
file, prints a JSON summary, and leaves the input unchanged. It does not call a
model, fetch evidence links, execute report content, verify provenance or judge
whether submitted labels and outcomes are truthful. Produce the evidence with
your application's real evaluation runner and review it using the
[evaluation contract](ai-evaluation.md).

```bash
python3 tools/check_evaluation.py path/to/evaluation-report.json
python3 tools/check_evaluation.py --help
```

The output preserves task, acceptance and provenance identifiers, reports each
run's outcome counts, and reports comparable cases, regressions and required
case results separately. `quality_passes` contains a numerator and denominator;
the denominator includes only `pass` and `quality_failure` outcomes. A zero
denominator conveys no measured quality. Total case counts and incomplete
outcome counts remain visible, so infrastructure problems cannot inflate a
reported quality denominator or disappear from the gate.

| Status | Exit code | Meaning |
| --- | --- | --- |
| `passed` | 0 | Every case is comparable, every required candidate case passes, and regressions are within the declared maximum |
| `failed` | 1 | A required candidate case has a quality failure, or observed regressions exceed the declared maximum |
| `inconclusive` | 1 | No decisive quality rejection exists, but at least one baseline or candidate outcome is incomplete |
| `invalid` | 2 | The file cannot be read or does not satisfy the versioned contract |

A decisive failure takes precedence over incomplete evidence; both appear in
the summary's reasons and counts. Failures and incomplete evaluations must
propagate to the calling workflow. Preserve the input report and summary;
do not replace the gate's exit code with a later successful cleanup command.
Use the application's evaluation artifact in application CI. This template's
CI tests the report checker with synthetic inputs; it does not certify a model.

## Version 1 input contract

All listed fields are required unless marked optional. Unknown fields,
duplicate JSON object keys, duplicate case IDs, unsupported versions and
incorrect types are invalid. Strings must contain non-whitespace text.
Do not place credentials or sensitive raw evidence in a committed report.

| Object | Fields |
| --- | --- |
| Report | `version`: integer `1`; `task`; `acceptance`; `baseline`; `candidate` |
| `task` | `id`: user task identifier; `case_set_id`: frozen case-set revision or content identifier |
| `acceptance` | `required_cases`: nonempty array of unique case IDs; `max_regressions`: explicitly declared nonnegative integer |
| Each run (`baseline`, `candidate`) | `provenance`; `cases`: nonempty array of case records |
| `provenance` | Nonempty identifiers for `code`, `config`, `data`, `model`, `evaluator`, `environment` |
| Each case | `id`; `expected`; `outcome`; `evidence`: observation reference or reason; optional `measurements` |
| Labeled `expected` | `status`: `labeled`; `label`: the expected result or a versioned rubric reference |
| Unlabeled `expected` | `status`: `missing_label`; no `label` field |
| `measurements` | Object of nonempty metric names and finite numeric values; include units in names, such as `latency_ms` |

Use actual commits, content hashes or immutable artifact identities for
provenance. Where a dimension genuinely does not apply, use an explicit
explanation such as `not-applicable: deterministic non-model evaluator`.
Identifiers are assertions supplied by the report producer, not automatically
verified references. Preserve the full effective configuration and provenance
elsewhere and point to it; this compact format does not replace those artifacts.
Review whether any changed data, evaluator or environment still supports a
fair comparison. Agreement of IDs alone cannot establish that fact.

Baseline and candidate must contain exactly the same unique case IDs and the
same expected-label record for each ID. Order is irrelevant. Every required ID
must occur in that set. The checker has no universal score or minimum pass-rate
threshold: the task owner declares required behavior and the allowed count of
regressions before the candidate run. A regression is a baseline `pass` becoming
a candidate `quality_failure`. A nonrequired case that fails in both runs is an
existing failure: it remains visible in the counts but consumes no regression
budget. Newly regressed nonrequired cases must stay within the declared budget.
Required candidate failures always fail the gate, regardless of baseline outcome
or regression budget. Mark a case required when an existing failure must block
acceptance.

| Outcome value | Meaning and completeness |
| --- | --- |
| `pass` | Labeled behavior was checked and met; quality evidence is complete |
| `quality_failure` | Labeled behavior was checked and missed; quality evidence is complete |
| `execution_error` | Execution or evaluation failed; incomplete, separate from quality |
| `missing_label` | The expected result is unavailable; incomplete |
| `not_run` | No execution evidence; incomplete |
| `skipped` | Deliberately omitted with a reason in `evidence`; incomplete |

`pass` and `quality_failure` require a labeled expected result.
`missing_label` requires an unlabeled expected record. Other incomplete outcomes
may have either label status. A known unanswerable question is labeled: for
example, the expected result can be `decline unsupported answer`. It can pass
when that behavior is observed. It must not be confused with an absent label.
Any incomplete case, including a nonrequired case or baseline case, prevents a
passing comparison. Booleans, strings, nulls, NaN and infinities are invalid
measurements. Finite measurements are preserved in the input; version 1 does
not aggregate them or apply numeric thresholds.

## Synthetic examples and verification

[passing.json](../examples/evaluation/passing.json) and
[incomplete.json](../examples/evaluation/incomplete.json) are **handwritten,
synthetic demonstrations**. No real model or provider was run, and their
identifiers and latency are not experimental findings. Replace them with real
runner-produced evidence for an application decision.

```bash
python3 tools/check_evaluation.py examples/evaluation/passing.json
python3 tools/check_evaluation.py examples/evaluation/incomplete.json
python3 -m unittest discover -s tests -p test_evaluation.py -v
```

The first command exits 0. The second deliberately exits 1 with `inconclusive`
because a required candidate case simulates an execution error. Tests exercise
the public CLI using valid, malformed, mismatched, incomplete and failed
reports, including comparison budgets, known unanswerable labels, duplicate
keys, nonfinite values, unavailable files and preservation of input bytes.
