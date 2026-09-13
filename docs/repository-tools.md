# Choose a repository tool

Use this guide when you know the problem but need the right command. Run from
the repository root with the Python environment prepared in
[template setup](using-the-template.md). Python 3.12 or newer supports repository
tools; it does not select an application stack. Pins belong in the manifests and
installer, not in a second dependency list here.

For everyday file/content search, JSON inspection and terminal work, follow the
[agent tooling defaults and setup](agent-tooling.md). The commands below are the
foundation's validation and setup interfaces.

## Inspect and validate

These commands do not intentionally rewrite project source. Tests and tooling
may create temporary fixtures, bytecode or caches. Investigate nonzero results;
a successful command establishes only the boundary described below.

| Need | Command | Prerequisites | Result and boundary |
| --- | --- | --- | --- |
| Check the template foundation and local links | `python tools/check_repository.py` | Python standard library | Checks required files, markers and repository conventions; not application behavior or live GitHub settings |
| Diagnose agent and skill metadata | `python tools/check_ai_configuration.py --json` | PyYAML | Reports static metadata and paths; does not prove a host discovered or invoked them |
| Check the capability catalog is current | `python tools/ai_catalog.py` | PyYAML | Compares generated content with the committed catalog; no write by default |
| Validate completed agent designs | `python tools/check_design.py` | PyYAML | Checks coverage, accepted ADR references and content bindings; does not grant approval |
| Check coverage before a protected edit | `python tools/check_design.py --paths .github/agents/engineer.agent.md` | PyYAML and a ready ADD listing the actual paths | Allows binding drift during implementation; not the final delivery check |
| Check scanner readiness | `python hooks/agent_hooks.py --event session` | Installed Ruff and Gitleaks | Checks tool availability; not host hook invocation |
| Scan the current working tree | `python hooks/agent_hooks.py --event check` | Git, Ruff and Gitleaks | Checks bounded working-tree content, including eligible untracked files; not a full-history secret audit |
| Run the portable Git checks | `python -m pre_commit run --all-files` | Git, pre-commit; first hook setup needs network/cache | Checks tracked working-tree files; does not activate commit hooks or include every untracked file |
| Test repository tooling | `python -m unittest discover -s tests -v` | Development dependencies and Git for fixtures | Offline after setup; hook/scanner behavior uses controlled fixtures |
| Exercise real Git hooks and scanners | `python -m unittest discover -s tests/integration -v` | Git, pre-commit hook environment, Ruff and Gitleaks | Disposable Git repositories and real executables; record skips when local scanner prerequisites are missing; CI requires them |
| Assess a saved evaluation report | `python tools/check_evaluation.py path/to/report.json` | Standard library and a [version 1 report](evaluation-reports.md) | Prints JSON: exit 0 passed, 1 failed/inconclusive, 2 invalid input; does not run a model or authenticate reported evidence |

For missing executables, follow setup before interpreting a failure as a policy
finding. For metadata errors, repair the reported definition. For catalog drift,
regenerate and review the diff. For design drift, reconcile the design and actual
implementation before sealing; a fresh digest cannot repair an inaccurate design.

## Explicit setup and generated-file writes

| Need | Command or entrypoint | Writes and conditions |
| --- | --- | --- |
| Personalize a new generated project | [Initializer arguments in README](../README.md#start-here), using `tools/initialize.py` | Default previews only; `--write` updates five declared identity files and `template.json`. Keep the shared source uninitialized. Identical repeated inputs preserve content; different inputs are refused after initialization |
| Install the pinned secret scanner | `python tools/install_hook_tools.py` | Downloads and checksum-verifies a platform archive, then installs under `.tools/bin`; `--archive PATH` uses a local archive with the same verification |
| Activate commit checks in this clone | `python -m pre_commit install` | Writes local Git hooks; first inspect existing hooks and effective `core.hooksPath` using [hook preflight](git-hooks.md) |
| Regenerate the capability catalog | `python tools/ai_catalog.py --write` | Validates definitions, then writes `docs/ai-catalog.md`; inspect and commit the result |
| Bind a completed design to its files | `python tools/check_design.py --seal docs/add/0001-template-agents-and-hooks.md` | Select the affected ADD, reconcile its scope and narrative, then record its digest; preserves status. Run the default check afterward |

## Add project tools when they exist

Keep verified application commands in [project context](project.md#commands).
For a new tool, record the problem it solves, actual entrypoint, prerequisites,
side effects, expected output or exit status, and important limits. Link its
owning manifest, CLI or runbook. Recheck the entry when that interface changes.

The [AI catalog](ai-catalog.md) lists procedures and declared agent tool scopes;
it is not an installed-tool inventory. A recommendation in an external repository
does not establish that a tool is available or suitable for the current project.
