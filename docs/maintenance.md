# Maintain the template and generated projects

Assign an owner for the template and an owner for each generated repository. Record the template release or commit used to start each project and note deliberate deviations. A template is a starting snapshot: creating a repository from it does not establish automatic updates or a shared Git history. [GitHub: repository templates](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template).

## Review changes that alter the contract

Treat initializer arguments, `template.json`, required check names, supported runtimes, ruleset behavior, and shared workflow inputs as interfaces. A change to these can break a generated project or block merging even when a text diff looks small.

For a template release:

1. Prepare [the validation environment](using-the-template.md) in a clean checkout. Run foundation and AI configuration checks, offline unit tests, and the separate [hook checks and integration tests](git-hooks.md).
2. Initialize a disposable copy with realistic owner, team, and reporting values. Confirm the generated files contain the intended identities and the checks still pass.
3. Review changes to workflow triggers, permissions, action sources, required checks, and scripts that write files.
4. Update the release notes with the user-visible change, migration steps, changed settings, and known compatibility limits.
5. Tag the reviewed commit and publish a release through the team's normal process. GitHub releases are associated with tags; record the exact commit for reproducibility. [GitHub: releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases).

Use a consistent version policy. For this template, reserve major versions for incompatible initialization or CI contracts, minor versions for optional additions, and patches for compatible corrections. Version numbers communicate your policy; they do not make an upgrade safe without review.

## Follow the changed contract to its dependents

Use this matrix to find affected files; it does not require changing every file
for every edit. Preserve current project facts and verify the behavior that changed.

| Change | Inspect and update together | Evidence before completion |
| --- | --- | --- |
| Initializer arguments or project markers | `tools/initialize.py`, `template.json`, declared customization files, `tests/test_initialize.py`, README setup | Preview, intended writes, repeat behavior and initialized-copy checks |
| Required files or repository checks | `tools/check_repository.py`, `tests/test_check_repository.py`, CI and [command map](project.md) | Relevant missing/invalid-file cases and local-link checks |
| Agent/skill metadata or routing | Definitions, `AGENTS.md`, Copilot instructions, AI checker/tests and [AI assistance](ai-assistance.md) | Static diagnostics; separate host discovery/invocation evidence for runtime claims |
| Hook selection, revision, arguments or filters | `.pre-commit-config.yaml`, `tests/integration`, CI and [hook guide](git-hooks.md) | Clean-checkout scan, affected rejection/acceptance cases, staged-content behavior |
| Tooling dependency or Python version | `requirements-dev.txt`, CI setup, hook environment, setup docs and Dependabot configuration | Fresh environment plus relevant offline and integration lanes |
| Workflow trigger, permission or check name | CI, reusable-workflow consumers, ruleset recipe, live rules and [GitHub setup](github-setup.md) | Actual run at the changed SHA; no absent required context |
| Model, prompt, retrieval, data or evaluator | Actual project implementation/cases, [evaluation record](ai-evaluation.md), project context and deployment artifact reference | Comparable baseline/candidate evidence, provenance and data boundaries |
| Decision, public behavior or release | Current decision status, affected callers/tests/docs, migration notes and template version | Observable acceptance behavior and recorded compatibility limits |

Stop review when acceptance behavior is verified, blocking findings are resolved
and remaining limits are recorded. Another round needs new evidence, a changed
boundary or a failed acceptance case; unrelated suggestions can be deferred.

## Keep dependencies current

Review Dependabot pull requests on a regular schedule. The base configuration covers GitHub Actions and pinned Python validation dependencies; add application ecosystems and directories when introduced. Dependabot can update action and reusable workflow references. [GitHub: updating Actions with Dependabot](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/auto-update-actions).

