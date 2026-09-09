---
applyTo: ".github/workflows/**/*.yml,.github/workflows/**/*.yaml"
---

Use explicit minimal permissions and timeouts. Pin external actions to verified
full commit SHAs and retain a release-version comment for maintenance.
Keep checkout credentials disabled unless a documented job requires them.
Never run untrusted PR code using pull_request_target with secrets or a write token.
Pass untrusted expression values through environment variables, not inline shell code.
Use lockfiles for application dependencies and the supported project runtime.
Do not add path filters to required checks without handling skipped runs.
Keep `Repository checks` aligned with the ruleset; preserve merge_group support.
Restrict deployment permissions and credentials to separate protected jobs.
