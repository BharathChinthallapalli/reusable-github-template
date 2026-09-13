# Kun adoption validation

Prepared 13 September 2026 for template 3.2.0, based on template commit
`93121920cf26c059aa90441e71da5c31c6851eff`. See the
[source review and implementation plan](kun-adoption.md) and
[accepted decision](../adr/0007-local-engineering-guidance.md).

This record covers the initial Kun adaptation at
`098348b77e5b4e24f3fc7d5348820be91717a866`, which added guidance and catalog
navigation without changing scanner policy, initializer inputs, dependencies or
CI configuration. The later [agent tooling follow-up](agent-tooling.md) records
the user's additional command defaults and Copilot setup changes separately.

## Environment and command evidence

Local environment: macOS 26.2, Python 3.12.11, Apple Git 2.39.5,
pre-commit 4.6.2, PyYAML 6.0.3, Ruff 0.16.6 and Gitleaks 8.30.1.
The development requirements were installed in a virtual environment, the pinned
scanner archive passed the shipped installer's checksum check, and pre-commit
prepared its configured hook environment. Commands ran from the source root
unless an initialized copy is specified.

| Check | Observed result and scope |
| --- | --- |
| `python tools/check_repository.py` | Passed foundation and local-link checks in source and initialized copies |
| `python tools/check_ai_configuration.py --json` | Passed; 34 skills and 13 agents; host discovery/invocation explicitly not checked |
| `python tools/ai_catalog.py --write`, followed by `python tools/ai_catalog.py` | Regenerated the catalog and passed freshness; existing catalog tests cover deterministic output and stale/invalid input |
| `python tools/check_design.py --paths ...`, `--seal docs/add/0001-template-agents-and-hooks.md`, then default mode | Planned paths accepted; affected design reconciled and bound; complete coverage/bindings passed in source and initialized copies |
| Skill-creator `quick_validate.py .agents/skills/context-maintenance` | Changed skill entrypoint passed format validation |
| `python hooks/agent_hooks.py --event session` and `--event check` | Passed using installed Ruff and Gitleaks, including eligible untracked working-tree files |
| `python -m pre_commit run --all-files` | Passed applicable tracked-file checks; file-type hooks with no eligible input reported skips |
| `python -m unittest discover -s tests -v`, default macOS temporary directory | 134 of 136 tests passed, with the same two path-alias failures as the base commit; details below |
| `TMPDIR=/private/tmp python -m unittest discover -s tests -v`, interpreter path without spaces | All 136 passed in source and initialized copies; this canonical-path environment does not fix macOS aliases |
| `REQUIRE_AGENT_HOOK_TOOLS=1 python -m unittest discover -s tests/integration -v` | 22 cases: 21 passed, one filesystem case-collision case skipped on this case-insensitive volume. All seven real-scanner cases ran and passed |
| Evaluation report CLI with shipped passing/incomplete examples and a nonexistent path | JSON statuses and exit codes matched: passed/0, inconclusive/1, invalid/2. These are synthetic report checks, not model evaluations |

The tool guide was checked against actual CLI parsers/help, owning scripts and
the commands above. Setup and write behavior also have the existing initializer,
catalog, design and installer unit cases. No new wording-matching tests or
runtime interfaces were added for this documentation change.

## Disposable initialization

A separate copy of deliverable files used synthetic project values for
`example-org/catalog-service`. The initializer preview changed no content;
`--write` changed exactly `.github/CODEOWNERS`, `README.md`, `SECURITY.md`,
`SUPPORT.md`, `docs/project.md` and `template.json`. Repeating identical arguments
preserved all deliverable bytes. The initialized metadata retained version 3.2.0,
and foundation, metadata, catalog and bound-design checks passed. The shared
source remains uninitialized.

## Independent guidance exercises

A fresh agent read the revised local references and applied them to four
synthetic requests. It received task facts without an expected-answer rubric and
followed relevant existing skills. These were forward responses and a completed
synthetic context record, not application implementation or native host tests.

| Task | Observed behavior |
| --- | --- |
| Already-authorized CSV feature preserving JSON and existing files | Began at the missing application boundary, requested actual entrypoints instead of inventing template code, and selected consumer-level quoting and preservation checks without another approval cycle |
| Export error with a missing parent followed by cleanup failure | Treated the first error as a hypothesis to reproduce, inspected path ownership before choosing directory creation, preserved primary-error evidence, and added run/SHA/job evidence for the Actions variant |
| Behavior-preserving export refactor with an overwrite-coverage gap | Reused sufficient JSON/quoting checks, derived an existing-file assertion from the actual contract, and separated any newly requested behavior from the refactor |
| SDK workaround repeated across guidance with distinct payment/catalog ADRs | Consolidated at a canonical runbook, limited supersession to the tested SDK path, retained distinct ADR scopes, kept a delivery-only preference temporary, and preserved unfinished migration/publication work |

No remaining guidance defect was identified in these bounded exercises. They
have no baseline comparison or measured quality improvement; the scenario facts
themselves constrain the responses. The agent ran the foundation checker but did
not execute an export application, SDK migration, external tool or publication.
Source research and the final raw-diff review are separate from these exercises.
The final independent review inspected the changed and new files against the
requested four adaptations and checked documented CLI contracts against source.
It reported no actionable findings; that review did not execute tests itself.

## Existing platform failures

Before implementation, the 136-test offline suite on macOS passed 134 tests and
failed two in `tests/test_agent_hooks.py`: absolute editor paths through the
system temporary directory were rejected, and a changed-file assertion compared
an unresolved temporary path with its resolved equivalent. macOS exposes `/var`
and `/tmp` as symlink aliases of `/private/var` and `/private/tmp`. The first
failure also reproduced with an absolute `/tmp` editor path outside the test.

These failures existed on the base commit. This guidance change does not alter
hook path policy or tests. A canonical-path rerun, if recorded, establishes only
that narrower environment; it does not repair alias handling. Linux CI is a
separate check and must be matched to the delivered revision.

An initial unit invocation used an interpreter inside a directory containing a
space. Test fixtures embed `sys.executable` directly in an executable shebang;
that produced scanner-unavailable failures. Rerunning with the same Python
version at a path without spaces reduced the result to the two established
alias failures above. No assertion, scanner policy or test source was changed.

## Delivery and limits

Match GitHub's `Repository checks` job to the delivered PR revision. Local
integration exercised macOS; Linux CI supplies separate platform evidence. No
Windows execution, native Copilot/VS Code/Codex discovery or live hook invocation
was performed. Passing static checks does not establish those capabilities.

The user authorized implementation and GitHub publication. Delivery uses a
feature branch and pull request in the existing repository. No main-branch
merge, live ruleset change, access grant, license selection, release tag, external
model service or scheduled job is part of this update.
