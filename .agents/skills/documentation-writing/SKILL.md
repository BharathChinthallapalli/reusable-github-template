---
name: documentation-writing
description: Write or repair developer documentation, onboarding guides, technical references and explanations from repository evidence, then verify the reader's actual task. Use for substantive documentation work; use write-adr for decision records.
---

# Write documentation readers can use

Identify the reader, their starting knowledge, the task and the intended result.
Read the relevant implementation, manifests, accepted decisions and existing
documentation before selecting claims or commands. Preserve the requested format
and the repository's publishing system; do not add a docs framework to write a page.

Choose the page's job: first successful learning task, practical how-to, technical
reference, or explanation. Keep one canonical home for each contract and link to
it from other pages. For a substantial page or migration, read
[writing and verification](references/writing-and-verification.md) and adapt the
[documentation plan](assets/documentation-plan.md); a wording fix needs neither
a separate plan nor a full onboarding run.

Draft with concrete prerequisites, real paths and detected versions. Show
expected results for commands and the recovery for a relevant likely failure.
Differentiate observed behavior from intended behavior and unverified assumptions.
If implementation contradicts an accepted contract, report the discrepancy and
resolve it within the task; do not silently document a bug as the new contract.

Verify changed claims at their consumer boundary. Run the project's available
documentation checks and authorized reader commands in a disposable environment.
For a rendered site, inspect the affected page/navigation at the relevant viewport.
No renderer means Markdown/link review, not a fabricated browser result. Do not
execute a deployment or destructive example merely because it appears in a guide.

Return the actual edits, command/reader evidence and any untested environments.
Publication follows the existing task authorization; a documentation request
does not itself require a new website or public announcement.
