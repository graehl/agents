# Software aesthetic — coordinated rules

Rules here pay off only when observed project-wide. Apply to greenfield projects or ones that already follow them consistently. Introducing them into a project that doesn't observe them adds cost without benefit until coverage reaches a threshold.

For universal per-unit rules, see [software-aesthetic.md](software-aesthetic.md).

## Boundary discipline

Validate only at system boundaries (user input, external APIs); trust internal code and framework guarantees downstream. Do not add validation or error handling for scenarios that cannot occur given upstream guarantees. This only holds when the whole codebase maintains the boundary — in a mixed codebase, validate defensively.

## Error handling

Concentrate error handling at execution or load-time boundaries; rely on exceptions rather than threading error state through call chains. Requires consistent exception discipline throughout the project.

## Input normalization

Liberal-accept: absorb input variation at the boundary (with or without a warning) so that interior code can assume a normalized form. Only works if the normalization boundary is maintained everywhere input enters the system.

## Output contracts

Fix+warn: at the output stage, detect problems, fix them, warn, and keep output strictly well-formed — rather than failing or silently misbehaving. Apply only where the system's error-handling philosophy calls for defensive recovery rather than hard failure.

## Canonical utilities

Reuse existing canonical utilities rather than creating bespoke near-duplicates. Logic belongs in the module that already owns the concept. Requires an established and consistently maintained canonical layer; in a project without one, this is aspirational rather than actionable.

## One spelling per concept

<!-- speculative: adopted 2026-09-15 with software-aesthetic § Names are search queries; see software-aesthetic.evidence.md -->

Pick `organizationId` or `orgId` and use it everywhere; every synonym halves every future search. Reuse the vocabulary already in the codebase being edited rather than coining a near-synonym; where the project has a `GLOSSARY.md`, it is the arbiter. Pays off only when the whole codebase holds to it; in a mixed codebase, match the nearest neighbors of the edit.

## Colocated tests

<!-- speculative: see § One spelling per concept -->

Put a unit's test beside it (`foo.test.ts` next to `foo.ts`) so one search finds behavior and its specification together. Where the project already keeps a separate test tree (common in Python), follow it; introducing colocation into such a project splits the test corpus.
