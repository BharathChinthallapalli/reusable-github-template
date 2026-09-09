# Configure a generated repository

This template supplies files and a working scaffold check. Repository administration remains an explicit setup task. Complete these steps before treating a generated repository as ready for team development.

## 1. Create and initialize

On the template repository, select **Use this template → Create a new repository**, choose the owner and visibility, and copy the default branch only. A generated repository starts its own history; later template changes do not automatically propagate. [GitHub: creating from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template).

Clone the new repository. From its root, using Python 3.12, substitute your real values in this example:

```bash
python tools/initialize.py \
  --name 'Policy Assistant' \
  --slug policy-assistant \
  --owner example-org \
  --codeowner '@example-org/maintainers' \
  --security-contact 'mailto:security@example.com' \
  --description 'Internal policy Q&A service.' \
  --write
python tools/check_repository.py
python -m unittest discover -s tests -v
```

Review the changed files and `template.json`, then commit and push. These commands validate the scaffold and its tooling; application behavior has no tests until you add an application.

The workflow assumes the default branch is `main`. If your organization uses another name, align workflow branch filters, documentation, and deployment restrictions before enabling required checks. The supplied ruleset targets the default branch.

Choose the project's licensing and distribution terms before sharing it. Add the appropriate license and preserve notices for any reused material. A public repository without a license does not grant general reuse rights. [GitHub: licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).

## 2. Separate files from settings

| Supplied in Git | Configure or verify in GitHub |
| --- | --- |
| `CODEOWNERS` entries | Actual users, visible teams, repository access |
| Workflow YAML | Actions enablement, allowed actions, token policy, runners |
| Ruleset JSON | Imported ruleset and its enforcement state |
| Issue forms and PR template | Issues availability, labels, project automation |
| Security reporting instructions | A working private reporting channel and security features |
| Deployment guidance | Environments, reviewers, variables, secrets, Azure identity |

Do not assume settings, permissions, integrations, labels, or secrets were copied from the source template. Organization policies may independently apply to the new repository. Inspect those existing policies before adding overlapping rules.

## 3. Verify ownership and CI

Ensure every configured code owner can review the repository. A team must be visible and have explicit write access; its members having access individually is insufficient. `CODEOWNERS` must exist on the PR's base branch to request owners. [GitHub: code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).

Open a small PR after initialization reaches `main`. Confirm **CI / Repository checks** succeeds and the expected owner receives a review request. Confirm another eligible person can approve: a one-person team cannot supply independent review of its own PRs. Agree a suitable review policy before activation.

## 4. Import and activate the ruleset

1. In repository **Settings**, open **Rulesets** under **Code and automation**, then the **Rulesets** page. Some sidebars group this under **Rules**.
2. Open the **New ruleset** dropdown and choose **Import a ruleset**. Select `.github/rulesets/main.json`.
3. Inspect every imported rule, the default-branch target, and bypass list. Keep enforcement **Disabled**, then click **Create**.
4. Verify the required check is exactly **Repository checks**, with GitHub Actions as its expected source where selectable. The workflow title `CI` is not the check name.
5. Only after a successful PR run and verified reviewers, edit the ruleset to **Active** and save. Exercise a normal reviewed PR to confirm the merge gate works.

The JSON file alone enforces nothing. Importing and enforcement are separate operations. Review account plan and repository visibility support before adopting these settings. [GitHub: managing rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/managing-rulesets-for-a-repository), [ruleset availability and enforcement](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository).

## 5. Enable suitable security features

Under repository security settings, verify dependency graph and Dependabot
alerts/updates. The included Dependabot file requests weekly GitHub Actions
version updates. Review the first update PR to confirm it runs.

When application manifests exist, add their ecosystems and evaluate code
scanning, dependency review, secret scanning, and push protection. For private or
internal repositories, some features depend on GitHub Code Security or Secret
Protection licensing. Confirm availability before making a scanner a required
merge check. [GitHub security features](https://docs.github.com/en/code-security/getting-started/github-security-features).

The workflows request read-only contents access. Review Actions permissions,
allowed actions, fork-PR approval policy, and runner access in GitHub; local YAML
cannot change organization policy. Keep deployment credentials and elevated
permissions out of pull-request validation jobs.
