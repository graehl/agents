# Frontier: tokenizer-free span tagging

> Void map and provisional claims over [`survey.md`](survey.md). Grounding mode
> `grounded`; the falsification searches below were run 2026-08-16 and are
> recorded with their queries so a later pass can re-run them.

## Void map

Axes: **input** (subword / character-or-byte / vocabulary-free-with-hashing) ×
**backbone** (pretrained transformer / small recurrent / small convolutional) ×
**training** (gold only / distilled from a large encoder). Cells are span
tagging; classification-only results do not fill a cell.

| input | backbone | training | status | evidence |
|---|---|---|---|---|
| subword | pretrained transformer | gold | `filled` | mBERT/XLM-R everywhere; the incumbent |
| subword | small recurrent | distilled | `filled` | XtremeDistil (35×/51×, 88.64 vs. 91.86 on WikiAnn-41); Farina et al. (1M student beats 220M teacher at 100 gold) |
| subword | small convolutional | gold | `filled` | spaCy MultiHashEmbed + 8-layer CNN, 0.77–0.79 Spanish CoNLL |
| subword | small convolutional | distilled | `filled` | Nityasya et al. CNN students on Indonesian sequence labeling |
| word (not subword) | small convolutional | gold | `filled` | ID-CNN, 90.32 CoNLL at 14× BiLSTM-CRF speed |
| character/byte | small recurrent | gold | `filled` | CharNER (7 languages); Gillick BTS (4 languages) |
| character/byte | pretrained transformer | gold | `filled` | CANINE (−13.8 CoNLL vs. mBERT), ByT5 (beats mT5 on WikiAnn), Cao 2023 |
| vocabulary-free + hashed n-grams | pretrained transformer | gold | `filled` | CANINE-C + n-grams (−1.1 CoNLL, +4.3 MasakhaNER) |
| character/byte | small convolutional | gold | **`untried`** | no located span-tagging system; the CNN char literature (Zhang, VDCNN) is classification-only |
| character/byte | small convolutional or recurrent | **distilled from a large encoder** | **`untried`** | every located student keeps a subword table |
| character/byte | any small model | gold | `tried-failed` *in one narrow form* | CharWNN's char-only variant, 60.06 vs. 82.21 — but with a 5-character context window, and CharNER reached 82.18 on the same corpus |
| rendered pixels | pretrained transformer | gold | `filled` | PIXEL on MasakhaNER |

Two voids survive. They are the same design seen from two sides.

### Void 1 — a character-native convolutional span tagger

No located work puts a deep convolutional network directly on characters and
predicts spans. The convolutional tagger literature (ID-CNN, spaCy) is
word/subword-input; the deep character CNN literature (Zhang et al., VDCNN) is
document classification with global pooling. The character *tagging* literature
(CharNER, BTS, CANINE) is recurrent or transformer.

**Why it is unexplored, plausibly:** the two lineages peaked in different years
(char taggers 2015–2017, fast CNN taggers 2017) and were superseded together by
BERT in 2018–2019, before anyone crossed them. Nothing in the evidence suggests a
barrier — the ingredients (dilated/tied blocks for receptive field, depth over
width, character dropout, structured decode) all exist and all point the same
way.

**Why it would matter:** the `O(1)`-sequential-depth argument that makes CNN
taggers 14× faster than recurrent ones gets *stronger* at character length, which
is exactly where character models are usually said to be too slow. It converts
the character model's main cost into the convolution's main advantage.

### Void 2 — distilling a large multilingual encoder into a character-level student

Every located distillation-to-small-tagger keeps the teacher's subword vocabulary
in the student. XtremeDistil says explicitly that mBERT's 110K×768 embedding
matrix (92M parameters) is what blocks massive compression, and then works around
it by shrinking the embedding dimension. A character student deletes that matrix
outright — ~200 alphabet rows instead of 110 000 — and XtremeDistil's own
ablation says the embedding initialization is worth only 1.2 F1 (SVD-of-mBERT
88.64 vs. random 87.43).

