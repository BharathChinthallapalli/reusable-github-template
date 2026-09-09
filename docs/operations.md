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

## Failure and recovery checks

Select only boundaries the application uses and the change affects. Document
the expected failure response, recovery condition and evidence for that boundary.

| Changed boundary | Relevant checks |
| --- | --- |
| External dependency | Timeout or unavailable response terminates within the intended budget; normal service resumes after recovery |
| Retry policy | Transient failures use bounded attempts and delay; permanent failures terminate; a lost response after a successful write does not duplicate the business effect |
| Queue consumer | Duplicate delivery and restart after partial processing preserve the intended result; exhausted attempts follow the documented recovery route |
| Cache | A write or expiration produces the expected freshness; invalidation and cache unavailability respect the documented fallback and consistency contract |
| Authentication or authorization | Expired credentials and denied permissions produce the intended failure without exposing protected data; restored access works through the intended identity |

Use an existing test harness or authorized test environment. These are
conditional failure cases, not a requirement to provision cloud resources or
run load or chaos tests for every task. Record limitations of simulated checks.
Use the [investigation record](troubleshooting.md#investigation-record) for
incidents, distinguishing a confirmed repair from a workaround.

Consult the selected dependency's current documentation. Microsoft's
[Retry pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry)
and [Cache-Aside pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside)
explain retry side effects and freshness trade-offs; they do not require adopting
an Azure service or either pattern.
