# Figures, diagrams, and quantitative displays in research documents

> Choose the smallest Quarto-native display that preserves the claim, and
> generate quantitative figures reproducibly from versioned or
> provenance-tracked data into matched web and print assets.

Topic: `document-writing-figures`

Use this topic when a paper, handout, progress report, or research blog asks
for a graph, diagram, visual summary, or unusually rich table. It translates
the request's information and visual-weight intent into Quarto's authoring
vocabulary and a reproducible external plotting path. The requester need not
name a plotting library or exact layout. When the information shape recurs,
choose and name it through
[`result-visualization-templates`](result-visualization-templates.md) before
selecting the renderer.

## Select the display before selecting the tool

Use the simplest row whose information contract fits:

| reader need | default authoring form |
|---|---|
| exact values in a modest comparison | Markdown pipe table with caption, label, and nearby interpretation |
| one existing or generated image | Quarto captioned image with `#fig-*`, `fig-alt`, and an extensionless multiformat path |
| several distinct images that need comparison | Quarto figure div with `layout-ncol` or `layout-nrow` |
| process, sequence, state, or timeline | Quarto-native Mermaid cell |
| dependency graph, hierarchy, or network topology | Quarto-native Graphviz `{dot}` cell |
| simple bar, line, scatter, or distribution used by one document | Python/R executable cell; Matplotlib is the Python default |
| custom annotations, coordinated small multiples, reused figure, or exact matched assets | external quantitative-figure generator reading stable data |
| disposable exploratory plot | Python/R executable cell, promoted when its implementation needs independent testing or reuse |
| filter, hover, selection, or linked exploratory views | Quarto Observable JavaScript (OJS) plus a same-data static figure or table |

Quarto's native Markdown owns placement, layout, captions, alt text,
cross-references, format selection, tables, and text-defined diagrams. It is
not the default quantitative chart grammar. Do not force measured-data charts
through Mermaid merely because a chart-shaped extension exists. A table is
not a substitute when the claim is a curve shape, crossing, distribution, or
dominance relation; a graph is not a substitute when readers need exact
point values.

## Quarto-native vocabulary

