# Distinguish the cause before changing CI

| Failure class | Evidence that separates it |
| --- | --- |
| Platform or runner | Setup logs, runner image, capacity or outage information |
| Dependency resolution | Exact package or action reference, lockfile and resolver error |
| Authentication or access | Event origin, token scope, environment gate and service response |
| Application or test | First failing assertion, input, stack trace and matching local command |
| Workflow configuration | Parsed workflow error, condition, job dependency and required-check name |

For a canceled or skipped job, inspect concurrency and conditions before
calling it a test failure. For multiple failures, distinguish independent
causes from downstream effects of a failed setup or prerequisite job.

For a required check that stays pending, verify its exact name and source,
the expected commit SHA, and whether the intended event produced a run. A
successful check on an earlier commit cannot satisfy the new revision. Use
the pull request checks view to distinguish head from test-merge checks; when
a merge queue is configured, also check its `merge_group` event.

Inspect branch/path filters and skip messages before adding reruns: a skipped
workflow can leave a required check pending, while a conditionally skipped job
is reported differently. Keep the required `Repository checks` name aligned
with the ruleset. If an aggregate required job is used, inspect upstream
results explicitly so a failed prerequisite cannot produce a false success.

Compare runtime version, working directory, operating system and environment
variable names between local execution and CI. Inspect names and configuration
sources without printing secret values. A local pass on another revision or
runtime does not establish that the failing CI environment is repaired.

Keep evidence for each attempt. Logs for a partial rerun may omit jobs from
earlier attempts. Do not erase failure evidence or disable an assertion,
required job, security control or timeout to manufacture a green result.
Use the [investigation record](../../../../docs/troubleshooting.md#investigation-record)
for expected/actual behavior, the first causal error, observed evidence versus
hypotheses, and exact validation. Label the result confirmed fix, workaround or
unresolved; a rerun passing does not by itself prove a transient cause.

When a new permission is actually necessary, explain the operation requiring
it and scope it to the relevant job under existing task authorization. Preserve
the read-only workflow default and separation from untrusted pull-request code.

Official sources to check when the relevant behavior is uncertain:

- [Workflow run logs](https://docs.github.com/en/actions/how-tos/monitor-workflows/use-workflow-run-logs)
- [Required status checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks)
- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
