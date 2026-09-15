---
name: context-maintenance
description: Refresh repository instructions, project context or a work handoff from current code, commands and accepted decisions. Use when context is stale or work must resume; avoid inventing persistent user preferences or promoting one-off fixes into policy.
---

# Maintain reliable working context

Required: follow [official documentation and actual tool contracts](../../../docs/official-documentation.md)
before external technical claims, commands or implementation choices.

Identify the context consumer: the next implementation session, a maintainer,
a specialist subtask or a host reading instructions. Inspect the current files
and relevant callers before changing them. Use
[repo-discovery](../repo-discovery/SKILL.md) when the actual project boundary is
unclear; an example directory or tooling dependency does not define the app stack.

When consolidating guidance:

1. Capture the supporting file, command result or explicit user decision, its
   revision or date, and affected version, environment and scope. Label inference.
2. Find the canonical owner and classify each incoming claim as new, duplicate,
   changed, superseded or conflicting before adding another instruction.
3. Merge duplicates at the owner and update consumers to point there. Replace
   changed guidance with current evidence; retain useful historical rationale and
   a replacement pointer for superseded guidance. Preserve distinct facts and
   unresolved conflicts instead of choosing by recency alone.
4. Check affected links, commands and consumers. State a recheck trigger when a
   runtime, interface or external assumption could invalidate the guidance.

Inspect only context relevant to the requested work. An explicit user choice is
authoritative within its stated scope; an inferred preference is not a durable
rule. If evidence adds no durable information, leave permanent instructions alone.

Refresh the smallest source of truth. Record commands from manifests/CI and
contracts from code/tests; label proposed behavior and unverified environments.
Preserve the user's active objective, corrections, authorized scope, unfinished
work and evidence needed to resume. Use the
[context refresh record](assets/context-refresh.md) for a substantial handoff.

Separate durable guidance from temporary state. Stable interface constraints and
repeated, verified conventions can belong in project instructions. A failing run,
current branch SHA or experiment outcome belongs in its work record. Do not store
secrets, fabricate user preferences or turn a single review comment into a rule.

For a community workaround or recurring failure, confirm the affected version,
reproduction and resolution before updating guidance. Retain the minimal repro,
deduplicate existing advice, reconcile the accepted decision and update the
relevant runbook. Mark superseded workarounds with their replacement and evidence;
repeated forum claims alone do not establish a current fix.

Consult the [decision index](../../../docs/adr/README.md) for ADR status and
supersession. If two accepted decisions conflict, investigate scope and evidence;
the newer timestamp alone does not settle the conflict. Follow the
[change-dependency map](../../../docs/maintenance.md) for related files.

Keep root instructions short enough to act on. Link conditional procedures rather
than duplicating them across agents and skills. Check that links, path ownership
and documented commands still match the repository. A static configuration check
does not prove a host loaded the revised context; use
[AI diagnostics](../../../docs/ai-assistance.md) when that is the actual question.

Report what changed and why, with remaining contradictions or unverified facts.
Resume the active task after a context refresh instead of treating the handoff as
completion of the user's implementation request.

When several instructions repeat a procedure, trace their actual consumers before
extracting a shared skill. Consolidate only rules that must change together;
preserve host-specific contracts and update every caller. Keep a source and
revision for externally learned guidance. Recheck examples and commands after a
schema or interface change. A one-off workaround or generated preference is not
stable policy. Route reader-facing tutorials and guides to
[documentation-writing](../documentation-writing/SKILL.md).
