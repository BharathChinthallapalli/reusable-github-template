# Prepare release notes

Reusable procedure for `/release-notes`. Invocation syntax and availability
depend on the client; see [command setup](../README.md).

## Input and scope

Use the requested release identifier and comparison range. Inspect release
conventions, existing notes, tags and relevant changes. If the repository has
no Git history, work from an explicit supplied change set and disclose that
limit. Do not invent commits, a previous release or release status.

## Procedure

1. Resolve the base and target to exact commit identities when Git is available;
   state the range in the working record. A moving branch name is not sufficient
   provenance. If no range was supplied, identify the latest relevant published
   release as a proposed base and the requested target; if a reliable comparison
   cannot be established, draft from known changes and ask only for the missing
   range. Keep uncommitted work separate from a committed release candidate.
2. Read the relevant diff, merged PR descriptions and decision/migration records.
   Confirm what changed rather than copying every commit subject. Identify
   user-visible additions, fixes, incompatible behavior, configuration changes,
   deprecations and required migrations. Group related implementation commits
   into one useful outcome using the project's release categories.
3. Explain each noteworthy change in terms of its effect on users or maintainers.
   Include actionable migration steps and compatibility limits with supporting
   paths or links. Exclude secrets, private incident details and unverified
   security claims. Do not turn internal refactoring into a new product feature.
4. Check claims against evidence for this candidate: test results, artifact
   identity and deployment/release status. Separate verified fixes from known
   limitations and distinguish a prepared artifact from a published release or
   healthy deployment. Do not claim passing checks from another revision.
5. Create or update the requested notes file or draft using existing conventions.
   Use the [release changes record](../../.agents/skills/release-notes/assets/release-changes.md)
   to preserve the range, included evidence and gaps for a substantial release.
   Summarize changes, migration actions and known issues; avoid empty categories.

## Delivery boundary

Return the prepared notes and their comparison range, with any missing evidence
that affects a claim. Writing notes does not create a tag or GitHub release.
When publication or deployment is already part of the user's authorized task,
continue through [release delivery](../../.agents/skills/release-delivery/SKILL.md)
and verify the exact artifact. Send release announcements or other messages only
when explicitly authorized.
