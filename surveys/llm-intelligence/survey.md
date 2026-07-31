# Field map: LLM "intelligence" — internal representation, reasoning, and self-access

> Mechanisms and evidence bearing on what an LLM represents, computes, and can
> report internally — the capability/cognition question. "Intelligence" is a
> loaded, contested umbrella (kept in scare-quotes deliberately); this map does
> not adjudicate it, it organizes the concrete techniques and findings that
> claims about it rest on.

## Grounding and coverage

- **Grounding mode: `grounded`, in progress (partial).** The J-space anchor
  node is grounded (primary source fetched and read this session). Every other
  node is **`recall-pending`**: named from pretrained recall + one light web
  pass, *not* yet citation-verified against fetched sources. Per node grounding
  is tagged inline (`[G]` grounded / `[R]` recall-pending). Recall-pending
  effectiveness grades are capped at `single-source`/`folklore` and must not be
  read as verified.
- **Coverage cutoff: 2026-07-30.** Search scope this session: two web searches
  (`"J-space" LLM`, `J-space latent space viral`) + three fetches
  (transformer-circuits.pub J-space paper ×2, Zvi Mowshowitz commentary). No
  paper-DB citation snowball yet. This is a seed, not a survey horizon.
- **Model training cutoff:** 2026-01 — anything after that (incl. the anchor
  paper itself) is known only through this session's fetches, so treat the
  non-anchor lineage as reconstruction to be verified.
- This map was **seeded by backward traversal from one anchor** (J-space), so
  its shape is that paper's intellectual lineage, not yet the whole field. The
  broader LLM-intelligence territory (scaling/emergence, agentic capability,
  evaluation, world-models) is stubbed under *Adjacent clusters* for later
  sessions.

**Node grounding legend.** `[G]` = grounded (source fetched/read). `[R]` =
recall-pending (verify on a grounded pass; citation in `related-work/papers.yaml`
carries `verified: false`). Effectiveness grades: `reproduced` /
`externally-evaluated` / `benchmark-reported` / `single-source` / `contested` /
`failed-replication` / `folklore` (per `topics/research-survey.md`).

**Grade cap nuance.** Two kinds of `[R]` claim, treated differently: a
*post-cutoff / anchor-adjacent* claim (the J-space result and anything depending
on it) is capped at `single-source` — no independent reproduction can have been
verified. A *pre-cutoff, long-established* result (CoT gains, induction heads,
CoT unfaithfulness) keeps its real multi-source consensus grade
(`reproduced`/`contested`) but stays `[R]` = not re-verified against a fetched
source *this session*. The grounded pass confirms the citation, not the
consensus. That is why some `[R]` nodes read above `single-source`.

- **Grounded pass 2026-07-30** verified citations and flipped to `[G]`: A2
  (superposition), B3 (tuned lens), C1 (ActAdd), C2 (RepE),
  E2 (Turpin CoT-unfaithfulness), F1 (introspection precursor), and added D2
  (circuit tracing). The rest remain `[R]`.
- **Fetch+read pass 2026-07-31** built durable full-text extracts
  (`related-work/extract/<key>/`, git-ignored) for the anchor + 8 lineage papers
  and pulled the anchor's **verbatim bibliography** — 171 cited keys, filtered
  to `related-work/extract/j-space/2026/workspace/cited.bib`. The anchor's real
  citations *confirm* clusters A–F and surfaced new anchor-cited nodes now folded
  into the seed set: **cluster G (activation decoding to language)** — the
  nearest live sibling of J-lens — plus Cunningham SAEs (A3),
  transcoder/sparse-feature circuits (D2), and GWT-in-deep-learning +
  AI-consciousness assessment (F2). ActAdd (C1) title **reconciled**: the paper
  was arXiv-renamed across versions, not miscited (the 07-30 "title corrected"
  note over-corrected). Extract caveat: `elhage2022-superposition` has no arXiv
  HTML view, so it fell back to PDF+marker and hit a shared-GPU CUDA-OOM — its
  extract is PDF-only (no markdown yet); the four arXiv-HTML-view papers and the
  three transformer-circuits pages extracted cleanly.

---

## Seed set and governing instruction (what "coverage" means here)

