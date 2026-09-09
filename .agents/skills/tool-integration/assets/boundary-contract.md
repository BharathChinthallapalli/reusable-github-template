# Provider or tool boundary contract

Status: Draft. Name the actual operation; complete only relevant boundaries.

| Contract | Project value |
| --- | --- |
| Operation, caller and handler/adapter path | |
| SDK/protocol version and official documentation | |
| Effective endpoint, model/deployment and configuration revision | |
| Input/output schemas, limits and validation | |
| Caller identity, authorized resources and side effects | |
| Completion signal, partial-result and error-state semantics | |
| Timeout/cancellation, maximum attempts and total elapsed budget | |
| Retry-eligible failures, backoff and write idempotency | |
| Workspace/resource identity across local and remote execution | |
| Diagnostic channels, trace correlation and sensitive-data treatment | |
| Local test command and actual integration evidence | |

## Effective data flows

Include inference, embeddings/memory, search, evaluation and telemetry when used.
Record what is sent and where; a provider name in a README is not runtime proof.

| Purpose | Effective destination/model | Data sent | Identity/access boundary | Retention/logging behavior | Evidence |
| --- | --- | --- | --- | --- | --- |

## Boundary cases

| Case | Expected observable behavior | Fixture/command | Actual outcome/evidence |
| --- | --- | --- | --- |
| Valid request | Output and actual effect satisfy the declared contract | | Not run |
| Invalid input | Rejected before unintended work or side effects | | Not run |
| Denied access | Expected denial without exposing protected data | | Not run |
| Timeout/cancellation | Work terminates or reports its known state within the declared budget | | Not run |
| Transient failure/rate limit | Eligible bounded retry, followed by explicit success or exhaustion | | Not run |
| Permanent failure | Terminates without an unbounded or ineffective retry | | Not run |
| Lost response after a write | Retry/reconciliation follows the idempotency contract | | Not run |
| Malformed/partial provider output | Distinct failure or documented partial result | | Not run |
| Remote workspace | Checked artifact is the artifact actually changed | | Not run |
| MCP stdio, when used | Initialization/tool exchange succeeds with protocol-only stdout | | Not run |

Mark inapplicable cases with a reason. A simulated result proves the simulated
boundary only; record separate evidence for an actual provider/host exchange.
