# Threat-model worksheet

Complete this against actual code and deployment choices. Use the smallest
model that captures the system's real access and data boundaries.

1. Identify users, administrators, service identities, data sources, and outputs.
2. Trace the data from entrypoint through processing and storage. Mark where
   identity, authorization, validation, and logging occur.
3. Record concrete threats, controls, verification, and remaining risk.

| Boundary or operation | Failure to investigate | Verification evidence |
| --- | --- | --- |
| User reads a record | Another user's or tenant's data is returned | Authorization tests for allowed and denied callers |
| External input | Injection or unsafe parsing changes execution | Malformed and adversarial input tests |
| Background identity | Service can read or modify excessive resources | Effective permission review and denied-operation test |
| Logs and exports | Secrets or restricted content are disclosed | Sanitized fixtures and log/export inspection |
| Build and deployment | Untrusted contribution gains credentials | Workflow and environment permission review |
| Dependency update | Compromised or incompatible dependency enters release | Lockfile diff, upstream review, behavior checks |

For AI applications, also test permission-aware retrieval, prompt injection,
tool authorization, unintended writes, sensitive outputs, and resource exhaustion.
Treat model output and retrieved text as untrusted inputs to privileged actions.

Assign each concrete finding an owner and disposition. Link to the code or
configuration implementing the control. This worksheet is not a security certification.
