# Execute and verify delivery

## Before the first mutation

Confirm the effective cloud, tenant, subscription, environment, resource group,
region and artifact from actual configuration. Use the existing supported
deployment tool and required environment controls. Respect active authorization;
do not introduce a repeated permission prompt for an already-authorized action.
For identity/OIDC setup, use [Azure delivery](../../../../docs/azure-delivery.md).

Verify the current validation record covers the deployed inputs and proposed
changes. Resolve destructive replacements, data migration, access changes, new
cost or target changes before execution. Review recovery feasibility: redeploying
an older binary does not undo a schema migration or restore deleted data.
Set a finite attempt/time budget from the operation, and define stop conditions.

Create a record with status in-progress before execution. Record the tool/run ID,
target, artifact identity, start time and intended resource changes. Do not put
tokens, credentials or complete environment dumps in the record.

## Execute the selected path

Follow repository scripts/workflows and their actual meaning. For azd, distinguish
provisioning infrastructure from deploying application code; do not invoke a broad
`up` operation when only a code deployment is authorized. For Bicep/Terraform,
consume the validated templates/parameters or reviewed plan through the project's
state and environment controls. The names of commands alone do not prove scope.

Poll known operations within timeout instead of repeating a write after an
ambiguous response. Inspect resulting state before retrying; failures may have
created some resources. Classify authentication, authorization, policy/quota,
configuration, application, transient service and unknown outcomes. Retry only
eligible failures, respecting provider backoff and idempotency. Preserve the first
causal error and attempted remedies. A changed region/SKU/identity or replacement
strategy needs renewed validation and any authorization its new impact requires.

## Verification and handoff

Confirm control-plane completion, then application startup, readiness, expected
version and a relevant user path. For a dependent app, test actual downstream
access with its runtime identity. An HTTP 200 can be a fallback page while the
database, secrets or tools are unavailable. Verify the user-visible behavior and
relevant error path without publishing sensitive data or generating uncontrolled
load. Record probes, environment, time and result.

Finalize success, partial or failed even when recovery cannot complete. Give the
operator artifact/run/resource references, observed health, remaining risks,
monitoring links and next recovery action. Keep retained resources and any cleanup
separate. Update IaC/configuration with in-scope corrections to avoid drift.

Sources: [Microsoft deployment](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-deploy/SKILL.md),
[onboarding delivery and health checks](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-app-onboard/deploy/SKILL.md).
