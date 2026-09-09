# Foundry evaluation and observability

Resolve the agent root, environment, project endpoint, actual deployment identity,
agent/model version and current evaluation configuration. Prefer the deployment
tool's authoritative values over a stale metadata cache; report conflicts before
executing an evaluation against the wrong environment. Do not copy secret
environment dumps into evaluation artifacts.

Pin dataset, evaluator/rubric, candidate and baseline versions together. Confirm
remote suite/dataset references actually resolve when running in Foundry. A local
file named eval.yaml is not proof of a registered or executed remote suite.
Keep transport/authentication/quota failures distinct from model-quality failures.
The template's report validator checks record structure, not whether a model ran.
Track model-output quality, orchestration/job health, tool/action-handler success
and the final observed artifact or user outcome separately. A successful model
response, empty output or completed job does not prove the requested effect.

When traces explain a regression, scope to environment and time window, correlate
requests/tools by observed trace identifiers and retain enough provenance to link
failure to evaluated response/version. Read the current emitted schema and
supported GenAI telemetry conventions. Sampling, missing spans and unobserved
conversations limit conclusions; an absence of recorded failures is not proof of
quality. Avoid exporting raw prompts or personal information unnecessarily.

Use [Azure dataset guidance](../../data-contracts/references/azure.md) when turning
production failures into test cases. Keep held-out evaluation separate from prompt
optimization. Bound trials, calls, tokens, elapsed time and spend; changing the
rubric or dataset mid-comparison creates a different experiment. Continuous
evaluation or automatic redeployment needs its own operational/cost scope; it is
not enabled by this skill. Compare meaningful user outcomes and failure clusters,
then retain or reject a candidate on evidence.

Sources: [Foundry observe](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/microsoft-foundry/foundry-agent/observe/observe.md),
[Foundry trace](https://github.com/microsoft/azure-skills/blob/d4259f09db8f5631dce643427f0a55619b3f854f/skills/microsoft-foundry/foundry-agent/trace/trace.md).