**Why it would matter:** the character family's documented weakness is sample
efficiency (Cotterell and Duh below 1 000 sentences; Zhang et al. needing
millions; ByT5's 1.2–4.5× slower fine-tuning convergence). Distillation
manufactures supervision from unlabelled text, which is the one input a
tokenizer-free student can consume without alignment problems: teacher and
student disagree about tokenization, but they agree about *character offsets*, so
teacher span decisions and even token-level posteriors can be projected onto
character positions. No located paper does this.

## Falsification gate

`prior-art-checked: 2026-08-16`

Queries run, and what they returned:

- OpenAlex forward citations of CharNER (W2574163994), 2022+: 15 works, all
  applied NER systems citing it as a baseline mention; none revisits chars-only
  tagging.
- OpenAlex forward citations of ID-CNN (W2740462959), 2022+: 20 works, mostly
  Chinese/biomedical domain NER reusing IDCNN-BiLSTM stacks at word level; none
  character-native.
- OpenAlex forward citations of CANINE, ByT5, Charformer crossed with "named
  entity recognition" / "sequence labeling" / "token classification": surfaced
  Ara-CANINE (2024), a Hinglish token-free benchmark (2026), Sub-Character
  Tokenization for Chinese (2023), Cao 2023, Sun 2023, and Rahman 2023 — all
  transformer-backbone or tokenizer-variant work, none a character CNN tagger.
- arXiv full-text search: `abs:"tokenizer-free"`, `abs:"token-free"`,
  `abs:"character-level" AND abs:"named entity"`, `abs:"byte-level" AND
  abs:"named entity"`, `all:"character-level" AND all:"named entity
  recognition" AND all:"multilingual"`. 2022+ hits are dominated by
  tokenizer-free *language modelling* (H-Net++, FlexiTokens, ByteFlow, adaptive
  chunking, MambaByte) and speech; the only NER-adjacent hits were Pattnayak et
  al. 2025 (character arm excluded before measurement) and a 2024 arXiv posting
  of Cotterell and Duh 2017.
- Distillation searches (web + OpenAlex, "distill … into character CNN / small
  character student / NER"): returned XtremeDistil, Wang et al. 2020, Farina et
  al. 2023, Nityasya et al. 2022, Tang et al. 2019, and DistilBERT-family work.
  No character-level student located.

Both voids survive the search. Novelty confidence is **moderate-to-high** for the
combination (character input + convolutional backbone + distilled from a
multilingual encoder + span tagging) and only **moderate** for each ingredient
pair, since applied work that does not describe itself in these terms is the
residual risk.

## Capstone ranking

1. **Distilled character-convolutional multilingual span tagger** (Voids 1+2
   jointly).
   *Impact:* high if it lands within ~1–2 F1 of a fine-tuned XLM-R at an order of
   magnitude less latency, because it removes the tokenizer, the vocabulary
   matrix, and the script-coverage failure mode (mBERT scores 0 on Amharic) at
   once. Moderate even if it loses, because the matched comparison does not
   exist and its absence is why 2025 papers still discard character input without
   measuring it.
   *Tractability:* high. All components are standard; the teacher already exists
   in the PII program; unlabelled text is free; the character-offset alignment
   between teacher and student is exact.
   *Novelty confidence:* moderate-to-high, per the gate above.
   *Cheapest discriminating check:* train the character CNN twice, with and
   without hashed character n-gram features, on one language pair, and see
   whether the n-gram variant closes a CANINE-sized gap. If the gap without
   n-grams is much smaller than −13.8, the memorization story is weaker than
   CANINE suggests and the design space is wider than assumed.

2. **Character-native convolutional tagger trained on gold only** (Void 1 alone).
   *Impact:* lower — it mostly re-measures CharNER with a faster backbone.
   *Tractability:* higher; no teacher needed.
   *Value:* it is the correct **ablation** of candidate 1, not a separate
   project: it isolates how much of the result is distillation and how much is
   the architecture.

## Provisional claims to revisit

- **"NER is a word-meaning task, so keep the subword vocabulary"** (Rahman et
  al. 2023). Regime: 10-step few-shot cross-lingual transfer, MasakhaNER, CANINE-C
  without n-grams. Independent check: none located. Cheapest discriminating
  check: converged in-language F1 with a memorization channel present. Revisit if
  a paper reports converged (not few-shot-adaptation) character-vs-subword NER.
- **"Character-level tokenization is impractical for NER"** (Pattnayak et al.
  2025). Regime: intrinsic proxies on FLORES-200, character sequences fed to a
  subword-pretrained IndicBERT, no downstream character measurement. Treat as
  unsupported for a character-*native* model. Unscheduled reminder: re-check if a
  downstream character arm appears in a revision.
- **"Hashed character n-grams recover the memorization gap"** (CANINE, +12.7 of
  13.8 F1). `single-source`, one architecture, one pretraining setup. This is the
  load-bearing assumption of capstone 1; the check above tests it directly and
  cheaply.
