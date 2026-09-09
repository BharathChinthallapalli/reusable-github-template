# Validation record

Template version: 2.0.0. Prepared 9 September 2026.

## Results and scope

- Linux, Python 3.12.14 and Git 2.51.1; pre-commit 4.6.2, PyYAML 6.0.3.
- All **80 offline tooling tests** passed in both the uninitialized source and an initialized disposable project. The lane includes 16 evaluation-report CLI tests and 10 catalog CLI tests, alongside metadata, foundation and initializer tests.
- All **15 real Git integration tests** passed with no skips or failures. The warm-cache lane completed in 9.552 seconds. The existing ten checks still cover staged-content behavior, malformed files, synthetic private-key markers, path edge cases, hook collisions, bypass detection in a clean clone and the documented LFS exception.
- Foundation checks, static diagnostics for **21 skills and 10 agents**, catalog freshness and all-files hook scans passed in both source and initialized copies. All 21 skill entrypoints also passed the skill format validator.
- Initialization preview changed no deliverable; writing customized exactly six declared files; repeating identical inputs preserved every deliverable byte.
- Independent forward exercises produced a feature plan, bounded delegation, independently derived regression cases, a first-cause diagnosis and an AI selection decision. A separate implementation review challenged code, host claims and coverage, including 625 evaluation outcome combinations. See [capability validation](docs/research/capability-validation.md) for inputs, outcomes, findings and limits.

Tests use synthetic fixtures and disposable repositories. No actual credential
or model/provider call was needed. Hook revisions and dependencies retain the
version 1.3 pins; source/top-level pins do not lock the entire transitive closure.
Native Windows/macOS execution and editor discovery/invocation were not performed.

## Commands

In [the prepared environment](docs/using-the-template.md), from a Git checkout:

```bash
python -m pre_commit validate-config
python -m pre_commit run --all-files
python tools/check_repository.py
python tools/check_ai_configuration.py --json
python tools/ai_catalog.py
python -m unittest discover -s tests -v
python -m unittest discover -s tests/integration -v
```

The offline lane is separate from Git integration. ZIPs can run foundation, AI,
catalog and unit checks after dependency setup without Git initialization.
The all-files hook command uses tracked working-tree files; a clean CI checkout
supplies revision-specific evidence. The evaluation checker tests synthetic
reports; an application must supply its own real runner and acceptance evidence.

## Published evidence

Version 1.3 passed [GitHub CI](https://github.com/BharathChinthallapalli/reusable-github-template/actions/runs/34402368104).
For version 2.0, match [CI](https://github.com/BharathChinthallapalli/reusable-github-template/actions/workflows/ci.yml)
and [Copilot setup runs](https://github.com/BharathChinthallapalli/reusable-github-template/actions/workflows/copilot-setup-steps.yml)
to the delivered commit. This file cannot contain the hash of its own future
commit; the delivery report records that exact revision and observed results.
A successful setup workflow proves prerequisite setup, not cloud-agent invocation.

## Boundaries

Foundation checks cover expected files, markers, local Markdown links, Python
syntax, limited workflow properties and required-job agreement. They are not a
complete GitHub schema or security analysis. AI diagnostics validate core
metadata; the catalog checks drift from those definitions. None proves client
discovery, invocation, effective permissions or instruction compliance. Use
[host diagnostics](docs/ai-assistance.md) in the actual client.

The [offline evaluation gate](docs/evaluation-reports.md) validates a report's
shape and declared decision contract. It does not authenticate its provenance,
execute a model or establish application quality. The task exercises used
supplied evidence and did not execute fictional applications.

[Git checks](docs/git-hooks.md) are bypassable and do not scan history or detect
every secret. A live ruleset is needed for required-check merge enforcement.
No ruleset, cloud infrastructure, application deployment or model service was
activated by this expansion. Existing generated repositories require a reviewed
[version 2 migration](docs/maintenance.md).

The [research map](docs/research/capability-expansion.md) accounts for 32
substantiated improvement families; the 494-repository inventory remains an
inventory with tiered overview and source samples. External projects were not
executed or certified. Application behavior, performance and production readiness
require project-specific evidence.
