# Data contract

Status: Draft; no dataset validation recorded.

| Contract | Project value |
| --- | --- |
| Dataset ID, owner, source and snapshot/hash | |
| Consumer task and observable acceptance | |
| Collection/source rights and permitted uses | |
| Stable record identity, uniqueness and duplicate policy | |
| Label source, procedure, revision and known uncertainty | |
| Transformation code/configuration and canonical output format | |
| Invalid/missing data behavior and rejected-record evidence | |
| Train/validation/test purpose and split construction | |
| Entity/time/duplicate boundary and leakage checks | |
| Preprocessing fit partition and application to other partitions | |
| Data retention, deletion and downstream refresh behavior | |
| Validation command, environment and evidence location | |

## Fields and relationships

| Field or relationship | Type/unit | Required? | Constraint and rationale | Invalid-value behavior | Check |
| --- | --- | --- | --- | --- | --- |

## Snapshot verification

| Evidence | Baseline | Candidate |
| --- | --- | --- |
| Exact data and transformation identities | | |
| Input / accepted / rejected / output counts | | |
| Relevant label, group and missing-value counts | | |
| Duplicate and cross-partition leakage findings | | |
| Schema, transformation and persistence check results | | |
| Known drift and downstream behavior impact | | |

Record whether counts cover the entire snapshot or a specified sample. Account
for filtering and expansion so output counts can be reconciled with inputs.
Do not invent labels for unavailable expected outcomes; report coverage instead.

Decision: Not assessed. Record accepted changes, blocking findings and remaining
uncertainty after the checks actually run.
