# Operations worksheet

Complete this for a deployed service. A library or documentation project may
mark inapplicable sections with a reason. Do not invent availability promises.

| Topic | Record for the project |
| --- | --- |
| Owner | Support channel, technical owner, escalation route |
| Environments | Purpose, region, resource identifiers, access boundaries |
| Configuration | Required names, source, validation, rotation ownership |
| Release | Build command, immutable artifact identifier, promotion procedure |
| Rollback | Previous artifact, data compatibility, restore procedure and evidence |
| Observability | Health check, logs, metrics, trace correlation, alert recipient |
| Reliability | User-facing failure modes and agreed availability/latency objectives |
| Data | Classification, retention, deletion, backup and restore ownership |
| Cost | Expected usage, budget owner, alerts and application-enforced limits |
| Incident | Triage commands, access procedure, containment, recovery verification |

For AI features, add model/deployment version, prompt and evaluation version,
token and request limits, evaluation thresholds with rationale, fallback behavior,
and treatment of sensitive prompts and outputs. Test whether a limit actually
stops usage: a billing alert alone is not a spending cap.

Record the last verified recovery exercise and the evidence location when the
system exists. Keep credentials and confidential resource exports out of this file.
