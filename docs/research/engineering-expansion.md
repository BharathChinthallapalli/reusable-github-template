# Version 3.1 engineering expansion

The user requested broader agents and skills from `asw101/gh-aw` and
`microsoft/azure-skills`, including documentation writing, plus principal and
solution architecture and solutions engineering practice. This release adds ten
skills and three profiles, extends existing procedures, and preserves the v3.0
initializer, CI and hook contracts. The resulting catalog has **34 skills and
13 profiles**. Catalog size is inventory, not a quality score.

## Sources and scope

| Source | Exact scope | Limits |
| --- | --- | --- |
| [gh-aw fork review](gh-aw-skills.md) | Pinned February 2 revision; complete tree, 24 top-level skills plus one GitHub skill, eight profiles, developer instructions, all 149 workflow purposes; 204 retrieved definitions/consumer/test files | Selected semantic and consumer traces; no upstream code executed; dated fork is not current upstream |
| [Azure Skills review](azure-skills.md) | Pinned September 9 revision; all 28 canonical families and 38 entrypoints including nested phases; three additional graph-plugin families; 925 mirrored payload blobs compared | Entry-point screening plus selected detailed procedures/scripts; no cloud operations or native skill invocation |
| [Architecture practice](architecture-practice.md) | Microsoft workload design, SEI, arc42/C4, author-hosted Staff Engineer and Cosmic Python material, publisher sample and field evaluation guidance | Exact excerpts and article coverage recorded; no full-book or complete-framework claim |

## Shipped additions and acceptance behavior

| Requested or observed capability | Implementation | What should change in a real task |
| --- | --- | --- |
| Technical documentation writer | `documentation-writing`, `documentation-writer`, [documentation guide](../documentation.md) | Produce the needed document type, trace claims to code, verify the reader's actual path and distinguish prose/build/runtime checks |
| Solution discovery and proof | `solution-discovery`, `solutions-engineer` | Establish a real task and baseline, agree a bounded evaluation, implement or demonstrate the smallest useful slice and report limitations |
| Workload architecture | `solution-architecture`, enhanced existing `architect` | Connect requirements to actual/proposed interfaces, measurable quality scenarios, delivery and operations |
| Specification authoring | Specification mode in the design method and packet | Identify consumers, normative requirement IDs, failure/version behavior and requirement-to-check evidence |
| Principal architecture | `architecture-review`, `principal-architect` | Compare cross-system consequences, shared constraints, scoped exceptions and migration; return evidence-backed advice without inventing authority |
| Operational handoff | `operational-readiness` and existing release delivery | Separate working demo, deployed artifact, observed critical path and operational ownership/recovery evidence |
| Azure preparation | `azure-prepare` | Detect current stack, preserve its deployment tool and prepare the missing or changed plan/IaC/configuration |
| Azure validation | `azure-validate` | Record actual static/local/live checks with artifact/environment identity; keep missing access and stale evidence explicit |
| Azure delivery | `azure-deploy` within `release-delivery` | Execute the authorized target using current evidence, verify effects, diagnose bounded failures and hand off |
| Azure inventory | `azure-resource-discovery` | Discover scoped live resources with pagination and provenance; distinguish observed relationships from inferred topology |
| GitHub Agentic Workflows | `agentic-workflow-development`, [authoring guide](../agentic-workflows.md) | Separate workflow intent, selected compiler/engine, compiled output and actual run/effect; define bounded no-change and failure behavior |

## Extended existing capabilities

| Finding | Existing capability strengthened |
| --- | --- |
| Repeated instructions and skill extraction need consumer evidence | Context maintenance traces shared knowledge, callers, source revision and factual drift before consolidation |
| Multi-run campaigns need bounded scope and duplicate control | Task orchestration adds finite target sets, identity, output/time/cost bounds and explicit no-change results |
| Large GitHub queries can waste context and conceal partial scope | Evidence research requests relevant fields, follows pagination and distinguishes ranked matches from complete inventories |
| Schemas, parsers, examples and docs drift independently | Interface validation adds requirement-to-consumer evidence and compatibility/error cases |
| Azure diagnosis needs environment and first-cause evidence | Systematic debugging adds a conditional service-diagnosis reference |
| Billing estimates and optimization measurements differ | Performance analysis adds scoped actual/amortized/forecast/estimate semantics and savings evidence |
| Cloud identity and tools are not created by skill text | Security and tool integration add scope/discovery/invocation distinctions and conditional Azure references |
| Agent traces and evaluation datasets need provenance | AI evaluation and data contracts add environment/version lineage, redaction, deduplication and held-out-case boundaries |

The [Azure capability map](../azure-capabilities.md) accounts for specialist
families through bundled procedures or a source route with explicit limits. A
source route is not a claim that a provider-specific workload is implemented.

## Choices deliberately not copied

Do not turn the fork's 149 workflows into 149 scheduled jobs. They include
repository-specific tooling, demos, personas, external services and outputs that
need their own product scope. Preserve the useful authoring and operating contract.
The recipe is inactive until a project chooses and validates its runtime.

Do not copy deprecated agent metadata, forced models, broad command/network
allowlists, automatic issue/comment creation or unchecked output handlers. The
existing host controls and actual task authority remain in effect.

Do not vendor Azure's 925-file mirrored skill payload, `@latest` MCP launchers,
marketing-only tools or unconditional infrastructure criteria into every project.
Use only the relevant current official service documentation, actual host schemas,
workload requirements and authorized target. Preparing a document does not validate
an application or provision its identity.

Do not create a second solution-architect profile that repeats `architect` or a
specialist profile for every service. Distinct outputs and tool boundaries justify
the three additions. Independent review found two concrete acceptance needs:
formal contract mapping and preservation of an existing Terraform delivery path.
The implementation includes both for forward testing.

## Verification categories

The validation record distinguishes deterministic source/initialized-project
checks, independent synthetic or local task exercises, actual GitHub CI, and
unperformed native host/cloud/gh-aw execution. See [VALIDATION.md](../../VALIDATION.md)
and [forward exercises](engineering-validation.md) for observed results and limits.
No model-quality benchmark is inferred from skill-format tests or an agreeing
reviewer. Source code inspection is not execution evidence.