For an action update, verify the upstream repository and commit, read release notes for changed runtime requirements or permissions, and confirm CI completes. Preserve full commit SHA references. A version comment helps reviewers understand the intended release but is not the executed reference. [GitHub: secure use](https://docs.github.com/en/actions/reference/security/secure-use).

GitHub's guidance reviewed for this template states that Dependabot vulnerability
alerts do not cover SHA-pinned Actions. Keep version-update PRs enabled and
monitor the upstream Actions' release and security notices; do not treat an
empty alert list as evidence that these dependencies have no vulnerabilities.

Hook repository revisions need a separate reviewed update. Run
`python -m pre_commit autoupdate --freeze` to propose full commit hashes, inspect
upstream changes and the resulting diff, then run the hook scan and integration
lane. Dependabot's pip entry updates `requirements-dev.txt`; it does not update
the hook repository `rev`. Top-level dependency pins and a hook commit pin do
not lock every transitive package. [pre-commit: frozen updates](https://pre-commit.com/#pre-commit-autoupdate).

For application dependencies, review the lockfile change and run the application's checks. Escalate urgent security fixes according to the project's reporting process. Avoid blanket auto-merge until the repository has enough meaningful coverage and a clearly agreed update policy.

## Update existing repositories through pull requests

Compare a generated project's recorded template version with the desired release. Select relevant file changes, preserve project-specific content, and open a focused migration PR. Do not overwrite its README, owners, license, or reporting channel with generic defaults. Do not rerun initialization across an established repository without first reviewing what it will write.

If a migration adds a required check, first ship the workflow and observe a successful run. Then update the live ruleset and the versioned recipe. If it removes or renames a check, coordinate the live rule change so that no required context is left permanently absent. Keep evidence of the settings change with the migration.

For multiple repositories, prefer the versioned reusable-workflow approach in [extending CI](extending-ci.md). Use explicit consumer upgrade PRs and a small pilot group. Do not assume changes in the template repository repair existing consumers.

## Adopt version 1.2

This update adds `tools/check_ai_configuration.py`, its tests, and
`requirements-dev.txt`. Install the pinned development dependency in your
validation environment and include the new command in CI; keep the existing
`Repository checks` job name. The initializer and foundation checker still run
without external packages. Review the new pip Dependabot entry if your project
already has one for the root directory; merge entries instead of duplicating them.

Merge the project-context, decision-status, troubleshooting, and agent guidance
with your project's actual facts. Do not replace its decisions with this
template's examples. Use [decision maintenance](decisions/README.md) to mark
superseded choices and verify [host discovery](ai-assistance.md) in the target client.

## Adopt version 1.3

Merge `.pre-commit-config.yaml`, updated development dependencies, the hook
integration tests and CI steps with existing project configuration. The
`Repository checks` job name stays the same, but now includes the all-files
hook scan and a separate integration lane. New checks can reject previously
accepted files: resolve baseline failures or document narrow project exceptions
before adopting the gate. A successful CI run detects compliance; enforcing it
on main also requires the project's live ruleset.

Install dependencies in the prepared environment. In a real Git checkout, run
`python -m pre_commit run --all-files` and
`python -m unittest discover -s tests/integration -v`; keep
`python -m unittest discover -s tests -v` as the offline unit-test lane after
dependency setup. First-time hook environment preparation needs network access;
reuse the prepared cache for integration tests. An extracted ZIP can still run
the foundation and unit checks before Git initialization. An all-files scan
does not prove untracked files or repository history were checked.

Local automatic checks are optional and require activation in each clone;
copying the configuration or installing the Python package does not activate
them. Follow [hook setup](git-hooks.md) to inspect existing hooks and effective
`core.hooksPath`, then use `python -m pre_commit install` without overwriting
managed hooks. CI runs independently of local installation. [pre-commit: usage](https://pre-commit.com/#usage).

Merge the [optional AI evaluation guidance](ai-evaluation.md) and maintenance
matrix with project procedures. They add no model service, runtime or application
framework, and do not replace application tests or authorize deployment.

## Periodically inspect operational drift

| Inspect | Resolve |
| --- | --- |
| Owners and reviewers | Departed staff, invisible teams, insufficient reviewer coverage |
| Live rules and workflow check names | Disabled protection, mismatched checks, unneeded bypasses |
| Environments and identities | Overbroad access, obsolete credentials, missing deployment restrictions |
| Reporting and docs | Broken contacts, stale local commands, incorrect support claims |
| Actions usage | Unused workflows, excessive runtime, unnecessary artifact retention |

Choose the review frequency based on project activity. Changes to organizational policy, repository visibility, ownership, or deployment identity should trigger an immediate targeted review. Archive abandoned projects through the team's normal process and remove their unused deployment access.
