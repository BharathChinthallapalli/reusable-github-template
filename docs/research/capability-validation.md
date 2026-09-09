# Capability validation and plan challenges

Date: 2026-09-09. Scope: version 2.0 capability expansion. This record separates
static format, executable tooling and task-output evidence. No native Copilot,
Codex or Claude discovery/invocation trace was captured.

## Challenge the implementation from different perspectives

| Perspective | Concrete concern | Disposition |
| --- | --- | --- |
| User outcome | Research had mainly produced Git checks and prose | Bundle 21 task skills, 10 agents and reusable records; map every substantiated family to actual files |
| Evidence | A 494-repository inventory could be misrepresented as a full code audit | Preserve metadata, README and selected-source coverage tiers; distinguish observation from inference |
| Runtime | A perfect aggregate score could conceal a timeout or omitted case | Offline gate makes incomplete comparisons nonpassing, preserves outcome counts and separates provider errors from quality |
| Maintainability | Multiple host copies could drift or duplicate names | One canonical skill folder, shared metadata reader, duplicate detection and generated catalog checked in CI |
| Integration | Setup might be mistaken for a successful agent task | Reserved Copilot setup job prepares prerequisites; document startup despite setup failure and separate invocation evidence |
| Scope | Generic worksheets did not cover runtime, persistence and repository-shape findings concretely | Add linked boundary references for correlation, retries, cancellation, artifact identity, crash limits, writers and repository classification |
| Contract | Regression budget wording could imply a total-failure allowance | Clarify new regressions versus unchanged nonrequired failures; add an explicit public CLI case |

The review used counterexamples, failure premortems, alternative-cost comparison,
independent test oracles and a separate implementation reviewer. Review stopped
after these material findings were resolved; it did not require an unbounded
series of opinions or a fixed multi-agent chain for future routine work.

## Forward task exercises

A separate worker read the relevant bundled procedures and completed each
supplied task. Another independent worker exercised the AI decision procedures.
These fixtures requested plans, test proposals or decisions from supplied
information, not application execution. No fictional run was reported as real.

| Scenario | Expected distinguishing behavior | Observed output |
| --- | --- | --- |
| Plan customer CSV export alongside existing JSON command | Preserve callers, select fields explicitly, protect existing files and challenge edge cases | Chose separate command, excluded token data, specified CSV escaping and exclusive creation, identified unknown API and platform evidence |
| Split a CSV implementation within 20 minutes | Prevent competing writers, resolve dependencies and stop at budget | Assigned sole owners, froze serializer interface before dependent edits, reserved integration/review time and defined partial/blocked handoffs |
| Design quote-cell regression cases | Reject an expected-value helper that calls production code | Derived seven literal cases independently, including quotes, commas, newline, Unicode and empty text; proposed a separate CSV-reader consumer check |
| Diagnose export followed by upload failure | Identify the first local cause rather than changing cloud credentials | Identified missing output parent as first failure, proposed a cwd/resolved-parent check and kept directory-creation policy unresolved pending evidence |
| Select a retrieval prompt candidate with partial evidence | Reject omitted required cases and provider errors despite a perfect reported score; respect unrelated edits and budget | Retained the baseline, classified timeout as incomplete execution, rejected omitted required B, preserved teammate API edits and stopped at 15 minutes |

The AI exercise initially encountered a report-document link while that file was
still being authored. It did not invent a schema or execution evidence. The
completed [report contract](../evaluation-reports.md) and all local links were
subsequently validated. No behavioral skill defect was found in these bounded
fixtures; this does not predict every future task or client.

## Executable evidence

The [validation record](../../VALIDATION.md) records complete repository checks.
New catalog tests exercise missing/stale output, deterministic generation,
metadata escaping, duplicate definitions, invalid roots and preservation of files
on invalid input. Evaluation CLI tests cover valid and malformed reports,
provenance, case/label identity, required failures, regression budgets, incomplete
outcomes, duplicate keys, nonfinite numbers and unchanged input bytes.

The independent reviewer also checked 625 two-case combinations of complete and
incomplete outcomes against a separately derived decision oracle; no decision
mismatch was found. This was a bounded semantic inspection, not a model benchmark.
The reviewer reported no blocking evaluator or catalog implementation defect.
