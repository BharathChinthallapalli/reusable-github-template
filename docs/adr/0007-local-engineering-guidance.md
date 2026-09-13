# 0007: Route tasks through local, maintained engineering guidance

Status: Accepted
Date: 2026-09-13

## Context

The user requested research and implementation of task routing, engineering
judgment, a problem-oriented tool catalog and context consolidation inspired by
`kunchenguid/kun`. The existing 34 skills and 13 profiles already implement most
of the individual procedures. The [source review](../research/kun-adoption.md)
identifies navigation and maintenance improvements without adding another agent.

## Decision

Keep the task-shape table in `docs/engineering-workflows.md` as the single routing
reference for ideation, features, bugs, refactors and explanations. AGENTS.md and
the existing engineer profile link to it. Select the route and relevant skills
for the actual request; routine edits still proceed directly.

Use `docs/engineering-principles.md` as a concise explanation and index of
accepted decisions and current procedures. It does not create a higher policy
authority or supersede ADRs. Read it when a tradeoff needs context. Resolve a
material contradiction through the decision process before changing a contract.

Keep a separate repository tool reference linked from the generated AI catalog.
Describe actual prerequisites, effects, outputs and limits, and preserve the
existing commands. Update it alongside changed CLI contracts. Project tools are
added only when their manifests and use establish them.

Maintain guidance by comparing each candidate claim with existing evidence and
its canonical owner. Deduplicate, update or mark superseded as appropriate; keep
temporary state in its task record. Record scope, revision and a recheck trigger
for contingent facts. Do not infer permanent preferences from one failed run.

## Alternatives and consequences

A new catchall skill would compete with existing routing. Copying all upstream
documents would import an unrelated persona, tool preferences and considerable
context. Fetching mutable remote instructions during each task would make
template behavior depend on network access and unreviewed upstream changes.

Local versioned references preserve repeatable adoption and selective loading.
The tradeoff is deliberate maintenance by template and project owners. Existing
ADRs 0004, 0005 and 0006 remain accepted; counts, permissions, initializer inputs,
host integrations and runtime checks keep their current contracts. Version 3.2
is an additive guidance release. No scheduled updater or provider is enabled.

## Validation and reconsideration

Check links, metadata, generated catalog freshness and ADD bindings. Exercise
realistic requests to verify route selection, tool prerequisites and evidence
consolidation without inventing user preferences or external authorization.
Reconsider a new dispatcher or executable catalog only when the current guidance
causes demonstrated misrouting or command drift that warrants the added machinery.
