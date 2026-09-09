---
name: azure-validate
description: Validate an Azure change against its actual application artifacts, infrastructure, target configuration and deployment prerequisites. Use for Azure preflight or readiness checks; distinguish local evidence from unverified live checks.
---

# Validate an Azure change

Verify the target artifact and deployment plan using
[the validation procedure](references/validation.md). Reuse an existing equivalent
plan and evidence; there is no required vendor-specific status file.

1. Establish the revision, artifact, configuration, environment and intended
   change. Resolve missing design through
   [azure-prepare](../azure-prepare/SKILL.md) when necessary; a request to validate
   an existing file does not require generating replacement infrastructure.
2. Select checks from the actual deployment path and failure consequences. Record
   each observed result in [the validation record](assets/validation-record.md).
3. Fix in-scope failures and rerun affected checks. Mark unavailable tools/access,
   skipped checks, ambiguous previews and stale evidence explicitly.
4. Report ready only for the scope proved. If required live checks remain unknown,
   report that boundary rather than a blanket pass. Hand off to
   [azure-deploy](../azure-deploy/SKILL.md) only when deployment is already requested
   and required validation is current.

Validation itself does not authorize cloud changes. A plan status, checklist or
successful syntax check cannot substitute for the application's critical path.