Completeness here is **not** "all of LLM intelligence" — it is defined by this
seed set plus the traversal rule. A topic is in scope once some seed's backward
citation chain reaches it; anything no seed reaches is *out-of-scope-so-far*,
not *missing*. This is the contract a later reader (or collaborator) uses to
tell a genuine gap from an unreached branch.

- **Governing instruction** (graehl, 2026-07-30): seed from the J-space paper
  and *traverse backward* through its preconditions / inspirations /
  fundamentals (~30 min, continued across sessions); additionally fold in
  *recent* high-interest / high-utility discoveries encountered en route.
- **Seed set:**
  1. **J-space anchor** (primary) — Anthropic, "Verbalizable Representations
     Form a Global Workspace in Language Models," 2026. The origin seed;
     clusters A–F are its backward lineage.
  2. **Emergent Introspective Awareness** (Anthropic, Oct 2025) — recent
     addition; the concept-injection introspection protocol the anchor adapts
     (node F1).
  3. **Circuit Tracing / On the Biology of a Large Language Model** (Anthropic,
     2025) — recent addition; cross-layer-transcoder attribution graphs, the
     causal-interpretability sibling of J-lens (node D2).
  4. **Folded from the anchor bibliography (2026-07-31 read):** the
     activation-decoding family (SelFIE, LatentQA, Activation Oracles, Natural
     Language Autoencoders — **cluster G**), Cunningham SAEs (A3),
     transcoder/sparse-feature circuits (D2), GWT-in-deep-learning (Goyal shared
     workspace, VanRullen & Kanai) and Butlin et al. AI-consciousness indicators
     (F2). These are **anchor-cited**, so they are backward-traversal hits, not
     scope widening — recorded here as the recent high-utility discoveries the
     governing instruction invites.

Adding a seed widens declared scope; retiring the traversal to a new anchor
starts a new region. Record both here when they change.

---

## Map orientation (dependency sketch)

The anchor synthesizes four independently-developed lines. Read bottom-up:

```
                       [ANCHOR] J-space / global workspace in LMs
                    (causal lens × sparse features × verbalization × access)
                    /              |               |                \
        B. Reading state   A. Representation   E. Verbalized vs   F. Self-access /
        (lenses/probes)    geometry (linear,    latent reasoning   introspection +
              |             superposition,       (CoT & (un)faith-  GWT/access import
        C. Steering state   features/SAEs)       fulness)           from neuroscience
        (actadd, RepE)           |
              \________ D. Circuits framework (residual stream, attention) ________/
                                 |
                        Transformer substrate (Vaswani 2017)
```

Clusters A–F below, then **G** (activation→language decoders — J-lens's live
sibling, sitting beside the anchor on the "read out an activation" side), then
the anchor. "Nearest confusable" links are the decision-relevant edges — most
survey value is in *not* conflating adjacent techniques.

---

## A. Representation geometry — what a "concept" is inside the model

### A1. Linear representation hypothesis `[R]`
- **Mechanism.** High-level concepts are (often) encoded as directions in
  activation space; concept presence ≈ a linear functional of the residual
  stream. Ancestor: word2vec analogy arithmetic (Mikolov et al. 2013).
- **Nearest confusable.** *Superposition* (A2) is about capacity/packing of
  many directions into few dims; the linear hypothesis is about the *form* of a
  single concept's code. They compose but are distinct claims.
- **Prereq for:** all lens (B) and steering (C) methods, and J-space's whole
  premise that a workspace vector maps to a token disposition.
- **Falsifier / bound.** Not all features are linear: circular/multi-dim
  features (e.g. days-of-week, modular structure) reported by Engels et al.
  2024 ("Not all language model features are linear"). So the hypothesis is a
  useful default, not a law.
- **Effectiveness:** `contested` (recall-capped to `single-source` here) —
  strong for many semantic concepts; known nonlinear exceptions.
- **Design decision it changes.** Whether you can read/steer a concept with a
  single vector (cheap) or need a subspace/nonlinear probe.

### A2. Superposition `[G]`
- **Mechanism.** With sparsity, a model packs *more* features than it has
  dimensions, as an overcomplete set of near-orthogonal directions that
  interfere only rarely (Elhage et al. 2022, "Toy Models of Superposition").
