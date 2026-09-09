# Azure and Foundry tool boundaries

Treat these as separate facts: skill files present, host discovers them, MCP
connection configured, server authenticated, tool exposed, operation authorized,
and invocation observed. A plugin README or prompt naming a tool proves none of
the later facts. Inspect the selected host manifest and actual callable schema;
discover exact names/parameters instead of assuming an upstream alias exists.

The Azure Skills snapshot researched for this template declares Azure MCP through
an unpinned npx package, while its README also describes Foundry MCP. Do not copy
that startup configuration or promise Foundry access. Connect/install only for an
actual authorized project need; record provider version, startup source, transport,
identity, cloud/tenant/subscription scope and telemetry destinations. Preserve host
trust and enterprise controls. A CLI fallback must preserve the same scope and
authorization, not work around a denial.

Choose guidance by the actual boundary: Azure identity and token audience; Storage
or messaging data-plane retry/idempotency; Search/retrieval schema and permission
filtering; Foundry model/deployment and evaluation contract; API Management backend
authentication and per-caller limits; MCP transport and tool errors. Read current
Microsoft Learn/SDK documentation for the installed version before adding code.
Do not embed every Azure SDK, hard-code a vendor tool catalog, or add a service
because an upstream skill lists it. For specialized AKS, GPU, VM, migration,
fine-tuning or Entra Agent ID work, first establish the consuming requirement and
load only the relevant current source route in
[Azure capabilities](../../../../docs/azure-capabilities.md).

Record control-plane versus data-plane side effects, cancellation, timeout,
idempotency and unknown outcomes. Exercise the actual consumer flow when permitted;
static metadata and mocked results must be labeled. Local developer MCP tools are
not automatically an appropriate production backend for end users.

Sources: [Microsoft Azure MCP overview](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/overview),
[pinned plugin configuration](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/.github/plugins/azure-skills/.mcp.json).
