# Evaluation plan

Status: Not run. Complete before evaluation; a blank field is unknown evidence.
Use the project's established format if it records the same decisions.

| Field | Project value |
| --- | --- |
| User task and decision owner | |
| Observable acceptance, metric direction and tolerances | |
| Baseline and candidate code/artifact identities | |
| Effective inference, embedding and judge providers/models | |
| Prompt, tool, retrieval and evaluator configuration revisions | |
| Case set ID/revision and selection rationale | |
| Label/rubric source, independence and holdout boundary | |
| Data source, usage rights and approved evidence location | |
| Relevant slices and minimum evidence needed for a conclusion | |
| Command, runtime/dependency environment and seed where applicable | |
| Repetitions and treatment of uncertainty | |
| Maximum attempts, wall time, tokens/cost and timeout/retry limits | |
| Conditions for stopping and declaring inconclusive | |

## Case design

Add one row per case or link the versioned case file. Select boundaries relevant
to the task, such as a grounded answer, no answer, permission denial, malformed
input, tool side effect or provider failure. Expected outcome comes from the
contract, not from the candidate's response.

| Case ID | Slice | Input/fixture reference | Expected outcome or label status | Observable assertion | Required? |
| --- | --- | --- | --- | --- | --- |

## Result handoff

| Evidence | Recorded value |
| --- | --- |
| Exact completed run/report identities and timestamps | |
| Commands and effective configuration actually used | |
| Case counts by outcome and relevant slice | |
| Concrete failures, coverage gaps and budget consumed | |
| Baseline/candidate comparison and uncertainty | |
| Accept, reject or inconclusive, with rationale | |
| Evaluated artifact identities and remaining limits | |

Use the result states and machine-readable format documented by the repository;
this planning worksheet is not itself a passing evaluation report. Keep sensitive
raw inputs and outputs in the project's approved evidence location.
