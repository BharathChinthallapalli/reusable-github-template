# Research and design evidence

Reviewed on **9 September 2026**. This is a synthesis of first-party examples and
current official documentation, not a ranking of companies or a claim about
their internal engineering standards.

- [Seven company examples](company-comparison.md): GitHub, Microsoft, Azure,
  Vercel, and historical Google/Azure examples; observed files and adopted patterns.
- [GitHub guidance](github-guidance.md): template behavior, ownership, rulesets,
  Actions security, dependency maintenance, feature availability, and verified action commits.
- [Design decision](../decisions/0001-repository-foundation.md): why the foundation
  stays independent of the application stack.
- [Validation record](../../VALIDATION.md): local evidence and limits.
- [AI defaults](../ai-assistance.md): agents, skills, clean-code
  guidance, current discovery settings, and host validation steps.
- [Community lessons](community-lessons.md): version 1.2 adjustments, original
  creator material, reported failures, confirmed fixes, and research limits.
- [Public repository review](repository-review.md): 494 public account repositories,
  two targeted AI repositories, complete inventories, source samples, and hook decisions.

## How the research affected the deliverable

| Finding | Implementation |
| --- | --- |
| Corporate starters contain project-specific identities and policies | Initializer supplies real project metadata, ownership, and private reporting contact |
| Application starters are not general repository governance | Core has no framework, database, cloud account, or production deployment |
| GitHub files and platform settings have different lifecycles | Disabled ruleset plus separate import, verification, and activation instructions |
| Immutable action references require an update process | Verified SHAs and weekly Dependabot version updates |
| A new repository cannot inherit application-specific test evidence | CI is explicitly named and documented as foundation validation |
| Template copies do not receive future updates automatically | Version record and reviewed maintenance process |
| AI assistants need real repository context | Short AGENTS.md and Copilot files reference maintained project facts and real commands |
| Current cloud identity defaults differ from older tutorials | Azure guide describes immutable and earlier OIDC subjects, requiring exact claim matching |

Some first-party sample files do not implement every practice in current GitHub
security guidance. Where they differ, this template follows current guidance
rather than reproducing the sample verbatim. Archived examples are explicitly
identified and used only to discuss historical structural patterns.

## Further official references

- [Repository-wide, scoped, and agent instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions)
- [Ruleset API fields](https://docs.github.com/en/rest/repos/rules#create-a-repository-ruleset)
- [Dependabot configuration options](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference)
- [GitHub OIDC claims](https://docs.github.com/en/actions/reference/security/oidc)

The research is original paraphrase with links. No company endorsement, company-wide
adoption, or production certification is implied. Recheck release versions and
feature support when adopting the template in a different GitHub environment.
