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

Compare runtime version, working directory, operating system and environment
variable names between local execution and CI. Inspect names and configuration
sources without printing secret values. A local pass on another revision or
runtime does not establish that the failing CI environment is repaired.

Keep evidence for each attempt. Logs for a partial rerun may omit jobs from
earlier attempts. Do not erase failure evidence or disable an assertion,
required job, security control or timeout to manufacture a green result.

When a new permission is actually necessary, explain the operation requiring
it and scope it to the relevant job under existing task authorization. Preserve
the read-only workflow default and separation from untrusted pull-request code.

Official sources to check when the relevant behavior is uncertain:

- [Workflow run logs](https://docs.github.com/en/actions/how-tos/monitor-workflows/use-workflow-run-logs)
- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
