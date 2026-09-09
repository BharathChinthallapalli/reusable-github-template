# Azure incident evidence

Resolve the affected environment, resource IDs, release/version and incident time
window before querying. Check service/resource health and recent deployment or
activity changes, then application logs, dependency failures and metrics. Use
available read tools; a resource configuration lookup is not itself a Resource
Health check. Distinguish platform outage from application/identity/network error.

Select only the relevant service lane: Container Apps image/start/probe/port and
revision; App Service startup/deployment/runtime/plan; Functions trigger/binding,
host startup and timeout; messaging connection, lock renewal, checkpoint and
redelivery; AKS scheduling/node/network only when the workload actually uses AKS.
Discover installed SDK versions before consulting current service troubleshooting
docs. Avoid guessing commands or table names from another version/environment.

For Foundry traces, resolve the deployed agent and environment before selecting
App Insights. Inspect the actual emitted schema. Correlate top-level request,
tool/dependency spans and failure by trace/operation identifiers; nested agent
names need not identify the deployed agent. Start with bounded summaries and
drill into needed spans; do not export raw conversations by default. Preserve
environment, version, time range, query and coverage in findings.

Authentication, RBAC/data-plane authorization, DNS/network and application
failures require different fixes. Confirm the first causal error; do not broaden
roles, disable networking controls or restart production as an exploratory read.
Apply in-scope remediation, bound attempts and verify the original user path.
Persist useful recovery evidence in the project's runbook.

Sources: [Azure diagnostics](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-diagnostics/SKILL.md),
[Foundry trace procedure](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/microsoft-foundry/foundry-agent/trace/trace.md).
