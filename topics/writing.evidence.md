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

## 2026-09-24 — stress position as a strong, scoped technical-writing rule

Contributing-model: fable-5.1.

User-directed: graehl recalled the advice "put the uncertain/most important
information, the part driving interest toward the next sentence, at the end
of the sentence," characterized it as a corrective heuristic of the same
kind as "avoid passive voice" (wrong as a law, good as a hint), and asked
for the appropriately scoped strong version in `technical-writing`, plus
the zoomed-out (paragraph/section) equivalent, framed as one axis of quality
traded off against others. He reports applying it when mechanically
reshaping sentence sequences he judges inadequate, and expects it to help
non-native English writers in particular. Session:
`63b5dd3a-a496-4957-9334-3002cda9a13f`.

Source located: Gopen and Swan, "The Science of Scientific Writing",
*American Scientist* 78(6):550–558, 1990 (topic position / stress position;
"none of these reader-expectation principles should be considered rules").
Its CS-community transmission that I could verify is Michael Ernst's
technical-paper advice page, which quotes Norman Ramsey: "For material you
want to carry weight or be remembered, use the end of a sentence." The
specific ~2008 NLP/ML-community write-up graehl recalls was not found; Jason
Eisner's advice index has no page on sentence craft. `writing` already
carried the general *old before new* bullet (Williams); the new section
owns the strong scoped form and `writing` links to it.

Agent-derived, not from a source: the ordered fix list (move qualifier
forward, split, choose the subject), the claim that the check pays off
because it is mechanical, and the non-native rationale (English marks
topic/focus mainly by position; case/particle/free-order languages transfer
badly). The last is standard contrastive-linguistics reasoning but was not
checked against a citation.

Trace checks: a sentence ending in a citation moves the citation forward or
splits; a paragraph ending on a caveat nothing later uses is flagged; the
front-loaded document order and first-sentence topic announcement stay in
force, so the section states the reconciliation explicitly; a deliberate
violation for a must-not-miss qualification is allowed and named as such.
Effectiveness is the user's practice plus source authority, not a measured
comparison.

## 2026-09-24 — priority order, rule limitations, defect list

Contributing-model: fable-5.1.

User-directed, same session as the entry above. graehl asked for
limitations on any contradictory or dangerous advice in technical-writing,
suggested an explicit priority order as the concise encoding, and stated
the aim: frontier-authored text already shows taste, so the guidance
should unlock elision rather than pile on checklists that each add
material. His stated overriding concern for technical prose is making it
less necessary to skim. He hates over-repeated AI-ese, naming the
superfluous abstract/metaphor restatement specifically.

Decisions during the exchange, each a user correction of my draft:

- Item 1 is not absolute: qualification can wait for an appendix when
  carrying it inline costs too much method detail. Rewritten as truth *at
  the stated precision* of the surviving sentence, with deferral allowed.
- Item 3 originally required a first sentence announcing each paragraph.
  Rejected: the heading already carries the reason to read. Then "enterable
  cold" with section references for every referent was rejected: "the X"
  is fine when X's home is the previous section or deducible from headings;
  section references are for hard-to-locate antecedents only. Final form is
  "worth reading in order," with sub-point openings (slug or claim, never
  announcement) only when a section holds separable sub-points. He was not
  sure a flat "no topic sentence" was wanted; I illustrated three cases
  (restated heading, referent tag, multi-sub-point section) and he accepted
  the softer form.
- Added on his report of an observed defect: paragraph-local edits break
  determiners ("the X" whose introducing mention moved), with a recheck
  instruction.
- Added mid-turn: no meta celebration of having followed a writing rule, in
  the artifact or in the delivery note.

The Common contract paragraph was softened from scanner-first to "headings
and displays serve the scanner; prose serves the reader who reads," since
the old wording justified the scaffolding the priority order removes.
Inherited `writing` bullets (rhythm, signposting, one example per
abstraction, first-sentence announcement) received technical-prose limits
here rather than edits to `writing.md`.
