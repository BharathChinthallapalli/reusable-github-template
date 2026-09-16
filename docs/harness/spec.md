# Harness specification

Scope: repository-level capability and acceptance map. Reviewed 2026-09-16
against `25c38b3fd557376b854537b7b02982d99c4a4090` and the accompanying
documentation change. This is not a feature implementation plan or proof of
deployment. Runtime/version details remain in their linked canonical contracts.

## Actors and boundary

The project owner supplies the outcome and consequential decisions. Contributors
(people or agents) inspect, implement and leave evidence. Reviewers assess the
actual change. Hosts execute tool calls under their own permissions. Guardian's
reviewer and protected issuer have distinct responsibilities; see the
[glossary](domainglossary.md) and [Guardian contract](../guardian.md).

The harness supplies repository conventions, reusable procedures and tooling.
Application behavior, cloud resources, live repository settings and deployed
trust boundaries require their own implementation and acceptance.

## Current contract and acceptance map

| ID / goals | Required behavior | Canonical mechanism and verification boundary |
| --- | --- | --- |
| H1 / G1, G2 | Initialization previews its declared edits and refuses incompatible reinitialization. | [Initializer](../../tools/initialize.py), [setup](../using-the-template.md), [tests](../../tests/test_initialize.py). Initialization does not provision GitHub or Azure. |
| H2 / G1, G3 | Select relevant local procedures and references for the actual task. | [Task routes](../engineering-workflows.md#choose-the-task-route), [catalog](../ai-catalog.md), [AI diagnostics](../ai-assistance.md). Static validity, host discovery and observed invocation are separate checks. |
| H3 / G2 | Verify the foundation independently from application correctness. | [Repository checker](../../tools/check_repository.py), [CI](../../.github/workflows/ci.yml), [tool guide](../repository-tools.md). Passing foundation checks cannot substitute for application acceptance. |
| H4 / G2, G4 | Protected agent/hook changes have explicit design scope and accurate file bindings. | [ADD contract](../add/README.md), [design checker](../../tools/check_design.py). Ready/sealed identifies a bound design, not permission or human approval. |
| H5 / G4, G6 | Guardian applies its shared policy to supported requests and requires authentic review where specified. | [Engine and integration contract](../guardian.md), [validation record](../research/guardian-validation.md). Production issuer, identity, managed deployment and native interception remain separate prerequisites. |
| H6 / G5 | A bounded change records its outcome, dependencies, verification and useful continuation state. | [Change plan](../../.agents/skills/implementation-planning/assets/change-plan.md), [handoff](../../.agents/skills/task-orchestration/assets/task-handoff.md), [context refresh](../../.agents/skills/context-maintenance/assets/context-refresh.md). These are procedures/assets, not an automatic memory service. |
| H7 / G7 | Delivery readiness is established for an actual project and target. | [SDLC purpose](../sdlc-template-purpose.md), [operations](../operations.md), [Azure delivery](../azure-delivery.md). The foundation does not ship a deployed application. |
| H8 / G8 | Harness terms have scoped definitions; application facts retain their project owner. | [Domain glossary](domainglossary.md) and [project context](../project.md#domain-terms). Review definitions against their linked contract; link checks do not establish semantic consistency. |

## Documentation contract

The eight pages have distinct jobs: [vision](vision.md) describes direction;
[goals](goals.md) define success; [non-goals](nongoals.md) set boundaries;
[philosophy](philosophy.md) explains the design lens; [opinions](opinion.md)
record revisable judgments; this specification maps behavior;
[roadmap](roadmap.md) sequences work; [glossary](domainglossary.md) owns terms.
They are read on demand, not imported as an always-on bundle.

Preserve [AGENTS.md](../../AGENTS.md), applicable accepted ADRs and the actual
runtime controls. A roadmap entry cannot authorize execution; a glossary entry
cannot implement a gate. If code and an accepted contract disagree, record and
resolve the discrepancy rather than silently treating either as corrected.

## Proposed extensions and unresolved evidence

The owner-supplied *HARNESS MASTER PROMPT*, version 2026-09-16, is design input.
Its signed scope compiler, broader lifecycle automation, Rust gate, monitoring
bands and bookkeeper are not implemented by these pages. Existing Guardian code
is Python with host adapters. A proposed replacement still needs implementation
and verification. Use [roadmap](roadmap.md) for reviewable next increments.

Completion of this documentation change means all eight pages are discoverable,
local links resolve, terms distinguish current from proposed concepts, and the
existing repository/design/catalog checks retain their contracts. Runtime,
endpoint, cloud and application acceptance are outside this documentation change.
