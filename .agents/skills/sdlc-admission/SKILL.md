---
name: "sdlc-admission"
description: "Validate intent, Kiro-style specifications and task waves before proposing an AI-native SDLC handoff; use for readiness, spec rendering and missing-gate diagnosis."
---

# sdlc admission

Follow [official-documentation rules](../../../docs/official-documentation.md).
Source: [official reference](https://academy.claude.com/courses/ai-native-sdlc-playbook/plan-mode). Version/evidence: Anthropic playbook and Kiro specs, fetched 2026-09-16.

## Checklist

1. Read the exact intent, requirements, design and tasks for the change; preserve Guardian and current human decisions.
2. Run the local spec and DoR checks only through an already authorized shell-capable host; read-only agents return the command plan instead.
3. Check semantic acceptance criteria and requirement-to-test meaning after structural validation; a file reference is not coverage.
4. Require authenticated acceptance bound to the exact revision before a dispatch handoff. Neither accepted metadata nor an exit-zero result is authority.
5. Escalate unknown requirements, unresolved compliance, invalid waves or source-provenance gaps; never synthesize an approval.

## Tool contract

This skill grants **no tools or permissions**. Use native read/search and the
available documented web-fetch tool; discover actual host tool names rather than
inventing them. If a required source/tool is absent, report the specific missing
evidence. Never obtain shell access to circumvent a read-only agent profile.
An authorized shell-capable coordinator may inspect and run these project-local
commands from the repository root under the existing Guardian policy:

```text
python scripts/spec-check.py <change-id>
python scripts/dor-check.py <change-id>
```

Replace bracketed arguments with the explicitly selected change/path; never pass
them literally. For searches use scoped rg/fd and jq when available, without
installing tools or searching user profiles. Existing test results and references
are evidence only for their recorded revision.

## Output

Use [the project artifact](../../../docs/SDLC.md) and report completed checklist
items, exact evidence, limitations and the next required decision. Do not mark
human acceptance, enforcement, deployment, compliance or performance as proven
when only structural checks were run.
