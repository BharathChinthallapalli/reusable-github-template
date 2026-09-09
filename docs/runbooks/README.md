# Operational runbooks

Runbooks describe how to recognize a failure, choose a bounded response and
verify recovery. They complement the [operations worksheet](../operations.md)
and [troubleshooting evidence](../troubleshooting.md); they do not provision a
runtime or make an undocumented recovery command safe.

| Runbook | Use |
| --- | --- |
| [Agent recovery](agent-recovery.md) | Interrupted, duplicated, denied or uncertain agent/tool execution |
| [Runbook template](template.md) | Capture a verified procedure for a project-specific operational failure |

Create a runbook when a repeated or consequential failure needs a repeatable
response. Fill the template from the actual application, relevant provider
documentation and a verified recovery exercise. Name an owner and review trigger;
record unknown commands or targets as unknown until confirmed. Keep stable steps
here and transient execution details in the issue, incident or task record.

Record run identifiers, exact artifact/revision, sanitized evidence and the
result of each action. Preserve existing task authorization, and request only
an actually missing permission for a concrete action. Do not widen access,
publish information, send messages or bypass checks as a side effect of recovery.

After recovery, verify the original user-visible outcome and any affected state,
then resume the authorized task. A process restart or successful retry alone
does not establish that the cause was repaired.
