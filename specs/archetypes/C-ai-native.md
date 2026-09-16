# C — Model, RAG or agent

Requested defaults: Microsoft Foundry model/agent capabilities, Azure AI Search where appropriate, versioned prompts, Application Insights tracing and content-safety controls. Verify exact model/deployment/region and integration maturity before pinning.

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

### AI supply chain

Record decisions, assumptions, measurable constraints, evidence and owner.

### AI threat model

Record decisions, assumptions, measurable constraints, evidence and owner.

### Data governance

Record decisions, assumptions, measurable constraints, evidence and owner.

## Test and eval profile

Groundedness,task success,safety,injection/leakage,regression-per-incident,prompt-diff and retrieval quality; calibrated graders; relevant fairness/robustness/error analysis and baseline comparison.

## Monitoring profile

Indicators: eval pass rate,groundedness/safety outcomes,latency,cost/request,model deprecation dates. Supply per-metric baseline version, mean, positive standard
deviation, direction, sample freshness and owner in monitoring/bands.yaml.
Do not reuse the synthetic latency baseline as a production calibration.
1σ logs;2σ proposes read-only diagnosis;3σ proposes an intent PR. Missing or
invalid data escalates. No automatic remediation is enabled.

## Compliance delta

AI Act classification and role-specific obligations, NIST GenAI actions, OWASP controls and GDPR scope. Not all provider high-risk duties automatically apply.

## Guardian delta

az cognitiveservices/ml/search and KeyVault reads in scope; existing hard-denied secret dumps remain denied.

## Infrastructure and delivery

Use the [shared platform baseline](../../docs/sdlc/AZURE-BASELINE.md).
This profile contains no deployed IaC module set or validated azd template.
Fetch official module source and actual parameter contract before authoring Bicep,
pin the verified version, run build/what-if under authorized scope, and retain
output. OIDC and production environment approvals are separate required controls.
No subscription, deployment, teardown or what-if success is assumed.
