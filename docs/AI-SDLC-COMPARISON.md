# What we took from AI-SDLC and why

Source: [ai-sdlc-framework/ai-sdlc](https://github.com/ai-sdlc-framework/ai-sdlc/tree/4ad7699af244d709625afe65e42b1f06f1770c3f),
Apache-2.0. Modified concept adaptations, not its TypeScript orchestrator.
See [NOTICE](../NOTICE), [DRIFT](DRIFT.md) and [reading evidence](../.guardian/READING-LOG.md).

| Their concept | Our artifact/check | Why / implementation limit |
| --- | --- | --- |
| DoR seven-gate rubric | tools/sdlc_governance.py, scripts/dor-check.py | Refuse unresolved work; semantic review and authentic acceptance remain separate |
| Signal shortcut | Caller-only2/3/7 evaluation, content gates marked SKIPPED | Preserve structure without trusting self-declared source |
| AutonomyPolicy | .ai-sdlc/autonomy-policy.yaml, change_gate | Observer0/Junior1,200lines,5files; no automatic promotion |
| AgentRole constraints | PROTECTED/ALLOWED_MUTATIONS and automation prompts | Deny wins; no new agent execution tools |
| QualityGate tiers | .ai-sdlc/quality-gate.yaml | Hard non-overridable versus soft/advisory; runtime overrides need authentication |
| Cross-harness v6 evidence | review_independence semantic precheck | Reject same-harness/absent stages; NOT an interoperable signature verifier |
| Untrusted PR gate | change_gate | Protected paths, renames, binary/link mutations, new uses and size checks; trusted diff adapter pending |
| Failure catalogue | failure_action and .ai-sdlc/orchestrator-failure-patterns.yaml | Security failures immediate; unknown modes escalate, unsafe remediation excluded |
| Review principles | finding_check and reviewer prompt | Major/critical need a concrete failure scenario |
| Decision principles | Guardian review guidance, one decision question | Counterargument and human consequence; no self-issued approval tokens |
| Emergent capture | intent/captures/template.md | Capture now, triage separately; no interrupting or auto-dispatch |
| Exploration | specs/_template/exploration.md | Timeboxed read-only work; crystallized implementation requires normal gates |
| Compliance posture | compliance/posture.yaml and posture_check | Explained overrides; no guessed statutory retention |
| Spec bridge | Kiro triad and spec-check.py | Strict missing-task/reference rejection; issue import not activated |
| Worktrees / rebase conventions | SDLC automation prompts | Separate contracts; no automatic destructive cleanup or merge |
| Framework-quality monitoring | Reviewer lensL18 | Distinguish framework defect from missing operator decisions |

Not taken: pnpm, husky, TypeScript orchestration, session-start installation,
user-home tool-sequence collection, secret-scan evasion, implicit merge authority,
unverified local signing as proof of isolation, or invented regulatory durations.
