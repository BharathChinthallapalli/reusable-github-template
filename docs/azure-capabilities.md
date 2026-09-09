# Azure capability coverage

This template includes original Azure procedures and selective extensions to its
engineering skills. It does not vendor the Microsoft plugin, install Azure/Foundry
MCP, provision resources or certify a live workload. Skills are available for
relevant tasks; host discovery, authenticated tools and real execution are separate.

## Use the task procedure

| Need | Procedure |
| --- | --- |
| Prepare application/IaC for Azure | [azure-prepare](../.agents/skills/azure-prepare/SKILL.md) |
| Validate current artifacts and target | [azure-validate](../.agents/skills/azure-validate/SKILL.md) |
| Execute authorized prepared delivery | [azure-deploy](../.agents/skills/azure-deploy/SKILL.md) |
| Discover actual resource scope/topology | [azure-resource-discovery](../.agents/skills/azure-resource-discovery/SKILL.md) |
| Diagnose a service or agent trace | [Azure debugging](../.agents/skills/systematic-debugging/references/azure.md) |
| Review identities and data access | [Azure security](../.agents/skills/security-review/references/azure.md) |
| Assess spending and utilization | [Azure cost/performance](../.agents/skills/performance-analysis/references/azure.md) |
| Compare Foundry versions and trace failures | [Azure evaluation](../.agents/skills/ai-evaluation/references/azure.md) |
| Curate trace-derived datasets | [Azure data contracts](../.agents/skills/data-contracts/references/azure.md) |
| Integrate SDKs/MCP/provider boundaries | [Azure tool integration](../.agents/skills/tool-integration/references/azure.md) |

## Reviewed source and meaning of coverage

