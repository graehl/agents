# Research discovery and direction decisions

> Rules and rationale for field surveys, frontier mapping, and skeptical research-advisor handoffs.

Read this packet before field-survey, prior-art, or direction-ranking work, and
when a material research decision or changed evidence state triggers the
research advisor. `RESEARCH.md` is the router and wins on conflict.

## Binding rules

Read Field surveys and frontier mapping for discovery work, and
Research-advisor handoff when its decision/document trigger applies. A survey
does not by itself require advisor lifecycle or recovery reads.

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

When the current repo has no `surveys/`, resolve bare survey paths against
`~/agents/surveys/`. Cite the shared map or concept path so another reader can
find it. Keep paper-local related work only when no shared survey covers the
field or the material belongs to that paper's overlap tier.

An explicit field- or frontier-survey request defaults to grounded: fetch and
read sources, verify citations, and maintain
`~/agents/surveys/<field-slug>/`. Only explicit `light`, `recall`, or
`ungrounded` wording selects a conversation-only pass that downloads no
primary-source corpus and persists nothing. An ordinary explanation that does
not request a survey is not promoted into persistent survey work.

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

Load and follow `advisor/serve.md` completely for ordinary scope resolution,
packet delivery, followed-document synchronization, semantic reconciliation,
and the challenge memo. Its condition table routes rare lifecycle or recovery
work to exact sections of `research-advisor.md` and `advisor/charter.md`; do
not read either catalog in full merely because a consultation is due. Do not
substitute “advisor review would help” for invocation.
Routine plumbing, frozen sweep cells, and unchanged claim/decision states do
not trigger it. A topology-only notification is a `tell`. The trigger is the
coherent intended-v1 or completed-change boundary, not file creation, first
touch, or first line. Deliver promptly—normally in the next advisor interaction,
or as its own `tell` when none is otherwise due. It may be bundled or briefly
deferred, but remains owed and is delivered before the working session ends or
transfers its scope.