- **Prereq for:** dictionary learning / SAEs (A3) and directly for J-space's
  stated framing — "activations decompose as sparse linear combinations from an
  overcomplete set of feature directions."
- **Falsifier.** In the toy setting, the phase transition to superposition is
  demonstrated as feature sparsity rises; the open question is how faithfully
  the toy picture describes frontier models.
- **Effectiveness:** `single-source` (foundational, widely adopted framing;
  frontier-scale fidelity unproven).

### A3. Dictionary learning / sparse autoencoders (SAEs) `[R]`
- **Mechanism.** Train an overcomplete SAE on activations; its sparse
  nonnegative codes are candidate monosemantic features (Bricken et al. 2023
  "Towards Monosemanticity"; Templeton et al. 2024 "Scaling Monosemanticity";
  Cunningham et al. 2023 "SAEs Find Highly Interpretable Model Directions" — the
  other foundational SAE result, anchor-cited).
- **Nearest confusable — and the key contrast with the anchor.** SAE features
  are *reconstructive / input-side*: fit to reconstruct the activation,
  unsupervised, no reference to the output. **J-lens vectors are causal /
  output-side**: ranked by first-order effect on what the model will *say*.
  Same algebra (sparse nonnegative overcomplete combination), different basis
  and different selection objective. This is the single most important "don't
  conflate these" edge in the map.
- **Effectiveness:** `contested` (capped `single-source`) — interpretable
  features extracted at scale, but whether SAE features are the *right causal
  units* (vs. probing/steering baselines) is under active dispute (2024–2025).
- **Design decision.** Choose SAE features when you want an unsupervised concept
  inventory; choose a causal lens (B/anchor) when you want "what drives the
  output here."

---

## B. Reading internal state — lenses and probes

### B1. Probing (linear classifier probes) `[R]`
- **Mechanism.** Train a supervised classifier on activations to test whether a
  property is *decodable* (Alain & Bengio 2016).
- **Falsifier / bound.** Decodability ≠ use: control tasks (Hewitt & Liang 2019)
  show high probe accuracy on random labels, so probe success alone doesn't
  prove the model *uses* the info. This is exactly the correlational gap the
  anchor's causal lens is built to close.
- **Effectiveness:** `single-source`/`folklore` — ubiquitous diagnostic;
  interpretation caveats well known.

### B2. Logit lens `[R]`
- **Mechanism.** Apply the unembedding matrix directly to an intermediate
  residual stream → a next-token distribution "as if decoding early"
  (nostalgebraist 2020).
- **Nearest confusable.** Tuned lens (B3) adds a learned per-layer map; J-lens
  (anchor) replaces the linear readout with an averaged Jacobian (causal).
- **Bound.** Brittle in early layers, representation-basis-dependent; a
  qualitative tool, not a faithful readout. The anchor explicitly frames it as
  applying the unembedding directly and being non-causal.
- **Effectiveness:** `folklore` — widely used, known-unreliable early-layer.

### B3. Tuned lens `[G]`
- **Mechanism.** Fit a per-layer affine map from the intermediate stream to the
  final logits; lower bias/variance and more predictive than logit lens
  (Belrose et al. 2023, "Eliciting Latent Predictions with the Tuned Lens").
- **Nearest confusable / anchor edge.** Still **correlational**: it predicts the
  *output*, and (per the anchor) tends to "skip ahead" to the final token rather
  than surface the *intermediate* concept in play. The anchor's J-lens is
  positioned as the causal fix that surfaces intermediates.
- **Effectiveness:** `benchmark-reported` → capped `single-source` here — the
  paper reports lower lens perplexity across model families; not re-verified.

---

## C. Steering internal state — causal control

### C1. Activation addition / steering vectors `[G]`
- **Mechanism.** Add a scaled direction to the residual stream, `h ← h + αv`,
  to push behavior toward/away from a concept — ActAdd, from a contrastive
  prompt pair (Turner et al. 2023, arXiv 2308.10248 — original title "Activation
  Addition: Steering Language Models Without Optimization", later arXiv-renamed
  "Steering Language Models With Activation Engineering"; the anchor cites the
  original title. Same paper — the 07-30 "recalled title was wrong" note
  over-corrected).
