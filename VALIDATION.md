# Validation record

Template version: 3.0.0. Prepared 9 September 2026.

## Results and scope

- Linux, Python 3.12.14 and Git 2.51.1; pre-commit 4.6.2, PyYAML 6.0.3.
- **136 offline tests** pass in the source and a disposable initialized project: the prior 80 tests plus 24 hook CLI, 18 design-gate and 14 installer tests.
- The existing **15 real Git integration tests** pass locally. The seven new real-scanner cases require Ruff 0.16.6 and Gitleaks 8.30.1; local absence is reported as a skip, while CI requires the tools and runs those cases as a failing gate if setup is missing.
- Foundation checks, static diagnostics for **24 skills and 10 agents**, catalog freshness, scoped design coverage/bindings and all-files Git hook scans pass in source and initialized copies. All 24 skill entrypoints pass the skill format validator.
- Initialization preview changes no deliverable; writing customizes exactly six declared files; repeating identical inputs preserves deliverable bytes. The sealed design remains valid because project identity customization is outside its protected implementation scope.
- Independent review resolved input-controlled secret suppression, scanner module shadowing, host path/error differences, literal command variants, setup usability and generated-bytecode handling. See [hook verification](docs/research/hook-validation.md) for evidence and limits.

Offline tests use synthetic fixtures and controlled subprocesses. No candidate
command under inspection was executed, and no real credential or model/provider
call was used. The local environment could not obtain the real scanner executables;
actual scanner checks and pinned installation are configured to run in GitHub CI.
The delivery response records whether the exact delivered commit passed. Native
Windows/macOS execution and live Copilot/VS Code/Codex hook invocation were not
performed locally. The Windows command override and six installer targets are
configured and tested structurally; the configured runtime test target is Linux CI.

## Commands and evidence levels

Use [the prepared environment](docs/using-the-template.md). Install the pinned
scanner before the complete hook checks:

```bash
python tools/install_hook_tools.py
python hooks/agent_hooks.py --event session
python hooks/agent_hooks.py --event check
python -m pre_commit run --all-files
python tools/check_repository.py
python tools/check_ai_configuration.py --json
python tools/ai_catalog.py
python tools/check_design.py
python -m unittest discover -s tests -v
python -m unittest discover -s tests/integration -v
```

The offline lane uses controlled scanner fixtures, independent of real tool
installation. Git integration exercises actual Git/pre-commit. The agent hook
integration class requires real pinned tools; CI sets
`REQUIRE_AGENT_HOOK_TOOLS=1` so missing prerequisites cannot silently pass as skips.
Application testing, AI quality evaluation and native host invocation remain
separate evidence categories.

## Published evidence

Version 2.0 passed [GitHub CI](https://github.com/BharathChinthallapalli/reusable-github-template/actions/runs/34405570005).
For version 3.0, match [CI](https://github.com/BharathChinthallapalli/reusable-github-template/actions/workflows/ci.yml)
and [Copilot setup](https://github.com/BharathChinthallapalli/reusable-github-template/actions/workflows/copilot-setup-steps.yml)
to the delivered commit. The delivery response records the exact observed runs;
this file cannot contain the hash of its own future commit.

CI prepares the checksum-pinned scanner, checks current design bindings, runs
Ruff/Gitleaks, verifies repository metadata/catalog, and executes both test lanes.
Setup success proves prerequisites, not that a cloud agent selected or executed a
hook. [Host verification](hooks/README.md) requires the actual client and its trust
controls; current Codex requires review through `/hooks`.

## Boundaries

The foundation checker validates expected files, markers, links and syntax, with
limited workflow checks. Metadata validation and catalog generation do not prove
native activation. The ADD gate checks structure, explicit coverage, accepted
ADR references and current content bindings; it cannot approve business actions,
authenticate a reviewer or certify semantic correctness. Sealing preserves status.

The [agent hooks](hooks/README.md) reject detected secrets and known command/path
violations. They do not sandbox arbitrary programs or reverse post-edit effects;
host timeouts, interactive input and uncovered tools retain documented limits.
The working-tree scanner does not scan repository history. A live ruleset is
needed for merge enforcement; no rule, access grant, cloud deployment or model
service was activated by this update.

The [evaluation report gate](docs/evaluation-reports.md) remains an offline evidence
contract with synthetic examples, not a model runner. The [32-family research map](docs/research/capability-expansion.md)
retains the original inventory/source-review limits. [Cloudflare research](docs/research/cloudflare-agents.md)
adds focused pinned source observations. Existing generated projects need a
reviewed [version 3 migration](docs/maintenance.md).
