# Match verification to the risk

| Change | Useful evidence |
| --- | --- |
| Parsing or validation | Accepted input, rejected input and a relevant boundary value |
| Access or tenant filtering | Permitted request and denied or cross-tenant request |
| Data transformation | Representative input and externally meaningful output |
| State mutation | Expected state, error behavior and rollback or retry where relevant |
| Interface or adapter | Contract at the boundary and an affected caller |
| Workflow configuration | Trigger, permissions, required job names and relevant run logs |
| Documentation only | Paths, examples and consistency with the implemented behavior |

Choose entries that match the actual diff. A reversible wording edit usually
does not need a new test suite. A passing formatter does not establish behavior;
a mocked unit test does not establish a live integration.

When the change affects a failure boundary, consider only relevant cases:

| Boundary | Behavior to demonstrate |
| --- | --- |
| Dependency call | Timeout, unavailable response and successful recovery stay within the intended request budget |
| Retry | Attempts and delay are bounded; permanent failures stop; a response lost after a committed operation does not duplicate its effect |
| Queue processing | Duplicate delivery and restart after partial work preserve the intended business result |
| Cache | Write/invalidation, expiry and unavailable cache follow the specified freshness and fallback contract |
| Access | Expired credentials, denied permissions and a valid request enforce the intended boundary |

Use an existing harness and the selected dependency's actual contract. Local
controlled failures may be sufficient; cloud provisioning, load testing and
chaos experiments are not defaults. See [operations](../../../../docs/operations.md#failure-and-recovery-checks)
for recording the intended failure and recovery behavior.

For a regression, capture a minimal reproducer or behavioral test. Where
practical, show that it fails for the relevant reason before the fix and passes
afterward. Do not disturb the user's working tree to obtain this comparison.

When checks fail, record the failing command, exit status and concise error
evidence. Classify the cause as a demonstrated regression, an established
baseline failure, an environment blocker or an unresolved cause. An untested
guess that the failure predates the change is not a baseline result.
Keep the client/runtime version, revision, and CI attempt with the evidence.
Use the [investigation record](../../../../docs/troubleshooting.md#investigation-record)
to distinguish a confirmed fix, workaround and unresolved cause. Check the
original symptom again after recovery; setup success alone is insufficient.

Do not run deployment, production writes or paid external requests merely to
validate a local change. Use authorized test environments and state the limit
when an integration cannot be exercised. Stop when required gates and the
remaining credible risks are sufficiently addressed.
