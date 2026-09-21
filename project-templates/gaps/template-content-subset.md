---
slug: template-content-subset
noticed: 2026-09-21
where: project-templates/ and its repository-relative dependencies
---

**Gap:** the template library needs a more intuitive, discoverable path subset
of this repository. Its usable content can include files outside
`project-templates/`, such as topics and skills. Downloading that directory
alone does not establish a complete source, and downloading the entire
repository hides which content actually belongs to the template task.

**User-directed scope:** refactor the source layout so a consumer can start at
the configured template path and discover its complete dependency closure.
A content directory plus carefully placed relative symlinks is a candidate,
not a settled directory name or a requirement to duplicate canonical files.
Preserve shared content owners and existing consumers when reorganizing paths.

Review included content for suitability for the intended task, not merely
whether every link resolves. The existing
[portable capability review](portable-capability-bases.md) owns the editorial
acceptance criteria; [content authoring](content-authoring-capabilities.md)
owns the writing-specific remainder. This gap owns organization and explicit
retrieval boundaries, without duplicating those reviews.

**Fix sketch:** inventory the manifests, symlinks and routed resources for
App canvas, Storybook and Web page; establish a legible entry subtree and
explicit links to any shared content outside it. Keep links relative and
within this repository. Make transitive dependencies mechanically discoverable
rather than relying on a consumer to guess paths from arbitrary prose.
Review every included instruction/resource against its task and remove or
conditionally route irrelevant material without leaving dangling references.

**Closure evidence:** from one immutable revision, retrieve the entry subtree
and only its discovered dependencies; compose the three templates and compare
their bytes/modes with a full-checkout composition. Verify source/link closure,
the reviewed content choices, and that created projects still build, test and
use supported add-ons after the source checkout becomes unavailable. A smaller
download alone does not establish task suitability.

YA's corresponding retrieval work is tracked in
`~/ya/gaps/project-template-selective-retrieval.md` (repository
`graehl/yepanywhere`, path `gaps/project-template-selective-retrieval.md`).
YA's default source is this repository on GitHub with content root
`project-templates`, overridable in configuration; a standalone repository is
not required for this work. This entry records future work, not a layout change.

Opened 2026-09-21 during YA template-source clarification.
Contributing-model: 6-Astra.
