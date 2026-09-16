# A — Web app

Requested defaults: Next.js plus FastAPI or .NET; PostgreSQL Flexible Server or Cosmos DB; Entra/managed identity; Container Apps or App Service; Static Web Apps only where its constraints fit; private networking and a justified WAF-protected public entry.

## Required design sections

Add all common design sections plus the following **level-two headings**.
Each needs project-specific content or a justified, reviewed N/A. For C/D/E,
intent also needs feasibility, measurable KPIs, ethical impact and regulatory review.

### API contract

Record decisions, assumptions, measurable constraints, evidence and owner.

### Data model and migrations

Record decisions, assumptions, measurable constraints, evidence and owner.

### Auth matrix

Record decisions, assumptions, measurable constraints, evidence and owner.

### Performance budgets

Record decisions, assumptions, measurable constraints, evidence and owner.

### Accessibility and i18n

Record decisions, assumptions, measurable constraints, evidence and owner.

## Test and eval profile

Unit; OpenAPI contracts; integration against an explicitly authorized disposable environment; Playwright journeys; load smoke; accessibility; SAST/DAST and secret scanning. A per-PR resource-group lifecycle needs platform approval; Guardian resource-group-delete denials are not bypassed by cleanup.

## Monitoring profile

Indicators: p95 latency,5xx rate,error-budget burn,auth failures,cost/day. Supply per-metric baseline version, mean, positive standard
deviation, direction, sample freshness and owner in monitoring/bands.yaml.
Do not reuse the synthetic latency baseline as a production calibration.
1σ logs;2σ proposes read-only diagnosis;3σ proposes an intent PR. Missing or
invalid data escalates. No automatic remediation is enabled.

## Compliance delta

GDPR processing record and DPIA trigger where relevant; public tracking/cookie consent needs its applicable legal assessment. Add C when AI is embedded.

## Guardian delta

az webapp/containerapp/postgres/cosmos operations in scope; production release requires authenticated authorization.

## Infrastructure and delivery

Use the [shared platform baseline](../../docs/sdlc/AZURE-BASELINE.md).
This profile contains no deployed IaC module set or validated azd template.
Fetch official module source and actual parameter contract before authoring Bicep,
pin the verified version, run build/what-if under authorized scope, and retain
output. OIDC and production environment approvals are separate required controls.
No subscription, deployment, teardown or what-if success is assumed.
