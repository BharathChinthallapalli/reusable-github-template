# Lessons applied from creator material and community reports

Checked 9 September 2026 for template version 1.2.0. This is original synthesis.
Community reports establish particular observed failures; they do not establish
failure rates or universal product behavior. Recheck versions and resolution
status before applying a workaround.

## Video coverage and source limits

The user supplied four videos. Direct analysis failed for all four; full
transcripts were not available. The following accessible material supports the
changes, without claiming the videos were watched end to end:

| Video | Material actually reviewed |
| --- | --- |
| [Git & GitHub Crash Course](https://www.youtube.com/watch?v=mAFoROnOfHs) | Sumit Saha's [companion handbook](https://www.freecodecamp.org/news/learn-how-to-use-git-and-github-a-beginner-friendly-handbook/): working tree, index, commits, remotes, branching, and recovery |
| [Software Fundamentals Matter More Than Ever](https://www.youtube.com/watch?v=v4F1gFy-hqg) | Matt Pocock's [architecture article](https://www.aihero.dev/how-to-make-codebases-ai-agents-love), [small vertical slices](https://www.aihero.dev/tracer-bullets), and [current TDD guidance](https://www.aihero.dev/skills-tdd) |
| [The Only GitHub Guide You'll Ever Need](https://www.youtube.com/watch?v=pJYOG6klqj8) | Title and a short introductory excerpt only; no implementation decision is attributed to the full video |
| [System Design for Beginners](https://www.youtube.com/watch?v=SE2KF-vxvS0) | KodeKloud's [official course description and syllabus](https://kodekloud.com/courses/system-design-for-beginners): requirements, access patterns, incremental components, introduced failure modes, and recovery labs |

The practical application is clear project vocabulary, explicit interfaces,
small verifiable changes, and architecture choices justified by the current
problem. No framework, module-size rule, fixed test quota, or infrastructure
stack follows automatically from these sources. Code-quality judgments retain
the [clean-code skill's source boundary](../../.github/skills/clean-code/references/sources.md).

Pocock's August TDD guide acknowledges configuration tests that merely repeat
implementation, unclear test boundaries, and imperfect instruction adherence.
Our verification procedure selects observable behavior and meaningful checks.
It does not require a test-first loop for every prose or configuration edit.

## Concrete community findings

| Report | Evidence and status when checked | Applied response |
| --- | --- | --- |
| [GitHub Community #30724](https://github.com/orgs/community/discussions/30724) | GitHub Support's accepted answer explains pending required checks caused by matrix check-name mismatches | Keep the stable check name; inspect name, source, SHA and event before rerunning or changing protection |
| [VS Code #321765](https://github.com/microsoft/vscode/issues/321765) | Agent metadata sometimes failed to load after restart. Open; saving the file was a reporter workaround, and a maintainer requested a newer-version retest | Separate static validation from inspection of actual available tools and host metadata |
| [VS Code #334454](https://github.com/microsoft/vscode/issues/334454) | Custom skill locations were not inherited by submodules; open. Current docs deprecate that location setting | Keep standard discovery directories and record the opened workspace root |
| [VS Code #334590](https://github.com/microsoft/vscode/issues/334590) | A valid skill was visible to one agent runtime but missing in another. Closed with Insiders release and verification-needed labels | Record runtime and version; do not treat file presence or patch availability as successful invocation |
| [Pocock discussion #847](https://github.com/mattpocock/skills/discussions/847) | Users describe contradictory decisions both marked accepted. Visible status, supersession links and an index are community proposals | Require explicit status and links when decisions change; investigate conflicting accepted decisions |
| [Pocock discussion #1028](https://github.com/mattpocock/skills/discussions/1028) | Proposal for diagnostics cites missing dependencies, unreachable skills, name collisions, and host differences | Add bounded static checks and a separate manual host check; do not claim full host/dependency-graph validation |
| [Tracked files and gitignore](https://stackoverflow.com/questions/1274057/how-do-i-make-git-forget-about-a-file-that-was-tracked-but-is-now-in-gitignore) | Accepted answer matches Git's index semantics | Explain ignored files, tracked files and retained history separately |
| [Undoing a local merge](https://stackoverflow.com/questions/2389361/undo-a-git-merge-that-hasnt-been-pushed-yet) | Accepted answer contains alternatives with different effects, including destructive ones | Identify merge state and preserve work; do not copy a hard reset as a generic fix |

Current technical checks used [Git ignore semantics](https://git-scm.com/docs/gitignore),
[Git merge recovery](https://git-scm.com/docs/git-merge),
[Git pull modes](https://git-scm.com/docs/git-pull),
[required status checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks),
[VS Code skills](https://code.visualstudio.com/docs/agent-customization/agent-skills),
and [custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents).
For example, `git pull` behavior depends on its options/configuration; a merge
can fast-forward without a merge commit. Tutorial simplifications are not
repository operating rules.

## Delivery boundaries

The template adds diagnostics, maintained context/decisions, and evidence-based
troubleshooting. It does not install community skill collections, provision
services, run agents continuously, or establish that a client's model complies
with instructions. See [validation](../../VALIDATION.md) for checks actually run.
