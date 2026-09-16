# Spec job — accepted-intent to proposed specification

Event design: accepted intent merge, bound to the exact repository/revision and
authorized product-owner decision. A mere file push is not proof of acceptance.

The isolated noninteractive generator receives the intent and only applicable
[standards](../STANDARDS.md), plus the [generation prompt](../../../llmops/prompts/spec-job.md).
It has read/search/source-fetch access, no shell/Azure tools, deployment credentials,
signing key or mutation authority. Its output is untrusted proposed artifacts.

A separate trusted coordinator validates output schema, EARS, references,
compliance, concerns, archetype headings, task traceability and waves using
scripts/spec-check.py and scripts/dor-check.py. Only an authorized bounded writer
may open the specification PR; product/policy/technical owners decide acceptance.

After accepted tasks, the future dispatcher creates one issue per task with
copied requirement IDs/criteria and assigns eligible tasks to Copilot coding
agents on separate branches. Preserve manual bot-workflow approvals, prevent
duplicate fallback work, and require independent review. Missing runtime,
capability, source, token or authenticated acceptance is BLOCKED—not fallback
role-play or broad allow-all.

This repository ships the prompt and deterministic validation, not an active
model/issue-writer workflow. Activation prerequisites remain explicit.
