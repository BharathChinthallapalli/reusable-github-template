# Add Azure delivery deliberately

The base template contains no Azure deployment workflow or cloud resources. Use this guide after an application builds and its target service, environment ownership, and rollback procedure are known.

## Establish a deployment boundary

Write down the application artifact, Azure tenant and subscription, target resource group, hosting service, runtime identity, deployment identity, and environment names. Give deployment and application runtime separate identities because their duties differ. Start with a non-production environment and the narrowest Azure role and scope that can perform the actual deployment.

Prefer OpenID Connect (OIDC) federation for GitHub Actions authentication. It exchanges a workflow identity for Azure access without storing a long-lived client secret in GitHub. Use an Entra application/service principal or supported user-assigned managed identity with a federated credential. [Microsoft: Azure Login with OIDC](https://learn.microsoft.com/en-us/azure/developer/github/connect-from-azure-openid-connect).

## Match the actual OIDC claims

For GitHub.com and Azure public cloud, the relevant values are:

| Claim | Value or illustrative example |
| --- | --- |
| Issuer | `https://token.actions.githubusercontent.com` |
| Audience requested by Azure Login | `api://AzureADTokenExchange` |
| Earlier environment subject format | `repo:example-org/policy-assistant:environment:prod` |
| Immutable environment subject format | `repo:example-org@123456/policy-assistant@456789:environment:prod` |
| Earlier branch subject, without an environment | `repo:example-org/policy-assistant:ref:refs/heads/main` |

The names and numeric IDs above are examples. Copy neither subject into production unchanged. Verify your repository's OIDC configuration and match the actual subject exactly in Azure.

As documented on 9 September 2026, GitHub.com repositories created after 15 July 2026 use immutable subjects containing owner and repository IDs. Older repositories can retain the earlier format unless opted in; renames and transfers also change this behavior. Customized organization/repository subject templates can add further claims. GitHub Enterprise Server differs. [GitHub: OIDC reference](https://docs.github.com/en/actions/reference/security/oidc).

When the job uses `environment: prod`, its normal subject carries the environment context instead of the branch context. Restrict allowed deployment branches in that environment; the environment subject alone does not assert `main`. Azure sovereign clouds may require a different audience. [GitHub: Azure OIDC configuration](https://docs.github.com/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-azure), [Microsoft: audience configuration](https://learn.microsoft.com/en-us/azure/developer/github/connect-from-azure-openid-connect).

## Configure before running

1. Create the target GitHub environment under **Settings → Environments**, then configure its permitted deployment branch and any required reviewers. Confirm these controls are supported for your plan and visibility. Required reviewers for private repositories are not included in every plan. [GitHub: managing environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments).
2. Configure the Azure federated credential and narrowly scoped role assignment. Record who owns each identity and how access is revoked.
3. Store client, tenant, and subscription IDs as environment configuration according to organizational policy. These identifiers are not passwords. Put actual application secrets in the approved secret store; never commit them.
4. Add a separate deployment job referencing the configured environment. Give that job `contents: read` and `id-token: write`; the latter permits requesting an OIDC token and does not itself grant Azure resource access. Pin `azure/login` and other actions to verified upstream SHAs. [GitHub: Azure OIDC configuration](https://docs.github.com/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-azure).
5. Make delivery consume the artifact from a successful application build. Record its commit and digest or checksum. Deploy to non-production, verify health and the critical user path, and rehearse rollback before enabling production delivery.

Keep infrastructure definitions in version control once the target is selected. Review their proposed changes before applying them. A deployment workflow also needs sensible concurrency, timeouts, retained failure evidence, and a named operator; successful authentication alone proves none of those properties.

For authentication failures, compare issuer, audience, subject, environment spelling, and repository ID configuration first. For authorization failures after login, inspect Azure role and resource scope. Inspect only needed claims and identifiers; do not print raw identity or access tokens into logs.


## Reusable Azure task procedures

Use [azure-prepare](../.agents/skills/azure-prepare/SKILL.md) for a concrete
application/IaC plan, [azure-validate](../.agents/skills/azure-validate/SKILL.md) for
current evidence, and [azure-deploy](../.agents/skills/azure-deploy/SKILL.md) for an
already-authorized rollout. These phases preserve existing Bicep, Terraform, azd
or other project tooling. Reuse an existing equivalent plan and checks whose
input identities, target and acceptance scope still match; do not generate new
infrastructure just to satisfy a phase name. The general
[release-delivery](../.agents/skills/release-delivery/SKILL.md) skill remains the
artifact/release coordinator.

The records distinguish static/local checks from live prerequisites and observed
user outcomes. Missing tools, credentials, incomplete previews and stale evidence
remain unverified. A plan status or ready ADD cannot grant permissions or prove a
deployment. Useful local preparation can proceed before Azure access exists.

For inventory/topology use [azure-resource-discovery](../.agents/skills/azure-resource-discovery/SKILL.md).
See [Azure capability coverage](azure-capabilities.md) for diagnostics, identity,
cost, AI evaluation, data lineage and SDK/MCP extensions, and the explicit routes
for service-specific work not bundled in this foundation.
