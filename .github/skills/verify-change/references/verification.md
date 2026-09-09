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

For a regression, capture a minimal reproducer or behavioral test. Where
practical, show that it fails for the relevant reason before the fix and passes
afterward. Do not disturb the user's working tree to obtain this comparison.

When checks fail, record the failing command, exit status and concise error
evidence. Classify the cause as a demonstrated regression, an established
baseline failure, an environment blocker or an unresolved cause. An untested
guess that the failure predates the change is not a baseline result.

Do not run deployment, production writes or paid external requests merely to
validate a local change. Use authorized test environments and state the limit
when an integration cannot be exercised. Stop when required gates and the
remaining credible risks are sufficiently addressed.
