# char-word-hybrid — the class whose results do *not* transfer to a sole char encoder

> Read-backed digest `[G]` (cluster D; Ma and Hovy's headline is `reproduced`,
> the rest `single-source`). These are the most-cited "character-level NER"
> papers, and all of them keep a word or subword table. Their character
> components buy +0.7 to +3.7 F1 on top of word embeddings. The one paper here
> that also ran the *reverse* ablation found the character-only variant 22 F1
> below the hybrid — with a 5-character context window, which is why that number
> bounds less than it appears to.

**Papers.** dos Santos and Guimarães, "Boosting Named Entity Recognition with
Neural Character Embeddings," NEWS workshop at ACL-IJCNLP 2015 (CharWNN);
Lample, Ballesteros, Subramanian, Kawakami, and Dyer, "Neural Architectures for
Named Entity Recognition," NAACL 2016; Ma and Hovy, "End-to-end Sequence
Labeling via Bi-directional LSTM-CNNs-CRF," ACL 2016; Ganesh and Reddy,
"…A Reproducibility Study," arXiv:2510.10936, 2025.
**Full text:** [CharWNN PDF](https://aclanthology.org/W15-3904.pdf) ·
[Lample PDF](https://aclanthology.org/N16-1030.pdf) ·
[Ma and Hovy PDF](https://aclanthology.org/P16-1101.pdf) ·
[Reproduction HTML](https://arxiv.org/html/2510.10936) ·
local extracts under `related-work/extract/`.

## Mechanism

All three share one template: compose each word's characters into a fixed vector
(CNN over a character window for CharWNN and Ma and Hovy; a BiLSTM over the
word's characters for Lample), concatenate it with a pretrained word embedding,
run a sentence-level BiLSTM (or a window classifier, for CharWNN), and decode
with a CRF. The character component is small — Ma and Hovy use 30 filters of
window 3.

## Evidence

**How much the character channel adds, on top of word embeddings:**

| paper | dataset | without characters | with characters | Δ |
|---|---|---|---|---|
| Lample et al. | CoNLL-2003 English | 90.20 | 90.94 | +0.74 |
| Lample et al. | CoNLL-2003 German | 75.06 | 78.76 | +3.70 |
| Lample et al. | stack-LSTM, English | 87.96 | 90.33 | +2.37 |
| Ma and Hovy | CoNLL-2003 English (BLSTM → BLSTM-CNN) | 87.00 | 89.36 | +2.36 |

Ma and Hovy's full stack reaches **91.21** English test F1 (and 97.55% PTB POS
accuracy); the CRF layer is worth a further +1.85 over BLSTM-CNN. A 2025
independent PyTorch reimplementation obtains **91.18** F1 and 97.52% POS
accuracy, attributing the residual to initialization and implementation detail —
so this number is `reproduced`, and it is the appropriate pre-transformer
English ceiling to quote.

**How much is lost when the word channel is removed** (CharWNN, Spanish
CoNLL-2002 test F1, identical architecture and hyperparameters across rows):

| variant | features | test F1 |
|---|---|---|
| CharWNN | word emb. + char emb. | **82.21** |
| WNN | word emb. + suffix + capitalization | 79.15 |
| WNN | word embeddings only | 70.87 |
| **CharNN** | **character embeddings only** | **60.06** |

This 22-point drop is the most-quoted evidence that "character-only does not
work" — and it is weaker than it looks. CharNN there is a window model with a
5-character context window and 200 convolutional units: its receptive field is
five characters, roughly one morpheme, with no sentence-level recurrence.
CharNER's contemporaneous chars-only 5-layer BiLSTM scored **82.18** on the same
Spanish CoNLL-2002 corpus — statistically indistinguishable from CharWNN's
hybrid 82.21. The CharWNN ablation measures a crippled context window, not the
character input.

CharWNN's other useful result: char embeddings replaced hand-built suffix and
capitalization features and did 3 F1 *better* (82.21 vs. 79.15), and its
architecture beat a feature-rich AdaBoost system using gazetteers, POS tags,
trigger words and entity-length features (82.21 vs. 81.39 on HAREM I).

## Contested and negative details

- These are the numbers most often cited as "character-level NER results". They
  are hybrid results. Any comparison that puts a chars-only tagger against them
  must say so, because the hybrids' word embeddings are pretrained on large
  unlabeled corpora and the character part is a small residual contributor.
- Every one of these systems is English/German/Spanish/Portuguese newswire with
  whitespace tokenization, so none of them tests the setting where a
  tokenizer-free model is most motivated (no reliable word segmentation, unseen
  script, noisy input).
- The reproduction study is a single independent reimplementation reported in a
  preprint; it confirms the score, not the paper's comparative claims.

## Design edge and limits

Use this class as the *contrast*: it establishes that character evidence is
complementary to word identity worth roughly 1–4 F1, that a CRF or equivalent
structured decode is worth about 2 F1 on top of a strong encoder, and that 91.2
is the reproduced pre-transformer English CoNLL number. Do not use it as
evidence for or against a sole character encoder — for that, the controlled
comparisons live in `charner.md`, `char-only-classical.md` and
`rendered-text-encoder.md`.
