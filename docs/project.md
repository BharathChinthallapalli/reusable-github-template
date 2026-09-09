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

## Architecture

Document actual entrypoints, modules, data stores, trust boundaries, and
external services. Link to code and decisions. Add a diagram when relationships
are clearer visually; do not draw services that have not been selected.

## Commands

| Task | Current command |
| --- | --- |
| Repository validation | `python3 tools/check_repository.py` |
| Repository tooling tests | `python3 -m unittest discover -s tests -v` |
| Application install, run, lint, typecheck, test, build | Record verified commands after adding the application |

Record runtime versions, package manager, lockfile, required configuration names,
and safe sample values. Never document real secrets. Keep commands aligned with CI.

## Operational constraints

Record permissions, data location, retention, latency, availability, cost limits,
and support ownership when these are known. Link to [operations](operations.md)
and the [threat model](threat-model.md). Mark assumptions explicitly.
