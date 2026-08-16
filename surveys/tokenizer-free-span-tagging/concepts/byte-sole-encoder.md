# byte-sole-encoder — bytes and characters as the only input, at three scales

> Digest `[S]`: read from the sibling survey's committed extracts
> (`../../shallow-surface-encoders/related-work/extract/…`), not re-fetched here.
> Trust `single-source` each. Three systems put raw bytes or codepoints in and
> span labels out at three very different scales, and together they give the
> quantitative core of this survey: **−13.8 F1 without a memorization channel,
> ~0 with one, and depth is where the quality comes from.**

**Papers.** Gillick, Brunk, Vinyals, and Subramanya, "Multilingual Language
Processing From Bytes," NAACL 2016 (BTS); Clark, Garrette, Turc, and Wieting,
"CANINE," TACL 2022; Xue, Barua, Constant, Al-Rfou, Narang, Kale, Roberts, and
Raffel, "ByT5," TACL 2022. **Full text:**
[BTS PDF](https://aclanthology.org/N16-1155.pdf) ·
[CANINE PDF](https://aclanthology.org/2022.tacl-1.5.pdf) ·
[ByT5 PDF](https://aclanthology.org/2022.tacl-1.17.pdf).
Sibling digests: [byte/codepoint compute](../../shallow-surface-encoders/concepts/byte-codepoint-compute.md) ·
[local downsampling](../../shallow-surface-encoders/concepts/local-downsampling.md).

## BTS — a byte-only span tagger, trained from scratch, four languages

Stacked LSTMs read UTF-8 bytes one at a time over 60-byte windows and emit span
triples `(start byte, length in bytes, type)`. No tokenizer, no vocabulary, no
gazetteer, no pretrained embeddings.

Exact-span F1 on CoNLL:

| system | en | de | es | nl |
|---|---|---|---|---|
| Florian et al. 2003 (gazetteers + external NER) | 88.76 | 72.41 | — | — |
| Carreras et al. 2002 | — | — | 81.39 | 77.05 |
| Klein et al. 2003 (character-level) | 86.07 | 71.90 | — | — |
| **BTS (one model, all 4 languages)** | **86.50** | **76.22** | **82.95** | **82.84** |
| BTS* (per-language models) | 84.57 | 72.08 | 81.83 | 78.08 |

Three results to carry:

1. **A byte-only tagger beat the best resource-free systems of its era** on all
   four languages, and beat the gazetteer-equipped CoNLL-2003 winner in German
   (+3.81) while trailing it slightly in English (−2.26).
2. **Multilingual joint training beat per-language training** by +1.93 (en),
   +4.14 (de), +1.12 (es), +4.76 (nl). For a byte model, pooling languages is a
   quality lever, not a compromise.
3. **Depth carries the quality; width barely matters.** Macro-averaged NER F1
   over the four languages:

   | depth ↓ / width → | 320 | 640 |
   |---|---|---|
   | 1 | 76.15 | 77.59 |
   | 2 | 79.40 | 79.73 |
   | 3 | 81.44 | 81.93 |
   | 4 | 82.13 | 82.18 |

   Four layers at width 320 (82.13) beats one layer at width 640 (77.59) by 4.5
   F1. Doubling width at depth 4 buys 0.05. This independently reproduces
   CharNER's recurrent finding and Conneau et al.'s convolutional one.

4. **Regularization is worth as much as architecture.** Average NER F1 rises
   74.75 (vanilla) → 78.76 (+dropout) → **82.13** (+byte-dropout, replacing
   random input bytes with a `DROP` marker). A 7.4-F1 swing from input-level
   noise alone; CharNER independently reports +2 F1 from character dropout.

POS tagging over 13 languages: BTS 95.85 average accuracy versus a feature CRF's
96.04 — i.e. within 0.2 of a strong feature system with no features at all.

## CANINE — pretrained character encoder, and the memorization deficit

CANINE hashes Unicode codepoints, applies a local transformer, downsamples 4×
before a deep stack, then upsamples for per-character predictions. NER F1
(CoNLL-2002/2003 average and MasakhaNER), against the authors' own retrained
mBERT to hold pretraining data constant:

| model | CoNLL | MasakhaNER |
|---|---|---|
| mBERT (theirs) | 87.8 | 72.4 |
| CANINE-C (pure character) | **74.0 (−13.8)** | **65.5 (−6.9)** |
| CANINE-C + character n-grams | 86.7 (−1.1) | 76.8 (+4.3) |

This is the single most important number in the survey. The authors' diagnosis
is memorization: NER "is a task in which memorization is often a very effective
strategy", mBERT's vocabulary hands it entity strings directly, and adding
vocabulary-free hashed character n-grams recovers 12.7 of the 13.8 lost points
and *exceeds* mBERT on the African languages. Their error analysis is concrete —
CANINE-C fails to label rare lexical items (*JCPenney*), and splits long
entities ("State Street Bank and Trust Company" → two spans; "TAMPA BAY" →
"TAMPA") — both of which n-grams mostly fix.

The coverage argument appears here too: mBERT emits nothing usable for Amharic
(no Ge'ez in its vocabulary) while CANINE reaches 50 F1 on a language absent
from its own pretraining.

Cost: a plain character BERT baseline (characters as input *and* prediction unit)
ran **10× slower** than subword BERT (925 vs. 9 000 pretraining examples/sec) and
lost 3.7 TyDi QA F1; CANINE's downsampling brings the full model back to roughly
mBERT's speed at 4× the sequence positions and ~30% fewer parameters.

## ByT5 — at scale, bytes win the span task

ByT5 is mT5 with UTF-8 bytes, a 3:1 encoder/decoder depth ratio, and the
vocabulary parameters reallocated into depth. On WikiAnn NER in the in-language
multitask setting (gold data in all target languages), parameter-matched:

| size | mT5 | ByT5 | Δ |
|---|---|---|---|
| Small | 86.4 | 90.6 | +4.2 |
| Base | 88.2 | 91.6 | +3.4 |
| Large | 89.7 | 91.8 | +2.1 |
| XL | 91.3 | 92.6 | +1.3 |
| XXL | — | 92.2 | — |

A byte-only model beats its subword twin at **every** size on multilingual span
tagging, with the advantage largest at the smallest size — the regime a small
deployed tagger lives in. ByT5 also degrades far less under input noise (random
casing: −1.5/−0.2 vs. mT5's −25.7/−14.3).

The price is sequence length: 1.5–2.6× slower inference on short word-level
tasks, 3.7–6.4× on summarization, 6.4–9.5× on sentence-pair classification, and
1.2–4.5× more fine-tuning steps to converge, except on tasks that favour bytes.

## Reading the three together

BTS and ByT5 say a byte-only model can match or beat its word/subword twin at
span tagging; CANINE says a character-only model without a memorization channel
loses 13.8 F1 on high-resource NER and recovers it with hashed n-grams. The
reconciling variables are (a) whether the model has *some* way to memorize
surface strings, (b) depth, and (c) whether the comparison is against a
vocabulary that actually covers the data. All three agree that width is cheap
and depth is not optional, and two of the three measure a large gain from
input-level noise regularization.

## Limits

None of these is a convolutional model, none reports a fair
throughput-matched comparison against a modern fine-tuned XLM-R tagger, and
CANINE's and ByT5's numbers depend on pretraining budgets far outside a small
from-scratch tagger's reach. BTS is the only one trained from scratch on
labelled data alone — and it is a 2016 system evaluated against 2003 baselines.
