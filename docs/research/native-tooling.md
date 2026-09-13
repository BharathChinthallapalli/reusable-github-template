# Native tooling: adoption and evidence

Reviewed 13 September 2026 against template branch baseline
`7ef30d93e522b7833f7214938181e238a78d338c`. The user requested research, useful
implementation and a GitHub push. [ADR 0009](../adr/0009-native-tooling-and-review-evidence.md)
records the decision; [agent tooling](../agent-tooling.md) owns command policy.

## Adopted scope

| Tool | Repository evidence and change |
| --- | --- |
| Ruff | Already pinned at 0.16.6 and invoked by the hook/CI checks. There is no Black or Flake8 to replace. Keep the existing correctness rules; a formatter migration requires an actual formatting contract |
| uv | Pin 0.12.13 and setup-uv v9.0.0 at `c771a70e6277c0a99b617c7a806ffedaca235ff9` in both workflows. Install the same requirements into the Python selected by setup-python. Prefer uv in local virtual environments with a pip fallback |
| ripgrep | Existing shared default and Copilot package smoke check. Keep it for scoped text searches; Gitleaks continues to check secrets |
| ast-grep | Install the official ast-grep-cli 0.45.3 binary wheel in Copilot setup. Verify a Python call matches while comment/string lookalikes do not. Add scoped structural-search guidance without a generic lint gate |
| Semgrep | Retain relevant reviewed-rule analysis and record tool/rule versions, coverage, errors and findings. It complements structural searches rather than running on every search |

