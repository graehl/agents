# Writing guidance evidence

## 2026-09-21 — paragraph review with addressable rulings

Contributing-model: 6-Astra.

User-directed: after a research-paper trimming pass, graehl requested an
annotated artifact or paragraph-by-paragraph quotations explaining why each
passage belongs, its later payoff, and whether a visualization plus caption
would convey it better. He requested guided discussion, batch section/document
review with out-of-order rulings, and a selectable autonomous version.
Session: `01a0c4f4-afab-7ba2-96d6-e45304acdb21`.

Agent-chosen name: paragraph review. The shared procedure lives in writing;
technical-writing links to it and specializes the evidence test. The workflow
is optional, so a spelling correction does not incur a document annotation
ritual. Its effectiveness is assumed, not established by a measured comparison.

Forward traces:

- Guided review: `next` after a proposed trim advances the cursor while the
  ruling remains pending. Explicit acceptance can apply the edit when editing
  is authorized. Navigation alone cannot delete text.
- Batch review: the author rules on paragraph 9 before paragraph 2. Original
  locators remain stable after renumbering; changing a definition triggers
  reconsideration of the later claim it supported. Review-only leaves source
  text untouched.
- Autonomous revision: an unnecessary dataset list goes to the local trims
  companion, but an unexciting qualification stays because removing it would
  overstate the result. The revised render and decision record remain
  available for selective reconsideration.
- Narrative review: a paragraph establishing tension can earn inclusion
  without a technical claim. A straightforward copy edit does not activate
  the full review procedure.

These traces motivated explicit navigation/approval separation, stable
locators, dependency checks, and a reader-purpose test broad enough for fiction.

## 2026-09-21 — diagram fit and out-of-band explanation

Contributing-model: 6-Astra.

User-directed corrections to ontology bubble diagrams: enlarge label and
cluster containers before bending text severely, compute bounds first, permit
optical tweaks, balance nested clearances, and crop for screen legibility.
General explanatory captions are out of band and may be boxed/styled by the
container; only spatial labels belong within the diagram geometry. Prefer
standard diagram formats/layout libraries, extending the existing preference
for standard plotting tools. The user asked to record this preference rather
than undertake a library survey during the figure repair.

Trace checks: a named node keeps its spatial label; a general scope note goes
in a distinct caption box; a cramped long label grows its container; an SVG
with unreadable embedded text still fails the screen check. An established
renderer receives the same inspection instead of being assumed correct.
These are user preferences with trace-checked safeguards, not measured
evidence that any particular layout tool performs better.

The user clarified that embedded figures place general explanation in the
document frame and prefer spatially attached labels over prose referring back
to marks. They also requested coordinated typography inside and outside the
figure. The guidance distinguishes shared styling from external SVG's lack
of page-CSS inheritance, and calls for font availability and renewed bounds
checks when fonts change.
