# Findings a maintainer can act on

A defect finding needs a cause, a reachable condition and a consequence. Quote
only the minimal evidence required; never reproduce credentials or private data.

Use this compact structure when it improves clarity:

- **Title and impact:** what breaks, for whom, and how severely.
- **Location:** file path, symbol and relevant line when available.
- **Condition:** concrete input, configuration or execution order.
- **Evidence:** the changed behavior, affected caller or contract, and why
  existing checks do not prevent it.
- **Verification:** reproduced with a stated check, established by a complete
  code trace, or still a hypothesis requiring a named missing fact.

Do not call an issue verified merely because a suspicious pattern exists.
For example, a missing authorization check inside a handler is a candidate;
inspect the registered middleware and alternate entrypoints to determine
whether a reachable unauthorized path actually exists.

Review changed behavior against the base. Mention an existing issue separately
only when it materially affects the change or the user requested a wider audit.
Avoid repeated findings that share the same root cause and correction.

An optional improvement should explain a specific maintenance burden, such as
duplicated validation that has already diverged. Label it optional unless it
violates an applicable requirement or causes a demonstrated defect.

Tests can strengthen a finding but are not mandatory for every code-path proof.
If dependencies, credentials or runtime access are unavailable, state what was
inspected and which behavior remains unverified.
