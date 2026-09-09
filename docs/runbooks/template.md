# Runbook: Failure or operation name

Owner:
Applicable component, environment and versions:
Last verified date and exercise/evidence reference:
Review trigger:

## Detect and scope

- User-visible symptom and expected behavior:
- Signal or alert and its evidence location:
- Affected revision/artifact and action/run identity:
- First failed stage and last confirmed successful stage:
- Impact and safe containment condition:
- Related decisions and provider documentation:

## Preconditions and state

- Required access and existing task authorization:
- Read-only inspection commands with scope and expected output:
- Durable state source, version/checkpoint and retention:
- Transient state that cannot prove completion:
- In-flight workers, operation keys and duplicate-execution risk:
- Known recovery target and data/configuration compatibility:
- Secret redaction and permitted evidence locations:

## Choose the response

Replace these rows with the component's actual conditions and commands. Do not
execute placeholders or introduce arbitrary retry limits without an owner or
service contract.

| Observed condition | Action and exact scope | Bound and stop condition | Success evidence |
| --- | --- | --- | --- |
| Completion uncertain after a lost response | Query authoritative operation state | Stop before replaying an unconfirmed side effect | Existing result or proven safe retry |
| Transient failure with replay safety established | Retry the failed stage | Record attempt/time/cost budget and backoff | Same intended effect without duplication |
| Permanent failure or stale/concurrent state | Pause that operation and preserve evidence | No repeated unchanged attempt | Corrected precondition or clear blocked action |
| Incompatible or unhealthy released artifact | Use verified recovery procedure and compatible target | Stop if data restore or target compatibility is unknown | Target identity and user-visible recovery |

## Execute and recover

1. Record sanitized evidence, action identity and current state before mutation.
2. Confirm the chosen action is within the current task and access. If a required
   permission is missing, prepare the concrete action and state why it is blocked.
3. Claim the operation through the application's supported concurrency control;
   verify state/version and artifact identity immediately before action.
4. Execute the narrow action. Preserve its outcome and exit status even if later
   reporting or cleanup succeeds. Record partial completion explicitly.
5. Verify the exact recovered artifact, affected state and original user outcome.
   Release claims/leases through their documented path and resume authorized work.

Rollback or compensating action, prerequisites and verification:
What must never be automatically replayed:
Fallback if recovery fails, with precise owner/access route:

## Execution record

Record timestamps, run/attempt and action IDs, observed state/version, chosen
action, relevant authorization reference, sanitized result evidence and remaining
work. Store credentials and opaque capability-bearing resume tokens only in the
system's approved secret/state storage; never paste them into the runbook.

Outcome: confirmed recovery, workaround, unresolved, or blocked.
Follow-up that changes this runbook, with supporting evidence:
