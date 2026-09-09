# gh-aw research for template expansion

Reviewed 2026-09-09. Repository: asw101/gh-aw, default branch main, commit `bc153047bde1afe62da5cd4bf03a9dc607d79c7d` (2026-02-02). GitHub identifies its parent as github/gh-aw. The upstream comparison endpoint resolves this same commit and reports identical against asw101:main; this establishes shared revision identity, not equality with today's upstream main. Treat the fork as a dated source and verify current compiler/host documentation before installation.

## Coverage and provenance

The complete nontruncated recursive tree contains 2,959 entries. Fetched all 24 top-level skills, all 8 agent profiles plus the developer instructions file, the one .github skill, all 149 top-level Markdown workflows, LICENSE and README (185 files). Inspected every workflow's purpose and section taxonomy; read selected relevant bodies more deeply. Read 19 additional consumer/generated/config/test files. Source ledger [the source ledger](gh-aw-coverage.json) gives all 204 exact paths, blob SHAs and pinned links. The large scratch ledger preserves the first 185 raw sources for local research; none is needed in the template.

This is a comprehensive definition inventory and targeted semantic review, not a claim that every line of the 2,959-entry repository was manually read or any upstream workflow was executed. All testing evidence below is static inspection of authored tests and consumers.

## Concrete additions

| Capability | Source definitions | Proposed template action |
| --- | --- | --- |
| Documentation writing | .github/agents/technical-doc-writer.agent.md; skills/documentation/SKILL.md; .github/workflows/technical-doc-writer.md | New documentation-writer agent and documentation-writing skill. Choose reader, task and document type; derive claims from code/config; record prerequisites and expected results; maintain one canonical explanation; run the actual project's docs/link/build checks. |
| Documentation usability | docs-noob-tester.md; claude-code-user-docs-review.md; daily-multi-device-docs-tester.md | Include clean-start user walkthrough and host-specific setup verification in writing skill. Browser/render review only where a rendered surface exists. Capture actual failed step and expected/observed behavior. |
| Formal specification | .github/agents/w3c-specification-writer.agent.md | Add architecture/specification reference and artifact template: distinguish normative requirements from rationale, identify consumer/conformance class, define inputs/outputs/error behavior, trace requirements to tests, document version compatibility. Do not claim W3C endorsement. |
| Agentic workflow authoring | .github/agents/agentic-workflows.agent.md; .github/aw/create-agentic-workflow.md; create-shared-agentic-workflow.md; debug-agentic-workflow.md; update-agentic-workflow.md; upgrade-agentic-workflows.md | New agentic-workflow-development skill with bounded optional documentation-maintenance recipe. Source markdown plus compiler-generated lock YAML, exact compiler/version evidence, least read permissions, tools/network budget, separate bounded output handler, inspect compiled permissions and run staged/manual checks. |
| Instruction lifecycle and reuse | workflow-skill-extractor.md; instructions-janitor.md; developer-docs-consolidator.md; workflow-normalizer.md | Extend context-maintenance: inspect real duplicated consumers, extract stable shared procedures only where contract agrees, retain source provenance and test consumers; update from actual code/schema changes, avoid copying transient incidents into always-on instruction files. |
| Operational reliability and cost | workflow-health-manager.md; agent-performance-analyzer.md; daily-copilot-token-report.md; metrics-collector.md; portfolio-analyst.md; safe-output-health.md | Extend existing evaluation/performance/recovery guidance: distinguish agent output quality, execution health, token/runtime cost and actual handler success; measure comparable denominators, trace run identity, detect duplicate/no-op outputs, use bounded evidence windows and early exit. |
| Cross-layer contract consistency | schema-consistency-checker.md; cli-consistency-checker.md; breaking-change-checker.md; skills/error-messages/SKILL.md | Strengthen data-contracts/tool-integration/interface-validation/release-delivery: schema ↔ parser/runtime ↔ docs ↔ examples, consumer compatibility and actionable error messages. |
| Efficient repository querying | skills/github-issue-query/SKILL.md; github-pr-query; github-discussion-query; corresponding query-issues.sh; shared/github-queries-safe-input.md | Existing research/triage skills can inspect schema/count first, request only useful fields, paginate and state completeness. Do not install an extra tool server just to duplicate available GitHub access. |

## Documentation writer consumer trace

The technical-doc-writer workflow explicitly selects `engine.agent: technical-doc-writer` and imports both the agent file and documentation skill. Trigger is manual workflow_dispatch with a topic. It builds docs before review, asks for another build after edits, and asks to create a PR only for actual changes after successful verification. It separates read permissions from safe-output capabilities. The checked-in generated technical-doc-writer.lock.yml has top-level permissions empty and distinct activation, agent, detection and safe_outputs jobs.

