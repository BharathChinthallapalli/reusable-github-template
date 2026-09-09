# @@PROJECT_NAME@@

@@PROJECT_DESCRIPTION@@

Repository: `@@GITHUB_OWNER@@/@@PROJECT_SLUG@@` · Owner: @@CODEOWNER@@

## Start here

This is a reusable repository foundation for applications, services, automation,
and AI projects. It bundles 21 reusable engineering skills, 10 specialist agents,
task records, AI evaluation tooling, CI and collaboration conventions. Application
code, application tests, providers and deployment use each project's requirements.

1. Follow [template setup](docs/using-the-template.md) to create your template
   repository, then use GitHub's **Use this template** for each new project.
2. Clone the new project and run the initializer below with your real values.
3. Complete [project context](docs/project.md), add your application, and extend
   CI using [the application CI guide](docs/extending-ci.md).
4. Follow [GitHub setup](docs/github-setup.md) to configure reviewers, rules,
   security features, and repository settings.

Requires Python 3.12 or newer for repository tools. The initializer and foundation
checker use the standard library; AI validation and Git checks use the development
dependencies in `requirements-dev.txt`. Python is a tooling dependency,
not a choice of application language. Follow [environment setup](docs/using-the-template.md)
before running the full checks. On Windows, use the prepared environment's Python.

```bash
python3 tools/initialize.py --name 'Policy Assistant' --slug policy-assistant --owner example-org --codeowner '@example-org/maintainers' --security-contact 'mailto:security@example.com' --description 'Internal policy question answering service.'
```

The command previews changes. Add `--write` to apply them. Use a real monitored
security address or private HTTPS reporting page. Initialization is local and
does not create a GitHub repository or grant access.

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pre_commit run --all-files
python3 tools/check_repository.py
python3 tools/check_ai_configuration.py
python3 tools/ai_catalog.py
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s tests/integration -v
```

In each clone, activate commit checks with `python3 -m pre_commit install` after
the [hook installation preflight](docs/git-hooks.md). CI checks tracked files
independently. Hook commands require Git; ZIP validation and setup are explained
in [environment setup](docs/using-the-template.md).

`Repository checks` validates this foundation and tests its setup tools. It does
not certify an application's behavior, security, or production readiness.

## Included

| Area | Files and purpose |
| --- | --- |
| Collaboration | Issue forms, PR template, contribution guide, support and security reporting |
| Ownership | CODEOWNERS populated by the initializer; reviewer permissions configured in GitHub |
| CI | SHA-pinned actions, read-only token, clean checkout, timeout, cancellation, merge-group trigger |
| Git checks | Ten portable checks, staged-commit validation, all-files CI, real Git integration tests |
| Maintenance | Dependabot for GitHub Actions and validation dependencies; release-note categories; template version tracking |
| Governance | Disabled ruleset for import; explicit activation instructions |
| AI assistance | [Specialist agents and shared skills](docs/ai-catalog.md), default task routing, clean-code guidance, scoped instructions |
| Engineering | Domain and acceptance context, maintained architecture decisions, operations and troubleshooting guides |
| AI experiments | Optional [evaluation contract](docs/ai-evaluation.md) for baselines, outcomes, budgets and provenance |
| Working assets | Research, plans, handoffs, tests, experiments, data/tool contracts, dependency and release records bundled with their skills |
| Executable AI tooling | Static catalog with drift checks, [offline evaluation-report gate](docs/evaluation-reports.md), Copilot environment setup |
| Adoption | Safe initializer, repository checker, AI configuration diagnostics, tooling tests, stack and Azure extension guides |
| Evidence | [Company comparison and current sources](docs/research/README.md); [32 capability families mapped to shipped improvements](docs/research/capability-expansion.md) |

## Default AI assistance

New repositories inherit the agents, skills, and workspace defaults. In a
supported Copilot session, repository instructions apply automatically and route
relevant work to clean-code, discovery, verification, review, and CI-debugging
procedures. The expanded catalog covers research, planning, orchestration,
debugging, test design, AI/data/retrieval/tool engineering, security, performance,
interfaces, dependency upgrades, context maintenance and release delivery.
Select `engineer` for coordinated implementation, or choose a specialist directly.
See [example tasks](docs/working-with-agents.md) and [AI assistance](docs/ai-assistance.md)
for the inventory
and a discovery check that separates valid files from observed host behavior.
Use [troubleshooting](docs/troubleshooting.md) for reproducible failure reports
and state-aware Git or CI recovery. Skills load as needed; these files do not start
agents in the background or consume model usage on their own.

Skills use one canonical `.agents/skills` folder for supported Copilot and Codex
clients. `CLAUDE.md` imports the shared instructions for Claude Code. Custom-agent
menus and invocation differ by client; the [host guide](docs/ai-assistance.md)
records those boundaries. The Copilot setup workflow prepares repository tools;
CI remains the independent required-check source.

## Project status

After initialization, replace this section and the template introduction with
your project's purpose, users, prerequisites, run command, and supported versions.
Keep the setup guidance in `docs/` for maintainers.

## License

A project license has not been selected. Choose the appropriate license or
internal-use policy before distributing this repository; see
[licensing decisions](docs/licensing.md). Referenced companies do not endorse
this template. Their code and policies have not been bundled.
