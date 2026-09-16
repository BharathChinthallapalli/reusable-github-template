---
name: "cost-modelling"
description: "Build an assumption-led cloud and AI unit-cost model with verified current rates, measured workload inputs and explicit uncertainty."
---

# cost modelling

Follow [official-documentation rules](../../../docs/official-documentation.md).
Source: [official reference](https://azure.microsoft.com/en-us/pricing/calculator/). Version/evidence: Calculator landing page fetched 2026-09-16; no unit rates or contract prices verified.

## Checklist

1. Specify currency, region, purchase channel, model/deployment, traffic, tokens, storage, indexing, networking and operational overhead.
2. Fetch current official prices for the actual workload; distinguish list rates from contracted cost and billing units.
3. Model baseline, peak, retries/failures, evaluations and fallback; present sensitivity to uncertain assumptions.
4. Separate alert budgets from enforced spending/step ceilings. Record cost per successful task only from a complete comparable event window.
5. Do not query billing, Graph or Azure without authorized scope and Guardian approval; missing prices remain unverified inputs.

## Tool contract

This skill grants **no tools or permissions**. Use native read/search and the
available documented web-fetch tool; discover actual host tool names rather than
inventing them. If a required source/tool is absent, report the specific missing
evidence. Never obtain shell access to circumvent a read-only agent profile.
An authorized shell-capable coordinator may inspect and run these project-local
commands from the repository root under the existing Guardian policy:

```text
python scripts/metrics.py <project-relative-events.json>
```

Replace bracketed arguments with the explicitly selected change/path; never pass
them literally. For searches use scoped rg/fd and jq when available, without
installing tools or searching user profiles. Existing test results and references
are evidence only for their recorded revision.

## Output

Use [the project artifact](../../../docs/metrics.md) and report completed checklist
items, exact evidence, limitations and the next required decision. Do not mark
human acceptance, enforcement, deployment, compliance or performance as proven
when only structural checks were run.
