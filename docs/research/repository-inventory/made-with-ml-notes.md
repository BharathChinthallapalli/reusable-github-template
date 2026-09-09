# Made With ML: read-only source assessment for reusable template decisions

Inspected 9 September 2026. Repository: GokuMohandas/Made-With-ML. Default branch: main. Current head observed through the GitHub connector: `3361aeb8ddfc2affdba9f545c978c38c85cee764`, committed 4 March 2026 at 23:44:17 UTC. Commit tree: `836548557605dde112445051aff7a4c90266b8b7`. The recursive inventory returned 56 tracked files and was not truncated. This is an original intermediate research note, not copied upstream documentation.

Read-only scope: metadata, recursive tree, README, dependency and formatting manifests, license, all three YAML GitHub workflows and their report converter, deployment configuration/job script/service entrypoint, representative source modules and tests, notebook source cells, and the headers of all four CSV files. No upstream code, test, install command, notebook, deployment or hook was executed. No current CI success, live deployment, performance benchmark or security audit is claimed.

## Purpose and constraints observed

The README explicitly presents a course taking ML experiments through deployment and iteration. The implemented application classifies ML project titles/descriptions into topic labels using SciBERT, Ray and PyTorch, with MLflow tracking and Ray Serve/FastAPI serving. Local laptop instructions exist, but the default expanded setup and supplied production configs assume an Anyscale teaching environment on AWS.

- [README](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/README.md)
- [Core model](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/madewithml/models.py)
- [Deployment environment](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/deploy/cluster_env.yaml)

The current tree has no AGENTS.md, copilot-instructions.md, custom agents, or SKILL.md files. Its value here is workflow and code evidence; it does not establish an agent-discovery or always-on skill convention.

## Six transferable, stack-neutral decisions

### 1. Separate deterministic code checks, data contracts and model behavior evaluation

Observed: `tests/code` checks helpers and preprocessing; `tests/data/test_dataset.py` checks schema, supported labels, identifier uniqueness, nulls and compound title/description uniqueness; `tests/model/test_behavioral.py` checks minimum functionality, invariance and directional behavior. Data/model fixtures accept dataset locations and model run IDs.

Template decision: AI work instructions should identify which of these layers changed and run the relevant existing command. Code changes need deterministic tests where useful; data/retrieval/prompt/model changes also need task cases and assertions over observable behavior. Keep optional provider/model evaluation separately callable from offline repository checks, and report which layers were actually exercised.

Do not copy a folder hierarchy as a requirement for every language. This repository's `tests/code` also includes actual two-epoch training and tuning with six workers and remote data; it is not a fast or offline unit-test suite. Its dataset uniqueness checks do not themselves establish that train and holdout sets are disjoint.

- [Data contracts](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/tests/data/test_dataset.py)
- [Behavior tests](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/tests/model/test_behavioral.py)
- [Training test cost](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/tests/code/test_train.py)
- [Remote code-test fixture](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/tests/code/conftest.py)

### 2. Require evaluation beyond one aggregate number

Observed: `evaluate.py` records weighted overall precision/recall/F1, per-class metrics and named slices (`nlp_llm`, `short_text`), each with sample counts, together with timestamp and run ID. Behavioral tests supplement numerical metrics.

Template decision: an AI evaluation/review skill should require a baseline or current behavior, representative cases, relevant subgroups, sample counts, concrete failure examples and project-defined acceptance criteria. Keep metrics appropriate to the task (for example retrieval evidence or permission behavior for a policy agent); do not impose classifier F1 on every project. For repeated/stochastic results, document repetition and uncertainty rather than claiming a single run proves improvement.

Caveat: this source computes metrics but does not implement a numeric deployment threshold or baseline comparison in the inspected workflow. Small slice counts and untested evaluator logic remain limitations; `pyproject.toml` excludes evaluation and serving modules from coverage.

- [Evaluator](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/madewithml/evaluate.py)
- [Coverage exclusions](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/pyproject.toml)

### 3. Keep experimentation reusable through explicit module and entrypoint boundaries

Observed: the README moves notebook experiments into `data`, `train`, `tune`, `evaluate`, `predict`, `serve` and configuration modules. The train path loads data, stratifies train/validation, fits preprocessing on training data, uses the same fitted mapping for validation, reports checkpoints and saves structured results. Prediction reconstructs preprocessing from checkpoint metadata; the HTTP service calls the same prediction implementation.

Template decision: clean-code guidance should move reusable behavior from notebooks/handlers into named functions/modules with clear inputs and outputs, while retaining a thin CLI or transport adapter. Share preprocessing and model/artifact contracts between evaluation and serving. Refactor at real responsibility boundaries, preserving behavior and avoiding a mandatory framework architecture.

Caveat: the repository also illustrates things not to carry over: importing `config.py` creates directories and changes global logging/MLflow state; importing `deploy/services/serve_model.py` runs AWS CLI downloads. Reusable components should make consequential initialization/I/O explicit instead of surprising callers.

- [Notebook source](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/notebooks/madewithml.ipynb)
- [Training orchestration](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/madewithml/train.py)
- [Predictor/checkpoint contract](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/madewithml/predict.py)
- [HTTP service](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/madewithml/serve.py)
- [Configuration side effects](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/madewithml/config.py)
- [Deployment import side effects](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/deploy/services/serve_model.py)

### 4. Make code, data, configuration and output provenance explicit

