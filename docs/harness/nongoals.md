# Harness non-goals

Scope: boundaries for the [vision](vision.md). A deferred roadmap item is not
automatically a non-goal; it may still be useful once its prerequisites exist.

| Non-goal | Boundary and implication |
| --- | --- |
| Autonomous ownership of business decisions | Agents contribute evidence and changes. They do not impersonate an owner, sign off for a person or manufacture authorization. |
| Guaranteed correctness, confinement or compliance | Repository guidance, fixture tests and local hooks cannot establish every host's behavior, OS isolation, legal compliance or production readiness. |
| A universal application architecture | Keep the base reusable. Select frameworks, data stores, providers and deployment resources from the actual project need. |
| Rebuilding working systems for aesthetic uniformity | Preserve useful behavior. Renames, abstractions and migrations need a concrete benefit and acceptance evidence. |
| Loading every document into every session | Route to the current task's contracts and glossary sections; avoid repeating the entire harness in each agent profile. |
| A mandatory agent organization chart | Add or delegate a role when its distinct task warrants it. Agent count is not a quality metric. |
| An ever-growing memory transcript | Maintain current facts and resumable task state. Keep historical rationale identifiable without treating old conversation as current policy. |
| A new project-management platform | Use versioned files and existing GitHub collaboration until a demonstrated workflow needs more machinery. |
| Replacing host permissions or endpoint controls | A repository decision cannot override the host, tenant, OS or security owner. A missing integration is a gap to resolve. |
| One-pass generation of an entire production system | Deliver bounded features, integrate them, and verify actual operations on the selected environment. |
| Mandatory completion of all templates for every edit | Apply documentation and review proportionately; preserve the existing protected-path design gate. |
| Automatic changes to adopting repositories | Adoption is an explicit, reviewed migration that preserves project-specific facts and behavior. |

To reconsider a boundary, record the user need, smallest alternative, cost and
acceptance evidence. Use the [decision process](../adr/README.md) if the change
would alter an accepted contract. A proposal or [opinion](opinion.md) does not
silently change that contract.
