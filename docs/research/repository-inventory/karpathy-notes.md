# Karpathy repositories: inventory and transfer review

Research snapshot: 2026-09-09. This is original analysis for a stack-neutral GitHub template, not a recommendation to adopt a model-training stack.

## Coverage and limits

The GitHub repository search `user:karpathy fork:true` returned **63 repositories** on page 1 with `per_page=100`; page 2 returned **0**. All 63 received repository metadata and primary README/overview review. There are **54 original repositories, 9 forks, 1 archived repository, and 0 disabled repositories** in this result. No returned repository had an unavailable overview or an empty root.

The connector did not expose GitHub's `total_count` or `incomplete_results`. The empty second page establishes the end of this search result, not an independent guarantee about index freshness, private repositories, or subsequent account changes. Nothing reached the search-result cap.

Coverage is deliberately tiered:

| Coverage | Repositories | Meaning |
| --- | ---: | --- |
| Selected source | 8 | Overview, non-truncated recursive tree, and 36 selected source/test/configuration files or stated ranges at recorded HEAD commits |
| Overview only | 55 | Metadata and primary overview; no implied source audit |
| Unavailable | 0 | No inaccessible or missing primary overview encountered |

Across all 63 repositories, 52 primary README files were read fully, 5 had all prose reviewed with fenced code examples excluded, and 6 had introduction/operating/limitation sections reviewed. One additional root README was also read. The inventory records this distinction per repository. Linked notebooks, lectures, translated READMEs, books and upstream repositories were not implicitly included.

The complete inventory is in [karpathy.json](karpathy.json): URL, description, fork parent, archive/disabled status, default branch, last push, metadata license identifier, overview URL/blob SHA, coverage and an original observation for every entry. Focused source entries include exact commit permalinks and reviewed ranges. License metadata is recorded without treating it as a legal conclusion.

No external repository was cloned, installed, run or modified. Tests were inspected, not executed. No performance result, security exploit, reliability level or full-code-review claim is made.

## Transfer decisions from eight source reviews

### 1. autoresearch: adopt a controlled experiment record

