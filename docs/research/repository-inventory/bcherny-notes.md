# bcherny public-repository research

As of 2026-09-09. This is an original, evidence-linked synthesis for the reusable GitHub template.

## Coverage and limits

The supported GitHub repository search query `user:bcherny fork:true` returned 100, 100, 71, and 0 repositories on pages 1–4 (100 per page): **271 unique public repositories, including 111 forks and 160 non-forks; none marked archived**. Separate metadata reads verified fork parents, descriptions and flags. The connector did not expose GitHub's `total_count` or `incomplete_results`, so this is complete coverage of the paginated visible search results, not a guarantee against newly unindexed or changing repositories.

All 232 nonempty discoverable root READMEs had their opening substantive overview read; alternate casing and one misspelled name were resolved through directory listings. Longer README bodies were not audited in full. For 31 repositories with no usable root README, primary-file/manifest inspection found 30 readable alternatives and one blank static site; one alternative was a nested slideshow README. Eight further repositories are API-confirmed empty.

| Coverage tier | Count | Meaning |
| --- | ---: | --- |
| deep-sampled | 7 | Selected actual code, tests and configuration inspected in seven repositories. |
| directory-only | 1 | whotracksme.org has a blank README and blank static index. |
| empty-metadata-only | 8 | Contents API reports the repository is empty; no behavior inferred. |
| overview-read | 227 | README opening; short files in full. Minimal placeholders remain explicitly identified. |
| primary-file-read | 28 | Selected manifest, source or primary page where the root README was missing/blank. |

No remote code was cloned, installed or executed. No tests, hooks, websites or account actions were run. These observations do not certify quality, security, test results or current package compatibility. A fork is not evidence that Boris Cherny authored every upstream behavior. The companion JSON records each repository's metadata, overview path/blob SHA, coverage, and source links; detailed inspections include fetched default-branch head SHAs and pinned file URLs.

## Patterns to adapt

- Keep instructions and hooks small enough to explain their inputs, output, failure behavior and activation event. Availability is different from execution: the inspected Claude workflow reacts to an explicit mention, and the emitter's cycle diagnostics are an explicit development option.
- Validate configuration semantics and the artifact a consumer will actually use. JSON-schema-to-TypeScript independently type-checks generated output; presence of a test file, schema field, matrix entry or command name is insufficient.
- Test rejection and nonmatching cases as well as success. Useful examples distinguish null/undefined from false, zero and empty strings; cover subscribe/unsubscribe lifecycles; and verify protected file contents remain unchanged after a rejected operation.
- Preserve failure exit status and make every required CI dependency participate in the final check. Several inspected examples show how comments or script names can overstate what really runs.
- Separate quick local checks from host/OS permissions. A pre-commit formatter is convenient local feedback. The sandbox fork applies actual restrictions in platform code with separate integration tests; it does not turn the Git hook itself into a sandbox.
- Document an observed performance issue, controlled measurement procedure and an expected result before adding architecture. The Undux memory profile names a lifecycle scenario and explicitly leaves CI automation unfinished.

## Detailed source inspections

### json-schema-to-typescript

Default-branch head: `5caacfc53671f9c891bb4e2a78bccc6190ed3ef4`. 

- Compiler phases are mapped to concrete files; option validation throws descriptive errors before processing.
- Generated declarations are snapshot-tested and independently compiled by TypeScript under strict options. Invalid-input cases assert rejection rather than recording error text as success.
- CI separately exercises built package compatibility, a minimum runtime, fuzz seeds and corpus/spec output. The Claude workflow is triggered by explicit @claude text and needs a secret.
- Static integration defect: ci-ok depends on build, bun, engines, fuzz and output but checks only build/fuzz/output results. Its comment overstates the aggregate guarantee.

Template implication: Keep a concise command/contract map, validate generated artifacts with the consuming tool, and make required-check aggregation include every required job.

Do not carry forward: Do not copy the secret-dependent mention workflow, auto-publish policy, package stack, action tags or incomplete aggregate check as universal defaults.

Inspected files:

- [ARCHITECTURE.md](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/ARCHITECTURE.md) — File read.
- [CONTRIBUTING.md](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/CONTRIBUTING.md) — File read.
- [.github/workflows/claude.yml](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/.github/workflows/claude.yml) — File read.
- [.github/workflows/ci.yml](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/.github/workflows/ci.yml) — File read.
- [src/optionValidator.ts](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/src/optionValidator.ts) — File read.
- [test/typecheck.test.ts](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/test/typecheck.test.ts) — File read.
- [test/e2e.test.ts](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/test/e2e.test.ts) — File read.
- [package.json](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/package.json) — File read.

### undux

Default-branch head: `687a4f0f0d3326356460285e29d6b706e95b571d`. 

- Public Store interface carries key/value relationships; StoreSnapshot and StoreDefinition separate observed state from updates.
- Connected store owns its subscription and unsubscribes during unmount; browser tests check rendered values after clicks and missing-provider failure.
- Memory benchmark records allocate/unmount/snapshot steps and explicitly leaves CI automation unfinished.
- Static CI mismatch: matrix declares operating systems but runs-on is fixed to ubuntu-latest. Bad-case Flow files exist, but the inspected npm test path does not call their shell runner.

Template implication: Verify visible behavior and cleanup across lifecycle transitions, and distinguish declared test coverage from commands actually executed.

Do not carry forward: Do not install React/RxJS for a neutral template or describe a declared OS matrix/manual memory profile as verified coverage.

Inspected files:

