# 0009: Adopt native tooling with independent, current verification

Status: Accepted
Date: 2026-09-13

## Context

The user requested research and implementation of native CLI improvements and
the no-mistakes repository's useful practices. Ruff already provides the
template's Python correctness checks. The source has no application bundler,
Black or Flake8 configuration to replace. Its Python tools and pre-commit still
need an interpreter, irrespective of how dependency installation is accelerated.

## Decision

Use SHA-pinned astral-sh/setup-uv with explicit uv version 0.12.13 in CI and
Copilot setup. Install the existing requirements with `uv pip install`, targeting
the Python selected by setup-python. Keep the interpreter, dependency versions,
required checks and command interfaces. Do not use sync against a shared runner
environment or infer a full dependency lock from top-level version pins.
Leave persistent caching off until measurements justify restoration overhead.
Prefer uv in local virtual-environment setup; document pip as a fallback.

Install ast-grep-cli 0.45.3 from its binary wheel in Copilot setup and check
syntax-aware matching with positive and negative examples. Require available
ast-grep for structural searches, while retaining rg for text and Semgrep for
relevant analysis. Projects may add reviewed, tested structural rules when they
have a concrete policy; no blanket TODO, print or debug-log ban is introduced.
Use the explicit `ast-grep` command to avoid Linux's unrelated `sg` executable.

Refine the existing code-review, test-design and verify-change skills with
independent review of fixes and their tests, meaningful declarative assertions,
and invalidation of affected evidence after edits. Adapt ideas in original
wording with pinned-source attribution. Keep task routing and host permissions.
No upstream daemon, Git proxy, autonomous publication or fixed review pipeline
is installed. Required local gates and the user's authorization remain valid.

## Validation and consequences

Verify fresh installation, smoke behavior, source/initialized checks and actual
CI/Copilot runs at the delivered revision. Exercise the revised guidance with
bounded synthetic cases; this is not proof of universal model effectiveness.
Report measured job/step timing with runner and cache scope. Package benchmarks
do not establish repository-wide speedups or savings.

Adding uv setup and ast-grep has download and maintenance costs. Maintain the uv
and ast-grep versions in both workflows where used, review the action pin, and
rerun the actual jobs after updates. Roll back by restoring the prior pip setup
and removing ast-grep's setup step; existing validation commands still work.
Frontend tools remain project-specific choices requiring compatibility checks
and measured builds. Rust memory safety does not promise OOM immunity, complete
RCE prevention, static linkage on every target or deterministic latency.

See [tool research](../research/native-tooling.md) and
[source adoption](../research/no-mistakes-adoption.md) for evidence and exclusions.
