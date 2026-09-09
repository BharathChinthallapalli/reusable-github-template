# Azure trace-to-dataset lineage

For an Azure/Foundry dataset, record source scope, environment, agent/deployment
version, extraction query/time window, sampling, schema and access limitations.
Keep raw traces in their authorized storage boundary. Select only fields required
for the evaluation, redact or replace personal/secret data, and preserve a safe
provenance pointer rather than copying complete production conversations.

Treat harvested failures as candidates for review. Establish expected behavior
from an independent source; a model's previous answer is not ground truth.
Deduplicate related traces and prevent near-duplicate conversations, documents or
users from crossing partitions where that would leak evaluation information.
Separate training/optimization/development and held-out evaluation. Record changes
to case selection and evaluator labels; failure-only sampling cannot estimate
overall production success rates without a representative comparison sample.

Version the dataset content, transformation and schema. Keep stable dataset
identity separate from version and physical local/remote locations. Record hashes,
case counts, split lineage, source reference, reviewer decisions and retention.
For Foundry, verify registered dataset/suite versions against the actual exposed
API; preserve returned URIs and identifiers. Do not assume arbitrary metadata tags
are supported by a particular tool. Local curation does not automatically require
uploading data or replacing a remote suite.

When refreshing a dataset, preserve reproducibility of previous evaluation runs.
Report what changed, which comparisons become invalid, and what was not collected.
The same procedure applies to service data exports used for testing: a successful
upload or schema check does not establish accuracy, consent or representativeness.

Source: [Foundry evaluation dataset lifecycle](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/microsoft-foundry/foundry-agent/eval-datasets/eval-datasets.md).
