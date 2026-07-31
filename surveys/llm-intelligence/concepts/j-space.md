# j-space — verbalizable global workspace in language models

> Understanding/summary page (our ideas + beliefs about the work — the primary
> artifact we reason on). Short handle: `j-space`. Trust: `single-source`
> (one lab, one paper, not independently reproduced). Grounded from the primary
> source (WebFetch 2026-07-30); full HTML + bibliography extract built 2026-07-31.
>
> **Authors** (from the paper's Author Contributions; the byline is JS-rendered
> and front-matter `authors:[]` is empty): Wes Gurnee (led J-lens development)
> and Jack Lindsey (corresponding, jacklindsey@anthropic) conceived the method,
> with Nicholas Sofroniew, Subhash Kantamneni, Mateusz Piotrowski, Isaac Kauvar,
> and Adam Pearce (Anthropic).

**Sources (for reconstituting the git-ignored full-text extract):**
- Primary: "Verbalizable Representations Form a Global Workspace in Language
  Models," Anthropic, 2026 —
  https://transformer-circuits.pub/2026/workspace/index.html
- Companion announce: https://www.anthropic.com/research/global-workspace
- Skeptical read (useful counterweight): Zvi Mowshowitz, "No Space Like
  J-Space," https://thezvi.substack.com/p/no-space-like-j-space

Extract (built 2026-07-31, git-ignored):
`related-work/extract/j-space/2026/workspace/` — full page + figures, plus
`bibliography.bib` (the 807-entry shared transformer-circuits bib) and
`cited.bib` (the **171 keys this paper actually cites**). Consult only for
specifics this summary omits (e.g. exact layer indices per model, the full
five-property experiment tables).

Map node: [`survey.md` § ANCHOR](../survey.md). Related concept pages (as they
land): `activation-decoding` (cluster G — the live sibling family), `tuned-lens`,
`sae`, `actadd`, `attribution-graphs`, `cot-faithfulness`, `introspection`,
`global-workspace`.

## What it is

Two coupled artifacts:

- **J-lens** — for layer ℓ, the averaged Jacobian `J_ℓ = E[∂h_final,t′/∂h_ℓ,t]`
  over token positions and ~1,000 prompts: the *first-order causal effect* of an
  activation on the final output. Applied to an activation it returns a ranked
  list of vocabulary tokens that activation is "disposed to make the model say."
- **J-space** — the set of points expressible as **sparse nonnegative
  combinations of J-lens vectors**. Empirically: ~10–25 vectors active per
  position; overcomplete (n_vocab ≫ d_model); **<10% of activation variance**;
  concentrated in **middle layers** (~38–92 in the large model), flanked by
  "sensory" (early) and "motor" (late) regions.

**Five functional properties** argued to make J-space a *global workspace*:
(1) verbal report — swapping J-lens vectors causally changes the model's output;
(2) directed modulation — the model can deliberately activate workspace vectors
on instruction; (3) internal reasoning — intermediate steps ("spider"→"8 legs")
appear as J-lens vectors before being said; (4) flexible generalization — a
vector works across functions; (5) selectivity — mediates flexible reasoning but
not automatic processing (e.g. text parsing).

## Why it matters (the load-bearing distinction)

J-lens vectors are **causal, output-disposition units**. Keep them distinct from
the two things they most resemble:
- **not** a correlational lens (logit lens = raw unembedding; tuned lens =
  learned affine — both predict the *output* and skip the intermediate);
- **not** reconstructive SAE features (same sparse-nonneg-overcomplete algebra,
  but SAEs fit to *reconstruct the activation*, input-side and unsupervised;
  J-lens ranks by *effect on what is said*, output-side).

So J-space is the proposed instrument for "what latent, verbalizable concept is
actually driving this output" — a causal read of the reasoning the model does
*without writing it down*, which is exactly the gap that CoT unfaithfulness
(said ≠ used reasoning) opens. Its nearest recent sibling is Anthropic's
attribution-graph circuit tracing (2025): both are causal interpretability from
the same lab — attribution graphs map the *pathway between features*, J-lens
ranks a single activation's *output-token disposition*.

A second, more direct sibling family — surfaced by reading the paper's actual
citations — is **activation→language decoding** (SelFIE, LatentQA, Activation
Oracles, Natural Language Autoencoders; survey cluster G). Those decode an
activation into *free-text* explanation; J-lens decodes it into a *ranked token
disposition* carrying a first-order **causal** guarantee (∂output/∂activation).
Expressivity vs. causal faithfulness is the axis, and J-space is the causal pole
of exactly this family — which is why it reads as "the causal version of asking
the model what an activation means."

## Our assessment / trust

- **Grade `single-source`.** One lab, one 2026 paper; no independent
  reproduction. Effects concentrate on Anthropic models (Opus/Sonnet/Haiku) and
  vary with scale — no cross-architecture transfer shown.
- **Consciousness framing is coverage hype the authors disclaim.** They state
  "we take no position" on consciousness and separate *access* (functional,
  reportable — what they study) from *phenomenal* (subjective). They do **not**
  claim transformers reproduce the brain's global-workspace architecture (no
  encapsulated modules, no recurrence, no sharp ignition). Secondary press ("Is
  Claude conscious?") over-reads. Zvi: a real mechanistic advance, but
  "privileged representation → functional unity → global workspace" are three
  escalating claims, each needing more evidence.
- **Self-stated limits:** J-lens sees only **single-token** concepts; Jacobian
  averaging over 1,000 prompts may smear context-specific content; "empty" early
  layers may be lens degeneracy, not genuine absence. Authors call J-lens "an
  imperfect tool [that] only approximately and incompletely captures the model's
  underlying workspace structure."
- **Scope reminder:** J-space is <10% of activation variance — a *small* slice.
  Claims about "the model's thinking" are claims about this slice, not the whole
  computation.

## Open questions

Now answerable from the local extract (fetched, not yet distilled here — the
next in-depth read):
- Exact per-model layer ranges and the sensory/middle/motor boundary criteria.
- The full five-property experiment tables and any ablations/baselines.
- The verbatim introspection protocol and how directly it adapts Anthropic's
  2025 *Emergent Introspective Awareness* concept-injection method.

Resolved on the 2026-07-31 pass: the **bibliography is extracted** (171 cited
keys, `related-work/extract/j-space/2026/workspace/cited.bib`), confirming the
survey's cluster structure and surfacing cluster G; and the **author list** is
recovered from the Author Contributions section (see the header).
