# Field map: shallow surface encoders for token classification

> Read-backed prior art for adding inexpensive orthographic, lexical, and local
> sequence evidence to a strong token encoder, with multilingual PII span
> labeling as the live design case.

## Grounding and coverage

- **Grounding mode: `grounded`.** Thirty-seven primary papers were fetched and read;
  seventeen concept pages distill them below. Effectiveness claims are
  `single-source` unless a row explicitly says otherwise.
- **Coverage cutoff: 2026-08-14.** Search scope: ACL Anthology, arXiv,
  OpenReview, and OpenAlex forward citations; queries covered character-aware
  and byte-level encoders, token/character fusion, multilingual named-entity
  recognition (NER), shallow probes, local downsampling, late task fusion,
  Unicode character encodings, exchangeability, distributional character
  embeddings, Brown/PPMI character clustering, raw-byte versus codepoint
  modeling, byte-subword and morphology-driven compression, and fixed or
  learned entropy-coded text views, multilingual named-entity corpora,
  gazetteers, and locale/identifier registries for authentic entity surfaces.
- **Anchor set:** CharacterBERT, CANINE, Cao's controlled character-encoder
  comparison, SCRIPT, and Tsai's exchangeability classes. Forward citations
  were sorted by both recency and citation count; direct recent-paper searches
  supplemented the newest uncited edge.
- **Saturation was not reached.** The focused architecture region is adequate
  for a pilot decision, but this is not a claim that no adjacent 2026 system
  implements the exact proposed sidecar.

`[G]` means fetched and read. The full-text sources are linked from each digest;
the regenerable manifest is
[`related-work/papers.yaml`](related-work/papers.yaml).

## Read-backed digests

| cluster | digest | papers | decision-relevant result |
|---|---|---|---|
| A | [name-likelihood features](concepts/name-likelihood-features.md) | Yu et al. 2018 | character 6-gram likelihood alone identifies names across eight languages; simple features help six |
| A | [contextual string LM](concepts/contextual-string-lm.md) | Akbik et al. 2018 | pretrained bidirectional character-LM states were strong NER features |
| A | [character CNN](concepts/character-cnn.md) | CharacterBERT | word-local CNNs improve domain/noise robustness, at real pretraining cost |
| A | [token-embedding orthography](concepts/token-embedding-orthography.md) | Kaushal et al.; Itzhak & Levy | ordinary token embeddings already expose substantial spelling information |
| B | [local downsampling](concepts/local-downsampling.md) | CANINE; Charformer | locality plus early compression makes raw-character encoders feasible, not cheap |
| B | [encoder recipe](concepts/encoder-recipe.md) | Cao 2023 | controlled comparisons favor Charformer downsampling plus CANINE upsampling |
| C | [shallow hierarchy](concepts/shallow-hierarchy.md) | Sun et al. 2023 | a small intra-word encoder plus a deep word encoder can approach token-model throughput |
| C | [token-character cross-attention](concepts/token-character-crossattention.md) | Strawberry | a 1M-parameter character branch can alter character learning; downstream NER is untested |
| D | [dual character/subword channel](concepts/dual-channel-character-subword.md) | CharBERT | repeated fusion helps NER and noise robustness, but requires substantial continued pretraining |
| D | [retrofitted character embeddings](concepts/retrofit-character-embeddings.md) | XRayEmb | a roughly 1M-parameter character CNN can retrofit a token model; strong-base gains are inconsistent |
| D | [dual-stream fusion](concepts/dual-stream-fusion.md) | Wang et al. 2024 | full character and subword backbones yield small, mixed multilingual NER gains at high cost |
| E | [late task fusion](concepts/late-task-fusion.md) | EMBER | a small probe can turn frozen LM states into spans, but trails fine-tuned encoders |
| F | [byte local/global hierarchy](concepts/byte-local-global.md) | BLT | hashed short n-grams and local byte blocks are useful motifs inside a much larger LM |
| F | [byte state-space model](concepts/byte-ssm.md) | MambaByte | fixed-state causal byte modeling is efficient, but supplies no encoder-NER evidence |
| G | [character projections](concepts/character-projections.md) | SCRIPT; Tsai; Boldsen; Mayer; Kashioka; Liu | structural Unicode addresses and distributional substitutability classes solve different problems; no fixed Unicode-wide substitute map was located |
| H | [byte/codepoint compute](concepts/byte-codepoint-compute.md) | Gillick; Costa-jussà; Cherry; Wang; Khan; Shaham; ByT5; Libovický; Wolleb; MYTE; Zheng | bytes buy fixed-alphabet coverage and noise tolerance but lengthen non-Latin paths; full-codepoint composition and reversible compression are the supported remedies |
| I | [entity-surface resources](concepts/entity-surface-resources.md) | JRC-NAMES; MultiNERD; MultiCoNER v2; UNER | authentic carriers, structured seeds, and locale validators are complementary; none supplies representative PII surfaces across the target languages |

