---
name: interface-validation
description: Validate a changed UI, CLI, API or packaged integration through the interface its consumer actually uses, including relevant error and accessibility behavior. Use when static checks or unit tests cannot establish the affected interaction.
---

# Check the consumer's interface

Identify the changed consumer contract and the real entrypoint from code and
project commands. Select only the relevant mode in the
[interface case record](assets/interface-cases.md). Use the project's existing
runner and available host tools; do not invent a browser capability, start a
provider integration or install a new test framework to satisfy this procedure.

- **UI:** Exercise the changed user task and relevant loading, empty, error and
  recovery states. Inspect rendered behavior at supported sizes where layout is
  affected. For changed controls, verify keyboard reachability, visible focus,
  accessible names and errors, and focus behavior after the interaction. A
  screenshot or automated accessibility result alone is incomplete evidence.
- **CLI:** Invoke the real command with representative arguments. Check exit
  status, stdout/stderr contract, help/invalid arguments and affected filesystem
  state. Failed operations must not appear successful because a wrapper masks an
  exit code. Use an isolated directory for mutating cases.
- **API:** Exercise the affected request/response and side effect with synthetic
  fixtures. Check status, schema and relevant malformed/unauthorized cases at the
  actual boundary. Mocks can verify adapter logic but do not prove a live identity,
  network or provider contract works.
- **Package or host integration:** Inspect the built artifact and load it through
  the supported consumer when available. Verify required files, excluded private
  or development-only material, and the behavior affected by this change. A valid
  manifest does not prove discovery, invocation or successful operation.

Use [test-design](../test-design/SKILL.md) for repeatable cases and
[verify-change](../verify-change/SKILL.md) for the complete verification report.
Keep the inspected artifact/revision, environment and case results together.
If a required browser, editor host, provider or test identity is unavailable,
report that boundary as blocked or not run with a precise next check. Do not
claim that inspecting markup or configuration exercised the interface.

For a versioned contract, compare the declared schema, parser/runtime behavior,
documented errors and representative examples. Trace a requirement ID to the
consumer-visible assertion; successful schema parsing alone does not establish
runtime conformance. Include a compatible existing consumer and the changed
failure case when relevant. Use the specification mode in
[solution-architecture](../solution-architecture/SKILL.md) when defining the contract.
