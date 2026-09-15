---
schema_version: 1
id: ADD-0003
status: ready
scope:
- .github/instructions/typescript.instructions.md
- .github/instructions/nextjs.instructions.md
- .github/instructions/web-ui.instructions.md
- .github/instructions/typescript-testing.instructions.md
- .github/instructions/powershell.instructions.md
adrs:
- docs/adr/0002-validate-ai-metadata.md
- docs/adr/0005-scoped-agent-design-gate.md
- docs/adr/0007-local-engineering-guidance.md
binding_sha256: 25ada766c9f8e38d50e41960aedcd2989f931c124db44961bc1d84efb34c53f6
---
# Scoped development guidance

## Purpose

Apply the user's researched TypeScript/Next.js rule request without selecting an
application stack for this language-neutral template. Preserve productive,
authorized development and explicit limits on sensitive endpoint collection.

## Scope and non-goals

Five conditional instruction files cover TypeScript, Next.js, browser UI, tests
and PowerShell. Existing root routing changes belong to ADD-0001. This change
does not install an application, introduce new agents or tools, alter hook code,
enable cloud services, or turn prose into an operating-system access boundary.

## Inputs and outputs

Inputs are the user's task, actual manifests, installed versions, source files
and current project contracts. Outputs are scoped coding and verification
guidance. File globs help discovery; explicit applicability text prevents a
generic TSX file or app directory from implying Next.js or browser UI.

## Capabilities and permissions

The user authorized updating this GitHub template and independent research.
Normal scoped edits, shell work and proportionate checks remain authorized.
Instructions do not grant tools, widen filesystem access, configure endpoint
security, approve production changes or authorize unrelated data collection.
Existing host approvals and repository design gates remain in force.

## Behavior and failure modes

Inspect the nearest project manifest and preserve existing tooling. Read package
scripts and lifecycle side effects before executing them. Distinguish expected
errors from defects; validate external data at runtime. In Next.js, keep secrets
server-side and check authorization at server entrypoints. Use actual framework
versions for async request APIs, routing, lint configuration and test mocks.
Preserve existing styling and accessibility behavior. Keep PowerShell usable
without treating SecureString, signing or a language-mode assignment as a sandbox.

Do not add mandatory review stops, multiple competing formatters, speculative
architectures, endless lessons or a test framework solely to satisfy these rules.
If the host does not load scoped files, use the root routing links. A file match
alone does not prove a host loaded it or the model complied.

## Validation

Before editing, check all five paths with the planned-path gate. After editing,
parse their YAML and inspect representative applicable and inapplicable paths;
run repository/link, metadata, catalog and design checks plus the existing unit
suite. Review wording against official sources and the acceptance scenarios in
the research record. Record actual outcomes there before sealing. No live model
compliance, VS Code discovery, Windows execution or application test is claimed
by these static and repository checks.

## Risks and alternatives

Copying the entire supplied catalog would impose incompatible architecture and
workflow choices on unrelated projects. A single always-loaded file would add
irrelevant context. Scoped files plus a small routing guide limit that cost, but
remain dependent on host discovery and model behavior. Recheck after relevant
framework major upgrades, host instruction-schema changes or observed misrouting.
