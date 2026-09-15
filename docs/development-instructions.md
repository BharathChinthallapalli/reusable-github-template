# Choose development instructions by the actual project

The template remains language-neutral. Version 3.4 adds conditional guidance,
not a Next.js application, new dependencies or a mandatory architecture. Start
with the nearest project manifest and current source; keep existing conventions.

| Work | Canonical guidance | Applicability |
| --- | --- | --- |
| TypeScript implementation/tooling | [TypeScript](../.github/instructions/typescript.instructions.md) | TypeScript and its compiler/linter configuration |
| Next.js server and route work | [Next.js](../.github/instructions/nextjs.instructions.md) | Actual Next.js app; identify version and router first |
| Browser UI | [Web UI](../.github/instructions/web-ui.instructions.md) | Browser components, CSS and related styling configuration |
| JavaScript/TypeScript tests | [Tests](../.github/instructions/typescript-testing.instructions.md) | Existing unit/component/integration/browser tests |
| PowerShell | [PowerShell](../.github/instructions/powershell.instructions.md) | Project scripts and modules |
| GitHub Actions | [Workflows](../.github/instructions/workflows.instructions.md) | Existing CI/CD workflow paths |

Read the relevant row, not every file. Other hosts can follow these links from
AGENTS.md when native scoped-instruction loading is unavailable. These files
guide agents; they do not configure compilers, linters, permissions or isolation.

## Use in VS Code and existing projects

1. Merge the applicable instruction files and root routing with existing project
   guidance. Preserve local policies and customizations; avoid duplicate copies.
2. Record actual versions and application commands in `docs/project.md`. No
   framework or formatter needs installation merely to load an instruction file.
3. In VS Code Chat, inspect the customizations/instructions UI and use Chat
   diagnostics to check discovery. Ask a small task involving an actual matching
   file and inspect the loaded instructions and resulting behavior.
4. Check an unrelated task too: a Python utility should not acquire Next.js
   requirements, and a React Native component should not acquire browser DOM rules.
5. Preserve existing host approvals and managed security settings. Diagnose an
   unexpected denial at the active hook/profile; editing instructions does not
   override a hook, and disabling it is not the recovery procedure.

The `applyTo` patterns select candidate files. A pattern match alone does not prove
activation or model compliance, and scope support differs by Copilot surface.
These repository files are not a universal GitHub account policy. Follow
[AI diagnostics](ai-assistance.md) for host-specific evidence and
[VS Code's documentation](https://code.visualstudio.com/docs/agent-customization/custom-instructions)
for current instruction loading behavior.

## Keep the useful parts of a rule catalog

Retain boundaries, meaningful tests, accessibility, clear errors and maintained
contracts. Use the existing discovery, planning, clean-code, review and context
skills rather than adding duplicate mandatory lifecycle stages.

Only introduce microservices, event sourcing, offline synchronization, DDD,
feature-sliced design, CLI plugins, SDK generation or support timelines when an
actual requirement warrants them. Embedded firmware, Solidity and native mobile
rules do not belong in a general Next.js instruction file. Pick one coherent
styling/formatting setup, and let its configuration enforce mechanical style.

Do not require a new plan approval for every edit, re-open finished work to seek
elegance, or save every correction as a permanent rule. A substantive plan should
name the target, boundary and acceptance evidence; stop once those are satisfied.
Do not publish real sandbox API keys, source maps or test artifacts as a side
effect of documentation or debugging. Use placeholders and an explicitly approved
publication target when publication is part of the task.

See [selection decisions, sources and verification](research/scoped-development-rules.md).
