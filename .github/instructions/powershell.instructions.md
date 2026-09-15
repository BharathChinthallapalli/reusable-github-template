---
description: "PowerShell development and review within the authorized project; avoid sensitive endpoint collection and injection."
applyTo: "**/*.ps1,**/*.psm1,**/*.psd1"
---

# PowerShell development

PowerShell is allowed for authorized development. Inspect the script and its
targets before running it. Keep searches within the task's project scope and
respect [the shared endpoint boundaries](../../AGENTS.md). A permitted interpreter
does not authorize collecting credentials, browser databases or mailbox caches.

- Invoke known commands with separate arguments and parameter binding. Never
  evaluate externally sourced command strings with `Invoke-Expression` or dynamic
  script blocks. Validate allowed paths, destinations and parameter values;
  a type cast is not authorization or universal sanitization.
- Use the approved authentication mechanism or secret provider. Pass PSCredential
  or SecureString where the cmdlet requires it; do not hardcode, print or embed
  secrets in script source. Get-Credential is interactive, not a CI default.
- Converting plaintext to SecureString does not erase existing string copies.
  SecureString lacks internal encryption on non-Windows. For encrypted storage,
  keep key management separate; never save the AES key beside its ciphertext.
- Keep TLS certificate validation enabled and use approved destinations. Do not
  disable certificate checks or download-and-run an arbitrary repair script.
- Preserve organization-managed signing, execution policy and endpoint controls.
  AllSigned is not a security boundary. Setting a session's LanguageMode is not
  an enforced sandbox. Do not change policy, logging or JEA endpoints as a side
  effect of a coding task; those are separately scoped administrative changes.
- Use the project's terminating-error and exit-code conventions. Report useful
  sanitized failures; do not suppress errors and claim successful execution.
- Use existing PSScriptAnalyzer/Pester checks when available and relevant. The
  plaintext-password rules identify specific patterns, not every credential leak.
  Use synthetic fixtures; never probe real credential or Outlook stores in tests.

References: [PowerShell corrections and sources](../../docs/research/scoped-development-rules.md).
