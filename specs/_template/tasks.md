---
{
  "schema_version": 1,
  "kind": "tasks",
  "id": "change-name",
  "status": "proposed",
  "tasks": [
    {
      "id": "T-1",
      "requirements": [
        "R-1"
      ],
      "depends_on": [],
      "wave": 1,
      "surface": [
        "src/change.py"
      ],
      "acceptance": "When the documented trigger occurs, the system shall produce the documented observable outcome.",
      "done": "The requirement is implemented and demonstrated by independently reviewed verification.",
      "verification": [
        "tests/test_change.py"
      ]
    }
  ]
}
---
# Build plan

One issue is one contract. Map each task to requirement IDs and an issue; waves
execute sequentially, with independent tasks eligible for isolated branches.
Record issue ownership to prevent duplicate Copilot/engineer dispatch. A local
status change to accepted is not authenticated product-owner approval.

Tests and evals are protected: the junior worker proposes necessary changes for
human-authorized handling and may not weaken checks to make its implementation pass.
Before each dispatch, revalidate head/base, acceptance, dependencies, unclaimed
task, provenance, Guardian and change budget.
