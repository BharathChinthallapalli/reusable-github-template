# Agent Design Documents

An ADD describes how an agent, instruction, skill or hook will behave for an
authorized task. Write or update the relevant record before protected edits.
Use [the template](template.md), read its referenced [Accepted ADRs](../adr/README.md),
and resolve concrete design conflicts before implementation.

The [design gate](../../tools/check_design.py) checks explicit scope, document
structure and delivered content. It cannot assess design quality, grant tool
permissions or certify human approval. Existing user authorization remains the
authority for work; routine edits do not require a new permission request.

## Workflow

1. Copy the template to `docs/add/NNNN-short-title.md`, assign a unique `ADD-NNNN`
   ID, and fill its seven sections with the requested outcome and repository
   evidence. Record actual authorization and relevant limits in the permissions
   section. Do not invent application decisions or reviewer sign-off.
2. List exact repository-relative file paths in `scope`, including new paths
   before they exist. Link the relevant current Accepted decisions in `adrs`.
   A new record may replace an old record's scope only after that old scope is
   removed or the old record is retired; each protected path has one ready owner.
3. Set `status: ready` when the design can guide the authorized work. Run the
   pre-edit check for the actual affected paths, then implement and verify them.
4. Reconcile the design against the finished diff and evidence. Explicitly seal
   the affected record, then run the default gate before delivering the change.
   Reviewers assess whether the narrative and scope accurately describe the work.

```bash
python3 tools/check_design.py --paths .github/agents/engineer.agent.md
python3 tools/check_design.py --seal docs/add/0001-template-agents-and-hooks.md
python3 tools/check_design.py
```

All commands accept `--root PATH` for an alternate repository directory. They
return zero on success and nonzero on rejected input or failed checks. `--paths`
and `--seal` are mutually exclusive. Only `--seal` writes a file; invalid input
leaves the target unchanged and successful sealing preserves its status.

## What each mode checks

| Mode | Required result | Content drift |
| --- | --- | --- |
| `--paths PATH...` | Valid records, current Accepted ADR references, and exactly one ready ADD for each supplied protected path | Allowed while implementing; this is the pre-edit planning gate |
| Default, no mode flag | The same structural checks, every existing protected file covered by exactly one ready ADD, and matching bindings for every ready ADD | Rejected before delivery and in CI |
| `--seal ADD` | Structurally valid records and target, no ambiguous ready scope; record the target's current binding | Recorded explicitly without changing status or implying approval |

The pre-edit gate can cover a missing file because creation must be planned.
It does not require unrelated current paths to be covered during an incremental
design migration. The default gate does require complete current coverage.
Renames require planning both paths; deletions change the old path to an absent
state and require resealing. All modes reject malformed record metadata.

## Record contract

| Field | Contract |
| --- | --- |
| `schema_version` | Integer `1` |
| `id` | Unique string in `ADD-0001` form |
| `status` | `draft`, `ready`, or `retired`; only ready records cover edits |
| `scope` | Explicit file paths; nonempty for ready records; no globs, traversal, directories or symlinks |
| `adrs` | Explicit numbered files directly under `docs/adr`; nonempty and currently Accepted for ready records |
| `binding_sha256` | Empty while preparing a record, or the digest written by `--seal`; ready delivery requires a matching digest |

`README.md` and `template.md` are guidance, not records. Every other Markdown
file directly under `docs/add` is parsed as a record. Unknown frontmatter keys,
duplicate YAML keys, duplicate IDs and duplicate scope entries fail. Draft and
retired records retain valid metadata and ADR paths but need not have completed
sections or current bindings. They never authorize coverage.

Ready records require filled `Purpose`, `Scope and non-goals`, `Inputs and outputs`,
`Capabilities and permissions`, `Behavior and failure modes`, `Validation`, and
`Risks and alternatives` sections. Empty text, comment-only or code-only content,
and obvious `TODO`/`TBD`/`FIXME` placeholders fail. This is a minimum structural
check; plausible filler still needs review.

The SHA-256 binding covers canonical metadata excluding the digest itself, the
ADD narrative, explicit scope file contents, and referenced ADR contents. Absent
files have a distinct marker. UTF-8 content normalizes CRLF to LF; other bytes
are hashed unchanged. It does not use Git history, timestamps or network access,
so ZIP consumers can run the same check. Do not list `docs/add` files in scope:
each record already binds its own design, and cross-record bindings could cycle.

## Protected files

All files and assets under `.agents/skills/`, `.github/agents/`,
`.github/instructions/`, `.github/hooks/` and `hooks/` are protected. The following
individual paths are also protected:

- `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, `.codex/hooks.json`
- `tools/check_design.py`, `tools/install_hook_tools.py`, `tools/check_ai_configuration.py`
- `.pre-commit-config.yaml`, `ruff.toml`, `.gitleaks.toml`, `requirements-dev.txt`, `.gitignore`
- `.github/workflows/ci.yml`, `.github/workflows/copilot-setup-steps.yml`

The checker owns this path list. Adding a protected file requires explicit
scope; an old directory-wide design never covers future files automatically.
Automatic discovery excludes regular `.pyc` and `.pyo` files beneath
`__pycache__` directories, so importing a hook does not create an unplanned
implementation change. This exclusion never follows symlinks or hides source
files, other file types, or bytecode outside a cache directory. Keep generated
bytecode out of ADD scope. Explicit `--paths` requests still check their exact
paths, including paths inside cache directories.
Ordinary application paths and unrelated documentation do not require an ADD.
For a material project agent outside these locations, extend the path policy
and its tests in the same reviewed design change.

## Index

| Record | Status | Purpose |
| --- | --- | --- |
| [0001: Template agents and hooks](0001-template-agents-and-hooks.md) | Ready | Current shared procedures, explicit design gate, local hook policy and validation boundaries |

Sealing demonstrates matching content, not compliance with every sentence. A
ready record is editable and is not an authenticated approval. Host hooks and
local commands are also editable; required CI and review need server settings
that are configured separately. See [ADR 0005](../adr/0005-scoped-agent-design-gate.md).