The syntax below follows Quarto's current documentation for
[figures and layout](https://quarto.org/docs/authoring/figures-and-layout.html),
[tables](https://quarto.org/docs/authoring/tables.html), and
[diagrams](https://quarto.org/docs/authoring/diagrams.html).

### Figures and matched web/print assets

Generate `figures/swept-curves.svg` and `figures/swept-curves.pdf`, then leave
the extension off in the source:

```markdown
![V11 and GLiNER2 sweep curves by language; higher is better.](figures/swept-curves){#fig-swept-curves fig-alt="Ten shared-scale panels compare both systems over the sweep parameter for overall results and nine languages." width=100%}

The common-scale comparison in @fig-swept-curves shows ...
```

Quarto chooses a target-specific extension. Make SVG the HTML default while
retaining Quarto's PDF-via-LaTeX default of PDF:

```yaml
format:
  html:
    default-image-extension: svg
  pdf:
    keep-tex: true
```

Use an explicit extension only when the same asset is genuinely correct for
every target or no matched form exists. Keep the caption in the document and
make the `fig-alt` description complementary rather than a caption copy.

Treat the document fields as separate semantics:

- the visible figure caption and any subcaptions state the claim, context, and
  panel meaning;
- `fig-alt` describes what a reader who cannot inspect the image needs to know;
- a Markdown image title (`"..."` after the path) becomes an HTML image-title
  attribute, but is optional mouse-hover metadata rather than an accessibility
  substitute; and
- axes, units, facet identifiers, data annotations, and mark/linestyle legends
  stay in the generated asset because they decode the marks. Figure titles,
  captions, sources, and prose codas stay in Quarto.

Quarto accepts Markdown footnote references inside figure-div captions and
ordinary image captions. Keep qualifications as document footnotes so they
remain visible in the endnote stream and printable output. For HTML, enable
the native supplemental popups without making them the sole disclosure:

```yaml
format:
  html:
    footnotes-hover: true
    crossrefs-hover: true
    citations-hover: true
```

Quarto's documented
[`footnotes-hover` and `crossrefs-hover`](https://quarto.org/docs/reference/formats/html.html#footnotes)
cover document references, not arbitrary regions inside a plotted SVG.
Mark/subregion tooltips and legend-decoding interaction remain a researched integration in
[`result-visualization-templates.sketches.md`](result-visualization-templates.sketches.md).

For separately meaningful subfigures, use a figure div. Blank lines between
the div, images, and caption are significant:

```markdown
::: {#fig-two-errors layout-ncol=2}

![False positive.](figures/false-positive.svg){#fig-fp}

![False negative.](figures/false-negative.svg){#fig-fn}

Representative error modes.
:::
```

Do not split one coordinated small-multiple chart into independent Markdown
images merely to obtain layout; one generator should own its shared axes,
legend, annotations, and geometry.

When the evidence is textual, keep it native rather than rendering it through
a plotting library. A cross-referenceable figure div may lay out ordinary
Markdown blocks:

````markdown
:::: {#fig-output-contrast layout-ncol=2}

::: {.condition-card}
**Baseline output**

Role: assistant

The exact selectable output, with **the claim-bearing span** marked.
:::

::: {.condition-card}
**Intervention output**

Role: assistant

The matched selectable output, with **the changed span** marked.
:::

Matched outputs for the same input; bold is redundant to the condition label.
::::
````

Supply responsive HTML and LaTeX styling for `.condition-card` only when the
ordinary block layout is insufficient. Keep literal condition/role labels and
print-safe underline, border, or weight cues even when HTML also uses color.

### Tables

Use a pipe table when a compact set of exact values is the display:

```markdown
| system | peak F1 | sweep value at peak |
|---|---:|---:|
| V11 | 0.91 | 0.30 |
| GLiNER2 | 0.89 | 0.25 |

: Overall sweep summary (higher is better). {#tbl-sweep-summary}
```

Refer to it as `@tbl-sweep-summary`. Follow
[`technical-writing`](technical-writing.md) and the research result-table
rules for population, split, N, metric direction, cost boundary, and nearby
interpretation. A generated table reads the same provenance-tracked evidence as its
figure; do not manually transcribe one from the other.

### Mermaid and Graphviz

Use Mermaid for a compact process or sequence:

````markdown
```{mermaid}
%%| label: fig-evaluation-flow
%%| fig-cap: "Evaluation flow from saved predictions to the handout."
flowchart LR
  A[Saved predictions] --> B[Score and validate]
  B --> C[Figure and summary table]
```
````

Use Graphviz when graph layout is the substance:

````markdown
```{dot}
//| label: fig-dependencies
//| fig-cap: "Evidence dependencies for the headline claim."
digraph G {
  runs -> scores
  scores -> claim
  baselines -> claim
}
```
````

Quarto renders Mermaid natively in HTML and uses Chrome or Edge to create a
PNG for print formats. Keep that documented default for LaTeX PDF; forcing
Mermaid SVG adds conversion dependencies and can clip multiline text. A large
diagram may live in a `.mmd` or `.dot` file and use the cell's `file:` option.

## Default quantitative-figure toolchain

For a Python-oriented research project, default to Matplotlib 3.8 or later.
For a custom, reused, or independently validated figure, use the noninteractive
Agg backend: a committed script reads the canonical tidy CSV/JSON or run-
produced extract, validates its expected conditions, and emits same-stem SVG
and PDF in one run. Emit PNG only for a known raster-only consumer.

```python
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

fig = plt.figure(figsize=(10.5, 5.6), constrained_layout=True)
grid = fig.add_gridspec(9, 2, width_ratios=(3.2, 1.7))
main_ax = fig.add_subplot(grid[:, 0])
breakout_axes = [
    fig.add_subplot(grid[row, 1], sharex=main_ax) for row in range(9)
]
# Read and validate data; draw the overall result on main_ax and one
# language on each breakout axis. Apply the declared y-range policy.
fig.savefig("figures/swept-curves.svg", bbox_inches="tight", facecolor="white")
fig.savefig("figures/swept-curves.pdf", bbox_inches="tight", facecolor="white")
```

Set the physical size in plotting code for a per-figure requirement. Quarto's
Jupyter `fig-width` and `fig-height` options are document/project-level rather
than reliable per-cell sizing controls. Use vector output, shared axes where
comparison demands them, restrained major grid lines, machine-readable text,
and a color-blind-safe palette with line style or markers as a redundant cue.
Do not smooth between sampled measurements unless the interpolation is part of
the declared analysis.

Keep the generator outside the manuscript when the figure is reused, expensive,
custom enough to regression-check, or expected to survive a later LaTeX
cutover. A simple one-document claim-bearing figure may remain an executable
cell when its stable inputs and code are committed and both target renders are
audited. An inline Python figure may use:

````markdown
```{python}
#| label: fig-quick-check
#| fig-cap: "Exploratory score distribution."
#| fig-alt: "Histogram of scores with a long lower tail."
#| echo: false

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(5.5, 3.0), constrained_layout=True)
# draw
plt.show()
```
````

Promotion means moving the plotting logic to a script and including its
generated assets; do not retain a second independently edited implementation
in the cell. The worked PII sweep below merits promotion because coordinated
axes, computed annotations, validation, and exact cross-format layout are part
of its claim.

### External alternatives

Choose for the program's existing language and the artifact's real need:

| tool | use it when | cost or boundary |
|---|---|---|
| [Matplotlib](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html) | default Python static publication figure; custom annotations and exact layout matter | imperative code; commit the generator and both vector outputs |
| [Seaborn atop Matplotlib](https://seaborn.pydata.org/tutorial/relational.html) | an existing Python project benefits from concise faceting or statistical defaults | custom peak/crossing labels still use Matplotlib axes; do not add it for one trivial plot |
| [ggplot2](https://ggplot2.tidyverse.org/reference/ggsave.html) | the research pipeline is already R-native; facets and grammar-of-graphics composition fit | use `ggsave()` for explicit same-size SVG and PDF outputs; do not introduce R only for a figure |
| [Altair + `vl-convert-python`](https://altair-viz.github.io/user_guide/saving_charts.html) | a committed Vega-Lite JSON specification or one declarative source for static and interactive variants is valuable | save JSON, SVG, and PDF; `vl-convert` is the maintained image-export path |
| [Observable Plot in OJS](https://quarto.org/docs/interactive/ojs/) | client-side filters, selections, or responsive exploratory views materially help the HTML reader | retain a same-data static view for print and JavaScript failure; avoid remote runtime data |
| [Plotly](https://plotly.com/python/static-image-export/) | the project already uses it or zoom, 3-D, geographic, or specialized interaction earns the dependency | static SVG/PDF export requires Kaleido and a compatible Chrome/Chromium; not the ordinary static default |
| [PGFPlots/TikZ](https://ctan.org/pkg/pgfplots) | LaTeX is already canonical and exact TeX typography or geometry dominates | weak browser path; use after print-first selection or cutover, not as the Markdown-plus default |

Prefer the project's already competent stack over ecosystem churn. A tool
choice never relaxes the same-data web/print contract.

## Build and freshness contract

A small Quarto project can make regeneration explicit through Quarto's
[project scripts](https://quarto.org/docs/projects/scripts.html):

```yaml
project:
  type: default
  pre-render: scripts/figures/build-swept-curves.py

format:
  html:
    default-image-extension: svg
  pdf:
    keep-tex: true

execute:
  echo: false
```

Run and debug the generator independently, then render both targets:

```bash
quarto run scripts/figures/build-swept-curves.py
quarto render index.qmd --to html
quarto render index.qmd --to pdf
```

These commands follow Quarto's [`run`](https://quarto.org/docs/cli/) and
[`render`](https://quarto.org/docs/cli/render.html) interfaces.

For the normal reproducible path, `quarto render` at the project root invokes
the `pre-render` script from that root. Record the Quarto, Python/R, and plotting
package versions beside the document. A script must fail clearly on missing
inputs, unexpected categories, duplicate keys, nonfinite plotted values, or an
unwritable output—not silently omit a panel or retain an old asset.

Do not enable Quarto `freeze: auto` around externally changing claim-bearing
data and assume freshness: Quarto's execution cache keys primarily on source
changes, so changed external inputs can leave frozen output stale. Prefer an
explicit generator/pre-render step. If a site deliberately commits `_freeze`
for portability, document how external-data changes invalidate and refresh it.

## Worked pattern: V11 versus GLiNER2 main-and-breakout curves

Interpret “a small graph of the swept curves for each of nine languages and
overall, spark style with peak/crossing labels, usual scale” as an information
and visual-weight request, not a demand for a particular library. The nearest
faithful default is the **main-and-breakout figure** defined in
[`result-visualization-templates`](result-visualization-templates.md): the
weighted overall curve is a full-height main panel on the left, while nine
short rectangular language panels stack in a breakout column on the right.

- the main `overall` panel keeps the ordinary full metric scale and reading
  priority; language panels use one shared truncated linear range where
  possible, or clearly label their different ranges if local shape rather than
  cross-language level is the intended comparison;
- keep language panels short and wide, put their y ticks on the outer right
  edge, and use an unmistakable break mark only when a separated low point
  makes simple truncation impossible;
- V11 and GLiNER2 keep the same color, line style, marker, and order in every
  panel; show markers at sampled sweep values and use one shared legend;
- each panel header carries a compact literal summary, for example
  `V11 .91@.30 · G2 .89@.25 · cross ≈.18`, leaving the plot area uncluttered;
- peak labels give the measured maximum and sampled sweep value; ties follow
  one stated rule rather than whichever row is encountered first;
- report an exact crossing only when measured equality exists. Otherwise use
  `≈` only for linear interpolation between adjacent sampled points where the
  signed system difference changes sign. Never extrapolate or infer a crossing
  from smoothing. Say `no cross` when none is observed; if there are several,
  report the count or the decision-relevant one under a stated rule;
- uncertainty ribbons appear only when repeated measurements or a justified
  interval exist; the absence of a ribbon must not imply certainty; and
- the caption defines aggregation for `overall`, metric and good direction,
  split and N, common scale, crossing interpolation, and the intended takeaway.

The generator consumes tidy rows with at least `language`, `system`, sweep
parameter, metric, split, and N (plus seed/interval fields when applicable).
Before plotting, assert exactly the expected ten panels and two systems,
unique condition keys, sorted sweep values, and the intended main/breakout
scale policies.
Emit a compact summary CSV or table of peaks and crossings when exact lookup
matters.

If a two-column venue makes the asymmetric composition illegible, place
`overall` full-width above a 3-by-3 language grid, or use a full-width figure
environment. For a Quarto-to-LaTeX target whose class uses the conventional
two-column float, add `fig-env="figure*"` to the figure attributes and verify
the venue output. A lower-weight fallback may reduce tick labels and annotate
only the peaks/crossings that affect the conclusion. Do not silently make each
language panel a differently autoscaled sparkline; every local range is visible
and the caption states what cross-panel comparisons remain valid.

## Interactive variant

Interaction is optional enhancement for this example. For a static generated
image, Quarto's HTML [`lightbox: true` or image class
`.lightbox`](https://quarto.org/docs/output-formats/html-lightbox-figures.html)
supplies a supported click-to-enlarge path and carries its document caption
into the lightbox. An OJS selector may instead enlarge one language, inspect
exact points, or toggle uncertainty, reading the same local CSV with
`FileAttachment`. The static main-and-breakout display remains in initial HTML
and PDF and carries the claim; do not make hover the only source of peak or
crossing values. Third-party OJS `require()` imports normally load from a
content delivery network, so use built-ins or local modules for a durable,
simple-host artifact unless an online dependency is explicitly accepted.

## Release check

Before dissemination:

1. regenerate from the recorded source data and inspect generator validation;
2. render HTML and PDF using the recorded commands;
3. compare values, scales, defaults, captions, and selection between the
   figure, summary table, interactive view, and source rows;
4. inspect SVG at browser width and PDF at actual print size in color and
   grayscale for clipped text, disappearing distinctions, unreadable panels,
   missing glyphs, or rasterized vector content; and
5. run the cold-reader scan from [`technical-writing`](technical-writing.md).

For quality-versus-cost comparisons of three or more systems, also follow the
specialized [`pareto-figures`](pareto-figures.md) contract.
