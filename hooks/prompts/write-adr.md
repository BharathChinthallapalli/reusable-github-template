# Write an architecture decision record

Reusable procedure for `/write-adr`. Invocation syntax and availability depend
on the client; see [command setup](../README.md).

## Input and scope

Use the proposed decision, the problem it resolves, and the affected repository
area. Read [project context](../../docs/project.md), relevant code, and the
[ADR conventions and index](../../docs/adr/README.md). A routine implementation
detail does not need an ADR unless the user requests one or its consequences
justify a maintained decision.

## Procedure

1. Identify the decision boundary and evidence: current behavior, constraints,
   affected consumers and observable acceptance criteria. Separate observed
   facts, agreed requirements and assumptions. Use the optional
   [decision evidence record](../../.agents/skills/write-adr/assets/decision-evidence.md)
   when competing claims need a traceable working record.
2. Read relevant ADR statuses and supersession links before treating a choice
   as binding. Resolve conflicts through scope and evidence; a later timestamp
   alone does not override an Accepted decision. Inspect viable alternatives,
   including keeping the current behavior, and identify what would disprove
   the preferred choice. For a material design, follow the repository's design
   review procedure and carry resolved findings into the rationale.
3. Choose the next unused number after inspecting `docs/adr/`; check again
   immediately before writing when other contributors are active. Create
   `docs/adr/NNNN-short-title.md` from the canonical
   [ADR template](../../docs/adr/template.md). Keep its structure; do not maintain
   a second ADR template in this skill.
4. Write a specific title, decision date, context, viable options, choice and
   rationale, costs, introduced failure modes, migration/recovery and the
   condition for revisiting the decision. Link code and sources that support
   the claims; label version-dependent or unverified claims. Describe how the
   intended outcome will be checked.
5. Use Proposed status unless the task or recorded decision process already
   establishes acceptance. An implementation or drafted ADR alone does not
   establish that a decision was accepted. For an accepted replacement, update
   both supersession links and the old status together; do not supersede an
   accepted record merely because its proposed replacement exists. Update the
   decision index and inspect local links.

## Result

Return the ADR path and status, the decision it captures, key trade-offs and
any specific unresolved question. Preserve existing authorization and continue
the user's requested implementation when its decision gate is satisfied;
writing the ADR is not itself permission to publish, deploy or change access.
