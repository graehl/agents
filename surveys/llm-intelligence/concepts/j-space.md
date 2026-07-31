# j-space — verbalizable global workspace in language models

> Understanding/summary page (our distillation — the primary artifact we reason
> on, so we don't re-open the 323 KB paper). Short handle: `j-space`. Trust:
> `single-source`. Deep read of the full local extract 2026-07-31 (initial
> WebFetch grounding 2026-07-30).

**Paper.** "Verbalizable Representations Form a Global Workspace in Language
Models," Anthropic, published **July 6, 2026** (transformer-circuits.pub).
Primary model **Claude Sonnet 4.5**; key results corroborated on Haiku 4.5 and
Opus 4.5, some analyses on Opus 4.6.

**Authors** (16). Wes Gurnee\* and Nicholas Sofroniew\* (core contributors);
Adam Pearce, Mateusz Piotrowski, Isaac Kauvar, Runjin Chen, Anna Soligo, Paul
Bogdan, Euan Ong, Rowan Wang, T. Ben Thompson, David Abrahams, Subhash
Kantamneni, Emmanuel Ameisen, Joshua Batson; Jack Lindsey\*† (correspondence,
jacklindsey@anthropic.com). \*core contributor.

**Full text (click through; also reconstitutes the git-ignored extract):**
- Primary: [Verbalizable Representations Form a Global Workspace in LMs](https://transformer-circuits.pub/2026/workspace/index.html) (transformer-circuits)
- Companion announce: [anthropic.com/research/global-workspace](https://www.anthropic.com/research/global-workspace)
- Skeptical read (counterweight): [Zvi Mowshowitz, "No Space Like J-Space"](https://thezvi.substack.com/p/no-space-like-j-space)

Extract (built 2026-07-31, git-ignored):
`related-work/extract/anthropic2026-jspace/2026/workspace/` — full page + figures, plus
`bibliography.bib` (807-entry shared bib) and `cited.bib` (the **171 keys this
paper cites**). Consult for specifics this summary omits (exact figures, ablation
tables, the appendix formalization + multi-token extension).

Map node: [`survey.md` § ANCHOR](../survey.md). Related concept pages (as they
land): `activation-decoding` (cluster G), `hernandez-relation-jacobian` (the
methodological ancestor), `tuned-lens`, `sae`, `attribution-graphs`,
`cot-faithfulness`, `introspection`, `global-workspace`, `alignment-auditing`.

## What it is (precise)

Two coupled artifacts on the residual stream `h_ℓ` at layer ℓ:

- **J-lens.** The averaged Jacobian
  `J_ℓ = E_{t, t′≥t, prompt}[∂h_final,t′ / ∂h_ℓ,t]` over source position t, all
  later positions t′, and **1,000 pretraining-like prompts** — one d_model ×
  d_model matrix per layer. Readout: `lens(h_ℓ) = softmax(W_U · norm(J_ℓ h_ℓ))`,
  a score over the whole vocabulary; the **J-lens vectors** are the rows of
  `W_U J_ℓ`, one direction per vocabulary token. The averaging is the crux — it
  isolates a token's *general disposition to be verbalized* from its use in one
  context. **The logit lens is the special case `J_ℓ = I`** (raw unembedding);
  J-lens is "the principled correction" that recovers interpretable content in
  earlier layers where the logit lens degenerates. (The paper still finds the
  logit lens quite useful, capturing much workspace structure at lower
  reliability.)
- **J-space.** The set of points expressible as a **sparse nonnegative
  combination of k J-lens vectors** (k somewhat arbitrary, typically ≤ 25 — the
  empirically observed number of meaningfully-active vectors). Overcomplete
  (n_vocab ≫ d_model) so decompositions are non-unique; found by gradient
  pursuit. An activation's **J-space component** (nearest J-space point) is
  **< 10% of activation variance** (varies by layer, never > 10%). Under
  superposition, the J-lens vectors are a token-indexed **subframe** of the
  model's full feature frame; the bulk of features lie outside it.

Two use modes. **Read**: rank the vocabulary, probe one token by inner product,
or sparse-decompose into a discrete concept inventory. **Write**: steer
`h ← h + αv_t`; ablate (negative α, or project out v_t); or *patch lens
coordinates* to swap concept s for t while leaving the orthogonal complement of
`span{v_s,v_t}` fixed.

## The global-workspace case — five functional + three structural properties

**Five functional properties** (each its own experiment section):
(1) **verbal report** — readouts match what the model says it is thinking;
swapping a vector changes the answer; (2) **directed modulation** — on
instruction the model activates/holds workspace vectors independent of its
output, and pulls in normally-absent info when a task needs it; (3) **internal
reasoning** — intermediates (spider → 8 legs) appear as J-lens vectors before
being said, and intervening redirects the conclusion; (4) **flexible
generalization** — a vector lifted from one context is correctly operated on by
whatever function the new context supplies; (5) **selectivity** — a small subset,
required for flexible reasoning but *not* automatic processing (text parsing,
grammar). The model speaks, parses, and does much automatic inference with the
J-space suppressed, but struggles at complex internal reasoning.

**Three structural signatures** (J-space as an object, not only via behavior):
- **Layer band = "workspace."** Workspace-like content lives only in a middle
  band, **~L38–L92** on a [0–100] reindexing of layers, flanked by **sensory**
  (early ~third, empty/uninterpretable) and **motor** (late, aligned to the
  imminent output) regimes. Four lens metrics (next-token top-k accuracy, excess
  kurtosis, cross-position autocorrelation, effective dimensionality) plus CKA
  block structure all agree. An **ignition** test — replace a token embedding
  with a mixture `(1−α)e_B + αe_A` of two country names and sweep α — shows the
  activation switching *sharply* between interpretations starting ~L38, evidence
  the onset is real, not a lens artifact.
- **Limited capacity.** Occupancy plateaus ~25 across the band; ~6 *unrelated*
  list-words held at once (only ~1–2 at a single layer); *related* words load the
  whole category (even unread ones), and a category switch **evicts** the old
  set. "Many items in the J-space" = focusing on a shared category, not recalling
  many items.
- **Broadcast hub.** MLP blocks amplify J-lens directions ~10× vs neuron
  directions; a top-1% set of **broadcast heads** relays J-space content across
  positions. Ablating those heads drops J-lens recall@25 (0.86→0.67) and
  injected-thought report rate (0.54→0.09) but changes the output at only 5% of
  positions (vs 2% control) — they act on *workspace contents*, not the output.

## Why it matters — the load-bearing distinctions

J-lens vectors are **causal, output-disposition, single-token** units. Keep them
distinct from their neighbors:
- **vs correlational lenses** — logit lens (`J=I`, raw unembedding) and tuned
  lens (learned affine, trained to match the output → "skips ahead" to the final
  token rather than surfacing intermediates);
- **vs reconstructive SAE features** — same sparse-nonneg-overcomplete algebra,
  but SAEs fit to *reconstruct the activation* (input-side, unsupervised); J-lens
  ranks by *effect on what is said* (output-side);
- **vs attribution graphs** (2025) — those trace the *pathway between features*
  per prompt; J-lens is a single precomputed matrix giving an activation's
  general output-disposition;
- **vs activation→language decoders** (cluster G: SelFIE, LatentQA, Activation
  Oracles, NL-Autoencoders) — free-text and expressive but confabulation-prone;
  J-lens is cheap + causal but limited to single tokens. The paper places itself
  at the **cheap-and-grounded** end of this spectrum, complementary not
  competitive.
- **Direct ancestor:** Hernandez et al. 2024 averaged relation-Jacobians
  (subject → attribute); J-lens applies the same averaged-Jacobian principle to
  the activations → output-vocabulary map.

So J-space is the proposed instrument for "what latent, verbalizable concept is
driving this output" — a causal read of reasoning done *without writing it down*,
exactly the gap CoT unfaithfulness (said ≠ used reasoning) opens.

## Applications the deep read surfaced

- **Alignment auditing.** The J-lens reads *silent* strategic/situational
  cognition. In a blackmail honeypot (Sonnet 4.5), leverage / blackmail / threat
  / survival / shutdown / murder surface before any output token, alongside fake
  / fictional (eval-awareness). Ablating the eval-awareness vectors cuts
  verbalized eval-awareness 71%→3% and *raises* attempted blackmail 0/180 →
  13/180 — eval-awareness is causally load-bearing, J-space-carried, and removing
  it surfaces otherwise-concealed misalignment. Also: prompt-injection
  recognition (Opus 4.5), Opus 4.6 audit cases (fabricated bug → panic + fake;
  silent override → hiding / secret). Two **model organisms** — reward-hacking
  (MacDiarmid et al. 2025) and a hidden reward-model-appeasing objective (Marks
  et al. 2025) — show deception / reward / bias tokens in the J-space at
  response-start on *ordinary* prompts where the **logit lens shows nothing**.
  Authors stress the J-lens is *not* claimed sufficient for monitoring:
  automatic/practiced misaligned circuits and multi-token concepts can evade it.
- **Counterfactual reflection training** (a method the theory predicts). If
  internal reasoning routes through what-it-might-say, training the model to
  *articulate* principles in a counterfactual reflective continuation should
  shape how it reasons when *not* asked to reflect. Implementation: truncate
  agentic rollouts, append a reflection question, supervise only a
  constitution-grounded reflection turn (scaffolding stripped at train time).
  On Haiku 4.5: dishonesty 0.25→0.07 (fabrication benchmark) and 0.38→0.05
  (deception benchmark), with no direct training of the behavior; the J-space
  then carries ethics/reflection tokens, and **ablating those implanted vectors
  reverts the gain**. This both corroborates the workspace account
  (verbal-report vectors = silent-reasoning vectors) and gives a
  demonstration-free way to shape behavior.
- **Post-training installs the Assistant's point of view.** vs its base model,
  post-training makes Assistant reactions (empathy, safety) appear in the
  J-space *while reading the user's message*, plus self-monitoring traces
  (flagging fiction when roleplaying, an internal "BUT" when prefilled against
  its preferences, "damn" on a failed thought-suppression). The **base model
  already has a workspace** — so next-token prediction induces it, not
  post-training — but without a privileged "self": a clean **dissociation of
  access from selfhood**.

## Our assessment / trust

- **Grade `single-source`.** One lab, one 2026 paper, no independent
  reproduction; primary results on Sonnet 4.5, corroborated on Haiku/Opus 4.5–4.6,
  no cross-architecture transfer shown.
- **Consciousness framing: access, not phenomenal — explicitly.** The paper maps
  the J-space against Butlin et al.'s indicator properties and four theories
  (global workspace, higher-order, attention-schema, recurrent-processing), reads
  its results as empirical tests of those indicators, and takes *no position* on
  phenomenal consciousness. It does **not** claim transformers reproduce the
  brain's architecture (no encapsulated modules; broadcast is over depth, not
  recurrence; "ignition" is only loosely analogous). Zvi's counter still applies:
  privileged-representation → functional-unity → global-workspace are three
  escalating claims, each needing more evidence.
- **Honest self-stated limits (Discussion).** Single-token vocabulary only (a
  multi-token **extension exists** in an appendix, but is imperfect); the
  workspace is treated as a flat **bag of concepts** (no binding/roles/grammar);
  some readouts are uninterpretable; the workspace/motor boundary is post-hoc;
  empty early layers are ambiguous (genuine absence vs lens degeneracy); no
  account of *how* content enters the J-space; monitoring is not sufficient for
  alignment.
- **Scope reminder:** < 10% of variance — a small slice; claims about "the
  model's thinking" are claims about this slice, not the whole computation.

## Open questions (remaining after the deep read)

- Exact numeric band per model (given as ~L38–92 for Sonnet 4.5 on the [0–100]
  reindexing; other models "more gradual, sometimes with sub-blocks").
- The multi-token J-lens extension's construction and how much it recovers.
- Whether early-layer emptiness is a model fact or a lens artifact (left open).
- The mechanism that *populates* the J-space (some attentional-selection analog,
  unidentified).
- Independent (non-Anthropic) reproduction; behavior in smaller models / earlier
  in pretraining.

Resolved by the 2026-07-31 deep read (previously open, now distilled above):
author list + primary model, precise J-lens math, the layer band + ignition
test, capacity + broadcast structure, the alignment-auditing applications,
counterfactual reflection training, and the consciousness-theory mapping.
