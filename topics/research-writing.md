# Research writing

> Research writing inherits the cold-reader contract from technical writing
> and adds prior-art, attribution, and citation-coverage rules calibrated to
> papers, research blogs, handouts, and progress reports.

Topic: `research-writing`

## Research-specific layer

Follow [`technical-writing`](technical-writing.md) for organization,
terminology, displays, and first-contact comprehension. This topic owns the
additional obligation created when a document makes a research claim: place
the claim among the work that most directly competes with, enabled, or bounds
it, and make borrowed ideas and artifacts traceable.

Citation coverage matters more than citation count. Do not target a references
quota, imitate a venue's cite-heavy surface, or pad a bibliography with papers
that the prose never distinguishes. A short bibliography can be inadequate;
an enormous one can still omit the one competitor that changes the claim.

## Build the prior-art map before selecting citations

Treat the bibliography as a selected attribution and comparison surface, not
as the field map itself. Before making a novelty, superiority, or “no prior
work” claim:

- search the shared `~/agents/surveys/<field-slug>/` tree and follow
  [`research-survey`](research-survey.md) rather than rebuilding a paper-local
  account of an already mapped field;
- use [`literature-search.md`](../literature-search.md) to retrieve work and
  [`field-map.md`](../field-map.md) to organize the relevant territory,
  effectiveness grades, contested results, negative results, and baseline
  sensitivity; and
- for a fresh claim, apparent void, or frontier position, use
  [`frontier-map.md`](../frontier-map.md) in grounded mode and run its
  falsification search aimed at finding the supposedly absent work.

A paper-specific related-work cache is still useful for a narrow overlap tier
or when no shared survey covers the field. It supplements the map; it does not
create a second factual map.

## Citation coverage contract

For each central research claim, include and discuss, when they exist:

1. the closest competing method, result, or alternative interpretation under
   a comparable regime;
2. the most influential or inspirational intellectual parent works, including
   a parent whose idea was adapted rather than copied literally;
3. the primary source for a borrowed task, dataset, metric, protocol, code
   base, theorem, visualization, or method component; and
4. contradictory, failed-replication, or boundary-setting work whose omission
   would make the claim look broader or more settled than it is.

Use primary sources for central provenance and competitive claims. A survey or
review may efficiently locate and summarize a territory, but it should not
replace the primary work whose result or idea the document relies on. Verify
bibliographic metadata and the cited source's actual support for the adjacent
claim; do not cite from title resemblance or another paper's paraphrase.

Synthesize a citation cluster. Explain the relationship that makes each work
relevant instead of appending an undifferentiated list. Place citations close
enough that their scope is unambiguous. One well-placed citation may support
several adjacent sentences; repeat it only when a reader could otherwise
misassign the source.

## Calibrate by artifact

- **Paper:** cover the nearest competitive neighborhood completely enough that
  an informed reader can audit the novelty and comparison. Cite every true
  intellectual parent and every source that owns a central task, datum,
  method, or result. Broader background can be selective and synthesized;
  venue custom does not justify padding.
- **Research blog:** use a lighter surface—direct inline links are often
  better than formal citation syntax—but still name the closest alternatives
  and the works that actually inspired the result. Use stable scholarly
  references and a bibliography when the post makes dense or durable research
  claims.
- **Handout or progress report:** cite the prior art that changes a current
  interpretation, baseline, decision, or candidate publication claim. Link a
  fuller survey or paper for breadth rather than reproducing its bibliography.
  Never leave a borrowed method, figure, dataset, or evaluation unattributed.

The renderer topics preserve citation keys, links, hover cards, bibliography
formatting, and print output. They do not decide which work deserves citation.
Documentation and other technical-writing subgenres may borrow the same
provenance principles when external claims matter, but they do not inherit a
paper-shaped citation density merely by following `technical-writing.md`.
