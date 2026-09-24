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

## 2026-09-24 — base-layer reconciliation and the vendored-advice caveat

Contributing-model: fable-5.1.

User-directed, same session. graehl asked whether `writing` (the base
layer under `technical-writing`) carries advice that conflicts with what he
wants in technical prose. Four bullets did, and each was restated as the
invariant it approximated rather than overridden per genre: findable ideas
(heading or first sentence, whichever the prose has), transitions carried by
heading or previous ending with a transition sentence as fallback, length
follows content (the short-after-long mannerism removed outright since he
dislikes it in every genre), and qualification allowed in a note or
appendix. The base now says genre topics narrow it and win on conflict.
technical-writing's inherited-limits paragraph shrank to the one genuine
genre difference (examples only when they are the shortest way to make a
claim checkable).

graehl's epistemic statement, recorded because it governs how every rule in
`writing.md` should be read: all expert-level artistic-performance advice in
this repo is vendored blindly; he has never tried to follow it himself. He
asked for a broader research/trace/reconsideration of `writing.md`; that is
`gaps/writing-advice-provenance.md`.

## 2026-09-24 — writing.md audit: per-bullet verdicts

Contributing-model: fable-5.1.

User-directed; closes `gaps/writing-advice-provenance.md`. Three questions
per bullet: does the source have a record of being read rather than only
of giving advice; what does a capable writer produce following the rule
literally; does it conflict with `technical-writing` § Priority order or
`AGENTS.user.md` § Writing and summary style. graehl agreed with the
verdict table in full and set two dispositions: reasonably contested rules
move to this annex; advice aimed at human or new writers moves to a new
topic agents are not routed to (`writing-practice`).

Source credibility, as assessed: McPhee, Le Guin, Leonard, Orwell, and E. B.
White are proven writers. Williams and Gopen/Swan are the only sources whose
rules rest on reader-comprehension work; Pinker restates the same rules from
cognition and was added as a named source. Zinsser, Lamott, and King are
proven by sales and write mostly about the human writer's psychology.
Strunk and White's grammar claims were publicly demolished by Pullum
("50 Years of Stupid Grammar Advice", 2009); "omit needless words" was not
the target and stays.

| bullet | source | verdict | disposition |
|---|---|---|---|
| name the reader / purpose / promise | Williams, Zinsser | keep | "keep collecting until the sentence comes" was human process; now "ask the author" |
| collect, then choose | McPhee | keep | unchanged |
| order by the reader's need | McPhee | keep | index-card ritual clause dropped |
| use the reader's words | Williams, Pinker | keep | unchanged |
| one concrete example per abstraction | Pinker | rewrite | literal following adds; restated as a test (instantiate or cut), with "do not add an example to an abstraction that already lands" |
| prefer the specific, concrete, plain | Orwell, Zinsser | keep | Orwell's rule 1 folded in, extended to figurative restatement |
| actor as subject, action as verb | Williams | keep | best-evidenced rule in the file |
| omit needless words | Strunk | keep | unchanged |
| adverbs and intensifiers are confessions | King | rewrite | literal following strips truth-bearing adverbs; restricted to intensifiers |
| old before new | Williams, Gopen | keep | unchanged |
| vary length for rhythm | Le Guin, Zinsser | removed earlier this session | annexed below |
| prefer active voice | Orwell, Strunk | derive | annexed below; replaced by "voice is not chosen separately" |
| read it aloud | Le Guin, Zinsser | rewrite | agent cannot; the checks it performs are listed; original moved to `writing-practice` |
| Orwell's six rules | Orwell | reduce | annexed below; rules 2 and 3 already bullets, 4 derived, 5 conflicts with peer register, 6 is the layering note |
| bad first drafts / short assignments / door closed | Lamott, King | move | `writing-practice` |
| revise in passes, largest unit first | consensus | keep | "announce its point" removed from the paragraph pass |
| cut ten percent | King | rewrite | quota annexed; the list of cuts stays as "cut what the text already showed" |
| leave out the part readers skip | Leonard | promote | now the first Structure bullet, stated as the rule the rest serve |
| check the promise | consensus | keep | unchanged |
| let it cool | consensus | rewrite | agent equivalent "cold read"; original moved to `writing-practice` |
| following a rule is silent | graehl | keep | unchanged |
| expository forms in brief | mixed | keep | unchanged |

### Annex: contested rules removed from `writing.md`

Verbatim as they stood, with why each is contested. Not guidance.

- **Prefer active voice** unless the actor is unknown, unimportant, or you
  want the receiver in the subject position for emphasis. — Contested:
  Pullum's critique shows the popular rule mis-teaches what the passive is,
  and the exceptions swallow the rule once old-before-new is applied.
  Derived rule replaces it.
- **Vary length for rhythm, but on purpose.** A run of long sentences numbs;
  a run of short ones jabs. A short sentence after a long one lands. —
  Contested: literal following produces the punchy one-liner graehl dislikes
  in every genre; fiction keeps its own rhythm guidance in `story-writing`.
- **Adverbs and intensifiers are usually confessions** that the verb or
  adjective was weak. Fix the verb instead. — Contested as stated: "only",
  "approximately", "not yet" carry truth conditions in technical prose.
- Orwell's six rules paragraph: never use a figure of speech you are used
  to seeing in print; never use a long word where a short one will do; if
  it is possible to cut a word, cut it; never use the passive where you can
  use the active; never use a foreign phrase, scientific word, or jargon
  word if there is an everyday equivalent; break any of these rules sooner
  than say anything outright barbarous. — Rule 4 contested as above; rule 5
  conflicts with writing at peer register, where the technical term is the
  reader's word; Orwell himself violates several in the essay that states
  them.
- **Cut ten percent.** King's formula for the second draft is the first
  draft minus ten percent. — The number is a rejection-slip anecdote;
  the cuts it names are kept without the quota.

## 2026-09-24 — sections named by age instead of content

Contributing-model: opus-5.5.

User-directed: graehl observed that section names such as "earlier X" arise
organically in agent writing and read as vague and poorly named, and asked
that a more specific signification be researched before settling on
"prior", "earlier", or "historical". Session:
`48283649-2d49-41b7-9d22-aceb9a574e1d`.

Placed in `writing` § Structure rather than `technical-writing`, because the
pattern appears in topics, handoffs, and docs as well as research artifacts;
the genre topics inherit it. The observation that agents drift toward these
labels is the motivation, kept here rather than in the rule. graehl
attributes the habit to human cop-out naming in papers that agents learned,
and directed that the rule be a try-harder trigger traded against other
costs, not a ban; the first draft's "stays only when anchored" wording was
softened to match. He then set the goal of at most one "earlier" sense
per paper, explained in prose, and asked that a bare "not from the latest
round" distinction be made in less clichéd terms only when relevant, and
named grouping all non-current material into a single scope as the usual
means.

Trace checks: `progress-report`'s "Generate by reconciling the previous
report" passes, since the previous report in a dated series is a definite
anchor; `research-writing`'s "prior-art map" passes as a term of art; a
handoff section "Earlier approach" fails and becomes the named approach plus
what superseded it. A sweep of `~/agents` headings found no current
violation, so the rule steers new writing only.
