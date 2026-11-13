**Source:** *Capitalization and Punctuation Restoration: a Survey* — [PDF](https://arxiv.org/pdf/2111.10746) · [arXiv](https://arxiv.org/abs/2111.10746)

## 2026-11-13 — fable-5.2, sections 1, 2.7, 3, 4 and 5 in full; sections 2.1–2.6 skimmed

Purpose: choosing form, size and data for a Vietnamese case+punctuation restorer for words-only phone ASR output. Line citations are to
`extract/pais2021-survey/pais2021-survey.md`.

### Claims

- **Task and labels.** Case is four word-level classes: all-lower,
  first-upper, all-upper, mixed; sometimes a fifth "no case" for numbers and
  symbols. Sentence-initial capitals presuppose segmentation, so the two
  tasks are intertwined (`:37-39`, `:108-114`). Neural truecasers work at
  word level (class per word) or character level (case per letter) (`:172`).
- **IWSLT 2011 reference, per-mark F1 (period / comma / question).** Tilk &
  Alumäe 2016: 72.9 / 54.8 / 66.7; Yi & Tao 2019: 79.9 / 64.1 / 74.8; Yi et
  al. 2020: 84.1 / 73.6 / 75.8 (`:287-295`). Overall 64.4, 72.9, 77.8
  (`:266-281`).
- **ASR output.** Overall F1 falls 64.4 → 61.4, 72.9 → 68.8, 77.8 → 73.3
  (`:309-316`).
- **Comma is the hardest common mark** for every neural system listed;
  period leads comma by more than 10 F1; comma precision exceeds recall
  (`:299`, `:332`, `:338`).
- **Case, Wikipedia corpus, F1.** Lita et al. 2003: 86.8; Stanford CoreNLP:
  90.9; character RNN (Susanto 2016): 93.2; character CNN-BiLSTM-CRF (Ramena
  2020): 94.0, with P 94.9 and R 93.1 (`:340-349`).
- **Medical ASR (Sunkara 2020, as cited).** Period 79 and comma 69 on
  conversations, 85 and 72 on dictation; first-upper 83 and 87 (`:353`).
- **Data size beats model order for n-gram truecasing.** 58M → 55B tokens
  gave +6% case F1; n-gram order 3 → 6 gave under 1% (`:98`).
- **Prosody.** Pause duration is the most useful acoustic feature, and
  mixed text+audio models beat either alone in the work surveyed (`:214-216`,
  `:363-365`).
- **Distillation.** An ensemble teacher with a KL loss yields a single
  student above each individual model (Yi et al. 2017; `:238`).
- The IWSLT TED data is CC BY-NC-ND 3.0 (`:260`).

### Meaning for our purpose

- Gives the standard four-class case scheme and the option of
  character-level case for mixed-case words.
- Establishes, across many pre-2021 systems, the comma-below-period ordering
  and a 4-point clean-to-ASR drop.
- For case, more text mattered more than a bigger model in the n-gram era;
  suggests spending on names-rich Vietnamese text.
- Our transducer has token timings; pause duration is the cheap acoustic
  feature the literature most consistently finds useful.

### What it does not show

- Coverage stops before pretrained-encoder taggers became standard; its
  "state of the art" is 77.8 on IWSLT, below later 82–84.
- Tables collect self-reported numbers on subsets of IWSLT that the authors
  assume are comparable (`:262`); case numbers come from one paper's
  re-evaluation.
- No joint-vs-separate comparison, no model-size or latency data, nothing
  on Vietnamese or other languages without the English punctuation habits.
- No split of case accuracy into sentence-initial and proper-name words.

### Leads worth fetching

- Sunkara et al. 2020, *Robust prediction of punctuation and truecasing for
  medical ASR* (`:202`): joint model, domain and task adaptation, ASR
  augmentation.
- Susanto et al. 2016 and Ramena et al. 2020: character-level truecasing
  (`:174-176`).
- Yi et al. 2017, distillation from an ensemble (`:238`).
- Tilk and Alumäe 2016, the BiRNN baseline with pause features (`:234`).
- Gravano et al. 2009, data-size study for case and punctuation (`:98`).
- Augustyniak et al. 2020, ASR homophone errors and retrofitted embeddings
  (`:250`).
