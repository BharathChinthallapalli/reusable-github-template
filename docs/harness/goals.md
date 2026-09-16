# Harness goals

These are acceptance targets for the [vision](vision.md), not reported results.
The harness maintainer owns their prioritization; an adopting project owns its
application outcomes. Record measurements with revision, host/model where
relevant, task set, method and limitations. No performance baseline is supplied
by this documentation change.

| ID | Outcome | Acceptance evidence |
| --- | --- | --- |
| G1 | Understand the project without reconstructing chat history | A new contributor can locate purpose, terms, current contracts, commands and the next bounded action from the maintained entrypoints. Record unanswered questions and time taken. |
| G2 | Preserve useful behavior while improving the harness | Each changed contract has relevant acceptance evidence; pre-existing failures are distinguished from regressions. Record any unresolved regression explicitly. |
| G3 | Reduce unnecessary context and coordination | Compare representative tasks before/after using the same host/model and task conditions: loaded tokens where observable, files read, repeated instructions and task success. Claim improvement only with a measured baseline. |
| G4 | Make controls usable and their limits clear | Distinguish rejected legitimate operations from expected policy denials on an agreed inert corpus; record false-denial rate, denial coverage, recovery and hook latency. Native-host evidence is required for interception claims. |
| G5 | Resume across sessions and contributors | A fresh session uses the handoff to identify the checked revision, pending work, blockers, file ownership and next action without repeating completed work. |
| G6 | Keep model and host choices separable | The same bounded acceptance task can be attempted on selected hosts/models without changing its contract or permissions. Report unsupported surfaces and differences; do not assert universal parity. |
| G7 | Demonstrate useful delivery and maintenance | One selected project moves a feature from accepted need to verified operation, then ships a repair using the same records and proportionate checks. |
| G8 | Maintain a shared domain language | Terms affecting behavior have one scoped definition and a source/owner. Specs, interfaces and tests use it consistently; unresolved meanings remain explicit. |

Use [specification](spec.md) to locate existing mechanisms and
[roadmap](roadmap.md) for the remaining work. Goal IDs provide lightweight
traceability; they do not require a new tracking service.

Choose numeric budgets before a performance experiment, using the measured
baseline and actual task constraints. Do not invent token savings, latency
targets, model quality, delivery speed or compliance scores to fill a dashboard.
See the existing [AI evaluation contract](../ai-evaluation.md) when a comparison
includes model behavior. Feature counts, document counts and agent counts alone
do not demonstrate these outcomes.