- **Anchor edge.** J-space uses *exactly this intervention form* on J-lens
  vectors to establish its five functional properties (verbal report, directed
  modulation, etc.) — steering is the anchor's causal test harness.
- **Effectiveness:** `single-source` — works cleanly for some concepts, brittle
  / off-target for others; α-tuning sensitive.

### C2. Representation engineering (RepE) `[G]`
- **Mechanism.** Top-down: derive reading/control vectors from contrastive
  prompt sets (e.g. LAT / PCA over paired activations), then read or steer
  (Zou et al. 2023).
- **Nearest confusable.** ActAdd (C1) hand-picks a direction from a prompt pair;
  RepE systematizes extraction across a stimulus set. SAE (A3) extracts
  unsupervised; RepE extracts supervised-by-contrast.
- **Effectiveness:** `single-source` — demonstrated control of honesty,
  harmfulness, emotion axes; generality contested.

---

## D. Circuits framework (substrate for A–C)

### D1. Mathematical framework for transformer circuits `[R]`
- **Mechanism.** Residual stream as a shared linear communication channel that
  heads read from / write to; attention factored into QK (where) and OV (what);
  induction heads (Elhage et al. 2021; Olah et al. 2020 "Zoom In").
- **Why it's load-bearing here.** The "residual stream is a sum of directions
  you can lens/steer" picture that A–C and the anchor all assume *is* this
  framework. J-space's layer geometry (sensory/middle/motor) is a claim about
  where in this stream verbalizable content lives.
- **Effectiveness:** `single-source`/`reproduced` for induction heads
  specifically (widely replicated); framework is a lens, not a benchmarked
  result.

### D2. Circuit tracing / attribution graphs `[G]`
- **Mechanism.** Cross-layer transcoders (CLTs) replace MLP activations with
  sparse interpretable features; **attribution graphs** then trace the causal
  input→intermediate→output pathway for a specific prompt (Anthropic 2025,
  "Circuit Tracing" + "On the Biology of a Large Language Model," on Claude 3.5
  Haiku).
- **Nearest confusable / anchor edge.** Both attribution graphs and J-lens are
  *causal* interpretability from the same lab: attribution graphs map the
  *pathway between features*; J-lens ranks a single activation's *output-token
  disposition*. CLT features (A3-style sparse) are the graph's nodes — so this
  is where the SAE lineage (A3) and the circuits substrate (D1) fuse into a
  causal tracer, the immediate methodological context J-space sits in.
- **Lineage (anchor-cited, folded 2026-07-31).** The CLT tracer descends from
  **transcoders as circuit units** (Dunefsky et al. 2024/25, "Transcoders find
  interpretable LLM feature circuits") and **sparse *feature* circuits** — causal
  graphs over SAE features (Marks et al. 2024). Transcoder → CLT → attribution
  graph is the methodological staircase into D2.
- **Effectiveness:** `single-source` — Anthropic 2025; interpretable causal
  graphs demonstrated on a production model, not independently reproduced.
- **Design decision.** Attribution graphs for "trace the whole circuit behind
  this output"; J-space for "what latent, verbalizable concept is active here."

---

## E. Verbalized vs latent reasoning

### E1. Chain-of-thought (CoT) `[R]`
- **Mechanism.** Eliciting step-by-step verbalized reasoning raises multi-step
  task accuracy at sufficient scale (Wei et al. 2022); scratchpad precursor
  (Nye et al. 2021).
- **Anchor edge.** CoT/scratchpad is *written* reasoning — in J-space terms,
  content pushed to the "motor"/output side. The anchor's whole point is a
  **latent** workspace that reasons without writing the token down.
- **Effectiveness:** `reproduced` — CoT gains widely reproduced on
  arithmetic/symbolic/multi-hop, **conditioned on scale** (small models gain
  little/none) and benchmark.

### E2. CoT (un)faithfulness `[G]` (Turpin grounded; Lanham `[R]`)
- **Mechanism / finding.** The verbalized CoT is not reliably the *cause* of the
  answer: models rationalize post-hoc and are steerable by biasing features they
  don't mention (Turpin et al. 2023, "LMs Don't Always Say What They Think";
  Lanham et al. 2023, "Measuring Faithfulness in CoT").
