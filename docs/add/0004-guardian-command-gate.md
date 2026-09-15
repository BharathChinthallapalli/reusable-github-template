---
schema_version: 1
id: ADD-0004
status: ready
scope:
- .guardian/engine/policy.py
- .guardian/engine/ledger.py
- .guardian/engine/gate.py
- .guardian/engine/issuer.py
- .guardian/adapters/dispatch.py
- .guardian/adapters/copilot.ps1
- .guardian/adapters/claude.ps1
- .guardian/adapters/codex.ps1
- .guardian/requirements.txt
- .guardian/ledger.schema.json
- .guardian/policy.json
- .guardian/profiles/copilot-cli.json
- .guardian/profiles/claude-managed.json
- .guardian/profiles/codex.rules
- .guardian/profiles/copilot-denies.json
- .github/hooks/guardian.json
- .github/agents/guardian.agent.md
- .github/instructions/never-do.instructions.md
- .claude/settings.json
- .claude/agents/guardian.md
- .codex/agents/guardian.toml
adrs:
- docs/adr/0011-guardian-command-gate.md
binding_sha256: 00a8c5893c18e172566a8a2a1b9fd1b527e1cdea36e29eb451444cd9cb7fe2e8
---
# Guardian command gate

## Purpose

Require explicit four-answer review before supported in-scope commands and
refuse prohibited endpoint and cloud operations independently of the reviewer.

## Scope and non-goals

One engine and three adapters share policy and ledger contracts. This repository
does not configure an actual Windows security boundary, sign production scripts,
provision an identity, or guarantee that no Defender or Sentinel alert occurs.

## Inputs and outputs

Inputs are bounded host envelopes, exact commands, workspace roots, verified
approval signatures and ledger history. Outputs are host-native denial or normal
permission-flow continuation, with chained audit records and explicit reasons.

## Capabilities and permissions

The current task authorizes implementation and synthetic tests. The guardian
has read tools plus a dedicated approval issuer; it cannot execute commands.
Production signing keys require a separate identity and protected service. The
worker has no authority to install keys, weaken policy or configure its issuer.

## Behavior and failure modes

Parse shell syntax with tree-sitter, reject unsupported effects and apply hard
denials before tokens. Bind signed approvals to exact requests and expiry.
Lock and verify the ledger; ledger failure denies. Track same-session follow-ups
and recent cross-runtime pivots. Host timeouts may fall through independently of
engine decisions. File-tool and alternate execution paths require coverage tests.

## Validation

Run parser, protocol, signature, replay, corruption, concurrency and pivot tests
with synthetic commands only. Record timings and precise coverage. Native CLI,
Windows extension and Defender observations remain explicitly untested when
unavailable; fixture replay never substitutes for installed-runtime acceptance.

## Risks and alternatives

Mutable hooks, same-user signing keys and local ledger truncation are not secure
boundaries. Managed deployment and external checkpoints are prerequisites for
stronger claims. Offline local files cannot form a durable shared cloud ledger.
Conservative unsupported-command denial can limit productivity until reviewed
command families are added with behavioral tests.
