---
name: "tool-integration"
description: "Implement or repair model-provider, agent-tool and MCP boundaries with explicit schemas, data flows and failure behavior; use for integrations, timeouts, retries and tool side effects."
---

# Integrate a provider or tool boundary

1. Trace the existing caller, handler, transport and side effect. Read the
   selected SDK/protocol's current official documentation for the actual version
   in the project. Record effective inference, embeddings, memory, evaluation and
   telemetry destinations separately in
   [the boundary contract](assets/boundary-contract.md).
2. Define inputs, validation, outputs and machine-distinguishable failures.
   Record identity, permitted resources, side effects and the caller's completion
   signal. A successful tool response must match the actual resource or artifact
   changed; inspect workspace synchronization when execution is remote.
3. Choose timeouts, cancellation and retry behavior from the operation's semantics.
   Bound every retry path by attempts and elapsed time. Retry only eligible
   failures, respect provider guidance and establish idempotency before retrying
   a possibly completed write. Do not convert provider errors into quality scores
   or conceal a partial result as complete.
4. Implement the smallest adapter in the existing architecture using
   [clean-code](../clean-code/SKILL.md). Keep consequential I/O explicit and
   configuration inspectable. Use the selected host's supported schema; a prompt
   naming a tool or filesystem boundary does not enforce that boundary.
5. Exercise relevant cases in the boundary contract with the project's harness.
   Check pure validation/error mapping locally and the actual integration when
   the task authorizes it. For stdio MCP, verify protocol-only stdout and route
   diagnostics to stderr; test initialization and the chosen transport behavior.
6. Record observed requests/results, exact effective configuration, artifact
   identity and limits of substitutes. Link model behavior checks to
   [ai-evaluation](../ai-evaluation/SKILL.md), and recovery behavior to
   [operations](../../../docs/operations.md).

Credentials, external tools and paid runtimes are configured only for an actual
task need under existing authorization. This skill's availability grants no new
permissions and does not install a server.

Sources: [MCP transport contract](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports),
[John Papa integration observations](../../../docs/research/repository-inventory/johnpapa-notes.md),
and [nanochat execution-boundary tests](https://github.com/karpathy/nanochat/blob/92d63d4e8bb4df75c3b71618f31ddde2378b2bcd/tests/test_execution.py).
The latter illustrate failure testing, not adversarial process isolation.
