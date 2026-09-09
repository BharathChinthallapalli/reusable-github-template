# John Papa repository research

Source snapshot limit: the accompanying [inventory](johnpapa.json) records file blob SHAs and tree SHAs, but no verified commit HEAD for these selected files. Source links therefore retain their recorded default branches; blob and tree SHAs are not substituted as commit references.

Checked 2026-09-09 using current, first-party GitHub repository metadata, file contents, and recursive Git trees. This document contains original analysis; no source implementation or manual was copied into the template. No external repository was installed or executed.

## Coverage and limits

The accompanying `johnpapa.json` enumerates **160 unique public repositories** returned by repository search `user:johnpapa fork:true`. Pagination used 100 results per page: page 1 returned 100, page 2 returned 60, and pages 3 and 4 returned zero. The inventory is complete for that search at fetch time, below GitHub's search-result cap. Public indexing can lag changes; this is not an inventory of private repositories.

| Coverage | Count |
| --- | ---: |
| Repository metadata/overview inspected | 160 |
| Original repositories | 108 |
| Forks, with parent attribution retained | 52 |
| Archived repositories, overlapping the groups above | 14 |
| READMEs retrieved and introductions/initial headings inspected | 155 |
| No root README after root-directory inspection | 3 |
| Empty repositories | 2 |
| Selected deeper reviews of docs/configuration/implementation/tests | 8 repositories |
| Additional non-README files whose text was reviewed | 45 |
| Full repository code audits | 0 |

The broad pass read repository descriptions and README introductions/headings, not every line of every README or every source file. Selected reviews below inspected concrete files; their paths, blob SHAs, and coverage are recorded per repository in the JSON. Trees were complete for these inspections. Read operations occurred over several minutes, so they do not establish a single atomic snapshot across all repositories.

`TypeScriptDemos`, `es6.io`, `Breeze-Angular-Meetup-20130312`, `ngconf2015demo`, and `static-web-apps-cli` use lowercase `readme.md`; these were retrieved after inspecting the root directory. `.github`, `vscode-import-bug`, and `BroncoSueWeb` had no root README. `dotfiles` and `test` were empty. These five exceptions are labeled explicitly rather than counted as README reviews.

## Findings from the eight selected repositories

### ai-ready

