# 0005: Bind agent and hook changes to explicit designs

Status: Accepted
Date: 2026-09-09

## Context

The requested template layout distinguishes `docs/adr` decisions that agents
must respect from `docs/add` Agent Design Documents that gate their work. It
also adds pre-tool restrictions, post-edit checks, and reusable hook prompts.
Existing instructions explain good behavior but cannot establish that a
particular agent or hook implementation matches a completed design.

## Options

- Keep instructions alone: easy to maintain, but an empty or unrelated design
  could appear to satisfy the request without covering the files being edited.
- Require human approval for every edit: adds a new authorization rule even for
  routine work that the user has already authorized.
- Require explicit design scope and a content binding: makes missing design,
  incomplete structure, uncovered paths and stale delivered content detectable
  while leaving semantic review and task authorization with their existing owners.

## Decision

Use [Agent Design Documents](../add/README.md) with explicit file paths, current
Accepted ADR references, and filled behavior, permission and validation sections.
`draft` and `retired` records cannot cover protected edits. `ready` means that the
design is complete enough to guide the authorized task and be reviewed; it is
not an approval signature or permission grant.

Use the existing development-only safe YAML parser from
[0002](0002-validate-ai-metadata.md). A pre-edit `--paths` check validates the
ready design and exact scope while allowing implementation drift during work.
The independent default check requires every current protected file to have
exactly one ready design and every ready design's binding to match its scope,
its own narrative and metadata, and referenced ADR content. Add no glob-based
standing exemptions. Future paths can be planned explicitly before creation;
deleted paths retain a distinct absent state until scope is deliberately revised.

An explicit `--seal` operation records the current content fingerprint without
changing design status or claiming approval. It runs after the design and diff
have been reconciled under the task's existing authorization. Protect the checker,
hook policy, host adapters and CI entrypoints as well as agent and skill files.
The [gate contract](../add/README.md) is the authoritative path and command guide.

## Consequences and review

Content changes require reconciling the affected design and resealing before
delivery. This is intentional drift detection, including for small protected
edits; ordinary application code and unrelated prose do not require an ADD.
Text bindings normalize CRLF so checkout line endings alone do not fail the gate.

The checker can reject missing sections and obvious placeholders. It cannot
determine whether prose is truthful, a design is safe, or the task authorizes an
operation. A contributor can edit the checker or reseal content, so independent
review and configured server rules remain necessary where enforcement matters.
Host hooks remain best effort and client-dependent; passing this gate does not
prove a host loaded them or prevent unrestricted shell writes.

Verify planned-path success, uncovered-file rejection, non-ready rejection,
accepted-decision references, content drift, safe path handling and failed seal
preservation with `python3 -m unittest discover -s tests -p test_design.py -v`. Revisit this choice
if explicit scope maintenance becomes disproportionate, host event inputs change,
or the project needs authenticated approval instead of reviewable design records.
