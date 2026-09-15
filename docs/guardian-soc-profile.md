# Agent Activity Profile — guardian gate

Profile date: 2026-09-15. Status: **target Windows endpoint not observed**.
Owner: repository maintainer with endpoint/SOC administrator. The Linux authoring
environment is not the user's Windows device. No process name, identity or
Defender mode below is inferred from product branding.

| SOC field | Current evidence / required capture |
| --- | --- |
| Copilot CLI / VS Code process chain | Unknown; capture exact PID and bounded parent chain on target |
| Claude CLI / VS Code process chain | Unknown; capture exact PID and bounded parent chain on target |
| Codex CLI / VS Code process chain | Unknown; capture exact PID and bounded parent chain on target |
| Copilot cloud process chain | Unknown; requires runner-specific authorized observation |
| Authorized workspace | This checkout root; target device absolute path must be recorded at deployment |
| Guardian runtime | `.guardian/venv`, `.guardian/engine`, `.guardian/adapters`; deployed protected absolute locations must be recorded |
| Temporary/cache paths | Not inventoried; record only actual tool-created paths from bounded observation |
| Azure/Entra identity | Unconfigured/unverified; execution denied pending protected identity broker |
| Defender AI runtime mode | Unknown: obtain effective Block/Audit/Disabled mode from device administrator |
| Defender per-call verdict | Unknown unless an authenticated observable verdict is supplied; absence is not allow |
| Ledger | Workspace `.guardian/ledger.jsonl`; collector/checkpoint location not provisioned |
| Coverage | [Validation matrix](research/guardian-validation.md); native surfaces not yet accepted |

## Bounded Windows process observation

A human administrator may run this read-only query after selecting the actual
runtime PID in Task Manager. It queries at most six specific local PIDs, omits
command lines/environment variables, and does not enumerate files or credentials.
Replace the sample PID; do not treat it as a discovered process. Run separately
for each CLI and extension host. PID reuse means capture creation timestamps and
validate that a parent existed before its child.

```powershell
$targetProcessId = 12345 # Replace with the observed runtime PID.
$seenProcessIds = [System.Collections.Generic.HashSet[uint32]]::new()
for ($depth = 0; $depth -lt 6 -and $targetProcessId -gt 0; $depth++) {
    if (-not $seenProcessIds.Add([uint32]$targetProcessId)) { break }
    $processRecord = Get-CimInstance -ClassName Win32_Process -Filter "ProcessId = $targetProcessId" -Property ProcessId, ParentProcessId, Name, ExecutablePath, CreationDate
    if ($null -eq $processRecord) { break }
    $processRecord | Select-Object ProcessId, ParentProcessId, Name, ExecutablePath, CreationDate
    $targetProcessId = [uint32]$processRecord.ParentProcessId
}
```

This procedure has **not** been run on the endpoint. Permission-related missing
ExecutablePath values stay unknown. Sources:
[Get-CimInstance](https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/get-ciminstance?view=powershell-7.5),
[Win32_Process](https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-process).

## Decision lookup and prohibited behavior

One bounded lookup by incident session ID:

```text
jq -c --arg session 'INCIDENT_SESSION_ID' 'select(.session_id == $session)' .guardian/ledger.jsonl
```

Use the [full policy denylist](guardian.md#prohibited-operations): mail stores;
credential/DPAPI/browser/key/token/history collection; LSASS dumps; obfuscation,
downloaders and evasion; Defender tampering; persistence/remoting; bulk discovery
and exfiltration; sensitive Key Vault operations; RBAC/PIM, network/logging,
mass-delete and Entra security changes; borrowed identities and equivalent pivots.
The ledger answers what the gate observed and decided, not every machine action.

Retain audit data under SOC access controls; never commit incident ledgers or
secret-bearing command text to Git. A local hash chain needs external checkpoints
and a protected writer to resist rewrite/truncation. Cloud and endpoint ledgers
need an authenticated shared collector before cross-device claims are valid.
Defender remains authoritative and may independently alert in audit or block
mode; guardian must never suppress it. No alert-free assurance is claimed.