## Map: what each family buys

### A. Surface evidence can be useful without another deep encoder `[G]`

The closest task evidence is older and simpler than the recent byte-model
literature. Yu et al. train separate entity and non-entity character 6-gram
language models on token strings. Their score reaches 92.8 token-level P1 F1 in
English and 70.5 averaged over seven other languages, versus 96.5 and 76.8 for
their contextual NER ceiling. Adding a few likelihood features improves the
incumbent in six of eight languages, but hurts Tagalog. Flair instead pretrains
bidirectional character LMs and extracts boundary states for a downstream
sequence labeler; its 2018 English/German NER gains established that surface
form plus local context can complement word semantics. Both are
`single-source`, older-baseline results.

Two probes bound the need for explicit characters. Frozen subword-token
embeddings let trained probes recover character presence far above random in
Latin, Arabic, Devanagari, and Cyrillic scripts, and reconstruct substantial
fractions of unseen token spellings. Yet spelling-enriched initialization
converges to the same masked-language-model loss within about 1,000 updates.
The design implication is narrow: the existing token lookup is a credible cheap
surface input, while a generic spelling objective is not evidence that a new
branch will help entity tagging.

### B. Full character encoders need locality and compression `[G]`

CANINE and Charformer replace subword inputs with much longer character or byte
streams. Both make them tractable by doing cheap local work before the expensive
global stack and by reducing sequence length early. CANINE also shows a sharp
task warning: its plain character model trails mBERT badly on NER, while adding
character n-grams recovers or exceeds the baseline on the tested multilingual
set. Cao's matched study finds the strongest tested encoder-only recipe combines
Charformer downsampling with CANINE upsampling, but still costs about 2.7 times
the FLOPs and 0.68 times the throughput of its token baseline. These are useful
motifs for a later branch, not the first PII pilot.

### C. A small local branch can carry a distinct inductive bias `[G]`

Sun et al. use a four-layer intra-word transformer, a learned word aggregate,
and a twelve-layer inter-word transformer. It is nearly as fast as BERT in their
inference comparison and is strongest on open-vocabulary, domain, and noisy
English tasks, but its word segmentation is not suitable as-is for Chinese or
Japanese. Strawberry uses a roughly 1M-parameter character transformer and
token/character cross-attention; reducing its character width to 12.5% of the
main model did not materially change its synthetic character-learning curves.
This supports starting small. It does not establish a real NER gain.

### D. Deep or repeated fusion is a later rung `[G]`

CharBERT carries character and token channels through every transformer block;
Wang et al. repeatedly cross-attend between complete CANINE and XLM-R/RoBERTa
backbones. CharBERT improves clean CoNLL NER by 0.57 F1 over BERT and 0.27 over
RoBERTa in its report, with much larger synthetic-noise gains, but needs 320,000
continued-pretraining steps. The dual-backbone paper's MasakhaNER improvement
over XLM-R-large is only 0.09 mean F1 and is mixed by language, while requiring
roughly two to three times the memory. XRayEmb is the cheaper retrofit: a
roughly 1M-parameter character CNN replaces selected word embeddings. Its
strongest RoBERTa results largely come from domain-adaptive pretraining, and
replacing every word is noncompetitive. These results argue for late residual
fusion before architecture-wide interaction.

### E. Late task heads isolate cheap complementary value `[G]`

EMBER shows that a roughly 11.5M-parameter task probe over frozen decoder states
can add span detection at about 1% streaming overhead. Its NER quality remains
below fine-tuned encoder systems, and its causal context is a poor fit for
offline redaction. The useful precedent is architectural: freeze/cache the
expensive semantic path, train a small task path, and fuse only where the task
decision is made.

### F. Byte-scale systems offer motifs, not a pilot baseline `[G]`

BLT combines a local byte encoder, global latent transformer, and local decoder;
hashed 3--5-gram features carry much of the n-gram gain before diminishing
returns. MambaByte uses a causal selective state-space model to avoid attention's
quadratic byte-sequence cost. Both target general language modeling. Neither
tests a small bidirectional sidecar on multilingual token classification.

### G. Structural and distributional projections solve different problems `[G]`

