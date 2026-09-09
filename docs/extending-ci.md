# Extend CI when an application exists

The base workflow is named **CI** and exposes one job named **Repository checks**. It runs on `ubuntu-24.04` with Python 3.12, uses full commit SHA references for checkout and Python setup, and requests `contents: read`.

Its commands are:

```bash
python tools/check_repository.py
python -m unittest discover -s tests -v
```

Passing these checks means the repository scaffold meets its local checks. It does not establish application correctness, security, deployment readiness, or that GitHub settings are active.

## Add a concrete application contract

Once you choose a stack, add its manifest, lockfile, supported runtime version, source code, and documented local commands in one change. Then add an application CI job that runs those same commands from a clean checkout.

| Stage | Required evidence |
| --- | --- |
| Install | Reproducible install using the chosen package manager's locked or frozen mode |
| Lint | Rules appropriate to the language and codebase; fail on actionable violations |
| Types | Static type checking where the selected language supports it |
| Tests | Behavior tests for a real requirement, including a relevant failure case |
| Build | The actual production build, package, or container that delivery will consume |

Use meaningful scripts that exist in the repository. Do not add placeholder commands that print success, disable failures, or silently pass when tests are missing. A documentation-only project can retain the scaffold checks; it does not need an invented application build.

Choose a small runtime matrix only when you promise compatibility with those versions. Record the supported versions in the README. Add caching once dependency restoration is measurable, key it to the lockfile and runtime, and keep credentials and sensitive outputs out of caches and artifacts.

## Preserve a dependable merge gate

Keep **Repository checks** unchanged while adding an independently named application job. After the application check succeeds on a PR, add its exact observed name to the live ruleset and update the JSON recipe. A local JSON change does not update GitHub's active settings.

Required checks must reliably report for every applicable PR. Avoid workflow-level path filters that leave a required workflow unreported. If you later introduce conditional jobs or an aggregate gate, explicitly fail the gate on failed or unexpectedly skipped dependencies. Demonstrate that behavior with a deliberate failure before requiring it.

When adopting a merge queue, verify every required workflow runs on `merge_group`; a successful `pull_request` run does not satisfy the queue's separate check request. [GitHub: workflow events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#merge_group).

## Keep privileges tied to work

Retain read-only permissions for validation. Put publishing and deployment in separate jobs with only their necessary permissions. Pin additional actions to full upstream commit SHAs and retain a version comment for review. Avoid privileged triggers that execute untrusted PR code. Pass untrusted text as data instead of inserting it into shell programs. These choices follow [GitHub's secure use guidance](https://docs.github.com/en/actions/reference/security/secure-use).

Add language-specific dependency update entries only when the corresponding manifests exist. Select code scanning and dependency review based on supported languages, repository visibility, and organizational entitlement; document any resulting required checks.

## Evolve across repositories

When several repositories share a proven CI contract, move that contract into an owned automation repository with a `workflow_call` workflow. Define typed inputs, explicit secrets, outputs, and supported versions. Call it at job level and pin consumers to reviewed commit SHAs associated with documented releases. Avoid mutable `main` references for shared delivery policy. [GitHub: reusable workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows).

Roll out upgrades through pull requests to consuming repositories. Pilot breaking changes in one representative project before wider adoption. Keep application-specific commands and tests owned by each product team; a central workflow should not hide what is being validated. See [maintenance](maintenance.md) for the update process and [Azure delivery](azure-delivery.md) when a deployable application is ready.