The [skill](https://github.com/johnpapa/ai-ready/blob/main/skills/ai-ready/SKILL.md), [detection tables](https://github.com/johnpapa/ai-ready/blob/main/skills/ai-ready/references/detection-tables.md), [GitHub discovery procedure](https://github.com/johnpapa/ai-ready/blob/main/skills/ai-ready/references/github-discovery.md), [mechanism guide](https://github.com/johnpapa/ai-ready/blob/main/docs/how-it-works.md), and both CI/setup workflows were read.

Useful ideas are discovering actual manifests and commands before writing guidance; distinguishing a real workspace from a collection of independent examples; preserving existing configuration; checking for instruction drift on subsequent runs; and recording exact related files that must change together. The last idea is especially relevant to the template: changes to initializer parameters, supported metadata, CI job names, or development requirements affect identifiable tests, documents, and workflow configuration.

Review feedback can provide candidate conventions, but repeated comments should be checked against current accepted decisions and code before being promoted into instructions. A small, bounded sample is enough unless it leaves a specific uncertainty.

Do not adopt the repository's asset-count readiness score as evidence of successful agent behavior. Its prose makes broad host/discovery claims, and its skill includes automatic file-generation and merge policies that must not supersede task authorization. Generating an MCP server configuration merely because a dependency was detected is inappropriate for a portable starter without an established integration need.

The [actual CI](https://github.com/johnpapa/ai-ready/blob/main/.github/workflows/ci.yml) checks skill metadata, manifest-version alignment, and CLI discovery. These are distinct checks worth separating. However, the workflow uses mutable Action tags and `skills@latest`, and imports PyYAML without declaring its installation in the inspected workflow. Reuse the validation boundaries, not its dependency assumptions.

### vscode-peacock

The [agent guide](https://github.com/johnpapa/vscode-peacock/blob/main/AGENTS.md), [CI](https://github.com/johnpapa/vscode-peacock/blob/main/.github/workflows/ci.yml), Copilot setup workflow, contribution guide, configuration updates, command tests, and [package-content checker](https://github.com/johnpapa/vscode-peacock/blob/main/scripts/check-vsix-contents.js) were inspected.

This provides the strongest current engineering example in the selected set. It separates tests for pure logic from tests in the real VS Code extension host, with browser tests for its documentation site. Its host tests exercise command results and the clipboard, while configuration code avoids writing a new empty settings file. This is a useful model for selecting tests according to the boundary being changed instead of choosing one test style universally.

The packaging check examines the actual extension contents, excludes development-only paths, and checks size. The portable lesson is to validate what gets distributed when an application gains a package or deployment artifact. A generic repository should not inherit VSIX-specific files or a size threshold.

The guide gives concrete registration chains for adding commands and settings and points at real source files. That is more valuable than generic clean-code slogans. Its long release/social-publishing procedure is specific to this maintainer and is not appropriate for the shared base.

Core CI ignores Markdown. That is a poor default for this template, where Markdown contains agent instructions and skill definitions that require validation. The inspected workflow also uses Action tags rather than immutable commit pins. Preserve the template's stronger existing controls.

### lite-server

The complete README and [AGENTS.md](https://github.com/johnpapa/lite-server/blob/main/AGENTS.md), package scripts, default configuration, [server implementation](https://github.com/johnpapa/lite-server/blob/main/lib/lite-server.js), [behavioral tests](https://github.com/johnpapa/lite-server/blob/main/test/lite-server.spec.js), CI, setup, and Dependabot configuration were read.

A small entry point delegates to named defaults and a focused implementation. Tests exercise configuration merging, an absent optional configuration file, and function-based configuration. They clean up mocks between tests. The agent guide names the actual command expansion and test-isolation requirements, and explicitly records that the project needs no compiler. Carry this evidence-based specificity into generated project context; do not introduce a toolchain because a reference project has one.

Its current [Copilot setup workflow](https://github.com/johnpapa/lite-server/blob/main/.github/workflows/copilot-setup-steps.yml) has a job named `copilot-setup`. GitHub requires the single job to be named `copilot-setup-steps`; the filename alone is insufficient. This is a concrete discovery failure, not just a formatting preference. [GitHub's environment configuration documentation](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-environment) also says setup failure can leave the agent working in the partially prepared environment. Validate both the identifier and the observed setup result.

The inspected CI uses mutable Action tags and `npm install`. Its conventions and tests remain useful, but its workflow should not replace the current template's pinned Actions and explicit dependency setup.

### github-templates

The complete README, contribution guide, issue template, PR template, EditorConfig, and complete 11-file tree were inspected. The repository's last push was in 2017. [Its files](https://github.com/johnpapa/github-templates) offer clear places to record reproduction steps, environment versions, purpose, and verification. They contain no executable initializer or CI.

Treat this as historical documentation design. It contains old environment examples, placeholders, and a force-push instruction. The existing template's validated initializer, modern issue forms, and explicit verification already provide a stronger foundation. Adding more boilerplate from this repository would not improve it.

### cloud-coding-with-codespaces

The README workflow, [development container](https://github.com/johnpapa/cloud-coding-with-codespaces/blob/main/.devcontainer/devcontainer.json), Dockerfile, scripts, [Playwright configuration](https://github.com/johnpapa/cloud-coding-with-codespaces/blob/main/playwright.config.ts), browser tests, and deployment workflow were inspected.

The transferable idea is a coherent first-run path: distinguish editing from running, name the services and ports, prepare a reproducible environment, and let tests start the required local services with readiness checks. It uses a nonroot development user and explicit port labels.

The actual container selects Node 16, the app selects Angular, and the workflow is tied to a particular Azure Static Web App. The install command joins app/API installation with a semicolon, which can obscure the first failure if the second command succeeds. These are reasons to write an optional, current project-specific devcontainer after stack selection, not copy the sample into the neutral base. Publicly forwarding a demonstration port should remain an explicit sharing decision.

### shopping-for-codespaces

The README, complete tree, [package scripts](https://github.com/johnpapa/shopping-for-codespaces/blob/main/package.json), and [entry point](https://github.com/johnpapa/shopping-for-codespaces/blob/main/index.js) were inspected. The tiny application makes the transition from browser editing to a runnable environment easy to explain.

The inspected tree has no dedicated test suite or checked-in development container, and package scripts provide only start/dev commands. Its value is onboarding narrative, not production completeness. Do not infer an environment specification or test gate merely from a Codespaces name or README walkthrough.

### vscode-cloak

The README's operation and scope explanation, [configuration-writing code](https://github.com/johnpapa/vscode-cloak/blob/main/src/configuration/update-configuration.ts), basic host tests, and [CI](https://github.com/johnpapa/vscode-cloak/blob/main/.github/workflows/ci.yml) were inspected.

The extension changes editor token colors to conceal values visually. It does not establish data access restrictions. This is a useful example for describing the boundary of a control precisely: visual concealment, static validation, host discovery, and authorization are different properties.

The workflow makes the extension test step nonblocking with `continue-on-error: true`, while continuing to package the extension. That behavior should not be copied into a required template quality gate. A check must distinguish pass, failure, skipped, and unavailable evidence.

### mcp-starwars

The README overview/tool documentation, [entry point](https://github.com/johnpapa/mcp-starwars/blob/main/src/index.ts), [schemas](https://github.com/johnpapa/mcp-starwars/blob/main/src/schemas.ts), tool handlers, [cache implementation](https://github.com/johnpapa/mcp-starwars/blob/main/src/caching.ts), release workflow, package scripts, local MCP configuration, and empty environment template were inspected.

Explicit tool schemas, named tool handlers, and cache hit/miss statistics are useful concepts. The code also provides concrete failure cases for a portable engineering guide:

- The server uses `StdioServerTransport` while emitting banners and request logs through `console.log`. MCP requires stdout to contain protocol messages only; diagnostic output belongs on stderr. This follows directly from the [MCP transport specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports).
- On HTTP 429, the cache code decrements `maxRetries` but never checks whether it has reached zero before recursively retrying. A counter in a signature is not an enforced retry limit.
- The selected package has no test script and its tree has no dedicated test suite. Its local MCP configuration contains a maintainer-specific path. Neither should be treated as a portable, verified integration.

Use these as examples for meaningful boundary tests and finite retry budgets. Do not add this MCP server, its dependencies, release credentials, or runtime to the template.

## Other useful exclusions

[skill-verify](https://github.com/johnpapa/skill-verify) currently describes planning and future installation; the complete tree contains only README and LICENSE. It is not an implemented validator to adopt. [security-strategy-essentials](https://github.com/johnpapa/security-strategy-essentials) describes a picture-memory game in its README. Repository names, badges, or search rank do not establish engineering content or readiness.

The many Angular/Vue/Svelte/React examples and upstream forks are retained in the inventory. They can inform an optional stack-specific starter, but they do not justify choosing a framework, cloud, package manager, or architecture in the shared foundation.

## Fit for the existing portable template

1. Add or refine a concise change-dependency table derived from this repository: initializer contract → initializer/checker tests and setup docs; AI metadata contract → validator/tests/host guidance; dependency change → local setup and CI; CI job rename → ruleset and setup docs; ADR replacement → statuses, index, and backlinks.
2. Keep onboarding commands and prerequisites identical across README, agent guidance, local setup, and CI. A future Copilot setup workflow should run the same declared setup, with its reserved job identifier validated.
3. Keep required checks active for AI Markdown and configuration changes. Do not turn failures into green checks to accommodate an unavailable host.
4. Select tests by observable behavior and integration boundary. Add distribution-content checks only once there is an actual package to distribute.
5. Keep optional runtime containers, application frameworks, MCP servers, deployment credentials, and publishing workflows out of the neutral base until a project requires them.
6. Report separate evidence for static validity, discovery in a named host, actual invocation, and observed behavior. None of the inspected repository badges replaces these checks.

The existing initializer protections, 51 tests, pinned Actions, explicit setup dependency, and static-versus-host distinction should be preserved. The highest-value improvement from this account is tighter relationships between evidence, instructions, commands, and verification—not a larger collection of files.
