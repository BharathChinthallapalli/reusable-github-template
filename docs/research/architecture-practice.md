# Architecture and solutions engineering research

Read on 2026-09-09. This is a bounded source review for the reusable template,
not a claim to have read entire books, the complete Microsoft framework, or the
complete GitLab handbook. Recommendations below are original synthesis. No book
chapters, source diagrams, or external templates are copied.

## What should change

The existing `architect` agent already discovers repository boundaries, compares
options, respects ADRs, and proposes implementation and rollback. Preserve that
working role. The missing capabilities are measurable architecture evaluation,
cross-workload strategy, and evidence from discovery through a bounded customer
or internal-user evaluation into an operational handoff.

| Capability | Trigger | Concrete output | Boundary |
| --- | --- | --- | --- |
| Principal architect | A choice affects shared platforms, multiple workloads, or repeated organizational decisions | Strategy record: evidence from existing decisions, common constraints, exceptions, owners, migration sequence, and reconsideration conditions | Advisory scope; no authority to override accepted ADRs, owners, access controls, or funding |
| Solution architect | A workload needs a new boundary, integration, migration, or consequential design | Existing architect extended with a compact solution packet and measurable quality scenarios | Do not create a second agent that merely repeats the existing architect |
| Solutions engineer | An unclear business request needs discovery, a demonstration, feasibility proof, or adoption handoff | Discovery brief, evaluation agreement, evidence matrix, and operational handoff | Outcome validation is distinct from architecture approval and production readiness |
| Architecture evaluation skill | Alternatives differ in availability, security, cost, change effort, or other significant qualities | Scenario table and option comparison with risks, uncertainty, and disconfirming evidence | A lightweight review inspired by ATAM is not a certified/full ATAM evaluation |

This division is an inference from the sources, not a universal job-title standard.
Will Larson describes the architect's enduring technical-domain responsibility;
Microsoft describes workload lifecycle responsibilities; GitLab supplies a field
evaluation practice. Roles should be selected for these different tasks, not run
as a compulsory hierarchy on every edit.

## Original assets to implement

### 1. Quality scenario and option assessment

Use one row per consequential runtime, failure, or change scenario:

`id | business outcome | trigger/source | affected boundary | operating condition |
required response | measurement and threshold | evidence/test | owner | status`

Include a normal case and the failure or change case that differentiates the
options. Unknown thresholds stay unknown with an evidence-gathering next step;
the agent must not invent SLOs, traffic, budget, or recovery targets.

For each feasible option, record: hard constraints met/failed/unknown; affected
scenarios; implementation and operating effort; uncertain assumptions; new failure
modes; recovery and migration; and what observation would reverse the choice.
Reject violations of hard constraints before weighted preference scoring.
Weights, if useful, must have a stated rationale; a score is not proof.

SEI's ATAM description supports scenario-based analysis of architectural choices,
interacting qualities, and business-threatening risks. arc42 makes quality
requirements measurable and covers both use and change scenarios. This template
asset is a reduced practical application, not a reproduction of either method.

### 2. Solution packet for the existing architect

Keep the package small and linked rather than copying overlapping prose into ADR,
ADD, and architecture documents. Record outcome and constraints, actual system
context, ownership and trust boundaries, interface/data contracts, relevant
runtime and deployment views, significant decisions, verification, and operations.
Show observed and proposed systems separately. Link accepted ADRs; use the ADD
only for its existing agent-change gate responsibility.

Routine, exceptional, and recovery operations need concrete answers: who can
operate the system, what signal reveals a problem, where the runbook lives, what
can be restored, and how recovery is demonstrated. Record RTO/RPO only when
relevant and established, and distinguish a documented design from a successful
recovery exercise. Microsoft's architecture specification explicitly includes
contracts, compatibility, rollout/rollback, testing, monitoring, and recovery.

### 3. Strategy record

`recurring problem | source decisions/incidents | workloads affected | constraints |
proposed common approach | exceptions | accountable owner | migration slices |
adoption evidence | cost of change | review trigger`

Use this only where repository evidence demonstrates a recurring or shared
problem. A single application does not require an enterprise strategy. Distinguish
the current common pattern from the proposed standard. Exceptions must state
their reason and scope rather than silently weakening the rule for all workloads.
Larson's strategy guidance supports extracting direction from specific designs,
keeping templates simple, and stopping when further analysis delays useful work.

### 4. Discovery, evaluation, and handoff

Discovery record: user and task; current workflow; concrete pain/example; existing
baseline and evidence; desired outcome; constraints and dependencies; decision
owner; unverified assumptions; smallest next validation.

Evaluation agreement: hypothesis; representative use cases and data; measurable
pass/fail criteria; baseline; environment and access prerequisites; owner;
time/cost bounds; evidence capture; stop conditions; decision date.

Result matrix: criterion; observed result; evidence link; environment/version;
pass/fail/inconclusive; limitation; follow-up owner. A demo proves only the tested
flow. Synthetic data, mocked integration, and absent operational checks are made
explicit. Lack of evidence is inconclusive, not a successful evaluation.

Handoff record: proven behavior; unproven assumptions; remaining production work;
known defects and risks; setup/reproduction instructions; service ownership;
monitoring and runbook links; credentials/access obtained through approved paths;
rollback/recovery; outstanding decision and next owner. Reuse existing bounded
experiments and release skills instead of introducing competing execution loops.

