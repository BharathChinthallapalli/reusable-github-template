---
name: "compliance-mapping"
description: "Map an AI project's applicable legal and governance obligations to evidence, controls and owners without claiming certification; use during intent and design review."
---

# compliance mapping

Follow [official-documentation rules](../../../docs/official-documentation.md).
Source: [official reference](https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/eng). Version/evidence: AI Act consolidated 2026-07-27; current official GDPR/BetrVG/NIS2 sources in reading log.

## Checklist

1. Identify each system's intended purpose, risk class, provider/deployer role, entity scope and applicable dates before selecting obligations.
2. Fetch current official provisions using the actual available web tool; record URL, section, version, date and read extent. Draft guidance is not law.
3. Fill applicability, reason and owner for AI Act, GDPR, BetrVG and NIS2. An unresolved assessment blocks spec rendering.
4. Record per-record retention and legal basis; never turn incident reporting clocks into retention periods.
5. Keep ISO clause mapping and the missing Annex I draft explicitly unverified under the user's exception; seek qualified review for consequential legal decisions.

## Tool contract

This skill grants **no tools or permissions**. Use native read/search and the
available documented web-fetch tool; discover actual host tool names rather than
inventing them. If a required source/tool is absent, report the specific missing
evidence. Never obtain shell access to circumvent a read-only agent profile.
An authorized shell-capable coordinator may inspect and run these project-local
commands from the repository root under the existing Guardian policy:

```text
python scripts/spec-check.py <change-id>
python scripts/governance-check.py posture compliance/posture.yaml
```

Replace bracketed arguments with the explicitly selected change/path; never pass
them literally. For searches use scoped rg/fd and jq when available, without
installing tools or searching user profiles. Existing test results and references
are evidence only for their recorded revision.

## Output

Use [the project artifact](../../../compliance/MATRIX.md) and report completed checklist
items, exact evidence, limitations and the next required decision. Do not mark
human acceptance, enforcement, deployment, compliance or performance as proven
when only structural checks were run.
