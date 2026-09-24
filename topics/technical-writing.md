# Technical writing

> Shared cold-reader guidance for research handouts, progress reports, blog
> posts, and papers: make the current claim, evidence, scope, and decision
> self-contained and legible when scanned.

Topic: `technical-writing`

## Common contract

Use this topic before substantially revising a research handout, progress
report, blog post, or paper for readers outside the working session. The
artifact-specific topic adds its own purpose, lifecycle, and evidentiary bar;
this topic owns the advice they share. When the artifact makes research claims,
also follow [`research-writing`](research-writing.md) for prior-art,
attribution, and citation coverage.

Assume a first-time reader whose attention has not yet been earned. They do
not know the working vocabulary and may have ignored earlier updates.
Headings, captions, and displays serve the reader who first scans to decide
whether the document deserves attention; that scan should yield at least one
specific evidence-grounded takeaway. The prose serves the reader who then
reads: it should be dense enough in reader value that reading in order beats
skimming, and a full reading delivers the artifact's complete reader promise.

The artifacts differ mainly in how they select and reshape program work:

| artifact | selection basis | relationship to research effort |
|---|---|---|
| serious paper | chosen theme and governing form | backfill justified evidence and interest-building work until the claim is supported or narrowed |
| handout | rewarding discussion lead plus representative account of what was done | open selectively, then organize existing work by theme; add only a small, labeled prospective coordination layer |
| progress report | prior promised threads plus work since | reconcile the delta, group threads by theme when useful, and state concise dispositions/plans |
| research blog | the cool thing that worked | showcase-selective; bound the claim and point to the fuller record |

## Priority order

The rules in this topic and in [`writing`](writing.md) pull in different
directions. When they conflict, this order wins, and no rule below the
second ever adds material:

1. **Truth at the stated precision.** No cut, move, or reorder may leave a
   sentence claiming more than the evidence at the level of precision it
   states. Detail that only sharpens an already-true claim (method,
   conditions, minor caveats) can move to an appendix, footnote, or pointer.
   A qualification stays inline only when its absence would make the inline
   sentence false or the result irreproducible from the main text's promise.
   When keeping it inline is longer than weakening the sentence, weaken the
   sentence.
2. **Elision.** Material earns inclusion on its merits: it supports a claim,
   explains a display, sets up a named later statement, or supplies a
   condition the main text's claim depends on. Everything below applies
   only to material that survives this test and never justifies adding,
   restating, summarizing, or motivating.
3. **Worth reading in order.** The aim is prose a reader need not skim:
   every sentence carries something, so reading straight through is
   cheaper than hunting. Headings carry the claim; paragraphs owe no topic
   sentence under one. An in-order reader resolves a definite reference
   ("the baseline", "the 32k run") from what they just read; supply a
   section reference or tag only for an antecedent that is genuinely hard
   to locate, such as something introduced in passing several sections
   back. When a section holds several sub-points a reader might want
   separately, give each a findable opening: a subheading or lead slug,
   else a first sentence stating that sub-point's claim ("Sentence length
   explains most of the de-en gap"), never one announcing its subject ("We
   now examine sentence length").
4. **Clarity.** Actor as subject, action as verb, the concrete word, one
   term per concept.
5. **Momentum.** The stress position of each unit holds the fact the next
   unit uses (*End each unit on what drives the next*).
6. **Rhythm and voice.** Sentence variety and active voice are tie-breakers
   for reordering only.

Inherited `writing` rules carry these limits in technical prose: rhythm is a
reason to reorder, never to add, split, or restate; a signpost is a heading
or the previous paragraph's handoff, not a sentence about the document; an
example earns its place only when it is the shortest way to make the claim
checkable; "one idea per paragraph, announced by its first sentence" reduces
to one idea per paragraph.