SCRIPT gives every Unicode scalar a compact, collision-free block/index
address. Its block is a Script/category cue and its index is codepoint order
inside that block; neither component is learned from substitutability. Tsai's
exchangeability and location-independence counts are the closest located
direct class method: characters group only when both orders and, for the
location-aware form, both initial and non-initial positions occur inside known
tokens. Positional PPMI, adjacent mutual-information hierarchies, and Brown
clusters supply nearby distributional alternatives.

The located artifacts are small per-language vectors or corpus-trained classes,
not a released flat multilingual Unicode map. A live projection should
therefore be learned from train-only target-corpus units. Test the actual class
collapse separately from an identity-preserving `(cluster, within-cluster
index)` address; the latter can help a neural encoder without showing that
characters in one cluster are interchangeable.

### H. Byte alphabets trade vocabulary for sequence path `[G]`

The closest direct byte-versus-codepoint translation comparison is mixed:
Costa-jussà et al.'s byte BLEU ranges from about 3.3 points worse to 0.8 better
than Unicode characters, with faster convergence in their old recurrent setup.
At modern scale, ByT5 gains noise and spelling robustness by reallocating
vocabulary parameters into a deeper encoder, while paying longer sequences,
more FLOPs, and slower inference. Libovický et al. likewise find that modern
character translation generally remains slower and below subword quality,
apart from clear source-noise robustness. Bytes are a coverage and robustness
choice, not a universal clean-text quality advantage.

Byte-level BPE shortens the raw-byte path and retains exact round-trip coverage.
Wang et al. show that a one-layer bidirectional GRU is especially helpful when
BBPE tokens contain partial characters, but do not isolate those arbitrary
fragments as the cause of any gain. Land and Arnett supply the relevant
negative ablation: requiring byte merges to complete Unicode characters first
eliminates mixed partial-character tokens and almost universally improves
compression across their tested encodings and corpora. The default for a clean
Unicode sidecar should therefore compose complete codepoints first, then permit
multi-codepoint compression only inside the incumbent SentencePiece token span.

MYTE demonstrates that a different reversible 256-symbol code can shorten all
99 tested languages and substantially reduce non-Latin path-length disparity,
but its morphology-derived inventory is corpus-dependent and downstream NER is
roughly tied/slightly lower than ByT5. Binary or n-ary Huffman codes optimize
storage length rather than neural sequence cost; no located paper establishes
binary Unicode-codepoint streams as a strong sole neural input. Learned proxy
compression transfers when the code preserves local structure, while gzip-like
views are unstable and weak. For fixed-compute comparisons, measure actual
bytes per codepoint by language, match effective codepoint receptive field, and
report measured throughput as well as quality.

### I. Entity-surface data must preserve source role `[G]`

JRC-NAMES and Wikidata provide multilingual person/organization aliases;
GeoNames provides language-tagged place-name variants; CLDR, libphonenumber,
and the SWIFT IBAN registry provide locale or region validity constraints.
These are seeds and validators, not contextual span supervision. MultiNERD,
MultiCoNER v2, and UNER provide authentic or corpus-derived carriers, but their
language sets, annotation construction, entity types, and licenses differ.
MultiNERD is noncommercial, MultiCoNER's paper and AWS registry disagree on
ShareAlike, and UNER covers only person/organization/location under CC BY-SA.

The resulting acquisition contract is layered: human gold, mapped authentic
NER carriers, structured seeds, high-precision mining from authentic text, and
locale-audited synthetic data remain separately attributable. A source-blind
human audit samples both occurrence-weighted exposure and distinct surfaces.
The proposed fifteen-language extension owes the same acquisition and fluent-
review pass as the incumbent twenty; incidental corpus overlap does not close
that debt. See the digest for the exact language matrix and admission fields.

## Recommended pilot for multilingual PII

The first experiment should answer one question: **does cheap surface/local
evidence add held-out P1 span information after the incumbent XLM-R decision is
known?** It should not begin by rebuilding a character language model.

### Rung 0: non-neural diagnostic

Train entity/non-entity character n-gram likelihoods on the same training split
and add their log-odds as a P1 residual feature. This is the cheapest direct
test of the Yu et al. mechanism and a useful lower bound. It is not the proposed
ceiling.

### Rung 1: small independently trainable sidecar

Use the incumbent tokenizer and keep the deep XLM-R path frozen and cached.
Compare two input adapters feeding the same small local body:

1. **Frozen lookup:** XLM-R's token embedding (`H_-1`) projected to 64--128
   dimensions. This uses no transformer layer and begins with pretrained
   orthographic signal.
