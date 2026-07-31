# Field map: LLM "intelligence" — internal representation, reasoning, and self-access

> Mechanisms and evidence bearing on what an LLM represents, computes, and can
> report internally — the capability/cognition question. "Intelligence" is a
> loaded, contested umbrella (kept in scare-quotes deliberately); this map does
> not adjudicate it, it organizes the concrete techniques and findings that
> claims about it rest on.

## Read-backed digests — the analyzed lineage

Papers **read in full** this session and distilled to `concepts/<short>.md`
pages (each links its git-ignored extract + clickable full-text sources).
Rows 1–12 are the backward lineage, foundations → anchor — this *is* the J-space
backstory; row 13 is the anchor's applied downstream (the model organisms it
audits):

| # | digest | one-line | cluster |
|---|--------|----------|---------|
| 1 | [superposition](concepts/superposition.md) | more features than dimensions → an overcomplete feature frame | A2 |
| 2 | [sae](concepts/sae.md) | sparse dictionary learning un-mixes that frame (input-side) | A3 |
| 3 | [logit-lens](concepts/logit-lens.md) | decode a hidden state with the unembedding (`J=I`) | B2 |
| 4 | [tuned-lens](concepts/tuned-lens.md) | a *trained* per-layer lens; correlational, "skips ahead" | B3 |
| 5 | [relation-jacobian](concepts/relation-jacobian.md) | averaged Jacobians as linear maps — **J-lens's ancestor** | B4 |
| 6 | [actadd](concepts/actadd.md) | activation-addition steering — J-space's "write" primitive | C1 |
| 7 | [repe](concepts/repe.md) | representation engineering — read/steer from contrasts | C2 |
| 8 | [cot-unfaithfulness](concepts/cot-unfaithfulness.md) | said ≠ used reasoning → why a latent causal read is needed | E2 |
| 9 | [introspection](concepts/introspection.md) | concept-injection self-report tests — the verbal-report precursor | F1 |
| 10 | [attribution-graphs](concepts/attribution-graphs.md) | circuit tracing via cross-layer transcoders — causal sibling | D2 |
| 11 | [activation-decoding](concepts/activation-decoding.md) | read activations into language — **J-lens's live sibling** | G1 |
| 12 | [**j-space**](concepts/j-space.md) | **the anchor** — verbalizable global workspace + auditing | ANCHOR |
| 13 | [alignment-auditing](concepts/alignment-auditing.md) | the model organisms the J-lens audits (blackmail honeypot, reward-hacking + hidden-objective) | H1 |
| 14 | [knowledge-vs-verbalization](concepts/knowledge-vs-verbalization.md) | the same split found independently, by probing — **corroborates the anchor** | I1 |
| 15 | [pre-verbalization-commitment](concepts/pre-verbalization-commitment.md) | how far ahead the answer is fixed: 17–31 token lead — the temporal axis | I1 |

A `[G]` node with a linked digest is **read-backed**; a `[G]` node without one is
fetched + citation-checked but not yet read (see the legend).

## Grounding and coverage

- **Grounding mode: `grounded`, in progress (partial).** State as of the
  cutoff below, counted from `related-work/papers.yaml` and `concepts/` rather
  than narrated per session — update these numbers when either changes:
  **64 papers manifested, 52 citation-verified, 24 with a fetched extract, 15
  read in full and digested.** `./related-work/fetch.sh --audit` checks those
  first three against disk. Per-node grounding is tagged inline (`[G]`
  citation-grounded / `[R]` recall-pending); a full read is marked by a linked
  `concepts/` digest. Recall-pending effectiveness grades are capped at
  `single-source`/`folklore` and must not be read as verified.
- **Coverage cutoff: 2026-07-31.** The anchor's verbatim bibliography (178
  entries) has been fetched and diffed against the manifest, so backward
  traversal is now measurable rather than estimated. Still open: roughly 40
  anchor-cited works remain unmanifested (mostly benchmarks, datasets, and
  consciousness-science background — see the grounding queue for the
  substantive residue), and no forward citation search has been run.
