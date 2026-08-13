# Research discovery and direction decisions

> Rules and rationale for field surveys, frontier mapping, and skeptical research-advisor handoffs.

Read this packet before field-survey, prior-art, or direction-ranking work, and
when a material research decision or changed evidence state triggers the
research advisor. `RESEARCH.md` is the router and wins on conflict.

## Binding rules

### Field surveys and frontier mapping

For field survey, prior-art, or direction-ranking work, load in order:

1. `literature-search.md` — retrieval and citation snowballing;
2. `field-map.md` — field organization and maintenance; and
3. `frontier-map.md` — provisional claims, voids, and capstone questions.

Resolve repo-root files first, then `~/agents/`; report a missing trigger target
once and continue. Search shared `~/agents/surveys/<field>/` before extracting a
field afresh from any repo. A survey's `survey.md` is the map and
`concepts/<short>.md` holds read-backed per-concept understanding. A paper
references and extends the shared survey rather than duplicating its extraction
cache, except for paper-specific overlap material. The full survey schema is
`topics/research-survey.md`.

### Research-advisor handoff

Use one durable logical research advisor per declared research program, with
the project-wide fallback for standalone/cross-program work. Invoke the
applicable advisor once for each new decision/evidence state that:

- commits to, reverses, parks, or revives a material direction, architecture,
  evaluation regime, or program specification;
- changes the causal story after a surprising, weak, or null result;
- promotes a provisional claim or uses it to justify a material next step;
- consolidates local results into a paper, progress report, or portfolio
  narrative;
- completes the intended v1, rename, retirement, or role change of a program
  working document, or completes the intended v1, scope/path change, or
  retirement of a live handoff for that program; or
- operationally addresses the advisor (tell/ask advisor).

Treat the advisor as a proxy for a critical reviewer of the paper or program
material it follows and the directly linked evidence needed to read that
material. The user and working session normally have broader program context
and greater familiarity. Interpret comments first as document-repair evidence:
correct verified inconsistencies, and state consequential exclusions or
boundaries when a reviewer asks why something is absent. Preserve user-laid
plans unless independently verified evidence or a governing artifact changes
them. Verify alleged factual or methodological errors directly. Ask at most the
immediate clarification needed to locate or understand a criticism; do not ask
the advisor to accept a rebuttal or wait for convergence before continuing.
Do not outsource your decisions. The user or working session retains
object-level decisions unless a cited user instruction or governing artifact
explicitly delegates one. State the worker's proposed choice and rationale,
then ask the advisor for findings and arguments for and against it. Do not ask
the advisor to choose or rank what the worker should do, or to authorize,
permit, deny, or veto a run, resource allocation, priority, acceptance
decision, or plan. After the memo, the worker separates verifiable claims from
advice and makes its own decision. Report that the advisor supported or
opposed an action, never that it authorized or denied one.
Track this calibration in the
[`frontier-capability-review`](../topics/frontier-capability-review.md)
register and reassess it at the first instruction-policy review after each
major frontier-model generation.

Load and follow `research-advisor.md` for scope resolution, packet
deduplication, followed-document state, semantic reconciliation, and the
challenge memo. Do not substitute “advisor review would help” for invocation.
Routine plumbing, frozen sweep cells, and unchanged claim/decision states do
not trigger it. A topology-only notification is a `tell`. The trigger is the
coherent intended-v1 or completed-change boundary, not file creation, first
touch, or first line. Deliver promptly—normally in the next advisor interaction,
or as its own `tell` when none is otherwise due. It may be bundled or briefly
deferred, but remains owed and is delivered before the working session ends or
transfers its scope.


## Retained detail and examples

### Field surveys and frontier mapping

Three companion files cover field-survey work, in pipeline order:
- `literature-search.md` — the **retrieval method**: citation snowballing from
  trusted anchors (paper-DB relevance/citation scores), with keyword search
  filtered by a known-labs/authors prior for the freshest, not-yet-cited work.
  Finds the papers the other two organize and rank.
- `field-map.md` — building and maintaining a survey's field map for
  research, instruction, or prior-art reconnaissance on a subtopic.
- `frontier-map.md` — provisional-claim intake, void mapping, and
  capstone-question suggestion built on top of a field map.

