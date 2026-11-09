# Causal LMs for first-pass shallow fusion: what has been measured

Grounded from fetched full text (2026-11-09) unless a line says otherwise.
Map node: [survey.md § Causal LMs](../survey.md#causal-lms-for-shallow-fusion).

**Sources read** (full text, local extracts):

- Kannan et al., ICASSP 2018, *An analysis of incorporating an external LM
  into a sequence-to-sequence model* —
  [HTML](https://arxiv.org/html/1712.01996) · [PDF](https://arxiv.org/pdf/1712.01996) ·
  [extract](../related-work/extract/kannan2018-sf-analysis/html/1712.01996.md)
- Likhomanenko, Synnaeve, Collobert, Interspeech 2019, *Who Needs Words?
  Lexicon-Free Speech Recognition* —
  [PDF](https://arxiv.org/pdf/1904.04479) ·
  [extract](../related-work/extract/likhomanenko2019-lexicon-free/likhomanenko2019-lexicon-free.md)
- Irie, Zeyer, Schlüter, Ney, Interspeech 2019, *Language Modeling with Deep
  Transformers* — [HTML](https://arxiv.org/html/1905.04226) ·
  [extract](../related-work/extract/irie2019-deep-transformers/html/1905.04226.md)
- Kim et al. (Facebook), ICASSP 2021, *Improved Neural LM Fusion for
  Streaming RNN-T* — [HTML](https://arxiv.org/html/2010.13878) ·
  [extract](../related-work/extract/kim2021-nnlm-streaming-rnnt/html/2010.13878.md)
- Huang et al. (Google), Interspeech 2021, *Lookup-Table Recurrent Language
  Models for Long Tail Speech Recognition* —
  [HTML](https://arxiv.org/html/2104.04552) ·
  [extract](../related-work/extract/huang2021-lookuplm/html/2104.04552.md)
- Cabrera et al. (Google), 2021 preprint, *Language model fusion for
  streaming end to end speech recognition* —
  [HTML](https://arxiv.org/html/2104.04487) ·
  [extract](../related-work/extract/cabrera2021-lm-fusion-streaming/html/2104.04487.md)
- Synnaeve et al., SAS@ICML 2020, *End-to-end ASR: from Supervised to
  Semi-Supervised Learning with Modern Architectures* —
  [PDF](https://arxiv.org/pdf/1911.08460) ·
  [extract](../related-work/extract/synnaeve2019-e2e-modern/synnaeve2019-e2e-modern.md)
- Lei, EMNLP 2021, *SRU++* — [HTML](https://arxiv.org/html/2102.12459) ·
  [extract](../related-work/extract/lei2021-srupp/html/2102.12459.md);
  Peng et al., Findings of EMNLP 2023, *RWKV* —
  [PDF](https://arxiv.org/pdf/2305.13048) ·
  [extract](../related-work/extract/peng2023-rwkv/peng2023-rwkv.md);
  Gu and Dao 2023, *Mamba* — [HTML](https://arxiv.org/html/2312.00752) ·
  [extract](../related-work/extract/gu2023-mamba/html/2312.00752.md).
  These three were read for architecture and inference-cost claims only;
  none reports ASR fusion.

## Measured fusion results by architecture

| Claim | Setting | Numbers | Grade |
|---|---|---|---|
| Recurrent LM beats a same-unit n-gram in fusion | WSJ grapheme LAS (Kannan) | test WER 10.3 → char 20-gram 7.7, word 3-gram 7.6, 2×512 char LSTM 6.9 | single-source; same direction in our Sinhala bakeoff |
| Recurrent LM matches a 70× larger n-gram | Google Voice Search, 12.5k h LAS | 7.7 → 80 GB 5-gram 7.2; 1.1 GB 2×2048 wordpiece LSTM 7.0; rescoring with the 80 GB n-gram after the LSTM adds nothing | single-source |
| Char LM context length is the lever | LibriSpeech, letter AM, lexicon-free beam (Likhomanenko) | WSJ word perplexity: char 10-gram 211, 20-gram 177, char GCNN (57–81 char field) 76–90. Test-other WER: char 20-gram 14.7, char GCNN-20B (224M) 11.7, word GCNN 11.1 | single-source |
| Char LM ≈ word LM at matched context | same | lexicon-free char decoding within 0.1–0.6 WER of word LM; better on OOV utterances (test-clean OOV 7.7 vs 10.4) | single-source |
| Transformer LM beats LSTM LM, modestly | LibriSpeech AED, 10k BPE (Irie) | test-other 13.5 no LM → 4×2048 LSTM 9.9 → 24-layer Transformer 9.3 (−6% relative) | single-source; same direction in lattice rescoring (5.9 → 5.6) |
| A small dense LSTM plus a hashed n-gram embedding table matches a 6× larger LSTM | Google Maps, 4k wordpieces, 3B sentences (LookupLM) | head WER 7.1 base (5.5M dense) → 6.3 with table (9.6M dense + 806M sparse) vs 6.2 for a 59.5M dense LSTM; layer-0-only table (67.5M sparse) 6.5 | single-source |
| Cold fusion vs shallow fusion depends on the decoder | LibriSpeech RNN-T (Kim) vs Google RNN-T (Cabrera) | Kim: SF 8.6 beats CF 9.4 test-other; Cabrera: CF beats SF in Norwegian (22.4 vs 24.2) | contested |
| LM fusion can fail for a low-resource language | Google Sinhala RNN-T, 160 h, 60M wordpiece LSTM on 200M sentences (Cabrera) | 69.4 → SF 69.3, CF 69.0 WER; LM log perplexity 11.9 against 6.6–6.8 elsewhere (text mismatch) | single-source; our char-level Sinhala result contradicts it in direction |
| LM gains shrink as the acoustic model strengthens | LibriSpeech + 60k h pseudo-labels (Synnaeve) | GCNN LM relative gain ≈20% → ≈10% | single-source; consistent with Kannan's Voice Search result |

## Architectures without ASR-fusion evidence

- **SRU++** reaches Transformer-XL bits-per-character on enwik8 with
  3–10× less training compute and one attention layer; its reported
  inference speed is measured on a V100 at batch 1, not on a CPU.
- **RWKV** and **Mamba** run as recurrences at inference: constant state
  and per-token compute, independent of context length. Neither paper,
  nor any source located in this pass, measures them as a fusion LM in ASR
  ([frontier](../frontier.md#void-linear-recurrent-char-lms-in-fusion)).
- **QRNN, gated convolution and Transformer-XL** are verified citations
  only (not read here). Gated convolution is measured in ASR only through
  Likhomanenko's 163–224M char GCNNs above.

## Per-step cost at short context (our arithmetic, not a source)

With prefix beam search each surviving hypothesis carries its own LM state,
and a CTC frame may fork or merge hypotheses.

- **LSTM/GRU/RWKV/Mamba:** fixed-size state per hypothesis (3×1024 LSTM:
  6,144 values ×2 for cell and hidden); a fork copies a few KB.
- **Transformer with a KV cache:** a step costs roughly the dense matmuls
  of an equal-parameter LSTM plus attention over the window,
  \(\approx 4 L n d\) multiply-adds for window \(n\), \(L\) layers, width
  \(d\). For \(L=6, d=512, n=256\) that is 3.1M against ≈19M dense, about
  16% extra. The binding cost is state: \(2 L n d\) values per hypothesis,
  1.6M (6.3 MB fp32) at that shape, forked and gathered every frame for 16–32
  hypotheses. Irie et al. define the Transformer's search state as exactly
  these per-layer histories.
- **Character units make this worse:** a 256-character window is 40–60
  Latin words; 8-gram KenLM context is 8 characters. Subword units shorten
  sequences but enlarge the softmax and, in Kannan's WSJ setup, weakened the
  acoustic model (wordpiece LAS 12.3 vs grapheme 10.3).

## What transfers to our setting

- The strongest measured architecture gains (ConvLM over n-gram −20%
  relative, Transformer over LSTM −6%) come from 160M–431M-parameter LMs on
  800M+ words of English. Nothing located measures a 5–90M char LM on a phone
  CPU besides our own bakeoff.
- LookupLM is the only located method that buys quality without per-step
  dense compute, which is the phone's binding constraint (memory is not:
  21.7 MB used against a 3 GB budget). It was measured with wordpieces;
  hashing preceding characters instead is untested.
- Context length is the measured lever for char LMs; an LSTM's effective
  context is not bounded by a window, which may be why our 20M LSTM already
  ties the 8-gram.
