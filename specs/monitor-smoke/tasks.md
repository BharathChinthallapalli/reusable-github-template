---
{
  "schema_version": 1,
  "kind": "tasks",
  "id": "monitor-smoke",
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
        "src/monitor.py"
      ],
      "acceptance": "When a fresh latency sample reaches three standard deviations above its baseline, the monitor shall propose an intent without executing a command.",
      "done": "The synthetic breach returns tier three and a proposal with no execution tools.",
      "verification": [
        "tests/test_sdlc.py"
      ]
    }
  ]
}
---
# Synthetic build plan

No real issue, PR, human acceptance or merge is claimed.
