---
description: "TypeScript and JavaScript test changes; use existing test tools and risk-based coverage."
applyTo: "**/*.test.ts,**/*.test.tsx,**/*.spec.ts,**/*.spec.tsx,**/*.test.js,**/*.test.jsx,**/*.spec.js,**/*.spec.jsx,**/vitest.config.*,**/playwright.config.*,**/jest.config.*"
---

# Tests that establish behavior

Use the installed test runner, its version and the relevant existing configuration.
Follow the shared [test-design](../../.agents/skills/test-design/SKILL.md) and
[verification](../../.agents/skills/verify-change/SKILL.md) procedures when relevant.

- Assert observable outcomes against a known contract. Test meaningful failure,
  authorization and boundary cases; coverage percentages alone do not prove them.
- Reproduce a behavioral bug before fixing it when practical. Keep a regression
  case that fails for the old behavior, rather than mirroring the repaired code.
- Keep fixtures synthetic, deterministic and independent. Inline data is fine for
  simple cases; introduce factories only when they improve reuse or clarity.
- Await asynchronous assertions and clean up timers, spies, servers and files.
  In Vitest, `clearAllMocks()` clears call history, not implementations or configured
  return behavior. Use reset/restore deliberately according to the installed API.
- For current Vitest function typing, use a function signature such as
  `vi.fn<(id: string) => Promise<boolean>>()` or `vi.fn<typeof existingFunction>()`.
  Do not copy legacy two-generic mock examples without checking the installed version.
- Choose Node or browser-like test environments by the subject. Derive aliases from
  actual Vite/Vitest/TypeScript configuration; do not invent a `test.tsconfig` option.
- Mock external services at an explicit boundary or use an approved test environment.
  Inspect test setup/teardown, lifecycle scripts and endpoint configuration first.
  Recorded fixtures must be sanitized before committing.
- Run focused checks first and broader suites for affected contracts or required CI.
  Do not add Testcontainers, visual regression, mutation testing or load infrastructure
  solely to satisfy this guidance. Ordinary prose or style edits do not automatically
  need new test cases or a full E2E run.
- Keep failure screenshots and logs free of secrets and personal data. Check the
  application's keyboard/focus behavior as well as automated accessibility findings
  when an interaction changes. Report manual or screen-reader checks only if run.

Sources and limitations: [research](../../docs/research/scoped-development-rules.md).
