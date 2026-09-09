# Operational evidence and handoff

## Bind evidence to the transition

State the artifact revision, environment, configuration, data scope, and intended
operation. Evidence from a local mock or different tenant cannot establish a live
integration's behavior. Configuration drift can invalidate previous checks;
repeat only the checks whose assumptions changed.

Use these evidence states consistently:

| State | Meaning |
| --- | --- |
| Documented | A procedure or intended behavior exists |
| Statically checked | Configuration or source was examined by a named check |
| Exercised | A named operation ran in a recorded environment with captured results |
| Observed in operation | Runtime evidence supports behavior under stated conditions |
| Missing / blocked / failed | The needed evidence is absent, inaccessible, or contradicts the claim |

These states are not interchangeable readiness levels. A narrowly exercised
happy path does not cover an untested recovery requirement.

## Select consequential checks

For service takeover or production preparation, inspect:

- **Reproduction:** Can the recipient identify the artifact, required versions,
  configuration names, setup/run commands, and expected healthy result?
- **Ownership:** Is there an accountable service owner and a workable route for
  support, incidents, dependency changes, and unresolved decisions?
- **Access and data:** Do documented identity and authorization boundaries match
  the intended environment? Are data retention and restore requirements known?
  Share configuration names and approved access paths, never credentials.
- **Visibility:** Does a signal distinguish user-impacting failure from an idle
  system? Can logs/traces correlate an operation without exposing secret data?
  An alert rule existing is different from its delivery being exercised.
- **Recovery:** Is retry safe for the specific operation? What survives partial
  failure? Can the required state be restored and the business result reconciled?
- **Change:** Are deployment order, backward compatibility, rollback or
  compensation limits, and post-change verification understood?
- **Capacity and cost:** Where applicable, what measured workload, budget,
  consumption limits, and support capacity justify the operating assumptions?

Choose depth from actual requirements. Do not impose a 24/7 on-call model,
multi-region design, or invented recovery target on every project. Where targets
matter but are unknown, state the decision gap and responsible owner.

## Recover and transfer ownership

A backup job succeeding does not prove restore works. An infrastructure rollback
does not necessarily reverse a data mutation or external action. Record restore
or reconciliation steps, data-loss limits, and conditions for stopping retries.
Use existing runbooks and actual error evidence to make recovery actionable.

Separate disposable proof code and mocked connections from supported production
paths. Handoff the tested slice, reproducible evidence, known limitations,
remaining work, owners, and next decision. If external access is unavailable,
complete local preparation and identify the exact unverified boundary.

## Sources and scope

Reviewed 2026-09-09. Original guidance based on selected public articles, not a
vendor certification or a claim to have read an entire architecture framework.

- [Microsoft: architect fundamentals](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/fundamentals).
  Read responsibility and supportability sections; architecture includes
  operational visibility and support through the workload lifecycle.
- [Microsoft: architecture specification](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-design-specification).
  Read the article's recovery and implementation details; connect relevant
  recovery targets to how the design and its operational evidence meet them.
- [Microsoft: workload and platform collaboration](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/collaboration).
  Read the substantive article; distinguish a PoC's evidence from production
  code, and make temporary debt explicit and repayable.
- [Microsoft ISE design reviews](https://microsoft.github.io/code-with-engineering-playbook/design/design-reviews/).
  Read the article's review and documentation guidance; preserve artifacts that
  help the receiving engineering team operate and evolve the result.
