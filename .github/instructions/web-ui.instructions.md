---
description: "Browser UI styling, accessibility and responsiveness; preserve the actual application's design system."
applyTo: "**/*.tsx,**/*.jsx,**/*.html,**/*.css,**/*.scss,**/tailwind.config.*"
---

# Browser UI changes

Apply browser-specific guidance only to browser UI, not native/mobile components
or unrelated JSX renderers. Reuse the project's design system, installed styling
approach and formatter. Do not combine Tailwind, CSS Modules, CSS-in-JS and Sass
or install a component/animation library merely because they appear in a catalog.

- Keep semantic controls, accessible labels and visible keyboard focus. Use native
  HTML or existing accessible components before implementing custom ARIA widgets.
- For modal dialogs, manage entry focus, contain keyboard navigation, support the
  appropriate dismissal behavior and restore focus to the trigger or a logical
  successor. Verify the actual interaction against the WAI-ARIA dialog pattern.
- Keep status/error announcements proportionate; do not turn every update into an
  interrupting alert. Never encode meaning through color alone.
- Check narrow/wide layouts, zoom, overflow and touch targets. Preserve useful table
  content with an accessible overflow or alternate layout. Respect reduced motion.
- Keep design tokens and existing class composition helpers. `clsx` selects class
  names; it does not resolve Tailwind conflicts. Use the project's compatible merge
  helper only where override behavior is required.
- For Tailwind, inspect the major version. Version 4 uses `@utility` to register
  custom utilities; do not transplant v3 `@layer`/purge configuration unchanged.
  Keep existing CSS Modules or Sass conventions when those are the selected stack.
- Add lazy loading, list virtualization or memoization for a measured problem,
  preserving keyboard access and state. An arbitrary item-count threshold is not
  a performance requirement.
- Use existing UI tests and available visual inspection to verify changed states.
  Automated accessibility tools complement manual checks; do not claim a universal
  detection percentage or a screen-reader pass without observed evidence.

Sources and selection: [research](../../docs/research/scoped-development-rules.md).
