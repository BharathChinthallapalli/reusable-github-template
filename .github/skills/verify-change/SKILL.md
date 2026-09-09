---
name: "verify-change"
description: "Choose and run proportionate checks for a code or configuration change, distinguish existing failures from regressions and report evidence accurately."
---

# Verify the change

1. Read the diff and affected callers. Identify the observable behavior and the
   credible failure modes introduced or corrected by the change.
2. Derive commands, working directories, runtime versions and prerequisites
   from repository instructions, manifests, existing tests and CI. Inspect
   scripts before execution; do not invent a test command or install a new
   framework to satisfy a generic checklist.
3. Record existing failures when relevant and practical before editing. Preserve
   local work; use an isolated checkout if a baseline comparison is needed.
4. Select focused behavioral checks using
   [the verification guide](references/verification.md). Add regression coverage
   for meaningful failures; avoid tests that merely repeat implementation text.
5. Run required repository gates and relevant application checks. Broaden only
   for an unresolved risk, affected boundary or documented gate.
6. Report the revision or working tree checked, exact commands, results and
   material limitations. Distinguish passed, failed, blocked and not run.

Do not silence a failure, weaken assertions or update expected output merely to
make a check pass. Diagnose whether the expectation or implementation is wrong.
Use [clean-code guidance](../clean-code/SKILL.md) when correcting production code.
