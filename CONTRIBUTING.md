# Contributing

Read README.md and docs/project.md for the purpose, supported runtimes, and local
commands. Open an issue for a substantial design change so maintainers can
agree on the outcome before implementation.

1. Create a short-lived branch from the default branch.
2. Make one coherent change; include a regression test for a meaningful failure.
3. Run repository checks and the relevant application checks. List actual
   commands and results in the PR.
4. Explain why the change is needed, the resulting behavior, and any rollout
   or compatibility concerns. Request review from the relevant owner.
5. Resolve review discussions and merge using the repository's configured rules.

Use descriptive commit messages. Conventional Commits are optional unless the
project adopts release automation that requires them. Avoid mixing formatting
with unrelated behavior changes.

Do not include real customer information, production documents, secrets, or
unlicensed assets in fixtures. Route vulnerabilities through SECURITY.md.
Keep discussion respectful, specific, and focused on the work. Follow the
organization's adopted conduct policy, if one exists; this template does not
appoint an enforcement team or make response-time commitments.

Before adding a dependency, explain its purpose, alternatives, maintenance,
license, and runtime impact. Commit its lockfile and extend dependency updates.
Review AI-generated contributions using the same tests and ownership rules as
other code. The contributor remains responsible for the change.
