---
schema_version: 1
id: ADD-0005
status: ready
scope:
- tools/sdlc_contracts.py
- tools/sdlc_governance.py
- tools/sdlc_monitor.py
- tools/sdlc_metrics.py
- scripts/dor-check.py
- scripts/spec-check.py
- scripts/monitor.py
- scripts/metrics.py
- scripts/governance-check.py
- tests/test_sdlc.py
- docs/SDLC.md
- docs/DRIFT.md
- docs/HANDOVER.md
- docs/metrics.md
- docs/AI-SDLC-COMPARISON.md
- docs/sdlc/ACTIVATION.md
- docs/sdlc/WORKED-EXAMPLE.md
- .guardian/READING-LOG.md
- intent/_template/intent.md
- intent/_template/decision.md
- intent/captures/template.md
- specs/_template/requirements.md
- specs/_template/design.md
- specs/_template/tasks.md
- specs/_template/bugfix.md
- specs/_template/exploration.md
- specs/_template/gap-analysis.md
- monitoring/bands.yaml
- runbooks/incident.md
- runbooks/rollback.md
- runbooks/kill-switch.md
- compliance/MATRIX.md
- compliance/posture.yaml
- mlops/model-card.md
- mlops/data-card.md
- mlops/README.md
- llmops/README.md
- llmops/prompts/spec-job.md
- evals/README.md
- .ai-sdlc/dor-config.yaml
- .ai-sdlc/autonomy-policy.yaml
- .ai-sdlc/quality-gate.yaml
- .ai-sdlc/orchestrator-failure-patterns.yaml
- .ai-sdlc/untrusted-pr-gate.yaml
- NOTICE
- LICENSES/Apache-2.0.txt
- specs/archetypes/A-web-app.md
- specs/archetypes/B-automation.md
- specs/archetypes/C-ai-native.md
- specs/archetypes/D-multi-agent.md
- specs/archetypes/E-data-ml.md
- docs/sdlc/automations/researcher.md
- docs/sdlc/automations/reviewer.md
- docs/sdlc/automations/engineer.md
- docs/sdlc/automations/monitor.md
- docs/sdlc/automations/spec-job.md
- intent/monitor-smoke/intent.md
- specs/monitor-smoke/requirements.md
- specs/monitor-smoke/design.md
- specs/monitor-smoke/tasks.md
- specs/monitor-smoke/spec.md
- docs/sdlc/fixtures/events.json
- docs/sdlc/fixtures/samples.json
- compliance/ai-act/system-assessment.md
- compliance/ai-act/technical-documentation.md
- compliance/ai-act/oversight-and-post-market.md
- compliance/gdpr/records-and-dpia.md
- compliance/betrvg/co-determination.md
- compliance/nist-rmf/control-map.md
- compliance/owasp-llm/control-map.md
- compliance/iso42001/CLAUSES-UNVERIFIED.md
- docs/sdlc/AZURE-BASELINE.md
- .agents/skills/sdlc-admission/SKILL.md
- .agents/skills/compliance-mapping/SKILL.md
- .agents/skills/data-governance/SKILL.md
- .agents/skills/ux-standards/SKILL.md
- .agents/skills/brand-standards/SKILL.md
- .agents/skills/cost-modelling/SKILL.md
- docs/sdlc/STANDARDS.md
- docs/sdlc/VALIDATION.md
adrs:
- docs/adr/0004-portable-engineering-capabilities.md
- docs/adr/0005-scoped-agent-design-gate.md
- docs/adr/0011-guardian-command-gate.md
binding_sha256: bb2ead7824e5b8bf6bde638ee89362719bfe04a987a6a5ee321a7624d1a52d6b
---
# AI-native SDLC: local admission and artifact foundation

## Purpose

Implement the user's six-stage template loop using the canonical Anthropic playbook,
Kiro specifications and selected AI-SDLC governance concepts. The completed source
review and two-source exception are recorded in [.guardian/READING-LOG.md](../../.guardian/READING-LOG.md).
Keep unavailable implementation and operating evidence visible.

## Scope and non-goals

The explicit files above form a runnable local foundation: contracts, admission
checks, monitoring proposals, metrics, templates, profiles and operating guidance.
This change does not install a runtime, deploy Azure, merge a PR, grant a cloud
identity, create an approval issuer, or replace existing Guardian enforcement.
Existing tests, hooks and deny rules remain intact. Protected-runtime adaptations,
production dispatch and upstream v6 byte-level signing interoperability are
separate activation work; a schema-only check cannot stand in for them.

## Inputs and outputs

Markdown artifacts carry strict JSON frontmatter (a YAML subset). Bounded local
readers validate schemas, explicit workspace references, EARS syntax, task waves
and test traceability. Deterministic monitors emit proposals to stdout. Reports
identify structural readiness separately from authenticated acceptance. No CLI in
this slice executes a model-supplied command, writes an approval token or calls an
external service. Metrics report missing evidence as unavailable.

## Capabilities and permissions

Root performs this user-authorized implementation and local fixture tests.
Research agents stay read-only and never execute shell/Azure work. Tools use
explicit project paths, not home discovery. Shell preparation prefers rg/fd/jq;
fd absence uses scoped rg. Existing Python tooling is retained, with no new
TypeScript orchestrator, pnpm, husky or agent tool grants.

## Behavior and failure modes

Malformed input, duplicate keys, unsafe paths, unresolved markers, unknown
requirements, missing compliance, invalid dependency waves, excessive change
budgets, protected-path mutations and invalid overrides fail with actionable
messages. No self-declared source, accepted label or harness name authenticates
authority. The structural DoR shortcut is unavailable without a separately trusted
integration; source labels alone cannot unlock it. Unknown failures escalate.
GuardianDenied, PivotAttempt and HookTimeoutFailOpen escalate immediately.

## Validation

Run the existing design and repository checks, new table-driven negative tests and
an isolated scratch-project example. Cover unresolved decisions, forged monitor
provenance, task cycles, omitted tests, missing compliance, protected renames,
new Actions references, same-harness review, stale/invalid bands and missing notes.
Keep fixture results separate from native Windows, real review attestations,
GitHub workflow execution and Azure what-if/deployment results.

Merge review on 2026-09-16 re-fetched the cited OWASP page and corrected the
compliance matrix, control-map edition and source-log record to its observed
2025 risk IDs. No executable control, policy or scope changed. The updated
content binding must pass the existing hosted design check before merge.

## Risks and alternatives

An editable checkout is not a security boundary. Admission must eventually run
from a protected control plane against immutable input with authenticated approval
and replay protection. Regex EARS shape checks cannot prove semantic quality.
Sigma thresholds require domain calibration and are not incident probabilities.
Legal mappings remain scope/role qualified, with no ISO clauses inferred and no
Annex I draft-based classification. See [DRIFT](../DRIFT.md).
