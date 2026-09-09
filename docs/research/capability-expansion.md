# Capability expansion and research coverage

The template now maps **all 32 reusable improvement families** to shipped procedures,
references, records or repository tooling. The actual inventory is **21 shared skills
and 10 agent profiles**. Multiple families deliberately share a procedure; the count
of profiles is not a measure of readiness. The [machine-readable map](capability-expansion.json)
retains every family ID, source URL, execution boundary and repository-root-relative
artifact path. The [generated catalog](../ai-catalog.md) lists the actual skills and agents.

## What the research establishes

The [source review](repository-review.md) inventories **494 public account repositories**
and records selected source reviews of **23 account repositories plus two additional
AI targets**. It does not claim an every-file code audit. The account coverage is:

| Account | Metadata inventory | Overview reading | Selected source review |
| --- | ---: | --- | --- |
| [bcherny](https://github.com/bcherny) | 271 | 232 nonempty root READMEs and 30 alternative primary files; one blank site and eight empty repositories. Reading usually covers opening passages. | 7 repositories, 41 files |
| [karpathy](https://github.com/karpathy) | 63 | 63 primary overviews: 52 complete, five prose without code blocks, six selected sections | 8 repositories, 36 files |
| [johnpapa](https://github.com/johnpapa) | 160 | 155 README introductions/headings; three repositories without a root README and two empty repositories | 8 repositories, 45 non-README files |

For bcherny, the mutually exclusive tiers are 227 overview, 28 alternative primary
file, seven detailed samples, one directory-only and eight empty metadata-only.
Detailed samples overlap the README/alternative-file retrieval counts above; do not
add those overlapping counts to estimate a larger population.

The two AI targets are [AI Engineering Hub](https://github.com/patchy631/ai-engineering-hub/tree/2c9b106168d4540b88e727e4aa316c06c856c2b7)
and [Made With ML](https://github.com/GokuMohandas/Made-With-ML/tree/3361aeb8ddfc2affdba9f545c978c38c85cee764).
Their [file-level record](repository-inventory/ai-repositories-coverage.json) distinguishes
complete text retrieval, partial lockfile reading, sampled CSV rows and selected notebook
cells. Most independent hub demos and large/binary assets were not inspected.

A focused follow-up inspected only the [running-agent README](https://github.com/johnpapa/running-agent/blob/0673b9111746838c110855419f21153bcaa51166/README.md)
and [AGENTS.md](https://github.com/johnpapa/running-agent/blob/0673b9111746838c110855419f21153bcaa51166/AGENTS.md)
at revision `0673b9111746838c110855419f21153bcaa51166`. This adds UI instruction evidence,
not an application-source or browser-execution claim, and is recorded separately from
the original 23 account source samples. Changed-flow browser, responsive and accessibility
evidence was adapted; hard-coded counts and full-suite execution after every interaction
were not adopted.

Enumeration used empty-page termination: bcherny `100/100/71/0`, karpathy `63/0`,
and johnpapa `100/60/0/0`. These are all unique records returned by the connector;
its API did not expose `total_count` or `incomplete_results`. Index omissions,
private/hidden/deleted repositories and non-atomic retrieval remain limits.
No upstream code was executed, dependencies installed, upstream CI verified or service
deployed by those source reviews. Default-branch links remain mutable; recorded blob
hashes identify file content, not commits. The original [coverage records](repository-review.md)
and per-family source URLs in the JSON preserve that distinction.

## Shipped coverage

**Bundled** means the procedure, reference, routing or repository tooling is present.
**Project-configured execution (procedure shipped)** means the procedure is also present,
while actual application/provider/storage/browser/deployment execution uses the adopted
project's configuration and the task's authorization. Neither status claims host activation
or an already completed integration. All artifact links below refer to shipped paths.

| Family | Status | Shipped procedure and evidence surface |
| --- | --- | --- |
| Evidence-first research and coverage accounting | bundled | Record coverage, revisions, observations, inference and adoption decisions. [evidence-research](../../.agents/skills/evidence-research/SKILL.md); [evidence-ledger.md](../../.agents/skills/evidence-research/assets/evidence-ledger.md); [researcher.agent.md](../../.github/agents/researcher.agent.md) |
| Acceptance-led planning and multiple independent challenges | bundled | Compare feasible alternatives, challenge concrete failures, resolve findings and stop at sufficient acceptance evidence. [implementation-planning](../../.agents/skills/implementation-planning/SKILL.md); [change-plan.md](../../.agents/skills/implementation-planning/assets/change-plan.md); [architect.agent.md](../../.github/agents/architect.agent.md) |
| Bounded specialist delegation and independent synthesis | bundled | Partition independent work, assign one writer per shared area and integrate evidence-bearing handoffs. [task-orchestration](../../.agents/skills/task-orchestration/SKILL.md); [task-handoff.md](../../.agents/skills/task-orchestration/assets/task-handoff.md); [engineer.agent.md](../../.github/agents/engineer.agent.md) |
| Living project context and instruction drift repair | bundled | Refresh facts and handoffs from current commands, code and accepted decisions; preserve unfinished work. [context-maintenance](../../.agents/skills/context-maintenance/SKILL.md); [context-refresh.md](../../.agents/skills/context-maintenance/assets/context-refresh.md); [project.md](../../docs/project.md); [README.md](../../docs/decisions/README.md) |
| Repository-aware environment setup | bundled | Combine repository discovery, maintained setup commands and the Copilot setup workflow. [repo-discovery](../../.agents/skills/repo-discovery/SKILL.md); [context-maintenance](../../.agents/skills/context-maintenance/SKILL.md); [copilot-setup-steps.yml](../../.github/workflows/copilot-setup-steps.yml); [using-the-template.md](../../docs/using-the-template.md) |
| Monorepo, collection, docs, notebook and package classification | bundled | Classify applications, example collections, workspaces, notebooks, courses, generators and documentation from concrete evidence. [repo-discovery](../../.agents/skills/repo-discovery/SKILL.md); [evidence.md](../../.agents/skills/repo-discovery/references/evidence.md) |
| Independent behavior oracles and test design | bundled | Select regression, boundary and consumer cases with independent expectations and nonzero failure propagation. [test-design](../../.agents/skills/test-design/SKILL.md); [behavior-case-matrix.md](../../.agents/skills/test-design/assets/behavior-case-matrix.md); [test-engineer.agent.md](../../.github/agents/test-engineer.agent.md) |
| Real host, process, browser and transport boundary tests | project-configured execution (procedure shipped) | Record process, remote workspace, host, transport and consumer identity; distinguish simulated from actual execution. [runtime-boundaries.md](../../.agents/skills/systematic-debugging/references/runtime-boundaries.md); [persistence.md](../../.agents/skills/test-design/references/persistence.md); [interface-validation](../../.agents/skills/interface-validation/SKILL.md); [ai-assistance.md](../../docs/ai-assistance.md) |
| Hypothesis-led failure reproduction and repair | bundled | Trace the first causal error, compare hypotheses and choose the smallest discriminating experiment. [systematic-debugging](../../.agents/skills/systematic-debugging/SKILL.md); [diagnosis-record.md](../../.agents/skills/systematic-debugging/assets/diagnosis-record.md); [runtime-boundaries.md](../../.agents/skills/systematic-debugging/references/runtime-boundaries.md); [debugger.agent.md](../../.github/agents/debugger.agent.md) |
| Machine-readable evaluation contracts and honest outcomes | project-configured execution (procedure shipped) | Define versioned cases, outcomes and acceptance; provide an offline JSON report gate and negative-case tests. [ai-evaluation](../../.agents/skills/ai-evaluation/SKILL.md); [evaluation-plan.md](../../.agents/skills/ai-evaluation/assets/evaluation-plan.md); [evaluation-reports.md](../../docs/evaluation-reports.md); [check_evaluation.py](../../tools/check_evaluation.py); [test_evaluation.py](../../tests/test_evaluation.py); [ai-engineer.agent.md](../../.github/agents/ai-engineer.agent.md) |
| Bounded reproducible experimentation and optimization | project-configured execution (procedure shipped) | Freeze a baseline and evaluator, bound attempts and resources, preserve rejected trials and retain only verified improvements. [bounded-experiments](../../.agents/skills/bounded-experiments/SKILL.md); [experiment-record.md](../../.agents/skills/bounded-experiments/assets/experiment-record.md); [trials.tsv](../../.agents/skills/bounded-experiments/assets/trials.tsv) |
| Retrieval engineering and evidence-grounded answers | project-configured execution (procedure shipped) | Trace ingestion, identities, access filtering, retrieval, citations, updates and answer support. [rag-development](../../.agents/skills/rag-development/SKILL.md); [corpus-contract.md](../../.agents/skills/rag-development/assets/corpus-contract.md); [ai-evaluation](../../.agents/skills/ai-evaluation/SKILL.md) |
| Data validation, splits and lineage | project-configured execution (procedure shipped) | Record schema, provenance, transformations, partitions, rejected records and consumer impact. [data-contracts](../../.agents/skills/data-contracts/SKILL.md); [data-contract.md](../../.agents/skills/data-contracts/assets/data-contract.md); [corpus-contract.md](../../.agents/skills/rag-development/assets/corpus-contract.md) |
| Model, prompt, evaluator and serving consistency | project-configured execution (procedure shipped) | Tie effective model, prompt, evaluator, data transformation and delivered artifact identities to the comparison and consumer contract. [ai-evaluation](../../.agents/skills/ai-evaluation/SKILL.md); [data-contracts](../../.agents/skills/data-contracts/SKILL.md); [boundary-contract.md](../../.agents/skills/tool-integration/assets/boundary-contract.md); [release-delivery](../../.agents/skills/release-delivery/SKILL.md); [ai-engineer.agent.md](../../.github/agents/ai-engineer.agent.md) |
| Tool schemas, MCP protocol and integration validation | project-configured execution (procedure shipped) | Define schemas, identity, side effects, machine-distinguishable failures, retries and transport checks, including protocol-only stdio stdout. [tool-integration](../../.agents/skills/tool-integration/SKILL.md); [boundary-contract.md](../../.agents/skills/tool-integration/assets/boundary-contract.md) |
| Actual provider and external data-flow accounting | project-configured execution (procedure shipped) | Record effective inference, embedding, memory, search, evaluation and telemetry destinations separately. [boundary-contract.md](../../.agents/skills/tool-integration/assets/boundary-contract.md); [rag-development](../../.agents/skills/rag-development/SKILL.md); [security-review](../../.agents/skills/security-review/SKILL.md); [security-reviewer.agent.md](../../.github/agents/security-reviewer.agent.md) |
| Trust boundaries, secrets and denied-operation validation | bundled | Trace concrete trust boundaries and verify denied operations without unintended state changes. [security-review](../../.agents/skills/security-review/SKILL.md); [threat-path-record.md](../../.agents/skills/security-review/assets/threat-path-record.md); [security-reviewer.agent.md](../../.github/agents/security-reviewer.agent.md); [threat-model.md](../../docs/threat-model.md) |
| Timeout, retry, idempotency, cache and lifecycle failure contracts | project-configured execution (procedure shipped) | Select bounded retry, idempotency, cancellation, partial-result, recovery and cache/lifecycle checks for the actual failing boundary. [runtime-boundaries.md](../../.agents/skills/systematic-debugging/references/runtime-boundaries.md); [boundary-contract.md](../../.agents/skills/tool-integration/assets/boundary-contract.md); [operations.md](../../docs/operations.md) |
| Structured outcomes, correlation and diagnostic evidence | project-configured execution (procedure shipped) | Correlate operations and artifact versions; preserve useful redacted diagnostics and separate errors from quality and resource measurements. [runtime-boundaries.md](../../.agents/skills/systematic-debugging/references/runtime-boundaries.md); [boundary-contract.md](../../.agents/skills/tool-integration/assets/boundary-contract.md); [measurement-record.md](../../.agents/skills/performance-analysis/assets/measurement-record.md); [evaluation-reports.md](../../docs/evaluation-reports.md) |
| Validate generated and distributed consumer artifacts | project-configured execution (procedure shipped) | Inspect distributed contents, bind artifact identity and verify the built output through its consumer. [release-delivery](../../.agents/skills/release-delivery/SKILL.md); [release-record.md](../../.agents/skills/release-delivery/assets/release-record.md); [persistence.md](../../.agents/skills/test-design/references/persistence.md); [release-engineer.agent.md](../../.github/agents/release-engineer.agent.md) |
| Verification-bound release and rollback | project-configured execution (procedure shipped) | Promote the evaluated artifact, retain recovery identity and report prepared, published, deployed and healthy separately. [release-delivery](../../.agents/skills/release-delivery/SKILL.md); [release-record.md](../../.agents/skills/release-delivery/assets/release-record.md); [operations.md](../../docs/operations.md) |
| Dependency/runtime upgrade and compatibility maintenance | bundled | Assess release notes, compatibility, resolved dependencies, consumer behavior and rollback for focused upgrades. [dependency-maintenance](../../.agents/skills/dependency-maintenance/SKILL.md); [upgrade-record.md](../../.agents/skills/dependency-maintenance/assets/upgrade-record.md); [maintenance.md](../../docs/maintenance.md); [dependabot.yml](../../.github/dependabot.yml) |
| Intentional CI matrix and machine-detectable gates | bundled | Wire static metadata/catalog checks and offline report-tool tests into machine-detectable gates while retaining the Repository checks contract. [ci.yml](../../.github/workflows/ci.yml); [copilot-setup-steps.yml](../../.github/workflows/copilot-setup-steps.yml); [check_ai_configuration.py](../../tools/check_ai_configuration.py); [check_evaluation.py](../../tools/check_evaluation.py); [test_ai_configuration.py](../../tests/test_ai_configuration.py); [test_evaluation.py](../../tests/test_evaluation.py); [extending-ci.md](../../docs/extending-ci.md) |
| Developer documentation and interface maintenance | bundled | Keep source, command, decision and documentation relationships aligned in the existing context workflow. [context-maintenance](../../.agents/skills/context-maintenance/SKILL.md); [maintenance.md](../../docs/maintenance.md); [project.md](../../docs/project.md) |
| Responsive and accessible UI verification | project-configured execution (procedure shipped) | Verify changed flows, states, keyboard/focus, labels and relevant responsive views with explicit evidence limits. [interface-validation](../../.agents/skills/interface-validation/SKILL.md); [interface-cases.md](../../.agents/skills/interface-validation/assets/interface-cases.md); [test-engineer.agent.md](../../.github/agents/test-engineer.agent.md) |
| Measure before optimizing and preserve workload equivalence | project-configured execution (procedure shipped) | Measure comparable workloads with explicit units, included work, repetitions, failures and correctness constraints. [performance-analysis](../../.agents/skills/performance-analysis/SKILL.md); [measurement-record.md](../../.agents/skills/performance-analysis/assets/measurement-record.md); [bounded-experiments](../../.agents/skills/bounded-experiments/SKILL.md) |
| Persistence, atomic publication and recovery contracts | project-configured execution (procedure shipped) | Test save/load, version compatibility, partial writes, publication visibility, crash promises and concurrent-writer contracts. [persistence.md](../../.agents/skills/test-design/references/persistence.md); [behavior-case-matrix.md](../../.agents/skills/test-design/assets/behavior-case-matrix.md); [data-contracts](../../.agents/skills/data-contracts/SKILL.md) |
| Cohesive reusable logic and explicit side effects | bundled | Retain cohesive logic, explicit side effects, consumer contracts and evidence-based extraction across module, notebook and generated boundaries. [clean-code](../../.agents/skills/clean-code/SKILL.md); [safe-changes.md](../../.agents/skills/clean-code/references/safe-changes.md); [design-decisions.md](../../.agents/skills/clean-code/references/design-decisions.md); [evidence.md](../../.agents/skills/repo-discovery/references/evidence.md) |
| Discoverable capability catalog with semantic checks | bundled | Generate the capability catalog from real metadata, validate definitions and reject stale catalog output. [AGENTS.md](../../AGENTS.md); [ai_catalog.py](../../tools/ai_catalog.py); [check_ai_configuration.py](../../tools/check_ai_configuration.py); [test_ai_catalog.py](../../tests/test_ai_catalog.py); [ai-catalog.md](../../docs/ai-catalog.md) |
| Repository guidance across supported coding hosts | bundled | Keep one canonical skill directory, thin host pointers and a documented host discovery/invocation check. [AGENTS.md](../../AGENTS.md); [CLAUDE.md](../../CLAUDE.md); [copilot-instructions.md](../../.github/copilot-instructions.md); [ai-assistance.md](../../docs/ai-assistance.md); [copilot-setup-steps.yml](../../.github/workflows/copilot-setup-steps.yml) |
| Troubleshooting feedback into maintained practices | bundled | Turn reproduced failures and confirmed corrections into maintained context, runbooks and decision-aware guidance. [evidence-research](../../.agents/skills/evidence-research/SKILL.md); [systematic-debugging](../../.agents/skills/systematic-debugging/SKILL.md); [context-maintenance](../../.agents/skills/context-maintenance/SKILL.md); [troubleshooting.md](../../docs/troubleshooting.md) |
| Progressive examples and repository tours | bundled | Provide task prompts and progressive repository tours linked to the relevant working procedures. [working-with-agents.md](../../docs/working-with-agents.md); [ai-catalog.md](../../docs/ai-catalog.md); [using-the-template.md](../../docs/using-the-template.md); [repo-discovery](../../.agents/skills/repo-discovery/SKILL.md) |

Every original source URL is retained under its family in the
[JSON evidence map](capability-expansion.json). The map also retains deliberate exclusions,
such as framework-specific defaults, infinite experiments, inferred privacy guarantees
and automatic publication. Those exclusions do not remove the reusable procedure.

## Why responsibilities share a home

- Architect owns material planning; engineer owns coordination. A separate planner profile would duplicate those responsibilities.
- Context maintenance covers documentation and handoffs; discovery plus maintained setup handles onboarding. Separate prose-only roles would multiply sources of truth.
- Debugging and tool integration share resilience/observability references; test design owns persistence. These are boundary-specific procedures, not independent always-running services.
- AI engineer routes evaluation, retrieval, data, model and tool work to focused skills. Model/prompt identity and serving checks use those contracts plus release delivery.
- Researcher, test engineer, AI engineer and release engineer provide distinct work products, with evaluator providing independent comparison alongside reviewer, debugger, security reviewer, architect and engineer.
- Performance retains a dedicated measurement procedure because comparable workload and metric semantics require explicit treatment; multiple agent names or agreement are not acceptance evidence.

New standalone names suggested during research are not treated as shipped files.
The table and manifest use actual repository paths: planning is
`implementation-planning`, debugging is `systematic-debugging`, retrieval is
`rag-development`, tool/MCP work is `tool-integration`, dependency work is
`dependency-maintenance`, and interface work is `interface-validation`. Documentation,
onboarding, resilience and model consistency are covered through the linked procedures
and records rather than duplicate profiles.

## Bounded design challenges

The following dispositions explain the design. They are not a claim that every host,
provider or application test has run.

| Lens | Concrete challenge | Disposition |
| --- | --- | --- |
| User outcome | Does the expansion support a concrete request or merely increase the number of profiles? | Map all 32 families to a working procedure/artifact, route by the actual task, and preserve direct execution when no custom agent is selected. |
| Evidence | Could overview inventory, a mutable source link or a static pass be mistaken for verified implementation behavior? | Retain source tiers/revisions, independent oracles and explicit unrun/inconclusive states; keep upstream inspection separate from local and host execution. |
| Runtime | Would a neutral template silently select providers, publish artifacts or require unavailable infrastructure? | Ship executable local metadata/report tools and reusable integration procedures; actual external execution uses the adopted project and existing authorization. |
| Maintainability | Would separate agents for every family duplicate instructions and drift? | Use 21 canonical skills and 10 agent profiles, merge overlapping roles, link focused references and generate the catalog from real metadata. |
| Integration | Could parallel file edits, stale output identity or a failing dependency be hidden by a successful summary? | Give shared files one writer, inspect actual handoffs, bind checks to the combined artifact and require machine-detectable failure paths. |

The stopping rule is to resolve a finding through a plan change, acceptance evidence
or a bounded remaining limit. Reopen for a new finding, changed requirement or failed
gate; do not create an endless debate or a mandatory specialist chain for routine work.

## Verification boundaries

The map checks coverage and file identity. Repository metadata validation and catalog
freshness establish static consistency. The offline evaluation checker validates submitted
report structure and its declared gate; it does not execute a model or authenticate the
reported evidence. Source inspection, local substitutes, real consumer execution, host
discovery and observed invocation remain distinct evidence levels.

Actual check results belong in [validation](../../VALIDATION.md); host setup and smoke
records belong in [AI assistance](../ai-assistance.md), and task examples in
[working with agents](../working-with-agents.md). Adoption and migration use the
[template setup guide](../using-the-template.md); application gates use the
[CI extension guide](../extending-ci.md). A reusable procedure is available immediately,
but successful project execution must still be demonstrated against the relevant runtime.
