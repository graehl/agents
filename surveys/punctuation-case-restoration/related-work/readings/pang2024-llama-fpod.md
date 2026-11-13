**Source:** *LLaMA based Punctuation Restoration With Forward Pass Only Decoding* — [PDF](https://arxiv.org/pdf/2408.11845) · [arXiv](https://arxiv.org/abs/2408.11845)

## 2026-11-13 — fable-5.2, full text

Purpose: choosing form, size and data for a Vietnamese case+punctuation
restorer for words-only phone ASR output. Line citations are to
`extract/pang2024-llama-fpod/html/2408.11845.md`.

### Claims

- **Model.** LLaMA2 13B, LoRA-tuned on 20k examples from LibriSpeech-PC
  train-clean-360 with an instruction/input/response prompt (`:204`).
- **Forward-pass-only decoding (FPOD).** Copy the unpunctuated input into
  the response slot, run one forward pass, and insert a mark wherever the
  next-token prediction at a response position is a punctuation symbol
  (`:62-66`). Token count and wording are unchanged, which the authors
  present as removing hallucination (`:130`).
- **LibriSpeech-PC test, F1 question / period / comma and speed:**
  autoregressive 0.80 / 0.84 / 0.74 at 88.72 tokens/s; speculative decoding
  with a 350 MB distilled assistant, same F1 at 173.43 tokens/s; FPOD 0.79 /
  0.85 / 0.66 at 1,760.30 tokens/s, 19.84× (`:204-208`, `:227-243`).
- **Recursive FPOD.** Because one pass conditions each prediction on an
  unpunctuated history (`:134`), a second pass is run with inserted marks
  fed back (`:146-148`).
- **Long video set** (in-house, 1.2k utterances averaging 5 minutes; 808
  question marks, 9,837 periods, 6,457 commas): RNN-T 1B 0.63 / 0.68 / 0.40;
  Whisper large v2 0.58 / 0.65 / 0.46; FPOD 0.79 / 0.82 / 0.63; recursive
  FPOD 0.93 / 0.95 / 0.87 at 959.1 tokens/s, 10.8× autoregressive
  (`:262-280`, `:288`).
- Long input is processed with a padded sliding window (`:138`).

### Meaning for our purpose

- FPOD is a causal LM used as a tagger. It shows that the "cannot alter
  words" property is available to decoder-only models, at one forward pass
  per window, and that left-only context costs commas (0.74 → 0.66) unless a
  second pass sees its own marks.
- The idea transfers to a small causal LM: if a causal character or subword
  LM is already on the phone for fusion, a punctuation head read from its
  next-token distribution is a candidate form. This paper does not test
  anything small.
- Recognizers that emit their own punctuation scored comma F1 0.40–0.46 on
  5-minute inputs. A separate restorer after a words-only transducer is not
  a handicap on this evidence.

### What it does not show

- No encoder-tagger baseline at all; the comparison systems are the LLM's
  own decoding modes and two recognizers.
- Input is reference text with punctuation removed (`:200`), not recognizer
  output. No capitalization.
- A 13B model on unstated hardware; nothing about small models, CPUs or
  memory.
- The headline 0.93 / 0.95 / 0.87 is on a private set with no description
  of domain match to training, and the jump from single-pass FPOD on the same
  set is unexplained beyond the feedback argument. No autoregressive score
  is given on that set.
- No measured rate of word changes for the autoregressive mode.

### Leads worth fetching

- Meister et al. 2023, *LibriSpeech-PC: benchmark for evaluation of
  punctuation and capitalization capabilities of end-to-end ASR models* —
  the benchmark and its metrics.
- Courtland, Faulkner, McElvain 2020, *Efficient automatic punctuation
  restoration using bidirectional transformers with robust inference* —
  overlapping-window inference for taggers.
- Păiş and Tufiş 2022, *Capitalization and punctuation restoration: a
  survey*.
- Liu et al. 2024, *MobileLLM: optimizing sub-billion parameter language
  models for on-device use cases* — source of the 350 MB assistant.
