**Source:** *Vietnamese Capitalization and Punctuation Recovery Models* — [PDF](https://arxiv.org/pdf/2207.01312) · [arXiv](https://arxiv.org/abs/2207.01312)

## 2026-11-13 — fable-5.2, full text

Purpose: choosing form, size and data for a Vietnamese case+punctuation restorer for words-only phone ASR output.

### Claims

- ViCapPunc: 425,350 sentences from 50,000 medical question–answer pairs
  crawled from three Vietnamese health sites; labels CAP, ALL-CAP and comma,
  period, question mark; split 50/20/30
  (extract/uyen2022-jointcappunc/html/2207.01312.md:39-41). Test counts:
  137,865 commas, 111,717 periods, 16,718 question marks, 191,767 CAP,
  23,173 ALL-CAP (:58-63).
- JointCapPunc: shared encoder, case head, and a CRF punctuation head that
  receives a 256-d embedding of the case probabilities; loss weight on case
  0.15 (:100-138, :174).
- vELECTRA: case F1 86.75 and punctuation F1 80.10 joint, against 83.53 and
  78.65 for two single-task models and 84.16 and 79.33 for a
  punctuation-then-case joint baseline. XLM-R: 85.39 / 78.74 joint against
  83.55 / 78.48 single-task (:198-249).
- Ablations on vELECTRA: no case feature 83.13 / 79.13; softmax instead of
  CRF 83.98 / 78.71; FastText instead of the encoder 60.73 / 49.47
  (:272-306).

### Meaning for our purpose

- The only Vietnamese dataset read that has case labels, and the only
  Vietnamese evidence that one two-head model beats two separate models
  (+1.8 to +3.2 case F1, +0.3 to +1.5 punctuation F1).
- Case labels are two-way (CAP, ALL-CAP); mixed case would need an added
  class or a lexicon.
- Dropping the pretrained encoder is catastrophic in their setup (−26 case,
  −31 punctuation F1): a small student should be distilled from or
  initialised by a pretrained model, or at least have a real context layer.
- The authors themselves flag the encoder as too heavy for an ASR pipeline
  and leave a small model to future work (:326).

### What it does not show

- No per-class F1 (comma vs period; CAP vs ALL-CAP), no split between
  sentence-initial and proper-name capitals.
- Evaluated on typed Q&A text, not ASR output, despite the ASR motivation.
- Segments are cut at sentence ends (:41), so every test segment starts with
  a capital and ends with a mark; scores are optimistic for unsegmented
  streams.
- Single runs, no intervals; joint gains of under a point on punctuation are
  within plausible seed noise.
- The CRF ablation changes case F1 by 2.77 although the CRF is on the
  punctuation head; unexplained. Text and table disagree on the FastText
  drops (:322 vs :303-306).
- The FastText variant has no stated context layer, so it is not a fair
  small-model baseline.
- XLM-R size not stated; dataset licence not stated; one medical domain.

### Leads worth fetching

- Sunkara et al. 2020, *Robust prediction of punctuation and truecasing for
  medical ASR*: the punctuation-then-case design and ASR-aligned
  augmentation (:354).
- T. T. H. Nguyen et al. 2021 (IEICE), *Toward human-friendly ASR systems:
  recovering capitalization and punctuation for Vietnamese text* (:351).
- T. B. Nguyen et al. 2020 (Interspeech), Vietnamese NER from speech using
  case and punctuation recovery (:335).
- O. T. Tran et al. 2021 (PRICAI), *Punctuation prediction in Vietnamese
  ASRs using transformer-based models* (:345).
- Pahuja et al. 2017, joint BiRNN for case and punctuation (:353).
