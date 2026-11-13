**Source:** *A Small and Fast BERT for Chinese Medical Punctuation Restoration* — [PDF](https://arxiv.org/pdf/2308.12568) · [arXiv](https://arxiv.org/abs/2308.12568)

## 2026-11-13 — fable-5.2, full text

Purpose: choosing form, size and data for a Vietnamese case+punctuation restorer for words-only phone ASR output. Line citations are to
`extract/ling2023-small-fast-bert/html/2308.12568.md`.

### Claims

- **Recipe.** Give a 12-layer Chinese RoBERTa-wwm (102.3M) a
  punctuation-mark-prediction pre-training task on 50M tokens of unlabelled
  in-domain text (classify the mark at each mask slot; cross-entropy plus a
  0.1-weighted supervised contrastive loss), distil it into a student by
  matching hidden states with MSE for 100K steps, then fine-tune as a slot
  tagger (`:79-113`, `:171-199`, `:205`, `:351`).
- **Students.** 6 layers × 256 (10.3M), 4 × 312 (11.4M), 6 × 768 (59.7M)
  (`:126-128`).
- **Overall F1, Chinese medical test set, 10-seed means.** Teacher 90.68;
  PMP-H768 89.77; PMP-H256 85.74; PMP-H312 85.78; generic MiniRBT (10.3M)
  84.18; TinyBERT 83.95; RBT-6 (59.7M) 86.16; ALBERT (10.5M) 87.54
  (`:231-327`, `:335`).
- **Per class, teacher → PMP-H256.** Comma 95.03 → 90.07, period 91.00 →
  86.83, colon 86.00 → 80.32; comma recall 95.71 → 87.07 (`:232-243`,
  `:302-313`).
- **Ablation (PMP-H256, 30K steps).** Full 86.72; without contrastive loss
  85.56; without the punctuation cross-entropy 84.15; "w/o KD" 88.44
  (`:340-345`).

### Meaning for our purpose

- A 10M Transformer student keeps about 95% of a 100M teacher's punctuation
  F1 in-domain, losing 4–6 F1 on every class, period included.
- Task-specific distillation beats a generic same-shape student by 1.56 F1;
  a modest return for the pre-training cost. At 60M the gap to the teacher
  nearly closes (0.91).
- Teaching the encoder punctuation on unlabelled target-domain text before
  distilling is a reusable idea for Vietnamese.
- The loss in small students is recall, as in the English CNN-BiLSTM.

### What it does not show

- No case (Chinese), no ASR output, one narrow domain with few classes.
- No latency or memory figure despite "fast".
- ALBERT at 10.5M parameters beats both ~10M students and is compared only
  against the 59.7M one, with a "same number of parameters" claim the
  paper's own table contradicts (`:122`, `:126`, `:359`); stated 4.3%
  gains are 1.43 / 2.92 / 2.23 in the table.
- "w/o KD" beats the distilled model and is described as larger and slower
  (`:365`), so the ablation does not isolate distillation at fixed size.
- No comparison with simply fine-tuning the small model on more labelled
  data, or with logit distillation on the task.

### Leads worth fetching

- Yao et al. 2023, *MiniRBT: a two-stage distilled small Chinese pre-trained
  model* (`:388`), for the generic distillation recipe.
- Huang et al. 2021, *Token-level supervised contrastive learning for
  punctuation restoration* (`:381`).
- Lai et al. 2023, *Boosting punctuation restoration with data generation and
  reinforcement learning* (`:396`): written-to-spoken data gap.
- Fu et al. 2021, *Improving punctuation restoration for speech transcripts
  via external data* (`:379`).
