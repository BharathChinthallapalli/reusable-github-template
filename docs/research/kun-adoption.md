# Kun knowledge-layout review and adoption

Reviewed 2026-09-13 before implementation. Source:
[`kunchenguid/kun` at `2e2379571e43a5496d350ff9ebc095a21991c66d`](https://github.com/kunchenguid/kun/tree/2e2379571e43a5496d350ff9ebc095a21991c66d).
Template baseline: `93121920cf26c059aa90441e71da5c31c6851eff`, version 3.1.0.
The requested outcome is to adapt useful engineering guidance into the reusable
template and publish the implementation to its existing GitHub repository.

## Coverage and evidence

The complete seven-file tree was inventoried. README, ENTRY and the skill loader
were read in full. TOOLS was inspected for its entry contract and representative
tool descriptions. OPINIONS was inspected by headings and the engineering,
validation, context and interface sections; VOICE was inspected for its scope and
communication summary. This is selected-source review, not a full content audit.
No upstream skill, installer, model call, tool runtime or external automation ran.

| Source at the inspected revision | Observation | Template comparison and decision |
| --- | --- | --- |
| [ENTRY.md](https://github.com/kunchenguid/kun/blob/2e2379571e43a5496d350ff9ebc095a21991c66d/ENTRY.md) | Selects a different sequence for ideation, features, bugs, refactoring and explanations | Add one canonical task-shape table to the existing engineering workflow guide; root instructions and `engineer` route there. Reuse the current skills. |
| [OPINIONS.md](https://github.com/kunchenguid/kun/blob/2e2379571e43a5496d350ff9ebc095a21991c66d/OPINIONS.md) | Separates durable judgments and their evidence from operating instructions | Add a concise principles reference derived from the template's accepted ADRs and existing procedures. It explains tradeoffs and links the owner of each rule. |
| [TOOLS.md](https://github.com/kunchenguid/kun/blob/2e2379571e43a5496d350ff9ebc095a21991c66d/TOOLS.md) | Entries explain what a tool is, the problem it solves and how to use it | Add a problem-oriented guide to the tools actually shipped here, with prerequisites, commands, effects and limits. Link it from the generated AI catalog. |
| [OPINIONS.md: personal opinion maps](https://github.com/kunchenguid/kun/blob/2e2379571e43a5496d350ff9ebc095a21991c66d/OPINIONS.md#personal-opinion-maps-make-public-thinking-useful-to-agents) | Consolidates evolving evidence by concept instead of appending a chronological log | Extend the existing context skill and asset with claim classification, evidence/version, canonical destination, supersession and a recheck trigger. |
| [skills/kun/SKILL.md](https://github.com/kunchenguid/kun/blob/2e2379571e43a5496d350ff9ebc095a21991c66d/skills/kun/SKILL.md) | The small loader requires all four remote knowledge files in full on first invocation | Keep template guidance local and versioned, and read only the relevant route or reference. The four upstream files total 116,247 bytes at this revision; a small loader alone does not establish low context cost. |

The existing template already has independent review procedures, reproduction,
behavior-focused verification, bounded experiments, selective skill references,
and evidence-bearing handoffs. These remain the execution mechanisms. This work
adds usable navigation and a more explicit maintenance procedure rather than
claiming those capabilities are new.

## Adaptation boundaries

- Upstream judgments are attributed viewpoints, not platform guarantees or
  universal engineering rules. Template principles point to its current accepted
  decisions; conflicting project decisions must be resolved in their own context.
- The upstream workflow prefers Lavish for plans/explanations and no-mistakes
  for validation. Here the available project tools and proportional review apply;
  no external product, plan approval cycle or model is required by the new routes.
- TOOLS eligibility reflects the author's ownership and popularity criteria.
  This catalog instead includes shipped repository tools and documented project
  extension points; presence does not prove installation or authorization.
- The remote loader follows mutable `main` and requires network access. Generated
  template projects retain a local snapshot and upgrade through reviewed changes.
- VOICE describes Kun's personal identity. No persona, biographical claims or
  identity-specific tone are adopted into the shared template.
- README describes a daily external refresh. The inspected tree contains no
  updater implementation or workflow, so its execution was not verified and no
  background job is copied or created.

All additions are original project-specific writing. Upstream prose, skill
payloads and assets are not bundled. This review does not assign an upstream
license or change the template owner's outstanding licensing decision.

## Implementation and acceptance plan

1. Add task routing and a selectively loaded principles reference, linked from
   the current entrypoints. Preserve the 34 skills, 13 profiles and host settings.
2. Publish the repository tool reference from inspected CLI contracts; keep the
   generated AI catalog generated and existing command interfaces unchanged.
3. Update context-maintenance instructions and its reusable record to classify
   new evidence before changing the smallest canonical source.
4. Reconcile the existing ADD, validate planned paths, implement, review and seal.
   Bump the optional-addition version to 3.2.0 and provide consumer migration notes.
5. Run static checks, skill format checks, the offline and Git integration lanes,
   and disposable initialization. Exercise workflow selection and context updates
   with independent synthetic tasks. Record actual outcomes in
   [the validation record](kun-validation.md), separately from native host behavior.

The earlier macOS review identified two baseline path-alias failures. Record any
recurrence separately from new failures; this guidance change does not alter hook
path policy, scanner behavior, GitHub settings or application behavior.
