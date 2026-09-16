---
{
  "schema_version": 1,
  "kind": "design",
  "id": "change-name",
  "compliance": {
    "ai_act": {
      "applicability": "requires_assessment",
      "reason": "Record system-specific scope, role and applicability before admission.",
      "owner": "Assign the accountable policy owner."
    },
    "gdpr": {
      "applicability": "requires_assessment",
      "reason": "Record system-specific scope, role and applicability before admission.",
      "owner": "Assign the accountable policy owner."
    },
    "betrvg": {
      "applicability": "requires_assessment",
      "reason": "Record system-specific scope, role and applicability before admission.",
      "owner": "Assign the accountable policy owner."
    },
    "nis2": {
      "applicability": "requires_assessment",
      "reason": "Record system-specific scope, role and applicability before admission.",
      "owner": "Assign the accountable policy owner."
    }
  },
  "concerns": [
    "Resolve named policy-owner and technical concerns."
  ]
}
---
# Design

## Architecture
Boundaries, dependencies, deployment view and current ADD/ADR references.

## Data flows
Sequence diagram, input/output schemas, classifications, tenant/region crossings,
data subjects, storage, retention and deletion.

## Threat model
STRIDE assets, entry points, attackers, existing controls, residual risks and owners.

## Compliance
Repeat the assessed intent metadata. Map applicable requirements to controls,
evidence and accountable people; use reasoned N/A where appropriate.

## Cost model
Unit economics, traffic/volume, token/compute/storage/network assumptions,
dev/test/prod estimates, failure/retry costs, budget and sensitivity analysis.

## Well-Architected
Reliability, security, cost, operational excellence, performance. C/D also evaluate
the AI workload checklist using fetched current Microsoft documentation.

## Archetype sections
Insert every mandatory heading for each selected archetype from specs/archetypes.
This placeholder is deliberately not accepted by the renderer.
