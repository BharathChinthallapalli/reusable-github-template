# Metrics and evidence contract

`python scripts/metrics.py <project-relative-events.json>` computes supplied-event
metrics without external calls or writes. The JSON array is bounded; every event
has event_id, change, kind, timestamp with timezone, and value (null except numeric
eval/cost/gate_wait). Duplicate IDs, invalid kinds, negative values, conflicting
decisions and reversed paired timestamps fail.

| Indicator | Data required | Current calculation |
| --- | --- | --- |
| First conversation→intent | Conversation record plus intent commit event | Mean paired seconds |
| Intent survival | Explicit accepted/rejected decisions | Accepted / decided, not all outstanding intents |
| Intent→spec | First intent/spec events | Mean paired seconds |
| Spec rework after tasks | Exact Git content revisions, not timestamps alone | Unavailable |
| Gate wait | Trusted approval request/decision pair | Mean supplied gate_wait seconds |
| Gate violations reaching production | Complete release/control inventory | Unavailable when absent; never zero by assumption |
| Breach→intent | Same finding ID and events | Mean paired seconds |
| Finding→merged fix share | Classified finding cohort and linked merged fixes | Unavailable |
| Repeat incidents by class | Incident taxonomy and complete cohort | Unavailable |
| PR cycle time | Actual opened/merged events | Mean paired seconds |
| Eval trend | Versioned labeled eval outcomes over comparable windows | Supplied-window pass rate; time-series publication pending |
| Cost per successful task | Complete same-window cost and success inventory | Supplied cost / successful change count |

Event-source adapters must authenticate provenance and minimise personal data.
Git alone does not contain conversations, model billing, trusted approval timing,
or proof that a control violation reached production. Weekly Git/ledger/issue/cost
ingestion and publication are open activation work. Do not treat omitted events
as a zero denominator or a clean compliance result.

The [fixture events](sdlc/fixtures/events.json) are synthetic and labelled as such.
They demonstrate arithmetic, not project delivery performance.
