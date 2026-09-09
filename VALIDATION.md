# Validation record

Template version: 1.3.0. Prepared 9 September 2026.

## Results and scope

- Linux, Python 3.12.14 and Git 2.51.1; pre-commit 4.6.2, PyYAML 6.0.3.
- Fifteen real Git integration tests passed with no skips or failures. The final warm-cache lane completed in 9.742 seconds; the first 14-case run including environment preparation took 65.053 seconds.
- Hook environment: pre-commit-hooks 6.0.0 at `3e8a8703264a2f4a69428a0aa4dcb512790b2c8c`, with ruamel.yaml 0.19.1 resolved locally. Source/top-level pins do not lock the entire dependency closure.
- Integration covers actual rejected commits, sanitized examples, environment and broken symlinks, symlink case collisions, malformed JSON/YAML/TOML, conflict markers outside merges, synthetic private-key markers, leading-option and control-character filenames, exact size boundaries, the LFS attribute exemption, both partial-staging directions, bypass caught in a clean clone, legacy-hook execution/restoration and managed hook-path refusal.
- Two independent plan critiques found option parsing, symlink filtering, installation-collision and test-lane issues. An independent implementation review reproduced and corrected the symlink-only case-collision gap. See [the challenge record](docs/research/plan-review.md).

Foundation checks, static AI diagnostics, all 51 offline tests and all-files hook checks passed in both the uninitialized source and a newly initialized disposable project. Initialization preview changed nothing; writing customized exactly six declared files; repeating identical inputs preserved every deliverable byte.

Tests run only with synthetic fixtures in disposable repositories; no actual credentials were used. Native Windows/macOS execution and editor discovery/invocation were not performed.

## Commands

In [the prepared environment](docs/using-the-template.md), from a Git checkout:

```bash
python -m pre_commit validate-config
python -m pre_commit run --all-files
python tools/check_repository.py
python tools/check_ai_configuration.py --json
python -m unittest discover -s tests -v
python -m unittest discover -s tests/integration -v
```

The 51-test offline lane is separate from the Git integration lane. ZIPs can run the foundation and AI checkers and offline tests before Git initialization. The all-files hook command uses Git-tracked working-tree files; a clean CI checkout supplies revision-specific evidence.

## Published evidence

The prior 1.2.0 commit passed [GitHub CI](https://github.com/BharathChinthallapalli/reusable-github-template/actions/runs/34398700036). For this version, inspect [CI runs](https://github.com/BharathChinthallapalli/reusable-github-template/actions/workflows/ci.yml) and match the run to the delivered commit. This file cannot contain the hash of its own future commit; the delivery report records that exact revision and observed result.

## Boundaries

The repository checker validates expected files, project markers, local links, Python syntax, basic workflow properties and required-job agreement. Its workflow checks are limited textual checks, not a complete GitHub schema or security analysis.

The AI checker safely parses metadata and validates core names, descriptions, types and duplicate fields. Five agents and five skills remain available through supported hosts. Static format checks do not prove host discovery, invocation, tool access or instruction compliance; use [the host check](docs/ai-assistance.md) in the actual client.

[Git checks](docs/git-hooks.md) detect configured current-tree problems; they are bypassable and do not scan history or detect every secret. A live ruleset is needed for required-check merge enforcement. No ruleset, cloud infrastructure, application deployment, model benchmark or new external service was activated by these changes.

The [repository research](docs/research/repository-review.md) records inventory and sampled source coverage. External projects were inspected, not executed or certified. Application behavior, quality, performance and production readiness require project-specific evidence.