Observed: training saves timestamp, MLflow run ID, parameters and epoch metrics; checkpoint metadata includes the class mapping; evaluation records its run ID. The deployment job saves `run_id.txt` and the service loads that run. These are useful traceability building blocks.

Template decision: evaluation/deployment evidence should record the code commit, dataset/corpus revision or content hash, model identifier/revision, prompt/configuration revision, command/environment and resulting artifact/report identity. Preserve a stable mapping from what was reviewed to what is deployed.

Caveat: upstream examples load CSVs and build requirements from mutable `main` URLs; `from_pretrained` omits a model revision; results use shared per-user S3 paths rather than a commit-specific immutable handoff. The inspected explicit JSON result contract omits dataset hash and code SHA. Data files have IDs and creation timestamps, but these fields do not establish original collection rights or labeling provenance. No separate dataset card or data-license file appeared in the complete tree.

- [Result contract](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/madewithml/train.py)
- [Job inputs and uploads](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/deploy/jobs/workloads.sh)
- [Dependency URL in environment](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/deploy/cluster_env.yaml)
- [Model loading](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/madewithml/models.py)
- [Dataset](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/datasets/dataset.csv)
- [Holdout](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/datasets/holdout.csv)

### 5. Make the verification-to-release boundary enforce failure and artifact identity

Observed: `workloads.yaml` runs on PRs and manual dispatch, submits the cloud job, retrieves JSON results and comments Markdown onto the PR. `serve.yaml` rolls out on pushes to main. The job orders data tests, code tests, training, evaluation and model tests.

Template decision: keep machine-readable results and a concise reviewer summary; ensure failed checks propagate a nonzero result and block promotion. A deployment should consume the exact evaluated artifact for the reviewed commit, with a documented smoke check and rollback target. CI success should be stated only for the actual run/SHA.

Concrete source limitation: `deploy/jobs/workloads.sh` has neither fail-fast shell settings nor explicit return-code checks. A failed pytest is followed by `cat`, then additional commands; later successful commands can mask the earlier failure. Source inspection establishes this possibility, not an observed failed production run. The serve path retrieves mutable shared artifacts and has no explicit evaluated-commit binding or metric gate. These are reasons to improve the boundary, not to transplant this workflow.

- [PR workflow](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/.github/workflows/workloads.yaml)
- [Workload ordering and failure propagation](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/deploy/jobs/workloads.sh)
- [Deployment workflow](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/.github/workflows/serve.yaml)
- [Serving artifact selection](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/deploy/services/serve_model.py)

### 6. Keep cloud, resource and expensive model execution opt-in

Observed: CPU/GPU counts are arguments to training, but supplied production configs hard-code an education cloud, AWS region, g5.4xlarge head/worker instances, an Anyscale project and S3 paths. Both main ML workflows request `permissions: write-all`; Actions use version tags, not immutable commit SHAs. The dependency file mixes runtime, notebooks, docs, formatting, tests and deployment packages. The benchmark notebook installs OpenAI 0.27.8, uses 2023 model IDs and contains unbounded retry-until-success behavior.

Template decision: default foundation checks should run without cloud credentials or paid model calls. Provider-specific execution needs explicit configuration, bounded attempts/time/resources and clear expected side effects. Derive dependencies and commands from the actual project, using the parent's verified current GitHub/security documentation for least-privilege Actions and supported syntax. Do not add Ray, Anyscale, AWS, MLflow or the benchmark SDK as mandatory template dependencies.

Caveat: pinned requirements describe this educational snapshot (including Ray 2.7.0, PyTorch 2.0.0 and Transformers 4.28.1); they are not current compatibility or security recommendations. Notebook benchmark outputs are historical retained results, not a 2026 model comparison. No claim is made that declared infrastructure currently exists.

- [Compute assumptions](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/deploy/cluster_compute.yaml)
- [Job configuration](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/deploy/jobs/workloads.yaml)
- [Workflow permissions](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/.github/workflows/workloads.yaml)
- [Dependencies](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/requirements.txt)
- [Historical benchmark](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/notebooks/benchmarks.ipynb)

## Additional hook caveat

The local pre-commit hook runs `make clean`, which formats the repository, edits notebook cell numbers and deletes caches/results. This is not a read-only verification command. A template should label mutating format/cleanup commands clearly and not imply that having hook YAML enables the hook automatically.

- [Hook configuration](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/.pre-commit-config.yaml)
- [Make targets](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/Makefile)

## License and credit

Observed root license: MIT, copyright (c) 2023 Made With ML. [Exact license](https://github.com/GokuMohandas/Made-With-ML/blob/3361aeb8ddfc2affdba9f545c978c38c85cee764/LICENSE). Attribute the architectural/workflow inspiration to Goku Mohandas / Made With ML with the repository and inspected revision. If upstream code or substantial documentation is copied, retain its copyright and permission notice as the license requires. This note proposes original guidance derived from source inspection; it does not copy their assets, dataset or implementation. The root software license alone is not evidence for rights to independently sourced images, linked content, data or models.

## Access and verification limits

The large course notebook returned empty content through the file endpoint and was rejected by generic fetch; fetching its known Git blob succeeded. Its source cells and relevant metadata were inspected without executing them. Binary notebook images/outputs were not interpreted as fresh evidence. Dataset inspection here covers the headers, contracts and use paths, not a statistical audit. No external cloud calls or independent reproduction were attempted.