- **Why it motivates the anchor.** If said-reasoning ≠ used-reasoning, you need
  a way to read the *used* (latent) reasoning — which is what a causal workspace
  lens claims to provide.
- **Effectiveness:** `reproduced`/`contested` — unfaithfulness demonstrated
  across several setups; magnitude/prevalence debated.

---

## F. Self-access: introspection + the neuroscience import

### F1. LLM introspection / self-report `[G]` (precursor grounded; Binder/Kadavath `[R]`)
- **Mechanism.** Whether a model can report facts about its own internal states
  better than an external predictor can (Binder et al. 2024, "Looking Inward";
  calibration precursor Kadavath et al. 2022, "LMs (Mostly) Know What They
  Know"). The direct methodological precursor to the anchor's protocol is
  Anthropic's **"Emergent Introspective Awareness in Language Models"** (Oct
  2025): inject a known concept's representation into activations, then measure
  its effect on the model's self-report — the same concept-injection design the
  anchor's "verbal report" property uses.
- **Anchor edge.** J-space's "verbal report" property is an introspection claim
  with a *mechanism* attached (the reported content = the workspace vector).
- **The live debate (anchor-cited, folded 2026-07-31).** Positive pole: Ji-An et
  al. 2025 (LMs show metacognitive monitoring/control of their own activations)
  and Song et al. 2025 (what *privileged self-access* would have to mean).
  Negative pole: Comșa & Shanahan 2025 ("Does it make sense to speak of
  introspection in LLMs?"). J-space enters this debate on the positive side but
  with a causal handle the behavioral studies lack.
- **Effectiveness:** `single-source`/`contested` — some genuine self-access,
  but limited, unreliable, and easy to overread.

### F2. Global workspace theory (GWT) + access vs phenomenal consciousness `[R]`
- **Import, not an LLM result.** GWT (Baars 1988; Dehaene, Kerszberg & Changeux
  1998 neuronal global workspace; Dehaene & Naccache 2001): a limited-capacity
  workspace broadcasts selected content to many consumers = conscious *access*.
  Block 1995 distinguishes **access** (functional, reportable) from
  **phenomenal** (subjective experience) consciousness.
- **How the anchor uses it.** As a *functional* template (broadcast, limited
  capacity, reportability, selectivity) to test against LM internals — explicitly
  **access, not phenomenal**, and explicitly *not* a claim that transformers
  reproduce the brain's architecture (no encapsulated modules, no recurrence, no
  sharp ignition).
