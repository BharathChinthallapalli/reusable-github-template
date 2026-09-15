param([string]$Surface = "unknown", [string]$Event = "PreToolUse")
$ErrorActionPreference = 'Stop'
try {
    $guardianRoot = Split-Path -Parent $PSScriptRoot
    $python = Join-Path $guardianRoot 'venv/Scripts/python.exe'
    if (-not (Test-Path -LiteralPath $python -PathType Leaf)) { throw 'Guardian runtime missing' }
    $hookInput = [Console]::In.ReadToEnd()
    $hookInput | & $python -I (Join-Path $PSScriptRoot 'dispatch.py') --runtime codex --surface $Surface --event $Event
    if ($LASTEXITCODE -ne 0) { exit 2 }
    exit 0
} catch {
    [Console]::Error.WriteLine('Guardian unavailable; operation denied. Provision the managed runtime.')
    exit 2
}
