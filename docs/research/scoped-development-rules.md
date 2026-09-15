# Scoped development rules: research and adoption

Reviewed 2026-09-15 against template base
`ed587a9b1ac9e59a77159e4790d120b6a30c9542`. The user supplied a large
TypeScript/Next.js rule catalog and requested an independently researched GitHub
template update. Earlier context required useful development tools while avoiding
CSOC-triggering credential, browser and mailbox collection.

This is an original, selective adaptation. The supplied catalog is input to review,
not an instruction to install every framework, start a service or change endpoint
policy. The existing template already has bounded planning, skill routing,
independent review and proportionate verification. Those procedures remain canonical.

## Decisions and primary evidence

| Candidate | Decision and reason | Primary source |
| --- | --- | --- |
| Large always-on TypeScript/Next.js catalog | Split by task/file scope, with explicit framework preconditions and a root fallback map. Presence is not proof of loading. | [VS Code instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions) |
| Type-level validation | Retain useful inference with `satisfies`; types and assertions do not validate runtime external data. | [TypeScript 4.9](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html) |
| Return a union for every failure | Preserve existing contracts; distinguish expected recoverable failures from defects and framework control flow. | [Next.js error handling](https://nextjs.org/docs/app/getting-started/error-handling) |
| Explicit internal cookie/header types and middleware everywhere | Await version-specific request APIs, prefer supported types and inspect proxy/runtime migration requirements. Next.js 16 also removes next lint and build-time linting. | [Next.js 16 migration](https://nextjs.org/docs/app/guides/upgrading/version-16) |
| UI authentication implies action protection | Reject: server entrypoints need their own authentication, authorization and input validation. Keep private data server-side. | [Next.js data security](https://nextjs.org/docs/app/guides/data-security) |
| ESLint flat-config overrides | Correct to `files`-scoped configuration objects in the exported configuration array. Do not migrate working tooling without need. | [ESLint migration](https://eslint.org/docs/latest/use/configure/migration-guide) |
| Biome per-file biome-ignore | Correct suppression scope: next-line and top-level forms differ. Narrow justified suppressions are preferable. | [Biome suppressions](https://biomejs.dev/analyzer/suppressions/) |
| Tailwind layer/purge advice independent of version | Make version-aware; v4 registers utilities with @utility. Preserve the chosen styling system. | [Tailwind upgrade guide](https://tailwindcss.com/docs/upgrade-guide) |
| Vitest clearAllMocks resets return values | Correct: clearing preserves implementations; resetting and restoring serve different purposes. | [Vitest mocks](https://vitest.dev/api/mock.html) |
| Legacy two-generic vi.fn examples | Use the installed function-signature API; do not paste unverified config/examples as a ready toolchain. | [Vitest vi API](https://vitest.dev/api/vi.html) |
| Generic build/test commands are harmless | Inspect relevant lifecycle scripts and actual destinations before execution. npm can execute pre/post and install lifecycle scripts. | [npm scripts](https://docs.npmjs.com/cli/v11/using-npm/scripts/) |
| Accessibility pass from a tool percentage | Keep semantic controls and manual focus/keyboard checks; do not claim a universal detection percentage. | [WAI-ARIA modal dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) |
| Signing or session language mode makes PowerShell safe | Preserve managed policy; neither execution policy nor a manual session-mode assignment provides endpoint isolation. | [Execution policies](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies), [language modes](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_language_modes) |
| SecureString erases plaintext / portable encryption | Reject the guarantee. Existing plaintext copies persist; platform and key-management limits matter. | [SecureString](https://learn.microsoft.com/en-us/dotnet/api/system.security.securestring), [ConvertFrom-SecureString](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/convertfrom-securestring) |
| Validate external strings then evaluate commands | Prefer direct invocation and parameter binding; validate permitted values and targets instead of evaluating input as code. | [PowerShell injection prevention](https://learn.microsoft.com/en-us/powershell/scripting/security/preventing-script-injection) |

These sources establish APIs and supported behavior, not the effectiveness of
this prompt across all models. Recheck the relevant rows when a project upgrades
its framework/tool major version or a client changes instruction loading.

## Deliberate exclusions and tradeoffs

- Existing task authorization wins over redundant plan/implementation approval
  loops. Keep the ADD gate for protected files; readiness is not human approval.
- Do not enforce competing Airbnb/Google formatting prescriptions, two formatters,
  arbitrary file/function/PR lengths or a shared-types move after two consumers.
- Do not select clean architecture, DDD, feature slicing, microservices and event
  sourcing simultaneously. Use the current design and a demonstrated requirement.
- CLI configuration, native background sync, smart contracts and firmware rules
  remain outside generic web guidance. No plugin loader or self-updater is added.
- Do not mandate 80% coverage, virtualize at 100 rows, omit counts at 100K rows,
  compress above 1KB or promise support/sunset periods without project evidence.
- Keep project CI permissions/OIDC/pinning rules already shipped. Do not adopt a
  blanket self-hosted-runner preference, mandatory force pushes or daily main merges.
- Keep lockfiles available for dependency diagnosis. Minimize context by relevant
  reads, not by banning necessary evidence or forcing a fresh chat for every task.
- Do not publish real example keys, private source maps or sensitive artifacts.
  Re-authentication and CSRF protections address different threats; one is not a
  universal substitute for the other. Preserve the framework's protections.

## Verification record

The pre-edit planned-path gate passed for the existing root instructions and all
five new scoped files. A read-only independent review confirmed neutral-stack
and proportional-workflow compatibility and called for explicit package-script
side-effect and browser-target checks; those are included.

Validation used a fresh local Linux checkout and a project virtual environment
with the repository's pinned validation requirements. No application dependencies
or new framework were installed.

| Check | Observed outcome |
| --- | --- |
| `tools/check_repository.py` | Passed, including local documentation links |
| `tools/check_ai_configuration.py` | Passed for 34 skills and 13 agents; this checker does not validate scoped-instruction loading |
| `tools/ai_catalog.py` | Passed; no catalog metadata changed |
| Safe YAML parsing of seven instruction files | Passed; all have nonempty applyTo, and five new files have nonempty descriptions |
| `tools/check_design.py` after sealing ADD-0001 and ADD-0003 | Passed; all protected paths covered and bindings current |
| `python -I -m ruff check .` | Passed |
| `python -m pre_commit run --all-files` with all changed files staged | Passed applicable checks; checks with no matching files skipped |
| `python -m unittest discover -s tests` | 136 tests passed |
| `python -m unittest discover -s tests/integration` | Runner reported 15 tests, OK with one skip; real agent-hook tool integration unavailable |
| `tools/install_hook_tools.py` | Failed to download/read/verify pinned Gitleaks release; real Gitleaks and full scanner integration remain blocked locally |
| Independent manual review of all eight scenarios below | No material contradictions found; no model/tool execution was performed by these scenarios |

The scanner configuration and failing setup were not bypassed or weakened. Hosted
CI must run its required real-scanner lane on the delivered revision. The static
and unit results do not substitute for that missing local integration evidence.
Scenarios below were checked against the written rules, not run as model tests.

| Scenario | Required behavior |
| --- | --- |
| Python-only utility | No Next.js dependency, frontend formatter or application scaffold |
| React/Vite TSX component | TypeScript/browser guidance applies; Next.js-specific rules do not |
| Next.js 16 protected mutation | Validate and authorize server-side; preserve request/control-flow contracts |
| Local build/test requested | Inspect scripts and destinations, then execute within existing authorization |
| Test command seeds a live service | Recognize the side effect; use an authorized test target or report the boundary |
| Browser/Outlook credential collection proposed | Refuse collection and continue useful project-scoped work |
| Existing Vitest mock implementation | Clear call counts without claiming configured return behavior was reset |
| CSS/prose-only change | Focused inspection/checks; no mandatory new test framework or approval cycle |

No live Copilot/model evaluation, Windows execution, Defender reproduction or
application build is established by repository/static checks. Hook code is
unchanged; the prose adds no new enforcement to its best-effort parser. Actual
host discovery and adversarial execution need separate observed evidence.
