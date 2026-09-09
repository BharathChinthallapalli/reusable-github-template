# 0003: Share portable file checks between Git and CI

Status: Accepted
Date: 2026-09-09

## Context and alternatives

Instructions cannot ensure that a contributor checks the staged commit. Custom
shell hooks would require maintaining file parsing, partial staging, installation
and platform behavior. Host lifecycle hooks depend on the selected agent client.
CI alone gives feedback after upload. These mechanisms have different boundaries.

## Decision

Use development-only pre-commit 4.6.2 and the SHA-pinned upstream hook collection
in [.pre-commit-config.yaml](../../.pre-commit-config.yaml). Use its built-in
filename rejection hook instead of a custom scanner. Share that configuration
with an independent all-files invocation in the existing `Repository checks`
job. Keep the default source checks read-only and install hooks explicitly per
clone. Preserve the stack-neutral initializer and metadata validation from
[0002](0002-validate-ai-metadata.md); this decision adds a separate Git boundary.

The runner and collection use MIT licenses:
[runner](https://github.com/pre-commit/pre-commit/blob/v4.6.2/LICENSE),
[hooks](https://github.com/pre-commit/pre-commit-hooks/blob/3e8a8703264a2f4a69428a0aa4dcb512790b2c8c/LICENSE).
Dependency resolution also installs transitive packages; the upstream source
pin and top-level requirements are not a complete transitive lockfile.

## Consequences and evidence

Initial environment preparation needs network access and cache space. Existing
51 unit tests stay in the offline lane; real Git integration has its own explicit
lane in CI. It tests rejection, exit status, partial staging and installation
behavior. Retest on upgrades and keep documentation aligned with actual versions.

The one-MiB threshold is a visible starter policy, not a universal application
limit. The [hook guide](../git-hooks.md) records LFS exemptions, limited secret
detection, recovery patches and installation collisions. Local checks are
bypassable and editable; CI is enforcement only with configured server rules.
No hooks grant tool permissions or start agents. Revisit this choice if measured
latency, false positives or the selected application's tooling require a change.
