# No-mistakes: source review and adoption

Reviewed 13 September 2026 at
[`kunchenguid/no-mistakes@37ed23295bc2ffb1dca054563dbfe4e1791c0fcf`](https://github.com/kunchenguid/no-mistakes/tree/37ed23295bc2ffb1dca054563dbfe4e1791c0fcf),
release 1.75.1 dated 12 September. The repository is a Go-backed autonomous Git
delivery workflow under the MIT license, copyright 2026 Kun Chen. Its recursive
Git tree returned 1,015 entries (906 files/109 directories), `truncated: false`.
This is a complete path inventory and selected-source review, not an audit of
every file or a verification of upstream model effectiveness.

## Original adaptations in existing skills

| Local change | Pinned implementation evidence |
| --- | --- |
| Code review checks repair code and its changed tests against the original acceptance criteria; prior findings/fixer summaries remain claims | [review.go](https://github.com/kunchenguid/no-mistakes/blob/37ed23295bc2ffb1dca054563dbfe4e1791c0fcf/internal/pipeline/steps/review.go#L466) explicitly asks a subsequent review to verify both |
| Verify-change invalidates affected results after later edits and attributes passing evidence to the checked state | [prsummary.go](https://github.com/kunchenguid/no-mistakes/blob/37ed23295bc2ffb1dca054563dbfe4e1791c0fcf/internal/pipeline/steps/prsummary.go#L207) rejects mismatched TestedHeadSHA evidence, with a [regression case](https://github.com/kunchenguid/no-mistakes/blob/37ed23295bc2ffb1dca054563dbfe4e1791c0fcf/internal/pipeline/steps/prsummary_scenarios_test.go#L122) |
| Test-design distinguishes implementation-text checks from consumer behavior, parsed declarative meaning and actual text-output contracts | [test guidance](https://github.com/kunchenguid/no-mistakes/blob/37ed23295bc2ffb1dca054563dbfe4e1791c0fcf/internal/testguidance/guidance.go) makes this distinction explicit |

No source code or upstream skill text was copied. Existing local planning,
orchestration and review already cover simpler alternatives, concrete reachable
defects, independent raw artifacts, bounded iteration and proportional testing.
Three short refinements add the missing emphasis without another agent/skill.
The catalog stays at 34 skills and 13 agents. Shared routing makes these available
to agents following the repository instructions; it does not prove host loading.

## Choices not adopted

The upstream product includes a Git proxy/daemon, worktree custody, a fixed
nine-stage pipeline and automatic rebase/push/PR repair. Those require runtime,
credential and state-management contracts beyond this template request. No
transcript scraping, evidence-attachment publication, service or remote loader
was installed. A fresh-context review can be useful when independent review is
justified, but its mocked [session test](https://github.com/kunchenguid/no-mistakes/blob/37ed23295bc2ffb1dca054563dbfe4e1791c0fcf/internal/pipeline/steps/review_session_test.go#L233)
does not demonstrate better LLM defect detection.

The upstream test stage forbids local full-suite runs and parks no-runtime-surface
changes for human approval. These are product choices, not portable requirements.
This template retains required repository tests, ordinary documentation/config
work and the user's existing authorization. Blanket warnings about every
unrequested component are also omitted: necessary implementation details differ
from scope growth. Review stops when acceptance evidence is sufficient.

## Reviewed source coverage

All paths below are relative to the pinned upstream revision above.

- Fully read: `README.md`, `LICENSE`, `.no-mistakes.yaml`,
  `skills/no-mistakes/SKILL.md`, documentation concepts `pipeline.md` and
  `auto-fix.md`; upstream skills `pipeline-review-and-agents`,
  `testing-conventions`, `test-evidence-storage`, `branch-sync-and-push-safety`
  and `repository-routing-security`.
- Implementation/tests read: `internal/pipeline/sessions.go`;
  step files `review.go`, `test.go`, `intent_prompt.go`, `prsummary_scenarios.go`,
  `review_session_test.go`, `prsummary_scenarios_test.go`,
  `test_quality_guidance_test.go`; `internal/testguidance/guidance.go`;
  `cmd/genskill/main.go`.
- Relevant sections inspected: `AGENTS.md`, `internal/skill/skill.go`, step files
  `prsummary.go` and `test_scenario_contract_test.go`.
- Evaluation README descriptions inspected: `simplification_review`,
  `authorization_privacy_review` and `intended_usage_review` under step testdata.
  Individual model fixture diffs were not audited or evaluated.
- Local comparison: code-review, implementation-planning, test-design,
  task-orchestration, verify-change, their relevant references/assets, and
  security-review. No upstream executable or model evaluation was run.

## Verification approach

The changes are prose instructions, so no tests search their source text for
the newly added sentences. Apply the revised procedures to bounded synthetic
cases: a repair paired with a self-confirming test, stale CI after a code/config
edit versus an evidence-only note, and textual versus parsed/consumer assertions.
Record independent exercise outcomes and limits alongside the required static
metadata, catalog, design and repository checks. These exercises demonstrate
interpretation on the named cases, not broad agent reliability.

An independent reviewer exercised these cases with Python/YAML fixtures:

- A self-confirming quota test passed while a hand-derived inclusive-boundary
  assertion failed. An explicit exclusive-boundary contract accepted that same
  implementation, preserving legitimate requirement changes.
- A baseline check passed; subsequent code and configuration edits each failed
  it. An evidence-note edit preserved the checked input hashes.
- A source-comment marker passed a text assertion while the executable rejection
  behavior failed. A YAML comment fooled text matching but parsed permissions
  exposed `write`. An exact emitted-stdout contract correctly passed.

The same review caught an unquoted YAML scalar containing `: ` in the new
ast-grep install step. It was changed to a block scalar before delivery. Both
workflows then parsed, the actual structural smoke step passed, and a deliberately
incorrect match-count assertion returned failure. These are observed bounded
checks, not a claim that every host agent will apply the procedure correctly.
