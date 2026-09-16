# Harness philosophy

Design lens: reduce the effort required to understand, change and verify the
system. The canonical index of accepted engineering decisions remains
[engineering principles](../engineering-principles.md); this page explains the
reasoning behind that lens rather than creating another policy hierarchy.

## Make necessary complexity easier to carry

An added file, rule, service or agent should resolve a demonstrated problem.
Judge a design by the ordinary task it enables: how much must the contributor
read, how many places must change together, and what can fail unexpectedly?
Removing useful checks merely to reduce file count fails this test too.

Keep each fact in one maintained home. Link consumers to it. Put change-specific
state in a task record, durable rationale in an ADR, and executable restrictions
in the applicable control. A reader should not reconcile five definitions of
the same term before making a safe edit.

## Make the useful path predictable

Use deterministic tooling for repeatable checks and bounded model judgment for
ambiguous work. A failed check should identify the relevant contract and recovery
path. Select context for the task; a larger library need not mean a larger prompt.
Model capability changes how much investigation is useful, not who may approve
an action or which permissions apply.

## Preserve evidence and stopping points

Improve working systems in reviewable increments. Connect each change to an
observable result, retain enough evidence to reproduce it, and stop once the
accepted outcome is verified. New unrelated findings belong in later work.
State unknowns explicitly so the next session can continue without inheriting
false certainty. A passing check has a scope; it is never universal assurance.

## Source and interpretation

John Ousterhout, *A Philosophy of Software Design*, first edition (2018),
chapters 1-2, supplied by the owner, informs the focus on understanding and
modification cost, incremental design, and moderation when applying principles.
The harness applications above are this repository's synthesis. The book is not
a runtime policy and its text is not bundled here. See [opinions](opinion.md)
for revisable defaults and [non-goals](nongoals.md) for boundaries.
