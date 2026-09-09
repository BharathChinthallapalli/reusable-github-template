# Validation evidence

Start with exact input identity: commit plus dirty changes where relevant,
application artifact digest, IaC/modules/lockfiles, parameter files and target
environment. Record secret configuration names/references, never values. Evidence
from another environment or changed inputs is stale for affected checks. Reuse
current evidence whose input identities, environment and acceptance scope still
match; do not re-prepare an unchanged project merely to invoke a phase skill.

## Select the lane

| Lane | Check | What it can establish |
| --- | --- | --- |
| Repository/local | Existing build, tests and packaging; startup/probe and dependency contract | Observed behavior in that environment |
| IaC/static | Existing Bicep build/lint or Terraform validation, module versions and reviewed identity/network configuration | Syntax and configured relationships; not live permissions or deployability |
| Target/preflight | Correct cloud/tenant/subscription, required resource and data-plane access, provider/SKU/region/policy/quota evidence | Observed target prerequisites at the recorded time |
| Change preview | Bicep what-if or the project's Terraform plan | Proposed changes with documented uncertainty; not a successful deployment |
| Application integration | Authorized non-production smoke path and downstream dependency access | The exercised behavior, not every workload condition |

Discover exact commands from the repository and current official tool docs.
`az bicep build --file <file>` checks a Bicep file. Terraform initialization may
download providers/modules or contact a backend; inspect configuration and the
existing prepared environment before running it. A Terraform plan can query live
resources and its output/state can contain sensitive data. Preserve its intended
state/backend instead of silently validating against a different environment.

A what-if result can contain unsupported/unresolved evaluation, apparent changes
from expressions, or short-circuited resources. Identify these specifically; do
not report no changes from a partial preview. Review deletion, replacement,
network/identity change, migration and cost effects against authorized scope.
Do not run provision/apply to turn an unknown preview into a green result.

## Results and freshness

Use passed, failed, unverified or not-applicable per check, with a reason and
evidence. Record command/tool, input identity, time, exit/status, redacted evidence
path and target. Not-applicable requires an actual condition (for example no
database migration), not unavailable credentials. Summarize prerequisites that
remain required before deployment, separate from optional recommendations.

After an in-scope correction, repeat checks affected by changed inputs. A later
region, SKU, permission, artifact or parameter change invalidates the relevant
results. Do not edit a status field to imply a rerun. A model-written report is a
record of claimed evidence, not independent attestation.

Sources: [Microsoft validation workflow](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-validate/SKILL.md),
[Bicep what-if behavior and limitations](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deploy-what-if).