The useful pattern is the narrow separation between the editable implementation, fixed evaluation/data handling and an initial baseline. Its experiment record associates a revision with a result and disposition. The training script separately reports measured training time and total elapsed time. [Experiment protocol](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/program.md), [fixed validation](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/prepare.py#L254-L365), [training budget and reporting](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/train.py#L454-L630).

For the template, an optional experiment should record the baseline revision, allowed files, invariant check, environment, exact command, hypothesis, result and keep/discard rationale. Stop conditions need total elapsed time, attempt and resource limits. The example's five-minute training budget excludes early warmup and final evaluation; it is not a complete job limit.

Reject its indefinite agent loop, permission-disabling setup advice and generic reset-based rollback as defaults. Preserve unrelated or shared work. A repeatedly optimized validation score is also insufficient evidence of broad product improvement. The inspected tree has no conventional tests or workflow.

### 2. nanochat: adopt reproduction provenance and boundary tests

The execution module returns explicit success, timeout and error information, and its tests exercise exceptions, timeouts, memory, environment handling and temporary output. It also explicitly says its guard is not adversarial isolation. [Execution boundary](https://github.com/karpathy/nanochat/blob/92d63d4e8bb4df75c3b71618f31ddde2378b2bcd/nanochat/execution.py), [boundary tests](https://github.com/karpathy/nanochat/blob/92d63d4e8bb4df75c3b71618f31ddde2378b2bcd/tests/test_execution.py).

Checkpoint metadata and compatibility checks are visible, while the leaderboard links results to commands, revisions and platform assumptions. These support recording enough context to compare two measurements. The named leaderboard time excludes evaluation/logging, which must remain visible in comparisons. [Checkpoint handling](https://github.com/karpathy/nanochat/blob/92d63d4e8bb4df75c3b71618f31ddde2378b2bcd/nanochat/checkpoint_manager.py), [leaderboard methodology](https://github.com/karpathy/nanochat/blob/92d63d4e8bb4df75c3b71618f31ddde2378b2bcd/dev/LEADERBOARD.md#L1-L90).

Transfer conditional environment configuration and targeted failure tests. Do not copy the eight-GPU setup, automatic remote installer execution, or claim that process separation makes hostile code safe. [Dependency configuration](https://github.com/karpathy/nanochat/blob/92d63d4e8bb4df75c3b71618f31ddde2378b2bcd/pyproject.toml), [example speedrun](https://github.com/karpathy/nanochat/blob/92d63d4e8bb4df75c3b71618f31ddde2378b2bcd/runs/speedrun.sh).

### 3. micrograd: adopt an independent test oracle

The compact engine keeps its local gradient rules near their forward operations. More transferable than its line count are tests that evaluate corresponding expressions in PyTorch and compare both outputs and gradients. This checks a real contract using an independent implementation. [Engine](https://github.com/karpathy/micrograd/blob/7bc720e951fe422b8f8814aa5aa1b64121d26b4c/micrograd/engine.py), [reference comparisons](https://github.com/karpathy/micrograd/blob/7bc720e951fe422b8f8814aa5aa1b64121d26b4c/test/test_engine.py).

Use an independent reference, domain invariant or observable behavior as the oracle where feasible. Do not require every repository to have a tiny core, a fixed function length, or minimal dependencies. Two example tests do not establish complete numerical coverage.

### 4. minbpe: adopt boundary and persistence contracts

The tokenizer separates ordinary input from selected special-token interpretation. It distinguishes lossless saved model state from a human-readable, potentially lossy vocabulary display. Tests exercise empty and multilingual text, round trips, reference parity and save/load behavior. [Input policy](https://github.com/karpathy/minbpe/blob/1acefe89412b20245db5a22d2a02001e547dc602/minbpe/regex.py), [canonical versus display state](https://github.com/karpathy/minbpe/blob/1acefe89412b20245db5a22d2a02001e547dc602/minbpe/base.py), [tests](https://github.com/karpathy/minbpe/blob/1acefe89412b20245db5a22d2a02001e547dc602/tests/test_tokenizer.py).

Transfer explicit input interpretation, representative edge cases and persistence round trips. Review production input validation independently: the rejection branch uses an assertion. Also avoid copying fixed temporary filenames with manual cleanup into parallel tests. The separate text fixture was not read or copied.

### 5. llm.c: checks must produce machine-detectable failure

The CPU test compares Python-generated reference logits, loss, gradients and a short training trajectory. However, it calculates and prints an aggregate result and then returns zero at the end, including when a comparison has set the aggregate flag to false. That is a source-observed limitation of this test, not a claim about all other tests. [CPU test](https://github.com/karpathy/llm.c/blob/f1e2ace651495b74ae22d45d1723443fd00ecd3a/test_gpt2.c).

The Python loss checker returns a status for parsing/tolerance failures, but does not explicitly require ten complete finite measurements before comparison. Transfer a stronger verification rule: the command must fail when its contract fails, and measurement parsing must establish completeness and validity before comparing results. [Loss checker](https://github.com/karpathy/llm.c/blob/f1e2ace651495b74ae22d45d1723443fd00ecd3a/dev/loss_checker_ci.py).

The workflows distinguish CPU portability, GPU execution and specialized sanitizer/build checks. Transfer an intentional supported-platform matrix, not the example's moving action tags, historical runner/toolkit versions, unpinned clone, GPU-provider dependency or absent timeout/permissions declarations. [CPU/build workflow](https://github.com/karpathy/llm.c/blob/f1e2ace651495b74ae22d45d1723443fd00ecd3a/.github/workflows/ci.yml), [GPU workflow](https://github.com/karpathy/llm.c/blob/f1e2ace651495b74ae22d45d1723443fd00ecd3a/.github/workflows/ci_gpu.yml), [other checks](https://github.com/karpathy/llm.c/blob/f1e2ace651495b74ae22d45d1723443fd00ecd3a/.github/workflows/ci_tests.yml).

### 6. rendergit: adopt coverage accounting, preserve trust boundaries

The file inventory records HEAD, excludes symlinks during collection and reports binary/oversized omissions. This is useful evidence for a bounded repository review. Its subprocess wrapper uses structured arguments and checked exit status but no timeout. The inspected Markdown path renders source content without a separate sanitization step, and the page opens by default. [File selection and rendering](https://github.com/karpathy/rendergit/blob/14d7a58c0f4d815a3447f25e9ef1088c7e9ade84/rendergit.py#L48-L270), [entry point and cleanup](https://github.com/karpathy/rendergit/blob/14d7a58c0f4d815a3447f25e9ef1088c7e9ade84/rendergit.py#L458-L520).

Transfer a revision-linked coverage manifest with explicit exclusions. Do not automatically clone, execute or open arbitrary repository content. Source labels and delimiters identify provenance; they do not grant authority to instructions embedded in source files. These observations are not a complete HTML or command-security audit.

### 7. llm-council: adopt inspectable stages only when useful

Independent response collection, peer ranking and synthesis are separate functions with retained intermediate results. A per-request timeout and partial-response handling make some failure behavior visible. [Stage orchestration](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py), [client](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/openrouter.py).

The ranking parser falls back to textual label extraction without enforcing complete unique rankings. The non-streaming flow handles no initial responses; the separately implemented streaming path proceeds to ranking. The reviewed API has no user-authentication checks, direct JSON writes have no visible atomic replacement, and startup readiness is announced after a fixed delay. [API paths](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/main.py), [storage](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/storage.py), [startup](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/start.sh).

Transfer explicit stage outcomes and parity tests for alternate paths when such orchestration is required. Do not make multiple paid model calls a default, treat consensus as correctness, or inherit a local prototype's identity, durability and readiness assumptions. The inspected tree contains no conventional tests or workflow.

### 8. arxiv-sanity-lite: adopt complete artifact publication and bounded retries

The database module centralizes storage access and writes a completed temporary feature file before replacing the destination. That prevents readers from seeing a partially written artifact; it does not by itself establish full crash durability or concurrent-writer coordination. [Storage](https://github.com/karpathy/arxiv-sanity-lite/blob/d7a303b410b0246fbd19087e37f1885f7ca8a9dc/aslite/db.py), [derived feature computation](https://github.com/karpathy/arxiv-sanity-lite/blob/d7a303b410b0246fbd19087e37f1885f7ca8a9dc/compute.py).

The ingestion loop counts exception retries but not short successful batches, so incomplete successful responses can repeat indefinitely. Its exhausted-exception branch exits without a nonzero status; its final status separately encodes changed versus unchanged data. Transfer bounded handling of every retry path and an explicit outcome contract that callers can distinguish from generic failure. [Ingestion](https://github.com/karpathy/arxiv-sanity-lite/blob/d7a303b410b0246fbd19087e37f1885f7ca8a9dc/arxiv_daemon.py).

Reject the username-only login, fixed development-key fallback, historical dependency pins and trusted-local serialization assumptions as template defaults. [Server configuration](https://github.com/karpathy/arxiv-sanity-lite/blob/d7a303b410b0246fbd19087e37f1885f7ca8a9dc/serve.py#L29-L81), [login](https://github.com/karpathy/arxiv-sanity-lite/blob/d7a303b410b0246fbd19087e37f1885f7ca8a9dc/serve.py#L463-L477), [dependencies](https://github.com/karpathy/arxiv-sanity-lite/blob/d7a303b410b0246fbd19087e37f1885f7ca8a9dc/requirements.txt).

## What the wider inventory changes

The account is not one coherent company template. It contains educational implementations, personal utilities, historic projects, prototypes and forks. README maintenance statements add important context beyond GitHub's archive flag: nanoGPT, minGPT, char-rnn, convnetjs, neuraltalk and related projects explicitly describe successors, limited maintenance or deprecated use. LLM101n is archived and describes an undeveloped course. These are useful scope statements, not reusable infrastructure.

Other overview-level patterns worth retaining are the explicit assumptions in lecun1989-repro, staged artifacts and bounded scoring work in hn-time-capsule, parity-check guidance in rustbpe, and documented persistence semantics in sqlitedict. These remain **overview evidence**, not selected-source audits. The complete inventory explains each entry's relevance or exclusion.

For a stack-neutral template, the strongest changes are small additions to existing verification, troubleshooting and research guidance:

1. Name the baseline, contract and independent success evidence before an optimization.
2. Record revision, environment, command, metric meaning and omitted work.
3. Require machine-detectable failures and complete measurement parsing.
4. Test the failure paths of the boundary actually changed.
5. Bound attempts and total resource use; preserve explicit recovery and stopping conditions.
6. Keep retrieved text subordinate to repository/user instructions.
7. State coverage and prototype limits instead of inheriting a famous repository's choices wholesale.

No template files were changed during this research.