The setup-uv tag was resolved through GitHub's Git ref API and its pinned
`action.yml` was inspected: version/cache inputs exist and its action runtime
is Node 24. The uv 0.12.13 release notes were read. This is a package-installer
change, not a conversion to a Python application or a new dependency lockfile.
Top-level requirements remain pinned; their entire transitive closure is not.
Python and pre-commit still have runtime/environment requirements.
[uv integration](https://docs.astral.sh/uv/guides/integration/github/),
[pinned action](https://github.com/astral-sh/setup-uv/blob/c771a70e6277c0a99b617c7a806ffedaca235ff9/action.yml),
[uv release](https://github.com/astral-sh/uv/releases/tag/0.12.13).

The ast-grep documentation names the Python CLI distribution and distinguishes
Linux's unrelated `sg` command. Version 0.45.3 was checked against the upstream
release and installed from a binary wheel. No Node or Rust compiler installation
is needed for this distribution; this observation does not generalize to every
native tool. A project can introduce tested structural rules for a real policy.
[Installation and syntax](https://ast-grep.github.io/guide/quick-start.html),
[release](https://github.com/ast-grep/ast-grep/releases/tag/0.45.3),
[rule setup](https://ast-grep.github.io/guide/scan-project.html).

## Claims checked before adoption

| Proposed claim | Evidence-based interpretation |
| --- | --- |
| Ruff always reduces 45 seconds to 0.2 seconds | Ruff publishes substantial benchmark speedups. The supplied absolute times are not measurements of this repository, which already uses Ruff. [Ruff](https://docs.astral.sh/ruff/) |
| uv universally installs 10–50 times faster | Upstream benchmarks support evaluating uv, not a guarantee for this small dependency set. Include resolution, download and setup time when comparing; no repository-wide multiplier is claimed. [uv benchmarks](https://docs.astral.sh/uv/reference/internals/benchmarks/) |
| Every runner is a blank 2-core, 7 GB VM | Current public ubuntu-24.04 runners are listed as 4 CPUs/16 GB; private Linux standard runners as 2 CPUs/8 GB. Images carry preinstalled tooling. Public standard runner use is free, so faster runs here do not directly establish billable-minute savings. [GitHub runner reference](https://docs.github.com/en/actions/reference/runners/github-hosted-runners) |
| Python setup necessarily costs 30–90 seconds | setup-python can reuse the runner's cached interpreter. This repository's earlier run reports about 0 seconds at one-second timestamp resolution for Python setup and 3 seconds for pip installation. No universal setup tax is established. [uv integration](https://docs.astral.sh/uv/guides/integration/github/), [baseline run](https://github.com/BharathChinthallapalli/reusable-github-template/actions/runs/34755514830) |
| Rust binaries are always static and install in 1–2 seconds | Linkage depends on target, build flags and native dependencies. Download/decompression/setup vary; cargo-binstall may fall back to compilation when a binary is unavailable. [Rust linkage](https://doc.rust-lang.org/reference/linkage.html), [cargo-binstall](https://github.com/cargo-bins/cargo-binstall) |
| Rust prevents OOM and all RCE | Rust programs allocate memory and can fail/abort on allocation errors. Safe-Rust guarantees depend on valid unsafe/FFI contracts and do not remove authorization or application-logic flaws. [Allocation failure](https://doc.rust-lang.org/std/alloc/fn.handle_alloc_error.html), [unsafe Rust](https://doc.rust-lang.org/book/ch20-01-unsafe-rust.html) |
| No garbage collector means deterministic API latency | Lack of GC does not bound I/O, locks, scheduling or workload. This is an engineering inference, not a measured latency guarantee. Use the existing [performance procedure](../../.agents/skills/performance-analysis/SKILL.md) |
| Native frontend tools guarantee 50–80% faster builds and no OOM | No frontend application/build exists here to test that claim. JS plugins, compatibility, source maps and output quality still matter. Evaluate the framework-supported option on an actual application before replacing its toolchain |

## Frontend adoption boundary

[SWC](https://swc.rs/) supplies compilation/minification capabilities;
[Rolldown](https://rolldown.rs/) and [Rspack](https://rspack.rs/) supply bundling
with their own integration/compatibility surfaces. [Biome](https://biomejs.dev/)
combines formatting and linting; [Oxc](https://oxc.rs/) provides several JavaScript
tooling components. These tools are not interchangeable, and one binary does
not automatically cover every ESLint plugin, transform or bundler feature.
The [application CI guide](../extending-ci.md#select-native-tools-for-a-real-bottleneck)
now requires compatibility and workload evidence before such a migration.
No application runtime, frontend manifest or Azure service is added here.

## Source and measurement limits

The user-linked [Rust CI primer](https://rustprojectprimer.com/ci/github.html),
[rust-cache action listing](https://github.com/marketplace/actions/rust-cache)
and cargo-binstall README were inspected for installation/cache context, not
accepted as proof of the supplied blanket performance claims. The
[daily.dev page](https://daily.dev/posts/my-favorite-rust-development-tools-setups-and-ai-workflows-webopzhz0)
returned no readable article text; the
[YouTube link](https://www.youtube.com/watch?v=6vtmpznaAQg&t=965) could not be read.
Neither is used as factual support. No unreviewed upstream script was executed.

Baseline CI run 34755514830 completed its job in 49 seconds, with a 3-second pip
step, based on GitHub API timestamps. This is one observation at one-second
resolution, not a controlled benchmark. The follow-up will inspect one complete
CI run and one Copilot setup run at the pushed state, including uv setup costs.
Record their actual IDs/results in the PR; do not convert a single comparison
into a stable speedup claim. No persistent uv cache is enabled, and no cache-hit,
peak-memory, frontend-build or billing benchmark has been run.

Local macOS arm64 validation used uv 0.12.13 and managed CPython 3.12.14 in an
isolated temporary environment. Fresh installation of requirements plus ast-grep
resolved 12 packages in 1.91 seconds, prepared downloads in 20.16 seconds and
installed in 23 milliseconds according to uv. These phases exclude interpreter
and uv setup and are not comparable to the Linux CI baseline. This illustrates
why reporting installation alone can misrepresent total preparation time.

The structural smoke command returned exactly one real call; the scoped example
found one `subprocess.run` call in `tools/install_hook_tools.py`. A match is
discovery evidence, not a security finding. The final delivery checks and their
limitations are recorded with [version 3.3 validation](../../VALIDATION.md).

Final local checks passed before publication: foundation/links, all 34 skill and
13 agent definitions, catalog freshness, ADD scope/bindings, the three edited
skill-format checks, installed-package compatibility, Ruff/Gitleaks and all
applicable pre-commit hooks. The unit lane passed 136 tests; Git integration
passed 21 with the existing case-collision test skipped on this case-insensitive
macOS filesystem. Tests used `TMPDIR=/private/tmp` and an interpreter path without
spaces to avoid the previously documented host fixture issues. Linux CI must
exercise all 22 integration tests with real scanner prerequisites required.

A disposable initialized copy passed foundation, metadata, catalog and design
checks. Preview wrote nothing, initialization changed exactly the six declared
files, and repeating identical inputs preserved their bytes. Semgrep 1.177.0
with OSS `p/github-actions`, metrics/version checks disabled, ran 11 applicable
rules across both workflows with zero findings and zero scan errors. The actual
workflow smoke block passed locally; changing its expected match count failed.
The independent review checked all 17 workflow shell blocks with `bash -n`.

Hosted setup, actual native agent invocation, font rendering and Windows runtime
execution are separate from these local checks. Hosted results are attached to
the delivered PR revision, not inferred from earlier passing runs.
