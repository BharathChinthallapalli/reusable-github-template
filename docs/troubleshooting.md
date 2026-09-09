# Troubleshooting

Start with a reproducible symptom and the exact version that failed. A forum
answer suggests a hypothesis; verify its assumptions against the repository
and current official documentation before applying a fix.

## Investigation record

Keep one compact record in the issue or incident notes. Use links to permitted
evidence and sanitized excerpts; do not attach credentials or private datasets.

| Field | Record |
| --- | --- |
| Symptom | Expected result, actual result, affected operation and impact |
| Environment | Client, extension, runtime and operating-system versions that matter |
| Revision and execution | Commit SHA or application version; CI run URL, attempt and event when relevant |
| Reproduction | Minimal steps, synthetic input, prerequisites and frequency |
| First causal error | Earliest failure that explains the symptom, with surrounding context; separate downstream errors |
| Evidence and hypothesis | What was observed, what is inferred and the smallest check that separates competing explanations |
| Chosen fix | Specific change, why it addresses the cause, and the applicable official documentation |
| Validation | Exact command or reproduction steps, revision/environment, result and remaining gap |
| Outcome | Confirmed fix, workaround or unresolved; follow-up owner when needed |

Use **confirmed fix** when the relevant reproduction and checks support the
correction. Use **workaround** when the symptom is avoided but the underlying
cause remains. Use **unresolved** when evidence does not establish a repair.
A successful retry alone does not establish the cause of the original failure.

## Git state determines the recovery

Inspect `git status`, the current branch and its upstream, and recent history
before changing Git state. Preserve uncommitted work before integration or
recovery. Use a focused change rather than a blanket cleanup command.

| Symptom | Check and appropriate next step |
| --- | --- |
| Push rejected as non-fast-forward | Fetch the relevant remote and inspect the divergent commits. Integrate remote changes with the project's merge or rebase workflow, resolve conflicts and verify before pushing. Preserve collaborators' commits; plain force push is not the default fix. See [GitHub's guidance](https://docs.github.com/en/get-started/using-git/dealing-with-non-fast-forward-errors). |
| An ignored file still appears in changes | Check whether it is already tracked. When it should become untracked, remove that specific path from the index with `git rm --cached -- <path>`, keep its ignore rule and review the staged deletion. Other checkouts can receive that deletion. See [gitignore](https://git-scm.com/docs/gitignore) and [git-rm](https://git-scm.com/docs/git-rm). |
| Merge is still in progress | Resolve the conflicting changes and continue, or use `git merge --abort` to abandon the operation. Abort may not reconstruct changes that were uncommitted before the merge. See [git-merge](https://git-scm.com/docs/git-merge). |
| Merge completed locally and has not been shared | Identify the intended pre-merge commit using history/reflog. For a just-completed merge, verify `ORIG_HEAD` before considering `git reset --merge ORIG_HEAD`; later operations can change that reference. Preserve local work and compare the result with the intended state. See [git-reset](https://git-scm.com/docs/git-reset). |
| Unwanted merge has already been shared | Coordinate a history-preserving revert through the normal review process. Select the correct mainline parent for a merge commit and consider its effect on later merges. See [git-revert](https://git-scm.com/docs/git-revert). |

Removing a file from tracking does not remove its history. If it contains an
exposed credential, revoke or rotate it first; follow
[GitHub's sensitive-data guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
for any further cleanup. Do not use `reset --hard` as a general recovery recipe.

## CI is pending or green on a different run

Compare the required check's exact name and source with the emitted check, then
identify the commit that must pass: the latest head, test merge or merge-queue
commit. Record the event and attempt. An earlier successful run does not prove
the required revision passed.

Inspect branch/path filters, conditions, concurrency, approval gates and job
dependencies. A workflow skipped by a filter can leave a required check pending;
a skipped job has different reporting behavior. If a merge queue is used, check
the `merge_group` trigger. Preserve the `Repository checks` name used by this
template's ruleset. Follow [required-check troubleshooting](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks)
and the [Actions diagnosis guide](../.agents/skills/github-actions-debug/references/diagnosis.md).

## AI instructions, skills or agents are missing

Use the discovery checks in [AI assistance](ai-assistance.md). Record the actual
client and extension version, workspace root, file path and diagnostic message.
Distinguish a file that is not discovered from a discovered skill that was not
selected for a task. Check the supported host behavior before changing paths,
frontmatter or settings; repository files alone do not start an agent session.

For application failures involving an external dependency, retry, queue, cache
or authorization boundary, select relevant checks from
[verification](../.agents/skills/verify-change/references/verification.md) and
record operational recovery in [operations](operations.md).
