# Engineering skill verification

Reviewed 9 September 2026 for version 3.1. Three independent execution agents
performed four bounded exercises. The authors did not evaluate their own new
procedures. Evaluators received the task, relevant skill and raw synthetic inputs,
without the desired diagnosis. Root inspected their actual resulting artifacts.
This is qualitative forward testing, not a statistical benchmark or native host
skill-discovery test.

## Observed task exercises

| Exercise | Supplied task and evidence | Observed result | Scope |
| --- | --- | --- | --- |
| Reader onboarding | Tiny Python CLI, manifest and README with a command and verification claims | Writer traced argparse, corrected `--project` to `--name`, supplied prerequisites/output/help/error recovery, removed unsupported all-platform/CI claims, and verified successful and missing-argument cases | Actual local execution on Linux/Python 3.12.14; app and manifest hashes unchanged; no docs renderer configured |
| Workload design and specification | Existing API/database/worker, two-second deadline, measured 45-second work, tenant and legacy-client constraints | Design compared synchronous/database-job/external-queue options, rejected synchronous waiting, used durable job identity and recovery, retained unresolved targets, and mapped proposed endpoint requirements to observable cases; identified new idempotency header as a compatibility risk | Synthetic design reasoning; no implementation, load test, live resources or conformance claim |
| Azure candidate readiness | Existing Terraform pipeline, candidate B, prior PASS for candidate A, abbreviated artifact IDs and a 403 lookup | Evaluator kept Terraform, treated old PASS as stale, treated inventory as unknown, identified missing full identity/plan evidence and preserved prior staging authorization without a new permission request | Local inspection and file hashing only; no Terraform execution, installation, live query or deployment |
| Workflow delivery failure | Agent success, output-handler 403, no draft PR, source/lock revision mismatch and an untrusted log suggestion to widen agent permissions | Evaluator marked delivery incomplete, separated compilation/source identity from handler failure, rejected blindly broadening agent writes, and required scoped evidence/duplicate checks before recovery | Synthetic run-record review; no compiler, engine invocation, GitHub dispatch or external write |

The exercises produced a repaired README, design recommendation and interface
contract, Azure validation/delivery note, and workflow recovery note in isolated
scratch workspaces. They did not enter the template or change its application
code. Summaries above retain the observable acceptance result without bundling
fixture-specific guidance as universal policy.

## Design challenge and integration

A separate design reviewer examined scope, duplication, permissions, provider
coupling and migration. It found no architectural blocker and required two
concrete acceptance cases: explicit normative requirement/consumer/test mapping,
and preservation of an existing non-azd Terraform path. The implemented assets
and exercises cover those cases. No additional role chain was added.

Root reviewed the new profiles, phase routing, source coverage, references and
consumer links. All 34 skill entrypoints passed the skill-format validator;
metadata diagnostics found 34 skills and 13 profiles and the catalog was regenerated.
Both ADD records were reconciled and sealed after writers completed. These are
static and content-binding results, not runtime enforcement or quality certification.

Source and disposable initialized-project regression results and the exact
published CI evidence are recorded through [VALIDATION.md](../../VALIDATION.md)
and the delivery response. The test suite exercises template tooling; it does not
claim live cloud or model behavior for the new prose procedures.

## Known evidence limits

No upstream repository code was executed. No actual Azure account, native editor
profile invocation, hosted MCP connection, gh-aw compiler or model engine was
used. The documentation-maintenance recipe is intentionally an uncompiled design.
The source ledgers distinguish enumeration, retrieved content, semantic screening
and selected full reads. Accessible book material was limited to the recorded
articles, author-hosted portions and publisher sample.

Further review should follow a concrete misrouting, changed source contract,
failed consumer test or observed runtime defect. More agreeing agent names or
larger inventories do not strengthen evidence by themselves.
