# AI engineering repository research for the reusable template

Read-only inspection, 9 September 2026. These are original notes based on repository source, not a reproduction or benchmark. No downloaded code, notebooks, hooks, dependencies, cloud jobs or deployments were run. No template files were edited.

## Revisions and coverage

| Repository | Observed main head | Commit date | Inventory |
| --- | --- | --- | --- |
| [AI Engineering Hub](https://github.com/patchy631/ai-engineering-hub) | `2c9b106168d4540b88e727e4aa316c06c856c2b7` | 2026-08-26 21:04:15 UTC | 1,950 recursive tree entries, not truncated |
| [Made With ML](https://github.com/GokuMohandas/Made-With-ML) | `3361aeb8ddfc2affdba9f545c978c38c85cee764` | 2026-03-04 23:44:17 UTC | 56 tracked files, not truncated |

The Hub commit's tree object is `6e29d312a22a1e31e3f91e8fd042651055cafeb8`; Made With ML's is `836548557605dde112445051aff7a4c90266b8b7`. The accompanying `ai-repositories-coverage.json` lists inspected files and limits. These were API source snapshots, not executable local checkouts.

The Hub is a collection of independent demos, with per-demo dependencies and widely varying completeness. Its README's production-ready wording is an author claim. The complete root inventory contains no root AGENTS.md, Copilot instructions, workflow directory, dependency manifest or pre-commit configuration. There are instruction files and workflow examples nested inside `hugging-face-skills`; those do not establish active root CI or root agent customization. GitHub requires workflow files in the repository's root `.github/workflows` directory. [Hub README][hub-readme] [GitHub workflow location][workflow-doc]

Made With ML is an educational end-to-end classifier project, with notebook exploration, modular training/prediction/evaluation, tests, PR reporting and cloud deployment examples. It has no agent or skill instruction files. Its value for this template is lifecycle evidence, not a convention that enables agents. The independent detailed review is in [made-with-ml-notes.md](made-with-ml-notes.md). [Made With ML README][ml-readme]

## Eight transferable decisions

These are proposed adaptations. Repository observations justify the need; the target host's current official documentation must determine hook names, schema and execution behavior.

| Decision | Evidence | Practical stack-neutral adaptation |
| --- | --- | --- |
| 1. Distinguish instructions, tool interception and final verification | Hub has role prompts, a pre-tool hook and final human review as separate mechanisms. | Keep instructions available by default. Document a host hook's actual activation and behavior separately. Reuse the same deterministic repository checks in CI and a bounded local hook; do not claim static validity proves activation. |
| 2. Scope tools and verify the edited artifact | Hub separates explorer/coder/tester tool sets but combines local file access with remote test tools. | Trace entrypoints, tool scopes, workspace path and reviewed SHA. Run checks against the artifact actually changed. A prompt saying “only edit this file” is not an enforced filesystem boundary. |
| 3. Separate code, data and AI behavior evidence | Made With ML has code/data/model tests; Hub has five behavioral bug-fix tests and RAG question/answer/context cases. | Identify changed layers. Use cheap deterministic checks by default. For AI changes, add representative cases, evidence/citations, permissions or refusal cases where relevant, and task-specific assertions. Do not mandate a Python layout or model SDK. |
| 4. Compare quality fairly and keep error states distinct | Made With ML records class/slice metrics; Hub evaluator can conflate missing labels and failures with scores. | Record baseline, case IDs, dataset revision, expected outcomes, meaningful slices/counts, evaluator configuration and concrete failures. Separate not-run, unlabeled, provider error and quality failure. Avoid inventing a universal passing score. |
| 5. Trace code, data, model and output together | Hub's Kitfile groups artifacts and licenses; Made With ML passes run IDs/checkpoints into prediction. | A small project-specific evidence record should bind code SHA, corpus/data hash, model/prompt/config revision, dependency environment, command and output/report identity. Do not add a registry, MCP server or cloud just to keep this record. |
| 6. Describe actual provider/data flows | Hub's privacy README disagrees with source; the coding harness uses a separate memory embedding provider. | Record inference, embeddings/memory, search, evaluation and telemetry independently. State effective model/provider and what leaves the process. Start with local synthetic fixtures; make external execution explicitly configured and bounded. |
| 7. Preserve verification failures through promotion | Made With ML's shell workload orders tests before release work but can mask an earlier failed command. | A check must return its real status. CI should use the reviewed commit, and promotion should consume the evaluated artifact. Report exact run/SHA; keep deployment optional with project-specific smoke and rollback instructions. |
| 8. Make reusable logic and hook side effects explicit | Made With ML extracts notebook logic into modules, but its pre-commit command also formats and deletes results; Hub's generator mutates docs. | Use cohesive functions and thin entrypoints under the user's clean-code guidance. Label verification versus formatting/cleanup. A default check hook should not install packages, rewrite files, upload data, or ask redundant interactive approvals. |

Source detail below ties each decision to observed implementations. No listed demo framework or paid provider is required by these decisions.

## Hub implementation findings

### Coding harness: useful separation, incomplete enforcement

Read `build-code-harness/code_harness.py`, README, manifest, environment example, implementation fixture and tests. Explorer gets read/list tools; coder gets file and sandbox tools; tester gets test tools. The pre-tool function can reject a tool call, while `human_input=True` asks for final-result feedback. Checkpoints and memory are separate settings. Current CrewAI documentation recognizes the sample's decorator as a supported legacy API; it prefers a newer event API for new code. This is CrewAI behavior, not Copilot hook schema. [Harness source][hub-harness] [CrewAI tool hooks][crewai-hooks]

Important adaptation limits: file tools have no explicit root constraint in this source; tests are routed through E2B, with no workspace synchronization shown in this file. The test wrapper interpolates its path into a shell command. Source alone does not prove SDK workspace behavior, but the template must verify artifact identity and avoid treating arbitrary command strings as a safe test contract. The hook prompts on stdin and prints tool input; that design is unsuitable for unattended foundation CI. It is also not an authorization model to copy wholesale.

The tiny bank-account fixture deliberately has overdraft and recipient-transfer bugs. Its five tests check outcomes and unchanged balances on rejected operations. This is a good example of preserving independent acceptance assertions while repairing implementation; it is not a production finance component. No demo result was reproduced. [Fixture][hub-account] [Tests][hub-tests]

The manifest leaves top-level dependencies unconstrained but ships a large uv lock with resolved versions and hashes. The inspected lock header requires Python 3.11 or later. The environment example separates OpenRouter, E2B and the memory embedder's OpenAI key. A lock and a configured model do not establish runtime availability, privacy or reproducibility of external providers. [Manifest][hub-manifest] [Lock][hub-lock] [Environment example][hub-env]

### Evaluation: independent cases and honest result states

The Opik/LlamaIndex notebook loads five question/answer/context rows, instruments calls, and evaluates answer relevance, hallucination, context precision and context recall. It also downloads an essay from a mutable main-branch URL and defaults Opik configuration to hosted mode. Its experiment model label is not visibly bound to the query engine's actual instantiated model. These are reasons to record effective configuration and source revisions, not to copy a vendor stack. The 13 MB data-generation notebook returned empty content through the file endpoint and was not inspected; original label-generation provenance was therefore not verified. [Evaluation notebook][hub-eval] [Case CSV][hub-cases]

The invoice evaluator has a different failure mode: hard-coded expected answers are mapped by partial keywords; unmatched questions receive “data not available.” The scorer catches exceptions and returns a zero score. The CLI's comparison can name a winner on ties, and the evaluator clears/repopulates a shared dataset. These visible paths motivate explicit unlabeled/error states, comparable input budgets, immutable experiment identities and honest no-comparison outcomes. Provider failures should not silently become evidence of model quality. [Evaluation CLI][hub-eval-cli] [Evaluator implementation][hub-geval]

The same GroundX manifest declares pytest paths but the inspected subfolder tree has no tests directory. Configuration alone is not test coverage. This is a sampled directory observation, not a claim that the Hub contains no tests. [GroundX manifest][hub-groundx-manifest]

### Data flow and deployment: verify source claims

The deployment README describes a private API and instructs pulling a local model. The checked server comments out both local-model construction and agent model assignment, while adding a Serper search tool and documenting OpenAI/Serper keys. A reader cannot infer fully local execution from the README. That file also has no explicit authentication or request-boundary controls; framework/hosting behavior was not audited. A reusable template should supply a place to describe real trust boundaries, runtime dependencies and readiness checks, rather than copying the service as production infrastructure. [Deployment README][hub-deploy-readme] [Server][hub-server]

### Artifact manifest and instruction generation

The KitOps example names code, dependencies, dataset, docs and model in one manifest, with individual license fields. The sample is ten synthetic-looking rows, an unconstrained requirements file and a training script with no held-out evaluation. Its missing-data branch uses an exit without a failure status. The transferable part is the artifact relationship, not the model, serializer or tool server. No model binary was loaded. [Kitfile][hub-kit] [Training source][hub-kit-train]

The nested skill catalog is generated from SKILL metadata. Its generator sorts deterministically and validates catalog relationships, but uses a line-splitting YAML-like parser, silently skips missing required values, and writes outputs before validation completes. Our existing safe, read-only YAML diagnostics should be retained. The nested workflow checks generated-file drift; it is useful inspiration for consistency checking, but is not active root CI at this repository path. Another nested workflow uploads to a hosted Space and installs a CLI through a remote shell script; do not copy that into the template's default checks. [Generator][hub-generator] [Catalog instructions][hub-agents] [Nested validation][hub-nested-ci] [Nested publishing][hub-nested-publish]

## Made With ML implementation findings

The inspected source traces data loading and stratified splitting into fitted preprocessing, training, checkpoint metadata, evaluation and serving through shared prediction logic. Data tests check schema, labels, nulls and uniqueness; behavioral model tests cover minimum functionality, invariance and directional expectations. Some “code tests” actually train/tune with multiple workers and remote data, so their folder names do not imply cheap offline checks. [Data contracts][ml-data-tests] [Behavior tests][ml-model-tests] [Training tests][ml-train-tests]

The evaluator records weighted metrics, per-class outcomes, named slices and sample counts with run ID and timestamp. Its workflow does not visibly enforce a quality baseline or numerical deployment threshold. Models are loaded without an explicit revision, and examples use mutable dataset/dependency URLs and shared per-user output paths. This supports recording effective inputs and reviewed artifact identity. It does not support a claim of a reproducible 2026 benchmark. [Evaluator][ml-evaluate] [Training][ml-train] [Model loading][ml-models]

The PR workload runs data tests, code tests, training, evaluation and model tests; however, its shell script has no fail-fast settings or return-code checks. Later successful commands can mask failed tests. The main-branch serving workflow consumes shared artifacts without an explicit binding to the evaluated commit. Both main ML workflows request broad write permissions and use course-specific Anyscale/AWS infrastructure. Adapt the intended lifecycle using current GitHub documentation and existing neutral checks; do not transplant these workflow files. [Workload script][ml-workloads] [PR workflow][ml-workflow] [Deployment workflow][ml-serve-workflow]

The pre-commit hook runs `make clean`, which includes formatting, notebook edits and deletion of caches/results. It is not a read-only diagnostic. Configuration and serving imports also perform filesystem/logging/download effects. Use explicit entrypoint boundaries and documented hook behavior under the clean-code skill; do not invent arbitrary function-size or architecture rules. [Hook][ml-hook] [Makefile][ml-make] [Configuration][ml-config] [Deployment entrypoint][ml-serve]

## License, attribution and application boundaries

Hub's root license is MIT, copyright 2024 patchy631. The KitOps subproject additionally contains an Apache 2.0 license and labels artifacts accordingly; nested third-party content needs its own provenance review before copying. Made With ML's root is MIT, copyright 2023 Made With ML. Link to both authors/repositories and inspected revisions as inspiration. If copying substantial source or documentation, retain the applicable notices and license requirements. A root code license alone does not establish rights to external datasets, images, model weights or linked essays. These notes propose original guidance, not reuse of those assets. [Hub license][hub-license] [KitOps license][hub-kit-license] [Made With ML license][ml-license]

Proposed implementation boundary: improve existing agent/skill instructions, a focused AI engineering reference/evidence example, and a documented optional Git hook invoking existing checks. Retain offline, credential-free foundation CI. Do not add CrewAI, Ray, MLflow, Opik, KitOps, GPU requirements, hosted storage, a model server, paid evaluation or a pre-commit framework merely because a researched example uses one.

Verification limits: all conclusions are source observations or labeled adaptations. No live deployment, current CI result, actual discovery/invocation, performance claim, dataset audit or security certification was verified. Current official host documentation outranks repository samples for implementation details.

[hub-readme]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/README.md
[hub-harness]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/build-code-harness/code_harness.py
[hub-account]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/build-code-harness/workspace/account.py
[hub-tests]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/build-code-harness/workspace/tests/test_account.py
[hub-manifest]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/build-code-harness/pyproject.toml
[hub-lock]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/build-code-harness/uv.lock
[hub-env]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/build-code-harness/.env.example
[hub-eval]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/eval-and-observability/demo.ipynb
[hub-cases]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/eval-and-observability/data/test.csv
[hub-eval-cli]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/groundX-doc-pipeline/run_evaluation_cli.py
[hub-geval]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/groundX-doc-pipeline/evaluation_geval.py
[hub-groundx-manifest]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/groundX-doc-pipeline/pyproject.toml
[hub-deploy-readme]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/deploy-agentic-rag/README.md
[hub-server]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/deploy-agentic-rag/server.py
[hub-kit]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/kitops-mcp/ml-project/Kitfile
[hub-kit-train]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/kitops-mcp/ml-project/train.py
[hub-generator]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/hugging-face-skills/scripts/generate_agents.py
[hub-agents]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/hugging-face-skills/agents/AGENTS.md
[hub-nested-ci]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/hugging-face-skills/.github/workflows/generate-agents.yml
[hub-nested-publish]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/hugging-face-skills/.github/workflows/push-evals-leaderboard.yml
[hub-license]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/LICENSE
[hub-kit-license]: https://github.com/patchy631/ai-engineering-hub/blob/2c9b106168d4540b88e727e4aa316c06c856c2b7/kitops-mcp/ml-project/docs/LICENSE
[ml-readme]: https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/README.md
[ml-data-tests]: https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/tests/data/test_dataset.py
[ml-model-tests]: https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/tests/model/test_behavioral.py
[ml-train-tests]: https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/tests/code/test_train.py
[ml-evaluate]: https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/madewithml/evaluate.py
[ml-train]: https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/madewithml/train.py
[ml-models]: https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/madewithml/models.py
[ml-workloads]: https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/deploy/jobs/workloads.sh
[ml-workflow]: https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/.github/workflows/workloads.yaml
[ml-serve-workflow]: https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/.github/workflows/serve.yaml
[ml-hook]: https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/.pre-commit-config.yaml
[ml-make]: https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/Makefile
[ml-config]: https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/madewithml/config.py
[ml-serve]: https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/deploy/services/serve_model.py
[ml-license]: https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/LICENSE
[workflow-doc]: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#about-yaml-syntax-for-workflows
[crewai-hooks]: https://docs.crewai.com/v1.15.20/en/learn/tool-hooks
