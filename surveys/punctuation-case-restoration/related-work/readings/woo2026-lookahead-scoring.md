**Source:** *Efficient Punctuation Restoration via Weighted Lookahead Scoring Method for Streaming ASR Systems* — [PDF](https://arxiv.org/pdf/2606.05179) · [arXiv](https://arxiv.org/abs/2606.05179)

## 2026-11-13 — fable-5.2, full text

Purpose: choosing form, size and data for a Vietnamese case+punctuation
restorer for words-only phone ASR output. Line citations are to
`extract/woo2026-lookahead-scoring/html/2606.05179.md`.

### Claims

- **Method.** At each word boundary, score "no mark", comma, period and
  question mark with a causal LM:
  \(S(a)=\alpha\log P(a\mid \text{prefix})+(1-\alpha)\log P(\text{next }K\text{ tokens}\mid \text{prefix},a)\).
  Insert the best mark only if its margin over "no mark" exceeds \(\tau\).
  \(\alpha\) and \(\tau\) are grid-searched on validation data per \(K\);
  the transcript is never rewritten (`:140-176`, `:212`).
- **Data.** English side of IWSLT 2017, 357,117 / 1,501 / 10,799 sentences;
  the prefix is reset at reference sentence boundaries (`:60`, `:157`,
  `:188`).
- **Results, F1 comma / period / question / 4-class macro:**
  prompted Llama-3.2-1B-Instruct 0.457 / 0.699 / 0.622 / 0.566;
  ELECTRA-small tagger, 2 subword tokens of lookahead, 0.752 / 0.992 / 0.925
  / 0.913;
  Llama-3.2-1B scorer, no fine-tuning, \(K=2\), 0.790 / 0.932 / 0.871 /
  0.893;
  LoRA-tuned scorer, \(K=2\), 0.840 / 0.986 / 0.935 / 0.937 (`:259-361`).
- **Lookahead ablation** (tuned scorer; macro / punctuation-only macro):
  \(K=0\) 0.646 / 0.543; \(K=1\) 0.927 / 0.909; \(K=2\) 0.937 / 0.920;
  \(K=3\)–\(5\) 0.930–0.935 / 0.911–0.918 (`:398-405`).
- **Prompted generation fails at 1B:** the instruction model puts a comma
  after every word in the example; the base model repeats the prompt
  (`:200-204`).
- **Stated limits:** English TED text only, no noisy recognizer output, no
  latency or memory measurement (`:457`).

### Meaning for our purpose

- An untuned 1B causal LM used as a scorer is within 0.02 macro F1 of a
  trained small encoder and ahead of it on commas (0.790 vs 0.752). For a
  language with little punctuated speech data, scoring with an existing LM
  is a way to get labels or a baseline without training a tagger.
- Prompting a 1B model to rewrite is not viable (macro 0.566).
- Some right context is necessary for a causal model; one or two tokens
  captured most of the measured gain, in a setting that flatters short
  lookahead (below).
- Cost per boundary is four hypothesis scorings of a 1B model, far above a
  tagger's single pass; nothing here argues for it on a phone.

### What it does not show

- Sentence boundaries are given: the prefix resets at each reference
  sentence and the lookahead is truncated at the sentence end, so an empty
  lookahead marks a sentence end for any \(K\ge 1\). Our reading; it fits
  period recall rising from 6,338 to 10,006 of 10,153 between \(K=0\) and
  \(K=1\) (`:420`, `:434`). Period and question scores therefore say little
  about unsegmented input.
- The ELECTRA baseline is the small variant restricted to two tokens of
  right context; no larger or full-context tagger, and the paper does not
  state its training set explicitly.
- Clean text, three marks, English, no capitalization, one run.
- No timing, although "efficient" is in the title.

### Leads worth fetching

- Polacek, Cerva, Zdansky, Weingartova 2023, *Online punctuation
  restoration using ELECTRA model for streaming ASR systems* (Interspeech)
  — the lookahead-versus-quality measurements this paper relies on.
- Polacek and Cerva 2025, *Lightweight online punctuation and
  capitalization restoration for streaming ASR systems* (Speech
  Communication 173) — small model, case and punctuation jointly, 4-word
  lookahead; closest to our target.
- Zhong and Sun 2025, *Punctuation restoration: a case study of BERT-based
  models' task-specific excellence* (ICASSP) — reported LLM failure modes
  (repeated marks, altered tokens, cost).
- Pogoda and Walkowiak 2021, *Comprehensive punctuation restoration for
  English and Polish*.
