---
description: "TypeScript implementation and configuration; follow the nearest project's installed toolchain."
applyTo: "**/*.ts,**/*.tsx,**/*.mts,**/*.cts,**/tsconfig*.json,**/eslint.config.*,**/biome.json,**/biome.jsonc"
---

# TypeScript development

Read the nearest manifest, relevant lockfile entries, compiler configuration and
affected callers. This template does not select TypeScript, Next.js, a package
manager or a formatter for an application. Preserve the project's actual choices.

- Use meaningful types and narrowing. Treat external JSON as untrusted input;
  assertions, branded types, template literal types and `satisfies` do not perform
  runtime validation. Validate at the boundary with the project's existing approach.
- Use `satisfies` for compatible configuration shapes when retaining inference is
  useful. Do not force it onto every declaration or describe it as runtime checking.
- Preserve the existing error contract. Model expected recoverable outcomes with
  a discriminated union when callers need to branch; a union does not itself force
  callers to inspect the result. Do not hide unexpected failures in success values.
- Keep types near their owning feature; share a stable contract when there are real
  consumers. File counts do not justify a global types directory or new domain layer.
- Preserve interface/type conventions. Make mutation explicit, avoid surprising
  changes to arguments, and use default parameters or `??` according to whether
  only undefined or both null and undefined should trigger the fallback.
- Keep compiler checks enabled. Do not silence errors with broad `any`, casts,
  exclusions or ignored build errors to make verification pass.
- Reuse existing ESLint/Biome/formatter configuration. In ESLint flat config, use
  configuration objects with `files` patterns, not an eslintrc `overrides` property.
  Let the configured formatter own line wrapping and whitespace.
- Keep suppressions specific and explained. Biome's next-line `biome-ignore` and
  top-level `biome-ignore-all` have different scope; do not disable a whole file
  when a narrow correction is possible. Verify syntax against the installed version.
- Measure an actual bottleneck before introducing workers, caches, object pools
  or import rewrites. A namespace import alone does not prove failed tree shaking.

Before install/build/test, inspect scripts, relevant lifecycle hooks and target
configuration. A command name is not proof it is local or harmless. Use established
registries and lockfiles; do not auto-install a missing formatter or run an unknown
downloaded executable to satisfy a generic rule. Ordinary authorized development
commands remain allowed within [the shared boundaries](../../AGENTS.md).

Use [test guidance](typescript-testing.instructions.md) for affected tests and
[Next.js guidance](nextjs.instructions.md) only in an actual Next.js project.
Sources and selection decisions: [research](../../docs/research/scoped-development-rules.md).
