# Result-visualization templates

> Name and choose reusable layouts that make quantitative results, qualitative
> examples, and subgroup evidence quickly legible without hiding comparison or
> scale semantics.

Topic: `result-visualization-templates`

Use this registry after deciding what a reader should be able to see and before
choosing a plotting package. The names are communication handles for paper,
handout, progress-report, and research-blog work; they describe information
structure rather than a renderer.

Current status: the static layout contracts below are current guidance. The
component-level interaction, cross-renderer style bridge, and fully reusable
native qualitative panels remain researched sketches in
[`result-visualization-templates.sketches.md`](result-visualization-templates.sketches.md),
tracked by
[`gaps/result-visualization-templates-research.md`](../gaps/result-visualization-templates-research.md).

## Grounding and scope

This is a focused grounded reconnaissance, not an exhaustive visualization
survey. Coverage cutoff: 2026-08-12. The inspected anchors were foundational
visualization guidance, official renderer documentation, and visually polished
ML papers or research articles selected as examples of recurring forms. Their
publication success does not show that the visual form caused their success.

Two general results guide the registry:

- graphical-perception work favors position on a common scale for accurate
  numerical comparison; Heer, Bostock, and Ogievetsky summarize that evidence
  in [*A Tour Through the Visualization Zoo*](https://idl.cs.washington.edu/files/2012-VisualizationZoo-CACM.pdf);
- Shneiderman's [overview-first, detail-later pattern](https://hci.stanford.edu/courses/cs448b/papers/shneiderman96eyes.pdf)
  motivates overview/detail interaction, while a static compound figure must
  still expose the important detail without requiring interaction.

## Contracts shared by every template

### The document owns the context

The enclosing Markdown/Quarto source owns the figure-level title, claim-bearing
caption, coda, source/provenance, footnotes, and explanatory prose. Do not bake
those into a PNG, SVG, or plotting canvas merely so a copied image remains
self-explanatory. The rendered asset contains only what is needed to decode the
display itself: axes, ticks, units, short facet identifiers, mark or linestyle
legends, and data-anchored annotations.

This boundary keeps context selectable, searchable, cross-referenceable, and
able to reflow in HTML and print. A figure likely to circulate detached may use
a concise in-asset identifier, but it does not duplicate the document caption.
Long per-panel summaries belong in native panel captions, an adjacent native
table, or a footnote coda when feasible.

### Print proof is mandatory

Every print figure must remain legible in grayscale at its actual placed size.
Hue may reinforce a distinction but cannot own it. Pair color with a redundant
cue such as solid/circle versus dashed/square, direct labels, shape, or ordered
lightness. Text examples retain literal role labels or symbols when their
background colors disappear. This follows IEEE's explicit advice to test a
[grayscale printout and combine color with shape or line style](https://books.ieeeauthorcenter.ieee.org/prepare-your-book-manuscript/create-original-graphics/)
and the W3C rule that [color is not the only visual means](https://www.w3.org/WAI/WCAG20/Understanding/use-of-color).

The plot box is not sacred. A heavy four-sided rectangle can hide extrema and
overweight a compact panel. Prefer open axes or light graph-paper-like major
guides when they preserve orientation; remove or lighten a top/right spine that
competes with data; and give observed minima and maxima enough display padding
or unclipped margin that the frame does not cover them. Keep ticks and units.
Nature's figure guide requires axes and ticks while emphasizing legibility and
editable vector text; it does not require a four-sided box
([specification](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/)).

Inspect color, simulated grayscale, and the final PDF. A pale raw-point layer
that vanishes in grayscale is not evidence merely because the colored screen
version looked attractive.

### Scale changes announce themselves

Use a full or shared scale when absolute levels are part of the comparison.
Use a truncated linear range when local shape is the point and every observed
point remains visible; label its endpoints and state the truncation in the
caption. Use a broken axis only when a separated outlier would otherwise waste
most of the panel, with an unmistakable break mark. Use a log scale only for a
positive quantity whose multiplicative interpretation is meaningful. A compact
panel with axes is *spark-like*, not an unlabeled sparkline.

Panels with different ranges permit within-panel shape comparison, not silent
cross-panel level comparison. Use one shared breakout range when the levels
must be compared.

### Examples are data-bearing displays

Textual inputs, outputs, traces, and token highlights should normally remain
native selectable text laid out by Quarto/Pandoc blocks or tables. A plotting
library need not rasterize text to make it a subfigure. Keep condition, role,
selection rationale, and exact wording in markup; use restrained backgrounds,
underlines, borders, or inline labels for annotation. Reserve external images
for visual source material or geometry the document renderer cannot express.

## Template registry

| template | reader question | normal medium |
|---|---|---|
| **main-and-breakout figure** | What is the main result, and how does it vary in the important subgroups or examples? | asymmetric external plot or mixed plot/native blocks |
| **shared-scale small multiples** | How do equally important subsets compare under one visual grammar? | faceted external plot or Quarto figure panel |
| **annotated transcript contrast** | What changed between methods, conditions, or interventions on the same input? | native text blocks or table |
| **representative-example gallery** | What does the phenomenon look like across deliberately selected cases? | native cards, text rows, images, or mixed media |
| **distribution-and-exemplars display** | Where does the population lie, and what do meaningful positions in it look like? | quantitative overview plus linked native examples |
| **task–method–evidence teaser** | What is the task, what was built, and what concrete evidence or asset came out? | first-page/first-screen compound figure |
| **empirical-law grid** | Does one relationship recur across controlled axes, regimes, or scales? | coordinated repeated plots |

The established `pareto-figures` contract is a specialized comparison
template and remains in
[`pareto-figures.md`](pareto-figures.md). A failure atlas is a paper form; its
displays may use several templates here rather than constituting one fixed
layout.

## Main-and-breakout figure

The **main-and-breakout figure** is an asymmetric compound display. A
reading-priority main panel spans the full height on the left; a vertical stack
of compact breakout panels occupies the right. In narrow print, place the main
panel above a wrapped breakout grid rather than shrinking the labels to fit.

The main panel normally carries the aggregate, weighted result, canonical
scale, or conclusion. Breakouts answer “where did that come from?” They may be
compact curves, subgroup tables, annotated transcripts, or representative
example cards. Thus the form is broader than a Matplotlib subplot recipe.

For quantitative breakouts:

- retain an ordinary x scale and enough ticks to decode it;
- put compact-panel y ticks on the outer right edge when that reduces clutter;
- prefer a visibly labeled truncated linear range; use a broken or log axis
  only under the shared scale-change contract above;
- keep method encoding identical between main and breakout panels;
- remove or lighten a spine that coincides with an extremal curve; and
- preserve observed-point markers and do not smooth unsupported values.

The asymmetry is meaningful: if every panel deserves equal reading priority,
use shared-scale small multiples instead.

## Shared-scale small multiples

Use **shared-scale small multiples** when categories have equal status and
cross-panel comparison is the main act. Repeat the same mark grammar, axis
domains, ordering, and annotations; omit redundant labels only when shared
labels remain unambiguous. Vega-Lite calls this a trellis plot or small
multiple and documents it as a series of similar plots over data subsets
([faceting](https://vega.github.io/vega-lite/docs/facet.html)).

Shared scale is the default because position on a common scale is the reader's
comparison mechanism. If one subgroup needs a zoom, retain the shared-scale
figure and add a clearly labeled zoom/difference companion rather than quietly
autoscaling one facet.

## Annotated transcript contrast

Use an **annotated transcript contrast** for paired or small-multiple textual
conditions: baseline versus intervention, expected versus observed, or several
agent trajectories on the same task. Align the same input and role order,
label every condition literally, and highlight only the span or stage that
supports the claim. Color is redundant to role names, underlines, borders, or
symbols.

Prefer Quarto block layouts, fenced divs, or a width-controlled Markdown table
so the text remains selectable. Quarto's `layout` attributes apply to ordinary
block content as well as images
([block layout](https://quarto.org/docs/authoring/figures-and-layout.html#block-layout)).
The side-by-side first figure in
[*Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*](https://arxiv.org/abs/2201.11903)
and the role-colored trajectories in
[*ReAct*](https://arxiv.org/abs/2210.03629) are polished examples of the
comparison form. Their exact visual styling is inspiration, not a requirement.

## Representative-example gallery

A **representative-example gallery** uses a uniform card or row shell to show
several cases selected under an explicit policy: maximum activation, stratified
random draws, quantiles, boundary cases, failure modes, or a balanced mixture.
The selection rule appears in the caption or nearby prose; “interesting
examples” is not a sampling policy.

The gallery is evidence rather than decoration. Keep labels and annotations
stable across cards, include enough counterexamples or weaker cases to bound
the interpretation, and move exhaustive browsing to an appendix or interactive
companion. Distill's
[*Feature Visualization*](https://distill.pub/2017/feature-visualization/)
repeatedly juxtaposes optimized and dataset examples; Anthropic's
[*Scaling Monosemanticity*](https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html)
shows representative top-activating text with token-level activation strength
and links to a larger browser.

## Distribution-and-exemplars display

A **distribution-and-exemplars display** couples a quantitative population
view with examples anchored to meaningful locations such as high/low
activation, quartiles, a decision boundary, an outlier, or a transition. The
chart prevents cherry-picked examples from masquerading as prevalence; the
examples make the distribution semantically inspectable.

Link each exemplar to a plotted stratum or point. State how it was chosen and
show N and the population definition. A main-and-breakout layout is often a
good physical realization, with the distribution as main and example cards as
breakouts. *Scaling Monosemanticity* explicitly combines activation
distributions with low- and high-activation examples.

## Task–method–evidence teaser

A **task–method–evidence teaser** is a first-page or first-screen map of the
paper: one panel makes the task concrete, one gives only the method structure
needed to understand it, and one shows the resulting evidence, asset, or scale.
It is not an abstract pasted into boxes. The reading order and arrows must
state how the three pieces depend on one another.

Figure 1 of
[*Segment Anything*](https://arxiv.org/abs/2304.02643) connects its promptable
task, model, and data engine/dataset in one visual argument. Use this form when
the contribution genuinely has several interlocking objects; a one-method,
one-result paper usually needs a simpler worked-example contrast or result
figure.

## Empirical-law grid

An **empirical-law grid** repeats one relationship across controlled changes in
model size, data, compute, task, or regime. Use consistent axis transforms,
fit grammar, color/line semantics, and annotation placement. Put the law or
fit claim in the enclosing caption; reserve in-panel text for parameters,
regime labels, and data-anchored exceptions.

The opening figures of
[*Scaling Laws for Neural Language Models*](https://arxiv.org/abs/2001.08361)
use repeated log-scale plots and stable visual grammar to make one empirical
relationship legible across size, data, and compute. Do not use the form merely
to make unrelated plots look unified: the repeated grammar must correspond to
a repeated claim.

## Selection rule

Choose the template by the comparison the reader must perform:

1. one aggregate plus explanatory subgroups or examples →
   **main-and-breakout**;
2. equal-status subgroup comparison → **shared-scale small multiples**;
3. exact textual behavior under matched conditions →
   **annotated transcript contrast**;
4. breadth of a qualitative phenomenon → **representative-example gallery**;
5. prevalence plus semantics → **distribution-and-exemplars**;
6. task/contribution map at first contact →
   **task–method–evidence teaser**; and
7. one predictive relationship across controlled axes →
   **empirical-law grid**.

Combinations are legitimate when the reader questions genuinely combine. Name
the primary template and the embedded secondary template; do not collapse two
separate claims into one dense figure merely to save a figure number.
