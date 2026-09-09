# Discovery and bounded proof

## Recover the real requirement

Use a concrete recent example of the task to establish the current process:
who initiates it, what information they have, what they do, where it fails, and
what they do to recover. Distinguish a symptom from its suspected cause. A request
for a chatbot, microservice, or automation is a candidate solution until its
underlying need is understood; preserve a technology constraint when the user
has explicitly made it a requirement.

For every important claim, attach the supplied record, observation, repository
path, measurement, or accountable source. A forecast is not a baseline. Capture
domain terms and examples that reveal rules, especially exceptions and forbidden
state transitions. Keep divergent stakeholder needs visible instead of merging
them into an unsupported average user.

Classify constraints as fixed, negotiable, or unverified. Examples include data
access, supported environments, existing integration contracts, deadline, budget,
support capacity, and deployment scope. Investigate available project artifacts
before interrupting the user for facts already recorded there.

## Select the evidence-producing activity

| Remaining question | Activity | Evidence that answers it |
| --- | --- | --- |
| Can users understand this proposed flow? | Targeted demonstration or usability exercise | Observed task completion and confusion, with mocked behavior declared |
| Can this integration or algorithm work under a critical constraint? | Feasibility spike | Reproducible result at the real boundary, including failure behavior |
| Does the solution materially improve the user's task? | Proof of value | Comparable baseline and candidate outcomes on representative cases |

Define the experiment boundary before running: cases and data, environment,
measurement, criteria, execution owner, resource/time limits, and stopping rule.
Keep criteria stable during evaluation. If a requirement changes, record the
change and rerun affected comparisons rather than silently redefining success.
Use synthetic or approved data. Retrieve only the access needed by the task.

Measure the outcome at the user boundary. For example, faster generation alone
does not establish that a reviewed answer or completed task is faster. Include
human correction effort where it affects the claim. If samples are too few or
unrepresentative, report the limitation and an inconclusive decision where needed.

## Decide and hand off

Record what was built, what was real versus mocked, observed criterion results,
and the environment/revision. Separate acceptance evidence from assumptions
about scaling, identity, reliability, data handling, or ongoing support. Decide
whether to proceed, change the approach, stop, or gather a specific missing fact.
Do not relabel a prototype as production-ready because the demonstration worked.

## Sources and scope

Reviewed 2026-09-09. These are original procedures informed by selected sources,
not copied handbook text or a claim to have read complete books.

- [Microsoft: align technical strategy with business requirements](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/design-business-requirements).
  Read the listening-through-recommendation workflow; apply its separation of
  initial requests, motivations, measurable outcomes, and feasible constraints.
- [GitLab: proof of value](https://handbook.gitlab.com/handbook/solutions-architects/playbooks/pov/).
  Read the executive summary and evaluation definition. The page was a working
  draft; use its named ownership and outcome criteria as practice, not as a
  binding commercial process for another organization.
- [Architecture Patterns with Python: domain modeling](https://www.cosmicpython.com/book/chapter_01_domain_model).
  Read the author-hosted domain-language, behavioral-test, value-object, and
  entity sections, not the full book. Concrete business examples help discover
  rules that feature lists miss; no example code is imported.
