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
