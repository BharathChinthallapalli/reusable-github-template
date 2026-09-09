---
name: "ai-evaluation"
description: "Design and assess behavioral evaluations for prompts, models, retrieval, agents and evaluators; use for AI quality comparisons, regressions and acceptance gates."
---

# Evaluate AI behavior

1. Identify the user task and changed layer. Read the project's actual runner,
   cases and [evaluation contract](../../../docs/ai-evaluation.md). Separate
   deterministic code/data checks from model behavior and provider availability.
2. Establish observable acceptance before running. Use independent expected
   outcomes or a justified rubric; record baseline and candidate code, data,
   prompt, effective provider/model and evaluator revisions. Keep holdout cases
   separate from tuning and record the case-selection rationale.
3. Copy [the evaluation plan](assets/evaluation-plan.md) when the project lacks
   an equivalent record. Select relevant cases, slices and failure boundaries;
   give each case a stable ID. A correctly labeled unanswerable case is different
   from an unlabeled case. Define the comparison budget and stopping condition.
4. Run the existing harness against comparable inputs and information budgets.
   Start with local fixtures where useful, then execute the external evaluation
   already authorized by the task. Record actual commands, outputs and effective
   configuration. Do not change labels or thresholds to rescue a candidate.
5. Classify each result using the evaluation contract. Keep execution errors,
   missing labels and unrun cases separate from quality scores. Report coverage,
   relevant slice counts, failure examples and uncertainty for repeated runs.
   Check completeness and finite measurements before computing aggregates.
6. Produce accept, reject or inconclusive against the frozen criteria. For the
   bundled offline evidence format, follow
   [evaluation reports](../../../docs/evaluation-reports.md). Its checker
   validates submitted evidence; it does not run a model or prove label quality.
   Bind the decision to the evaluated artifacts and list remaining limitations.

For that report format, run `python3 tools/check_evaluation.py REPORT.json` from
the repository root. Exit 0 means the declared gate passed; exit 1 means failed
or inconclusive evidence; exit 2 means an invalid report. Inspect the JSON
result and preserve the report rather than treating every nonzero exit as a
model-quality failure.

For repeated candidate optimization, use
[bounded-experiments](../bounded-experiments/SKILL.md). For ingestion/schema or
retrieval failures, route to [data-contracts](../data-contracts/SKILL.md) or
[rag-development](../rag-development/SKILL.md). Ordinary repository checks are
not evidence of AI quality, and evaluation completion does not itself authorize
publication or deployment.

The procedure adapts Made With ML's
[behavioral tests](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/tests/model/test_behavioral.py)
and [slice evaluation](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/madewithml/evaluate.py),
and the error-state lessons in
[the Hub evaluation review](../../../docs/research/repository-inventory/ai-repositories-notes.md).
These sources motivate the procedure; they are not required dependencies.
