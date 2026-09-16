---
{
  "schema_version": 1,
  "kind": "requirements",
  "id": "monitor-smoke",
  "requirements": [
    {
      "id": "R-1",
      "story": "As a template adopter, I need a reproducible proposal-only monitor.",
      "acceptance": "When a fresh latency sample reaches three standard deviations above its baseline, the monitor shall propose an intent without executing a command.",
      "verification": [
        "tests/test_sdlc.py"
      ]
    }
  ]
}
---
# Synthetic requirements

The criterion is verified by deterministic local tests, not live Azure telemetry.