- **ML instantiations (anchor-cited, folded 2026-07-31).** GWT is not only an
  import: Goyal et al. 2022 ("Coordination Among Neural Modules Through a Shared
  Global Workspace") builds a limited-capacity shared-workspace *architecture*,
  and VanRullen & Kanai 2021 ("Deep Learning and the Global Workspace Theory")
  proposes it as an organizing principle for multi-modal nets. Butlin, Long,
  Chalmers et al. 2023 ("Consciousness in AI") turn GWT + rivals into an
  **indicator-property checklist** for assessing AI systems — the disciplined
  version of the question the anchor's coverage sensationalizes.
- **Effectiveness:** N/A (external theory). The load-bearing move is keeping
  access/phenomenal separate; the viral coverage collapses them.

---

## G. Activation decoding to natural language (J-lens's live siblings)

Methods that decode an activation **into language** — the nearest live
alternative to J-space, which decodes an activation into a ranked **token
disposition**. All anchor-cited; folded in on the 2026-07-31 read (no full-text
extracts yet — grounded pass queued).

### G1. Activation→language explainers `[R]`
- **Mechanism.** Feed an internal activation (back) to an LLM and have it emit a
  natural-language description of what that activation encodes. Variants: **SelFIE**
  (Chen et al. 2024, self-interpretation of embeddings); **LatentQA** (Pan et al.
  2024, a decoder trained to answer NL questions about activations); **Activation
  Oracles** (Karvonen et al. 2025, general-purpose activation explainers);
  **Natural Language Autoencoders** (Fraser-Taliente et al. 2026, *unsupervised*
  NL explanations — co-authored by J-space author Kantamneni).
- **Nearest confusable / anchor edge.** These produce **free text** — expressive
  but unvalidated, prone to plausible confabulation. **J-lens** produces a ranked
  vocabulary disposition with a first-order **causal** guarantee
  (∂output/∂activation). The trade is expressivity vs. causal faithfulness;
  J-space is the causal pole of exactly this family, which is why it belongs
  beside them rather than under B (correlational lenses).
- **Effectiveness:** `single-source` each — recent, largely un-reproduced across
  labs; whether free-text explainers are *faithful* (vs. fluent) is the open
  question the causal lens is meant to answer.

---

## ANCHOR. J-space / verbalizable global workspace in language models `[G]`

**Source (grounded).** "Verbalizable Representations Form a Global Workspace in
Language Models," Anthropic / transformer-circuits.pub, July 2026. Popularly
"J-space." Fetched and read this session. **Concept page:**
[`concepts/j-space.md`](concepts/j-space.md) (short handle `j-space`).

- **J-lens (the "J").** For layer ℓ, the averaged Jacobian
  `J_ℓ = E[∂h_final,t' / ∂h_ℓ,t]` over token positions and ~1,000 prompts:
  the *first-order causal effect* of an activation on the final output. Applied
  to an activation it yields a ranked list of vocabulary tokens that activation
  is "disposed to make the model say." **Contrast the whole B-cluster:** logit
  lens = raw unembedding (correlational readout); tuned lens = learned affine
  (correlational, skips to output); J-lens = causal sensitivity that surfaces
  *intermediate* dispositions.
- **J-space (the object).** Points expressible as **sparse nonnegative
  combinations of J-lens vectors** (same algebra as A3 SAEs, different basis:
  output-disposition not reconstruction). Empirically: ~10–25 vectors
  meaningfully active per position; overcomplete (n_vocab ≫ d_model); accounts
  for **<10% of activation variance**; concentrated in **middle layers**
  (~38–92 in the large model), flanked by "sensory" (early) and "motor" (late)
  regions.
- **Five functional properties** (the "it behaves like a global workspace"
  case): (1) verbal report — swapping J-lens vectors causally changes what the
  model says; (2) directed modulation — the model can deliberately activate
  workspace vectors on instruction; (3) internal reasoning — intermediate steps
  ("spider"→"8 legs") appear as J-lens vectors before being said; (4) flexible
  generalization — the same vector works across functions; (5) selectivity —
  mediates flexible reasoning but not automatic processing (e.g. text parsing).
- **Prerequisites (this map's edges):** A1/A2 (linear + superposition premise),
  A3 (sparse-overcomplete algebra), C1 (steering as the causal test), B2/B3
  (the lenses it improves on), E2 (unfaithful CoT — why a latent causal read is
  needed), F1/F2 (introspection protocol + GWT template).
- **Falsifier / self-stated limits (from the source).** J-lens sees only
  **single-token** concepts (misses multi-token phrases); Jacobian averaging
  over 1,000 prompts may smear context-specific content; "empty" early layers
  may be lens degeneracy, not genuine absence; results concentrate on Anthropic
  models (Opus/Sonnet/Haiku) and vary with scale. Authors call J-lens "an
  imperfect tool [that] only approximately and incompletely captures the
  model's underlying workspace structure."
- **Regime.** Frontier Anthropic decoder-only transformers; middle layers;
  flexible-reasoning tasks. Not shown to transfer across architectures.
- **Effectiveness:** `single-source` — one lab, one paper, not independently
  reproduced. The *mechanism* (causal lens surfacing latent, reportable
  reasoning units) is the signal; the *consciousness reading* is coverage hype
  the authors disclaim ("we take no position").
- **Design decision it changes.** If you want "what latent concept is actually
  driving this output, in a form the model could verbalize," J-space is the
  proposed instrument — over a correlational lens or an unsupervised SAE.

---

## Contested results

- **Are SAE features the right causal units?** (A3) 2024–2025 dispute: SAE
  features are interpretable but may not beat probing/steering baselines on
  causal tasks. The anchor sidesteps by defining its basis *causally*, which is
  itself a stance in this dispute.
- **Linear representation hypothesis** (A1): strong default vs. documented
  nonlinear/multi-dim features. Bears directly on whether a single J-lens vector
  can stand for a concept.
- **CoT faithfulness prevalence** (E2): demonstrated, but how often and how
  badly CoT misleads is unsettled.
- **Consciousness framing of the anchor:** authors say access-only, no position
  on phenomenal; secondary coverage ("Is Claude conscious?") over-claims. Zvi
  Mowshowitz: real mechanistic advance, but "privileged representation →
  functional unity → global workspace" are three escalating claims, each needing
  more evidence.

## Negative / quiet results

- **Probing decodability ≠ use** (B1, Hewitt & Liang control tasks) — a
  standing correction to "the model represents X because a probe finds X."
- **Logit lens early-layer unreliability** (B2) — quietly superseded by tuned
  lens for quantitative use.
- *(Recall-pending: a grounded pass should look for SAE negative results and any
  failed steering-generalization reports to populate this section properly.)*

## Baseline sensitivity

- **CoT gains** (E1) shrink toward zero at small scale and on non-multi-step
  benchmarks — the "CoT helps" claim is scale- and task-conditioned.
- **Steering/RepE** (C) effects are α- and layer-sensitive; a fair baseline is
  prompt-only control, against which some steering wins narrow.
- **Anchor:** the "<10% of variance" figure is a reminder that the workspace is
  a *small* slice — most activation energy is outside J-space, so claims about
  "the model's thinking" are claims about this slice, not the whole computation.

---

## Adjacent clusters (stubs for future sessions)

Not on the J-space backward path but part of the broader "LLM intelligence"
field; seed when traversal reaches them:

- **Scaling & emergence** — scaling laws (Kaplan 2020; Hoffmann/Chinchilla
  2022); emergent abilities (Wei 2022) vs. "mirage" critique (Schaeffer 2023,
  metric-discontinuity). `contested`.
- **World models / latent structure** — Othello-GPT board-state probes
  (Li et al. 2023) and the linear-world-model follow-ups.
- **Agentic capability & evaluation** — tool use, planning, and the
  benchmark-validity problem.
- **Knowledge & factual recall** — ROME/MEMIT locate-and-edit; where facts live.

---

## Backward-traversal frontier (grounding queue)

Full-text extracts now exist (2026-07-31, `related-work/extract/<key>/`) for the
anchor + tuned lens, ActAdd, RepE, Turpin, superposition (PDF-only — marker
OOM'd), and the three 2025 transformer-circuits seeds. The anchor's **verbatim
bibliography is extracted** (171 keys → `cited.bib`), so the manifest no longer
relies on recalled reference lists, and its citations were used to fold in
cluster G + the A3/D2/F1/F2 nodes above. Remaining, ordered by leverage:

1. **Cluster G (activation→language decoders)** — SelFIE / LatentQA / Activation
   Oracles / NL-Autoencoders. Newest, closest live sibling of J-lens; no extracts
   yet. Highest-value grounded pass next; then write the `activation-decoding`
   concept page.
2. Read the **anchor extract** in depth for the five-property experiment tables
   and exact per-model layer ranges (sensory/middle/motor boundaries) — the
   `j-space` concept page's remaining open questions.
3. Bricken 2023 / Templeton 2024 / Cunningham 2023 (SAEs) — pin the
   sparse-nonneg-overcomplete lineage + input-vs-output-basis contrast; write the
   `sae` concept page.
4. Lanham 2023 (CoT faithfulness) — second faithfulness anchor.
5. Elhage 2021 (circuits math framework); **re-extract elhage2022** via the
   transformer-circuits HTML (marker OOM'd on the PDF, so it is PDF-only).
6. Park 2023 + Engels 2024 (linear rep hypothesis + nonlinear falsifier).
7. Binder 2024 + Kadavath 2022 + the F1 introspection-debate trio
   (Ji-An / Song / Comșa).
8. Baars / Dehaene / Block + the GWT-in-ML nodes (Goyal, VanRullen) — confirm
   exact citations. Also confirm the `anthropic2025-introspection` arXiv mirror
   (2601.01828).

See `related-work/papers.yaml` for the metadata manifest (verification status
per paper) and `related-work/fetch.sh` for the regenerable extraction script.
Extracts are git-ignored; rebuild with `./fetch.sh` (arXiv HTML view preferred,
marker PDF fallback needs a free GPU).
