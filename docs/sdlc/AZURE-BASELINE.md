# Azure platform baseline — design contract, not deployed IaC

| Area | Required design decision | Validation / activation boundary |
| --- | --- | --- |
| Environments | dev/test/prod scopes, named owners, cost/data/archetype/intent tags | Confirm real subscription and tenant; no assumed access |
| Region | GermanyWestCentral/WestEurope default preference, explicit exceptions | Verify each service and inference-processing geography; EU resource location alone is insufficient |
| Identity | Entra users, managed service identities, OIDC workloads; least privilege | Verify actual subject claims and authorized role scope; Guardian identity restrictions remain |
| Secrets/config | KeyVault RBAC and AppConfiguration; no committed secrets | Secret dumps denied; secret-scanning evidence; no agent-created broad RBAC |
| Network | Private connectivity by default; public exposure justified behind WAF | Verify service support, DNS and integration; endpoint/security-policy changes require authorized platform handling |
| Governance | Regions/tags/network/diagnostics/Defender policies | Check definition IDs, effects, applicability and remediation identity; audit/deny not interchangeable |
| Observability | Project logs/traces/metrics, minimised payloads and retention | OpenTelemetry/ApplicationInsights; tested collection and failure behavior |
| Cost | Budgets, alerts, unit costs and sensitivity analysis | A budget is not a guaranteed spending hard stop; no prices asserted here |
| Delivery | Pinned verified modules; parameter contracts; build/what-if; rollback | No Bicep restore/build/what-if or Azure deployment performed in this environment |

Sources read on2026-09-16:
[AzurePolicy](https://learn.microsoft.com/en-us/azure/governance/policy/overview),
[OIDC Azure](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-azure),
[AVM catalog](https://azure.github.io/Azure-Verified-Modules/indexes/bicep/bicep-resource-modules/),
[Well-Architected](https://learn.microsoft.com/en-us/azure/well-architected/pillars),
[AI-SPM](https://learn.microsoft.com/en-us/azure/defender-for-cloud/ai-security-posture).

Verify module parameters before instantiating: catalog presence is not a validated
deployment contract. web/site supports Functions/LogicAppsStandard modes;
fabric/capacity does not establish Fabric workspace/pipeline provisioning.
Classic network/front-door is deprecated; assess current CDN-profile architecture.
No module parameter, OCI digest, OIDC subject or action permission is inferred.

Defender AI-SPM posture is distinct from runtime blocking. MCSBv2 is preview.
Foundry agent-level posture has licensing conditions; confirm them before promising
coverage. Do not label a configured baseline as regulatory compliance.
