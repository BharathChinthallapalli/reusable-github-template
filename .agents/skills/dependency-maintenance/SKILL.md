---
name: dependency-maintenance
description: "Upgrade dependencies, action pins or hook revisions; assess compatibility, lockfile changes and evidence before adopting an update."
---

# Maintain dependencies

Locate the dependency's actual consumers, manifest, lockfile and update mechanism.
Use [the maintenance map](../../../docs/maintenance.md) to identify coupled files.
A source pin, top-level package pin and resolved dependency closure are different
things; describe the one the project actually has.

Read the selected version's official release notes, runtime requirements and
relevant migration/security notices. Confirm repository ownership and exact refs.
Use [evidence-research](../evidence-research/SKILL.md) when current support is uncertain.
Keep the project's package manager; do not manufacture a new dependency ecosystem.

Record baseline behavior, then make the smallest coherent upgrade. Regenerate its
lockfile through the existing tool. Inspect changed transitive packages, install
scripts, optional downloads, licenses and permission changes relevant to the diff.
Do not hand-edit a lockfile to hide resolution failures or auto-merge on a badge.

Use the [upgrade record](assets/upgrade-record.md) for a consequential change.
Verify a fresh installation when resolution changed, relevant consumer behavior,
packaging/runtime compatibility and the actual CI revision. Test supported versions
the change affects; a declared matrix is not evidence that each lane executed.

For this template, keep Actions and hook references at verified full SHAs.
Dependabot updates pip and Actions; hook revisions use a reviewed
`python -m pre_commit autoupdate --freeze`. Follow [Git checks](../../../docs/git-hooks.md).
Complete with the adopted versions, compatibility changes, checks and rollback
commit. Publication follows the current task's authorization.
