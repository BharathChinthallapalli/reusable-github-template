# Build a useful trace

Follow one user-visible operation through the repository before describing the
whole system. Expand only when another boundary affects the task.

| Question | Evidence to inspect |
| --- | --- |
| What starts execution? | Route registration, main function, command mapping, workflow trigger |
| What interprets input? | Handler, schema, parser and validation calls |
| Who may perform the action? | Authentication middleware, authorization check and tenant filter |
| What changes or leaves the process? | Storage adapter, queue producer, outbound client and transaction |
| What observes the result? | Return type, response mapping, event consumer and behavioral test |
| Which versions are selected? | Runtime files, dependency constraints, lockfile and CI setup |

Distinguish three kinds of statement:

- **Observed:** a cited file or symbol directly establishes the statement.
- **Inferred:** evidence suggests it; state the missing runtime or configuration
  fact that would confirm it.
- **Unknown:** evidence is absent or inaccessible; avoid filling the gap with a
  common architecture pattern.

Example: a storage interface and a blob adapter prove an available integration.
They do not prove that production selects that adapter. Find the composition
root and configuration selection before claiming the active storage backend.

Treat documentation as a claim to compare with code. Generated files, fixtures
and abandoned modules may describe paths that are never executed. Resolve
contradictions explicitly and cite the evidence supporting the current path.

Deliver a compact map of the relevant entrypoint, calls, boundaries and checks;
include unresolved questions only when they affect the proposed work.
