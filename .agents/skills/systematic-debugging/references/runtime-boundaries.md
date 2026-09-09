# Diagnose runtime boundaries

Use this reference when the failing path crosses a process, service, queue,
provider or asynchronous task. Select boundaries the project actually uses.
Record the intended behavior before choosing a recovery policy; a generic retry
is not a diagnosis.

| Boundary | Discriminating evidence | Relevant contract check |
| --- | --- | --- |
| Retry | Initial failure, classification, attempt count, delay and total elapsed time | Every eligible retry path terminates within its attempt/time budget; permanent failures terminate through the declared error path |
| Side effect | Operation/idempotency identity and observable state after a lost response | A retry or duplicate delivery follows the intended business-effect contract; a timeout does not prove the original write failed |
| Cancellation | Request/deadline propagation, task state and effect after cancellation | Caller and worker report the documented terminal or partial state; distinguish a cancellation request from observed termination |
| Remote execution | Input revision, workspace/synchronization record, command and result artifact identity | The tested artifact is the artifact changed; a remote green run on stale inputs is not verification of the current diff |
| Provider | Effective endpoint/model, configuration and provider error/response | Setup, authentication, quota, timeout and parsing failures remain distinguishable from a completed result that fails the quality requirement |
| Recovery | Dependency/state before failure, correction and next successful operation | Verify recovery through the actual consumer path, including replay or reconciliation when relevant |

Follow one operation across logs, metrics and traces using the project's
correlation identifier and relevant timestamps. Record enough version, attempt,
state and duration information to distinguish competing hypotheses. Check
whether sampling, clock differences or missing correlation accounts for an
apparent ordering gap before declaring causality from adjacent log lines.

Keep diagnostic evidence useful without copying credentials, raw protected
payloads or unrelated user data. Use the project's redaction and approved
evidence location; retain safe artifact IDs, status/error codes and bounded
context. Verify that the information needed to diagnose the failure survives
redaction. For stdio protocols, use the designated diagnostic channel rather
than contaminating protocol output.

For a relevant failure, add a row to the skill's diagnosis record containing the
operation/artifact identity, first failure, competing hypothesis, discriminating
check and observed recovery. State whether the check used a simulated dependency
or the actual runtime. Do not classify a missing log as proof of a missing effect.

Use [tool-integration](../../tool-integration/SKILL.md) for a provider/tool contract,
[AI evaluation](../../ai-evaluation/SKILL.md) for model-quality evidence and
[operations](../../../../docs/operations.md) for the project's recovery procedure.
Consult the selected platform's current documentation for retry/cancellation
semantics; these checks do not prescribe a transport or reliability architecture.

Sources include the inspected retry and execution limitations in
[John Papa's integrations](../../../../docs/research/repository-inventory/johnpapa-notes.md)
and [Karpathy's repositories](../../../../docs/research/repository-inventory/karpathy-notes.md),
alongside Microsoft's [Retry pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry).
The examples motivate boundary checks; they are not evidence of this project's
runtime behavior.
