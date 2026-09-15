# Guardian command review

Guardian adds deterministic rejection and signed review to supported tool calls.
It does not guarantee that every runtime path is intercepted or that Defender
and Sentinel will never alert. Native-runtime acceptance is a deployment gate;
see [the validation record](research/guardian-validation.md) and
[SOC activity profile](guardian-soc-profile.md).

## Review and decision flow

The shared engine under `.guardian/engine/` parses commands without executing
them. Windows PowerShell adapters and the Linux Python adapter use that same
implementation. The policy has three classifications:

1. `HARD_DENY`: prohibited effects, malformed input or unsupported syntax.
2. `AUTO_ALLOW`: narrowly recognized, side-effect-free diagnostics.
3. `IN_SCOPE`: all supported file operations, Azure/Entra operations and commands
   needing impact review. No valid approval means denial with
   `Route this command through guardian first`.

The guardian reviewer obtains the exact command, intended purpose, necessity
including safer alternatives, and impact including failure blast radius. It
returns `APPROVED` or `DENIED` and a one-line rationale; it never executes the
operation. The approval issuer signs the reviewed request using Ed25519. Tokens
must match the pending request and session, expire within ten minutes and cannot
be reused. Hard-deny policy wins over every token. Successful review returns to
normal host permissions; it does not approve an independent host permission or
Defender decision.

Signatures bind full tool input, working directory, workspace, runtime, session,
agent and policy revision. The separate command hash preserves exact command
text for cross-runtime comparison; it is not a semantic-normalization proof.

Issuer signing authority belongs to a separate protected OS identity/service.
A custom agent name, a same-user MCP server name, or a writable approval JSON file
does not authenticate the guardian. Never put a production signing key in the
checkout, its environment, chat, or a worker-readable file. The repository ships
an integration contract; it does not provision that production trust boundary.
There is no registered guardian MCP server in this change. The role's
`guardian/append_decision` integration is a deployment prerequisite, not a
callable tool until an authenticated service implements and registers it.

For that service/operator integration, the supplied issuer primitive is:

```text
.guardian/venv/bin/python .guardian/engine/issuer.py --workspace ABSOLUTE_WORKSPACE --private-key PROTECTED_ABSOLUTE_KEY_PATH
```

Use `.guardian/venv/Scripts/python.exe` on Windows. Standard input is a JSON
proposal with `payload` (native host envelope), `runtime`, `surface`, `answers`
containing `command`, `purpose`, `necessity`, `impact`, `decision` (`APPROVED` or
`DENIED`), and one-line `rationale`. The private key is a protected raw 32-byte
Ed25519 key outside the workspace. The public key is configured as hexadecimal
`approval_public_key` in `.guardian/policy.json`; its default is null, so approvals
are unavailable until configured by the trusted operator. Running the issuer as
the same worker user does not satisfy the production separation requirement.

After a denial, the next three same-session requests receive heightened checks.
Recent denied command hashes are also checked across runtimes for ten minutes.
`PIVOT_ATTEMPT` records a detected retry. Recognized effect families catch some
tool changes; a command hash alone cannot establish semantic equivalence for all
programs. Unsupported wrappers and obfuscation are rejected instead of guessed.

## Prohibited operations

This is the deployment policy, independent of whether a specific SOC detection
is enabled. Unsupported forms are denied conservatively.

| Family | Denied effects |
| --- | --- |
| Mail | OST/PST access, copies and exports; Outlook caches, profiles, autocomplete and offline stores under AppData/LocalAppData |
| Credentials | Credential Manager/Vault; cmdkey including listing; vaultcmd; CredMan/Get-StoredCredential; DPAPI/ProtectedData/Unprotect/CryptUnprotectData and Protect/Credentials directories |
| Private data | Browser Login Data, Cookies and Local State/decryption; SSH private keys; AWS credentials; Azure tokens; kubeconfig; PSReadLine history; credential/secret/token dumps; saving prompted credentials |
| Process secrets | LSASS access/dumps, comsvcs MiniDump, procdump targeting LSASS, Out-Minidump |
| Hidden execution | Encoded PowerShell, decode-and-invoke, constructed command names, download cradles, IEX, suspicious LOLBin download/execute chains |
| Download destinations | Scripted downloads into AppData, Temp, Desktop, Users/Public or Windows directories |
| Evasion | Execution-policy bypass/unrestricted, hidden windows, remote content with NoProfile, AMSI bypass, security exclusions or disabling protection |
| Persistence and remote execution | WMI subscriptions; services with user-writable binaries; scheduled script tasks; startup and Run/RunOnce writes; PsExec, WinRM/remoting and remote process creation |
| Collection | Profile/mail/document archive staging or upload; bulk directory-user/local-group discovery |
| Key Vault | Vault/key/secret deletion, purge or backup; bulk retrieval and secret dumps |
| Azure control plane | Role assignment/PIM scripting; network/firewall/private endpoint or diagnostic changes; disabling logging/Defender plans; resource-group/subscription or mass deletion |
| Entra | App registrations with credentials, service-principal credential additions, consent grants, MFA/Conditional Access changes, borrowed identity/token replay |

