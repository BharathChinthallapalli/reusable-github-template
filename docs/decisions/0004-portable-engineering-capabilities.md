# Portable engineering capabilities

Status: Accepted
Date: 2026-09-09

## Context

Version 1.3 translated much of the repository research into Git checks and
passive guidance. The requested reusable template also needs actionable
planning, research, engineering, AI evaluation, maintenance and delivery
procedures. The [capability map](../research/capability-expansion.md) accounts
for the distinct substantiated families and preserves research coverage limits.

## Decision

Bundle 21 task-focused skills with reusable assets and 10 specialist profiles.
Use `.agents/skills` as one canonical source supported by current Copilot and
Codex discovery. Root instructions route relevant work there. Claude imports
AGENTS.md through a thin CLAUDE.md file; this does not provide native Claude
skill or agent menus. See [host support and sources](../ai-assistance.md).

Keep profiles eligible by default, inherit host models and permissions, and
select procedures by task. Coordinate independent work with explicit scope,
file ownership, integration evidence and a finite budget. Combine overlapping
planning and documentation roles with architect/researcher/engineer procedures
instead of adding duplicate agents. Do not launch a mandatory chain per edit.

Generate a catalog from validated metadata and check freshness in CI. Supply a
stdlib offline evaluation report gate with project-owned acceptance criteria,
provenance and nonpassing incomplete evidence. Its synthetic examples exercise
the contract; there is no model runner, paid call or claimed benchmark. Prepare
Copilot's validation prerequisites using its documented setup job.

## Alternatives and consequences

Keeping broad capabilities as future optional suggestions would repeat the
scope gap. Copying source projects' frameworks, datasets and providers would
impose unrelated application choices and maintenance. Bundled reusable
procedures make that knowledge actionable while execution uses project facts.

Duplicating all skills under several host directories would risk drift and
ambiguous names. Shared procedures improve portability, but each host's native
agent format, permissions and discovery must be verified separately. A larger
catalog also needs concise descriptions and selective reference loading.

The skill path move requires a major version. Existing consumers must migrate
custom changes deliberately; see [maintenance](../maintenance.md). Decisions
0002 and 0003 remain accepted for metadata validation and Git checks. This
addition does not imply host invocation, application quality or deployment
readiness from static validation alone.
