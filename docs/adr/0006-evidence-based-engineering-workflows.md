# 0006: Add distinct engineering procedures with progressive context

Status: Accepted
Date: 2026-09-09

## Context

The user requested substantive reuse of asw101/gh-aw and microsoft/azure-skills,
including documentation writing and principal/solution architecture and solutions
engineering. Version 3.0 has broad engineering procedures but no dedicated reader
validation, solution proof, workload design packet, cross-system architecture
review, Azure phase guidance or agentic-workflow authoring procedure.

## Decision

Extend the existing shared skills with ten task-specific procedures and three
profiles with distinct outputs and tool boundaries. Keep the existing architect
name for compatibility and clarify its solution-design responsibility. A principal
architect reviews cross-system tradeoffs without editing or granting exceptions;
a solutions engineer implements and demonstrates a bounded solution; a documentation
writer edits reader-facing documentation and reports what was actually verified.
No mandatory chain or seniority-based authority is added.

Use small skill entrypoints with selectively loaded references and reusable task
records. Extend existing debug, security, performance, AI evaluation, data and tool
skills for Azure-specific evidence instead of adding competing general dispatchers.
Azure preparation, validation, delivery and resource discovery use the project's
actual toolchain, resource scope and authorization. They do not select Azure for
an unrelated project or install upstream MCP servers by default.

Agentic-workflow guidance records the authoring/compilation/run boundaries and
bounded output contract. Optional recipes remain outside active workflow folders
until a project selects its engine, credentials and authorized behavior. Existing
CI, hooks and design gates retain their contracts. This is an additive minor release.

## Alternatives and consequences

Copying upstream plugin bundles would duplicate local names, bring unnecessary
provider/runtime choices and inherit stale metadata or overly broad triggers.
Keeping every addition in root instructions would increase unrelated context.
Adding a role for every Azure service would duplicate existing responsibilities.
The selected profiles support distinct tasks; their procedures remain usable
when native profile invocation is unavailable.

This extends decision 0004's initial inventory; it does not impose a new maximum
or revise its portability rule. Existing ADD bindings still require reconciliation
for affected files. Source notes distinguish inspected entrypoints and excerpts
from a full implementation audit. Architecture books inform original criteria;
no book chapters, upstream skill payloads or vendor implementation are bundled.

## Validation and reconsideration

Check all links, metadata, catalog and explicit ADD coverage; exercise the new
procedures against concrete repository and synthetic delivery scenarios. Report
structural checks separately from independent behavioral walkthroughs and native
host execution. Revisit a split if tasks routinely need the same procedure or a
new profile cannot demonstrate a distinct output or permission boundary.