Its implementation is deliberately repository-specific: Astro/Starlight, Node, docs/dist, `make build-docs`, a particular navigation base, and deprecated `infer: false` metadata. Adapt the useful procedure; do not copy these assumptions. The workflow also allows comments/assets and a nondraft PR. Those are not appropriate implicit actions for every template consumer.

A template writer should establish one of four document jobs: teach a first successful task, guide an already-understood task, describe a technical contract, or explain a design. The user-facing page should not mix all four by default. Examples must match detected dependencies and platform. Link success cannot establish factual correctness; a walkthrough cannot establish every supported platform. Report these separately.

## Optional workflow integration contract

Provide an authoring skill and inert recipe, not 149 enabled schedules. Before activation establish concrete repository, workflow purpose, selected engine authentication availability, installed compiler version, output scope, finite runtime/cost allowance and acceptance evidence. A recipe can be manually invoked, read-only while researching, with at most one documentation draft PR and no comments/issue spam; output handler authorization remains separate. Compile using the chosen version and review generated YAML. Stage it before allowing writes, then verify exact run/commit and actual resulting artifact.

Read tests establish that the compiler has explicit cases for safe-output default and explicit maximum counts, valid/invalid targets (including wildcard capability, which should not become a template default), recursive/cyclic/diamond imports, and custom sandbox command configurations. A test file's existence is evidence of an intended contract; these tests were not run here. Consumer workflow `pkg/cli/workflows/test-custom-agent.md` and reference `docs/src/content/docs/reference/custom-agents.md` connect agent profiles to workflow engine configuration.

Potential stale-source issue: update-agentic-workflow.md first distinguishes markdown-only behavior changes from frontmatter compilation but later says always compile. A reusable template should consistently compile and inspect outputs with its chosen compiler instead of copying contradictory version-sensitive instructions.

## Entire workflow family inventory: adoption boundaries

All 149 workflow names and exact source revisions are in the machine-readable ledger. They span documentation; issue/PR triage and lifecycle; workflow creation/upgrades/debugging; security/remediation; dependency/release maintenance; code quality/refactoring; test/smoke checks; CLI usability; research and Q&A; metrics/observability/cost; orchestration/campaigns; MCP/tool integrations; and demonstrations/media/personas.

Existing template skills already cover research, orchestration, triage, release, dependency maintenance, clean code, debugging, security, test design, performance, evaluation, data and tool integration. Strengthen those with specific source-backed procedures rather than create renamed duplicates. New documentation and workflow authoring are substantive gaps.

Do not adopt generic daily issue creation, auto-merge/close routines, persona sarcasm, arbitrary fixed quality scores, forced 20% cost improvement targets, mandatory minimum diagram counts, broad shell wildcard tools, external Slack/Notion servers, poem/news/video demonstrations, or all repository-specific Go/JS compiler implementation procedures. These either duplicate existing scope, need explicit deployment/product context, introduce costs/side effects, or optimize a different repository. Campaign specifications are useful as bounded objective/dependency/budget/stop-condition records inside task-orchestration, not permission for autonomous account-wide work.

## License

The pinned LICENSE is MIT, copyright (c) 2025 GitHub Next. Recommendations above are original paraphrases and structural ideas. If any source code or substantial source prose is later copied, retain the required copyright and license notice and record the exact origin. Current proposal does not require vendoring their implementation, agent prose or generated locks.

## Key pinned links

- [Technical writer](https://github.com/asw101/gh-aw/blob/bc153047bde1afe62da5cd4bf03a9dc607d79c7d/.github/agents/technical-doc-writer.agent.md)
- [Writer workflow consumer](https://github.com/asw101/gh-aw/blob/bc153047bde1afe62da5cd4bf03a9dc607d79c7d/.github/workflows/technical-doc-writer.md)
- [Documentation procedure](https://github.com/asw101/gh-aw/blob/bc153047bde1afe62da5cd4bf03a9dc607d79c7d/skills/documentation/SKILL.md)
- [New-user walkthrough](https://github.com/asw101/gh-aw/blob/bc153047bde1afe62da5cd4bf03a9dc607d79c7d/.github/workflows/docs-noob-tester.md)
- [Specification writer](https://github.com/asw101/gh-aw/blob/bc153047bde1afe62da5cd4bf03a9dc607d79c7d/.github/agents/w3c-specification-writer.agent.md)
- [Workflow skill extraction](https://github.com/asw101/gh-aw/blob/bc153047bde1afe62da5cd4bf03a9dc607d79c7d/.github/workflows/workflow-skill-extractor.md)
- [Safe output maximum tests](https://github.com/asw101/gh-aw/blob/bc153047bde1afe62da5cd4bf03a9dc607d79c7d/pkg/workflow/safe_outputs_max_test.go)
- [License](https://github.com/asw101/gh-aw/blob/bc153047bde1afe62da5cd4bf03a9dc607d79c7d/LICENSE)
