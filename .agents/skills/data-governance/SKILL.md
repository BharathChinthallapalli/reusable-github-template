---
name: "data-governance"
description: "Prepare dataset provenance, lineage, access, retention and split evidence for AI/ML design and evaluation without collecting sensitive source data."
---

# data governance

Follow [official-documentation rules](../../../docs/official-documentation.md).
Source: [official reference](https://sites.research.google/datacardsplaybook/). Version/evidence: Data Cards introduction, fetched 2026-09-16; linked deep dives must be fetched when used.

## Checklist

1. Identify owner, lawful collection/use, intended purpose, license, consent scope, classification and permitted locations.
2. Create a card per immutable dataset version with provenance, transforms, split policy and contamination controls.
3. Design access, minimisation, retention/deletion propagation and telemetry redaction at actual data-flow boundaries.
4. Evaluate representativeness, missingness and bias against the intended population; avoid collecting unnecessary personal data.
5. Use approved references and hashes; never inspect mailbox caches, browser stores, credentials or private datasets to complete a card.

## Tool contract

This skill grants **no tools or permissions**. Use native read/search and the
available documented web-fetch tool; discover actual host tool names rather than
inventing them. If a required source/tool is absent, report the specific missing
evidence. Never obtain shell access to circumvent a read-only agent profile.
An authorized shell-capable coordinator may inspect and run these project-local
commands from the repository root under the existing Guardian policy:

```text
python scripts/spec-check.py <change-id>
```

Replace bracketed arguments with the explicitly selected change/path; never pass
them literally. For searches use scoped rg/fd and jq when available, without
installing tools or searching user profiles. Existing test results and references
are evidence only for their recorded revision.

## Output

Use [the project artifact](../../../mlops/data-card.md) and report completed checklist
items, exact evidence, limitations and the next required decision. Do not mark
human acceptance, enforcement, deployment, compliance or performance as proven
when only structural checks were run.
