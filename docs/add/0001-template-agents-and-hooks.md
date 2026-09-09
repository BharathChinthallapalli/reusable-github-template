---
schema_version: 1
id: ADD-0001
status: ready
scope:
- .agents/skills/ai-evaluation/SKILL.md
- .agents/skills/ai-evaluation/assets/evaluation-plan.md
- .agents/skills/bounded-experiments/SKILL.md
- .agents/skills/bounded-experiments/assets/experiment-record.md
- .agents/skills/bounded-experiments/assets/trials.tsv
- .agents/skills/clean-code/SKILL.md
- .agents/skills/clean-code/references/design-decisions.md
- .agents/skills/clean-code/references/safe-changes.md
- .agents/skills/clean-code/references/sources.md
- .agents/skills/code-review/SKILL.md
- .agents/skills/code-review/references/findings.md
- .agents/skills/context-maintenance/SKILL.md
- .agents/skills/context-maintenance/assets/context-refresh.md
- .agents/skills/data-contracts/SKILL.md
- .agents/skills/data-contracts/assets/data-contract.md
- .agents/skills/dependency-maintenance/SKILL.md
- .agents/skills/dependency-maintenance/assets/upgrade-record.md
- .agents/skills/evidence-research/SKILL.md
- .agents/skills/evidence-research/assets/evidence-ledger.md
- .agents/skills/github-actions-debug/SKILL.md
- .agents/skills/github-actions-debug/references/diagnosis.md
- .agents/skills/implementation-planning/SKILL.md
- .agents/skills/implementation-planning/assets/change-plan.md
- .agents/skills/interface-validation/SKILL.md
- .agents/skills/interface-validation/assets/interface-cases.md
- .agents/skills/performance-analysis/SKILL.md
- .agents/skills/performance-analysis/assets/measurement-record.md
- .agents/skills/rag-development/SKILL.md
- .agents/skills/rag-development/assets/corpus-contract.md
- .agents/skills/release-delivery/SKILL.md
- .agents/skills/release-delivery/assets/release-record.md
- .agents/skills/release-notes/SKILL.md
- .agents/skills/release-notes/assets/release-changes.md
- .agents/skills/repo-discovery/SKILL.md
- .agents/skills/repo-discovery/references/evidence.md
- .agents/skills/security-review/SKILL.md
- .agents/skills/security-review/assets/threat-path-record.md
- .agents/skills/systematic-debugging/SKILL.md
- .agents/skills/systematic-debugging/assets/diagnosis-record.md
- .agents/skills/systematic-debugging/references/runtime-boundaries.md
- .agents/skills/task-orchestration/SKILL.md
- .agents/skills/task-orchestration/assets/task-handoff.md
- .agents/skills/test-design/SKILL.md
- .agents/skills/test-design/assets/behavior-case-matrix.md
- .agents/skills/test-design/references/persistence.md
- .agents/skills/tool-integration/SKILL.md
- .agents/skills/tool-integration/assets/boundary-contract.md
- .agents/skills/triage-issue/SKILL.md
- .agents/skills/triage-issue/assets/triage-record.md
- .agents/skills/verify-change/SKILL.md
- .agents/skills/verify-change/references/verification.md
- .agents/skills/write-adr/SKILL.md
- .agents/skills/write-adr/assets/decision-evidence.md
- .codex/hooks.json
- .github/agents/ai-engineer.agent.md
- .github/agents/architect.agent.md
- .github/agents/debugger.agent.md
- .github/agents/engineer.agent.md
- .github/agents/evaluator.agent.md
- .github/agents/release-engineer.agent.md
- .github/agents/researcher.agent.md
- .github/agents/reviewer.agent.md
- .github/agents/security-reviewer.agent.md
- .github/agents/test-engineer.agent.md
- .github/copilot-instructions.md
- .github/hooks/agent-checks.json
- .github/instructions/python.instructions.md
- .github/instructions/workflows.instructions.md
- .github/workflows/ci.yml
- .github/workflows/copilot-setup-steps.yml
- .gitignore
- .pre-commit-config.yaml
- AGENTS.md
- CLAUDE.md
- hooks/README.md
- hooks/agent_hooks.py
- hooks/prompts/release-notes.md
- hooks/prompts/triage-issue.md
- hooks/prompts/write-adr.md
- requirements-dev.txt
- ruff.toml
- tools/check_ai_configuration.py
- tools/check_design.py
- tools/install_hook_tools.py
adrs:
- docs/adr/0002-validate-ai-metadata.md
- docs/adr/0003-portable-git-checks.md
- docs/adr/0004-portable-engineering-capabilities.md
- docs/adr/0005-scoped-agent-design-gate.md
binding_sha256: 2ded516774e4568e7a4e5b7715c5d1c36462f2020e57a719082c0509cdc17160
---
# Template agents, design gate and local hooks

## Purpose

Deliver the requested reusable engineering template with architecture decisions
under `docs/adr`, Agent Design Documents under `docs/add`, operational runbooks,
pre-tool restrictions, post-edit Ruff and Gitleaks checks, and reusable triage,
ADR-writing and release-note prompts. Existing shared skills and agent profiles
supply the task workflow; this design makes their boundaries and the new local
checks explicit. The user's request authorizes implementation of this template
change. It does not supply an application's domain, cloud account or deployment
authorization.

## Scope and non-goals