Load them (repo root first, then alongside this file in `~/agents/`) when
the task is to survey a field, gather prior art before planning a solution,
or rank unexplored research directions. If a triggered file is missing,
report once and continue.

Field surveys are standalone, cross-branch reference material under
`surveys/<field-slug>/`, not branch-scoped `research/` artifacts. When a
`surveys/<field-slug>/` covering a paper's field exists, the paper's
related-work should **reference and extend that shared survey's
`related-work/` extraction artifacts** rather than maintain a private
duplicate. Keep a per-paper `research/<paper-name>/related-work/` only when
no `surveys/` subdir covers the field, or for the paper-specific
overlap tier (suspected proposal-overlap papers) that does not belong in a
general field survey. A paper that draws on a survey should cite the
`surveys/<field-slug>/` path so a future agent can find the shared map.

**Canonical, cross-repo.** The shared field surveys live under
`~/agents/surveys/<field-slug>/`. Research or prior-art work in **any** repo —
including one whose own tree has no `surveys/` (e.g. `~/draft`) — should search
them there before extracting a field afresh, and resolve a bare
`surveys/<field-slug>/` reference to `~/agents/surveys/` when the current repo
has none. Within a survey, the two things to search and cite are the `survey.md`
map and the read-backed per-concept **`concepts/<short>.md`** digests — each our
distilled understanding of one paper/idea, keyed by a short handle and read from
a git-ignored full-text extract. `concepts/` is a survey-scoped convention,
distinct from repo-wide `topics/` (cross-cutting contracts); it is the
understanding-page tier defined in `topics/research-survey.md`.

### Research-advisor handoff

Use one durable logical research advisor per research program; its provider
session is a replaceable serving incarnation.
Discover programs by the `Research program:` declaration in
`research/<program>/GLOSSARY.md`; their advisors live at
`research/<program>/advisor/`. Root-level standalone papers and cross-program
syntheses use the project-wide fallback at `research/advisor/`. The object-level
research session **must invoke the applicable advisor once** for each new
decision/evidence state satisfying any of these conditions:

- before committing to, reversing, parking, or reviving a material research
  direction, architecture, evaluation regime, or program-level specification;
- when a surprising, weak, or null result changes the causal story or motivates
  a rescue explanation or another conceptual branch;
- before promoting a provisional claim to a supported conclusion, or using it
  to justify a material next step;
- when a paper, progress report, or portfolio synthesis consolidates several
  local results into one research narrative;
- when the session completes the intended v1, rename, retirement, or role
  change of a human-readable program working document, or completes the
  intended v1, scope/path change, or retirement of a live handoff for that
  program; and
- whenever graehl operationally addresses or refers to the advisor, including
  `tell advisor ...`, `tell the advisor ...`, `ask advisor ...`, and
  `ask the advisor ...`.

Invocation obtains a bounded critical review; it does not delegate the
decision. Do not outsource your decisions. Unless a cited user instruction or
governing artifact explicitly says otherwise, the worker owns research
direction, run and resource choices, priority, acceptance, and execution. A
packet states the worker's proposed choice and rationale, then asks for
findings and arguments for and against it. It does not ask the advisor to
choose or rank what the worker should do, or for permission or a veto. The
worker evaluates the answer as advisory input rather than reporting that the
advisor authorized or denied the action.

Working documents and live handoffs are separate classes. Report both through
the packet fields in `research-advisor.md`; neither notification automatically
makes its path a followed document. The advisor records current live-handoff
scope/path entries in metadata for reboot visibility, while `docs/state.md`
remains the sole followed-document registry. The notification boundary is a
coherent intended v1 or completed topology change, not the first write. Send it
promptly enough not to lose it—normally in the next interaction, otherwise as a
`tell`—and no later than session end or transfer. Several changes at the same
natural boundary may share one interaction.

Load and follow `research-advisor.md` to resolve the program or project-wide
advisor, deduplicate unchanged packet states, compose its
charter/notes/document-state/packet startup bundle, keep the relevant evolving
documents in its `docs/state.md` followed set, reconcile its semantic
understanding in `notes.md` through that document cursor, and return the
challenge memo. Do not merely record that review would be useful, and do not
request a scan of the whole `research/` tree when current-program paths
suffice. Routine implementation, plumbing, frozen sweep cells, and results
that leave both the claim and next decision unchanged do not invoke the
advisor.