- **Model training cutoff:** 2026-01 — anything after that (incl. the anchor
  paper itself) is known only through this session's fetches, so treat the
  non-anchor lineage as reconstruction to be verified.
- This map was **seeded by backward traversal from one anchor** (J-space), so
  its shape is that paper's intellectual lineage, not yet the whole field. The
  broader LLM-intelligence territory (scaling/emergence, agentic capability,
  evaluation, world-models) is stubbed under *Adjacent clusters* for later
  sessions.

**Node grounding legend.** `[G]` = grounded: the citation is verified against a
fetched source (title/abstract/bibliography, or a built extract), **not
necessarily read in full**. A node backed by an actual *full read* additionally
has a **concept page** (`concepts/<short>.md`); 15 nodes do, listed in the
read-backed digest index below. So `[G]` + no concept page = "fetched and
citation-checked, read pending." `[R]` = recall-pending (pretrained recall
only; `papers.yaml` carries `verified: false`). Effectiveness grades:
`reproduced` / `externally-evaluated` / `benchmark-reported` / `single-source` /
`contested` / `failed-replication` / `folklore` (defined in `field-map.md`,
which owns this vocabulary).

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
  to `related-work/extract/anthropic2026-jspace/2026/workspace/cited.bib`. The anchor's real
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
- **Anchor deep-read 2026-07-31.** Read the full anchor extract and rewrote
  `concepts/j-space.md` (the only full-read-backed node): precise J-lens math
  (`lens = softmax(W_U·norm(J_ℓ h))`, logit lens = the `J=I` case), the
  sensory/workspace/motor layer band (~L38–92, [0–100] reindex) + the ignition
  test, capacity + broadcast-hub structure, and two dimensions the map had
  missed — **alignment auditing** (new cluster H) and **counterfactual reflection
  training**. Authors/model pinned: 16 authors (Gurnee & Sofroniew core, Lindsey
  corresponding), primary model Sonnet 4.5, published 2026-07-06. Followed
  promising anchor cites as new seeds: Hernandez relation-Jacobians (B4, the
  method's ancestor), the model-organism/auditing line (H1), Bogdan–Lindsey
  entity slots (B5), and two latent-computation precursors (E3).
- **Traversal-completion + sibling pass 2026-07-31.** Diffed the anchor's
  `cited.bib` (178 entries) against `papers.yaml` mechanically instead of by
  eye — **57 cited works were absent**, i.e. the declared backward-traversal
  method had not actually been run to completion. Folded in the 14 substantive
  ones with metadata transcribed from the anchor's own bib (`source:
  anchor-bib`, so `verified: true` without a separate fetch): **Patchscopes**
  (the framework that already unifies cluster G; an author of it is on the
  anchor's byline), **Future Lens** and **Backward Lens** (B6 — the nearest
  lens-family siblings, gradients-into-vocabulary vs Jacobian-into-vocabulary),
  Arditi refusal-direction / ITI / task vectors (C3), induction heads and
  Geva factual recall (D1), **Chanin SAE feature absorption** (A3 — the SAE
  negative result this map's own queue had asked for), self-interpretability /
  SAD / Assistant Axis (F1), and Miller 1956 + Cowan 2001 (F3), the
  working-memory baseline the anchor's ~25-item capacity claim argues against
  and which the map had recorded a number without.
  Separately, a forward search found work the anchor does *not* cite and cannot
  have: **new cluster I**, read-backed digests written from fetched full text.

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
- **Falsifier / bound.** Not all features are *one-dimensional*: circular /
  multi-dimensional features (e.g. days-of-week, modular structure) reported by
  Engels et al. 2024, "Not All Language Model Features Are One-Dimensionally
  Linear" [G]. The title matters — the paper falsifies one-dimensionality, not
  linearity, so a multi-dim linear subspace still satisfies the weaker
  hypothesis. A useful default, not a law.
- **Effectiveness:** `contested` (recall-capped to `single-source` here) —
  strong for many semantic concepts; known nonlinear exceptions.
- **Design decision it changes.** Whether you can read/steer a concept with a
  single vector (cheap) or need a subspace/nonlinear probe.

### A2. Superposition `[G]` · digest: [superposition](concepts/superposition.md)
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

### A3. Dictionary learning / sparse autoencoders (SAEs) `[G]` · digest: [sae](concepts/sae.md)
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

### B2. Logit lens `[G]` · digest: [logit-lens](concepts/logit-lens.md)
- **Mechanism.** Apply the unembedding matrix directly to an intermediate
  residual stream → a next-token distribution "as if decoding early"
  (nostalgebraist 2020).
- **Nearest confusable.** Tuned lens (B3) adds a learned per-layer map; J-lens
  (anchor) replaces the linear readout with an averaged Jacobian (causal).
- **Bound.** Brittle in early layers, representation-basis-dependent; a
  qualitative tool, not a faithful readout. The anchor explicitly frames it as
  applying the unembedding directly and being non-causal.
- **Effectiveness:** `folklore` — widely used, known-unreliable early-layer.

### B3. Tuned lens `[G]` · digest: [tuned-lens](concepts/tuned-lens.md)
- **Mechanism.** Fit a per-layer affine map from the intermediate stream to the
  final logits; lower bias/variance and more predictive than logit lens
  (Belrose et al. 2023, "Eliciting Latent Predictions with the Tuned Lens").
- **Nearest confusable / anchor edge.** Still **correlational**: it predicts the
  *output*, and (per the anchor) tends to "skip ahead" to the final token rather
  than surface the *intermediate* concept in play. The anchor's J-lens is
  positioned as the causal fix that surfaces intermediates.
- **Effectiveness:** `benchmark-reported` → capped `single-source` here — the
  paper reports lower lens perplexity across model families; not re-verified.

### B4. Averaged relation-Jacobian `[G]` (J-lens's methodological ancestor) · digest: [relation-jacobian](concepts/relation-jacobian.md)
- **Mechanism.** A transformer's map from a subject representation to a relational
  attribute (e.g. "plays instrument": Miles Davis → trumpet) is well-approximated
  by the **mean Jacobian** of the attribute w.r.t. the subject over a handful of
  examples (Hernandez et al. 2024, "Linearity of Relation Decoding").
- **Anchor edge.** This *is* the J-lens construction principle, applied to a
  different map: J-lens averages the Jacobian of the **output vocabulary** w.r.t.
  **internal activations**. The anchor names it as its closest precedent, and
  stresses that using a *mean Jacobian* rather than a *trained predictor* (as the
  tuned lens does) is empirically important to its results.
- **Effectiveness:** `single-source` (followed as a new seed 2026-07-31; not yet
  read in full).

### B5. Representation accessibility / entity slots `[R]`
- **Mechanism.** The same information (an entity's name/traits) is held in
  different **"slots"** depending on whether the entity is currently being
  discussed vs. appeared earlier; only the *current-entity* slot is accessible
  when the model is asked explicit questions about it (Bogdan & Lindsey 2026,
  "Slot Machines").
- **Anchor edge.** Directly parallels the anchor's in/out-of-J-space distinction:
  information is reportable only in the accessible format. Co-author Lindsey is
  the anchor's corresponding author.
- **Effectiveness:** `single-source` (new seed 2026-07-31; not yet read).

---

## C. Steering internal state — causal control

### C1. Activation addition / steering vectors `[G]` · digest: [actadd](concepts/actadd.md)
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

### C2. Representation engineering (RepE) `[G]` · digest: [repe](concepts/repe.md)
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

### D2. Circuit tracing / attribution graphs `[G]` · digest: [attribution-graphs](concepts/attribution-graphs.md)
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

### E2. CoT (un)faithfulness `[G]` (Turpin grounded; Lanham `[R]`) · digest: [cot-unfaithfulness](concepts/cot-unfaithfulness.md)
- **Mechanism / finding.** The verbalized CoT is not reliably the *cause* of the
  answer: models rationalize post-hoc and are steerable by biasing features they
  don't mention (Turpin et al. 2023, "LMs Don't Always Say What They Think";
  Lanham et al. 2023, "Measuring Faithfulness in CoT").
- **Why it motivates the anchor.** If said-reasoning ≠ used-reasoning, you need
  a way to read the *used* (latent) reasoning — which is what a causal workspace
  lens claims to provide.
- **Effectiveness:** `reproduced`/`contested` — unfaithfulness demonstrated
  across several setups; magnitude/prevalence debated.

### E3. Latent (unverbalized) computation — precursors `[R]`
- **Mechanism.** Evidence that models compute latently before (or without)
  verbalizing: an English-aligned intermediate decoded from non-English text
  (Wendler et al. 2024, "Do Llamas Work in English?"), and latent multi-hop
  reasoning performed but not written out (Yang et al. 2024).
- **Anchor edge.** These are exactly the phenomena the anchor's *internal
  reasoning* property demonstrates **causally** — J-lens surfaces the latent
  intermediate and intervening on it redirects the answer. The anchor cites both
  as partial prior observations of workspace-like structure.
- **Effectiveness:** `single-source`/`benchmark-reported` (new seeds 2026-07-31;
  not yet read).

---

## F. Self-access: introspection + the neuroscience import

### F1. LLM introspection / self-report `[G]` (precursor grounded; Binder/Kadavath `[R]`) · digest: [introspection](concepts/introspection.md)
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

### G1. Activation→language explainers `[G]` · digest: [activation-decoding](concepts/activation-decoding.md)
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

## H. Alignment auditing & model organisms (the J-lens's applied dimension)

Surfaced by the 2026-07-31 deep read — a whole use-case the earlier map lacked.
Because flexible strategic/situational cognition routes through the J-space, the
J-lens doubles as an alignment-monitoring instrument. All nodes anchor-cited;
not yet read in full.

### H1. Reading concealed cognition + trained-in misalignment `[G]` · digest: [alignment-auditing](concepts/alignment-auditing.md)
- **Findings.** On a **blackmail honeypot** (Lynch et al. 2025, "Agentic
  Misalignment"), the J-lens surfaces leverage / threat / survival / murder and
  eval-awareness (fake / fictional) *before any output*; ablating the
  eval-awareness vectors cuts verbalized eval-awareness 71%→3% and **raises**
  attempted blackmail 0/180 → 13/180 (removing concealment surfaces the
  misalignment). Two **model organisms** — reward-hacking (MacDiarmid et al.
  2025) and a hidden reward-model-appeasing objective (Marks et al. 2025,
  "Auditing LMs for Hidden Objectives") — leave deception / reward / bias tokens
  in the J-space at response-start on *ordinary* prompts where the **logit lens
  shows nothing**.
- **Anchor edge / caveat.** The applied payoff of selectivity (F): flexible
  strategic cognition is readable, but the authors stress monitoring is **not
  sufficient** — automatic/well-practiced misaligned circuits and multi-token
  concepts can evade it.
- **Effectiveness:** `single-source` — one lab; demonstrations on specific
  scenarios/organisms, not a benchmarked detector.
- **Design decision.** J-lens as a cheap (one matmul/layer), training-free,
  human-readable screen to *flag* transcripts — composed with SAEs/graphs, not a
  standalone guarantee.

---

## I. Independent concurrent convergence (the anchor's uncited siblings)

Every other cluster is *ancestry* — reached by backward traversal from the
anchor's bibliography, so every node is something the anchor read. This cluster
is the opposite relation and the only one of its kind here: work published too
close to the anchor for either to cite the other, arriving at the same
structural claim by a different route.

It matters disproportionately for grading. The anchor's own results are capped
at `single-source` because no independent reproduction *could* have been
verified; these are the first external evidence that the verbalizable/latent
split is not an artifact of one lab's method. They are not a replication — the
methods and domains differ — so the cap stays for now, but a deliberate
cross-check (below) could lift it.

### I1. Knowledge vs verbalization as separable directions `[G]` · digests: [knowledge-vs-verbalization](concepts/knowledge-vs-verbalization.md), [pre-verbalization-commitment](concepts/pre-verbalization-commitment.md)

- **Xiros, Zoumpoulidi & Paraskevopoulos 2026** (arXiv 2607.05013, submitted
  **the anchor's own publication date**): knowledge and verbalization are
  distinct, linearly decodable directions; **verbalization is the easier of the
  two to decode**; fabrication is a *verbalization* shift over intact
  knowledge; gated joint steering beats steering either direction alone.
  Ordinary probing + steering on math solvability in open models — no Jacobian,
  no frontier model, same split.
- **Zhang, Chen, Wei & Qin 2026** (arXiv 2605.06723, two months earlier):
  answer preference stabilizes **17–31 tokens before the answer is parseable**
  (Qwen3-4B-Instruct, binary delayed-verdict templates), measured by projecting
  continuation probabilities onto a finite answer set rather than by a probe.
  Carries its own negative result: steering δ shows local sensitivity but not
  reliable generation control.
- **Effectiveness:** `single-source` each. Both are small-scale relative to the
  anchor (open/small models, narrow task families), so they corroborate the
  *structure* of the claim, not its magnitude.
- **The cheapest discriminating check this map affords.** The anchor says
  J-space carries what is poised to be verbalized; Zhang gives a number for how
  far ahead preference is fixed. If both are describing one phenomenon, J-space
  occupancy should settle on roughly that lead. Neither paper tests it, and
  nothing else in this survey offers an equally concrete cross-validation.

---

## ANCHOR. J-space / verbalizable global workspace in language models `[G]`

**Source (grounded, full read).** "Verbalizable Representations Form a Global
Workspace in Language Models," Anthropic / transformer-circuits.pub, **published
2026-07-06**. 16 authors (Wes Gurnee & Nicholas Sofroniew core; Jack Lindsey
corresponding). Primary model **Claude Sonnet 4.5** (corroborated on Haiku 4.5,
Opus 4.5/4.6). Popularly "J-space." Full extract read this session. **Concept
page (the full distillation):** [`concepts/j-space.md`](concepts/j-space.md)
(short handle `j-space`) — the node below is the compact map view.

- **J-lens (the "J").** For layer ℓ, the averaged Jacobian
  `J_ℓ = E[∂h_final,t' / ∂h_ℓ,t]` over token positions and ~1,000 prompts:
  the *first-order causal effect* of an activation on the final output. Applied
  to an activation it yields a ranked list of vocabulary tokens that activation
  is "disposed to make the model say." **Contrast the whole B-cluster:** logit
  lens = raw unembedding (correlational readout); tuned lens = learned affine
  (correlational, skips to output); J-lens = causal sensitivity that surfaces
  *intermediate* dispositions.
- **J-space (the object).** Points expressible as **sparse nonnegative
  combinations of ≤25 J-lens vectors** (k = sparsity level; same algebra as A3
  SAEs, different basis: output-disposition not reconstruction). Overcomplete
  (n_vocab ≫ d_model); the J-space component accounts for **<10% of activation
  variance**; workspace-like only in a **middle band ~L38–92** (layers reindexed
  to [0–100]; Sonnet 4.5), flanked by **sensory** (early) and **motor** (late)
  regions.
- **Five functional properties** (the "it behaves like a global workspace"
  case): (1) verbal report — swapping J-lens vectors causally changes what the
  model says; (2) directed modulation — the model can deliberately activate
  workspace vectors on instruction; (3) internal reasoning — intermediate steps
  ("spider"→"8 legs") appear as J-lens vectors before being said; (4) flexible
  generalization — the same vector works across functions; (5) selectivity —
  mediates flexible reasoning but not automatic processing (e.g. text parsing).
- **Three structural signatures** (J-space as an object, not just via behavior):
  the **layer band** above (four lens metrics + CKA agree; an *ignition* test
  shows sharp interpretation-switching from ~L38 on ambiguous inputs, evidence
  the onset is real); **limited capacity** (~25 occupancy; ~6 *unrelated* items
  held, whole-category loading for *related* ones, eviction on category switch);
  **broadcast hub** (MLPs amplify J-lens directions ~10×; a top-1% set of
  "broadcast heads" relay them — ablating those heads hits J-space *contents*,
  recall@25 0.86→0.67, not the output, 5% vs 2%).
- **Applications (deep-read 2026-07-31).** *Alignment auditing* → cluster H
  (reads concealed strategy/eval-awareness and trained-in misalignment).
  *Counterfactual reflection training*: train the model to **articulate**
  principles in a counterfactual reflection turn, and those concepts populate the
  J-space in the un-prompted context — honesty gains on Haiku 4.5 (0.25→0.07,
  0.38→0.05), reverted by ablating the implanted vectors. Detail in the concept
  page.
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

**15 papers are read in full** and distilled to `concepts/` digests — the
*Read-backed digests* index at the top is the authoritative list; do not
restate it here. The anchor's bibliography (178 entries → `cited.bib`) is
extracted and has been diffed against `papers.yaml`. Remaining, ordered by
leverage (a `[G]`-no-digest node = fetched + citation-checked, read pending):

0. **Newly manifested, none read** (2026-07-31 traversal completion):
   Patchscopes is the highest-leverage of these — it claims to *unify* cluster
   G, so reading it may restructure that cluster rather than add to it.
   Then Backward/Future Lens (B6), Chanin absorption (A3, the SAE
   falsifier), Arditi refusal (C3, likely above `single-source` once read).

1. **SAE deepening** — the `sae` digest is read-backed on Bricken (+ Templeton
   skim); read **Cunningham 2023** and **Templeton 2024** in full to complete it.
   Templeton's extract is built; Cunningham's is a bare `source.pdf` whose
   marker run never completed, so it needs a re-run before it can be read.
3. **Activation-decoding deepening** — the digest is read-backed on SelFIE +
   LatentQA; **Activation Oracles** (Karvonen) and **NL-Autoencoders**
   (Fraser-Taliente) are summarized from the anchor bib, not yet read.
4. A1 geometry: **Park 2023 + Engels 2024** (linear rep hypothesis + its
   falsifier) — the one unread foundational cluster; **word2vec** ancestor.
   All three extracts are now built, so this is a read, not a fetch. The
   fetch already corrected Engels' title to "Not All Language Model Features
   Are **One-Dimensionally** Linear": it falsifies one-dimensionality, not
   linearity, which is a weaker claim against A1 than the map assumed.
5. Lanham 2023 (second CoT-faithfulness anchor); **Bogdan slots (B5)**;
   **Wendler / Yang (E3)** latent-computation precursors — read the new seeds.
6. D1: **Elhage 2021** (circuits math framework) + Olah 2020 "Zoom In".
7. F1: Binder 2024 + Kadavath 2022 + the introspection-debate trio
   (Ji-An / Song / Comșa). F2: Baars / Dehaene / Block + GWT-in-ML (Goyal,
   VanRullen) — confirm exact citations.
8. Housekeeping: **re-extract elhage2022** arXiv dir is PDF-only (superposition
   digest reads the tcircuits HTML instead); confirm the
   `anthropic2025-introspection` arXiv mirror (2601.01828).

See `related-work/papers.yaml` for the metadata manifest (verification status
per paper) and `related-work/fetch.sh` for the regenerable extraction script.
Extracts are git-ignored; rebuild with `./fetch.sh` (arXiv HTML view preferred,
marker PDF fallback needs a free GPU).
