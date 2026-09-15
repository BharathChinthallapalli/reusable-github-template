# 0011: Shared guardian command gate

Status: Accepted
Date: 2026-09-15

## Context

The user requires deterministic command review across three agent runtimes.
Fetched runtime contracts expose timeout, alternate-tool and mutable-hook gaps.
Agent names and writable approval files cannot authenticate a reviewer.

## Options

Instructions alone cannot enforce review. Independent policy implementations drift.
A privileged execution broker offers stronger confinement but requires managed
endpoint deployment outside this repository change.

## Decision and rationale

Use one parser-based engine, thin host adapters and a hash-chained ledger. Require
signed, expiring, single-use approvals for supported in-scope operations. Keep
signing authority outside the worker identity. Unknown syntax and unavailable
identity evidence deny. Preserve independent host permissions and Defender.
Ship deployment profiles and explicit unverified coverage, not a universal
security guarantee. See the guardian guide for fetched contracts and acceptance.

## Consequences and review

Python provides portable tree-sitter bindings; PowerShell is a thin Windows
adapter. Rust-based uv prepares pinned dependencies outside hooks. Host startup
and mutable repository configuration remain trust prerequisites. Native Windows,
VS Code and cloud coverage require separate acceptance on installed versions.
A remote collector and managed execution boundary are required for durable
cross-machine audit and timeout-independent enforcement. Revisit on runtime
contract changes or a newly supported command family.
