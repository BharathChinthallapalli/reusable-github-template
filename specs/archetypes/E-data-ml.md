# E — Data / training / fine-tuning

Requested defaults: Azure Machine Learning or Fabric where appropriate; versioned datasets, model registry and drift monitoring. A Fabric capacity module is not proof of workspace or pipeline provisioning.

## Required design sections

Add all common design sections plus the following **level-two headings**.
Each needs project-specific content or a justified, reviewed N/A. For C/D/E,
intent also needs feasibility, measurable KPIs, ethical impact and regulatory review.

### Data lineage

Record decisions, assumptions, measurable constraints, evidence and owner.

### Feature definitions

Record decisions, assumptions, measurable constraints, evidence and owner.

### Training and eval splits

Record decisions, assumptions, measurable constraints, evidence and owner.

### Bias and fairness

Record decisions, assumptions, measurable constraints, evidence and owner.

### Retraining and retirement

Record decisions, assumptions, measurable constraints, evidence and owner.

### AI supply chain

Record decisions, assumptions, measurable constraints, evidence and owner.

### AI threat model

Record decisions, assumptions, measurable constraints, evidence and owner.

### Data governance

Record decisions, assumptions, measurable constraints, evidence and owner.

### Eval plan

Record decisions, assumptions, measurable constraints, evidence and owner.

### Human oversight

Record decisions, assumptions, measurable constraints, evidence and owner.

## Test and eval profile

Schema/data validation; leakage/contamination controls; training reproducibility; holdout evaluation and bias/robustness analysis before promotion; data/model version rollback.

## Monitoring profile

Indicators: data/concept drift,model performance relative to baseline,retraining SLA,pipeline failures,cost. Supply per-metric baseline version, mean, positive standard
deviation, direction, sample freshness and owner in monitoring/bands.yaml.
Do not reuse the synthetic latency baseline as a production calibration.
1σ logs;2σ proposes read-only diagnosis;3σ proposes an intent PR. Missing or
invalid data escalates. No automatic remediation is enabled.

## Compliance delta

Data-governance duties for applicable high-risk provider systems; GDPR legal basis and DPIA trigger if personal data is used. No automatic permission to process special categories.

## Guardian delta

Training,registry,dataset and cloud operations in scope; destructive cloud/identity changes remain hard denied.

## Infrastructure and delivery

Use the [shared platform baseline](../../docs/sdlc/AZURE-BASELINE.md).
This profile contains no deployed IaC module set or validated azd template.
Fetch official module source and actual parameter contract before authoring Bicep,
pin the verified version, run build/what-if under authorized scope, and retain
output. OIDC and production environment approvals are separate required controls.
No subscription, deployment, teardown or what-if success is assumed.
