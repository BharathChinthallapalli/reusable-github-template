# Maintain the template and generated projects

Assign an owner for the template and an owner for each generated repository. Record the template release or commit used to start each project and note deliberate deviations. A template is a starting snapshot: creating a repository from it does not establish automatic updates or a shared Git history. [GitHub: repository templates](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template).

## Review changes that alter the contract

Treat initializer arguments, `template.json`, required check names, supported runtimes, ruleset behavior, and shared workflow inputs as interfaces. A change to these can break a generated project or block merging even when a text diff looks small.

For a template release:

1. Run `python tools/check_repository.py` and `python -m unittest discover -s tests -v` from a clean checkout.
2. Initialize a disposable copy with realistic owner, team, and reporting values. Confirm the generated files contain the intended identities and the checks still pass.
3. Review changes to workflow triggers, permissions, action sources, required checks, and scripts that write files.
4. Update the release notes with the user-visible change, migration steps, changed settings, and known compatibility limits.
5. Tag the reviewed commit and publish a release through the team's normal process. GitHub releases are associated with tags; record the exact commit for reproducibility. [GitHub: releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases).

Use a consistent version policy. For this template, reserve major versions for incompatible initialization or CI contracts, minor versions for optional additions, and patches for compatible corrections. Version numbers communicate your policy; they do not make an upgrade safe without review.

## Keep dependencies current

Review Dependabot pull requests on a regular schedule. The base configuration covers GitHub Actions; add package ecosystems and directories when an application actually introduces them. Dependabot can update action and reusable workflow references. [GitHub: updating Actions with Dependabot](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/auto-update-actions).

For an action update, verify the upstream repository and commit, read release notes for changed runtime requirements or permissions, and confirm CI completes. Preserve full commit SHA references. A version comment helps reviewers understand the intended release but is not the executed reference. [GitHub: secure use](https://docs.github.com/en/actions/reference/security/secure-use).

GitHub's guidance reviewed for this template states that Dependabot vulnerability
alerts do not cover SHA-pinned Actions. Keep version-update PRs enabled and
monitor the upstream Actions' release and security notices; do not treat an
empty alert list as evidence that these dependencies have no vulnerabilities.

For application dependencies, review the lockfile change and run the application's checks. Escalate urgent security fixes according to the project's reporting process. Avoid blanket auto-merge until the repository has enough meaningful coverage and a clearly agreed update policy.

## Update existing repositories through pull requests

Compare a generated project's recorded template version with the desired release. Select relevant file changes, preserve project-specific content, and open a focused migration PR. Do not overwrite its README, owners, license, or reporting channel with generic defaults. Do not rerun initialization across an established repository without first reviewing what it will write.

If a migration adds a required check, first ship the workflow and observe a successful run. Then update the live ruleset and the versioned recipe. If it removes or renames a check, coordinate the live rule change so that no required context is left permanently absent. Keep evidence of the settings change with the migration.

For multiple repositories, prefer the versioned reusable-workflow approach in [extending CI](extending-ci.md). Use explicit consumer upgrade PRs and a small pilot group. Do not assume changes in the template repository repair existing consumers.

## Periodically inspect operational drift

| Inspect | Resolve |
| --- | --- |
| Owners and reviewers | Departed staff, invisible teams, insufficient reviewer coverage |
| Live rules and workflow check names | Disabled protection, mismatched checks, unneeded bypasses |
| Environments and identities | Overbroad access, obsolete credentials, missing deployment restrictions |
| Reporting and docs | Broken contacts, stale local commands, incorrect support claims |
| Actions usage | Unused workflows, excessive runtime, unnecessary artifact retention |

Choose the review frequency based on project activity. Changes to organizational policy, repository visibility, ownership, or deployment identity should trigger an immediate targeted review. Archive abandoned projects through the team's normal process and remove their unused deployment access.