Aliases, wrappers or alternate tools do not authorize equivalent effects.
The engine is a restricted parser-based policy, not a proof of arbitrary-program
behavior or a model of all proprietary detections. It cannot certify the
non-exhaustive “anything that could alert” condition.

Every Azure/Entra request additionally needs fresh protected identity evidence
for the named user or dedicated `copilot-agent` principal. A display name/tag or
worker-supplied `az account show` string is insufficient. No production identity
broker is configured by this change: Azure execution remains denied until that
boundary and its context binding have been deployed and tested.

## Supported command language

This first implementation supports literal workspace `cat`, `cp`, selected `rg`
file queries, `Get-Content`, `Set-Content`, and `Copy-Item`, plus explicit native
file edits. Standalone `pwd`, `Get-Date`, `Get-Location`, `Get-Process`, and bounded
workspace `Get-ChildItem` are diagnostics. Nested interpreters require review;
`cmd /c` effects remain unsupported. Scripts, builds, package managers, dynamic
expressions, recursive native searches and unknown tools are denied until an
appropriate effect contract and isolated executor exist. This restrictive scope
is deliberate and must be assessed before deployment to a normal coding workflow.

Parser dependencies and APIs were fetched from [tree-sitter Python](https://tree-sitter.github.io/py-tree-sitter/),
[PowerShell grammar](https://github.com/airbus-cert/tree-sitter-powershell),
[Ed25519 50.0.1](https://cryptography.io/en/50.0.1/hazmat/primitives/asymmetric/ed25519/),
[Python pathlib](https://docs.python.org/3.12/library/pathlib.html) and
[POSIX locking](https://docs.python.org/3.12/library/fcntl.html).

## Prepare and deploy

1. Review `.guardian/policy.json`, runtime configurations and this guide with the
   endpoint owner. Record installed runtime/extension versions and Defender mode.
   Do not inspect credential stores or collect an entire process/environment dump.
2. In a human-controlled setup session, prepare the isolated dependencies using
   installed Rust-based `uv` and Python 3.12+. These commands create a virtual
   environment and download pinned wheels; they do not install system policy:

   ```text
   uv venv --python 3.12 .guardian/venv
   uv pip install --python .guardian/venv/bin/python --only-binary :all: -r .guardian/requirements.txt
   ```

   On native Windows use `.guardian/venv/Scripts/python.exe` for the `--python`
   argument. If a wheel is unavailable, setup fails; do not compile or download a
   replacement from inside a hook. See [uv's CLI reference](https://docs.astral.sh/uv/reference/cli/).
3. An administrator deploys policy/engine/configuration with worker-read-only
   permissions and a separately authenticated signing service. Validate keys and
   paths through the issuer contract before enabling approvals. Do not give a
   worker general shell access merely to let the guardian append decisions.
4. Merge with existing hooks and managed Defender hooks; never overwrite, disable
   or weaken either. Use repository configurations for development only. Managed
   host policies and an execution boundary outside the worker are prerequisites
   for tamper resistance and timeout-independent enforcement.
5. Run the inert acceptance protocol on each installed surface. A missing hook,
   failed token check, uncovered tool path or unbounded startup blocks rollout.
   Do not enable a surface based solely on successful JSON fixture replay.

The policy path must resolve independently of the command's working directory.
The adapter entry point accepts `--runtime copilot|claude|codex`,
`--surface cli|vscode|cloud|auto` and `--event PreToolUse`, with the native JSON
envelope on standard input. For example, an inert fixture can be replayed through
`.guardian/venv/bin/python .guardian/adapters/dispatch.py --runtime codex --surface cli --event PreToolUse`.
This invokes policy evaluation, not the command contained in the fixture.
`rg`, `fd` and `jq` are preferred when the relevant operation needs them; the
decision path uses the shared parser/JSON implementation without unnecessary
subprocess startup, network fetches or tool installation.

## Runtime contracts and fetched sources

Fetched 2026-09-15. These are documentation findings; installed behavior has a
separate evidence column in the validation record.

| Surface | Configuration and material limitation | Source |
| --- | --- | --- |
| Copilot CLI | `.github/hooks/guardian.json`; exec/args is CLI-specific and cannot share one entry with shell command fields. PermissionRequest is CLI-only. Timeout may fall through even for policy hooks. | [Hook reference](https://docs.github.com/en/copilot/reference/hooks-reference) |
| Copilot VS Code | Converts compatible event names/command fields, ignores matchers, uses its own tool names and envelope. Exit 2 blocks; do not assume CLI error handling. | [VS Code hooks](https://code.visualstudio.com/docs/agent-customization/hooks) |
| Copilot cloud | Default-branch repository hooks and Linux bash path; no CLI permissionRequest/Windows PowerShell parity. Local offline ledger cannot serve as shared endpoint/cloud authority. | [Hook reference](https://docs.github.com/en/copilot/reference/hooks-reference) |
| Claude CLI/extension | Settings hooks apply in IDE extensions and subagents. Command/args executes directly; Windows needs an executable. Timeout, missing executable and ordinary exit 1 are nonblocking; exit 2 blocks PreToolUse. | [Hooks](https://code.claude.com/docs/en/hooks), [subagents](https://code.claude.com/docs/en/sub-agents), [permissions](https://code.claude.com/docs/en/permissions) |
| Codex CLI | User/project hooks; hooks enabled by default. Bash normalization covers exec_command; apply_patch and MCP/local tools have separate names. write_stdin does not rerun PreToolUse. Unsupported ask/common-output fields must not be emitted. | [Hooks](https://learn.chatgpt.com/docs/hooks), [schemas](https://github.com/openai/codex/tree/main/codex-rs/hooks/schema/generated) |
| Codex extension | Windows command override is documented; hook invocation inside this installed extension is unverified. Static execution rules alone do not establish complete coverage. | [IDE](https://learn.chatgpt.com/docs/codex/ide), [rules](https://learn.chatgpt.com/docs/agent-configuration/rules) |

Codex custom guardians use `.codex/agents/guardian.toml`, with `name`,
`description`, `developer_instructions` and supported config keys. A read-only
sandbox is not a no-shell capability restriction; test the disabled shell and
unified-exec features. [Custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents),
[configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

Static deny profiles are supplementary. Copilot tool permissions, Claude deny
patterns and Codex argv-prefix rules do not parse every equivalent program.
See [Copilot tool permissions](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools).
Copilot's Windows local sandbox support is documented for the relevant Insiders
path; check the deployed edition before relying on it.
[Local sandboxing](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/understanding-local-sandboxing).

Claude's native Windows Bash sandbox is unavailable. Use managed
`allowManagedHooksOnly`, default permission mode and managed
`permissions.disableBypassPermissionsMode: "disable"` as appropriate; these are
administrator deployment choices, not settings this repository activates.
[Sandboxing](https://code.claude.com/docs/en/sandboxing),
[permissions](https://code.claude.com/docs/en/permissions).
`CLAUDE_CODE_USE_POWERSHELL_TOOL=1` enables the PowerShell tool where supported;
test the installed version. Do not add `-ExecutionPolicy Bypass` to the guardian
launcher: it conflicts with this policy's hard denial.
[Environment variables](https://code.claude.com/docs/en/env-vars).

Issue reports are version-specific, not specifications: Copilot
[#2392](https://github.com/github/copilot-cli/issues/2392) was closed;
[#2540](https://github.com/github/copilot-cli/issues/2540) and
[#3874](https://github.com/github/copilot-cli/issues/3874) were open at research.
Codex [#18491](https://github.com/openai/codex/issues/18491) remained open but its
narrower coverage/rewrite description is superseded by the fetched documentation.
Test subagents anyway; a stop hook cannot undo a command already executed.
Claude [#39344](https://github.com/anthropics/claude-code/issues/39344) was closed
(reported ask/deny interaction; no fix version established in this research).
[#26862](https://github.com/anthropics/claude-code/issues/26862) was closed as not
planned. Do not emit `ask` for hard denials or treat an issue author's security
claim as a runtime guarantee.

The requested [cmd-guard](https://github.com/KudoLayton/cmd-guard) source
could not be retrieved; no implementation claim depends on having read it.
The accessible reference implementations informed parsing review only:
[claude-code-command-guard](https://github.com/Yodaisgaming/claude-code-command-guard),
[Hookshot](https://github.com/CorridorSecurity/hookshot).
Hookshot reports different Codex failure behavior from current official docs and
main source; the gate avoids those unsupported outputs rather than relying on
that disagreement.

## Ledger and SOC lookup

`.guardian/ledger.jsonl` holds the shared local JSONL decision history, using
`.guardian/ledger.schema.json`. Each record links to the previous line's SHA-256.
The writer serializes concurrent appends and rejects an invalid chain. Decision
computation precedes append, but a successful durable append must precede an
allow response. Ledger failure denies locally; host timeout behavior still needs
an external execution boundary.
Ledger capacity is bounded at 8 MiB and lock acquisition at 250 ms. Exhaustion
denies; no automatic checkpoint/rotation service is implemented. Arrange protected
retention and reviewed maintenance before reaching the bound; workers must never
truncate the file to recover.

Records associate timestamp, runtime/surface, session/agent/tool, exact request
hash, command representation, review answers, decision/reason/rule/layer,
identity evidence, pivot flag, token expiry and observed Defender verdict.
Unknown identity or Defender verdict is recorded as unknown, never as approved.
Malformed envelopes, missing dependencies or an unavailable ledger can prevent
an audit append; the adapter emits a denial to stderr. Host/SOC collection of
those errors is necessary to account for these audit gaps. The file alone cannot
answer an event which never reached a functioning writer.
The schema retains raw command text, so do not paste secrets into command strings.
This implementation does not promise automatic secret redaction. Access-controlled
audit material must not become a second credential store; SOC must handle any
incident record containing an accidentally supplied literal as sensitive data.

From the authorized project root, an installed `jq` can answer one session query:

```text
jq -c --arg session 'SESSION_ID_FROM_THE_INCIDENT' 'select(.session_id == $session)' .guardian/ledger.jsonl
```

A hash chain detects changes against a retained trusted head; it cannot prevent
same-user rewriting or undetectable truncation without external checkpoints.
OS ACLs, protected writer identity, retention and a SOC collector are deployment
requirements. The repository does not provision them. Copilot cloud rollout is
blocked until authenticated shared collection/state and managed execution exist;
an offline file in an ephemeral runner cannot enforce cross-device pivots.

Defender remains independent. Never emit an allow that overrides its denial or
infer its verdict from lack of a local alert. Microsoft documents native event
inspection and Block/Audit/Disabled modes; audit still raises alerts.
[AI runtime protection](https://learn.microsoft.com/en-us/defender-endpoint/ai-agent-runtime-protection-overview).
ASR rule names are not a complete EDR signature list.
[ASR reference](https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction-rules-reference).
Sentinel analytics depend on the deployed solution/rule/version, not a universal
25-call threshold. [Sentinel solutions](https://github.com/Azure/Azure-Sentinel/tree/master/Solutions).

The fetched [Sensitive Key Vault operations rule](https://github.com/Azure/Azure-Sentinel/blob/master/Solutions/Azure%20Key%20Vault/Analytic%20Rules/KeyVaultSensitiveOperations.yaml)
(version 1.0.4) lists the destructive/backup operations above and uses its own
scheduled query. This supports that policy category, not a universal volume
threshold or assurance about the tenant's effective analytics.

For VS Code, `.vscode/settings.json` disables importing Claude settings as
Copilot hooks, because that host does not document Claude's exec/args format.
The dedicated Copilot hook file remains configured. Native extension acceptance
must confirm the effective source and tool names. The supplemental Copilot
PermissionRequest handler checks hard denials and defers to normal host
permissions; token consumption occurs at mandatory PreToolUse only.
