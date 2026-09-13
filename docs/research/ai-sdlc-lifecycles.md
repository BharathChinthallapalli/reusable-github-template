# AI, LLMOps, ML and specification-driven lifecycles

Research date: **13 September 2026**. Template baseline:
`a94e2a5995803653a5b993c56bd82bb450b130c6`.

Reader: a maintainer responsible for moving an idea into production and operating
it, with limited Git/CI/CD/Azure experience. Decision: how this SDLC template
should support that work through bounded features and specifications.
The [owner's purpose and requirements](../sdlc-template-purpose.md) are canonical.
Here, “MLSLDC” is interpreted as the machine-learning development lifecycle.

**Recommendation:** use one feature/spec delivery loop, with additional evidence
for ML or LLM features when applicable. Project-wide lifecycle support does not
mean whole-project generation by one agent. Multiple agents also need bounded
work, dependency-aware integration and independent acceptance evidence.

The proposed template design below is original synthesis. Sources describe
methods and products; they do not establish that adopting a tool or increasing
agent count will improve this template's delivery performance.

## 1. These terms describe different concerns

| Term | What it concerns | Unit of change and additional evidence |
| --- | --- | --- |
| SDLC | Delivering and maintaining software, from a user need through operations | A feature, repair or technical change; requirements, code, tests, release and runtime evidence |
| AI-assisted / AI-driven SDLC | Using AI during discovery, design, coding, review or operations | The same bounded software change; additionally verify generated claims, context and tool effects |
| AI-system lifecycle | Building a product whose behavior depends on AI | Data/model behavior, affected people, evaluation, operational risks and changing dependencies across the lifecycle |
| ML development / MLOps | Developing, evaluating, delivering and operating trained statistical models | Dataset/label/feature/pipeline/model changes, experiment lineage and evidence beyond passing software tests |
| LLMOps / GenAIOps | Operating applications using generative models, prompts, retrieval and tools | A compatible application/model/prompt/data/tool bundle, quality evaluation, access controls and runtime observations |
| Specification-driven development | Keeping implementation connected to an explicit description of required behavior | One feature spec or coherent slice, mapped to tasks, implementation and acceptance evidence |

These categories can coexist. An agent can help implement a normal application
that contains no AI at runtime. A generative application can consume a model API
without training a model. Fine-tuning adds ML data/training requirements to that
application. A specification-driven approach can organize any of these cases.
“AI SDLC” is used inconsistently; this document separates development assistance
from the lifecycle of the AI product being built.

## 2. AI-assisted and AI-driven SDLC

AWS's AI-DLC methodology groups work into Inception, Construction and Operations.
It describes elaborating business intent into smaller work units, creating code
and design with human input, and retaining context for delivery and operations.
This is one vendor's methodology, not a universal SDLC standard or independent
proof of its productivity claims. Its adaptive workflow also varies process
depth with the task. [AWS method](https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/),
[adaptive workflow](https://aws.amazon.com/blogs/devops/open-sourcing-adaptive-workflows-for-ai-driven-development-life-cycle-ai-dlc/).

DORA's small-batch guidance specifically warns about large AI-generated changes
and delayed downstream feedback. It recommends changes that can be understood,
tested and integrated in small units. Its 2025 report landing page describes AI
as amplifying existing organizational strengths and weaknesses. These findings
support evaluating the delivery process, not equating generated code volume with
successful features. No numerical productivity effect is inferred for this
repository. [Small batches](https://dora.dev/capabilities/working-in-small-batches/),
[2025 report overview](https://dora.dev/research/2025/dora-report/).

**Template adaptation:** agents can research, propose requirements, implement
bounded changes and prepare evidence. The maintainer supplies real business and
company constraints and resolves consequential choices. Instructions should
reuse existing authorization and scale checks to the task. Do not import mandatory
approval at every stage, new terminology for every role, transcript collection,
or an unrestricted whole-backlog execution command.

For AI products, risk work accompanies the lifecycle. NIST's AI RMF Playbook
organizes suggestions under Govern, Map, Measure and Manage and explicitly says
the playbook is not a checklist to execute in its entirety. Use relevant risk
questions in the feature/design/evaluation process, with explicit owners; do not
claim certification from completing Markdown headings. The site notes the
framework is being revised. [NIST Playbook](https://airc.nist.gov/airmf-resources/playbook/).

## 3. Machine-learning development and MLOps

ML includes software delivery, but introduces distinct data, experiment and model
boundaries. Google Cloud distinguishes component/pipeline CI/CD from continuous
training (CT). A training run produces a candidate; evaluation and serving checks
determine whether that candidate is suitable for promotion. Its maturity levels
describe progressively introducing automation, rather than requiring a complete
ML platform at the outset. [Google Cloud MLOps](https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning).

Microsoft's MLOps architecture distinguishes an experimental inner loop from
staging, production and monitoring. Production events can lead to investigation
or another training candidate. Monitoring includes model/data behavior and service
operation; the lifecycle also includes retiring unused models. A drift signal
does not by itself demonstrate that retraining will help.
[Microsoft MLOps architecture](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/machine-learning-operations-v2).

A practical ML feature loop is:

1. Define the business decision, baseline and relevant success/failure measures.
2. Establish permitted data, labels, schema, provenance and an appropriate split.
3. Run a bounded experiment, recording code, data, configuration and environment.
4. Evaluate the candidate against the baseline and important population slices.
5. Test the actual inference interface and promote only with sufficient evidence.
6. Monitor, investigate changes, evaluate a next candidate, recover or retire.

Evaluation data has to remain meaningful. Repeated selection against a test set
implicitly tunes to it; duplicates across training and evaluation can inflate
results. There is no universal split percentage suitable for every workload.
[Google dataset guidance](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets).
Learn preprocessing such as scaling or feature selection from training data only,
then apply it consistently to evaluation and inference inputs. A random seed alone
does not guarantee complete reproducibility.
[scikit-learn pitfalls](https://scikit-learn.org/stable/common_pitfalls.html).

**Template adaptation:** keep “pipeline code verified,” “candidate model
evaluated” and “production model promoted” as distinct claims. An ML section in
the selected feature spec should identify dataset/split revisions, labels,
baseline, evaluation slices, experiment bounds and serving compatibility. A
product feature is a user capability; an ML input feature is an input variable.
Use those terms explicitly when decomposing work.

Reuse [data contracts](../../.agents/skills/data-contracts/SKILL.md),
[bounded experiments](../../.agents/skills/bounded-experiments/SKILL.md),
[AI evaluation](../../.agents/skills/ai-evaluation/SKILL.md) and release/readiness
procedures. Do not require a feature store, managed training platform, model
registry or automatic retraining until the project needs that capability.

## 4. LLMOps and GenAIOps

Microsoft's GenAIOps guidance emphasizes pretrained-model selection, prompts,
grounding and orchestration alongside ordinary application and data operations.
These practices can extend an existing delivery pipeline. Training a foundation
model is not assumed. [Microsoft lifecycle guidance](https://learn.microsoft.com/en-us/azure/well-architected/ai/mlops-genaiops).

Model dependency maintenance is part of delivery. A provider/model update can
require prompt, orchestration or grounding changes. A retired model may no longer
be available for rollback, so recovery may need a tested supported fallback.
[Foundation-model lifecycle](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/manage-foundation-models-lifecycle).

MLflow distinguishes evaluating candidate versions offline from evaluating
sampled production traces online. Curated cases, expectations, human feedback
and trace observations serve different purposes. Production evaluation adds
ongoing evidence; it does not replace pre-release comparisons.
[Evaluation overview](https://mlflow.org/docs/latest/genai/eval-monitor/),
[automatic evaluation](https://mlflow.org/docs/latest/genai/eval-monitor/automatic-evaluations/).
Its current automatic-evaluation feature supports LLM judges, illustrating why
that measurement cannot stand in for deterministic permission or interface tests.
The template does not need to install MLflow to adopt this distinction.

Tool permissions and document access must be enforced by the application, with
identity and authorization propagated through retrieval. Asking a model to hide
restricted information is not access enforcement. Latency, cost and failure
behavior belong in the actual feature contract.
[Microsoft AI application design](https://learn.microsoft.com/en-us/azure/well-architected/ai/application-design).

**Template adaptation:** version and evaluate the affected parts of a feature's
release together:

| Area | Record when applicable |
| --- | --- |
| Application | Code commit, package/container, runtime and dependency identities |
| Model dependency | Provider, model/version or deployment, API version, parameters and fallback policy |
| Prompts and tools | Prompt revision, orchestration, tool schemas, limits and integration versions |
| Retrieval | Source revision, parser/chunking settings, embeddings, index build/schema and retrieval settings |
| Access | Identity and permission-filter implementation/tests; current authorization remains authoritative |
| Evaluation | Dataset/provenance, independent expectations, scorer/judge/rubric version, baseline and candidate results |
| Operations | Target environment, rollout, signals, owner and supported recovery procedure |

Use a bounded cycle: specify one capability; establish baseline cases; compare a
small set of justified candidates; implement; review deterministic and model
evidence; release a compatible bundle; observe the result and open the next scoped
change. An average quality score can hide a critical failure. Keep execution
errors, missing labels and unrun cases separate from model-quality outcomes.

Online evaluation is not online training. Production conversations do not become
training data automatically. Reverting an application or index must not restore
revoked access or deleted sensitive content. Fine-tuning introduces the ML track's
data, split, training and checkpoint evidence. These are design recommendations
for this template, not claims of a currently deployed AI system.

## 5. Specification-driven development

Inspected source: `github/spec-kit` at
[`d848fb4e18f44640ad6b42e60a280551ee90cdce`](https://github.com/github/spec-kit/tree/d848fb4e18f44640ad6b42e60a280551ee90cdce)
(12 September 2026, MIT). Its feature template prioritizes independently
demonstrable user journeys. The plan supplies technical context, and the task
template maps work to stories, paths and dependencies. Parallel work is suitable
when files and prerequisites permit it.
[Feature template](https://github.com/github/spec-kit/blob/d848fb4e18f44640ad6b42e60a280551ee90cdce/templates/spec-template.md),
[plan](https://github.com/github/spec-kit/blob/d848fb4e18f44640ad6b42e60a280551ee90cdce/templates/plan-template.md),
[tasks](https://github.com/github/spec-kit/blob/d848fb4e18f44640ad6b42e60a280551ee90cdce/templates/tasks-template.md).
Kiro's official guidance also recommends separate specifications for distinct
features. [Kiro best practices](https://kiro.dev/docs/specs/best-practices/).

Specification, plan and task list answer different questions: what behavior is
required, how the affected system will support it, and what bounded work comes
next. A compact feature can keep these in one file; a complex change may benefit
from separate linked records. Do not require three new documents for a typo.

Spec Kit's analysis command checks consistency and coverage before implementation;
its convergence procedure inspects current implementation against intent.
These are useful review activities, but do not establish passing acceptance tests
or behavior of a particular release. Its evolving-spec guidance offers different
ways to retain history or maintain a living contract.
[Analysis](https://github.com/github/spec-kit/blob/d848fb4e18f44640ad6b42e60a280551ee90cdce/templates/commands/analyze.md),
[convergence](https://github.com/github/spec-kit/blob/d848fb4e18f44640ad6b42e60a280551ee90cdce/templates/commands/converge.md),
[evolving specs](https://github.com/github/spec-kit/blob/d848fb4e18f44640ad6b42e60a280551ee90cdce/docs/guides/evolving-specs.md).

An acceptance scenario written in Markdown becomes executable only when an actual
test or evaluator exercises it. For example, Cucumber scenarios bind steps to
implementation and assertions; headings alone provide no such execution.
[Gherkin reference](https://cucumber.io/docs/gherkin/reference/).

**Adopt selectively:** Spec Kit's implementation command processes the full task
list, so its input must first be bounded to the selected authorized feature/slice.
Its task command makes tests conditional on explicit requests; retain this
template's requirement for proportionate verification even when the user's prompt
does not mention tests. Its specify command caps clarification markers; do not
guess consequential company/access requirements to satisfy an arbitrary quota.
[Implementation](https://github.com/github/spec-kit/blob/d848fb4e18f44640ad6b42e60a280551ee90cdce/templates/commands/implement.md),
[task generation](https://github.com/github/spec-kit/blob/d848fb4e18f44640ad6b42e60a280551ee90cdce/templates/commands/tasks.md),
[specification generation](https://github.com/github/spec-kit/blob/d848fb4e18f44640ad6b42e60a280551ee90cdce/templates/commands/specify.md).

Do not repeat the methodology's stronger claims that generation eliminates the
specification/implementation gap. Keep actual behavior, accepted intent and tests
in agreement through evidence and review. No Spec Kit/Kiro installation or
upstream template copying is proposed by this document.

## 6. Proposed common feature loop

This is a design proposal for the template. It is not an installed workflow or
a new mandatory approval system.

1. **Discover and select.** Resolve enough of the business need and company
   constraints to select the next feature. Keep later roadmap items outside the
   current implementation scope.
2. **Specify.** Describe observable behavior, exclusions, existing behavior to
   preserve, dependencies, failure cases and evidence needed for acceptance.
3. **Plan the affected boundaries.** Resolve interfaces and consequential unknowns.
   Split work into coherent increments and identify shared prerequisites.
4. **Assign and implement one ready slice.** Give each worker bounded inputs,
   owned files/interfaces, expected outputs and a stopping condition. Parallelize
   only independent work; a coordinator integrates the result.
5. **Verify and review.** Run applicable code/data/model/interface checks and review
   the combined change against the specification, including changed tests.
   A slice is not accepted or release-ready while required acceptance evidence is
   failed, blocked or unrun. Correct the defect or record an explicitly agreed
   scope change; do not weaken criteria to excuse the implementation.
6. **Release when ready and authorized.** Identify the actual artifact/configuration
   and target; check compatibility, user behavior and recovery. A prepared release
   is distinct from a deployed one.
7. **Observe and refine.** Turn failures, changes and feedback into a bounded issue
   or specification revision. Keep earlier evidence attached to its earlier state.

The dependency chain is:

```text
Business outcome
  -> selected feature/spec revision
  -> ready tasks and interface contracts
  -> reviewed implementation revision
  -> applicable test/data/model evidence
  -> release artifact and target configuration
  -> operational observations
  -> next issue or revised feature
```

Do not implement all layers independently and postpone integration until the end.
Shared infrastructure work should be bounded to known prerequisites. One passing
branch or one agent's completion message cannot establish integrated correctness.
An implementation defect requires a correction; it is not a reason to rewrite
the specification or evaluation labels to excuse the defect.

### A compact feature specification

The following is a proposed record outline, not a new CLI or required folder:

```markdown
# Feature <ID>: <observable capability>
Status, owner, related issue and spec revision:

## Outcome and boundaries
User/problem; expected outcome; in scope; excluded behavior; behavior to preserve.

## Acceptance
Requirement IDs with representative success, failure and boundary cases.
Required quality constraints, measurement method and unresolved material decisions.

## Design and dependencies
Affected interfaces/data; prerequisite feature IDs; relevant decisions.
ML/LLM artifacts, baseline and evaluation scope only when applicable.

## Tasks
Task ID | Requirement | Prerequisites | Owned area | Expected result | Check

## Evidence and delivery
Spec revision -> PR/commit -> checks/evaluations -> artifact/config -> environment.
Passed, failed, blocked and unrun evidence; rollout/recovery and next action.
```

Traceability proves where evidence belongs, not that the evidence is truthful.
Keep sensitive data and credentials in approved storage; link sanitized evidence
instead of embedding production records or complete conversations in the spec.

### Example: an internal document assistant

This example is illustrative and has not been implemented or evaluated. The
company identity/data-access contract is a prerequisite, not something to invent.

| Feature | Bounded outcome | Independent evidence before claiming completion |
| --- | --- | --- |
| F-001: Authorized document search | Search a selected permitted collection; return matching excerpts and source links | Relevant retrieval cases; inaccessible documents never reach results; missing/invalid identity behavior; source update/deletion behavior |
| F-002: Grounded answers | Add answers from authorized retrieved passages with citations and an explicit insufficient-evidence response | Fixed answer/no-answer cases, citation support and permission regressions; baseline comparison; scoped latency/cost measurements |
| F-003: Retrieval improvement | Evaluate one justified chunking or ranking change against F-002 | Comparable baseline/candidate inputs, preserved access/deletion contracts, important failure slices and index compatibility/recovery evidence |

F-002 depends on F-001's retrieval/access interface. F-003 depends on the measured
baseline. Research may overlap other work; dependent implementation follows
validated interfaces. A selected feature can have several small PRs, and unfinished
features must not be exposed as complete capabilities. Scope does not become
safe merely because the work is distributed among several agents.

## 7. What to reuse and what to implement later

| Concern | Existing template support | Proposed next bounded improvement |
| --- | --- | --- |
| Discovery and specifications | Solution discovery, architecture, planning and task records | One beginner-facing feature/spec path connected to project context and Issues |
| Coordination | Task orchestration, engineer profile, independent review and current evidence rules | Trace requirement/task dependencies through the selected feature; preserve one writer per shared area |
| Ordinary delivery | Template checks and release/Azure procedures | Selected application CI and an observed delivery path, specified as separate work |
| ML evidence | Data contracts, bounded experiments, AI evaluation | Bind actual dataset/training/model evidence to a project's feature and release |
| LLM evidence | RAG, tool integration, security, evaluation and performance procedures | Bind prompt/model/retrieval/tool identities to comparable evaluations and operational observations |
| Maintenance | Operational readiness, troubleshooting, dependency maintenance | Project-specific signals, supported recovery and a demonstrated feedback-to-issue path |

These additions should reuse existing records and tools. A machine-readable
feature-state checker would need a separately specified schema and meaningful
failure cases. A Projects automation needs actual project fields and access.
A dev container needs tested prerequisites. A deployment needs a selected app
and target. None should be generated as empty success-reporting placeholders.

Suggested later acceptance exercise: take one underspecified idea, select one
feature, encounter a real dependency conflict, revise one requirement legitimately,
and demonstrate a failing acceptance case preventing completion. Then deliver and
observe the corrected slice within the project's authority. This research did
not run that end-to-end exercise or compare agent arrangements experimentally.

## 8. Source coverage and limits

Primary-source research was split into independent ML, LLMOps and specification
questions, with one writer integrating the documents. No upstream executable,
model call, training run, deployment or external setup script was executed.
No new dependency or service was installed. This is selected-source research,
not an exhaustive survey or a certification of any method.

- **AI-assisted SDLC:** AWS introduction and adaptive-workflow sections; DORA's
  small-batches page and 2025 report landing-page summary; NIST Playbook overview.
  The full DORA report, AWS white paper and full NIST framework were not audited.
  No vendor productivity claims were adopted as measured template outcomes.
- **ML:** Google Cloud MLOps sections on pipelines, maturity, validation, metadata
  and training triggers; Microsoft MLOps v2 lifecycle/monitoring/retirement;
  Google dataset partitioning; scikit-learn preprocessing/leakage/randomness;
  Microsoft MLOps/GenAIOps lifecycle. Read documentation, not running examples.
- **LLMOps:** Microsoft MLOps/GenAIOps, foundation-model lifecycle and AI application
  design; MLflow evaluation overview and automatic evaluation, including offline/
  online distinctions and sampling. No product deployment or source-code audit.
- **Spec Kit:** pinned commit above; untruncated recursive tree, selected source
  review. Fully read LICENSE, `spec-driven.md`, spec/plan/tasks templates,
  specify/plan/tasks/implement/analyze/converge command templates and
  `docs/guides/evolving-specs.md`. README and clarify command sections were read
  selectively. MIT license inspected; no upstream source or skill was copied.
- **Other specification sources:** Kiro best-practices page (displayed update
  4 August 2026) and Cucumber Gherkin scenarios/steps/assertions. Kiro's older
  concepts URL failed; the current best-practices page supplied the evidence.
- **Local comparison:** purpose/entrypoints, engineering workflow, discovery,
  planning/orchestration, data/RAG/evaluation, release and readiness procedures,
  current CI and project/operations records at the stated baseline.

Documentation URLs are mutable and should be rechecked before adopting concrete
product commands. Historical last-update dates do not prove current runtime
compatibility. The proposal preserves the application stack and current company
requirements; unknown budget, quality or recovery targets remain unresolved.

Document verification: repository link/foundation checks, existing design bindings
and applicable pre-commit checks passed. Independent reading of both documents
confirmed that an entire-document-assistant request resolves to prerequisite
discovery and the next ready feature, with later dependent features left in the
backlog. A failed acceptance scenario remains incomplete; review made that stop
condition explicit above. These were document/reader checks, not a live workflow
or model-quality evaluation. Markdown was checked as source, not browser-rendered.
