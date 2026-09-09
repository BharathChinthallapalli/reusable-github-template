# Build a useful trace

Follow one user-visible operation through the repository before describing the
whole system. Expand only when another boundary affects the task.

First classify the repository area from manifests, entrypoints and consumers.
More than one classification may apply; record which unit the task changes.

| Repository shape | Evidence that determines the change boundary |
| --- | --- |
| Single application or library | Entrypoint/public API, composition and consumers; distinguish application runtime from repository-maintenance tools |
| Collection of independent examples | Per-example manifests, README prerequisites and entrypoints; a root index does not establish shared runtime dependencies or root CI coverage |
| Multi-package workspace | Workspace/build configuration, package dependency graph and shared contracts; identify both affected package checks and integration consumers |
| Notebook or exploratory analysis | Cell order, hidden/imported state, data source and outputs; saved cell output is not proof of execution against current inputs |
| Course or educational repository | Exercise/solution boundaries, lesson-specific assumptions and setup; distinguish an illustrative implementation from a maintained deployment contract |
| Generator or generated consumer | Authoritative source/template, generation command and consuming package/runtime; determine which generated outputs must be committed and verified rather than assuming all generated files are disposable |
| Documentation or specification | Build/link checks, code examples, schemas and downstream consumers; identify executable instructions or normative contracts before treating a prose change as cosmetic |

Do not infer architecture or readiness from the owner's reputation, repository
name or a framework used by a neighboring example. For a large collection,
record inspected paths and exclusions; a repository inventory is not a complete
source audit. In a workspace, trace shared interfaces before expanding edits
across packages. For notebooks, verify only through the authorized environment
and state when the data or execution path was unavailable.

| Question | Evidence to inspect |
| --- | --- |
| What starts execution? | Route registration, main function, command mapping, workflow trigger |
| What interprets input? | Handler, schema, parser and validation calls |
| Who may perform the action? | Authentication middleware, authorization check and tenant filter |
| What changes or leaves the process? | Storage adapter, queue producer, outbound client and transaction |
| What observes the result? | Return type, response mapping, event consumer and behavioral test |
| Which versions are selected? | Runtime files, dependency constraints, lockfile and CI setup |
| What do domain terms mean here? | Scoped definitions, owner decisions, code usage and examples |
| What must callers know? | Public inputs/outputs, invariants, errors, side effects and contract tests |
| Which constraints justify a change? | Measured workload/access patterns, agreed targets, incident evidence and dated assumptions |

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

An ADR's date does not establish precedence. Read status and supersession links,
then check scope and assumptions. An index may be stale; unresolved conflicts
between Accepted decisions need investigation and an explicit resolution.

For a bottleneck claim, identify the operation, observed symptom, measurement or
reproduction, and expected improvement. If measurements are unavailable, propose
the smallest useful check and label the diagnosis as unverified. Do not fill in
latency, availability, traffic, or budget numbers from a typical system.

Deliver a compact map of the relevant entrypoint, calls, boundaries and checks;
include unresolved questions only when they affect the proposed work.
