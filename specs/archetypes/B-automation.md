# B — Integration and workflow

Requested defaults: Logic Apps Standard or Functions/Durable Functions; Event Grid/Service Bus; Power Automate/Dataverse for business-owned flows; Copilot Studio with solution-based ALM where appropriate. No environment-specific connection references committed.

## Required design sections

Add all common design sections plus the following **level-two headings**.
Each needs project-specific content or a justified, reviewed N/A. For C/D/E,
intent also needs feasibility, measurable KPIs, ethical impact and regulatory review.

### Trigger catalogue

Record decisions, assumptions, measurable constraints, evidence and owner.

### Idempotency and retries

Record decisions, assumptions, measurable constraints, evidence and owner.

### Connector inventory

Record decisions, assumptions, measurable constraints, evidence and owner.

### Tenant and region flows

Record decisions, assumptions, measurable constraints, evidence and owner.

### Run retention and DLP

Record decisions, assumptions, measurable constraints, evidence and owner.

## Test and eval profile

Functions unit tests; recorded-event replay; connector contracts; retry/poison-message chaos; conversational intent/topic evals. Keep fixtures synthetic or approved/redacted.

## Monitoring profile

Indicators: run failure rate,dead-letter depth,flow latency,connector throttling,license/credit consumption. Supply per-metric baseline version, mean, positive standard
deviation, direction, sample freshness and owner in monitoring/bands.yaml.
Do not reuse the synthetic latency baseline as a production calibration.
1σ logs;2σ proposes read-only diagnosis;3σ proposes an intent PR. Missing or
invalid data escalates. No automatic remediation is enabled.

## Compliance delta

Power Platform environment and DLP policy assessment; BetrVG when worker activity is monitored; applicable Article50 notices for user-facing bots.

## Guardian delta

pac,az logic/functionapp/servicebus and Graph calls in scope; publish requires human authority, not a generated ask/allow claim.

## Infrastructure and delivery

Use the [shared platform baseline](../../docs/sdlc/AZURE-BASELINE.md).
This profile contains no deployed IaC module set or validated azd template.
Fetch official module source and actual parameter contract before authoring Bicep,
pin the verified version, run build/what-if under authorized scope, and retain
output. OIDC and production environment approvals are separate required controls.
No subscription, deployment, teardown or what-if success is assumed.
