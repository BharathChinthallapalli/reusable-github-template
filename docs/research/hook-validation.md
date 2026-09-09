# Hook and design-gate verification

Date: 2026-09-09. Version 3.0 adds the requested ADR, ADD, runbook and prompt
structure plus lifecycle adapters for supported hosts. Source lessons are recorded
in [the Cloudflare review](cloudflare-agents.md), which inspected 25 pinned files
without running that SDK. Current primary host contracts are linked from
[the hook guide](../../hooks/README.md).

## Independent challenges and corrections

| Concrete concern | Correction and evidence |
| --- | --- |
| The design gate's imported loader and scanner pins were outside its scope | Protect the executable loader, dependency file, ignore policy and both CI entrypoints |
| Input-controlled `gitleaks:allow` could suppress a secret elsewhere in a serialized argument line | Disable inline suppression in both scanner modes; add pre-argument and post-file real-scanner regressions |
| A repository `ruff.py` or PYTHONPATH entry could replace the installed scanner | Invoke Ruff with isolated Python; test that shadow modules never create their execution marker |
| Absolute VS Code paths and nested working directories were rejected or resolved incorrectly | Normalize against the event cwd, reject external aliases, and pass contained root-relative paths to the gate |
| NUL or cyclic-symlink paths could produce a host fail-open exit | Translate path exceptions into sanitized host denial behavior; exercise malformed path and remote URI cases |
| Combined Git force flags and Windows recursive quiet deletion forms escaped checks | Reject the demonstrated literal variants without executing any candidate command |
| Manual session diagnostics waited for tool JSON that did not exist | Session and standalone check modes do not read stdin |
| Importing the hook created bytecode that the design gate treated as new implementation | Ignore only regular Python bytecode inside cache directories; retain source, standalone bytecode and symlink coverage |
| The ADD implied that ZIP scans omit environment files | Document the actual difference: Git ignore selection versus the ZIP filesystem fallback |

A separate reviewer inspected the implementation and installer ordering, then ran
five targeted hook CLI regressions independently. All passed. A separate gate
review found a narrative-validation weakness; ready sections now exclude code-only,
comment-only and obvious placeholder content. Final semantic accuracy still needs
review; a plausible paragraph is not proof of correct behavior.

The installer checks the pinned archive size and SHA-256 before extracting one
exact regular binary member. Only then does it run the staged binary's version
command and atomically replace the destination. All six platform pins match the
captured official release metadata. No unverified downloaded executable is run.

## Evidence categories

| Category | Coverage and limit |
| --- | --- |
| Offline hook CLI tests | Controlled scanner subprocesses exercise host schemas, denial, no automatic approval/execution, scope/path handling, deadlines, redacted diagnostics, Git selection and read-only checking |
| ADD tests | Ready/draft/retired state, explicit future/deleted paths, accepted ADRs, narrative validation, content drift, bytecode handling, safe paths and failed-seal preservation |
| Installer tests | Archive identity, size, member type, extraction, destination aliases, atomic replacement and preservation of existing binaries on failure |
| Real scanner integration | Seven cases use installed pinned Ruff/Gitleaks to check secret detection, suppression resistance, no auto-fix, module-shadow prevention, clean continuation and setup |
| Git integration | Existing 15 cases exercise the actual pre-commit configuration and Git behavior |
| Native host execution | Not performed; hook input replay and a successful setup workflow do not establish editor/client invocation |

The real-scanner suite skips locally when tools are absent. CI explicitly sets
`REQUIRE_AGENT_HOOK_TOOLS=1`, converting absence into a failure. This development
environment could not install the scanner binaries, so actual scanner execution
is configured to run through the published GitHub workflow. Its configuration
is not evidence that the delivered commit passed. Consult [the validation record](../../VALIDATION.md)
and match the delivery's workflow runs to the exact published commit.

These checks establish their recorded boundaries. A repository-owned command
policy is editable, post checks cannot undo effects, and arbitrary shell or
uncovered hosted tools need their host's isolation and permission controls.
The review stopped after concrete findings were resolved and their regression
cases passed; it did not claim exhaustive safety from a finite command list.
