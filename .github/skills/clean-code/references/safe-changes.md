# Safe changes

Fowler's second edition treats refactoring as restructuring without changing
observable behavior. A requested new output or error contract is a behavior
change, even if the implementation also becomes easier to read.

| Task | Useful verification boundary |
| --- | --- |
| Fix a defect | Reproduce it through an existing public operation; add a regression test when practical |
| Change behavior | Capture the relevant old contract, specify the new expectation, and check affected callers |
| Refactor covered code | Establish a passing relevant baseline, transform one responsibility, and rerun those checks |
| Change unfamiliar legacy code | Characterize the behavior at an accessible boundary before moving internal logic |

Use the smallest test boundary that demonstrates the requirement: returned
values, observable state, emitted events, or external requests. Avoid assertions
on private helper names or incidental call sequences. Add a narrow dependency
seam only when it makes a needed behavior controllable, such as supplying a
clock to verify expiry. Preserve the production contract.

Useful catalog candidates:

- [Extract Function](https://refactoring.com/catalog/extractFunction.html) for
  a concept whose name makes the caller clearer.
- [Inline Function](https://refactoring.com/catalog/inlineFunction.html) when
  an indirection no longer explains anything.
- [Replace Nested Conditional with Guard Clauses](https://refactoring.com/catalog/replaceNestedConditionalWithGuardClauses.html)
  when early exits reveal the main path.
- [Separate Query from Modifier](https://refactoring.com/catalog/separateQueryFromModifier.html)
  when a read unexpectedly changes state.

Check each meaningful structural increment. Avoid combining it with unrelated
renames, dependency updates, or formatting sweeps. Preserve error types,
serialized shapes, ordering, and side effects that callers depend on.

If a baseline failure blocks evidence, identify it and find a narrower valid
check where possible. Do not rewrite expected results simply to make the new
implementation pass. Finish with the relevant repository checks and a diff
review; distinguish observed results from untested assumptions.
