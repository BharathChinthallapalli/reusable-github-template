---
name: "repo-discovery"
description: "Trace an unfamiliar repository's entrypoints, dependencies, behavior and boundaries before explaining its architecture or planning a change."
---

# Discover the repository

1. Read applicable repository instructions, README and project context. Record
   the revision inspected and distinguish committed content from local edits.
2. Inspect manifests, lockfiles, runtime configuration, CI and directory layout
   as text. Do not run manifest scripts or install dependencies merely to inspect
   the repository. A tools directory alone does not establish the app stack.
3. Locate the entrypoint relevant to the user's task: route, command, worker,
   event handler or workflow. Follow its actual calls to state and side effects.
4. Use [the evidence guide](references/evidence.md) for a focused trace and
   confidence labels. Separate declared dependencies from observed use.
5. Explain the behavior and constraints with paths and symbols. Identify the
   smallest likely change boundary, open questions and the checks that cover it.

Inspect deployed resources only when the task requires it and existing access
allows it. Configuration names are not proof that resources exist or are live.
Use current official documentation for version-dependent platform behavior;
state when documentation cannot be checked. Apply
[clean-code guidance](../clean-code/SKILL.md) when proceeding to implementation.
