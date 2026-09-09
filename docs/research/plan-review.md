# Challenge record for the Git and AI engineering update

Date: 2026-09-09. This records decisions made before implementation and the
acceptance evidence required afterward. It is not a vote-based quality score.

## Goal and alternatives

Provide portable staged-file feedback and independent CI checks, preserve the
initializer and offline test contract, and make AI comparisons reviewable.
Considered CI alone, custom Git shell scripts, host lifecycle hooks, and a shared
pre-commit configuration. Selected the maintained runner because staged-content
handling, filenames and existing hooks would otherwise require custom machinery.

Research scope and source findings are in [the repository review](repository-review.md).
The implementation uses a finite review budget: two independent plan critiques,
resolution of material findings, then an independent implementation review and
actual behavior checks. Repeat only when new evidence exposes an unresolved risk.

## Round 1: threat model and pre-mortem

Asked how a bad commit, unusual path, inherited hook, or weakened workflow could
evade the planned checks. Traced the upstream runner and selected hook source.

| Finding | Decision and acceptance evidence |
| --- | --- |
| Root filenames can become argparse options | End selected hook arguments with `--`; test a leading-option filename beside violating content |
| Default file-type filter excludes symlinks | Use `types: []` for filename rejection; test environment symlinks and portable names |
| Existing hook migration can overwrite a legacy collision | Document inspection of both paths before installation; keep managed hooks paths intact; test ordinary migration/restoration and refusal with custom path |
| Staged content and working-tree content can differ | Test both partial-staging directions, index/commit contents, and byte-identical restoration |
| Web/API/no-verify commits bypass local checks | Run all-files checks independently in CI; test bypass followed by clean-checkout rejection |
| Config and workflows remain editable | Describe local detection and separately configured merge enforcement accurately |
| Size checks exempt LFS-attributed paths | Document and exercise this attribute exemption; do not claim LFS upload validation |
| Private-key markers are limited coverage | Document token/history limits and sanitized examples; do not invent a complete secret scanner |
| Unstaged patches remain in local cache | Warn against uploading caches or complete diagnostics; use synthetic test fixtures |

Sources: [argument handling](https://github.com/pre-commit/pre-commit/blob/v4.6.2/pre_commit/lang_base.py),
[installer](https://github.com/pre-commit/pre-commit/blob/v4.6.2/pre_commit/commands/install_uninstall.py),
[staging](https://github.com/pre-commit/pre-commit/blob/v4.6.2/pre_commit/staged_files_only.py),
[selected hook source](https://github.com/pre-commit/pre-commit-hooks/tree/3e8a8703264a2f4a69428a0aa4dcb512790b2c8c).

## Round 2: simplicity, adoption and failure reporting

An independent reviewer compared the proposal with the existing initializer,
ZIP instructions, test commands, maintenance obligations and AI repository evidence.

| Challenge | Resolution |
| --- | --- |
| Will an offline ZIP test unexpectedly download hook environments? | Preserve 51 unit tests; introduce a separate explicit Git integration lane |
| Will every temporary repository reinstall dependencies? | Prepare a shared hook cache once, bound subprocess time, surface setup failures |
| Is 1 MiB universally correct? | Treat it as an editable starter policy with narrow reviewed exceptions |
| Does a full Git SHA lock all dependencies? | State top-level/source pins precisely; document transitive resolution and reviewed updates |
| Does the AI guide need a framework or universal score? | Keep a worksheet linked through existing verification guidance; no SDK or generic evaluator |
| Are unknown labels or provider failures treated as poor quality? | Use separate outcomes, report denominators, and reject incomplete required evaluations |
| Can repeated criticism continue indefinitely? | Stop at verified acceptance, resolved blocking findings and recorded limits |

## Implementation review and proof

The independent implementation reviewer reproduced a symlink-only case
collision that the initial regular-file filter skipped. The final configuration
includes symlinks in `check-case-conflict`; the integration lane checks both
commit rejection and clean-checkout detection. This finding justified a focused
additional correction and regression test after the two plan reviews.

Inspect the final diff for accidental scope expansion, weakened checks, hidden
side effects and unsupported claims. Run the source and initialized-copy checks,
the real Git integration lane, then compare remote files and inspect CI at the
published revision. Record actual results and any remaining limits in
[VALIDATION.md](../../VALIDATION.md). Native OS and editor behavior must remain
unverified until observed in those environments.
