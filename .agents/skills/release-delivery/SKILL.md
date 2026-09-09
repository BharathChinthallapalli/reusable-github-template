---
name: release-delivery
description: "Prepare, verify and deliver a scoped package or deployment release with artifact identity, compatibility, smoke checks and recovery evidence."
---

# Deliver a reviewed artifact

Establish the requested release target and existing authorization. Read actual
build/package/deployment entrypoints, environments and release conventions.
Use [the release record](assets/release-record.md) to identify the candidate;
prepare the concrete artifact and review evidence before any additional approval
that the target environment genuinely requires.

Build through the project's declared command and inspect what will be distributed.
Check expected entrypoints, runtime dependencies, accidental fixtures/secrets and
relevant size constraints. Run a consumer smoke check against the built package
or deployable artifact, not only the source tree. Preserve failure exit statuses
through reporting and cleanup; a successful upload cannot repair failed tests.

Bind code revision, dependencies, configuration and artifact digest. For AI/data
assets include model, prompt, corpus and evaluator identities using
[ai-evaluation](../ai-evaluation/SKILL.md). Promote the artifact actually evaluated;
avoid rebuilding a different artifact or reading an unversioned shared output.

Describe compatibility, data changes, observable readiness, rollout signals and
the recovery target before release. Use [operations](../../../docs/operations.md)
and the project's selected hosting procedure; [Azure delivery](../../../docs/azure-delivery.md)
applies only to an Azure project. Do not create cloud resources to fill a template.

Complete authorized publication/deployment, verify the delivered revision or
digest and perform the agreed smoke check. If required access or authorization is
missing, return the prepared artifact and the precise blocked action. Report
prepared, published, deployed and healthy as separate observed states.

For an Azure target, use [azure-prepare](../azure-prepare/SKILL.md) only for missing
or changed preparation, [azure-validate](../azure-validate/SKILL.md) for applicable
artifact/environment evidence, and [azure-deploy](../azure-deploy/SKILL.md) for the
authorized execution. This skill remains the delivery coordinator. Preserve
Terraform, Bicep, azd or the existing pipeline rather than converting tools to
satisfy a template. Use [operational-readiness](../operational-readiness/SKILL.md)
for the actual service handoff; a proof of value alone is not production evidence.