2. **Token ID:** a learned low-dimensional lookup, mathematically a linear map
   from literal one-hot token IDs. One-hot is allowed; the lookup form avoids
   materializing sparse vectors.

The initial local body should be one bidirectional convolution block with
parallel widths 1, 3, and 5, or one small local-attention block if convolution
is inconvenient. It predicts only `O/B/I` (or the project's equivalent P1
boundary states). Broadcast that residual across fine types:

```text
typed-logit(O)   += surface-logit(O)
typed-logit(B-k) += surface-logit(B)   for every type k
typed-logit(I-k) += surface-logit(I)   for every type k
```

Thus the semantic path still ranks P9/P20 types, while the sidecar can change
entityness and boundaries. Zero-initialize the final residual projection so
step zero exactly reproduces the incumbent. Cache incumbent logits and sidecar
inputs; only the sidecar and residual scale need train during this pilot.

### Acceptance and scale-up ladder

- Primary gate: held-out P1 precision/recall or overlap improvement on the
  weighted Final20 and priority-nine views, with per-language deltas.
- Guard: no material P9/P20 regression after the shared P1 residual is applied.
- Report trainable parameters, incremental latency/memory, and seen-versus-new
  surface behavior. A changed output is a smoke test; a held-out gain is the
  pilot result.
- If rung 1 helps, add hashed character 3--5-grams or a token-local character
  CNN; then compare cached `H_0`/early-layer states; then widen/deepen. Repeated
  cross-attention or a second full encoder is last, because the located evidence
  shows much higher cost and small strong-baseline gains.
- Default to bidirectional context for offline redaction. Keep a causal variant
  only as a streaming/latency control.

## Contested, negative, and quiet results

- **Explicit spelling is not automatically useful.** Token embeddings expose
  spelling, but spelling-enriched initialization did not improve masked-LM
  convergence. This directly bounds a generic spelling-pretraining story.
- **Character-only is not automatically better for NER.** Plain CANINE is much
  weaker than mBERT on the reported NER sets; n-grams rescue it. XRayEmb's
  all-word replacement is noncompetitive.
- **Strong baselines shrink gains.** CharBERT's clean-task gains are smaller over
  RoBERTa than BERT; full XLM-R/CANINE fusion changes MasakhaNER mean F1 by only
  0.09 over XLM-R-large.
- **Language effects reverse.** Simple character-LM features help six of eight
  languages but hurt Tagalog; dual-backbone per-language deltas are mixed.
- **Objective and task matter.** Strawberry's synthetic character results and
  BLT/MambaByte language-modeling efficiency do not establish span-labeling
  value.
- **Structure is not semantic similarity.** SCRIPT's deterministic block/index
  address is a tokenizer representation, while Tsai/PPMI/Brown classes are
  corpus-derived. No located source supports treating codepoint order as a
  substitutability coordinate.
- **Partial UTF-8 fragments lack an isolated benefit.** BBPE systems can learn
  around fragments that straddle codepoint boundaries, but the located direct
  tokenizer ablation favors completing characters before cross-character
  merges. Keep arbitrary fragments for malformed/noisy-byte controls.
- **Compression is not automatically a useful representation.** Huffman and
  gzip-like codes may save storage while lengthening dependency paths or making
  nearby strings discontinuous; structured token/neural proxies transfer more
  reliably only in much larger causal models.
- **Named-entity coverage is not PII-surface coverage.** The located multilingual
  corpora concentrate on person, organization, location, and public entities;
  dates, phones, addresses, and identifiers still require locale standards,
  authentic mining, and direct review. License and translated/silver provenance
  also prevent treating raw corpus overlap as production-ready supervision.

## Baseline sensitivity and prior-art boundary

The most favorable historical NER numbers predate modern multilingual encoders,
so they justify a cheap test rather than a forecasted gain. The fair incumbent
is the project's best calibrated XLM-R, scored on the same held-out documents;
the sidecar must earn its extra parameters and latency there.

No located paper exactly matches a small token-aligned, independently trainable
surface branch fused only as a shared P1 logit residual into a strong
multilingual XLM-R tagger. Nearby ingredients are well established: character
likelihood features, token-embedding probes, local character CNNs, and late
task fusion. Nor did the search locate a released deterministic Unicode-wide
flat substitutability map; the nearest methods learn exchangeability, PPMI, or
Brown-style classes from a specific corpus. It also found no matched evidence
that non-codepoint-aligned byte-BPE fragments improve a clean-text model, or
that a binary Huffman encoding of Unicode codepoints is a competitive sole
input. Novelty confidence for the exact composition is **moderate**, not high,
because the focused search did not reach citation saturation.
