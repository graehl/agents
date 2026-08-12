# Handout writing

> Write a representative, paper-like decision and discussion starter that
> gives an interested reader the full picture while an uninvolved participant
> can recover the work's flavor and one evidence-grounded insight by scanning.

Topic: `handout-writing`

## Rewrite for first contact

Follow [`technical-writing`](technical-writing.md) for the common cold-reader,
terminology, evidence-separation, display, and whole-document revision
contract. Also follow the form-led claim, evidence-spine, and attraction
guidance in [`paper-writing`](paper-writing.md). A handout is free to discard
work chronology completely because its purpose is the current decision
snapshot.

Design for two reading speeds. An interested reader should get a representative
full picture of the work, its evidence, major bets, current interpretation, and
open decisions from the handout as a whole. An uninvolved participant may only
scan the displays during a discussion; give that reader the flavor of the work
and at least one concrete insight they can explain afterward. Assume this may
be the third update but their first moment of attention.

Lead with the current decision, claim, or evidence object that makes the
program rewarding to examine together. Reorganize or cut the chronology.
Merely prepending an executive summary to an unchanged running log does not
complete the pass.

One useful order is status/source map, decision summary, one-page result,
claim-bearing tables and limitations, current plan or ask, then detailed
research narrative and appendices. Treat it as a test, not a mandatory
template: headings, tables, and captions alone should still communicate the
current decision.

## Use the cooperative-review proof bar

The interested audience is curious what the program may achieve or has
achieved, not an adversarial submission referee. Apply the paper's honesty and
comprehension rules at a lower rigor/completeness burden:

- label established, provisional, speculative, and planned claims plainly;
- show the decisive result, representative example, or main comparison needed
  to understand the claim;
- keep limitations that change the reader's decision, interpretation, or trust
  in the main path;
- signal where the full run record, ablations, proof, derivation, raw results,
  or exhaustive caveats exist, with links or stable handles; and
- omit tedious detail that demonstrates diligence without helping this reader
  understand the claim or decide what follows.

This lowers the presentation and completeness burden, not the truth,
provenance, or evidence standard for claims actually made.

“The audit trail exists” must itself be checkable, but the handout need not
reproduce it. A pleasant visual cadence, representative input/output examples,
and a clean result-first narrative are substantive comprehension aids here, not
cosmetic polish.

## Lead with the rewarding discussion object

The opening may be blog-like and selective even though the complete handout is
representative. Lead with the result, failure, input/output example, result
table, base-model comparison, best technique, or unresolved contrast that is
most rewarding to examine and discuss. State the concrete insight, question,
decision, or reaction it is meant to kickstart.

When the program mostly failed, do not manufacture a win. Prepare an
evidence-backed “why did this fail?” puzzle: show enough data, outputs, and
comparisons to establish the failure, say what they appear to rule out, and
name the live explanations or next discriminating check. A negative program
can still give uninvolved participants a real object to reason about.

Handouts are especially disposed to a visual spine. Prefer a small number of
strong, self-describing result tables, representative input/output examples,
and repeated comparison layouts, with prose serving as orientation and
interpretation. A reader scanning the displays should recover the current
claim and discussion agenda.

Keep the displays inline where the claim is made. A final raw-results section
may preserve breadth, but the effective illustration does not belong only at
the end. Avoid a wall of weakly differentiated tables; each main-path display
earns its place by changing understanding.

## Represent the work without dwelling on every failure

Unlike a selective [`research blog`](research-blog-writing.md), a handout gives
an interested reader a representative full picture of the program's major
bets, successes, failures, and decisions. “Full picture” means the complete
decision-relevant account, not every run or chronological detail. Deemphasize
dead ends rather than deleting them. A compact note or appendix line is usually
enough:

```text
<attempt> — <outcome>; confidence this is a substantive negative:
<high | medium | low> (<brief reason, including likely bug debt>).
```

Use `low` when the attempt was probably bug-riddled, insufficiently validated,
or otherwise leaves a real possibility that the idea remains live. Do not turn
uncertainty into a rescue story; say what check would distinguish an
implementation failure from a method failure when that distinction matters.
Keep a dead end in the main path when it affects the headline claim's validity,
attribution, scope, or practical cost.

## Organize what was done

A handout is retrospective by default. Organize completed work by theme when
several themes make the program easier to understand; use the simplest direct
structure when there is only one. A small sprinkling of prospective material
may show how efforts could be unified or coordinated, but label it as planned
or speculative and do not backfill substantial new research merely to complete
the handout's story.

## Relationship to progress reports and papers

Handouts are mutable and may be rewritten as the audience or decision changes.
A [`progress-report`](progress-report.md) is the more delta- and
chronology-oriented sibling: it pays the same introductory burden in a clearly
marked refresher, then preserves a dated stream and carries corrections
forward.

A [`research blog`](research-blog-writing.md) is the more selectively
promotional sibling: it may focus on one cool thing that worked and need not
represent the program's failed bets proportionately. A handout may borrow that
showcase opening, then widen into the representative thematic account.

The handout inherits `paper-writing` without requiring a promoted proposal or a
submission-complete evidence package. When it presents or previews a durable
publication case, use [`paper-drafting`](paper-drafting.md) for proposal status.
The handout remains a decision artifact rather than becoming the manuscript.

The working PII exemplar and its corrective advisor record are
`~/draft/research/pii-redaction-frontier/incumbent-comparison-handout.md` and
`~/draft/research/pii-redaction-frontier/advisor/incumbent-comparison-handout-review.md`.
They are evidence for this guidance, not a universal handout template.
