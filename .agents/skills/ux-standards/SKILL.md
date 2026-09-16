---
name: "ux-standards"
description: "Plan and review accessible, localized project interfaces and AI interaction notices; use for web-app design and UX acceptance criteria."
---

# ux standards

Follow [official-documentation rules](../../../docs/official-documentation.md).
Source: [official reference](https://www.w3.org/TR/WCAG22/). Version/evidence: WCAG 2.2 Recommendation dated 2024-12-12; relevant current criteria must be fetched and checked.

## Checklist

1. Record users, critical journeys, errors, keyboard/focus behavior, responsive layout and de/en localization requirements.
2. Fetch the applicable WCAG 2.2 criteria; evaluate the requested AA target without claiming conformance from one automated scan.
3. Map critical journeys to observable tests, including manual assistive-technology checks where needed.
4. For AI interaction, assess applicable notices, uncertainty, escalation and human oversight with the compliance owner.
5. Use existing test tools only; author a project-specific verification plan when no application or browser runtime is present.

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

Use [the project artifact](../../../specs/archetypes/A-web-app.md) and report completed checklist
items, exact evidence, limitations and the next required decision. Do not mark
human acceptance, enforcement, deployment, compliance or performance as proven
when only structural checks were run.
