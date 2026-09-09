---
name: azure-prepare
description: Prepare an application or infrastructure change for Azure by tracing repository readiness, selecting justified services and producing deployment artifacts. Use before Azure validation or when preparing Azure IaC; preserve the project's existing deployment tool.
---

# Prepare an Azure change

Produce a concrete plan and the requested local artifacts. Preparation does not
provision resources. For a resource inventory alone, use
[azure-resource-discovery](../azure-resource-discovery/SKILL.md).

1. Read project context, accepted ADRs, application manifests, existing IaC and
   delivery configuration. Establish the requested outcome and existing resources
   to preserve; do not infer the application stack from this template's tools.
2. Use [preparation](references/preparation.md) to assess components and select
   services, identities, network boundaries, region/SKU and deployment method.
   Record findings in [the Azure plan](assets/azure-plan.md), adapting its size to
   the change. Separate observed evidence, agreed requirements and unknowns.
3. Generate or update only the authorized application/configuration/IaC files.
   Keep the existing azd, Bicep, Terraform or other deployment path unless a
   justified change is part of the task. Do not initialize over an existing app.
4. Run applicable local checks and hand the exact artifact/configuration set to
   [azure-validate](../azure-validate/SKILL.md). Continue to deployment only when
   the active task includes it and validation supports that target.

A missing subscription does not prevent useful local preparation. Record cloud
checks as unverified rather than signing in, registering providers or creating
resources merely to fill the plan.
