# @@PROJECT_NAME@@

@@PROJECT_DESCRIPTION@@

Repository: `@@GITHUB_OWNER@@/@@PROJECT_SLUG@@` · Owner: @@CODEOWNER@@

## Start here

This is a reusable repository foundation for applications, services, automation,
and AI projects. It provides repository tooling and collaboration conventions.
Application code, application tests, and deployment are added for each project.

1. Follow [template setup](docs/using-the-template.md) to create your template
   repository, then use GitHub's **Use this template** for each new project.
2. Clone the new project and run the initializer below with your real values.
3. Complete [project context](docs/project.md), add your application, and extend
   CI using [the application CI guide](docs/extending-ci.md).
4. Follow [GitHub setup](docs/github-setup.md) to configure reviewers, rules,
   security features, and repository settings.

Requires Python 3.12 or newer for repository tools. The initializer and foundation
checker use the standard library; AI configuration validation and the full test
suite use the dependency in `requirements-dev.txt`. Python is a tooling dependency,
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
python3 tools/check_repository.py
python3 tools/check_ai_configuration.py
python3 -m unittest discover -s tests -v
```

`Repository checks` validates this foundation and tests its setup tools. It does
not certify an application's behavior, security, or production readiness.

## Included

| Area | Files and purpose |
| --- | --- |
| Collaboration | Issue forms, PR template, contribution guide, support and security reporting |
| Ownership | CODEOWNERS populated by the initializer; reviewer permissions configured in GitHub |
| CI | SHA-pinned actions, read-only token, clean checkout, timeout, cancellation, merge-group trigger |
| Maintenance | Dependabot for GitHub Actions and validation dependencies; release-note categories; template version tracking |
| Governance | Disabled ruleset for import; explicit activation instructions |
| AI assistance | Default clean-code guidance, five custom agents, five automatically selectable skills, scoped instructions |
| Engineering | Domain and acceptance context, maintained architecture decisions, operations and troubleshooting guides |
| Adoption | Safe initializer, repository checker, AI configuration diagnostics, tooling tests, stack and Azure extension guides |
| Evidence | [Company comparison and current sources](docs/research/README.md) |

## Default AI assistance

New repositories inherit the agents, skills, and workspace defaults. In a
supported Copilot session, repository instructions apply automatically and route
relevant work to clean-code, discovery, verification, review, and CI-debugging
procedures. Select `engineer` for coordinated implementation, or choose a
specialist directly. See [AI assistance](docs/ai-assistance.md) for the inventory
and a discovery check that separates valid files from observed host behavior.
Use [troubleshooting](docs/troubleshooting.md) for reproducible failure reports
and state-aware Git or CI recovery. Skills load as needed; these files do not start
agents in the background or consume model usage on their own.

## Project status

After initialization, replace this section and the template introduction with
your project's purpose, users, prerequisites, run command, and supported versions.
Keep the setup guidance in `docs/` for maintainers.

## License

A project license has not been selected. Choose the appropriate license or
internal-use policy before distributing this repository; see
[licensing decisions](docs/licensing.md). Referenced companies do not endorse
this template. Their code and policies have not been bundled.
