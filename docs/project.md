# Project context

| Field | Value |
| --- | --- |
| Name | @@PROJECT_NAME@@ |
| Repository | @@GITHUB_OWNER@@/@@PROJECT_SLUG@@ |
| Purpose | @@PROJECT_DESCRIPTION@@ |
| Maintainer | @@CODEOWNER@@ |
| Security contact | [Private reporting](@@SECURITY_CONTACT@@) |
| Application stack | Not selected |
| Hosting and environments | Not selected |
| Data classification | To be determined by the project owner |
| License decision | Not selected; see docs/licensing.md |

## Users and outcome

Record the intended users, the task they need to complete, how success is
observed, and what is outside scope. Replace this guidance with real facts.

For each agreed outcome, record an input or starting condition, the observable
result, and how to verify it. Include relevant failure behavior. A completed
file, passing build, or generated screen alone does not establish user success.

## Domain terms

Define terms whose meaning affects behavior or naming. State their scope and
source; different domains may use the same word differently. Leave unknown
meanings unresolved rather than inventing a shared definition.

| Term | Meaning and scope | Source or owner |
| --- | --- | --- |
| Not yet defined | Add terms when the application domain is known | Not yet confirmed |

## Architecture

Document actual entrypoints, modules, data stores, trust boundaries, and
external services. Link to code and decisions. Add a diagram when relationships
are clearer visually; do not draw services that have not been selected.

For each relevant module, link its public contract: inputs, outputs, invariants,
failure behavior, side effects, and the behavioral checks that cover it. Show
what callers need to know; avoid duplicating implementation details. The
[decision index](decisions/README.md) helps locate rationale and current status.

## Commands

| Task | Current command |
| --- | --- |
| Validation dependency setup | `python3 -m pip install -r requirements-dev.txt` in [the prepared environment](using-the-template.md) |
| Repository validation | `python3 tools/check_repository.py` |
| Static agent and skill diagnostics | `python3 tools/check_ai_configuration.py` |
| Check capability catalog freshness | `python3 tools/ai_catalog.py` |
| Regenerate catalog after changing metadata | `python3 tools/ai_catalog.py --write` |
| Gate a project AI evaluation report | `python3 tools/check_evaluation.py path/to/report.json` using [the report contract](evaluation-reports.md) |
| Activate commit checks per clone | `python3 -m pre_commit install` after [hook preflight](git-hooks.md) |
| Check all tracked working-tree files | `python3 -m pre_commit run --all-files` |
| Repository tooling tests | `python3 -m unittest discover -s tests -v` |
| Git hook integration tests | `python3 -m unittest discover -s tests/integration -v` |
| Application install, run, lint, typecheck, test, build | Record verified commands after adding the application |

Record runtime versions, package manager, lockfile, required configuration names,
and safe sample values. Never document real secrets. Keep commands aligned with CI.

For an AI application, record its project-owned evaluation command and complete
the relevant [evaluation contract](ai-evaluation.md). Model quality, data contracts,
ordinary code checks and host discovery need separate evidence.

## Operational constraints

Record constraints as observed facts, agreed requirements, or unverified
assumptions. Attach a source, owner, or measurement and date. Do not invent
traffic forecasts, service targets, or budgets to fill the table.

| Constraint | Current evidence |
| --- | --- |
| Workload and access patterns: frequency, payload sizes, concurrency, reads/writes | Unknown until the application is defined |
| Permissions, data location, and retention | Not yet confirmed |
| Latency and availability requirements | Not yet agreed |
| Cost limit and support ownership | Not yet agreed |

Before changing the architecture for capacity or reliability, identify the
demonstrated bottleneck or required capability and the check that would show an
improvement. Link to [operations](operations.md) and the
[threat model](threat-model.md) for details relevant to the project.
