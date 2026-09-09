# Azure cost and utilization evidence

Separate five quantities: billed actual cost, amortized allocation, forecast,
catalog-price estimate and measured utilization. Record scope, currency, period,
granularity, pricing date and any incomplete pages or access. Never sum currencies
or compare different periods without an explicit conversion/normalization.
Account for shared resources, reservations/discounts and delayed ingestion where
they affect the conclusion. An error or empty permission-trimmed result is not zero
spend. If the task is a new workload estimate, no actual bill exists: model usage
assumptions transparently instead of pretending it has been queried.

For an existing workload, correlate actual spending with resource inventory,
usage/latency/error rates and relevant change history. Distinguish fixed idle cost,
per-request/token cost, storage/egress and observability ingestion. Estimate a
proposal's savings as a range with assumptions and migration/operating effort.
An apparently orphaned resource may support backup, failover or another team.
Recommend changes before executing them; optimization does not imply deletion.

For model-backed workloads, record input/output/cached tokens, request count,
model/version/SKU, retries, tool calls and evaluation/telemetry costs separately.
Test cache changes for answer correctness and tenant/data isolation. Do not raise
rate limits, lower safety thresholds or enable cross-region routing merely to
remove a 429 or reduce latency. Evaluate impact against the actual budget,
processing boundary and service requirements.

Use available current Cost Management/Monitor APIs and their response schemas.
Respect service-provided retry timing and a bounded query budget; do not repeatedly
query a throttled scope. Missing tools are a stated evidence gap, not a reason to
install an MCP server or activate paid monitoring automatically.

Sources: [Microsoft Cost Analysis](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/quick-acm-cost-analysis),
[Azure cost evidence distinctions](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/azure-cost/references/tools-and-best-practices.md).
