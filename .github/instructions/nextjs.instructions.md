---
description: "Next.js routes, rendering, server actions and configuration, only when the affected project actually uses Next.js."
applyTo: "**/app/**/*.ts,**/app/**/*.tsx,**/app/**/*.js,**/app/**/*.jsx,**/pages/**/*.ts,**/pages/**/*.tsx,**/pages/**/*.js,**/pages/**/*.jsx,**/next.config.*,**/middleware.ts,**/middleware.js,**/proxy.ts,**/proxy.js"
---

# Next.js application boundaries

Apply only when the nearest application manifest and source establish Next.js.
Identify its installed version and whether the affected path uses App Router or
Pages Router. Folder names alone do not establish the framework. Do not migrate
routers, runtimes or framework versions as a side effect of unrelated work.

- In App Router, keep server work server-side; introduce a client boundary only
  for interactivity or browser APIs. Send only necessary serializable data across it.
- Keep secrets and privileged data access out of browser imports and public
  environment variables. Use server-only boundaries where appropriate.
- Treat exported Server Actions and route handlers as external entrypoints.
  Validate input and check identity, tenant and object-level authorization inside
  the relevant server operation. A hidden button, layout check or proxy is not
  sufficient authorization for the underlying mutation.
- Match caching and invalidation to data ownership and freshness requirements.
  Never share personalized results through a public cache without a safe design.
  Do not add a service worker, CDN or cache library merely because this file exists.
- Follow the installed request API contract. For Next.js 16, await `cookies()`,
  `headers()` and asynchronous route inputs; prefer supported inferred/generated
  types over imports from private framework internals.
- Next.js 16 renames middleware to proxy with runtime differences. Review those
  differences before a migration; do not blindly rename an existing Edge entrypoint.
  Use native Request/Response or NextRequest/NextResponse as required by the API.
- Preserve framework control flow: expected form failures can be return values;
  unexpected defects use the appropriate error boundary. Do not swallow redirect
  or not-found signals in a broad catch block.
- Keep rendering free from business mutations. Use the application's supported
  mutation mechanism and handle validation, pending, failure and success states.
- Check the actual lint/typecheck/test/build scripts. Next.js 16 removes `next lint`
  and automatic build linting; a successful build is not evidence linting ran.
- Use the existing image and asset pipeline. Add responsive sizing, accessible
  alternatives and restrictive remote sources rather than a second image system.

Verify changed server contracts and user flows using the current project tools.
Use synthetic identities and an authorized test target; do not inspect personal
browser profiles or mutate a live tenant to validate a component.
See [research and version sources](../../docs/research/scoped-development-rules.md).
