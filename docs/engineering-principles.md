# Engineering principles and their sources

Use this reference when choosing between plausible engineering approaches. It
summarizes this template's accepted decisions and procedures; it is not a second
policy authority. Read the linked source when its contract matters. Current
project requirements, accepted decisions and the user's authorized scope govern
the work. A material contradiction belongs in the [decision process](adr/README.md).

## Begin with an observable result

Describe the user, input and expected result before choosing a mechanism. A
passing foundation check establishes the scaffold's health, not application
success. For an ambiguous request, identify the smallest proof that would resolve
the uncertainty; for an agreed correction, proceed to the relevant work.
See [project context](project.md), [task routing](engineering-workflows.md#choose-the-task-route)
and [ADR 0006](adr/0006-evidence-based-engineering-workflows.md).

## Let demonstrated needs justify complexity

Prefer the existing toolchain and the smallest change that satisfies the actual
contract. A new abstraction, dependency, service or agent needs a concrete problem
it solves. Separate a requested behavior change from refactoring that should
preserve behavior. When two alternatives remain credible, compare their effect
on the known constraints and choose the one whose tradeoffs the task supports.
See [clean-code design decisions](../.agents/skills/clean-code/references/design-decisions.md)
and [planning](../.agents/skills/implementation-planning/SKILL.md).

## Match evidence to the claim

Use a reproducer for a defect, preservation checks for a refactor, and a real
consumer path for a feature. Reuse sufficient existing checks. Expected results
must come from the contract, not merely mirror what the implementation returns.
Independent review examines the original request and actual diff. Report missing
evidence explicitly and distinguish static validity from native host invocation.
See [verification](../.agents/skills/verify-change/SKILL.md),
[review](../.agents/skills/code-review/SKILL.md) and
[ADR 0004](adr/0004-portable-engineering-capabilities.md).

## Keep choices portable and context selective

Repository tools maintain the foundation without selecting an application stack.
Use project manifests and configured tools for application work. Read only the
skill and reference needed for the current question. Keep shared guidance in its
canonical local file, so every generated project can review and version changes.
See [repository tools](repository-tools.md),
[ADR 0006](adr/0006-evidence-based-engineering-workflows.md) and
[ADR 0007](adr/0007-local-engineering-guidance.md).

## Separate engineering evidence from authority

A ready design, passing check or agent recommendation does not grant credentials,
publication rights or approval on another person's behalf. Complete work already
authorized by the task, and make any genuinely outstanding decision concrete.
Use isolated work and bounded assignments when parallel work warrants them.
See [ADR 0005](adr/0005-scoped-agent-design-gate.md) and
[task orchestration](../.agents/skills/task-orchestration/SKILL.md).

## Maintain a current explanation, not an accumulating log

Revise the canonical claim when evidence changes. Fold duplicates into their
owner, retain a pointer to historical reasoning, and keep run-specific state in
the task record. Evidence needs scope and revision: one environment's workaround
is not a universal rule. See
[context maintenance](../.agents/skills/context-maintenance/SKILL.md) and
[ADR 0007](adr/0007-local-engineering-guidance.md).

The separation of routing, judgment and tool knowledge was informed by the
[Kun source review](research/kun-adoption.md). These are original summaries of
the template's own decisions, not the author's personal opinions or persona.
When a source decision changes, revise its summary here in the same change.
