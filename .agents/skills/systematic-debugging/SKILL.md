---
name: systematic-debugging
description: Diagnose a reproducible application, tool or runtime failure by tracing the first causal error, testing competing hypotheses and verifying a focused fix. Route missing or failed GitHub Actions checks to github-actions-debug.
---

# Establish the cause before changing behavior

Capture the observed symptom, expected result, relevant revision, environment and
smallest reproduction. Record exact commands and the first causal error with
surrounding context. Keep secrets and unrelated personal data out of captured
logs. Use the [diagnosis record](assets/diagnosis-record.md) to retain evidence for
a multi-step investigation; align the outcome with
[troubleshooting guidance](../../../docs/troubleshooting.md).

Trace input through the relevant entrypoint, dependency and state change. Distinguish
an upstream failure from a downstream summary. A timeout, empty response or final
exit code is an observation, not automatically the root cause. Use
[repo-discovery](../repo-discovery/SKILL.md) when the causal path is unfamiliar.
For retries, cancellation, distributed execution or ambiguous telemetry, use
[runtime boundary diagnosis](references/runtime-boundaries.md) to select the
relevant failure evidence and recovery check.

Keep a small set of plausible hypotheses and choose the next check that best
distinguishes them. Change one relevant factor at a time where practical. Inspect
versions and current official documentation when platform behavior is uncertain;
use forum fixes as hypotheses tied to their original environment.

Preserve unrelated work and evidence. Do not start with destructive resets,
credential replacement, blanket retries, weakened validation or broadened access.
A transient rerun needs supporting evidence and an attempt/time limit. If required
logs, access or a reproduction are unavailable, state the blocker and the specific
evidence needed instead of presenting a guess as a confirmed diagnosis.

When fixes are authorized, make the smallest correction addressing the causal
path using [clean-code](../clean-code/SKILL.md). Check the original reproduction
and a nearby unaffected behavior; use [test-design](../test-design/SKILL.md) for
meaningful regression coverage. Verify the combined change through
[verify-change](../verify-change/SKILL.md).

Report confirmed cause versus workaround or unresolved hypothesis. For GitHub
workflow failures or missing required checks, use
[github-actions-debug](../github-actions-debug/SKILL.md) for event/SHA and job-level
diagnosis instead of rerunning an unrelated workflow.
