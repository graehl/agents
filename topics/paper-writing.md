# Paper writing

> Write a selected research paper as a form-led, evidence-traceable argument
> for a cold reader, inheriting the shared technical-writing contract without
> replaying the research program's chronology.

Topic: `paper-writing`

## Enter from a selected publication case

Follow [`research-writing`](research-writing.md), which inherits the shared
cold-reader, terminology, display, and synthesis contract from
[`technical-writing`](technical-writing.md) and adds prior-art, attribution,
and citation coverage. The proposal portfolio, evidence ceiling, form
selection, and promotion path remain in
[`paper-drafting`](paper-drafting.md). Start a paper from its promoted proposal,
not by treating every prior handout or “paper draft” as manuscript prose.

The selected form from
[`successful-paper-forms`](successful-paper-forms.md) controls the abstract
promise, section order, principal comparison, and repeated presentation
cadence. A paper normally has one governing form. A theoretical result may
support the same central empirical claim; an independent reader promise usually
deserves a separate paper.

Put an abstract at the beginning of every paper, immediately after its front
matter and before the body. Draft it early as part of the evidence-bearing
spine, then revise it after the body stabilizes. It states the problem and
regime, intervention or finding, principal quantitative result, and most
important scope boundary or community asset. A paper skeleton still begins
with an abstract; unsupported quantities remain explicit `TBD`s rather than
being omitted or made fluent.

## Backfill the selected paper case

A serious paper is prospective after theme and form selection: use its skeleton
to identify research effort that would strengthen both evidence and legitimate
reader interest. Typical backfill includes stronger simple baselines,
uncertainty and replication, breadth or boundary cases, decisive qualitative
examples, cleaner visual comparisons, related-work contrasts, and releasable
community assets.

Every backfill item names the proposal verdict or claim it could change and
remains a `TBD` until its evidence exists. The writing phase may propose this
effort but does not itself authorize runs. When backfill fails, costs too much,
or leaves the evidence ceiling unchanged, narrow the claim or choose another
form instead of defending the selected narrative.

## Draft the evidence-bearing spine

Draft the result-bearing spine before explanatory transitions: abstract claim,
principal comparison, one canonical figure or table, section-level takeaways,
and the limitations that bound the claim. Each load-bearing assertion traces to
the proposal's evidence matrix and then to a primary result, run record, or
source.

The form cannot raise the evidence ceiling. Keep unsupported assertions
explicitly speculative, and make every `TBD` name the missing measurement and
outcome that would confirm or falsify the surrounding claim. Failed attempts
that affect validity, attribution, generality, or practical cost remain visible
even when routine chronology moves to the log or appendix.

Consult [`paper-attractiveness`](paper-attractiveness.md) only after this spine
exists. Use its features to communicate a supported result or real community
asset, not to manufacture importance.

## Account for compute, energy, and dollar cost

Consider a compact compute, energy, and cost section for every empirical paper;
include it when the quantities are material and can be estimated honestly.
Separate the terminal reproduction run, the critical path that produced and
validated the reported result, and the full research program when more than one
is available. For each reported scope, give hardware, accelerator- or
device-hours, elapsed time, the measured or assumed average power in watts,
estimated energy in kilowatt-hours, and the uncertainty or estimation basis.
Do not present thermal design power as a meter reading.

Report actual AWS Spot expenditure separately from a local-compute equivalent.
For local accelerator use, estimate the AWS Spot-equivalent cost from a named
comparable instance, region, price observation date, and per-device allocation;
state hardware mismatches such as L40 versus L40S. Keep that counterfactual
distinct from money actually spent. A useful compact table is `scope | stage |
hardware | device-hours | power basis | kWh | actual cloud spend | local
cloud-equivalent cost`.

Promote efficiency into the abstract or introduction only when the paper has a
fair comparison showing an unusually strong result per critical-path energy or
dollar—not merely a small absolute run. Name the quality, coverage, or other
achievement held in the numerator and the critical-path boundary used in the
denominator. Energy, money, and carbon are different quantities; estimate
carbon only with a sourced time-and-region electricity-intensity assumption.

## Cover the work that determines the claim

Cover the nearest competitive neighborhood completely enough that an informed
reader can audit the novelty, baseline, and alternative interpretation. Always
include the closest competing or alternative work and the most influential or
inspirational intellectual parents. Cite primary sources for borrowed tasks,
data, metrics, methods, code, theorems, and central results, and include
counterevidence that materially bounds the claim.

Appropriate density is an outcome, not a quota. Synthesize broader background
selectively and explain how each cited cluster relates to the paper. A
cite-heavy venue style does not justify bibliography padding, while a short
paper is not excused from the one omitted competitor that would change its
publication case. Use the shared field/frontier survey route in
`research-writing.md` before making novelty or absence claims.

## Produce browser and submission artifacts

Follow [`document-writing`](document-writing.md) when the draft first needs a
renderer, bibliography, local assets, or multiple outputs. Start from one
canonical Markdown-plus source; Quarto is the operational default for ordinary
static HTML plus working PDF, while MyST or direct Pandoc may better expose a
future TeX handoff. Direct TeX becomes canonical only through an explicit
source promotion when a venue template cannot be represented repeatably.

Use [`document-writing-printable`](document-writing-printable.md) for the venue
and arXiv package. A browser companion follows
[`document-writing-browser-interactive`](document-writing-browser-interactive.md)
and supplies a static printable equivalent for every interactive claim.

## Relationship to shorter research artifacts

A handout inherits these authoring rules at the lower cooperative-review proof
bar in `handout-writing.md`; a progress report may preview a paper case. A paper
may cite their recorded decisions or tables, but neither substitutes for a
self-contained manuscript: inherit shared wording and displays deliberately,
then re-establish the evidence chain and reader promise under the selected
form.

Manuscript-pass and attraction-feature candidates remain explicitly untested in
[`paper-writing.sketches.md`](paper-writing.sketches.md). Collaboration
platform, coauthor workflow, and venue-specific final checklists should be
decided for the first real paper rather than guessed globally.
