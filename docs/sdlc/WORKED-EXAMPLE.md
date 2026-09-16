# Worked example — explicitly synthetic

Date: 2026-09-16 UTC. Environment: Linux, Python3.12.14. This example tests local
artifact checks, proposal generation and arithmetic. It is not a real product
owner acceptance, GitHub PR/merge, model evaluation or Azure deployment.

## Artifact chain

| Step | Artifact / observation | Authority |
| --- | --- | --- |
| Intent | intent/monitor-smoke/intent.md | Synthetic author; not accepted |
| Requirements/design | specs/monitor-smoke/requirements.md and design.md | Structural validation only |
| Tasks | specs/monitor-smoke/tasks.md, T-1 → R-1, wave1 | Proposed, not dispatchable |
| Render | specs/monitor-smoke/spec.md | Source-hash-bound local rendering |
| PR/merge | docs/sdlc/fixtures/events.json contains labelled synthetic events | **No real PR or merge performed** |
| Breach | samples.json:130 against mean100/stddev10 | Deterministic tier3 |
| Follow-up | breach-p95-latency-3d2631e6f7eed648b07a | Proposed intent; triage/compliance/acceptance still required |

## Reproduction

From the repository, using its prepared environment and applicable Guardian
approval, run the following inspected, local-only commands:

```text
python scripts/spec-check.py monitor-smoke
python scripts/dor-check.py monitor-smoke
python scripts/monitor.py docs/sdlc/fixtures/samples.json --now 2026-09-16T10:01:00Z
python scripts/metrics.py docs/sdlc/fixtures/events.json
python -m unittest discover -s tests -p test_sdlc.py -q
```

The spec and DoR reports explicitly keep dispatch BLOCKED pending authenticated
acceptance. The monitor emits PROPOSE_INTENT_PR, allowed_tools=[], authorization=NONE,
runbook_execution=DISABLED. It does not actually open the PR or write a follow-up.

## Observed synthetic metrics

| Metric | Fixture result |
| --- | --- |
| Conversation→intent |300seconds |
| Intent→spec |600seconds |
| Synthetic PR cycle |600seconds |
| Breach→intent |120seconds |
| Intent survival among decided fixtures |1.0 |
| Fixture eval pass rate |1.0 |
| Gate wait |60seconds |
| Cost/success |0.20 fixture currency units; no actual cloud charge |
| Spec rework / repeat incidents / absent production inventory |null, unavailable—not zero |

These figures verify the calculator, not real delivery performance or model quality.

## Scratch instantiation

The test suite copies explicit Git-tracked template files plus ADD-0005 additions
into a disposable directory, without copying .git, home profiles, environments or
tool caches. It runs the real initializer with example-org fixture values, checks
the initialized repository, renders the spec and reruns the monitor there. The
fixture is removed by its temporary-directory owner after the test.

The initial full-snapshot check caught a missing worked-example link while this
file was being completed; verification is rerun after completion. Test outcomes
are reported for the checked state, not inferred from earlier runs.

## Not run

Native Windows or any of the three installed CLI/VSCode extensions; privileged
OS setup; live malicious test commands; cross-runtime model behavior; production
approval, isolated signing or v6 interoperability; GitHub workflow execution;
scratch-subscription what-if/deploy for A/B. See [activation findings](ACTIVATION.md).
