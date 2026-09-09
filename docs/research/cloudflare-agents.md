# Cloudflare Agents: reusable engineering lessons

Reviewed **9 September 2026** against the public default branch `main` at
[`d5d250e8593edbebb286c0f97a05c224bd23d054`](https://github.com/cloudflare/agents/commit/d5d250e8593edbebb286c0f97a05c224bd23d054),
committed **2026-09-09 16:11:14 UTC**. This is the head observed during review,
not a promise that the branch still points there.

The GitHub recursive tree response was not truncated: **3,188 entries**, including
directories. Coverage is a selected-source review of **25 files** listed below,
with focused implementation/test excerpts for large files. It is not a complete
source or security audit. No upstream install scripts, code, tests, CI, deployment,
or paid services were executed. The MIT license was inspected (S20); this note
contains original paraphrase and links, with no upstream implementation bundled.

## Decisions for this template

| Observed evidence | Adopt in the reusable foundation | Boundary or reason |
| --- | --- | --- |
| Root instructions route readers to scoped instructions and actual package/test locations (S01). | Keep root instructions short and route agent implementation to the Agent Design Document procedure. | Do not import Cloudflare-specific preferences, package manager, Workers APIs, compatibility dates, dependencies, or approval rules. |
| Living topic designs describe current implementation; RFCs retain the reasoning and accepted/rejected outcome (S02–S04). | Keep `docs/add/` for current agent design and `docs/adr/` for decision history. Require a reviewed ADD before material agent behavior work, then reconcile it after implementation. | This template's ADD gate is a requested adaptation. Cloudflare's instructions do not establish that it has a machine-enforced ADD gate. Preserve existing decisions through an explicit migration or compatibility index. |
| Lifecycle design distinguishes startup, request, alarm, invocation context and reconstruction after hibernation (S06). | ADD records entrypoints, state ownership, initialization order, failure propagation, restart recovery and cleanup. | Do not require Durable Objects or invent a lifecycle framework for a stateless project. |
| Validation precedes persistence and broadcast; notification runs afterward (S08, S17, S22). | ADD identifies invariants and the exact pre-write validation/authorization boundary. Link checks that show rejected input has no persisted or external effect. | A notification callback cannot retroactively reject an already published update. |
| Durable approval results have explicit execution identity; stale requests do not revive settled executions (S05, S10, S14–S16). | ADD describes allowed transitions, approval scope, expiration, replay, concurrency, idempotency, and recovery checks. | Execution identity is necessary but not a complete authorization or argument-binding design. |
| The approval UI must use authoritative full arguments because transcript arguments can be truncated (S12, S14). | Bind a human decision to the concrete action, full relevant arguments, target, actor, and current action version; refresh stale requests before enabling approval. | Do not treat a model summary or truncated tool preview as the approval payload. Binding an action version is our stronger template requirement, not a claim about upstream implementation. |
| Rejection ends pending work; compensation is separate and only exists for tools with a revert operation (S10). | Runbooks distinguish cancel/reject, retry, compensation, and irreversible effects; inspect actual recorded outcomes before repeating a write. | Do not promise rollback of email, publication, payment, or other external effects merely because a workflow is durable. |
| Readonly shared-state protection does not cover SQL, HTTP entrypoints, or preceding external side effects (S11, S18, S22). | Threat model and ADD list every entrypoint and effect, with server-side identity/authorization before each protected effect. | A UI flag, prompt instruction, or state-write guard is not a general permission boundary. |
| Fetch tools define allowlisted destinations/headers, bounded responses, redirect policy, timeout and cancellation; tests exercise these policies (S23–S24). | Tool contracts and ADD declare permitted destinations, redirect handling, credentials source, size/time budgets, cancellation and expected denial behavior. | Do not copy the experimental fetch implementation or claim complete SSRF protection from URL checks alone. |
| Observability documents correlation identifiers and opt-in payload capture (S13). | ADD/runbooks specify run/action IDs, transition events, redaction, retention and an authoritative audit source. | Best-effort telemetry is not a durable audit ledger; lifecycle design explicitly requires an outbox where guaranteed delivery matters (S06). |
| Coverage matrix maps behaviors to test layers and distinguishes intentional live-service gates from disabled test debt (S07). | For material agent changes, map each required invariant to test file, command, CI job, evidence and known gap. | Test presence or a documentation check is not evidence that application behavior passed. |

## Agent Design Document additions

Use these prompts only where relevant to the actual agent:

- **Outcome and scope:** intended user, observable success, non-goals, permitted
  autonomy, and the simplest non-agent alternative.
- **Execution contract:** triggers, state transitions, durable/transient data,
  schema version and migration, retry owner, idempotency keys, replayed versus
  repeated effects, deadlines, cancellation, recovery and deletion.
- **Tool and approval contract:** caller identity, tool input/output schema,
  resources and network destinations, authorization enforcement, concrete review
  payload, action version, approval expiry, concurrent decisions and compensation.
- **Evidence and operations:** behavior-to-test/CI mapping, quality and resource
  budgets, useful correlation IDs, redaction/retention, runbook link and owner.

A reviewed ADD documents a decision; it does not prove authorization,
implemented runtime enforcement, successful tests or production readiness.
The repository gate should check the required record and review state while
application tests and host controls provide their own evidence.

## Runbook additions

For interrupted or awaiting-approval execution:

1. Identify the environment, run/action ID, current durable status and last
   confirmed effect. Separate missing telemetry from an absent side effect.
2. Inspect pending actions through the authoritative server record and check
   authorization, current arguments and expiry. Reconcile already completed,
   rejected or superseded requests instead of replaying a stale approval.
3. Choose the documented recovery transition. Retry only when the idempotency
   contract makes duplicate effects safe; otherwise reconcile with the external
   system first.
4. Apply compensation only where supported, record remaining irreversible effects,
   and verify the final user-visible and durable state.
5. Capture redacted evidence, root cause, recovery result and the design/test
   changes needed to prevent recurrence.

For missing guardrails, record host/version, discovered hook configuration,
event/input shape, command result and the independent CI fallback. These checks
diagnose whether hooks execute; they do not imply that a hook is a sandbox.

## Concrete limits and drift found

**The coverage prose and workflow disagree at this same commit.**
S07 describes codemode browser tests and the agents browser connector suite as
unwired nightly proposals. S25 already defines `e2e-codemode`,
`e2e-codemode-llm`, and a browser job running `pnpm run test:browser`.
Use the consuming workflow as configuration evidence, and reconcile design
matrices when wiring changes. No CI run was inspected to establish pass/fail.

S19 ignores `design/**` changes for its pull-request workflow and references
actions by version tags. Do not copy that trigger filter into this template's
required design gate, and retain the template's existing immutable action pins.
Its PR workflow also publishes package previews; that behavior is unsuitable for
a language-neutral repository foundation.

S14 includes an in-memory-handle-loss recovery test. S17 obtains another stub
for persistence checks, and S18 reconnects clients for readonly checks. Those
particular assertions do not establish full process eviction or a successful
deployed restart. Describe each test's actual failure mechanism.

The durable execution/HITL bridge and fetch surface reviewed here are explicitly
experimental (S05, S23). Their concepts can inform contracts without adopting
their APIs. Likewise, pre-tool secret/destructive-command guards, post-edit
Ruff/Gitleaks checks, and the requested `/triage-issue`, `/write-adr`,
`/release-notes` prompts are **requested template adaptations**, not practices
this review claims to have found in Cloudflare. They still need host-specific
configuration, their own tests, and clear enforcement limits.

## Pinned source ledger

Blob hashes below are Git object SHA-1 identifiers returned by GitHub, not
release signatures or locally computed SHA-256 digests. Every link resolves
against the same commit; the recursive inventory used that commit as its ref.

| ID | Exact source path | Git blob SHA |
| --- | --- | --- |
| S01 | [AGENTS.md](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/AGENTS.md) | `7450d93b73435348507af12dcb6770cdbfa06be1` |
| S02 | [design/AGENTS.md](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/design/AGENTS.md) | `85f5df9ccff76ddf826718dd3fb444695229dccb` |
| S03 | [design/README.md](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/design/README.md) | `ac23593c542b31cbb9c4bbb003f5a914f3106fd4` |
| S04 | [docs/AGENTS.md](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/docs/AGENTS.md) | `a39089b19ea6e2ba2101acbf5ce12f5858700340` |
| S05 | [design/think-execute-hitl.md](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/design/think-execute-hitl.md) | `dafac7486aae9675adc920d9e9a56119d865f0c2` |
| S06 | [design/durable-object-lifecycle.md](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/design/durable-object-lifecycle.md) | `d96a61b9ef816dcef0587fabe88800870d9a9160` |
| S07 | [design/test-coverage-matrix.md](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/design/test-coverage-matrix.md) | `778af6f0f7724b309dc137ae76c54a2ab2f6cf7c` |
| S08 | [docs/agents/state.md](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/docs/agents/state.md) | `e02fe49075462a8ba22b3af275943a7aa1c97a47` |
| S09 | [docs/agents/human-in-the-loop.md](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/docs/agents/human-in-the-loop.md) | `59fbd078920deb44c2db3695bb127b525f1537df` |
| S10 | [docs/codemode/approvals.md](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/docs/codemode/approvals.md) | `9641aba830e0b99f07fba60f53e2ef060d18a4ab` |
| S11 | [design/readonly-connections.md](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/design/readonly-connections.md) | `c4d9a4c9b83fd51c75c30ec788277d8756a4a5eb` |
| S12 | [docs/think/tools.md](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/docs/think/tools.md) | `63e478abdc0973a444d46a0ef0eabf5c5ae7af7b` |
| S13 | [docs/agents/observability.md](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/docs/agents/observability.md) | `2f15c10b5f0c9cf96fd6f675de116c33a066b2a3` |
| S14 | [packages/think/src/tests/execute-hitl.test.ts](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/packages/think/src/tests/execute-hitl.test.ts) | `e41e9293451b60303974b848fdb4990909be6e7d` |
| S15 | [packages/agents/src/chat/tool-state.ts](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/packages/agents/src/chat/tool-state.ts) | `461b7995aecac3a3284189ae71c957a199167a69` |
| S16 | [packages/codemode/src/runtime.ts](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/packages/codemode/src/runtime.ts) | `40f32ef2dc401d8a9724bd7eba8c253088de40fc` |
| S17 | [packages/agents/src/tests/state.test.ts](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/packages/agents/src/tests/state.test.ts) | `746fcc79aee847b3e7a23aae5e1f602b870c17e4` |
| S18 | [packages/agents/src/tests/readonly-connections.test.ts](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/packages/agents/src/tests/readonly-connections.test.ts) | `36270dcbc5ecf50b3d8b1b6224eeccefd68b37a0` |
| S19 | [.github/workflows/pullrequest.yml](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/.github/workflows/pullrequest.yml) | `54a5a5a79531278ad9215277a85602b22c8751c0` |
| S20 | [LICENSE](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/LICENSE) | `61cc9d46253c84da017eb24752d0264b433d8d7a` |
| S21 | [package.json](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/package.json) | `450b51fcf3542aafcc6e5221ff715e6c5f1811b9` |
| S22 | [packages/agents/src/index.ts](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/packages/agents/src/index.ts) | `c4106fe3d9195b27db759dfd95a960f02bdbc178` |
| S23 | [packages/think/src/tools/fetch.ts](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/packages/think/src/tools/fetch.ts) | `0691b21ddb2962ff7364914e1fcd382ac7ddcf3a` |
| S24 | [packages/think/src/tests/fetch-tools.test.ts](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/packages/think/src/tests/fetch-tools.test.ts) | `1dfc783513f88bf922eb0828c2e307bac2118224` |
| S25 | [.github/workflows/nightly.yml](https://github.com/cloudflare/agents/blob/d5d250e8593edbebb286c0f97a05c224bd23d054/.github/workflows/nightly.yml) | `afdfffa1ba2c73b7d66f6d15b603e24d0135ed9b` |

