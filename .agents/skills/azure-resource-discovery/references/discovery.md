# Resource inventory and topology

Record cloud/tenant/subscription/resource-group filters and collection time.
Use a resource ID when names collide; name-only matching can join different
environments. Explicit task context wins over a CLI default only when the actual
request is sent to that target. Do not change global login context unnecessarily.

Discover actual callable MCP tools and schemas. Prefer a supported read operation
for the selected resource. When suitable, use authorized Azure CLI/Resource Graph
or supplied exports. Distinguish management-plane resource visibility from
permission to read application data. Inventory needs configuration metadata,
not secret values, connection-string dumps or customer records.

## Coverage

Resource Graph returns bounded pages. Inspect continuation/truncation and total
counts; preserve stable ordering and the same filters on every page. Respect
query/time budgets. If more data remains, state exactly what was collected and
what remains. Access-denied or service errors mean unknown; an empty successful
response establishes absence only inside its queried visible scope.

For CLI query authoring, retain resource `id` and an ordered output where paging
requires it. An exploratory `take` is useful but cannot prove a full inventory.
Do not infer tenant-wide or company-wide coverage from one subscription's result.

## Relationships

Capture only needed fields: resource ID/type/name, location, SKU, relevant runtime
version, owner tags, configured identities, network references and parent/child
IDs. Verify relationships from explicit resource references, IaC or the actual
application configuration. Label the source for each edge. An assigned role does
not prove successful data access; a private endpoint does not prove working DNS;
an environment variable name does not establish a live connection.

For diagrams, separate resource containment, network path, application data flow
and identity authorization. Show external dependencies and unknowns. Split large
graphs around the question instead of placing all metadata inside every node.
Retain a complete inventory table for the collected scope. Render-check the
diagram with an available supported renderer when delivery depends on it; prose
review alone is not render evidence.

Sources: [Microsoft resource lookup](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-resource-lookup/SKILL.md),
[resource visualizer](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-resource-visualizer/SKILL.md),
[Resource Graph pagination](https://learn.microsoft.com/en-us/azure/governance/resource-graph/concepts/work-with-data).