The [Microsoft source](https://github.com/microsoft/azure-skills/tree/d4259f09db8f5631dce643427f0a55619b3f854f)
was pinned on 9 September 2026. Its complete tree has 2,522 entries. The 925
canonical skill files and 925 Azure-plugin mirror files have identical blob hashes.
There are 28 first-level families and 38 SKILL.md entrypoints including nested phase
documents, plus three distinct Kusto graph-plugin entrypoints. No native agent
profile definitions were found. All entrypoints were retrieved and screened;
detailed review focused on the procedures adopted here, not every reference line.

Each of the 38 canonical entrypoints is mapped below. Integrated means its
useful procedure was adapted into original guidance, not that the vendor runtime
or every subfeature is implemented. Deferred means a documented source route for
a concrete future project. Names do not establish native host discoverability of
nested source documents.

| Source entrypoint | Disposition | Template use or boundary |
| --- | --- | --- |
| [airunway-aks-setup](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/airunway-aks-setup/SKILL.md) | Domain workflow deferred | GPU/AKS serving only when a project requires it; preparation/integration first |
| [appinsights-instrumentation](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/appinsights-instrumentation/SKILL.md) | General procedure integrated | Operational readiness and performance; choose instrumentation from actual runtime/hosting |
| [azure-ai](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-ai/SKILL.md) | General procedure integrated | AI/data/tool skills; selected Search, Speech or extraction SDK documentation on demand |
| [azure-aigateway](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-aigateway/SKILL.md) | General procedure integrated | Tool integration, security and cost; gateway deployment/policies remain project-specific |
| [azure-app-onboard-prereq](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-app-onboard-prereq/SKILL.md) | Adapted into preparation | Component readiness with static versus executed evidence |
| [azure-app-onboard](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-app-onboard/SKILL.md) | Adapted into phase skills | Azure preparation, validation and deployment; no duplicate orchestrator |
| [azure-app-onboard/deploy](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-app-onboard/deploy/SKILL.md) | Adapted into phase skills | Azure preparation, validation and deployment; no duplicate orchestrator |
| [azure-app-onboard/prepare](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-app-onboard/prepare/SKILL.md) | Adapted into phase skills | Azure preparation, validation and deployment; no duplicate orchestrator |
| [azure-app-onboard/scaffold](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-app-onboard/scaffold/SKILL.md) | Adapted into phase skills | Azure preparation, validation and deployment; no duplicate orchestrator |
| [azure-cloud-migrate](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-cloud-migrate/SKILL.md) | Domain workflow deferred | Migration-specific SDK/data/cutover implementation requires a consuming workload |
| [azure-compliance](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-compliance/SKILL.md) | General procedure integrated | Security review; scoped findings without compliance certification |
| [azure-compute](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-compute/SKILL.md) | Domain workflow deferred | VM/VMSS, reservations and sizing require demonstrated workload needs |
| [azure-cost](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-cost/SKILL.md) | Procedure integrated | Azure reference in performance-analysis: actual, amortized, forecast and estimated costs |
| [azure-deploy](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-deploy/SKILL.md) | Procedure integrated | azure-deploy: authorized current artifacts, bounded recovery and real health |
| [azure-diagnostics](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-diagnostics/SKILL.md) | Procedure integrated | Azure reference in systematic-debugging: health, changes, logs and causal failure |
| [azure-enterprise-infra-planner](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-enterprise-infra-planner/SKILL.md) | General procedure integrated | Solution architecture plus Azure preparation; landing-zone provisioning remains project-specific |
| [azure-kubernetes](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-kubernetes/SKILL.md) | Domain workflow deferred | AKS setup/app rollout/Automatic migration require selected Kubernetes workload |
| [azure-kubernetes/azure-kubernetes-app-deploy](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-kubernetes/azure-kubernetes-app-deploy/SKILL.md) | Domain workflow deferred | AKS setup/app rollout/Automatic migration require selected Kubernetes workload |
| [azure-kubernetes/azure-kubernetes-automatic-readiness](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-kubernetes/azure-kubernetes-automatic-readiness/SKILL.md) | Domain workflow deferred | AKS setup/app rollout/Automatic migration require selected Kubernetes workload |
| [azure-kusto](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-kusto/SKILL.md) | General procedure integrated | Schema-first bounded telemetry queries; ADX-specific analytics on demand |
| [azure-messaging](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-messaging/SKILL.md) | General procedure integrated | Debugging/tool references: SDK version, locks, checkpoint and redelivery |
| [azure-prepare](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-prepare/SKILL.md) | Procedure integrated | azure-prepare preserves existing azd/Bicep/Terraform/other toolchain |
| [azure-quotas](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-quotas/SKILL.md) | General procedure integrated | Preparation/preflight distinguish quota, capacity, region and unknown access |
| [azure-reliability](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-reliability/SKILL.md) | General procedure integrated | Operational readiness and recovery requirements; no blanket redundancy deployment |
| [azure-resource-lookup](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-resource-lookup/SKILL.md) | Procedure integrated | azure-resource-discovery: scoped live/export/IaC inventory and pagination |
| [azure-resource-visualizer](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-resource-visualizer/SKILL.md) | Procedure integrated | Discovery plus architecture evidence; observed versus inferred edges |
| [azure-storage](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-storage/SKILL.md) | General procedure integrated | Preparation/data/tool references; actual service contracts and data-plane permission |
| [azure-upgrade](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-upgrade/SKILL.md) | Domain workflow deferred | Assess then implement the specific SDK/service migration without replacing generic maintenance |
| [azure-validate](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-validate/SKILL.md) | Procedure integrated | azure-validate: evidence tied to actual inputs, no status-file enforcement claim |
| [entra-agent-id](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/entra-agent-id/SKILL.md) | Domain provisioning deferred | Security/tool boundary guidance; agent identity creation requires a real integration need |
| [entra-app-registration](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/entra-app-registration/SKILL.md) | General procedure integrated | Security Azure reference: delegated/application access and separate identities |
| [microsoft-foundry](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/microsoft-foundry/SKILL.md) | General lifecycle integrated | AI evaluation/data lineage/traces/tool boundaries; hosted deployment/training protocols on demand |
| [microsoft-foundry/finetuning](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/microsoft-foundry/finetuning/SKILL.md) | General lifecycle integrated | AI evaluation/data lineage/traces/tool boundaries; hosted deployment/training protocols on demand |
| [microsoft-foundry/models/deploy-model](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/microsoft-foundry/models/deploy-model/SKILL.md) | General lifecycle integrated | AI evaluation/data lineage/traces/tool boundaries; hosted deployment/training protocols on demand |
| [microsoft-foundry/models/deploy-model/capacity](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/microsoft-foundry/models/deploy-model/capacity/SKILL.md) | General lifecycle integrated | AI evaluation/data lineage/traces/tool boundaries; hosted deployment/training protocols on demand |
| [microsoft-foundry/models/deploy-model/customize](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/microsoft-foundry/models/deploy-model/customize/SKILL.md) | General lifecycle integrated | AI evaluation/data lineage/traces/tool boundaries; hosted deployment/training protocols on demand |
| [microsoft-foundry/models/deploy-model/preset](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/microsoft-foundry/models/deploy-model/preset/SKILL.md) | General lifecycle integrated | AI evaluation/data lineage/traces/tool boundaries; hosted deployment/training protocols on demand |
| [python-appservice-deploy](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/python-appservice-deploy/SKILL.md) | Domain recipe deferred | Azure phase skills research the existing Python App Service project path when needed |
| [azure-kusto-graph](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/.github/plugins/azure-kusto-graph-skills/skills/azure-kusto-graph/SKILL.md) | Domain workflow deferred | Requires a selected ADX/IRQL investigation and verified database functions; no Kusto deployment or runtime bundled |
| [azure-kusto-irql-graph](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/.github/plugins/azure-kusto-graph-skills/skills/azure-kusto-irql-graph/SKILL.md) | Domain workflow deferred | Requires a selected ADX/IRQL investigation and verified database functions; no Kusto deployment or runtime bundled |
| [azure-kusto-irql](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/.github/plugins/azure-kusto-graph-skills/skills/azure-kusto-irql/SKILL.md) | Domain workflow deferred | Requires a selected ADX/IRQL investigation and verified database functions; no Kusto deployment or runtime bundled |

## Additional Foundry workflows beyond SKILL.md filenames

The Foundry router also points to Markdown workflows for creation, deployment,
CI/CD, invocation, routines, duplex voice/streaming, observation, traces, hosted-code
validation, optimization, dataset lifecycle, projects/resources, networking, quota,
RBAC and azd. This is why SKILL.md counts alone are incomplete. The template adopts
environment/version resolution, evidence, evaluation lineage and integration
boundaries. It defers scheduled execution, fine-tuning, live model provisioning,
voice transport and vendor-specific orchestration until a project needs them.
See the [pinned Foundry router](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/microsoft-foundry/SKILL.md).

## Consumer and evidence boundaries

The pinned Azure plugin MCP configuration declares Azure only, through an unpinned
npx package, despite the README also describing Foundry MCP. The marketplace
includes the separate graph plugin, while the APM manifest lists only Azure.
Inspect actual host configuration and exposed schemas before relying on a tool.
No upstream telemetry hooks or startup commands were copied. Source procedures
that force azd, repeat approvals already granted by the task, treat static
inspection as a successful build, or claim unmeasured savings are not adopted.

The visible upstream workflows build/deploy its site and create sync releases;
they do not prove native skill invocation or live cloud behavior. Template checks
likewise validate repository artifacts. Azure readiness, successful deployment and
model quality need their own observed evidence.

Sources are MIT-licensed by Microsoft; these task procedures are original synthesis
with attribution, not bundled upstream implementation. See the [source license](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/LICENSE).
