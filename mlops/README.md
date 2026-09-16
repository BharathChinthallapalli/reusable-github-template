# MLOps in the six-stage loop

Stage2 produces data cards, lineage, versioned splits and a reproducible training
design. Stage3 implements approved pipeline tasks. Stage4 requires quality/bias/
robustness evaluation before registry promotion. Stage5 binds artifact/model/data
versions to the release and rollback record. Stage6 monitors performance and
data/concept drift, retraining triggers and retirement.

A registry entry records immutable artifact digest, dataset/code/environment
versions, evaluator version, review and stage transitions. Promotion is never a
model self-assessment. No training job, registry or cloud credentials are created
by these templates. Google Rules ofML and Microsoft's classical MLOps maturity
model are source guidance, not evidence of the project's maturity.