The GitLab POV page is explicitly marked a **working draft** at review time.
Its transferable practice is an outcome-led, time-bounded evaluation with named
ownership and measurable criteria, not GitLab-specific commercial rules. The
Microsoft collaboration article distinguishes experimental PoC evidence from
production code and calls for implementation feedback and intentional debt.

## Critical review of the proposal

- **Duplication:** Keep `architect`; add specialized strategy/evaluation assets and
  a solutions-engineer task role. A separate solution-architect role with identical
  tools and outputs would increase selection ambiguity without adding capability.
- **Document burden:** Add only sections needed by a consequential decision. A
  correction to README wording does not need a solution packet or quality tree.
- **False authority:** Named architect roles cannot approve themselves into new
  permissions or turn a sealed ADD into human approval.
- **False rigor:** Multiple perspectives should produce distinct counterexamples
  or evidence; repeated agreement from differently named agents is not validation.
- **Platform bias:** Azure details load when Azure is in the project. Portable
  architecture assets should remain usable without Azure, GitLab, or Cloudflare.
- **Operations gap:** Require an owner and evidence for the handoff, not just a
  diagram. A recovery plan and an executed recovery exercise are separate states.
- **Novelty bias:** The simplest feasible extension is a comparison option. Domain
  patterns and additional abstraction are adopted only for demonstrated pressure.

## Exact source coverage

| Source | Material actually read | Applied lesson |
| --- | --- | --- |
| [Microsoft architect fundamentals](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/fundamentals) | Article body: responsibilities and guiding principles; updated 2025-12-09 | Workload lifecycle, business outcomes, supportability, decisions and tradeoffs |
| [Microsoft business requirements](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/design-business-requirements) | Listen, probe, clarify, evaluate, recommend sections | Separate a requested implementation from the underlying need; clarify constraints before service choice |
| [Microsoft architecture specification](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-design-specification) | Complete substantive article: technical specification, recovery, security documentation, consistency | Contracts, compatibility, rollback, tests, monitoring, linked design artifacts |
| [Microsoft collaboration](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/collaboration) | Complete substantive article; updated 2026-04-15 | Risk-first implementation, design feedback, PoC limitations, debt and platform ownership |
| [SEI ATAM collection](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) | Method overview, challenges, nine-step description, results and benefits; not every linked report | Scenario-driven architecture tradeoffs, uncertainty and risk themes |
| [arc42 overview](https://arc42.org/overview/) | Twelve-section overview and tailoring guidance | A small selected set of architecture views, linked decisions and risks |
| [arc42 quality requirements](https://docs.arc42.org/section-10/) | Sections 10.1 and 10.2 including scenario forms | Specific measurable runtime and change acceptance criteria |
| [C4 diagrams](https://c4model.com/diagrams) | Full short diagrams overview | Select views by audience and purpose; all four abstraction levels are not mandatory |
| [Staff Engineer: archetypes](https://staffeng.com/guides/staff-archetypes/) | Author-hosted guide, especially Architect section and distinctions between archetypes | Domain responsibility grounded in business and code; titles do not supply organizational authority |
| [Staff Engineer: engineering strategy](https://staffeng.com/guides/engineering-strategy/) | Author-hosted introduction, when/why, and design-document recommendations through “Prefer good over perfect” | Build strategy from concrete decisions and keep documentation proportionate |
| [Software Architecture in Practice, fourth edition](https://www.informit.com/store/software-architecture-in-practice-9780136886099) | Publisher description and displayed table of contents; not the full book | Bibliographic verification and topic coverage only |
| [Publisher sample: mobile systems](https://www.informit.com/articles/article.aspx?p=3131593) | Sample page 1: introduction, energy monitoring and throttling; not all eight pages | Resource constraints and lifecycle shape design; do not assume fixed-platform conditions in a portable template |
| [Architecture Patterns with Python: Domain Modeling](https://www.cosmicpython.com/book/chapter_01_domain_model) | Author-hosted chapter through domain language, behavioral test examples, value objects, and entities; not the full book | Concrete domain examples expose invariants; patterns should serve real domain complexity |
| [Microsoft ISE design reviews](https://microsoft.github.io/code-with-engineering-playbook/design/design-reviews/) | Complete substantive article, excluding unrelated navigation links | Review tradeoffs before expensive implementation; bound debate; keep design evidence with code |
| [GitLab solutions architect handbook](https://handbook.gitlab.com/handbook/solutions-architects/) | Key Attributes for Positioning Value section, not entire handbook | Discovery precedes a targeted demonstration and evaluation |
| [GitLab POV playbook](https://handbook.gitlab.com/handbook/solutions-architects/playbooks/pov/) | Working-draft status, executive summary, section 1, standard model introduction | Outcome, scope, owner, criteria, and decision date for an evaluation |
| [GitLab technical discovery](https://handbook.gitlab.com/handbook/solutions-architects/processes/technical-discovery/) | Public page contains only a linked Google document; that document was not read | No substantive discovery claims attributed to this pointer page |

The Microsoft pages include a generic authorization banner in extracted page
chrome, but their substantive public article bodies were returned and read. No
authentication bypass was attempted. arc42 and C4 have attribution/share-alike
licensing notices; this proposal links to their concepts and writes original
assets instead of importing templates or diagrams.
