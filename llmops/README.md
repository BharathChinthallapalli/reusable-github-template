# LLMOps in the loop

Keep prompt sources in llmops/prompts and bind their byte hashes, model/deployment
versions and evaluation versions to review evidence. Prompt changes are code
changes: PR, eval, independent review and human review where applicable.
Evaluation prompts and datasets remain protected.

Record fallback behavior, model deprecation deadlines, per-request and per-run
token/cost limits, retry/step ceilings and kill-switch authority. Traces should
minimise payloads, derive identity server-side and record redaction/retention.
Foundry evaluation, monitoring and OpenTelemetry traces are distinct; partial
evaluation is not passing evidence. No tracing collector is configured by this
worksheet. Cost rates and region/processing claims require current sources.
