---
name: operational-readiness
description: Assess and prepare a workload's operational handoff using evidence for setup, ownership, observability, failure recovery, and support. Use before a production transition or when taking over a service; a passing build or prototype demo alone is insufficient.
---

# Establish what can actually be operated

Identify the exact workload, revision, environment, transition, and receiving
owner. Read the project's operational requirements, relevant ADRs, deployment
configuration, and existing runbooks. Do not infer a live service or configured
access from repository files alone.

Read [readiness evidence](references/readiness-evidence.md) and adapt the
[readiness record](assets/readiness-record.md). Select checks relevant to the
workload's consequences. Distinguish documented intent, static validation, an
executed check, and an observed runtime result. Report blocked, failed, or unrun
checks without converting them to a pass.

Prepare missing setup instructions, useful signals, support ownership, and
recovery steps within the task's authority. Run meaningful authorized checks on
the intended environment; avoid deploying, triggering outages, or changing access
solely to complete a checklist. A dry run or mock has a narrower claim than a
live exercise. Recheck affected evidence after a material configuration change.

Use [release delivery](../release-delivery/SKILL.md) for an authorized release and
[systematic debugging](../systematic-debugging/SKILL.md) for a failed check. Carry
recoverable failures into [runbooks](../../../docs/runbooks/README.md). Return
demonstrated readiness, material gaps, next owners, and a bounded next action.
The record is evidence for the existing decision process, not a new approval or
production certification.
