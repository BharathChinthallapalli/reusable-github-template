---
{
  "schema_version": 1,
  "kind": "requirements",
  "id": "change-name",
  "requirements": [
    {
      "id": "R-1",
      "story": "As an affected user, I need a measurable outcome.",
      "acceptance": "When the documented trigger occurs, the system shall produce the documented observable outcome.",
      "verification": [
        "tests/test_change.py"
      ]
    }
  ]
}
---
# Requirements

Use EARS: The system shall…; When/While/Where condition, the system shall…;
If unwanted condition, then the system shall…. Each criterion must be binary
testable; grammatical shape alone does not establish quality. Test/eval references
must exist before the strict rendering gate. Author a test skeleton or an approved
test-design record through the appropriate protected-path review, not a fake pass.