- [src/index.ts](https://github.com/bcherny/undux/blob/687a4f0f0d3326356460285e29d6b706e95b571d/src/index.ts) — File read.
- [src/react/createConnectedStore.tsx](https://github.com/bcherny/undux/blob/687a4f0f0d3326356460285e29d6b706e95b571d/src/react/createConnectedStore.tsx) — File read.
- [test/test.ts](https://github.com/bcherny/undux/blob/687a4f0f0d3326356460285e29d6b706e95b571d/test/test.ts) — File read.
- [test/bad-cases/run.sh](https://github.com/bcherny/undux/blob/687a4f0f0d3326356460285e29d6b706e95b571d/test/bad-cases/run.sh) — File read.
- [.github/workflows/ci.yml](https://github.com/bcherny/undux/blob/687a4f0f0d3326356460285e29d6b706e95b571d/.github/workflows/ci.yml) — File read.
- [package.json](https://github.com/bcherny/undux/blob/687a4f0f0d3326356460285e29d6b706e95b571d/package.json) — Scripts, entrypoints and dependency metadata.
- [test/immutable.tsx](https://github.com/bcherny/undux/blob/687a4f0f0d3326356460285e29d6b706e95b571d/test/immutable.tsx) — File read.
- [test/react/createConnectedStore-context.tsx](https://github.com/bcherny/undux/blob/687a4f0f0d3326356460285e29d6b706e95b571d/test/react/createConnectedStore-context.tsx) — File read.
- [perf/memory/README.md](https://github.com/bcherny/undux/blob/687a4f0f0d3326356460285e29d6b706e95b571d/perf/memory/README.md) — File read.

### typed-rx-emitter

Default-branch head: `4ce8dd6caf09b2ea392e15fe5d847d36c5da4111`. 

- Emitter<K> connects channel names to message value types; optional development mode supplies runtime cycle diagnostics.
- Tests include event delivery, emission before subscription, listener disposal, sequential subscribe/unsubscribe and cycle/noncycle cases.
- Cycle detection is disabled by default and is a local diagnostic, not security enforcement. Tests mix observable behavior with some internal-map assertions.

Template implication: For hooks, test both matching/nonmatching events, repeat invocation and cleanup; enable relevant diagnostics explicitly with clear cost/behavior.

Do not carry forward: Do not infer that every available diagnostic or agent is always executed; avoid importing the old Node/CircleCI/TSLint stack.

Inspected files:

- [index.ts](https://github.com/bcherny/typed-rx-emitter/blob/4ce8dd6caf09b2ea392e15fe5d847d36c5da4111/index.ts) — File read.
- [test.ts](https://github.com/bcherny/typed-rx-emitter/blob/4ce8dd6caf09b2ea392e15fe5d847d36c5da4111/test.ts) — File read.
- [.circleci/config.yml](https://github.com/bcherny/typed-rx-emitter/blob/4ce8dd6caf09b2ea392e15fe5d847d36c5da4111/.circleci/config.yml) — File read.
- [tsconfig.json](https://github.com/bcherny/typed-rx-emitter/blob/4ce8dd6caf09b2ea392e15fe5d847d36c5da4111/tsconfig.json) — File read.

### tsoption

Default-branch head: `78eb71faf3ba34efbe01a82e0f2271aa9dd43fa3`. 

- Option/Some/None make missing data and fallback paths explicit in public types.
- Tests specifically distinguish null/undefined from 0, false and empty string, and cover a NaN fallback policy.
- Behavioral algebra laws are tested alongside concrete examples; these are deterministic examples rather than an exhaustive proof.

Template implication: Test default handling using absent, null, empty and false values so hook/config flags do not collapse distinct meanings.

Do not carry forward: No requirement to introduce an Option dependency or functional-programming vocabulary into every project.

Inspected files:

- [index.ts](https://github.com/bcherny/tsoption/blob/78eb71faf3ba34efbe01a82e0f2271aa9dd43fa3/index.ts) — File read.
- [test.ts](https://github.com/bcherny/tsoption/blob/78eb71faf3ba34efbe01a82e0f2271aa9dd43fa3/test.ts) — File read.
- [package.json](https://github.com/bcherny/tsoption/blob/78eb71faf3ba34efbe01a82e0f2271aa9dd43fa3/package.json) — File read.

### create-typescript-app

Default-branch head: `8518112cb82390de960cde9610d18d04017ded18`. 

- Generator substitutes project identity from existing npm/git configuration into a template and then attempts dependency installation.
- The command helper catches failures and returns an empty string; therefore the outer yarn-to-npm catch cannot observe a failed yarn install. This is a static inference from the code, not an executed reproduction.
- The root README, src/cli.ts and test/test.ts are blank. Template compiler strictness and named test scripts do not establish a tested initializer.

Template implication: Keep initialization reviewable, propagate command failures, test failure paths and verify generated content, including no-op and overwrite behavior.

Do not carry forward: Do not copy silent failures, automatic package installation, global-configuration requirements or blank tests as production defaults.

Inspected files:

- [src/index.ts](https://github.com/bcherny/create-typescript-app/blob/8518112cb82390de960cde9610d18d04017ded18/src/index.ts) — File read.
- [src/cli.ts](https://github.com/bcherny/create-typescript-app/blob/8518112cb82390de960cde9610d18d04017ded18/src/cli.ts) — File read.
- [test/test.ts](https://github.com/bcherny/create-typescript-app/blob/8518112cb82390de960cde9610d18d04017ded18/test/test.ts) — File read.
- [template/package.json](https://github.com/bcherny/create-typescript-app/blob/8518112cb82390de960cde9610d18d04017ded18/template/package.json) — File read.
- [template/tsconfig.json](https://github.com/bcherny/create-typescript-app/blob/8518112cb82390de960cde9610d18d04017ded18/template/tsconfig.json) — File read.

### mcp-ping

Default-branch head: `a8b739b7d590d5f089d8258cd1bf5b6972e08ce6`. 

- Small stdio server explicitly registers its tool and resource capabilities and rejects unknown tool/resource names.
- The declared ping input is required, but the handler does not inspect it; the result uses content: [] with an extra toolResult field.
- Manifest provides a build command and strict compiler configuration; the root tree contains no tests.

Template implication: Use a minimal host smoke probe to distinguish discovery from invocation, and validate real request/response behavior against current host documentation.

Do not carry forward: Do not treat this historical sample as a current MCP conformance reference or preinstall the server for every template consumer.

Inspected files:

- [index.ts](https://github.com/bcherny/mcp-ping/blob/a8b739b7d590d5f089d8258cd1bf5b6972e08ce6/index.ts) — File read.
- [package.json](https://github.com/bcherny/mcp-ping/blob/a8b739b7d590d5f089d8258cd1bf5b6972e08ce6/package.json) — File read.
- [tsconfig.json](https://github.com/bcherny/mcp-ping/blob/a8b739b7d590d5f089d8258cd1bf5b6972e08ce6/tsconfig.json) — Active compiler settings.

### sandbox-runtime

Default-branch head: `be72efd3352dc76c36a46d382132f90759e8fd16`. Fork of anthropics/sandbox-runtime; upstream authorship applies. 

- This is a fork of anthropics/sandbox-runtime, with upstream authorship/license retained.
- Pre-commit runs lint-staged for TypeScript formatting/linting. Runtime configuration is separately parsed with Zod and reports field-specific failures.
- Filesystem read/write and network defaults have different semantics, explicitly documented in internal interfaces. Selected Linux code adds mandatory deny paths with worktree/symlink handling.
- Selected tests assert both failing exit status and unchanged protected file contents; configuration tests reject invalid domains, paths and incompatible options. Cross-platform CI is visible; none was executed here.

Template implication: Separate fast local feedback, schema checks, behavioral checks and host/OS permissions. Test that rejected hook/config operations leave state unchanged.

Do not carry forward: Do not label a Git/agent hook a sandbox. Do not carry over filesystem-disabled, weaker-isolation, privileged runner or system-setting changes as template defaults.

Inspected files:

- [.husky/pre-commit](https://github.com/bcherny/sandbox-runtime/blob/be72efd3352dc76c36a46d382132f90759e8fd16/.husky/pre-commit) — File read.
- [package.json](https://github.com/bcherny/sandbox-runtime/blob/be72efd3352dc76c36a46d382132f90759e8fd16/package.json) — File read.
- [src/sandbox/sandbox-schemas.ts](https://github.com/bcherny/sandbox-runtime/blob/be72efd3352dc76c36a46d382132f90759e8fd16/src/sandbox/sandbox-schemas.ts) — File read.
- [src/utils/config-loader.ts](https://github.com/bcherny/sandbox-runtime/blob/be72efd3352dc76c36a46d382132f90759e8fd16/src/utils/config-loader.ts) — File read.
- [test/config-validation.test.ts](https://github.com/bcherny/sandbox-runtime/blob/be72efd3352dc76c36a46d382132f90759e8fd16/test/config-validation.test.ts) — Selected relevant sections and test descriptions.
- [test/sandbox/mandatory-deny-paths.test.ts](https://github.com/bcherny/sandbox-runtime/blob/be72efd3352dc76c36a46d382132f90759e8fd16/test/sandbox/mandatory-deny-paths.test.ts) — Selected relevant sections and test descriptions.
- [.github/workflows/integration-tests.yml](https://github.com/bcherny/sandbox-runtime/blob/be72efd3352dc76c36a46d382132f90759e8fd16/.github/workflows/integration-tests.yml) — File read.
- [src/sandbox/sandbox-config.ts](https://github.com/bcherny/sandbox-runtime/blob/be72efd3352dc76c36a46d382132f90759e8fd16/src/sandbox/sandbox-config.ts) — Selected relevant sections and test descriptions.
- [src/sandbox/linux-sandbox-utils.ts](https://github.com/bcherny/sandbox-runtime/blob/be72efd3352dc76c36a46d382132f90759e8fd16/src/sandbox/linux-sandbox-utils.ts) — Selected relevant sections and test descriptions.

## Specific caution when adapting source examples

The `json-schema-to-typescript` aggregate check declares five prerequisite jobs but only tests three job results. The `undux` workflow declares an OS matrix but fixes its runner to Ubuntu. `create-typescript-app` catches command failures internally, so its surrounding fallback cannot detect a failed install, and its inspected test file is empty. These are static readings, not executed bug reproductions. They are reasons to retain the intent and verify our own implementation, rather than treating popular repositories as automatically correct.

Do not add historical TSLint/Grunt/CircleCI stacks, a mandatory React/RxJS/Option architecture, automatic dependency installation, always-running external agents, account-specific publishing secrets, or weaker sandbox/host settings to a neutral template just because an example contains them. Existing template commands and explicit host documentation remain the implementation authority.

## Complete repository inventory

Descriptions, fork parents, archive flags, file provenance and SHA fields are in `bcherny.json`. The repository links below lead to the primary repository; “overview” links lead to the exact inspected README or alternative primary file where one exists.

| Repository | Fork | Archived | Coverage | Observation |
| --- | --- | --- | --- | --- |
| [-dev-null](https://github.com/bcherny/-dev-null) | No | No | overview-read | Lists separate frontend build/watch and backend start commands. [Overview](https://github.com/bcherny/-dev-null/blob/master/README.md). |
| [100-exercises-to-learn-rust](https://github.com/bcherny/100-exercises-to-learn-rust) | Yes: mainmatter/100-exercises-to-learn-rust | No | overview-read | Upstream training material uses incremental exercises and lists tool prerequisites; not authored here merely because it is forked. [Overview](https://github.com/bcherny/100-exercises-to-learn-rust/blob/main/README.md). |
| [angular-butter-scroll](https://github.com/bcherny/angular-butter-scroll) | No | No | overview-read | Explains a rendering-cost hypothesis and pointer-event suppression; effect on interaction must be evaluated per app. [Overview](https://github.com/bcherny/angular-butter-scroll/blob/master/README.md). |
| [angular-commonjs](https://github.com/bcherny/angular-commonjs) | No | No | overview-read | Exploration starts from concrete dependency-availability and discoverability problems in Angular's injector. [Overview](https://github.com/bcherny/angular-commonjs/blob/master/README.md). |
| [angular-lock-column-widths](https://github.com/bcherny/angular-lock-column-widths) | No | No | overview-read | Provides explicit lock/unlock operations plus separate build, watch and test commands. [Overview](https://github.com/bcherny/angular-lock-column-widths/blob/master/README.md). |
| [angular-scroll-table](https://github.com/bcherny/angular-scroll-table) | No | No | overview-read | Documents the wrapper/scrolling mechanism and a runnable browser demonstration. [Overview](https://github.com/bcherny/angular-scroll-table/blob/master/README.md). |
| [angular-search](https://github.com/bcherny/angular-search) | No | No | overview-read | Documents mouse and keyboard equivalents for search/clear; claimed coverage was not run. [Overview](https://github.com/bcherny/angular-search/blob/master/README.md). |
| [angular-sticky-table-header](https://github.com/bcherny/angular-sticky-table-header) | No | No | overview-read | Explains the concrete clone/measure/reposition algorithm behind sticky headers. [Overview](https://github.com/bcherny/angular-sticky-table-header/blob/master/README.md). |
| [angular-tab-when-full](https://github.com/bcherny/angular-tab-when-full) | No | No | empty-metadata-only | API-confirmed empty repository; metadata-only coverage, no README or code available. |
| [angular-twerk](https://github.com/bcherny/angular-twerk) | No | No | primary-file-read | Blank README; Bower manifest declares a web-worker request experiment with Angular mocks as a development dependency. [Overview](https://github.com/bcherny/angular-twerk/blob/master/bower.json). |
| [angular.js](https://github.com/bcherny/angular.js) | Yes: angular/angular.js | No | overview-read | Historical framework overview links testability to dependency injection and model/view boundaries. [Overview](https://github.com/bcherny/angular.js/blob/master/README.md). |
| [angular2react](https://github.com/bcherny/angular2react) | Yes: coatue-oss/angular2react | No | overview-read | Fork explains an adapter boundary and the need to capture Angular's injector. [Overview](https://github.com/bcherny/angular2react/blob/master/README.md). |
| [angular2react-demos](https://github.com/bcherny/angular2react-demos) | No | No | overview-read | Links small nested-component integration examples across two UI frameworks. [Overview](https://github.com/bcherny/angular2react-demos/blob/master/README.md). |
| [angularjs-ordinal-filter](https://github.com/bcherny/angularjs-ordinal-filter) | Yes: jdpedrie/angularjs-ordinal-filter | No | overview-read | Fork demonstrates ordinal formatting and credits its source snippet. [Overview](https://github.com/bcherny/angularjs-ordinal-filter/blob/master/README.md). |
| [annie](https://github.com/bcherny/annie) | No | No | overview-read | Makes browser feature-detection results visible through a documented object shape. [Overview](https://github.com/bcherny/annie/blob/master/README.md). |
| [anthropic-sdk-typescript](https://github.com/bcherny/anthropic-sdk-typescript) | Yes: anthropics/anthropic-sdk-typescript | No | overview-read | Fork overview uses server-side API access and environment-variable credentials; example model names are historical. [Overview](https://github.com/bcherny/anthropic-sdk-typescript/blob/main/README.md). |
| [anthropic-stream-repro](https://github.com/bcherny/anthropic-stream-repro) | No | No | overview-read | Excellent small bug report: event ordering, expected exactly-once content, and visible duplicate-output symptoms. [Overview](https://github.com/bcherny/anthropic-stream-repro/blob/main/README.md). |
| [antiscroll](https://github.com/bcherny/antiscroll) | Yes: Automattic/antiscroll | No | overview-read | Fork documents preserving native scrolling while making wrapper requirements explicit. [Overview](https://github.com/bcherny/antiscroll/blob/master/README.md). |
| [arrange.love](https://github.com/bcherny/arrange.love) | No | No | primary-file-read | No README; simple HTML landing page posts an email field to an external subscription service; no submission performed. [Overview](https://github.com/bcherny/arrange.love/blob/master/index.html). |
| [asciidoctor-vscode](https://github.com/bcherny/asciidoctor-vscode) | Yes: asciidoctor/asciidoctor-vscode | No | overview-read | Fork overview describes an alpha automatic AsciiDoc preview extension. [Overview](https://github.com/bcherny/asciidoctor-vscode/blob/master/README.md). |
| [attack](https://github.com/bcherny/attack) | No | No | overview-read | CLI overview describes ramped load testing; no network load test was executed. [Overview](https://github.com/bcherny/attack/blob/master/README.md). |
| [auditable](https://github.com/bcherny/auditable) | No | No | overview-read | Demonstrates change history with timestamps and call traces for a list abstraction. [Overview](https://github.com/bcherny/auditable/blob/master/README.md). |
| [augment-module-repro-47215151](https://github.com/bcherny/augment-module-repro-47215151) | No | No | empty-metadata-only | API-confirmed empty repository; metadata-only coverage, no README or code available. |
| [automata](https://github.com/bcherny/automata) | No | No | overview-read | README identifies exploratory cellular-automata work without claims of a reusable production framework. [Overview](https://github.com/bcherny/automata/blob/master/README.md). |
| [autoNumeric](https://github.com/bcherny/autoNumeric) | Yes: autoNumeric/autoNumeric | No | overview-read | Historical fork documents configurable regional formats and dynamic updates, not current financial guidance. [Overview](https://github.com/bcherny/autoNumeric/blob/master/readme.md). |
| [autotype](https://github.com/bcherny/autotype) | No | No | overview-read | Misspelled overview file contains only a future-work placeholder; no implemented capability inferred. [Overview](https://github.com/bcherny/autotype/blob/master/REAMDE.md). |
| [autoversion](https://github.com/bcherny/autoversion) | No | No | empty-metadata-only | API-confirmed empty repository; metadata-only coverage, no README or code available. |
| [awesome-guide-to-protractor-testing](https://github.com/bcherny/awesome-guide-to-protractor-testing) | No | No | overview-read | Historical testing notes advocate page objects and test-local state; CoffeeScript and Protractor choices are context-specific. [Overview](https://github.com/bcherny/awesome-guide-to-protractor-testing/blob/master/README.md). |
| [awesome-interview-questions](https://github.com/bcherny/awesome-interview-questions) | Yes: DopplerHQ/awesome-interview-questions | No | overview-read | Forked resource index points contributors to contribution rules; it is curated links, not implementation evidence. [Overview](https://github.com/bcherny/awesome-interview-questions/blob/master/README.md). |
| [awesome-people-finder](https://github.com/bcherny/awesome-people-finder) | No | No | overview-read | Minimal overview shows an environment-provided GitHub token and a Haskell entrypoint; no account lookup executed. [Overview](https://github.com/bcherny/awesome-people-finder/blob/master/README.md). |
| [awesome-speakers](https://github.com/bcherny/awesome-speakers) | Yes: karlhorky/awesome-speakers | No | overview-read | Forked community directory organizes speakers by location and topic. [Overview](https://github.com/bcherny/awesome-speakers/blob/master/README.md). |
| [babel](https://github.com/bcherny/babel) | Yes: babel/babel | No | overview-read | Fork illustrates compiler input/output and the role of supported runtime environments. [Overview](https://github.com/bcherny/babel/blob/master/README.md). |
| [bar](https://github.com/bcherny/bar) | No | No | overview-read | README explicitly says the chart implementation is not functional yet. [Overview](https://github.com/bcherny/bar/blob/master/README.md). |
| [bcherny.github.io](https://github.com/bcherny/bcherny.github.io) | No | No | primary-file-read | No README; primary About page identifies the author's blog and links Claude Code and the TypeScript book. [Overview](https://github.com/bcherny/bcherny.github.io/blob/main/about.md). |
| [better-asciidoctor-vscode](https://github.com/bcherny/better-asciidoctor-vscode) | No | No | overview-read | Alpha extension documents file-triggered preview behavior and its upstream inspiration. [Overview](https://github.com/bcherny/better-asciidoctor-vscode/blob/master/README.md). |
| [better-autocomplete](https://github.com/bcherny/better-autocomplete) | No | No | overview-read | Work-in-progress component lists keyboard navigation and local/remote data support. [Overview](https://github.com/bcherny/better-autocomplete/blob/master/README.md). |
| [bigo](https://github.com/bcherny/bigo) | No | No | overview-read | README is only a future-work placeholder; no runtime-analysis capability inferred. [Overview](https://github.com/bcherny/bigo/blob/master/README.md). |
| [bigo_gym](https://github.com/bcherny/bigo_gym) | No | No | overview-read | Work-in-progress README asks about measured algorithm runtime; no results provided. [Overview](https://github.com/bcherny/bigo_gym/blob/master/README.md). |
| [bo](https://github.com/bcherny/bo) | No | No | overview-read | Small mobile UI framework documents pane/trigger attributes; claimed test coverage was not run. [Overview](https://github.com/bcherny/bo/blob/master/README.md). |
| [bowser](https://github.com/bcherny/bowser) | Yes: bowser-js/bowser | No | overview-read | Fork motivates browser detection as a fallback when feature detection is insufficient. [Overview](https://github.com/bcherny/bowser/blob/master/README.md). |
| [browser-activity-monitor](https://github.com/bcherny/browser-activity-monitor) | Yes: coatue-oss/browser-activity-monitor | No | overview-read | Fork usage includes explicit destroy cleanup after registering activity listeners. [Overview](https://github.com/bcherny/browser-activity-monitor/blob/master/README.md). |
| [browser-profiler](https://github.com/bcherny/browser-profiler) | No | No | overview-read | Documents repeated timings, raw results and environmental controls for more reliable measurements. [Overview](https://github.com/bcherny/browser-profiler/blob/master/README.md). |
| [bst-next](https://github.com/bcherny/bst-next) | No | No | overview-read | README contains only the repository heading; metadata identifies the binary-tree successor problem. [Overview](https://github.com/bcherny/bst-next/blob/master/README.md). |
| [bun](https://github.com/bcherny/bun) | Yes: oven-sh/bun | No | overview-read | Fork overview describes an integrated runtime/test/package toolchain; no reason to impose that stack universally. [Overview](https://github.com/bcherny/bun/blob/main/README.md). |
| [Chart](https://github.com/bcherny/Chart) | No | No | overview-read | Pre-alpha README leaves cross-browser tests and benchmarks as future work; do not treat them as proven. [Overview](https://github.com/bcherny/Chart/blob/master/readme.md). |
| [Chart.PieceLabel.js](https://github.com/bcherny/Chart.PieceLabel.js) | Yes: emn178/chartjs-plugin-labels | No | overview-read | Fork prominently links breaking/deprecated option changes to changelog entries. [Overview](https://github.com/bcherny/Chart.PieceLabel.js/blob/master/README.md). |
| [chartjs-plugin-stacked100](https://github.com/bcherny/chartjs-plugin-stacked100) | Yes: y-takey/chartjs-plugin-stacked100 | No | overview-read | Fork requires explicit plugin enablement and shows a concrete chart configuration. [Overview](https://github.com/bcherny/chartjs-plugin-stacked100/blob/master/README.md). |
| [chromium-658894-repro](https://github.com/bcherny/chromium-658894-repro) | No | No | primary-file-read | No README; HTML is a small nested-layout/loader reproduction using a separate CSS file. [Overview](https://github.com/bcherny/chromium-658894-repro/blob/master/index.htm). |
| [clever-demo](https://github.com/bcherny/clever-demo) | No | No | overview-read | Lists statistical operations and explicitly identifies missing isolation between unit and integration tests. [Overview](https://github.com/bcherny/clever-demo/blob/master/README.md). |
| [clever-js](https://github.com/bcherny/clever-js) | Yes: Clever/clever-js | No | overview-read | Fork maps API resources into a documented query interface with result-type expectations. [Overview](https://github.com/bcherny/clever-js/blob/master/README.md). |
| [co](https://github.com/bcherny/co) | Yes: tj/co | No | overview-read | Historical fork explicitly documents a callback-to-promise API transition. [Overview](https://github.com/bcherny/co/blob/master/Readme.md). |
| [codenam.es](https://github.com/bcherny/codenam.es) | No | No | overview-read | Documents development/production commands and marks API routes implemented versus planned. [Overview](https://github.com/bcherny/codenam.es/blob/master/README.md). |
| [coffeescript](https://github.com/bcherny/coffeescript) | Yes: jashkenas/coffeescript | No | overview-read | Compiler repository overview reviewed; no agent workflow established from this historical fork. [Overview](https://github.com/bcherny/coffeescript/blob/master/README.md). |
| [colony](https://github.com/bcherny/colony) | Yes: hughsk/colony | No | overview-read | Fork visualizes code dependencies with explicit traversal and output-directory options. [Overview](https://github.com/bcherny/colony/blob/master/README.md). |
| [color-dungeon-solver](https://github.com/bcherny/color-dungeon-solver) | No | No | overview-read | Defines puzzle state and legal transitions before presenting a solver. [Overview](https://github.com/bcherny/color-dungeon-solver/blob/master/README.md). |
| [colour-schemes](https://github.com/bcherny/colour-schemes) | Yes: daylerees/colour-schemes | No | overview-read | Fork README is editor-theme installation guidance, not engineering workflow evidence. [Overview](https://github.com/bcherny/colour-schemes/blob/master/README.md). |
| [concat-maps](https://github.com/bcherny/concat-maps) | No | No | overview-read | Shows the result of merging two maps and a test entrypoint. [Overview](https://github.com/bcherny/concat-maps/blob/master/README.md). |
| [content-type-ext](https://github.com/bcherny/content-type-ext) | Yes: beeant/content-type-ext | No | overview-read | Fork demonstrates MIME/extension mapping within an HTTP-response example. [Overview](https://github.com/bcherny/content-type-ext/blob/master/README.md). |
| [content-type-to-ext](https://github.com/bcherny/content-type-to-ext) | No | No | overview-read | Documents a small bidirectional mapping API with example results. [Overview](https://github.com/bcherny/content-type-to-ext/blob/master/README.md). |
| [contributor.io](https://github.com/bcherny/contributor.io) | No | No | overview-read | Separates API consumption, local server use and optional environment-based authentication. [Overview](https://github.com/bcherny/contributor.io/blob/master/README.md). |
| [coursera_chrome_extension_migrations](https://github.com/bcherny/coursera_chrome_extension_migrations) | Yes: awessels/coursera_chrome_extension_migrations | No | overview-read | Fork documents UI mutation behavior and precise supported/unsupported timestamp formats. [Overview](https://github.com/bcherny/coursera_chrome_extension_migrations/blob/master/README.md). |
| [cpan-count](https://github.com/bcherny/cpan-count) | Yes: fayland/cpan-count | No | overview-read | Fork credits reused counting code and documents success/error callbacks. [Overview](https://github.com/bcherny/cpan-count/blob/master/README.md). |
| [crdt-demo](https://github.com/bcherny/crdt-demo) | No | No | overview-read | Worked state example links the underlying paper and exposes identifiers, neighbors and visibility markers. [Overview](https://github.com/bcherny/crdt-demo/blob/master/README.md). |
| [create-typescript-app](https://github.com/bcherny/create-typescript-app) | No | No | deep-sampled | Blank README; package manifest wires build before tests/publish and exposes a generator CLI; deep inspection follows. [Overview](https://github.com/bcherny/create-typescript-app/blob/master/package.json). |
| [css-to-matrix](https://github.com/bcherny/css-to-matrix) | No | No | overview-read | Provides conversion examples at the CSS-transform/matrix boundary. [Overview](https://github.com/bcherny/css-to-matrix/blob/master/README.md). |
| [css3FontConverter](https://github.com/bcherny/css3FontConverter) | Yes: zoltan-dulac/css3FontConverter | No | overview-read | Fork describes generated font formats/stylesheets and operating-system assumptions. [Overview](https://github.com/bcherny/css3FontConverter/blob/master/readme.txt). |
| [CT4S](https://github.com/bcherny/CT4S) | No | No | overview-read | Glossary maps mathematical notation to definitions, useful as a documentation example rather than software configuration. [Overview](https://github.com/bcherny/CT4S/blob/master/README.md). |
| [cufon](https://github.com/bcherny/cufon) | Yes: sorccu/cufon | No | primary-file-read | No README; one primary documentation page generates a font-scaling comparison chart; renderer not audited. [Overview](https://github.com/bcherny/cufon/blob/master/doc/optimal-scaling.html). |
| [curl](https://github.com/bcherny/curl) | Yes: cujojs/curl | No | overview-read | Fork README distinguishes the resource loader from the unrelated curl CLI and records repository relocation. [Overview](https://github.com/bcherny/curl/blob/master/README.md). |
| [david-issue-repro](https://github.com/bcherny/david-issue-repro) | No | No | overview-read | README provides a minimal compiler reproduction command without a claimed resolution. [Overview](https://github.com/bcherny/david-issue-repro/blob/master/README.md). |
| [DefinitelyTyped](https://github.com/bcherny/DefinitelyTyped) | Yes: DefinitelyTyped/DefinitelyTyped | No | overview-read | Fork documents declaration discovery and distinguishes bundled types from separate @types packages. [Overview](https://github.com/bcherny/DefinitelyTyped/blob/master/README.md). |
| [dimple](https://github.com/bcherny/dimple) | Yes: PMSI-AlignAlytics/dimple | No | overview-read | Fork provides a simpler charting API while retaining access to underlying d3 objects for extension. [Overview](https://github.com/bcherny/dimple/blob/master/README.md). |
| [distance-benchmarks](https://github.com/bcherny/distance-benchmarks) | No | No | overview-read | Names comparison methods, a concrete rental dataset and a separate analysis report. [Overview](https://github.com/bcherny/distance-benchmarks/blob/master/README.md). |
| [draggable](https://github.com/bcherny/draggable) | No | No | overview-read | Documents a small constructor/options boundary, browser-global and module usage, and dependency-free scope. [Overview](https://github.com/bcherny/draggable/blob/master/README.md). |
| [draggable.js](https://github.com/bcherny/draggable.js) | Yes: gtramontina/draggable.js | No | overview-read | Fork explicitly requires raw DOM elements and documents optional drag handles. [Overview](https://github.com/bcherny/draggable.js/blob/master/README.md). |
| [electron-quick-start](https://github.com/bcherny/electron-quick-start) | Yes: electron/minimal-repro | No | overview-read | Fork explains the responsibilities of a minimal app's three entry files. [Overview](https://github.com/bcherny/electron-quick-start/blob/master/README.md). |
| [enumerate](https://github.com/bcherny/enumerate) | Yes: albertywu/enumerate | No | overview-read | Fork provides a typed signature and examples for cutoff/placeholder behavior. [Overview](https://github.com/bcherny/enumerate/blob/master/README.md). |
| [es-module-stats](https://github.com/bcherny/es-module-stats) | No | No | overview-read | Documents sampling and multiple definitions of adoption; historical percentages are not current ecosystem facts. [Overview](https://github.com/bcherny/es-module-stats/blob/main/README.md). |
| [es6-promise-pool](https://github.com/bcherny/es6-promise-pool) | Yes: timdp/es6-promise-pool | No | overview-read | Fork explains bounded concurrency with just-in-time promise production rather than starting every operation at once. [Overview](https://github.com/bcherny/es6-promise-pool/blob/master/README.md). |
| [eslint-plugin-flowtype](https://github.com/bcherny/eslint-plugin-flowtype) | Yes: gajus/eslint-plugin-flowtype | No | overview-read | Fork provides a rule catalog and configuration structure; a catalog is not evidence that every rule fits this template. [Overview](https://github.com/bcherny/eslint-plugin-flowtype/blob/master/README.md). |
| [eslint-plugin-react](https://github.com/bcherny/eslint-plugin-react) | Yes: jsx-eslint/eslint-plugin-react | No | overview-read | Fork documents local dev installation and a recommended rule preset. [Overview](https://github.com/bcherny/eslint-plugin-react/blob/master/README.md). |
| [eslint-plugin-relay](https://github.com/bcherny/eslint-plugin-relay) | Yes: relayjs/eslint-plugin-relay | No | overview-read | Fork describes early static feedback and selectable recommended versus strict rule presets. [Overview](https://github.com/bcherny/eslint-plugin-relay/blob/master/README.md). |
| [esri-extent](https://github.com/bcherny/esri-extent) | Yes: GeoXForm/esri-extent | No | overview-read | Fork demonstrates a GeoJSON-to-extent contract, including spatial-reference metadata and callback failure handling. [Overview](https://github.com/bcherny/esri-extent/blob/master/README.md). |
| [excalidraw](https://github.com/bcherny/excalidraw) | Yes: excalidraw/excalidraw | No | overview-read | Fork overview exposes an embeddable editor and an open drawing format with export capabilities. [Overview](https://github.com/bcherny/excalidraw/blob/master/README.md). |
| [fantasy-land](https://github.com/bcherny/fantasy-land) | Yes: fantasyland/fantasy-land | No | overview-read | Fork specifies interoperable algebraic structures through explicit laws and terminology. [Overview](https://github.com/bcherny/fantasy-land/blob/master/README.md). |
| [fibonacci](https://github.com/bcherny/fibonacci) | No | No | overview-read | Visual recursion demo explicitly limits itself to WebKit. [Overview](https://github.com/bcherny/fibonacci/blob/master/readme.md). |
| [firegrid](https://github.com/bcherny/firegrid) | No | No | overview-read | Work-in-progress goals tie viewport work to instrumentation; scale/coverage goals are not demonstrated guarantees. [Overview](https://github.com/bcherny/firegrid/blob/master/README.md). |
| [Flashcards](https://github.com/bcherny/Flashcards) | No | No | primary-file-read | No README; private package manifest orchestrates client/server development in parallel. [Overview](https://github.com/bcherny/Flashcards/blob/main/package.json). |
| [flow-to-typescript](https://github.com/bcherny/flow-to-typescript) | No | No | overview-read | Pre-alpha converter exposes both CLI and asynchronous compile API and distinguishes conversion support. [Overview](https://github.com/bcherny/flow-to-typescript/blob/master/README.md). |
| [fold-array](https://github.com/bcherny/fold-array) | No | No | primary-file-read | No README; source includes input/output examples but its assertion helper only logs failure instead of failing the process. [Overview](https://github.com/bcherny/fold-array/blob/master/fold.js). |
| [foogle](https://github.com/bcherny/foogle) | No | No | empty-metadata-only | API-confirmed empty repository; metadata-only coverage, no README or code available. |
| [format-as-currency](https://github.com/bcherny/format-as-currency) | No | No | overview-read | Angular formatting directive illustrates extension through custom currency formatters. [Overview](https://github.com/bcherny/format-as-currency/blob/master/README.md). |
| [fps-profiler](https://github.com/bcherny/fps-profiler) | No | No | overview-read | Measures an operation repeatedly and reports mean, variability and raw samples instead of only an FPS claim. [Overview](https://github.com/bcherny/fps-profiler/blob/master/README.md). |
| [FreeCodeCamp](https://github.com/bcherny/FreeCodeCamp) | Yes: freeCodeCamp/freeCodeCamp | No | overview-read | Historical fork overview describes a project-based curriculum; certification details are not current recommendations. [Overview](https://github.com/bcherny/FreeCodeCamp/blob/staging/README.md). |
| [frontend-interview-questions](https://github.com/bcherny/frontend-interview-questions) | No | No | overview-read | README is an answer collection with a link to the original questions, not a reusable application foundation. [Overview](https://github.com/bcherny/frontend-interview-questions/blob/master/README.md). |
| [fullcalendar](https://github.com/bcherny/fullcalendar) | Yes: fullcalendar/fullcalendar | No | overview-read | Fork routes users and contributors to distinct documentation, fixes and coding guidelines. [Overview](https://github.com/bcherny/fullcalendar/blob/master/readme.md). |
| [fx](https://github.com/bcherny/fx) | No | No | overview-read | Overview explains animation fallbacks for older browsers; its speed claims were not benchmarked here. [Overview](https://github.com/bcherny/fx/blob/master/readme.md). |
| [gdbgui](https://github.com/bcherny/gdbgui) | Yes: cs01/gdbgui | No | overview-read | Fork presents browser debugging over gdb; installation examples were only read, never executed. [Overview](https://github.com/bcherny/gdbgui/blob/master/README.md). |
| [gem-count](https://github.com/bcherny/gem-count) | No | No | overview-read | Small counting API documents success/error handling through promises. [Overview](https://github.com/bcherny/gem-count/blob/master/README.md). |
| [github-actions-badge](https://github.com/bcherny/github-actions-badge) | Yes: CultureHQ/github-actions-badge | No | overview-read | README marks the project deprecated in favor of GitHub's built-in badge; reject installing this legacy badge service. [Overview](https://github.com/bcherny/github-actions-badge/blob/master/README.md). |
| [github-repos](https://github.com/bcherny/github-repos) | No | No | overview-read | Counting wrapper explicitly supports pagination progress; its old OAuth interface is not a modern authentication recommendation. [Overview](https://github.com/bcherny/github-repos/blob/master/README.md). |
| [gmaps](https://github.com/bcherny/gmaps) | Yes: hpneo/gmaps | No | overview-read | Fork's changelog records error-callback and cleanup-related fixes at a map abstraction boundary. [Overview](https://github.com/bcherny/gmaps/blob/master/README.md). |
| [grunt-contrib-coffee](https://github.com/bcherny/grunt-contrib-coffee) | Yes: gruntjs/grunt-contrib-coffee | No | overview-read | Fork explicitly ties plugin behavior to supported Grunt versions and a named compile task. [Overview](https://github.com/bcherny/grunt-contrib-coffee/blob/master/README.md). |
| [grunt-umd](https://github.com/bcherny/grunt-umd) | Yes: bebraw/grunt-umd | No | overview-read | Fork exposes source/destination defaults; missing destination can overwrite source, so do not adopt blindly. [Overview](https://github.com/bcherny/grunt-umd/blob/master/README.md). |
| [gulp-coffee](https://github.com/bcherny/gulp-coffee) | Yes: gulp-community/gulp-coffee | No | overview-read | Fork documents compilation and sourcemap task ordering with an optional compiler override. [Overview](https://github.com/bcherny/gulp-coffee/blob/master/README.md). |
| [hack-langspec](https://github.com/bcherny/hack-langspec) | Yes: facebookarchive/hack-langspec | No | overview-read | Fork links executable specification checks and its contribution process; version claims are historical. [Overview](https://github.com/bcherny/hack-langspec/blob/master/README.md). |
| [highlight.js](https://github.com/bcherny/highlight.js) | Yes: highlightjs/highlight.js | No | overview-read | Fork separates automatic language detection from explicit language selection and opt-out. [Overview](https://github.com/bcherny/highlight.js/blob/master/README.md). |
| [homelessIBMCognitiveFair](https://github.com/bcherny/homelessIBMCognitiveFair) | Yes: gregorydillon/homelessIBMCognitiveFair | No | primary-file-read | No README; selected HTML source identifies a San Francisco 311 neighborhood visualization; notebook not audited. [Overview](https://github.com/bcherny/homelessIBMCognitiveFair/blob/master/index.html). |
| [immut](https://github.com/bcherny/immut) | No | No | overview-read | Demonstrates an apparently mutable list interface with immutable history and trace output. [Overview](https://github.com/bcherny/immut/blob/master/README.md). |
| [immutable-js](https://github.com/bcherny/immutable-js) | Yes: immutable-js/immutable-js | No | overview-read | Fork explains structural sharing and immutable updates behind persistent collection APIs. [Overview](https://github.com/bcherny/immutable-js/blob/master/README.md). |
| [india](https://github.com/bcherny/india) | No | No | overview-read | Proposes comparing exported interface documentation across commits to identify versioning changes. [Overview](https://github.com/bcherny/india/blob/master/README.md). |
| [infinite-scroll](https://github.com/bcherny/infinite-scroll) | No | No | overview-read | Requires a thenable callback and motivates the directive through scrolling responsiveness. [Overview](https://github.com/bcherny/infinite-scroll/blob/master/README.md). |
| [ink](https://github.com/bcherny/ink) | Yes: vadimdemedes/ink | No | overview-read | Fork distinguishes terminal rendering from web rendering while retaining React's component model. [Overview](https://github.com/bcherny/ink/blob/master/readme.md). |
| [ink-image](https://github.com/bcherny/ink-image) | Yes: kevva/ink-image | No | overview-read | Fork documents its terminal support limit and fallback alternative text. [Overview](https://github.com/bcherny/ink-image/blob/master/readme.md). |
| [ink-syntax-highlight](https://github.com/bcherny/ink-syntax-highlight) | Yes: vsashyn/ink-syntax-highlight | No | overview-read | Fork exposes code, language detection and theme as separate component props. [Overview](https://github.com/bcherny/ink-syntax-highlight/blob/master/readme.md). |
| [internet-speed](https://github.com/bcherny/internet-speed) | No | No | overview-read | Overview shows configuration and a start command; personal monitoring architecture and credential-file layout are context-specific. [Overview](https://github.com/bcherny/internet-speed/blob/master/README.md). |
| [isbn-cover](https://github.com/bcherny/isbn-cover) | No | No | overview-read | Documents differing browser-element versus Node-data results and explicit error callbacks. [Overview](https://github.com/bcherny/isbn-cover/blob/master/README.md). |
| [isbnjs](https://github.com/bcherny/isbnjs) | Yes: coolaj86/isbnjs | No | overview-read | Fork demonstrates ISBN parsing, validity checks, formatting and conversion with expected values. [Overview](https://github.com/bcherny/isbnjs/blob/gh-pages/README.md). |
| [iscroll](https://github.com/bcherny/iscroll) | Yes: cubiq/iscroll | No | overview-read | Historical fork targets old mobile WebKit scrolling limitations; not a modern default dependency. [Overview](https://github.com/bcherny/iscroll/blob/master/README.md). |
| [izzy](https://github.com/bcherny/izzy) | No | No | overview-read | Documents runtime type predicates and their motivation around false-positive detection. [Overview](https://github.com/bcherny/izzy/blob/master/README.md). |
| [izzy-typings](https://github.com/bcherny/izzy-typings) | No | No | overview-read | README identifies a separate declaration package for an existing runtime library. [Overview](https://github.com/bcherny/izzy-typings/blob/master/README.md). |
| [jasmine-leak-test](https://github.com/bcherny/jasmine-leak-test) | No | No | overview-read | Reproduction records exact browser/OS context and a command for observing memory growth. [Overview](https://github.com/bcherny/jasmine-leak-test/blob/master/README.md). |
| [javascript-interview](https://github.com/bcherny/javascript-interview) | Yes: jkup/javascript-interview | No | overview-read | Forked preparation-resource list invites contributions; no production workflow validated. [Overview](https://github.com/bcherny/javascript-interview/blob/master/README.md). |
| [jekyll](https://github.com/bcherny/jekyll) | Yes: jekyll/jekyll | No | overview-read | Fork overview describes a file-to-static-site pipeline and routes detailed work to documentation. [Overview](https://github.com/bcherny/jekyll/blob/master/README.markdown). |
| [jQuery-Mask-Plugin](https://github.com/bcherny/jQuery-Mask-Plugin) | Yes: igorescobar/jQuery-Mask-Plugin | No | overview-read | Fork feature overview includes dynamic fields, cleanup and configuration; masking is not server-side validation. [Overview](https://github.com/bcherny/jQuery-Mask-Plugin/blob/master/README.md). |
| [jquery.threedubmedia](https://github.com/bcherny/jquery.threedubmedia) | Yes: threedubmedia/jquery.threedubmedia | No | primary-file-read | No README; fork manifest repackages upstream plugins under a scoped package and leaves tests unimplemented. [Overview](https://github.com/bcherny/jquery.threedubmedia/blob/master/package.json). |
| [jquery.touchToClick](https://github.com/bcherny/jquery.touchToClick) | Yes: viglesias/jquery.touchToClick | No | overview-read | Historical mobile event workaround targets an old click-delay issue, not a universal modern default. [Overview](https://github.com/bcherny/jquery.touchToClick/blob/master/README.markdown). |
| [js-math](https://github.com/bcherny/js-math) | No | No | primary-file-read | No README; small source separates tokenizing, lexing, parsing and expression evaluation. [Overview](https://github.com/bcherny/js-math/blob/master/index.js). |
| [js-schema](https://github.com/bcherny/js-schema) | Yes: molnarg/js-schema | No | overview-read | Historical fork illustrates declarative object validation and JSON Schema serialization. [Overview](https://github.com/bcherny/js-schema/blob/master/README.md). |
| [json-schema-ref-parser](https://github.com/bcherny/json-schema-ref-parser) | Yes: APIDevTools/json-schema-ref-parser | No | overview-read | Fork README includes a maintainer warning and describes mixed local/remote reference resolution; fork state may lag upstream. [Overview](https://github.com/bcherny/json-schema-ref-parser/blob/master/README.md). |
| [json-schema-to-typescript](https://github.com/bcherny/json-schema-to-typescript) | No | No | deep-sampled | Shows schema input alongside generated declarations and documents unsupported semantics; deep inspection follows. [Overview](https://github.com/bcherny/json-schema-to-typescript/blob/master/README.md). |
| [json-schema-to-typescript-browser](https://github.com/bcherny/json-schema-to-typescript-browser) | No | No | overview-read | Small browser demo with an explicit local start command. [Overview](https://github.com/bcherny/json-schema-to-typescript-browser/blob/master/README.md). |
| [jumbo](https://github.com/bcherny/jumbo) | No | No | overview-read | README marks an experimental algorithm implementation as unfinished and links background material. [Overview](https://github.com/bcherny/jumbo/blob/master/README.md). |
| [language-types-comparison](https://github.com/bcherny/language-types-comparison) | No | No | overview-read | Diagram overview cites language specifications rather than presenting a new runtime. [Overview](https://github.com/bcherny/language-types-comparison/blob/master/README.md). |
| [lazy-arr](https://github.com/bcherny/lazy-arr) | No | No | overview-read | Makes lazy evaluation and caching behavior explicit, including non-idempotent generator implications. [Overview](https://github.com/bcherny/lazy-arr/blob/master/README.md). |
| [learner](https://github.com/bcherny/learner) | No | No | overview-read | Experimental training program shows intermediate learned state rather than only a final output. [Overview](https://github.com/bcherny/learner/blob/master/README.md). |
| [learning-scala](https://github.com/bcherny/learning-scala) | No | No | primary-file-read | No README; selected exercise uses an annotated recursive helper; this is one exercise sample, not verification of every answer. [Overview](https://github.com/bcherny/learning-scala/blob/master/02.01-fibonacci.scala). |
| [learning-scala-v2](https://github.com/bcherny/learning-scala-v2) | No | No | overview-read | Book exercise answers include a direct command to run a chapter's tests. [Overview](https://github.com/bcherny/learning-scala-v2/blob/master/README.md). |
| [lodash](https://github.com/bcherny/lodash) | Yes: lodash/lodash | No | overview-read | Historical fork explains core/full/functional builds and selecting the relevant footprint. [Overview](https://github.com/bcherny/lodash/blob/master/README.md). |
| [low](https://github.com/bcherny/low) | No | No | overview-read | Before/after example shows a syntactic convenience over ordinary map callbacks. [Overview](https://github.com/bcherny/low/blob/master/README.md). |
| [LygoEdit](https://github.com/bcherny/LygoEdit) | Yes: lahdekorpi/LygoEdit | No | overview-read | Fork overview describes a planned inline contentEditable editor with no implementation proof in the README. [Overview](https://github.com/bcherny/LygoEdit/blob/master/README.md). |
| [magic-babbler](https://github.com/bcherny/magic-babbler) | No | No | overview-read | Prototype searches type-compatible function compositions and scores syntactic simplicity. [Overview](https://github.com/bcherny/magic-babbler/blob/master/README.md). |
| [mapbox-gl-js](https://github.com/bcherny/mapbox-gl-js) | Yes: mapbox/mapbox-gl-js | No | overview-read | Fork distinguishes shared fixtures from platform-specific SDK code and links contributor guidance. [Overview](https://github.com/bcherny/mapbox-gl-js/blob/master/README.md). |
| [mapf](https://github.com/bcherny/mapf) | No | No | overview-read | Provides an ergonomic wrapper around Promise.all with a before/after rationale. [Overview](https://github.com/bcherny/mapf/blob/master/README.md). |
| [matrix-utilities](https://github.com/bcherny/matrix-utilities) | No | No | overview-read | Presents explicit matrix operations with expected numeric results; no tests executed. [Overview](https://github.com/bcherny/matrix-utilities/blob/master/README.md). |
| [mcp-ping](https://github.com/bcherny/mcp-ping) | No | No | deep-sampled | No README; TypeScript entrypoint registers one ping tool and one static resource; a minimal protocol smoke example, not a complete agent. [Overview](https://github.com/bcherny/mcp-ping/blob/main/index.ts). |
| [microbox](https://github.com/bcherny/microbox) | No | No | overview-read | Documents compatibility with an existing lightbox API and its own two dependencies. [Overview](https://github.com/bcherny/microbox/blob/master/README.md). |
| [microjs.com](https://github.com/bcherny/microjs.com) | Yes: microjs/microjs.com | No | overview-read | Fork argues for focused small libraries; its size thresholds are editorial preferences, not template requirements. [Overview](https://github.com/bcherny/microjs.com/blob/master/README.md). |
| [milk](https://github.com/bcherny/milk) | No | No | empty-metadata-only | API-confirmed empty repository; metadata-only coverage, no README or code available. |
| [mootools-more](https://github.com/bcherny/mootools-more) | Yes: mootools/mootools-more | No | overview-read | Historical fork lists resource cleanup methods as unfinished maintenance work. [Overview](https://github.com/bcherny/mootools-more/blob/master/README.md). |
| [Moya](https://github.com/bcherny/Moya) | Yes: Moya/Moya | No | overview-read | Fork motivates an explicit network boundary through maintainability and testability. [Overview](https://github.com/bcherny/Moya/blob/master/Readme.md). |
| [ngimport](https://github.com/bcherny/ngimport) | No | No | overview-read | Before/after examples show moving Angular service access behind ES module exports. [Overview](https://github.com/bcherny/ngimport/blob/master/README.md). |
| [ngimport-demo](https://github.com/bcherny/ngimport-demo) | No | No | overview-read | Separate build/serve/test commands make the integration demonstration reproducible in principle. [Overview](https://github.com/bcherny/ngimport-demo/blob/master/README.md). |
| [ngimport-ngresource](https://github.com/bcherny/ngimport-ngresource) | No | No | overview-read | Extends the service-import adapter specifically for ngResource and provides a test command. [Overview](https://github.com/bcherny/ngimport-ngresource/blob/master/README.md). |
| [ngReact](https://github.com/bcherny/ngReact) | Yes: ngReact/ngReact | No | overview-read | Fork overview explicitly recommends successor adapters rather than treating its own approach as the latest choice. [Overview](https://github.com/bcherny/ngReact/blob/master/README.md). |
| [nishikarch.github.io](https://github.com/bcherny/nishikarch.github.io) | Yes: nishikarch/nishikarch.github.io | No | overview-read | Forked reading-club website documents local Jekyll development. [Overview](https://github.com/bcherny/nishikarch.github.io/blob/main/README.md). |
| [node-fileset](https://github.com/bcherny/node-fileset) | Yes: mklabs/node-fileset | No | overview-read | Fork wrapper makes include/exclude glob semantics and callback/emitter usage explicit. [Overview](https://github.com/bcherny/node-fileset/blob/master/README.md). |
| [node-timezone](https://github.com/bcherny/node-timezone) | No | No | overview-read | Records tested operating systems and explicitly leaves Windows verification unresolved. [Overview](https://github.com/bcherny/node-timezone/blob/master/README.md). |
| [npm-packages](https://github.com/bcherny/npm-packages) | No | No | overview-read | Documents pagination progress and openly admits scraping cannot distinguish a missing user from an empty account. [Overview](https://github.com/bcherny/npm-packages/blob/master/README.md). |
| [npm-www](https://github.com/bcherny/npm-www) | Yes: visnup/npm-www | No | overview-read | Historical fork's development bootstrap describes database setup and insecure development defaults; reject copying this automatically. [Overview](https://github.com/bcherny/npm-www/blob/master/README.md). |
| [nuget-count](https://github.com/bcherny/nuget-count) | No | No | overview-read | README openly documents an ambiguity in scraped missing-user versus zero-package results. [Overview](https://github.com/bcherny/nuget-count/blob/master/README.md). |
| [objectid](https://github.com/bcherny/objectid) | Yes: junosuarez/objectid | No | overview-read | Fork documents validation, conversion behavior and version-specific browser/driver compatibility. [Overview](https://github.com/bcherny/objectid/blob/master/README.md). |
| [olga](https://github.com/bcherny/olga) | No | No | overview-read | Proposed UI-test annotation approach remains marked as coming soon; not a proven automation engine. [Overview](https://github.com/bcherny/olga/blob/master/README.md). |
| [omaps](https://github.com/bcherny/omaps) | No | No | primary-file-read | No README; package manifest identifies a Cordova-era dependency set and a deliberately unimplemented test command. [Overview](https://github.com/bcherny/omaps/blob/master/package.json). |
| [OpenAPI-Specification](https://github.com/bcherny/OpenAPI-Specification) | Yes: OAI/OpenAPI-Specification | No | overview-read | Historical fork frames machine-readable service contracts; its pre-release version pointers are not current standards guidance. [Overview](https://github.com/bcherny/OpenAPI-Specification/blob/master/README.md). |
| [openclaw](https://github.com/bcherny/openclaw) | Yes: openclaw/openclaw | No | overview-read | Fork overview describes a single-user assistant with many messaging integrations and a gateway; its always-on product scope is not a template default. [Overview](https://github.com/bcherny/openclaw/blob/main/README.md). |
| [package-maker](https://github.com/bcherny/package-maker) | No | No | overview-read | Experimental dependency generator distinguishes stdout from file redirection; generated dependencies still require review. [Overview](https://github.com/bcherny/package-maker/blob/master/README.md). |
| [penner](https://github.com/bcherny/penner) | No | No | overview-read | Documents the units and arguments of easing functions with a concrete invocation. [Overview](https://github.com/bcherny/penner/blob/master/README.md). |
| [people-chess](https://github.com/bcherny/people-chess) | No | No | primary-file-read | No README; manifest names a chess entrypoint but uses an unimplemented test command. [Overview](https://github.com/bcherny/people-chess/blob/master/package.json). |
| [perfci](https://github.com/bcherny/perfci) | No | No | overview-read | README describes a performance-CI idea only; no functioning CI behavior inferred. [Overview](https://github.com/bcherny/perfci/blob/master/README.md). |
| [preact](https://github.com/bcherny/preact) | Yes: preactjs/preact | No | overview-read | Historical fork positions a smaller compatible UI surface with an explicit compatibility layer. [Overview](https://github.com/bcherny/preact/blob/master/README.md). |
| [programming-typescript-answers](https://github.com/bcherny/programming-typescript-answers) | No | No | primary-file-read | No root README; package manifest exposes compiler, lint and formatting entrypoints for book exercises. [Overview](https://github.com/bcherny/programming-typescript-answers/blob/master/package.json). |
| [programmingtypescriptbook.com](https://github.com/bcherny/programmingtypescriptbook.com) | No | No | primary-file-read | No README; HTML primary page identifies the book and includes a responsive layout; only page source inspected. [Overview](https://github.com/bcherny/programmingtypescriptbook.com/blob/master/index.html). |
| [promise-polyfill](https://github.com/bcherny/promise-polyfill) | Yes: taylorhakes/promise-polyfill | No | overview-read | Fork distinguishes opt-in global polyfilling from importing a module without global changes. [Overview](https://github.com/bcherny/promise-polyfill/blob/master/README.md). |
| [promise-seq](https://github.com/bcherny/promise-seq) | No | No | overview-read | Accepts promise factories to control execution order and documents a watch-test command. [Overview](https://github.com/bcherny/promise-seq/blob/master/README.md). |
| [qtip](https://github.com/bcherny/qtip) | No | No | overview-read | Documents progressive use of title attributes and lists browser API prerequisites. [Overview](https://github.com/bcherny/qtip/blob/master/README.md). |
| [quiet-light-atom](https://github.com/bcherny/quiet-light-atom) | Yes: nelsonpecora/quiet-light-atom | No | overview-read | Fork is a theme conversion with source attribution, not workflow automation. [Overview](https://github.com/bcherny/quiet-light-atom/blob/master/README.md). |
| [react](https://github.com/bcherny/react) | Yes: react/react | No | overview-read | Fork overview explains encapsulated components and declarative state-driven UI. [Overview](https://github.com/bcherny/react/blob/master/README.md). |
| [react-month-picker](https://github.com/bcherny/react-month-picker) | Yes: nickeljew/react-month-picker | No | overview-read | Fork documents desktop/mobile examples and single-month versus range inputs. [Overview](https://github.com/bcherny/react-month-picker/blob/master/README.md). |
| [react-month-picker-demo](https://github.com/bcherny/react-month-picker-demo) | No | No | primary-file-read | No README; entrypoint only requires and logs the component, so it is not evidence of an interactive demo. [Overview](https://github.com/bcherny/react-month-picker-demo/blob/master/index.js). |
| [react2angular](https://github.com/bcherny/react2angular) | Yes: coatue-oss/react2angular | No | overview-read | Fork shows a short component adapter with explicitly listed properties. [Overview](https://github.com/bcherny/react2angular/blob/master/README.md). |
| [realmath](https://github.com/bcherny/realmath) | No | No | primary-file-read | No README; literate source overview lists supported mathematical symbols and scope-extension intent. [Overview](https://github.com/bcherny/realmath/blob/master/realmath.coffee.md). |
| [realtime-graph](https://github.com/bcherny/realtime-graph) | No | No | empty-metadata-only | API-confirmed empty repository; metadata-only coverage, no README or code available. |
| [record-browser](https://github.com/bcherny/record-browser) | No | No | primary-file-read | No README; manifest defines browserify build/watch while its test command explicitly fails as unimplemented. [Overview](https://github.com/bcherny/record-browser/blob/master/package.json). |
| [Reddit-Enhancement-Suite](https://github.com/bcherny/Reddit-Enhancement-Suite) | Yes: honestbleeps/Reddit-Enhancement-Suite | No | overview-read | Fork discusses reproducible support through versioning and distinct redistribution identity. [Overview](https://github.com/bcherny/Reddit-Enhancement-Suite/blob/master/README.md). |
| [redirect-claude](https://github.com/bcherny/redirect-claude) | No | No | overview-read | README explicitly redirects users to the official scoped package and disclaims being that package. [Overview](https://github.com/bcherny/redirect-claude/blob/main/README.md). |
| [redrock](https://github.com/bcherny/redrock) | No | No | overview-read | Documents typed actions, decoupled emitters/stores and previous/current state for listeners. [Overview](https://github.com/bcherny/redrock/blob/master/README.md). |
| [regex-evolution](https://github.com/bcherny/regex-evolution) | No | No | primary-file-read | No README; primary design notes consider nonlinear fitness and alternative search/scoring strategies. [Overview](https://github.com/bcherny/regex-evolution/blob/master/IDEAS.md). |
| [registry](https://github.com/bcherny/registry) | Yes: typings/registry | No | overview-read | Historical fork requires schema validation before registry changes and describes version/license metadata. [Overview](https://github.com/bcherny/registry/blob/master/README.md). |
| [regress](https://github.com/bcherny/regress) | No | No | overview-read | Work-in-progress regression API demonstrates expected coefficients and predicted values. [Overview](https://github.com/bcherny/regress/blob/master/README.md). |
| [relay](https://github.com/bcherny/relay) | Yes: facebook/relay | No | overview-read | Fork emphasizes colocating data requirements with views and a documented mutation boundary. [Overview](https://github.com/bcherny/relay/blob/master/README.md). |
| [rental-finder](https://github.com/bcherny/rental-finder) | No | No | overview-read | README provides only separate client build and server start commands. [Overview](https://github.com/bcherny/rental-finder/blob/master/README.md). |
| [repocount](https://github.com/bcherny/repocount) | No | No | overview-read | Documents asynchronous paginated results and browser-based test setup. [Overview](https://github.com/bcherny/repocount/blob/master/README.md). |
| [resume](https://github.com/bcherny/resume) | No | No | overview-read | Personal-site README states screen-size limitations and marks unit tests unfinished. [Overview](https://github.com/bcherny/resume/blob/master/README.md). |
| [robbie-the-robot](https://github.com/bcherny/robbie-the-robot) | No | No | overview-read | Exercise repository links its genetic-algorithm source assignment. [Overview](https://github.com/bcherny/robbie-the-robot/blob/master/README.md). |
| [RxJS](https://github.com/bcherny/RxJS) | Yes: Reactive-Extensions/RxJS | No | overview-read | Historical fork separates version branches, migration guidance and unreleased code. [Overview](https://github.com/bcherny/RxJS/blob/master/README.md). |
| [rxjs-1](https://github.com/bcherny/rxjs-1) | Yes: ReactiveX/rxjs | No | overview-read | Historical fork separates version branches, migration guidance and unreleased code. [Overview](https://github.com/bcherny/rxjs-1/blob/master/README.md). |
| [rxjs-filesize-repro](https://github.com/bcherny/rxjs-filesize-repro) | No | No | overview-read | Minimal reproduction compares output size under two compiler module settings with a build command. [Overview](https://github.com/bcherny/rxjs-filesize-repro/blob/master/README.md). |
| [rxjs-observable](https://github.com/bcherny/rxjs-observable) | No | No | overview-read | README explicitly narrows the package to bundlers lacking tree-shaking and explains its type-only RxJS dependency. [Overview](https://github.com/bcherny/rxjs-observable/blob/master/README.md). |
| [sandbox-runtime](https://github.com/bcherny/sandbox-runtime) | Yes: anthropics/sandbox-runtime | No | deep-sampled | Fork describes OS-level filesystem/network enforcement and explicitly marks the API as a research preview; deep inspection follows. [Overview](https://github.com/bcherny/sandbox-runtime/blob/main/README.md). |
| [sara-tests](https://github.com/bcherny/sara-tests) | No | No | overview-read | README supplies only a short test-running procedure; test behavior needs file inspection. [Overview](https://github.com/bcherny/sara-tests/blob/master/README.md). |
| [SASS-Base64](https://github.com/bcherny/SASS-Base64) | No | No | overview-read | Documents a Ruby/Sass extension invocation and a quotation requirement for image paths. [Overview](https://github.com/bcherny/SASS-Base64/blob/master/readme.md). |
| [Sass-output-Javascript](https://github.com/bcherny/Sass-output-Javascript) | Yes: edwardoriordan/sass-attributes | No | overview-read | Fork is an experiment passing Sass values into generated JavaScript. [Overview](https://github.com/bcherny/Sass-output-Javascript/blob/master/README.md). |
| [sass-to-typescript](https://github.com/bcherny/sass-to-typescript) | No | No | overview-read | Overview explicitly warns that pre-alpha behavior is incomplete and should not be used. [Overview](https://github.com/bcherny/sass-to-typescript/blob/master/README.md). |
| [savant](https://github.com/bcherny/savant) | No | No | overview-read | Uses filename conventions to produce multiple font formats and generated stylesheet outputs. [Overview](https://github.com/bcherny/savant/blob/master/README.md). |
| [sha1-from-file](https://github.com/bcherny/sha1-from-file) | No | No | overview-read | Separates stream-based asynchronous hashing from synchronous string/buffer handling; not a cryptographic-security recommendation. [Overview](https://github.com/bcherny/sha1-from-file/blob/master/README.md). |
| [signature_pad](https://github.com/bcherny/signature_pad) | Yes: szimek/signature_pad | No | overview-read | Fork highlights resize/high-DPI examples and differentiates release code from the development branch. [Overview](https://github.com/bcherny/signature_pad/blob/master/README.md). |
| [skymaps](https://github.com/bcherny/skymaps) | No | No | primary-file-read | Blank README; package manifest combines React/Mapbox and a test entrypoint; application behavior not inspected. [Overview](https://github.com/bcherny/skymaps/blob/main/package.json). |
| [SlickGrid](https://github.com/bcherny/SlickGrid) | Yes: SimplGy/SlickGrid | No | overview-read | Fork explains renaming to make duplicated grid regions and control responsibilities easier to understand. [Overview](https://github.com/bcherny/SlickGrid/blob/master/README.md). |
| [snapper](https://github.com/bcherny/snapper) | No | No | overview-read | README marks reliable interval capture and network capture as unfinished. [Overview](https://github.com/bcherny/snapper/blob/master/README.md). |
| [sort](https://github.com/bcherny/sort) | No | No | primary-file-read | No README; binary.js is blank; manifest names a nodeunit test command, so implementation remains unproven. [Overview](https://github.com/bcherny/sort/blob/master/package.json). |
| [stanc.es](https://github.com/bcherny/stanc.es) | No | No | primary-file-read | Blank README; primary HTML arranges sourced policy viewpoints in a table; no policy claims validated here. [Overview](https://github.com/bcherny/stanc.es/blob/master/index.html). |
| [steer-screenshot](https://github.com/bcherny/steer-screenshot) | Yes: AndreasMadsen/steer-screenshot | No | overview-read | Fork documents screenshot validation before bounded retry and explains the race it addresses. [Overview](https://github.com/bcherny/steer-screenshot/blob/master/README.md). |
| [struct](https://github.com/bcherny/struct) | No | No | primary-file-read | No README; selected source defines a minimal linked-list node with value/next fields. [Overview](https://github.com/bcherny/struct/blob/master/linkedlist.js). |
| [Styled.js](https://github.com/bcherny/Styled.js) | No | No | overview-read | Legacy select-styling instructions include compatibility variants while leaving unit tests unfinished. [Overview](https://github.com/bcherny/Styled.js/blob/master/readme.md). |
| [Stylus](https://github.com/bcherny/Stylus) | Yes: billymoon/Stylus | No | overview-read | Fork explicitly records tested platforms, Unicode-path problems and a required external binary. [Overview](https://github.com/bcherny/Stylus/blob/master/README.markdown). |
| [svg-font-create](https://github.com/bcherny/svg-font-create) | Yes: fontello/svg-font-create | No | overview-read | Fork README explicitly lists its changes from upstream, including metadata conventions and less filesystem I/O. [Overview](https://github.com/bcherny/svg-font-create/blob/master/README.md). |
| [Talks](https://github.com/bcherny/Talks) | No | No | primary-file-read | No root README; one slideshow's own README provides hosted and local viewing instructions; other talks not audited. [Overview](https://github.com/bcherny/Talks/blob/master/why-typescript/README.md). |
| [tassert](https://github.com/bcherny/tassert) | No | No | overview-read | Alpha runtime assertion library distinguishes implemented types from unfinished coverage. [Overview](https://github.com/bcherny/tassert/blob/master/README.md). |
| [tds-frontend](https://github.com/bcherny/tds-frontend) | No | No | overview-read | Project README records mapping-token setup, local commands and an editor suggestion for its historical stack. [Overview](https://github.com/bcherny/tds-frontend/blob/master/README.md). |
| [tds-frontend-1](https://github.com/bcherny/tds-frontend-1) | Yes: bayesimpact/encompass | No | overview-read | Fork documents environment prerequisites and separate build/start/test commands for a mapping application. [Overview](https://github.com/bcherny/tds-frontend-1/blob/master/README.md). |
| [tds-frontend-mock-server](https://github.com/bcherny/tds-frontend-mock-server) | No | No | primary-file-read | No README; source returns fixture responses over a self-signed local HTTPS server and adds random population data. [Overview](https://github.com/bcherny/tds-frontend-mock-server/blob/master/index.ts). |
| [tdux-demo](https://github.com/bcherny/tdux-demo) | No | No | primary-file-read | No README; manifest separates stylesheet, HTML and JavaScript builds for a typed-state demo. [Overview](https://github.com/bcherny/tdux-demo/blob/master/package.json). |
| [testcheck-js](https://github.com/bcherny/testcheck-js) | Yes: leebyron/testcheck-js | No | overview-read | Fork describes property testing with generated inputs and minimizing a failing example. [Overview](https://github.com/bcherny/testcheck-js/blob/master/README.md). |
| [textwidth](https://github.com/bcherny/textwidth) | No | No | overview-read | Documents a style-registration boundary and admits non-WebKit compatibility is theoretical. [Overview](https://github.com/bcherny/textwidth/blob/master/README.md). |
| [token](https://github.com/bcherny/token) | No | No | primary-file-read | No README; generator emits alternative repeated-string encodings for size experiments. [Overview](https://github.com/bcherny/token/blob/master/generator.php). |
| [tracery](https://github.com/bcherny/tracery) | Yes: junosuarez/tracery | No | overview-read | Fork composes object predicates to validate nested structure at runtime. [Overview](https://github.com/bcherny/tracery/blob/master/README.md). |
| [transform-to-matrix](https://github.com/bcherny/transform-to-matrix) | No | No | overview-read | Lists supported transforms and links their mathematical definitions; claimed coverage was not independently run. [Overview](https://github.com/bcherny/transform-to-matrix/blob/master/README.md). |
| [ts-brand](https://github.com/bcherny/ts-brand) | Yes: kourge/ts-brand | No | overview-read | Fork motivates nominal identity through otherwise interchangeable numeric user/post identifiers. [Overview](https://github.com/bcherny/ts-brand/blob/master/README.md). |
| [tsedit](https://github.com/bcherny/tsedit) | No | No | overview-read | Notebook overview names execution interaction and explicitly leaves safe code persistence unresolved. [Overview](https://github.com/bcherny/tsedit/blob/master/README.md). |
| [tsinit](https://github.com/bcherny/tsinit) | No | No | overview-read | Generator shows exact produced files and unresolved initialization tasks; do not carry its old TSLint/CircleCI stack into a neutral template. [Overview](https://github.com/bcherny/tsinit/blob/master/README.md). |
| [tslint](https://github.com/bcherny/tslint) | Yes: palantir/tslint | No | overview-read | Historical fork documents rule/reporting extension points; use current host tooling rather than reinstalling this stack. [Overview](https://github.com/bcherny/tslint/blob/master/README.md). |
| [tslint-no-circular-imports](https://github.com/bcherny/tslint-no-circular-imports) | No | No | overview-read | Demonstrates actionable import-cycle chains and configurable warning severity; TSLint-specific integration is historical. [Overview](https://github.com/bcherny/tslint-no-circular-imports/blob/master/README.md). |
| [tsoption](https://github.com/bcherny/tsoption) | No | No | deep-sampled | Examples expose absent-value handling through Option/Some/None with statically constrained fallback types. [Overview](https://github.com/bcherny/tsoption/blob/master/README.md). |
| [tsresult](https://github.com/bcherny/tsresult) | No | No | empty-metadata-only | API-confirmed empty repository; metadata-only coverage, no README or code available. |
| [tstry](https://github.com/bcherny/tstry) | No | No | empty-metadata-only | API-confirmed empty repository; metadata-only coverage, no README or code available. |
| [tuple-map](https://github.com/bcherny/tuple-map) | No | No | overview-read | Examples make two-part keys and resulting map size explicit. [Overview](https://github.com/bcherny/tuple-map/blob/master/README.md). |
| [tuple-set](https://github.com/bcherny/tuple-set) | No | No | overview-read | Shows pair-key membership and size with a minimal test command. [Overview](https://github.com/bcherny/tuple-set/blob/master/README.md). |
| [turn-calendar](https://github.com/bcherny/turn-calendar) | Yes: phamductri/turn-calendar | No | overview-read | Fork specifies date-selection modes and comparative features; UI choice remains app-specific. [Overview](https://github.com/bcherny/turn-calendar/blob/master/README.md). |
| [tyler](https://github.com/bcherny/tyler) | No | No | overview-read | Tiling UI documents options and explicitly limits CSS support to WebKit. [Overview](https://github.com/bcherny/tyler/blob/master/README.md). |
| [type-o-rama](https://github.com/bcherny/type-o-rama) | Yes: stereobooster/type-o-rama | No | overview-read | Fork is a conversion-tool matrix between type systems, not proof that conversions preserve all semantics. [Overview](https://github.com/bcherny/type-o-rama/blob/master/README.md). |
| [typed-rx-emitter](https://github.com/bcherny/typed-rx-emitter) | No | No | deep-sampled | Separates compile-time channel/payload checking from a runtime cycle warning. [Overview](https://github.com/bcherny/typed-rx-emitter/blob/master/README.md). |
| [typed-store](https://github.com/bcherny/typed-store) | No | No | overview-read | Experimental Angular store documents runtime rejection of invalid assignments and immutable backing with a mutable facade. [Overview](https://github.com/bcherny/typed-store/blob/master/README.md). |
| [typed-trait](https://github.com/bcherny/typed-trait) | No | No | overview-read | Makes conflicting mixin members a compile-time error instead of relying on implicit override order. [Overview](https://github.com/bcherny/typed-trait/blob/master/README.md). |
| [typed-useragent](https://github.com/bcherny/typed-useragent) | No | No | overview-read | README identifies a separate declaration package for a user-agent library. [Overview](https://github.com/bcherny/typed-useragent/blob/master/README.md). |
| [typedex](https://github.com/bcherny/typedex) | No | No | overview-read | Design notes carry source code and location alongside extracted compiler signatures for traceability. [Overview](https://github.com/bcherny/typedex/blob/master/README.md). |
| [typeorm](https://github.com/bcherny/typeorm) | Yes: typeorm/typeorm | No | overview-read | Historical fork distinguishes stable versus development installation and warns documentation is incomplete. [Overview](https://github.com/bcherny/typeorm/blob/master/README.md). |
| [types-publisher](https://github.com/bcherny/types-publisher) | No | No | primary-file-read | Blank README; manifest makes tests a prepublish gate and compiles before tests. [Overview](https://github.com/bcherny/types-publisher/blob/master/package.json). |
| [TypeScript](https://github.com/bcherny/TypeScript) | Yes: microsoft/TypeScript | No | overview-read | Historical fork presents compiler installation channels and ways to verify submitted fixes. [Overview](https://github.com/bcherny/TypeScript/blob/master/README.md). |
| [typescript-chess](https://github.com/bcherny/typescript-chess) | No | No | overview-read | README identifies a book chapter example; the installation-only instructions do not demonstrate play behavior. [Overview](https://github.com/bcherny/typescript-chess/blob/master/README.md). |
| [typings-history](https://github.com/bcherny/typings-history) | Yes: andrew-w-ross/typings-history | No | overview-read | Fork README identifies its declaration target and an older typing-manager workflow. [Overview](https://github.com/bcherny/typings-history/blob/master/readme.md). |
| [u](https://github.com/bcherny/u) | No | No | overview-read | README explains extracting repeated small utilities and links literate implementation documentation. [Overview](https://github.com/bcherny/u/blob/master/README.md). |
| [umodel](https://github.com/bcherny/umodel) | No | No | overview-read | Documents nested-key behavior and change events with a compact model API. [Overview](https://github.com/bcherny/umodel/blob/master/README.md). |
| [undux](https://github.com/bcherny/undux) | No | No | deep-sampled | State API emphasizes typed get/set operations and separate connected React bindings; deep inspection follows. [Overview](https://github.com/bcherny/undux/blob/master/README.md). |
| [undux-fb](https://github.com/bcherny/undux-fb) | No | No | overview-read | Explicitly points general users to the main package; its internal wrapper is not a default to adopt. [Overview](https://github.com/bcherny/undux-fb/blob/master/README.md). |
| [undux-hot-module-reloading-demo](https://github.com/bcherny/undux-hot-module-reloading-demo) | No | No | overview-read | Provides a visible edit-and-observe loop for UI state/effect hot reload. [Overview](https://github.com/bcherny/undux-hot-module-reloading-demo/blob/master/README.md). |
| [undux-todomvc](https://github.com/bcherny/undux-todomvc) | No | No | overview-read | An end-to-end task application demonstrates persistence and filtering with local start instructions. [Overview](https://github.com/bcherny/undux-todomvc/blob/master/README.md). |
| [undux.org](https://github.com/bcherny/undux.org) | No | No | overview-read | Documentation site distinguishes local development from deployment commands. [Overview](https://github.com/bcherny/undux.org/blob/master/README.md). |
| [user-documentation](https://github.com/bcherny/user-documentation) | Yes: hhvm/user-documentation | No | overview-read | Fork separates guides from API reference and avoids duplicating another project's authoritative docs. [Overview](https://github.com/bcherny/user-documentation/blob/master/README.md). |
| [uxhr](https://github.com/bcherny/uxhr) | No | No | overview-read | Small request wrapper documents optional data and cancellation through an abort handle. [Overview](https://github.com/bcherny/uxhr/blob/master/README.md). |
| [vscode](https://github.com/bcherny/vscode) | Yes: microsoft/vscode | No | overview-read | Historical fork frames development around edit/build/debug and links contribution paths. [Overview](https://github.com/bcherny/vscode/blob/master/README.md). |
| [watch-dom](https://github.com/bcherny/watch-dom) | No | No | overview-read | Explains when DOM state, rather than Angular scope, is the appropriate observation boundary. [Overview](https://github.com/bcherny/watch-dom/blob/master/README.md). |
| [wd](https://github.com/bcherny/wd) | Yes: admc/wd | No | overview-read | Fork records a breaking touch API change and the external Selenium server prerequisite. [Overview](https://github.com/bcherny/wd/blob/master/README.md). |
| [website](https://github.com/bcherny/website) | Yes: json-schema-org/website | No | overview-read | Forked JSON Schema site lists local prerequisites, submodule setup and a project structure map. [Overview](https://github.com/bcherny/website/blob/main/README.md). |
| [whotracksme.org](https://github.com/bcherny/whotracksme.org) | No | No | directory-only | README and primary static index are both blank; directory-only coverage, no implemented behavior to learn. |
| [wikimedia-demo](https://github.com/bcherny/wikimedia-demo) | No | No | overview-read | Prototype distinguishes implemented threaded comments from proposed reply, sorting and loading features. [Overview](https://github.com/bcherny/wikimedia-demo/blob/master/README.md). |
| [winston-bugsnag](https://github.com/bcherny/winston-bugsnag) | No | No | overview-read | Shows an adapter between logging and error reporting, including user metadata attachment. [Overview](https://github.com/bcherny/winston-bugsnag/blob/master/README.md). |
| [wordscapes-solver](https://github.com/bcherny/wordscapes-solver) | No | No | overview-read | CLI example separates likely dictionary matches from less likely candidates. [Overview](https://github.com/bcherny/wordscapes-solver/blob/master/README.md). |
| [yocto-spinner](https://github.com/bcherny/yocto-spinner) | Yes: sindresorhus/yocto-spinner | No | overview-read | Fork overview includes signal handling, non-Unicode output and CI compatibility as terminal edge cases. [Overview](https://github.com/bcherny/yocto-spinner/blob/main/readme.md). |
| [yoga-wasm-web](https://github.com/bcherny/yoga-wasm-web) | Yes: shuding/yoga-wasm-web | No | overview-read | Fork distinguishes synchronous ASM initialization from asynchronous WASM binary loading. [Overview](https://github.com/bcherny/yoga-wasm-web/blob/main/README.md). |
| [zed](https://github.com/bcherny/zed) | Yes: zed-industries/zed | No | overview-read | Fork overview links platform-specific build guidance and makes dependency-license checks a CI concern. [Overview](https://github.com/bcherny/zed/blob/main/README.md). |

