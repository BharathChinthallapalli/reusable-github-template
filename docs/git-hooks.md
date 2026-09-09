# Git checks for every project

The inherited [.pre-commit-config.yaml](../.pre-commit-config.yaml) defines ten
checks. CI runs them on every tracked file. Install the commit hook once in each
clone to get the same checks before ordinary local commits.

## Activate in a clone

Prepare [the Python environment](using-the-template.md), then inspect the active
hook path before installing:

```bash
git config --show-origin --get core.hooksPath
git rev-parse --git-path hooks/pre-commit
git rev-parse --git-path hooks/pre-commit.legacy
```

The first command normally prints nothing and returns 1 when unset. If it prints
a configured path, coordinate with its owner; pre-commit refuses installation
with that setting. Do not unset or override a managed hook path to make setup pass.
Inspect any existing files at the two printed hook paths. The installer normally
chains an existing hook in migration mode, but an existing `.legacy` collision
can be overwritten. Preserve and reconcile that collision before installation.
Do not use `--overwrite`. On a fresh clone with no conflicting hooks, run:

```bash
python -m pre_commit install
python -m pre_commit run --all-files
```

Installation writes this clone's hook script; it does not configure global Git.
The first run downloads the pinned hook repository and prepares its Python
environment. It needs Git, network access and a writable cache. Keep the prepared
Python environment available; recreating or moving it may require reinstalling
the hook. `python -m pre_commit uninstall` removes the installed hook and normally
restores a migrated predecessor. Review local modifications before uninstalling.

Git does not copy client hooks when cloning or creating from a GitHub template.
A ZIP also has no Git index: initialize and stage its files before installing or
running hooks. See [setup](using-the-template.md). Instructions and skills do not
activate a client hook on your device. [Git book](https://git-scm.com/book/ms/v2/Customizing-Git-Git-Hooks),
[pre-commit installation and migration](https://pre-commit.com/#running-in-migration-mode).

## Included checks

| Check | Contract |
| --- | --- |
| Environment filenames | Reject `.env` and `.env.*` at any depth, including symlinks; allow `.env.example` and `.env.*.example` containing sanitized values |
| Private-key signatures | Reject recognized private-key markers in text files, without printing contents |
| JSON, YAML, TOML | Parse supported file syntax; YAML permits multiple documents but rejects duplicate keys |
| Merge conflicts | Detect leftover conflict markers even outside an active merge |
| Portable names | Detect case collisions and illegal Windows filenames |
| Symlinks | Detect broken links; this is not a filesystem access boundary |
| File size | Reject files over 1 MiB, including modified tracked files; review deliberate binary/data needs before changing the policy |

Checks do not rewrite source files. pre-commit itself temporarily saves/restores
unstaged tracked changes and writes its cache. Any inherited legacy hook can
have additional side effects. Arguments end with `--` so filenames beginning
with dashes cannot become checker options. The filename policy is case-sensitive,
matching the template's `.gitignore`; arbitrary credential filenames are outside
its scope. [Selected upstream implementation](https://github.com/pre-commit/pre-commit-hooks/tree/3e8a8703264a2f4a69428a0aa4dcb512790b2c8c).

The upstream size hook excludes paths attributed `filter=lfs`; that exemption
does not verify an uploaded LFS object or prevent someone changing attributes.
Private-key detection does not detect all API tokens, passwords or encoded
secrets. Example filenames are not proof of sanitized contents. Add a reviewed
provider-token/history scanner and configure available GitHub secret protection
when the project requires that coverage; those capabilities are not activated
by this configuration. Never test them with real credentials.

## What was checked

| Invocation | Content examined |
| --- | --- |
| Ordinary commit with installed hook | Changed staged files; pre-commit temporarily removes unstaged tracked edits |
| `python -m pre_commit run --all-files` locally | Current working-tree contents of tracked files; it can differ from the staged index |
| Same command in clean CI checkout | Tracked files at the checked-out CI revision; no full history scan |

Local hooks can be skipped, removed or changed. Web/API commits bypass client
hooks. CI detects these current-tree violations independently, but a required
successful check only blocks merging when a live ruleset enforces it. The shared
template's ruleset recipe is disabled until configured through
[GitHub setup](github-setup.md). Editing hooks, CI or their inputs can weaken
checks; review those changes. Neither Git hooks nor agent lifecycle hooks are
a sandbox or a guarantee that an unattended agent is safe.
[Git hook semantics](https://git-scm.com/docs/githooks),
[Copilot lifecycle hooks](https://docs.github.com/en/copilot/reference/hooks-reference).

## Troubleshooting and verification

- **Unstaged changes warning:** inspect `git diff` and `git diff --cached` before
  and after the run. pre-commit retains recovery patches in its cache; patches
  can include sensitive unstaged text. Do not upload the cache or full diagnostic
  bundles. If restoration fails, preserve the patch and working tree before
  attempting recovery. Do not default to a hard reset.
- **Hook not running:** check the effective `core.hooksPath`, installed hook,
  Python environment and selected Git client. A green manual command does not
  establish that the client invokes hooks.
- **Environment preparation fails:** use the first installation error and the
  configured proxy/network policy to diagnose it. A failed download is blocked
  verification, not a passing scan. Reuse a healthy cache; clear it only after
  preserving needed recovery patches.
- **Intentional file rejected:** review the narrow policy change with the owner
  and rerun the full check. Keep fixtures synthetic; do not blanket-exclude tests,
  docs or generated files. Store large datasets/model weights in a suitable
  artifact store when the project selects one.

Community cases informing these steps:
[managed hooks path](https://github.com/pre-commit/pre-commit/issues/1198#issuecomment-547963695),
[partial staging and recovery patches](https://github.com/pre-commit/pre-commit/issues/2648#issuecomment-1363198114).
Both are historical discussions; installation and staging behavior were also
checked against pre-commit 4.6.2 source and the integration lane.

Run the integration lane after preparing the hook environment:

```bash
python -m unittest discover -s tests/integration -v
```

It uses disposable Git repositories to exercise actual commits and failure
statuses. The existing `python -m unittest discover -s tests -v` lane remains
offline after installing its dependencies. See [maintenance](maintenance.md)
for reviewed hook and runner upgrades.
