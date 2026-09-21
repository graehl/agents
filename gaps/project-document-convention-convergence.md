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
and `AGENTS.global.md` accepts `docs/tactical/` while normally keeping `tasks/`
private. Neither establishes the meaning of Kyle's committed plan bundles.

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

Formal action plans are a distinct, task-like category from gaps/sketches.
For new projects they may belong in the committed record, potentially using
Kyle's `T-nnn` numbering rather than the user's current `tasks/nnn-` spelling.
Do not erase the legitimate private case: some shared repositories have no
appetite for committed plans, so the user's untracked `tasks/` remains useful.
Classify the artifact's audience/lifecycle and the repository's appetite before
choosing visibility or naming. This distinction is for review, not an approved
relocation of existing tasks.

**Interim interoperability:** Kyle's conventions are an "also look here"
read-only discovery target. Read existing `docs/plans/` and `docs/topics/`
where relevant, but do not start writing, migrating or creating artifacts in
that convention based on this gap. Its actual adoption needs a later decision.

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

Contributing-model: 6-Astra.
