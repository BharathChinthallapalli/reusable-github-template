---
name: test-design
description: Design meaningful regression, boundary and contract tests using independent expected results and real consumer behavior. Use for a new behavior, demonstrated bug or verification gap; skip tests for wording-only edits or checks that mirror the implementation.
---

# Design tests that can falsify a claim

Identify the public seam and observable behavior before choosing a framework:
function result, serialized artifact, CLI exit/output, HTTP response, rendered
interaction or state transition. Read existing tests and commands; use
[clean-code](../clean-code/SKILL.md) when implementing or changing test code.

Choose an oracle independent of the changed implementation where practical:
a hand-derived example, domain invariant, trusted reference, round trip with a
known expected value, or consumer-observable state. Copying the production
formula into an expected-value helper can reproduce the same bug. A snapshot
alone does not establish semantic validity of generated output.

Adapt the [behavior case matrix](assets/behavior-case-matrix.md) to the changed
contract. Select meaningful success, rejection and boundary cases, including
false/zero/empty distinctions only when the API treats them differently.
For lifecycle or persistence changes, test cleanup, repeat use or save/load through
the actual boundary; use [persistence contracts](references/persistence.md) when
serialization, compatibility or publication behavior changes. For a bug fix,
reproduce the reported failing case and a
nearby case that should continue working.

Confirm a failed assertion or invalid result causes a nonzero test-command result.
For generated code or packages, check the artifact through its consumer when the
change affects that boundary. Keep static metadata, integration behavior and real
host execution separate. Use isolated temporary state for tests that write files;
do not reuse fixed output paths across parallel tests.

For model, prompt, retrieval or dataset changes, follow
[AI evaluation](../../../docs/ai-evaluation.md): deterministic code checks do not
replace independent behavioral cases, and a provider error is not a quality score.

Run focused cases and required gates through
[verify-change](../verify-change/SKILL.md). Broaden only for a concrete remaining
risk. Report checks that were blocked or not run rather than weakening assertions
or changing expected results simply to obtain green output.
