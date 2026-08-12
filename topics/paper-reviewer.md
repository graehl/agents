# Paper reviewer

> An advisor-context-aware review mode that tests whether a proposed or drafted
> paper's form, focus, and claims fit the research program's actual evidence.

Topic: `paper-reviewer`

## Artifact-conditioned advisor guidance

Paper review is an artifact-conditioned instruction set available to every
research advisor, not a separate authority or fixed persona. The consulting
agent decides what it wants reviewed. By default the program advisor answers
with its independent trajectory, durable program understanding, followed
documents, and read-only stance; it does not become a supervisor over the
author or a second owner of program truth. A writing session may apply this
topic as a self-check, but it must not label its own assessment as advisor
output.

The user may instead request an ordinary research advisor scoped only to one
draft. That is a scope choice, not a paper-specific advisor type. Establish its
independent logical bundle at
`research/<program>/papers/<paper-slug>/advisor/` under
`research-advisor.md`; give it the program glossary, frozen proposal, current
draft, and the evidence-bearing documents needed for review. It loads the full
standard research-advisor charter and startup bundle; the paper-specific topics
are additive checks, not a reduced competency or context. Its followed set is
chosen manually under the ordinary advisor protocol. It does not write the
broader program advisor's state.

A live handoff for paper work identifies every advisor it relies on with the
exact `Advisor metadata:` and repeatable `Incumbent advisor session:` lines
from `topics/handoffs.md`. This applies whether the handoff names only the
program advisor, only a draft-scoped advisor, or both.

Use the ordinary `research-advisor.md` interaction and challenge memo. Name the
paper stage and include the proposal or draft as a working-document change;
request followed-document status when future deltas should remain in the
advisor's context.

## Review stages

### Proposal portfolio

Test whether each candidate's evidence ceiling supports its governing form and
reader promise. Scrutinize the matched simple-practitioner baseline, effect
size, uncertainty, public-data/model-access boundary, practical cost, and
contribution that survives a failed headline. Prefer a candid narrower paper to
a rescue narrative.

### Promoted skeleton

Test whether every load-bearing claim is either evidence-linked or explicitly
speculative with a named adjudicating measurement. Check that the selected form
actually governs the section spine, that failed attempts affecting validity,
scope, cost, or attribution remain visible, and that a second independent form
has not been smuggled into one manuscript.

### Completion or release

Trace headline numbers to primary evidence; recheck comparison fairness,
uncertainty, baseline strength, cost and data scope, table/caption contracts,
and related-work boundaries. Read the paper as an uninterested first-time
reader. Attraction features should clarify supported findings; flag charged
framing that needs the honest disclaimer described in the paper-drafting
sketch.

## Paper-specific review block

Append this compact block to the ordinary advisor challenge memo when it adds
information:

```markdown
Paper stage: proposal | skeleton | completion
Publication case: credible now | credible if <evidence> | unsupported
Evidence ceiling: <strongest claim the record carries>
Matched-baseline verdict: <win, tie, loss, or missing under named regime>
Form / focus fit: <does the reader promise match the evidence?>
Narrative integrity: <hidden failure, chronology, or selection concern>
Most valuable missing evidence: <one discriminating result or none>
Narrower viable paper: <best supported fallback or none>
```

Do not predict acceptance from polish alone. Do not recommend more experiments
without saying which proposal verdict they could change. If no form is
currently publication-worthy, say so and preserve the best proposal as
`credible-if`, parked, or rejected.

Alternative reviewer-session topology and a possible future skill wrapper are
kept in [`paper-reviewer.sketches.md`](paper-reviewer.sketches.md).
