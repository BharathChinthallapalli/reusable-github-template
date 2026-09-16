# AI-native SDLC

This is a **local, proposal-only foundation**, not an activated autonomous delivery
service. Follow the [canonical playbook](https://academy.claude.com/courses/ai-native-sdlc-playbook/introduction).
The [reading log](../.guardian/READING-LOG.md), [drift decisions](DRIFT.md) and
[activation findings](sdlc/ACTIVATION.md) describe its actual scope.

## One loop, six stages

| Stage | Traditional SDLC mapping | Committed contract | Required gate / current implementation |
| --- | --- | --- | --- |
| 1 Plan | Planning | intent/change/intent.md and decision | Product-owner acceptance from an authenticated channel; local metadata cannot provide it |
| 2 Design | Requirements analysis + design | requirements.md, design.md, rendered spec.md; data cards | EARS, compliance, archetype sections, references and concerns validated locally; human spec review still required |
| 3 Build | Development | tasks.md, requirement IDs, dependencies, waves | Seven structural DoR signals; semantic review and authenticated acceptance before dispatch |
| 4 Test | Testing | Tests, evals, calibrated thresholds, incident regressions | Existing CI discovers tests/test_sdlc.py; application/eval profiles are project-specific |
| 5 Deploy | Deployment | Reviewed diff, independent review evidence, rollback | CI and human authorization; no release or signing service activated by this slice |
| 6 Maintain | Maintenance | bands, findings, incidents, follow-up intents | Deterministic monitor emits proposals only; no automated runbook execution |

IBM's seven-phase terminology is mapped here; AWS groups six phases. The Kiro
triad is retained, with explicit playbook reviews even where a Quick Spec flow
would omit them. Product-owner acceptance and technical/policy reviews cannot be
replaced by an agent's confidence score.

## Local commands

Run from the repository using the prepared Python 3.12+ environment. Read the
scripts and applicable Guardian requirements first; these commands read project
files and may therefore require a Guardian token in configured hosts.

```text
python scripts/spec-check.py monitor-smoke
python scripts/spec-check.py monitor-smoke --render
python scripts/dor-check.py monitor-smoke
python scripts/monitor.py docs/sdlc/fixtures/samples.json --now 2026-09-16T10:01:00Z
python scripts/metrics.py docs/sdlc/fixtures/events.json
python -m unittest discover -s tests -p test_sdlc.py -v
```

Rendering and monitoring print to stdout. They do not write a spec, accept an
intent, post an issue, dispatch an agent, merge, deploy or grant permission.
`STRUCTURALLY_READY` is distinct from `authorization: UNVERIFIED`; do not use
exit code zero alone as a privileged dispatch decision.

## Artifact contracts

Copy the templates in intent/_template and specs/_template. Frontmatter is
**strict JSON inside YAML delimiters**, intentionally a narrow YAML subset:
no aliases, implicit dates, duplicate keys, unknown fields or non-finite numbers.
The input limit is 512 KiB per file. Change IDs are lowercase hyphenated slugs.
References are explicit workspace-relative files; links, junctions, traversal,
private paths and credential/mail file extensions are rejected.

Requirements contain IDs, user stories, EARS criteria and existing test/eval
references. Tasks contain IDs, requirement IDs, declared file surfaces, done
states, verification and dependencies in strictly earlier waves. These checks
prove structural traceability, not that a cited test exercises its requirement.
Review that semantic relationship before accepting the spec.

Every selected archetype must supply its headings. Multi-agent D projects should
also declare C when they need the single-model/RAG profile. For C/D/E the shared
AI supply-chain, threat, governance, evaluation and oversight sections are mandatory.
N/A compliance requires a reason and owner; unresolved assessments block rendering.

## Authority boundary

A trusted dispatcher must obtain acceptance and source provenance independently
of contributor files, bind it to repository, issue/task revision, specification
digest, PR head/base, policy version and authorized action, and enforce expiry
and replay protection. None of those controls can be supplied by a forged
`source: monitor`, `status: accepted`, reviewer name or workflow filename.

The caller-only monitor/spec shortcut keeps DoR gates 2/3/7 and records 1/4/5/6 as
SKIPPED, not PASS. No shipped CLI supplies authenticated source identity, so
ordinary DoR invocation evaluates all seven signals. Structural readiness never
permits implementation on its own.

Guardian remains the existing command enforcement layer. This foundation adds
no tools to agents and never turns an SDLC report into a Guardian approval.

## Institutional standards and operating loops

Existing .agents/skills remain canonical; do not duplicate them into a new root
and allow them to drift. See the existing security, data-contracts, ai-evaluation,
operational-readiness and Azure skills. Additional SDLC standard guidance is
linked from the profiles and compliance matrix. Research-only subagents retain
their existing tools; coding work belongs to separately authorized sessions.

The [automation prompts](sdlc/automations/spec-job.md) describe the intended
headless interfaces. They are not scheduled services. Every unsupported
integration is an open finding, never a silent fallback to an unconstrained shell.
