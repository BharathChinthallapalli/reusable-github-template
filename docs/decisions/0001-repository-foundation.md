# 0001: Keep the shared foundation independent of the application stack

Status: Accepted for the template, subject to review by adopting projects.

## Context

The template must support several languages and deployment models. A framework,
database, identity provider, or cloud service selected here would impose that
choice on every project. Repository files also cannot activate GitHub's remote
access and merge settings.

## Decision

Provide lightweight repository tooling, CI, contribution conventions, ownership,
AI context, and operational worksheets. Use Python's standard library for setup
and checks. Keep cloud deployment and application dependencies out of the base.
Provide a disabled ruleset for explicit import and activation.

## Consequences

The base runs without package installation or cloud credentials. Each project
must add real application CI and document its stack. The initial green check
validates the foundation only. Rulesets, reviewers, and security products need
configuration by the repository owner.

## Alternatives

- One full-stack starter: faster for a single stack, less reusable elsewhere.
- Documentation-only template: simpler but misses executable setup and checks.
- Central workflows immediately: valuable at organizational scale, but requires
  a real owning repository, access model, and update process first.

Revisit when several projects share a stable stack or repeated workflow changes.
