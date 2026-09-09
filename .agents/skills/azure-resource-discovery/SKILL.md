---
name: azure-resource-discovery
description: Inventory Azure resources and evidence-backed relationships within a requested scope. Use for live resource lookup, topology and configuration discovery; distinguish incomplete access from absence and do not change resources.
---

# Discover Azure resources

1. Resolve the requested cloud, tenant, subscription/resource group and purpose
   from task context. Do not scan every accessible subscription by default.
2. Use [discovery](references/discovery.md) to select an available read operation,
   follow pagination and capture safe configuration and provenance.
3. Write [the inventory](assets/resource-inventory.md) when a reusable artifact
   helps the task. Separate observed relationships from inferred/unknown ones.
4. For architecture questions, link inventory evidence to the application's code
   and IaC. For costs, use the Azure guidance in
   [performance-analysis](../performance-analysis/SKILL.md); apparently unused
   resources are not automatically waste or safe to delete.

If live access is missing, analyze supplied exports/IaC as their own dated
evidence source. Do not call them current live inventory, install a provider,
enable an MCP connection or expand permissions merely to complete discovery.
