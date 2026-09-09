# Architecture decisions

Use an ADR for a durable choice with meaningful alternatives and consequences.
Routine edits do not need one. Start from [the outline](template.md).

## Index

| Decision | Status | Scope |
| --- | --- | --- |
| [0001: Independent repository foundation](0001-repository-foundation.md) | Superseded | Replaced by 0002; retained as history |
| [0002: Validate AI metadata](0002-validate-ai-metadata.md) | Accepted | Shared template and development checks |
| [0003: Portable Git checks](0003-portable-git-checks.md) | Accepted | Staged commit checks and independent CI invocation |
| [0004: Portable engineering capabilities](0004-portable-engineering-capabilities.md) | Accepted | Shared skill location, expanded task workflows, catalog and offline evaluation gate |

This index is navigation. Read each relevant decision's current status and
reasoning, and compare its assumptions with repository evidence. Update the
index when a decision is added or its status changes.

## Status and changes

- Put `Status` and `Date` immediately below the title. Use exactly one status:
  Proposed, Accepted, Superseded, or Rejected. Label a review date as such if the
  original decision date is unknown.
- When a decision changes, write a new ADR describing why. Preserve the previous
  decision's reasoning; update its status metadata to Superseded and link to the
  replacement. Link back from the replacement with `Supersedes`.
- Proposed and Rejected decisions are historical or exploratory context, not
  current accepted choices. Follow supersession links to understand changes.
- If relevant Accepted decisions conflict, investigate their scope, assumptions,
  and code evidence. Do not treat the latest timestamp or this index as an
  automatic tie-breaker. Resolve a material conflict with the decision owner
  before making the affected change, then record the resolution explicitly.
