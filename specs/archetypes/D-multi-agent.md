# D — Multi-agent system

Requested defaults: Microsoft Agent Framework Python/.NET workflows with explicit checkpoints/HITL; hosted services only after maturity/availability checks; governed MCP; A2A only with justified need. Use functions for deterministic operations that do not need agent autonomy.

## Required design sections

Add all common design sections plus the following **level-two headings**.
Each needs project-specific content or a justified, reviewed N/A. For C/D/E,
intent also needs feasibility, measurable KPIs, ethical impact and regulatory review.

### Model choice and pinning

Record decisions, assumptions, measurable constraints, evidence and owner.

### Grounding and data cards

Record decisions, assumptions, measurable constraints, evidence and owner.

### Prompt versions

Record decisions, assumptions, measurable constraints, evidence and owner.

### Eval plan

Record decisions, assumptions, measurable constraints, evidence and owner.

### Human oversight

Record decisions, assumptions, measurable constraints, evidence and owner.

### Fallback and deprecation

Record decisions, assumptions, measurable constraints, evidence and owner.

### Agent roster

Record decisions, assumptions, measurable constraints, evidence and owner.

### Orchestration and termination

Record decisions, assumptions, measurable constraints, evidence and owner.

### Inter-agent trust

Record decisions, assumptions, measurable constraints, evidence and owner.

### State and checkpoints

Record decisions, assumptions, measurable constraints, evidence and owner.

### Containment and budgets

Record decisions, assumptions, measurable constraints, evidence and owner.

### AI supply chain

Record decisions, assumptions, measurable constraints, evidence and owner.

### AI threat model

Record decisions, assumptions, measurable constraints, evidence and owner.

### Data governance

Record decisions, assumptions, measurable constraints, evidence and owner.

## Test and eval profile

Per-agent evals; recorded-trace orchestration; tool-output injection into downstream agents; step/cost exhaustion; loop termination; checkpoint replay; isolation and per-agent kill-switch tests.

## Monitoring profile

Indicators: steps/run,cost/run,tool-call errors,HITL wait,injection detector hits. Supply per-metric baseline version, mean, positive standard
deviation, direction, sample freshness and owner in monitoring/bands.yaml.
Do not reuse the synthetic latency baseline as a production calibration.
1σ logs;2σ proposes read-only diagnosis;3σ proposes an intent PR. Missing or
invalid data escalates. No automatic remediation is enabled.

## Compliance delta

C controls plus each agent boundary's oversight/logging and agentic threat controls. Do not use raw inter-agent messages as a reason to retain unnecessary personal data.

## Guardian delta

C scope plus undeclared agent spawning denied by the planned roster controller; build-harness subagents remain research-only. Native roster enforcement is not activated by this profile.

## Infrastructure and delivery

Use the [shared platform baseline](../../docs/sdlc/AZURE-BASELINE.md).
This profile contains no deployed IaC module set or validated azd template.
Fetch official module source and actual parameter contract before authoring Bicep,
pin the verified version, run build/what-if under authorized scope, and retain
output. OIDC and production environment approvals are separate required controls.
No subscription, deployment, teardown or what-if success is assumed.
