# Agentic workflow development

The template includes a
[gh-aw authoring skill](../.agents/skills/agentic-workflow-development/SKILL.md)
and a [workflow design record](../.agents/skills/agentic-workflow-development/assets/workflow-design.md).
These support creating, validating and debugging workflows. The template does
not install gh-aw, choose a model engine or enable paid scheduled runs.

gh-aw compiles Markdown workflow source into GitHub Actions YAML. Use the
[upstream quickstart](https://github.github.com/gh-aw/setup/quick-start/) for
current setup, then record the actual installed version and inspect compiler
help before authoring executable configuration. A generated file and a successful
run are separate evidence.

## Documentation maintenance recipe

This is a design recipe, not an executable or compile-tested workflow.

| Contract | Starting design, adapted to the project |
| --- | --- |
| Task | Improve one named documentation topic using code/configuration evidence |
| Trigger | Manual dispatch with a topic; add recurrence only for a requested operational need |
| Scope | Named documentation paths and relevant read-only implementation sources |
| Procedure | Documentation-writing skill and documentation-writer agent if supported by the selected engine |
| Validation | Existing link/build checks plus the changed reader task |
| Result | No output when no useful change exists; otherwise one scoped documentation change |
| Delivery | Staged review first; at most one draft PR if that external operation is authorized |
| Other output | No automatic comments, issue creation, merge or publication; inspect failure-report defaults too |
| Budget | Agree finite runtime, retry and model-usage limits before dispatch |
| Replay | Match repository, source revision and topic to existing work before creating another output |

The engine should read and edit only the declared area. GitHub mutation belongs
to a bounded output handler, with actual generated permissions reviewed. A topic
string, retrieved page or issue body remains data; it cannot add permissions or
override accepted decisions.

## Turn the recipe into a runnable workflow

1. Identify the target repository, selected engine, available authentication and
   finite run budget from the task. Read existing workflow conventions.
2. Fill the design record and write Markdown source using syntax supported by
   the chosen compiler. Resolve imported files and agent references.
3. Compile and inspect generated YAML, including pins, all output types,
   permissions, network access, custom jobs and timeouts.
4. Test clean, no-change and missing-input cases with supported staged outputs
   where authorized. Staging can still run model calls and custom steps.
5. Run the authorized delivery path and verify exact run revision, handler
   result and resulting artifact. Report any untested boundary.

No compiler available means the result remains a design. Missing engine access
means compilation can be verified but runtime cannot. Avoid enabling a workflow
that claims these checks passed when they were not run.

## Research basis

The inspected
[gh-aw writer workflow](https://github.com/asw101/gh-aw/blob/bc153047bde1afe62da5cd4bf03a9dc607d79c7d/.github/workflows/technical-doc-writer.md)
connects its writer profile, documentation skill, build checks and separate
safe outputs. This recipe adapts that pattern without importing its Astro
assumptions, schedule catalog or nondraft/comment defaults. Use current
[safe-output documentation](https://github.github.com/gh-aw/reference/safe-outputs/)
and the selected compiler for actual configuration.
