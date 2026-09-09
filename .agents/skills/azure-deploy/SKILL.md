---
name: azure-deploy
description: Deliver an already-prepared Azure change using current validation evidence, the existing deployment path and an authorized target. Use for requested Azure deployment, rollout, recovery or delivery handoff; preparation alone does not trigger deployment.
---

# Deliver a prepared Azure change

[release-delivery](../release-delivery/SKILL.md) remains the general artifact and
release coordinator; this procedure supplies the Azure execution phase. Reuse
valid preparation and evidence rather than forcing an unchanged project through
new scaffolding.

1. Read the plan, target configuration and
   [validation evidence](../azure-validate/SKILL.md). Compare the current artifact,
   parameters and target with the validated inputs; resolve relevant drift.
2. Follow [delivery](references/delivery.md) to execute the existing deployment
   path within the task's authorization. If a consequential action exceeds it,
   first make the proposed change, target and impact reviewable.
3. Record outcomes as they occur in
   [the deployment record](assets/deployment-record.md), including partial failure.
   Verify the critical user path and dependencies before calling the service live.
4. Hand over deployed identity, evidence, known issues, recovery instructions and
   operational ownership. Do not infer permission to delete old resources, expand
   the region, change access or activate a schedule from a deployment request.

If the required provider or live access is unavailable, finish useful local
delivery preparation and report the specific blocker. Never report a generated
workflow or local simulation as a completed Azure deployment.
