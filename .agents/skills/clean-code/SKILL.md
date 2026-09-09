---
name: clean-code
description: Implement features, fix bugs, and refactor code with readable names, justified abstractions, preserved contracts, and behavior-focused verification. Use for code changes and clean-code requests; skip prose-only edits and unrelated planning.
---

# Clean code

Deliver the requested behavior with code that the next maintainer can follow.
Respect repository instructions, existing contracts, and established formatting.

Before editing, inspect the affected callers, tests, configuration, and current
diff. Identify the intended outcome, behavior to preserve, and a useful way to
verify the result. Discover commands from repository evidence.

- For naming, extraction, or abstraction choices, read
  [design decisions](references/design-decisions.md).
- For bug fixes, legacy code, or structural changes, read
  [safe changes](references/safe-changes.md).
- For attribution and the boundaries of this guidance, read
  [sources](references/sources.md). Consult official runtime documentation when
  an API or language behavior is uncertain.

Implement in small, reviewable increments. Limit cleanup to the affected
responsibility. Keep behavior changes distinguishable from refactoring, and
preserve public interfaces unless the requested outcome requires a change.
Do not widen the public API solely to expose private internals to tests.

Follow the repository's formatter and error conventions. Make side effects
visible. Document non-obvious decisions and constraints when code cannot
express them; avoid comments that repeat the next statement.

Verify at a stable observable boundary, using relevant success, boundary, and
failure cases. Select checks proportional to the change. Inspect the final
diff and report the outcome, checks actually run, and any remaining limitation.
A formatting check is not evidence of correct application behavior.

Apply source principles with judgment: function length alone does not justify
extraction, similar syntax does not prove shared responsibility, and shorter
code does not establish better performance.
