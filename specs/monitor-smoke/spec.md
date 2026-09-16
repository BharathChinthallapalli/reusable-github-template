# Rendered specification: monitor-smoke

<!-- source-sha256: {"intent/monitor-smoke/intent.md":"60916b6b917b2234208154455377d539e21ca8b0e75cc187bf48502338591f16","specs/monitor-smoke/design.md":"095e743638cd628b1a0bacd3a2ab608181e374be2109adeac8e0b2b967a577c2","specs/monitor-smoke/requirements.md":"fd207a6cf8e9f081d26a5c5d6579e5b0cadcf4278268c860e2e675fc4ade27f4","specs/monitor-smoke/tasks.md":"51b8626914c8806a76922297d33b61414e1380b5bea604582016ae88be9a2fc7"} -->

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


---
{
  "schema_version": 1,
  "kind": "design",
  "id": "monitor-smoke",
  "compliance": {
    "ai_act": {
      "applicability": "not_applicable",
      "reason": "Synthetic offline template fixture; no deployed AI system, personal data, employees or regulated entity is evaluated.",
      "owner": "Fixture maintainer; project adoption requires a fresh assessment."
    },
    "gdpr": {
      "applicability": "not_applicable",
      "reason": "Synthetic offline template fixture; no deployed AI system, personal data, employees or regulated entity is evaluated.",
      "owner": "Fixture maintainer; project adoption requires a fresh assessment."
    },
    "betrvg": {
      "applicability": "not_applicable",
      "reason": "Synthetic offline template fixture; no deployed AI system, personal data, employees or regulated entity is evaluated.",
      "owner": "Fixture maintainer; project adoption requires a fresh assessment."
    },
    "nis2": {
      "applicability": "not_applicable",
      "reason": "Synthetic offline template fixture; no deployed AI system, personal data, employees or regulated entity is evaluated.",
      "owner": "Fixture maintainer; project adoption requires a fresh assessment."
    }
  },
  "concerns": []
}
---
# Synthetic design

## Architecture
Local read-only command evaluates explicitly supplied JSON; no external service.

## Data flows
Explicit bands and sample -> finite/freshness validation -> JSON proposal on stdout.

## Threat model
Reject stale, future, non-finite and unknown inputs; untrusted source claims never grant authority.

## Compliance
Reasoned N/A for the synthetic fixture. Adoption requires its own assessment.

## Cost model
Offline CPU only; no model, Azure subscription, secrets or per-request service cost.

## Well-Architected
Reliability: deterministic fixtures. Security: proposal only. Cost: bounded input. Operations: clear errors. Performance: no network.

## API contract
Local JSON input/output contract; no HTTP endpoint, so OpenAPI is reasoned N/A.

## Data model and migrations
Versioned fixture schema; no persisted user database or migration.

## Auth matrix
No identity, tenant call, login or privileged operation; production identity is not simulated.

## Performance budgets
At most 100 explicitly named metrics and 512 KiB input; no throughput claim without measurement.

## Accessibility and i18n
CLI JSON fixture, no user web interface; web-app adoption must supply WCAG2.2AA and de/en design.
