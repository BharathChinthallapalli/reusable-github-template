---
name: "code-review"
description: "Review a diff for demonstrable bugs, authorization failures, data loss and regressions using affected callers, contracts and tests as evidence."
---

# Review a change

1. Establish the base and head revisions and the intended behavior. Read the
   complete diff and applicable instructions; inspect affected callers and
   contracts before judging a suspicious line in isolation.
   Use a supplied diff or an available read-only diff tool. If neither exists,
   request the missing baseline/diff or explicitly narrow the review to supplied
   files; never invent revision history or claim a complete diff review.
2. Prioritize incorrect results, access-control failures, data loss, broken
   compatibility, error handling and credible reliability regressions.
3. For each candidate, trace a concrete input or execution path to the impact.
   Check guards, framework behavior and tests that could disprove the concern.
4. Use [the finding standard](references/findings.md) to separate verified
   defects from hypotheses and optional improvements. Use current official
   documentation when a finding depends on platform or version behavior.
5. Report actionable findings in impact order with the smallest relevant code
   location, evidence and verification status. If none are found, say so and
   identify material coverage limits without declaring the change bug-free.

Apply [clean-code guidance](../clean-code/SKILL.md) for readability and design
advice. Respect established conventions; do not promote arbitrary function
lengths, naming preferences or speculative abstractions into blocking defects.
Review read-only unless the user also requested fixes. Do not publish review
comments or approve a pull request without authorization for that action.
