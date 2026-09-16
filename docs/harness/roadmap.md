# Harness roadmap

Planning snapshot: 2026-09-16. Baseline and current contracts:
[specification](spec.md). Sequence expresses dependency and priority, not dates,
approved budgets or permission to execute. The harness maintainer selects the
next bounded task; execution details belong in its change plan and PR.

## Existing foundation

Repository setup/checks, reusable skills, task assets, ADRs, ADD bindings and a
staged Guardian implementation exist. Their individual deployment and acceptance
limits remain in the linked contracts. The eight foundation pages are supplied
by this documentation change; merging them does not complete the work below.

## Proposed increments

| Order / goals | Work and dependency | Exit evidence | Status / accountable role |
| --- | --- | --- | --- |
| 1 / G1, G3, G4 | Establish representative onboarding, repair and feature tasks; measure context load, false denials and hook latency on the current revision. | Reproducible baseline with host/model versions, task conditions, pass/fail outcomes and unmeasured fields. | Proposed; harness maintainer. |
| 2 / G2, G4 | Resolve Guardian deployment and usability gaps using that baseline; preserve hard denials and independent controls. | Inert supported-operation tests and actual installed-surface acceptance, including failure/timeout behavior and a usable ordinary development path. | Blocked for production on protected issuer/identity integration and target-host evidence; maintainer with endpoint/security owner. |
| 3 / G1, G3, G5, G8 | Pilot a bounded specification and handoff on one project; reconcile duplicate terminology/context at its canonical owner. | Another contributor resumes a partially completed feature from versioned records and verifies the next step without recreating accepted decisions. | Proposed after a usable selected execution path; project owner and maintainer. |
| 4 / G5, G6 | Evaluate selected model/host combinations and independent contributor scopes on the pilot tasks. | Comparable task outcomes, actual discovery/interception limits, conflict handling and measured coordination cost. | Proposed after baseline and bounded task contract; maintainer. |
| 5 / G7 | Instantiate one project-specific Azure delivery path with application CI, identity, observability and recovery. | Identified artifact/target, authorized deployment, core user-path verification and recovery evidence. | Proposed after the project declares its stack and target; project/release owner. |
| 6 / G2, G7 | Exercise maintenance with a real failure or controlled incident and a bounded repair. | Observed signal, reproduced failure, repaired behavior and updated handoff/runbook. | Proposed after an operated pilot exists; service owner. |

## Later candidates

Signed scope compilation, purpose-class routing, a Rust fast path, shared audit
collection, monitoring bands and a bookkeeper appear in the master prompt.
Evaluate each against a measured gap. They are not a second implementation queue
and are not prerequisites for writing ordinary project documentation. A candidate
needs a bounded spec, owner, dependency and acceptance case before scheduling.

## Maintain the roadmap

Update an item when its dependency, scope or evidence changes. Use **proposed**,
**in progress**, **blocked**, **verified** or **deferred**, and link the actual
issue/PR and checked revision when they exist. Mark verified only when the exit
evidence is recorded. A prepared file, merged PR or passing fixture alone does
not establish production rollout. Keep detailed task state in the task record;
avoid copying its entire checklist here.
