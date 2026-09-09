# Azure identity and access review

Trace the denied or changed operation from caller to resource. Record deployment
identity separately from runtime/user identity, token audience, tenant, requested
action, assigned role and resource scope. Distinguish management-plane and
data-plane access; successful login or resource listing does not prove blob,
database, model or secret access. Inspect only necessary claims, never raw tokens.

For GitHub federation, use the project's actual issuer/audience/subject and
environment controls in [Azure delivery](../../../../docs/azure-delivery.md).
For application integration, determine delegated versus application access, user
authorization propagation, managed identity/federation support, token caching and
revocation. Research the actual SDK and service's current role definitions; avoid
an omnibus Contributor/Owner grant as a diagnostic shortcut.

Trace network enforcement independently: ingress, egress, private endpoint, DNS,
firewall and service configuration. Review secret metadata/lifecycle without
fetching secret values when values are unnecessary. Scope Key Vault or compliance
findings to observed checks; an automated configuration review is not a legal or
organization-wide compliance certification.

For agent/MCP integrations, the host tool list, consent and Azure RBAC are separate
controls. Determine whose identity an operation uses and whether caller-specific
authorization survives each boundary. Do not configure Entra Agent ID objects or
install a sidecar without an actual project requirement and current official docs.

Sources: [Microsoft Azure MCP overview](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/overview),
[Entra integration source](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/entra-app-registration/SKILL.md),
[Azure compliance source](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-compliance/SKILL.md).
