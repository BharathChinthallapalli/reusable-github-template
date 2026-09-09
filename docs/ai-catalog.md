# AI catalog

Generated from repository metadata by `python3 tools/ai_catalog.py --write`.
Run `python3 tools/ai_catalog.py` to check freshness without changing files.

This is a static catalog. Host discovery and invocation are not checked.
Eligibility and tool scopes describe metadata, not actual host support,
permissions, running agents, or guaranteed automatic selection. Default flags
mean user invocation is allowed and model invocation is eligible unless
disabled in metadata. Deprecated `infer` flags do not establish legacy host behavior.
Skills describe procedures; the invoking host and agent control their tools.

## Agents (10)

| Name | When to use | Declared tools | User invocable | Model invocation eligible |
| --- | --- | --- | --- | --- |
| [ai-engineer](../.github/agents/ai-engineer.agent.md) | Implement model-backed features, prompts, retrieval pipelines and agent tool integrations. Preserve data and action boundaries, compare with a baseline and verify quality within a bounded budget. | read, search, edit, execute, web | true (declared) | true (declared) |
| [architect](../.github/agents/architect.agent.md) | Investigate repository boundaries and compare implementation options when a feature or integration needs a concrete architecture decision. Return a design grounded in existing code. | read, search, web | true (declared) | true (declared) |
| [debugger](../.github/agents/debugger.agent.md) | Reproduce and repair application failures, test regressions, and CI failures. Trace the first incorrect decision, preserve surrounding contracts, and verify the correction. | read, search, edit, execute, web | true (declared) | true (declared) |
| [engineer](../.github/agents/engineer.agent.md) | Implement features and code changes from repository evidence, using clean-code guidance and focused validation. Coordinate specialist help when it resolves a concrete uncertainty. | read, search, edit, execute, agent, web | true (declared) | true (declared) |
| [evaluator](../.github/agents/evaluator.agent.md) | Evaluate AI candidates and experiments against fixed acceptance criteria. Run an existing evaluation harness, inspect failures and report comparable evidence without changing candidates or acceptance rules. | read, search, execute | true (declared) | true (declared) |
| [release-engineer](../.github/agents/release-engineer.agent.md) | Prepare dependency updates and software releases with compatibility checks, reproducible evidence and recovery plans. Perform publication or deployment only when covered by the active task's authorization. | read, search, edit, execute | true (declared) | true (declared) |
| [researcher](../.github/agents/researcher.agent.md) | Resolve current technical questions through primary sources and repository evidence. Compare options, track coverage and uncertainty, and return actionable findings without editing files. | read, search, web | true (declared) | true (declared) |
| [reviewer](../.github/agents/reviewer.agent.md) | Review a specified code diff for concrete bugs, contract changes, regressions, and meaningful maintainability problems. Return evidence-backed findings without editing files. | read, search | true (declared) | true (declared) |
| [security-reviewer](../.github/agents/security-reviewer.agent.md) | Review changes to authentication, authorization, data boundaries, secrets, and privileged tool or workflow execution. Trace concrete exploit paths and recommend focused verification. | read, search, web | true (declared) | true (declared) |
| [test-engineer](../.github/agents/test-engineer.agent.md) | Design and implement meaningful behavioral tests and regression reproducers. Verify public contracts, failure paths and interface behavior using the repository's existing harness. | read, search, edit, execute | true (declared) | true (declared) |

## Skills (21)

