---
name: context-maintenance
description: Refresh repository instructions, project context or a work handoff from current code, commands and accepted decisions. Use when context is stale or work must resume; avoid inventing persistent user preferences or promoting one-off fixes into policy.
---

# Maintain reliable working context

Identify the context consumer: the next implementation session, a maintainer,
a specialist subtask or a host reading instructions. Inspect the current files
and relevant callers before changing them. Use
[repo-discovery](../repo-discovery/SKILL.md) when the actual project boundary is
unclear; an example directory or tooling dependency does not define the app stack.

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

Consult the [decision index](../../../docs/decisions/README.md) for ADR status and
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