The frontmatter enumerates the shared instructions, skill files and assets,
agent profiles, hook implementation and configuration, design checker, supporting
loader, dependency configuration and CI entrypoints actually bound by this
record. Root guidance routes users to the shared procedures and relevant current
ADRs. Host-specific configuration calls portable repository-owned checks through
adapters appropriate to that host's event format.

This scope is the current template revision, not standing permission for future
agent files. New protected paths must be added explicitly before editing them.
Routine application changes and unrelated documentation are outside this gate.
No application framework, model provider, business requirement, production
identity, paid service or deployment is selected here. Instructions do not start
background agents or prove that a client discovered its customizations.

## Inputs and outputs

The running agent consumes the user task, repository instructions, relevant
Accepted ADRs, the scoped ADD and evidence from affected files. It returns the
requested change with verification results and unresolved limitations. Specialist
handoffs identify scope, file ownership, findings and integration evidence.

The design CLI consumes Markdown records with safe YAML frontmatter and explicit
repository-relative paths. Planned-path checks return success only for valid
ready coverage of each affected protected path. The default delivery check also
compares SHA-256 bindings against the ADD narrative, metadata, scoped content
and referenced ADR content. It produces readable diagnostics and a nonzero
failure status. Explicit sealing writes one record's binding and preserves its
status; it does not write implementation files or execute their content.

Hook adapters consume their documented host event input, normalize supported
structured edit paths or shell command fields, and return that host's continuation
or blocking result. The portable policy rejects known secret-file access and
known destructive shell forms; post-edit tools report lint and secret findings.
The actual event fields, unsupported operations and setup commands must match
[the hook guide](../../hooks/README.md) and implementation after integration.

## Capabilities and permissions

The current task authorizes template implementation, the requested GitHub repository update,
current-source research and proportionate validation. Agent profiles inherit the running host's
model, permissions and available tools. They may use existing authorization for
reversible work and bounded independent delegation; they cannot grant themselves
access, impersonate a reviewer, deploy, publish or contact third parties merely
because a profile or ADD says ready.

Repository checks read local repository files. Their content is data, not
instructions to execute. The design checker rejects unsafe scope paths and
symlinks. The hook tool installer is an explicit setup operation for pinned
validation tools, separate from the hook event; hooks must not install software
or contact external services when evaluating an edit. The post-edit scanner operates on a local snapshot without excluded tool
caches. Git enumeration omits ignored untracked files. A ZIP has no Git ignore
selection and its fallback can scan local environment files; this is local,
redacted secret detection, not a promise that those files are outside coverage. Use synthetic secrets in tests.

## Behavior and failure modes

Before protected edits, inspect the design and referenced decisions and run
`python3 tools/check_design.py --paths` with the concrete affected paths.
Malformed metadata, incomplete ready sections, non-Accepted referenced decisions,
unsafe paths and missing or ambiguous ready coverage fail. Draft and retired
records do not cover work. A future path may be planned before creation.

During a multi-file change, the pre-edit check permits content drift so ordinary
implementation can proceed. Before delivery, reconcile the design, inspect the
diff, run relevant behavior checks, explicitly seal the affected ADD and run the
default gate. A changed file, changed design or changed referenced ADR makes the
previous delivery binding stale. Deleted files have a distinct absent state.
Failed sealing leaves the original record intact.

Pre-tool hooks reject inputs that violate their supported policy; malformed or
unsupported host payloads must not be reported as verified safe. Exact behavior
and error propagation are tested at the adapter boundary. Post-edit checks keep
lint and secret-scan outcomes distinct from permission decisions. No parser of
shell text can establish that all possible interpreters, indirect reads and
external tools are safe. Host permissions, sandboxing, review and independent
CI remain separate controls. A successful local hook does not prove remote
server rules are enabled.

## Validation

Run `python3 -m unittest discover -s tests -p test_design.py -v` for ready-path success, uncovered
future files, non-ready rejection, accepted-decision references, malformed YAML,
unsafe scope, explicit deletion state, failed-seal preservation and digest drift.
The success fixtures contain meaningful independent expected outcomes; they are
not model-performance evidence. Run the repository's hook unit and integration
lanes for actual adapter input, policy rejection, command handling, tool failure
propagation, and preservation of local environment files.

Run the repository foundation, AI metadata and catalog checks, then the full
repository tooling suite and relevant Git integration lane. Run Ruff and Gitleaks
through the checked setup to verify real tool invocation. Final default design
validation must pass after all scoped writers finish and the binding is recorded.
Host discovery, actual hosted lifecycle events, cloud deployments and application
quality are separate evidence; report any unexercised boundary explicitly.

## Risks and alternatives

Instructions alone cannot detect an unrelated design or stale delivered files.
A compulsory human approval for every small edit would add a new permission
requirement that the user's task did not request. Explicit file scope plus a
content binding exposes concrete drift without creating that approval process.
The maintenance cost is updating scope for new files and resealing protected
changes after review. It is deliberately broader than a syntax-only check.

A ready narrative and fingerprint do not authenticate an author or prove semantic
correctness. Someone with repository write access can modify checks or reseal
content. Reviewers must examine the behavior and scope; server rules are configured
separately where required. Shell deny rules are best effort, local clients expose
different hook events, and pinned validation tools need maintained upgrade tests.
Revisit this design when those event contracts change, false positives obstruct
authorized workflows, or a project requires signed approval rather than editable
design records.