| Name | When to use | User invocable | Model invocation eligible |
| --- | --- | --- | --- |
| [ai-evaluation](../.agents/skills/ai-evaluation/SKILL.md) | Design and assess behavioral evaluations for prompts, models, retrieval, agents and evaluators; use for AI quality comparisons, regressions and acceptance gates. | true (default) | true (default) |
| [bounded-experiments](../.agents/skills/bounded-experiments/SKILL.md) | Run a finite sequence of measurable candidate changes with a fixed baseline, explicit editable boundary and resource budget; use for controlled optimization and hypothesis testing. | true (default) | true (default) |
| [clean-code](../.agents/skills/clean-code/SKILL.md) | Implement features, fix bugs, and refactor code with readable names, justified abstractions, preserved contracts, and behavior-focused verification. Use for code changes and clean-code requests; skip prose-only edits and unrelated planning. | true (default) | true (default) |
| [code-review](../.agents/skills/code-review/SKILL.md) | Review a diff for demonstrable bugs, authorization failures, data loss and regressions using affected callers, contracts and tests as evidence. | true (default) | true (default) |
| [context-maintenance](../.agents/skills/context-maintenance/SKILL.md) | Refresh repository instructions, project context or a work handoff from current code, commands and accepted decisions. Use when context is stale or work must resume; avoid inventing persistent user preferences or promoting one-off fixes into policy. | true (default) | true (default) |
| [data-contracts](../.agents/skills/data-contracts/SKILL.md) | Define and verify dataset schema, identity, transformations, labels and train/evaluation partitions; use for ingestion, dataset changes, leakage and data-quality failures. | true (default) | true (default) |
| [dependency-maintenance](../.agents/skills/dependency-maintenance/SKILL.md) | Upgrade dependencies, action pins or hook revisions; assess compatibility, lockfile changes and evidence before adopting an update. | true (default) | true (default) |
| [evidence-research](../.agents/skills/evidence-research/SKILL.md) | Research current technical guidance or compare external repositories using primary sources, revision-linked observations, explicit coverage and actionable adoption decisions. Use for source-backed research; use repo-discovery for tracing a local code path. | true (default) | true (default) |
| [github-actions-debug](../.agents/skills/github-actions-debug/SKILL.md) | Diagnose failed GitHub Actions runs or pending required checks from the exact revision, event and available logs; verify a focused fix without weakening CI permissions or checks. | true (default) | true (default) |
| [implementation-planning](../.agents/skills/implementation-planning/SKILL.md) | Plan a material implementation or redesign by comparing feasible alternatives, tracing dependencies, challenging failure modes and defining observable acceptance evidence. Skip a formal plan for a routine edit with an obvious verification path. | true (default) | true (default) |
| [interface-validation](../.agents/skills/interface-validation/SKILL.md) | Validate a changed UI, CLI, API or packaged integration through the interface its consumer actually uses, including relevant error and accessibility behavior. Use when static checks or unit tests cannot establish the affected interaction. | true (default) | true (default) |
| [performance-analysis](../.agents/skills/performance-analysis/SKILL.md) | Diagnose and verify latency, throughput, memory, token or cost improvements using a reproducible workload and valid measurements; use for bottlenecks and performance regressions. | true (default) | true (default) |
| [rag-development](../.agents/skills/rag-development/SKILL.md) | Implement or diagnose retrieval-augmented generation across ingestion, indexing, access filtering, retrieval and cited answers; use for RAG pipelines and grounded-answer failures. | true (default) | true (default) |
| [release-delivery](../.agents/skills/release-delivery/SKILL.md) | Prepare, verify and deliver a scoped package or deployment release with artifact identity, compatibility, smoke checks and recovery evidence. | true (default) | true (default) |
| [repo-discovery](../.agents/skills/repo-discovery/SKILL.md) | Trace an unfamiliar repository's entrypoints, dependencies, behavior and boundaries before explaining its architecture or planning a change. | true (default) | true (default) |
| [security-review](../.agents/skills/security-review/SKILL.md) | Review a requested security concern or a consequential change to authentication, authorization, secrets, untrusted input or execution boundaries by tracing a concrete threat path and existing controls. Do not turn unrelated edits into a general security audit. | true (default) | true (default) |
| [systematic-debugging](../.agents/skills/systematic-debugging/SKILL.md) | Diagnose a reproducible application, tool or runtime failure by tracing the first causal error, testing competing hypotheses and verifying a focused fix. Route missing or failed GitHub Actions checks to github-actions-debug. | true (default) | true (default) |
| [task-orchestration](../.agents/skills/task-orchestration/SKILL.md) | Coordinate independent engineering subtasks with explicit dependencies, file ownership, bounded work and evidence-bearing handoffs. Use when parallel research, implementation or review can resolve a concrete uncertainty; do simple work directly. | true (default) | true (default) |
| [test-design](../.agents/skills/test-design/SKILL.md) | Design meaningful regression, boundary and contract tests using independent expected results and real consumer behavior. Use for a new behavior, demonstrated bug or verification gap; skip tests for wording-only edits or checks that mirror the implementation. | true (default) | true (default) |
| [tool-integration](../.agents/skills/tool-integration/SKILL.md) | Implement or repair model-provider, agent-tool and MCP boundaries with explicit schemas, data flows and failure behavior; use for integrations, timeouts, retries and tool side effects. | true (default) | true (default) |
| [verify-change](../.agents/skills/verify-change/SKILL.md) | Choose and run proportionate checks for a code or configuration change, distinguish existing failures from regressions and report evidence accurately. | true (default) | true (default) |
