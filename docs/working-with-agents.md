# Work with the bundled capabilities

Describe the task, repository context and observable result. The default
instructions select relevant skills; you do not need to name every procedure.
Choose `engineer` for implementation when your client exposes the profile.
[The catalog](ai-catalog.md) is the complete list and [AI assistance](ai-assistance.md)
explains native host support.

The examples below are task requests, not claims that an application or model
has already been run. Replace file names, budgets and acceptance criteria with
project facts. Copy a skill asset into your project's work record when useful;
leave the reusable blank asset unchanged.

## Learn, plan and implement a feature

> Add CSV export to the existing JSON export flow. Preserve JSON callers and
> existing destination files, exclude access tokens, and support commas, quotes
> and newlines in values. Trace current callers first. Compare the smallest viable
> approaches, challenge compatibility and failure behavior, then implement and
> verify the agreed contract. Keep unrelated edits intact.

The [discovery](../.agents/skills/repo-discovery/SKILL.md),
[planning](../.agents/skills/implementation-planning/SKILL.md),
[clean-code](../.agents/skills/clean-code/SKILL.md) and
[test-design](../.agents/skills/test-design/SKILL.md) procedures produce a code
trace, a challenged plan, a focused implementation and independent assertions.
Use the [plan record](../.agents/skills/implementation-planning/assets/change-plan.md)
for a material change. If work is split, use
[orchestration](../.agents/skills/task-orchestration/SKILL.md) to assign one writer
per file area, an integration order and a finite stopping condition.

## Diagnose a failure without losing the first cause

> The export command reports upload failure. Logs first show that its output
> parent directory is missing. Reproduce on the recorded revision, trace which
> error occurred first, inspect the effective output path and working directory,
> and test one causal hypothesis at a time. Establish the intended directory
> behavior before changing it. Preserve the original failure if cleanup fails.

[Systematic debugging](../.agents/skills/systematic-debugging/SKILL.md) produces
a reproducible case, evidence for the cause, the smallest correction and a
regression check. Use [Actions debugging](../.agents/skills/github-actions-debug/SKILL.md)
when the failure belongs to a particular workflow run. Record a confirmed fix in
[context maintenance](../.agents/skills/context-maintenance/SKILL.md), linking the
repro and current runbook instead of accumulating stale instructions.

## Change retrieval or model behavior

> Compare the current retrieval configuration with a candidate using the same
> frozen cases and corpus. Include permission-denied, no-answer and stale-document
> cases. Separate retrieval failure, generation quality and provider errors.
> Freeze the rubric before trials, respect the agreed experiment budget and keep
> the baseline if required evidence is missing. Do not tune on held-out answers.

Use [RAG development](../.agents/skills/rag-development/SKILL.md),
[data contracts](../.agents/skills/data-contracts/SKILL.md),
[AI evaluation](../.agents/skills/ai-evaluation/SKILL.md) and
[bounded experiments](../.agents/skills/bounded-experiments/SKILL.md). Their assets
record provenance, access filtering, independent labels, effective model/prompt
configuration and finite trial decisions. For provider or MCP changes, add the
[tool integration](../.agents/skills/tool-integration/SKILL.md) contract.

The optional offline report gate can validate project-owned evidence:

```bash
python tools/check_evaluation.py path/to/report.json
```

Read [the schema and exit codes](evaluation-reports.md). The bundled passing and
incomplete examples contain invented data for exercising the checker. They are
not model evaluations. A parsed report cannot authenticate its claimed results.

## Verify the interface and deliver the artifact

> Verify the changed flow through its real consumer: keyboard and error states
> for a UI, help and exit behavior for a CLI, or authenticated responses for an
> API. Prepare the release from the reviewed revision. Inspect package contents,
> test installation or use in a clean consumer, and record the artifact identity,
> migration, smoke check and rollback. Complete publication when authorized.

[Interface validation](../.agents/skills/interface-validation/SKILL.md) chooses
checks appropriate to the actual interface.
[Release delivery](../.agents/skills/release-delivery/SKILL.md) supplies a release
record tying evidence to the artifact being delivered. The
[dependency maintenance](../.agents/skills/dependency-maintenance/SKILL.md) record
tracks verified upstream changes, consumer compatibility and rollback. Ordinary
CI cannot replace application-specific release evidence.

## Research and maintain useful context

> Investigate the reported workaround against current official documentation
> and the project's exact runtime. Distinguish reproduced failures, maintainer
> fixes and forum suggestions. Update the relevant decision, command or runbook
> only when evidence changes; preserve historical rationale and unresolved facts.

[Evidence research](../.agents/skills/evidence-research/SKILL.md) supplies a claim
ledger, while [context maintenance](../.agents/skills/context-maintenance/SKILL.md)
provides a current-context record. Use [security review](../.agents/skills/security-review/SKILL.md)
for an actual access or data-flow boundary and
[performance analysis](../.agents/skills/performance-analysis/SKILL.md) for a
measured bottleneck. These procedures require concrete evidence and a stopping
condition; a routine edit does not need every agent or asset.
