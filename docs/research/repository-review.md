# Public repository review

Research date: **9 September 2026**. This review inventories **494 public account
repositories and two targeted AI repositories**. It combines metadata and primary
overviews with selected source reviews of **23 account repositories plus both
targeted repositories**. It does not claim that every source file was read, that
upstream tests passed, or that any repository received a complete security audit.

## Coverage and evidence

| Account | Public repositories | Forks / archived | Overview coverage | Detailed source samples |
| --- | ---: | ---: | --- | ---: |
| [bcherny](https://github.com/bcherny) | 271 | 111 / 0 | 232 nonempty root READMEs; 30 alternative primary files; one blank site; eight empty repositories | 7 repositories, 41 files |
| [karpathy](https://github.com/karpathy) | 63 | 9 / 1 | All 63 primary overviews: 52 complete, five prose without code blocks, six selected sections | 8 repositories, 36 files |
| [johnpapa](https://github.com/johnpapa) | 160 | 52 / 14 | 155 README introductions/headings; three repositories without a root README; two empty repositories | 8 repositories, 45 non-README files |

All 494 have metadata records. Fork and archive counts overlap. bcherny's mutually
exclusive coverage tiers are 227 overview, 28 alternative primary file, seven
detailed samples, one directory-only, and eight empty metadata-only. Its overview
reading usually covers the opening passage, not the entire README. JohnPapa's
remaining repositories have overview or directory evidence, not source audits.
The ten empty repositories have no implementation evidence to assess.

Enumeration used `user:ACCOUNT fork:true`, 100 results per page, and empty-page
termination: bcherny **100/100/71/0**, karpathy **63/0**, johnpapa **100/60/0/0**.
The connector exposes neither `total_count` nor `incomplete_results`; these are all
unique repositories returned, not a guarantee against indexing omissions.
Private, hidden, deleted, or newly unindexed repositories are outside coverage.
Cross-account and metadata/file retrievals are not an atomic snapshot.

The two additional targets are
[patchy631/ai-engineering-hub](https://github.com/patchy631/ai-engineering-hub/tree/2c9b106168d4540b88e727e4aa316c06c856c2b7)
and [GokuMohandas/Made-With-ML](https://github.com/GokuMohandas/Made-With-ML/tree/3361aeb8ddfc2affdba9f545c978c38c85cee764).
Their selected workflow, evaluation, test, configuration, and source observations
are listed below; most independent hub demos and large/binary assets were not read.
The account repositories and two AI targets were inspected without cloning,
installing or executing them. Their tests were inspected only.

| Original notes | Machine-readable inventory and source scope |
| --- | --- |
| [bcherny findings and complete inventory](repository-inventory/bcherny-notes.md) | [271 records and selected source references](repository-inventory/bcherny.json) |
| [karpathy findings](repository-inventory/karpathy-notes.md) | [63 records and selected source references](repository-inventory/karpathy.json) |
| [johnpapa findings](repository-inventory/johnpapa-notes.md) | [160 records and selected source references](repository-inventory/johnpapa.json) |
| [AI Engineering Hub findings](repository-inventory/ai-repositories-notes.md) | [Both targeted repositories and file-level coverage](repository-inventory/ai-repositories-coverage.json) |
| [Made With ML findings](repository-inventory/made-with-ml-notes.md) | [Both targeted repositories and file-level coverage](repository-inventory/ai-repositories-coverage.json) |

Detailed bcherny, karpathy, and targeted repository references use recorded commit
HEADs where available. Many overview links and JohnPapa source links follow the
recorded default branch. Their JSON blob hashes identify fetched file content;
they are **not commit references**. Tree hashes are not commit references either.
The original notes preserve research observations, including rejected examples;
they are evidence, not instructions to execute upstream setup commands.

## Decisions applied to this template

| Lesson from inspected evidence | Adoption or rejection here |
| --- | --- |
| bcherny's schema generator separates generated-output checks from type compilation; its final CI gate omits two job results | Adopt behavioral and failure-path evidence; reject success gates that ignore dependencies. [CI](../../.github/workflows/ci.yml) and [validation](../../VALIDATION.md) state actual checks and limits. |
| Karpathy's autoresearch fixes a baseline and records outcomes, while its indefinite optimization loop serves a narrow experiment | Adopt bounded experiments, comparable baselines, and explicit stop conditions in [AI evaluation](../ai-evaluation.md); reject unlimited iteration and treating one score as product quality. |
| JohnPapa's AI assets and host-specific workflows show that filenames and counts cannot establish activation | Adopt metadata diagnostics plus documented host verification in [AI assistance](../ai-assistance.md); reject claims that agents, skills, or hooks automatically run everywhere. |
| Typed contracts, disposal tests, and rejected-input tests expose behavior that prose and snapshots can miss | Adopt observable acceptance criteria and real module contracts in [project context](../project.md), followed by a small behavior loop and independent review. No application framework is imposed. |
| AI Engineering Hub evaluations expose provider/label mismatches, missing evidence, and error-to-score conversion | Adopt explicit evaluation provenance and separate failures, unrun cases, and quality results in [AI evaluation](../ai-evaluation.md); reject demo labels as verification. |
| Made With ML separates code, data, and model checks, but its sample hook pipeline mutates files and its stack requires substantial infrastructure | Adopt checks matched to the change and workload; use ten read-only [Git hooks](../git-hooks.md). Reject mandatory formatters, paid services, ML dependencies, or infrastructure for this foundation. |
| Upstream examples include mutable dependencies, shell failure masking, and incomplete maintenance wiring | Keep immutable hook/action references, pinned development dependencies, and explicit failure propagation. [Maintenance](../maintenance.md) connects changes to documentation and validation. |
| The supplied unsupervised-agent examples mix Git and agent lifecycle hooks and include bypass mechanisms | Use hooks as local feedback, with CI and independently configured remote rules. Reject blanket permission bypasses, routine `--no-verify`, and claims of an agent security sandbox. |

## Hook sources and version boundaries

The three supplied sources were the [Git book's hook overview](https://git-scm.com/book/ms/v2/Customizing-Git-Git-Hooks),
[pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks), and
[Nathan Atherton's agent-hook article](https://www.nathanatherton.com/blog/11-git-hooks-that-make-ai-agents-safe-to-run-unsupervised/),
with its [companion gist](https://gist.github.com/Nathanavie/a23ebb0be2b4dcd3f1a99a65ea232277).
The article and gist are examples to inspect, not official guarantees of safe
unsupervised operation. Git hooks and agent lifecycle hooks have different hosts
and installation paths; copying this template does not install either globally.

The development runner is pinned to
[pre-commit 4.6.2](https://github.com/pre-commit/pre-commit/releases/tag/v4.6.2).
The separate hook collection is pinned to
[v6.0.0 commit `3e8a870`](https://github.com/pre-commit/pre-commit-hooks/tree/3e8a8703264a2f4a69428a0aa4dcb512790b2c8c)
in [the configuration](../../.pre-commit-config.yaml). The full SHA selects the
hook code; `minimum_pre_commit_version` is a minimum runner version, not an exact
runner pin. Exact installation versions are in [requirements-dev.txt](../../requirements-dev.txt).

Historical reports [#1198](https://github.com/pre-commit/pre-commit/issues/1198#issuecomment-547963695)
and [#2648](https://github.com/pre-commit/pre-commit/issues/2648#issuecomment-1363198114)
inform recovery and existing-hook precautions; they do not establish current bugs.
[Git hook guidance](../git-hooks.md) records current migration, staged-file,
cache/privacy, and bypass limits. [Plan review](plan-review.md) records the
independent review and resulting checks. Recheck versions and host behavior when
adopting this evidence later; popularity, ownership, and repository names are not
substitutes for inspected behavior.
