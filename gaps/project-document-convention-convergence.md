---
slug: project-document-convention-convergence
noticed: 2026-09-21
where: TOPICS.md, AGENTS.global.md, project-templates/bases/base
---

**Gap:** committed project documentation, planning, proposals and issue records
are not yet explicitly mapped between this instruction set and collaborator
conventions. Baking directory defaults into portable templates now could create
parallel hierarchies or imply agreement about privacy/lifecycle that does not
exist. Convergence, or at least mutual understanding, is a standing user goal.

**Noticed while:** designing redoc and default project-template directories.
The user reports that Kyle, a frequent collaborator, recently created a project
with `docs/plans/T-nnn-descr.md`, corresponding `T-nnn/` directories, and
`docs/topics/`. The topics serve the same purpose as ours; that project has not
been inspected here. `TOPICS.md` already permits established `docs/topics/`,
and the earlier global policy accepted `docs/tactical/` while normally keeping
`tasks/` private. Neither established the meaning of Kyle's committed plan bundles.

**Fix sketch:** inspect representative repositories together with Kyle's actual
conventions and make a compact semantic mapping for topics, evidence companions
(`.evidence.md`), gaps/issues, sketches/proposals, plans, and tasks. Determine
what is committed versus private; what is a durable aspect contract versus a
temporary work item; numbering, linked subdirectories, evidence placement,
retrieval triggers, status and closure/migration rules. Prefer one canonical
home plus pointers over duplicate trees. Convergence need not force identical
spelling where both layouts have an explicit, understood correspondence.

**User preference for that comparison:** do not put core semantic collections
under a generic `docs/` wrapper. Prefer root `gaps/` for bugs/unresolved work
and `gaps/sketches/` for tentative proposals, and root `topics/`
for long-term, converging or mostly stable developer documentation. User-facing
material may overlap with or be referenced from topics. User documentation
starts with README and its links; prefer `doc/` for additional human-audience-only
material, for example marketing/publication content. Compare these meanings
against Kyle's organization instead of assuming his `docs/...` spelling should
become the shared default. This records a preference to reconcile with current
gap/sketch/task policy, not a silent global policy or directory migration.

Formal action plans in Kyle's repositories remain a distinct discovery
category. Do not adopt his `T-nnn` numbering or relocate his files. The user's
own convention now uses gaps for unresolved work and handoffs for continuity;
visibility follows the artifact's audience and the repository's policy.

**Interim interoperability:** Kyle's conventions are an "also look here"
read-only discovery target. Read existing `docs/plans/` and `docs/topics/`
where relevant, but do not start writing, migrating or creating artifacts in
that convention based on this gap. Its actual adoption needs a later decision.

The interim discovery mechanism now lives in `AGENTS.global.md` under
First-run maintainer document discovery: a foreign repository lacking
`AGENTS.local.md` gets a private, Git-excluded table of its actual conventions
and an additive read-search instruction. YA's existing local instructions
received that table by explicit request. This addresses discovery, not the
remaining choice of shared authoring conventions or template directory defaults.

Before choosing default template locations or shipping empty topic/plan
directories, record the agreed mapping and identify any policy/helper changes.
The user prefers instructions naming default paths, with directories created
only when a file belongs there, rather than empty directories or `.gitkeep`
scaffolding. This matters especially for project types that may never need
tests or executable helpers. Application code defaults to project root,
without a compulsory `src/` wrapper; `tests/` and `scripts/` are preferred when
such artifacts exist. Existing project conventions still take precedence.

Consider a small set of additional purpose-based defaults in that review:
test fixtures under `tests/fixtures/`; maintained developer/operator helpers
under `scripts/`; explanatory images/diagrams beside their owning docs;
human-only publication assets under `doc/` when appropriate; app-served static
assets in the stack's actual public-assets directory; reproducible examples
under `examples/` only when useful. Keep
generated build output, temporary captures and private continuity state out
of committed source/documentation collections. These are review candidates,
not a requirement to ship a directory or impose every category on each project.

Template instructions should encourage agents to maintain useful cross-session
plans and aspect-based topics autonomously as consistency aids. Users, including
children, should not need to know, name or manually administer those artifacts.
Keep this proportional to actual project needs; redoc should make the hierarchy
legible and truthful, not create ceremony or empty paperwork to satisfy a tree.

**Closure evidence:** a reviewed mapping grounded in both conventions, a fresh
agent able to locate purpose/decisions/open work in either layout without chat
history, and template defaults that do not duplicate an established hierarchy.
Do not close merely by renaming directories or adding compatibility wording.

## Resolutions — 2026-09-21

Contributing-model: 6-Astra

- Extend this existing gap for the active convergence pass; no duplicate gap
  is needed. A temporary gap is useful even for a one-session change when it
  records the mismatch and chosen resolution. Small direct fixes need no
  obligatory gap. Most gaps close in one session; others may span arbitrarily
  many sessions and handoffs.
- Write settled intended-final-state contracts in their existing topic owners
  before closure, marking intended versus implemented where migration remains.
  [Handoffs](../topics/handoffs.md), [TOPICS.md](../TOPICS.md), and
  [gap lifecycle](README.md) own these decisions; no duplicate final-state topic.
- Retire `tasks/` as an authored convention. Gaps hold unresolved work;
  handoffs hold compiled continuity. Existing files are retained as readable
  evidence, not deleted or moved by this policy change. The retirement ledger
  cites the pre-change revision for retrospective recovery.
- A program is a coherent subproject in any domain. Default handoffs to the
  most specific owning program, with project root as fallback. The last
  explicitly specified handoff stays live for its scope, including before
  foreseeable token exhaustion. `ROOT` and `<program-path>/ROOT` may be
  temporary latest-handoff pointers; neither overrides a named scope.
- Keep Kyle's `~/ya` and `kzahel/aitutor` conventions as read-only comprehension
  through the existing first-run `AGENTS.local.md` discovery-table mechanism.
  That mechanism remains; this pass does not adopt or migrate his layout.
- Global boot carries the immediate steer and route. Conditional handoff,
  scheduling, and authoring details belong at the action that needs them.
  Installation is direct global-policy and skill symlinks; the installer is
  optional convenience, not a prerequisite.

**Current pass:** these resolutions and the user's global-text edits are
applied across the active instruction consumers. Static scenario review and
retired-rule searches cover the named-scope/ROOT, nested-program, partial-topic,
and read-only maintainer cases. Existing historical files remain in place.

**Remaining:** the user requested a full crawl of the global boot and scoped
activation hierarchy, including RESEARCH, RUNS, and TOPICS, for pruning,
scoping, and relocation. The comparative semantic mapping and template defaults
above also remain. `scripts/commit-msg-lint` still rejects subjects over 65
characters; the newly stated length aim is not yet reflected in that helper.
This gap stays open until its closure evidence is met.