Always a defect in technical prose, whatever rule seems to call for it: a
sentence that restates the previous one in abstract or figurative form; a
closing sentence that summarizes its own paragraph; a one-sentence paragraph
or fragment for effect; a "not X but Y" or triad built for cadence; a
rhetorical question; a bolded whole sentence; a sentence about the document
instead of the subject ("we now turn to"); an opener asserting importance
rather than showing it; "crucially", "notably", "importantly", "underscores",
"highlights". The correction is deletion, not replacement. Text that
remarks on its own compliance with a writing rule is a defect in every
authored piece, not only technical ones; see
[`writing` § Drafting and revising](writing.md#drafting-and-revising),
"Following a rule is silent."

Paragraph-local edits break determiners. "The X" presumes X was introduced
earlier; when a local reorder, cut, or move changes which mention of X comes
first, the new first mention becomes "a X" (or acquires its introduction),
and a later "a X" may need to become "the X". After any non-global edit,
find each definite reference in the edited span and confirm its antecedent
still precedes it.

## Order material for the reader

A working document naturally accretes in the order experiments, meetings, and
ideas happened. Before dissemination, perform a substantial whole-document
consolidate, review, and revise pass. The mechanism may be direct revision or
an available dream/review workflow; the required outcome is the revised
artifact, not a ritual invocation. Lead with:

1. why the subject deserves attention now, as a fact the reader can check or
   a gap the result closes; with no such fact, open with the result;
2. the current claim, result, or decision;
3. the evidence that supports and bounds it; and
4. what the reader should conclude, decide, or do.

Reorganize or cut chronology that does not explain a current conclusion. An
artifact may retain chronology when its reader promise is specifically to
report change over time, but it must curate that chronology for the reader.
Merely prepending an executive summary to an accumulated raw log does not
complete the pass.

## Review inclusion paragraph by paragraph

For a close reader-value pass, use
[`writing` § Paragraph review](writing.md#paragraph-review): annotated
passages with explicit inclusion rationales, guided/batch/autonomous modes,
addressable rulings, and preserved trims. Apply the test to named datasets,
models, techniques, and implementation details as well as whole paragraphs.
Each should support a useful claim or result, explain a display, establish
needed context for an identified later statement, or supply an essential
qualification or reproduction condition. Do not retrofit a performance claim
to justify an inventory. Mark a missing connection or missing evidence.

For contextual material, consider whether a diagram plus caption would make
the relationship clearer with less prose. Follow the display contract below
when producing it. Keep necessary definitions and uncertainty visible after
trimming, and recheck the whole argument after local rulings.

## End each unit on what drives the next

Readers stress whatever arrives at a point of syntactic closure: the end of a
clause, sentence, paragraph, or section. [`writing` § Sentences](writing.md#sentences)
states the general form as *old before new*. Technical prose, where most
sentences carry a result, a quantity, or a condition, gets the strong version:

Put in the stress position the element the reader must carry forward: the
result, the surprising or uncertain part, the quantity the next sentence
explains, or the condition the next paragraph relaxes. Open with the
linkage: the term already under discussion, or the clause that connects to
the previous sentence. A sentence built this way tells the reader what it is
about before it asks them to hold anything new, and leaves them holding
exactly the piece the next sentence uses.

When a sentence reads inadequately, check its stress position before
diagnosing anything else. The usual occupant is not the payload but a
trailing qualifier: a citation, a condition ("when N is large"), a locator
("as shown in Table 2"), a method aside ("in our preliminary experiments"),
or a hedge. Fixes, in order of preference:

1. move the qualifier forward, ahead of the payload;
2. split, giving the qualifier its own sentence with its own stress position;
3. choose the grammatical subject so the order comes out right. This is the
   legitimate use of the passive, and the reason "avoid the passive" is a
   corrective rather than a rule.

A sentence with nothing worth stressing is a candidate for deletion or for
merging into its neighbor.

The check is mechanical, so it applies to sentences already judged weak
without first naming why they are weak. It catches the two common failures
of long sentences: a payload buried mid-sentence under accumulated
qualification, and an ending on whatever the writer thought of last. It is
especially useful for writers whose first language marks topic and focus by
case, particles, or free word order; English marks them mainly by position,
so a literal transfer yields grammatical sentences with the emphasis in the
wrong place.

The same expectation holds at each larger closure. A paragraph's last
sentence and a section's last paragraph carry the consequence or open
question that the next unit takes up, so the reader arrives at the next
heading already wanting it. This does not conflict with the front-loading
in *Order material for the reader*: headings and section openings state the
claim; the ending selects, from what the unit established, the piece that
motivates what follows. Selects, never adds: a paragraph whose natural last
fact is weak is reordered or shortened, not given a closing sentence, and an
ending that rephrases the opening is deleted. A paragraph that ends on a
supporting detail, a citation list, or a caveat nothing later uses has spent
its stress position.

How strongly a unit's ending pulls the reader into the next unit is one axis
of quality, traded against the others: the front-loaded claim for a reader
who stops early, actor as subject, sentence length, and honest placement of
a qualification that must not be missed. Run the check on every sentence;
violate it when another axis wins, and know which one.

Source: Gopen and Swan, "The Science of Scientific Writing", *American
Scientist* 78(6), 1990, which names the topic and stress positions and
warns that none of its reader-expectation principles are rules. Williams's
*Style* and Pinker's *The Sense of Style* (given before new, light before
heavy, and the same ordering applied to passages) carry the same principle;
Michael Ernst's technical-paper advice page quotes it from Norman Ramsey for
computer-science readers.

## Reconstruct lost context

- Link the applicable glossary near the opening when one exists, but still
  define, at first use, the jargon and abbreviations the named reader does
  not already hold; a definition for a peer is filler.
- Replace internal run ids, checkpoint nicknames, and stage labels with literal
  reader-facing names. Retain an internal handle only as a provenance link.
- Separate measured observations, interpretations, deployment assumptions,
  normative choices, pending work, and downstream consequences. Do not rely on
  prose cadence to imply that one establishes another. This is a truth
  requirement on what each sentence asserts, not a labeling format.
- State the regime of a result: population or task, data/split, model-access
  boundary, and material cost or deployment constraint.

## Make displays self-decoding

Every claim-bearing table or figure identifies its population and comparison,
metric direction, split and N when applicable, principal baseline, and cost
boundary. Define nonstandard columns and conditions adjacent to the display.
State the intended takeaway once, in the caption or in the prose beside the
display, rather than asking a reader to infer it from bold cells; the other
refers to the display instead of restating it.

Before selecting or generating a graph, diagram, or quantitative display,
follow [`document-writing-figures`](document-writing-figures.md). It maps the
reader's information need to Quarto-native tables, images, panels, Mermaid, or
Graphviz and to reproducible external plotting when the claim is quantitative.

Place an effective results table or representative input/output example inline
beside the claim it illustrates. Give examples enough source, condition, and
output labeling to stand on their own. An appendix or final raw-results dump may
preserve exhaustive support, but it is not the sole home for the display that
makes a central claim understandable.

For diagram tooling, label fit, screen legibility, and out-of-band explanatory
notes, follow the [figure layout guidance](document-writing-figures.md#layout-labels-and-explanatory-notes).

Run a scan-only pass: headings, captions, tables, figures, and emphasized text
should convey the correct current claim and decision without requiring the
reader to reconstruct the working session. Full prose then supplies evidence,
qualification, and explanation.

## Artifact-specific contracts

- [`research-writing`](research-writing.md) adds the research-specific
  prior-art and citation layer without making citation density a generic
  technical-writing requirement.
- [`blog-post-writing`](blog-post-writing.md) owns static-site structure,
  navigation, rich web elements, and blog-specific citation presentation.
- [`handout-writing`](handout-writing.md) owns the mutable, paper-like decision
  snapshot and its cooperative-review proof bar.
- [`progress-report`](progress-report.md) owns the dated, cumulative, frozen
  report stream, clearly marked refresher, delta chronology, and
  pursue/hold/park triage.
- [`research-blog-writing`](research-blog-writing.md) owns the selective
  showcase of one cool result, demo, tool, or recipe.
- [`paper-writing`](paper-writing.md) owns the form-led durable publication
  argument; [`paper-drafting`](paper-drafting.md) owns proposal selection and
  promotion into that draft.

Do not flatten these differences into the common layer. Sharing the reader
contract does not make a handout a paper or a progress report a mutable draft.
