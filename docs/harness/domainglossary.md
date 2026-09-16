# Harness domain glossary

Canonical vocabulary for this development harness. Application business terms
belong in [project context](../project.md#domain-terms); the same word can have a
different meaning there. Read the relevant section, not the entire glossary,
when clarifying a task. Definitions describe concepts; they grant no authority.

## How to use and maintain terms

- Use the canonical term in specs, interfaces, tests and handoffs. Qualify an
  overloaded word, such as *agent host*, *project scope* or *business approval*.
- Follow the linked contract for exact fields, states and behavior. A glossary
  summary does not supersede that contract or an accepted ADR.
- Add a term when its meaning changes naming, behavior, ownership or acceptance.
  Give its scope, definition, source/owner and a useful distinction or example.
- Keep aliases with the canonical entry. Do not silently rename an API, enum or
  stored field to match prose; contract migrations require their own change.
- Mark unresolved meanings explicitly and identify who must resolve them. Mark
  proposed concepts as proposed; a definition is not implementation evidence.
- When behavior changes, update its contract and affected glossary entry together.
  The harness maintainer reviews harness meanings; the domain owner reviews
  business meanings. No separate glossary approval gate is introduced.

## System and participants

Source: [AI assistance](../ai-assistance.md), [catalog](../ai-catalog.md) and
[engineering workflows](../engineering-workflows.md).

| Term | Meaning in this harness | Boundary or common confusion |
| --- | --- | --- |
| Harness | Repository guidance, reusable procedures, checks and host integrations that support development. | Distinct from the application being built and the model doing reasoning. |
| Control plane | The harness's intended coordination of scope, decisions, checks and evidence. | A design description, not proof of a deployed central service. |
| Template | A reusable starting snapshot for a new repository. | Updating this repository does not automatically update its consumers. |
| Project | A maintained software outcome with users, an owner and an actual technical context. | May span repositories; it is not a chat session. |
| Application | The software a project delivers to its users. | Python repository tooling does not select the application's stack. |
| Model | The inference system used for reasoning or generation. | A model name conveys neither permissions nor a verified workload identity. |
| Agent | A running model/tool workflow pursuing a bounded task. | A role definition on disk does not start a running agent. |
| Agent profile | A stored role, instructions and host-supported tool configuration. | Called a custom agent by some hosts; it is not an authenticated person or service. |
| Host / runtime | The client that loads configuration and executes the agent's tools. | In these docs, usually the agent host; qualify *application runtime* separately. |
| Surface | A particular host entrypoint, such as CLI, editor extension or cloud session. | Evidence for one surface does not establish another surface's behavior. |
| Session / run | A bounded execution period with its available context and identity. | Durable project state must survive beyond the session. |
| Contributor / implementer | A person or agent making the scoped change. | Contributing is distinct from owning acceptance or release decisions. |
| Project owner | The accountable person or team defining application outcomes and consequential decisions. | A role label does not itself grant GitHub or Azure privileges. |
| Maintainer | The person or team accountable for the relevant repository's contracts and integration. | Distinguish harness maintainer from adopting-project maintainer. |
| Reviewer | A person or agent examining a change against its contract and evidence. | A review finding is not automatically human approval or deployment permission. |
| Skill | A reusable task procedure with a specific trigger and optional supporting assets. | Distinct from an always-loaded instruction, an executable tool or a permission. |
| Tool | A callable operation exposed by the host or an integration. | Its availability is not authorization for every possible invocation. |
| MCP server | An integration exposing capabilities through Model Context Protocol. | Naming one in a document does not register, authenticate or authorize it. |

## Intent, scope and delivery

Source: [SDLC purpose](../sdlc-template-purpose.md),
[planning](../../.agents/skills/implementation-planning/SKILL.md),
[orchestration](../../.agents/skills/task-orchestration/SKILL.md) and
[decision process](../adr/README.md).

| Term | Meaning in this harness | Boundary or common confusion |
| --- | --- | --- |
| Purpose | The users, job and observable outcome that justify a project. | Describes why the work matters; the current application home is `docs/project.md`. |
| Vision | The intended long-term experience and direction. | Does not describe all currently implemented capabilities. |
| Goal | An outcome with acceptance evidence. | A feature or document count alone is not a user outcome. |
| Non-goal | A deliberate boundary on what the harness seeks to do. | Different from useful work deferred for lack of prerequisites. |
| Philosophy | The reasoning used to assess design tradeoffs. | An explanatory lens, not another permissions system. |
| Opinion | A revisable judgment about a useful default. | Becomes a durable contract only through the applicable decision process. |
| Initiative | A broader business problem and expected outcome. | Usually decomposes into several features. |
| Intent | A statement of a desired change and why it matters. | The master prompt proposes a formal `intent.md` workflow; that automation is not supplied here. |
| Feature | One useful behavior with a bounded specification. | May require several tasks and PRs. |
| Specification / spec | An agreed description of behavior, constraints and acceptance. | This harness spec is an overview; a feature spec defines a particular change. |
| Requirement | A behavior or constraint that can be assessed against evidence. | Not the design mechanism chosen to satisfy it. |
| Acceptance criterion | An observable condition for accepting the outcome. | Writing a test or passing a build does not alone establish user success. |
| Task | A bounded unit of work with inputs, dependencies, output and stopping condition. | Can be an investigation whose honest result is inconclusive. |
| Scope | The authorized boundary of the current work. | Distinguish task files, project boundary and runtime-enforced access. Prose scope is not OS confinement. |
| Change / PR | A reviewable implementation increment and its evidence. | A PR can be prepared or merged without its application being deployed. |
| Roadmap | The proposed order and dependencies of future outcomes. | Not an instruction to execute every item or a promise of dates. |
| Worktree | A separate Git working tree used for isolated repository work. | Prevents some edit collisions; it is not a security sandbox. |
| Handoff | A concise continuation record: revision, completed work, evidence, blockers, ownership and next action. | Not a transcript or a substitute for current code. |
| Release | Identified software artifacts and relevant configuration prepared for delivery. | Distinguish release preparation, deployment and observed operation. |
| Deployment | Applying an identified release/configuration to a particular environment. | Requires target-specific authorization and verification. |

## Contracts, evidence and controls

Source: [ADD contract](../add/README.md), [tool guide](../repository-tools.md),
[Guardian](../guardian.md) and [Guardian validation](../research/guardian-validation.md).

| Term | Meaning in this harness | Boundary or common confusion |
| --- | --- | --- |
| Canonical source | The maintained home of a particular fact or contract. | Linked summaries are navigation, not competing authorities. |
| ADR | Architecture Decision Record: context, options, decision, status and consequences. | Proposed or superseded records do not override a current accepted contract. |
| ADD | Agent Design Document: purpose, behavior, permissions, exact protected-file scope and verification. | Means **Agent**, not Architecture, Design Document in this repository. |
| Ready / sealed design | A structurally ready ADD, with sealing binding its record to specified file contents. | Structural readiness and a current hash do not prove design quality or human approval. |
| Invariant | A property that must remain true across relevant operations. | An invariant needs checks at its actual boundary, not only a sentence in a prompt. |
| Evidence | A source or observed result supporting a scoped claim. | Record revision/environment; distinguish inspected code from an executed check. |
| Baseline | The recorded starting conditions and results for a comparison. | Not an assumed performance level or an undocumented earlier run. |
| Regression | A previously satisfied behavior that fails after a change under comparable conditions. | A pre-existing failure is not automatically introduced by this PR. |
| Evaluation / eval | A defined assessment of model or system behavior against cases and criteria. | Checking an evaluation report's schema does not run the model or authenticate its scores. |
| Policy | Rules deciding permitted behavior at a specified boundary. | Distinguish prose guidance, executable policy and deployed enforcement. |
| Gate | A check or decision that must succeed before a particular transition. | Name the transition and enforcing component; a checklist is not automatically enforced. |
| Hook | A host- or Git-invoked lifecycle handler. | Coverage, activation, failure and timeout behavior depend on its actual integration. |
| Sandbox | An execution boundary restricting accessible resources or effects. | A worktree, prompt or path-checking hook alone does not establish OS isolation. |
| Guardian | The staged shared command-policy engine, adapters, signed-review integration and ledger. | The reviewer does not execute commands; production integration has explicit prerequisites. |
| HARD_DENY | Guardian classification for prohibited effects, malformed input or unsupported syntax. | A review token cannot override it. |
| AUTO_ALLOW | Guardian classification for narrowly recognized side-effect-free diagnostics. | Still subject to the documented ledger and independent host controls. |
| IN_SCOPE | Guardian classification requiring the documented review for supported operations. | The name does **not** mean already authorized or approved. |
| Review approval / approval token | A Guardian review decision and its authentic signed, expiring, request-bound, single-use proof. | Not business acceptance, GitHub merge approval or an override of host permissions. |
| Issuer | The separately protected signing authority for authentic Guardian approval tokens. | A working agent cannot mint its own authorization; the production boundary must be deployed. |
| Identity | Authenticated actor information appropriate to the operation. | A display name, agent profile or worker-supplied claim is insufficient. |
| Ledger | The current local JSONL Guardian decision history with linked hashes. | Distinct from project memory; durability and tamper resistance need the documented external protections. |
| Pivot attempt | A detected attempt to retry a denied objective through another request or surface. | Detection covers documented hashes/effect families, not proof of all semantic equivalence. |
| False denial | A permitted operation rejected under the intended policy and actual prerequisites. | An expected denial for absent required authorization is not automatically a false denial. |
| Residual risk / coverage gap | A failure mode that the available controls or evidence do not resolve. | Record it explicitly; an absent alert does not establish safety. |
| Native acceptance | Observed behavior on the actual installed host/surface and version. | Synthetic envelope/fixture tests establish a different, narrower claim. |

## Proposed vocabulary from the master prompt

Source: owner-supplied *HARNESS MASTER PROMPT*, version 2026-09-16. The following
meanings describe proposed work, not active services or established enforcement.
See [roadmap](roadmap.md) before relying on their implementation status.

| Proposed term | Intended meaning and boundary |
| --- | --- |
| Core / supporting / helper | Purpose-relative classes: necessary user behavior; work making it faster/safer; optional assistance. Classifying a task does not implement automatic priority enforcement. |
| Wave | A bounded dependency-compatible set of tasks, followed by review before further work. No automatic wave scheduler is asserted. |
| Definition of Ready / DoR | Admission criteria for an implementable task. The master prompt's full rubric is not a shipped admission service. |
| Signed scope / scope compiler | An approved machine-readable boundary and a deterministic translator into host-specific restrictions. Do not confuse these with the existing ADD fingerprint. |
| Scoper | Proposed reviewer-side preparation of that scope for human acceptance. Not a currently registered service. |
| Capture | A recorded finding or emergent need kept outside the current task until triaged. A named capture command is not supplied by this glossary. |
| Monitoring bands | Proposed thresholds for observing, diagnosing or proposing action from operating metrics. Values need workload evidence. |
| Bookkeeper | Proposed independent reconciliation of audit, scope and control evidence. Not an implemented scheduled auditor. |

## Application domain vocabulary

Keep business definitions in [project context](../project.md#domain-terms), or
link one project-owned glossary from that section when it grows. Do not mix
customer records or business approval states into the Guardian policy vocabulary.

For each business term, record **term and aliases; bounded domain; definition;
invariant or behavior; example/counterexample; owner or source; status**. Keep
unknown definitions unresolved. For example, *approved trial revision* could
mean a reviewer accepted an exact version of a trial record; it would not mean
that data was already published downstream. This is an illustrative distinction,
not a confirmed contract for an application in this template.
