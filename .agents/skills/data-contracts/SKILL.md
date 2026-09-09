---
name: "data-contracts"
description: "Define and verify dataset schema, identity, transformations, labels and train/evaluation partitions; use for ingestion, dataset changes, leakage and data-quality failures."
---

# Define and verify data contracts

1. Identify the producer, consumer and decision the data supports. Inspect the
   actual loading/transformation code and representative approved samples. Record
   the dataset snapshot or hash, schema, stable identity and labeling provenance
   in [the data contract](assets/data-contract.md).
2. Derive constraints from consumer behavior: required types and fields, missing
   values, allowed labels/units, uniqueness and relationships. Specify rejection,
   quarantine or tolerated-invalid behavior explicitly. Avoid silently dropping
   invalid records and reporting the reduced dataset as complete.
3. Trace transformations and partition construction. Fit learned preprocessing
   only on the intended training partition; check the applicable entity, time or
   duplicate boundary for leakage. Stable record IDs alone do not prove that
   near-duplicates or the same subject cannot cross a split.
4. Add focused checks using the project's existing tooling at the changed seam.
   Exercise a valid sample and meaningful malformed, missing, duplicate or drift
   cases. Reconcile input, accepted, rejected and output counts. Check canonical
   saved/reloaded artifacts when persistence is part of the changed contract.
5. Compare the old and new snapshots on relevant distributions, label counts and
   consumer behavior. Separate intended data corrections from regressions. Use
   [ai-evaluation](../ai-evaluation/SKILL.md) when model behavior changes and
   [rag-development](../rag-development/SKILL.md) for retrieval/access evidence.
6. Produce the completed contract, data-check results, rejected-record counts and
   downstream impact. Bind evidence to the code and data actually checked. State
   limitations when only a sample was accessible. Keep sensitive records in the
   project's approved evidence location.

Read [clean-code](../clean-code/SKILL.md) before code changes. The project may
use tables, documents, events or model examples; this skill does not prescribe a
storage engine, dataframe library or folder layout. A code repository's license
does not establish rights to external datasets or model weights.

The procedure adapts Made With ML's
[dataset checks](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/tests/data/test_dataset.py)
and minbpe's
[persistence and boundary tests](https://github.com/karpathy/minbpe/blob/1acefe89412b20245db5a22d2a02001e547dc602/tests/test_tokenizer.py).

For Azure/Foundry exports or trace-derived evaluation datasets, read
[the Azure procedure](references/azure.md) before selecting tools or evidence.
