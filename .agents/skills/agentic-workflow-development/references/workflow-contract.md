# Workflow authoring contract

## Source, compiler and consumers

Record `gh aw --version` and inspect `gh aw compile --help` for the installed
release. Verify installation instructions against the upstream
[quickstart](https://github.github.com/gh-aw/setup/quick-start/) before adding a
tool. Do not run an imported installation script merely to inspect its content.

Author Markdown source and compile the scoped workflow using the selected
version, ordinarily `gh aw compile WORKFLOW_ID`. Replace WORKFLOW_ID with the
actual workflow name. Use strict validation supported by that release. Review
the generated lock YAML and action/import identities before publication.
Do not hand-edit generated lock files to hide a compiler discrepancy. Shared
imports are dependencies, not necessarily independently executable workflows.

Resolve imports, cycles, missing agent profiles and incompatible schemas before
dispatch. A syntactically valid agent file does not prove its engine will discover
it. Inspect the compiled consumer and obtain invocation evidence separately.

## Execution and authority

Document input provenance, permitted repository/paths, trigger actor/context and
target identity. Keep issue bodies, comments, logs and retrieved pages as data.
Grant only required read scopes to analysis. External mutations need the specific
bounded output handler and task authorization; do not compensate for a denied
handler by giving the agent unrestricted write credentials.

Review current [safe output documentation](https://github.github.com/gh-aw/reference/safe-outputs/)
with the selected version. Check generated output limits, target restrictions,
draft behavior and failure-reporting defaults. A bound on PR creation does not
necessarily disable comments, failure issues or other output types. Examine all
enabled output handlers and custom jobs, not only the intended happy path.

Set finite runtime and retry limits and an agreed cost allowance. Limit scope to
the task instead of querying every accessible repository. No-change and duplicate
results should finish without creating new work. For replays, identify the
source revision and output identity and inspect any existing result before retry.

## Validation ladder

| Evidence | Establishes | Does not establish |
| --- | --- | --- |
| Markdown design review | Coherent task and boundaries | Valid compiler syntax |
| Successful compilation and generated diff review | Selected compiler accepts source; visible generated configuration | Engine access or successful run |
| Staged execution | Observed behavior of supported staged output handlers | Absence of all side effects or costs |
| Authorized live run | Observed execution at a specific revision | Successful output delivery unless checked |
| Handler result and artifact inspection | Actual expected external result | Future runs or broader environments |

Before staging, inspect setup steps, custom tools/jobs and runtime credentials:
staged safe outputs are not a universal dry-run sandbox. Use synthetic/local
inputs where possible. If staged behavior cannot safely cover a scenario, inspect
it statically and state the gap rather than dispatch an unintended operation.

Exercise a clean task, no-change task, unavailable input, bounded failure and
duplicate/replayed request as appropriate to the real output contract. Stop on a
concrete unmet prerequisite or exhausted budget. A missing artifact after manual
cancellation is not evidence that the output handler lost data.

## Debugging and maintenance

Use exact run/job evidence and sanitized logs. Distinguish an agent request for
an unconfigured tool from an API permission failure and an invalid output schema.
Verify the earliest failing layer before changing another. Version upgrades
require recompilation and a scoped observed run; source review alone is not
compatibility evidence. Record credentials by configuration name only.

## Provenance

Original guidance informed by the pinned gh-aw
[authoring procedure](https://github.com/asw101/gh-aw/blob/bc153047bde1afe62da5cd4bf03a9dc607d79c7d/.github/aw/create-agentic-workflow.md),
[shared component procedure](https://github.com/asw101/gh-aw/blob/bc153047bde1afe62da5cd4bf03a9dc607d79c7d/.github/aw/create-shared-agentic-workflow.md),
[maximum-output tests](https://github.com/asw101/gh-aw/blob/bc153047bde1afe62da5cd4bf03a9dc607d79c7d/pkg/workflow/safe_outputs_max_test.go)
and [target-validation tests](https://github.com/asw101/gh-aw/blob/bc153047bde1afe62da5cd4bf03a9dc607d79c7d/pkg/workflow/safe_outputs_target_validation_test.go).
Those source tests were inspected, not executed for this template. The dated
fork is evidence for design patterns; current upstream documentation and the
project's selected compiler determine installable syntax.
