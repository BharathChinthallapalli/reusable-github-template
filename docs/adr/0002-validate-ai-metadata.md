# 0002: Validate AI metadata with a development-only YAML parser

Status: Accepted
Date: 2026-09-09
Supersedes: [0001: Independent repository foundation](0001-repository-foundation.md)

## Context

The template now includes custom agents and skills with YAML frontmatter.
Checking that files and metadata keys exist does not establish that the YAML
parses or that its values have the expected types. Malformed metadata can leave
instructions present on disk but unavailable to a coding agent.

Decision 0001 said the base required no package installation. Full validation
now needs a real YAML parser. This changes development checks, not the choice of
application language, framework, hosting, or runtime dependencies.

## Options

- Extend a hand-written parser: avoids a dependency but requires maintaining
  YAML semantics and risks accepting malformed input or rejecting valid syntax.
- Use a maintained YAML parser: adds a development dependency and an update
  obligation, while allowing checks to inspect parsed values reliably.

## Decision

Keep the stack-neutral foundation, standard-library initializer and foundation
checker, and separately activated GitHub settings from 0001. Add PyYAML 6.0.3,
an [MIT-licensed package](https://pypi.org/project/PyYAML/6.0.3/), pinned in
[requirements-dev.txt](../../requirements-dev.txt).
Use safe YAML parsing for AI metadata diagnostics; do not construct Python
objects from repository content.

The standalone AI diagnostics are optional to run locally and require the
development dependency. Full CI installs it; running the full test suite
requires it. It is not an application runtime dependency. Dependabot checks
the pip requirement weekly and proposes updates for review.

## Consequences and verification

The initializer and foundation checker still run without package installation.
Contributors running every check need the development requirements. Parser
updates can change accepted syntax or diagnostics, so review their diffs and
rerun the relevant tests before accepting an update.

Verify malformed YAML, invalid value types, and valid supported frontmatter;
keep regression cases for metadata failures the checker detects. Run foundation
checks and initializer tests too, so adding diagnostics does not change setup
behavior.

Static checks cannot prove that an installed host discovers a file, makes a
skill invocable, grants tools, or follows the instructions. Verify those in the
actual host when relevant; report untested behavior explicitly. Revisit this
decision if host formats change or parser maintenance outweighs its benefit.
