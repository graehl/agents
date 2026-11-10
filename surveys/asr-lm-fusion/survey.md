# Small LMs fused with on-device ASR: architectures, rescoring, LM-aware training

**Grounding:** grounded. 44 manifested papers: 33 with committed full-text
extracts, read for the claims cited; HAT read from its saved arXiv HTML;
Meng 2021 from its abstract; 4 architecture papers and 5 PDF-only or
closed papers cited by verified metadata only. The
[manifest](related-work/papers.yaml) marks each entry
([retrieval and limits](#retrieval-and-limits)).
**Coverage cutoff:** 2026-11-09. **Search scope:** arXiv (eess.AS, cs.CL),
ISCA/ICASSP/ACL proceedings through web search; arXiv API, OpenAlex and ACL
Anthology for citation checks. Query terms: shallow fusion, cold/deep/
component fusion, internal LM estimation, density ratio, LODR, CTC prior,
MWER with LM, masked-LM / BERT / ELECTRA rescoring, lattice rescoring,
character vs subword LM, lexicon-free decoding, on-device LM, LookupLM,
Mamba/RWKV/SRU/linear-attention LM with ASR.
**Anchors:** Kannan 2018 (shallow fusion analysis), Toshniwal 2018 (fusion
comparison), Meng 2021 (ILME), Salazar 2020 (PLL rescoring), Likhomanenko
2019 (character LMs).

Question (graehl, 2026-11-09): is there a better-grounded architecture than
a character LSTM for a small causal character- or subword-level LM used in
shallow fusion with on-device ASR, or a bidirectional LM used for n-best
rescoring; and can the recognizer's training account for the fused LM?

Setting the answers are judged against (speech-recognition program,
draft repository `research/speech-recognition/multilingual/ngram-fusion-v1/README.md`):
CTC students (0.6B w2v-BERT, omniASR-CTC-1B), a 68M Zipformer transducer
and the Oswald/Qwen3-ASR 0.6B AED; a Snapdragon 8 Gen 1 phone CPU, 4
threads, ONNX Runtime int8; Lao, Haitian Creole, Sinhala, Vietnamese with
0.3–3 GB of LM text; CTC prefix beam 16–32 with one batched LM step per
frame, about 10 steps per audio second at batch about 5. Measured there for
Sinhala: a 3×1024 character LSTM (21.6M parameters, 21.7 MB int8) ties a
168 MB character 8-gram and beats parameter-matched pruned n-grams by
0.2–0.3 CER; its int8 step is 1.53 ms at batch 5; the 20M arm saw 0.69
epochs of its text.

## Decisions this survey supports

- **No located source measures an architecture that beats an LSTM as a
  small character LM in ASR fusion at equal per-step cost.** The measured
  architecture gains (gated convolution over a 20-gram −20% relative,
  Transformer over LSTM −6%) are for 160M–431M-parameter LMs on 800M+
  English words, and a Transformer's per-hypothesis cache is the wrong
  shape for a 16–32-wide prefix beam
  ([causal LMs](#causal-lms-for-shallow-fusion)).
- **The cheapest measured lever is decode-time internal-LM correction**,
  which the program has not tried. For CTC, subtracting a frame-level
  label prior took an external-LM decode from 5.3 to 4.9 WER in-domain and
  15.9 to 14.7 cross-domain, at no inference cost
  ([ILM correction](#internal-lm-correction-at-decode-time)).
- **Quality per unit of phone compute** is best served by sparse capacity:
  a hashed n-gram embedding table added to a small LSTM matched a 6×
  larger LSTM in fusion WER (LookupLM). Phone memory is not the binding
  constraint; compute is.
- **Bidirectional rescoring is an add-on after fusion, not a substitute.**
  Every located comparison has fusion ≥ rescoring with the same LM; a
  distilled 5M BERT rescorer costs about 8 ms per 5 hypotheses on 2 CPU
  threads and gained 3–8% over a 4M LSTM rescorer
  ([rescoring](#bidirectional-and-discriminative-rescoring)).
- **LM-aware training is measured for transducers and AED** (LM-aware
  MWER: about 10% relative on rare-word sets over plain MWER), **not for
  CTC with a fused character LM**, which is a void
  ([LM-aware training](#lm-aware-training), [frontier](frontier.md)).

The ranked experiment list for the program's bakeoff is in
[§ Next bakeoff arms](#next-bakeoff-arms).

## Causal LMs for shallow fusion

Detail and sources: [concepts/causal-fusion-lms.md](concepts/causal-fusion-lms.md).

- **Proposition:** a neural LM fused per label step beats an n-gram of the
  same units, and for character units the gain tracks usable context.
- **Nearest confusable alternative:** perplexity gains at large scale. Most
  architecture comparisons (SRU++, RWKV, Mamba, Transformer-XL) report
  perplexity or bits per character only; fusion WER at small size is a
  different, rarely measured quantity.
- **Evidence:** RNN over n-gram in fusion at matched units, WSJ graphemes
  10.3 → 7.7 (20-gram) vs 6.9 (2×512 LSTM), `single-source`, consistent
  with our Sinhala bakeoff; a 1.1 GB wordpiece LSTM matches an 80 GB 5-gram
  on Voice Search, `single-source`. Character LMs need long context:
  20-gram to 224M gated-convolution LM, LibriSpeech test-other 14.7 →
  11.7, `single-source`. Transformer over LSTM in AED fusion, 9.9 → 9.3,
  `single-source`.
- **Sparse capacity:** LookupLM concatenates a hashed embedding of the
  preceding \(n\) tokens to each LSTM layer's input; 9.6M dense parameters
  plus a table of 806M sparse parameters matched a 59.5M dense LSTM (head WER 6.3
  vs 6.2; base 7.1), and a layer-0-only 67.5M table got 6.5.
  `single-source`, wordpieces, Google Maps queries.
- **Regime:** all architecture comparisons are English, 800M+ words,
  160M+ parameters for the non-recurrent arms. No located result for a
  5–90M character LM on a phone CPU, for linear-recurrent LMs (RWKV, Mamba)
  in fusion, or for Lao/Sinhala/Haitian/Vietnamese neural LMs except
  Google's wordpiece Sinhala RNN-T, where fusion gained nothing (69.4 →
  69.3 WER) with mismatched text (log perplexity 11.9 vs 6.7).
- **Decision it changes:** choose phone-side architecture by per-step cost
  under a forking beam, where recurrent state is cheapest; spend capacity on
  sparse tables or on training the LSTM longer before trying attention.

### Units: character versus subword

- Character LMs reach word-LM WER at matched context and handle OOV words
  better (LibriSpeech OOV utterances 7.7 vs 10.4), `single-source`.
- Subwords shorten the sequence but enlarged the softmax and weakened a
  small-data wordpiece AED (WSJ 12.3 vs 10.3 grapheme), `single-source`.
- For agglutinative Finnish and Estonian, character units stayed close to
  morph units in lower-resource tasks (Smit et al. 2017, per a search
  snippet; PDF not extracted, `single-source` unverified here).
- Unsegmented scripts (Lao, Thai): no located fusion study. Character units
  sidestep segmentation; the program's char-over-word results for Haitian
  and Vietnamese (char 8-gram beats word 5-gram) point the same way for
  syllable-spaced and Latin scripts.

## Bidirectional and discriminative rescoring

Detail and sources: [concepts/bidirectional-rescoring.md](concepts/bidirectional-rescoring.md).

- **Proposition:** a masked LM's pseudo-log-likelihood (PLL), or a
  single-pass score distilled from it, ranks n-best hypotheses better than a
  causal LM of similar size, because it sees the whole hypothesis.
- **Nearest confusable alternative:** a causal Transformer rescorer, which
  tied finetuned ELECTRA on a LibriSpeech CTC 5-best (10.45 vs 10.42
  test-other) at similar cost.
- **Evidence:** BERT PLL over a weak LAS 100-best, test-other 20.37 →
  15.96; distilled single-pass score 16.15; MWED-trained 15.60,
  `reproduced` in direction across Salazar and RescoreBERT. On a strong
  Switchboard Conformer transducer BERT/RoBERTa still help while GPT-2 does
  not, `single-source`.
- **Cost:** PLL needs one pass per token (27× a Transformer LM in Futami's
  timing); the distilled form needs one. A 5M distilled BERT scored 5
  hypotheses of 16 tokens in 7.6 ms (2 CPU threads) against 9.7 ms for a 4M
  LSTM, `single-source`.
- **Regime:** English and Japanese, wordpiece units, rich text. No
  low-resource-language rescoring result was located.
- **Decision it changes:** keep shallow fusion as the first pass; a
  distilled bidirectional rescorer is a cheap optional second pass whose
  value must be measured on our own n-best lists.
- **Lattice rescoring** belongs to hybrid WFST decoders; the pruned RNNLM
  lattice-rescoring paper (Xu et al. 2018) was not read. Our prefix beam
  emits n-best lists, so lattice methods do not apply directly.

## Internal-LM correction at decode time

Detail and sources: [concepts/ilm-correction.md](concepts/ilm-correction.md).

- **Proposition:** an end-to-end recognizer's posterior already contains a
  prior learned from its transcripts; dividing it out before multiplying in
  the external LM (Bayes' rule) beats plain shallow fusion.
- **Nearest confusable alternative:** a length or label bonus. Zhou et al.
  show part of the gain is boosting labels against blank (dev-other SF 5.1,
  SF + length reward 4.8, ILM correction 4.4).
- **Evidence:** transducers, LibriSpeech test-other SF 5.5 → ILM 4.8,
  `reproduced` in direction (Zhou, Zeyer, LODR). CTC, conformer, 10k BPE:
  external LM 5.3 → with frame-level prior 4.9 in-domain; 15.9 → 14.7
  (prior) and 13.8 (distilled ILM) cross-domain, `single-source`. Density
  ratio's advantage over SF shrinks as target-domain audio grows (17.5 base:
  14.5 vs 12.5; 21k h fine-tuned: 7.7 vs 7.4), `single-source`.
- **Regime:** subword units, English and Mandarin, 960 h to 190k h. No
  located character-level or low-resource-language result.
- **Decision it changes:** try the frame-level prior (free) and a
  transcript char n-gram as density ratio (one lookup) on the CTC students
  before any new LM architecture; zero-encoder ILME or LODR for Zipformer;
  ILME for the AED.

## LM-aware training

Detail and sources: [concepts/lm-aware-training.md](concepts/lm-aware-training.md).

- **Proposition:** train the recognizer, by sequence-discriminative loss
  over n-best lists decoded with the fused LM, so its scores complement
  that LM.
- **Nearest confusable alternatives:** architectural fusion (deep, cold,
  component), which gates LM state into the decoder; and decode-time ILM
  correction, which changes no weights.
- **Evidence:** LM-aware MWER over plain MWER on a 120M HAT, Voice Search
  6.0 → 5.5 and rare-proper-noun sets about 10% relative, `single-source`;
  MWER-ILME over MWER-SF −5.8% average relative on 30k-hour transformer
  transducers, `single-source` (abstract only). First-pass shallow fusion
  beat deep and cold fusion for LAS, `reproduced` in direction; cold fusion
  beat SF for one Google RNN-T, `contested`.
- **Applicability:** MWER-style training applies to every decoder type;
  architectural fusion needs a decoder (transducer or AED), so not CTC.
  No located paper trains CTC with a fused character LM in the loop.
- **Decision it changes:** for CTC, start with decode-time correction;
  treat LM-aware MWER as a frontier experiment. For Zipformer and the AED,
  LM-aware MWER is a measured fine-tuning stage.

## How much LM, text and training a neural LM needs

No located source gives a text-size threshold at which a neural LM
overtakes a strong n-gram in fusion. What was measured:

| Evidence | Regime | Numbers | Grade |
|---|---|---|---|
| A large Transformer LM beats a 4-gram at every labeled-audio size | wav2vec 2.0 Base, letter CTC, LibriSpeech LM text (800M words); 10 min to 100 h labeled | test-other 4-gram → Transformer: 15.6 → 12.9 (10 min), 11.3 → 9.3 (1 h), 9.5 → 7.8 (10 h), 8.0 → 6.3 (100 h) | single-source |
| A compact LSTM matches an n-gram 70× larger | Voice Search, ~0.5B sentences for the LSTM | 1.1 GB LSTM 7.0 vs 80 GB 5-gram 7.2 | single-source |
| Gains shrink as the recognizer improves | LibriSpeech, + pseudo-labels; Voice Search 12.5k h; density ratio with 21k h target audio | ~20% → ~10% relative; 7.7 → 7.0; 7.8 → 7.4 | reproduced in direction |
| Mismatched text gives nothing | Google Sinhala, 160 h, 200M sentences mostly non-transcript | 69.4 → 69.3 | single-source |
| One multilingual LM helps most of 50 languages | 84-language Voice Search, 2B AED; per-language text 581K–451B sentences | GLaM (1.9B, 2 experts active) improved 43/50 languages, 5.53% average relative on those | single-source |
| Our own: undertrained LSTM already ties the best n-gram | Sinhala, 1.18G characters seen (0.69 epochs) in 55 min | 21.6M LSTM 4.40 vs unpruned 8-gram 4.40 CER | program measurement |

- **Reading for our regime (0.3–3 GB of text):** the located evidence says
  larger and better-trained neural LMs keep improving fusion when text is
  in-domain, with shrinking returns as the acoustic model strengthens. It
  does not say where a 5–90M character model saturates on 0.3–3 GB; the
  program's 20M arm stopped below one epoch, so its size and training
  length are both unexplored.
- **Not yet read:** Liu et al. (Findings of ACL 2024), *How Important is a
  Language Model for Low-resource ASR?*, is the one located study aimed at
  this question; it is PDF-only and its CPU extraction was abandoned as
  too slow under host load, so it is unread. Read it first on a re-survey.

## Contested results

- **Cold vs shallow fusion:** SF wins for LAS (Toshniwal, Switchboard and
  Google) and LibriSpeech RNN-T (Kim, 8.6 vs 9.4); cold fusion wins for
  Google's multilingual streaming RNN-T (Cabrera, Norwegian 22.4 vs 24.2).
  The axis is the decoder and how blank is handled in SF, not the LM.
- **Which ILM correction:** in-domain, density ratio, ILME and LODR land
  within 0.05 average WER of each other (LODR's LibriSpeech row); they
  separate only cross-domain, with a different winner per corpus.

## Negative and quiet results

- **Fusion that did nothing:** Google's Sinhala RNN-T (wordpiece, 160 h,
  60M LSTM on mismatched text) gained 0.1 WER from SF and 0.4 from cold
  fusion. Our character-level Sinhala gains (6.20 → 4.35 CER with the
  8-gram) show the language is not the cause; units, text match and error
  metric differ.
- **Larger production n-gram, little more:** an 80 GB 5-gram gained 0.2
  over a 2 GB one on Voice Search (7.4 → 7.2).
- **GPT-2 rescoring on a strong transducer** traded deletions for
  insertions with no net gain (Udagawa).
- **Masked PLL** is accurate but 27× slower than a causal Transformer
  rescorer; its distilled replacements lose 0.1–0.4 absolute.
- **ILME can hurt:** +8.0 WER on a LibriSpeech-fine-tuned Whisper with a
  trigram, recorded in the program's TTS survey.

## Baseline sensitivity

- Gains are reported over weak first passes in most rescoring papers
  (LibriSpeech LAS 100-best at 20.4 test-other, oracle 12.9). On a strong
  Conformer transducer only bidirectional rescoring still helped.
- Fusion gains halve as audio grows: ~20% → ~10% relative with 60k h of
  pseudo-labels (Synnaeve); density ratio's margin over SF falls from 2.0
  to 0.3 absolute as target audio grows from 0 to 21k h.
- Our own setting already has the strong baseline the literature lacks: a
  tuned character 8-gram. Gains quoted against "no LM" overstate what a new
  arm can add over that.

## Transfer to our setting

| Method | CTC students | Zipformer 68M | Oswald / Qwen3-ASR AED | Phone cost | Evidence grade |
|---|---|---|---|---|---|
| Character LSTM SF (current) | yes | yes | yes | 1.53 ms/step int8 at 21.6M | program-measured |
| Frame-level CTC prior subtraction | yes | — | — | ≈0 | single-source |
| Transcript char n-gram as density ratio / LODR | yes | yes | yes | one KenLM lookup | single-source each |
| Zero-encoder ILME | no | yes | yes | one predictor/decoder pass | reproduced in direction |
| LookupLM (hashed n-gram embedding + small LSTM) | yes | yes | yes | small-LSTM step + one table row | single-source, wordpieces |
| Transformer char LM with KV cache | yes | yes | yes | ≈LSTM matmuls + MB-scale state per hypothesis | single-source (large-scale only) |
| RWKV / Mamba char LM | yes | yes | yes | recurrent, fixed state | no fusion evidence |
| Distilled bidirectional rescorer | yes | yes | yes | ≈8 ms per 5 hypotheses (server CPU, 2 threads) | single-source |
| LM-aware MWER | void | measured (HAT) | measured (MWER-ILME) | none at inference | single-source |
| Cold / component fusion | no | contested | ≤ SF | ≥ SF | contested |

## Next bakeoff arms

Ranked by expected gain per unit of phone compute and of experiment cost,
on the same Sinhala logprob cache, decoder and selection/test protocol as
the 2026-11-04 bakeoff. Phone costs use the bakeoff's measured int8 scaling
(about 0.07 ms per million LSTM parameters per step at batch 5, 10.1 steps
per audio second) and are estimates where marked.

1. **Internal-LM correction for the CTC students** (decode-only). Evidence:
   CTC frame-level prior, external-LM WER 5.3 → 4.9 in-domain and 15.9 →
   14.7 cross-domain (Yang 2025); density ratio and LODR for transducers.
   Phone cost: prior ≈0; transcript n-gram ≈ +0.001 RTF (the measured
   8-gram cost). Experiment: estimate the blank-free label prior as the mean
   softmax over a few thousand training-set frames of the pick; subtract
   \(\lambda_I \log P_{\text{prior}}\) on label (non-blank) emissions;
   separately, subtract a char 3- or 5-gram trained on the recognizer's
   own training transcripts. Grid \(\lambda_I \in \{0, 0.1, 0.2, 0.3,
   0.5\}\) jointly with α and β for both the 21.6M LSTM and the 168 MB
   8-gram.
2. **Train the character LSTM to convergence, then scale it.** Evidence:
   every located comparison has larger, better-trained neural LMs gaining
   in fusion with in-domain text; the 20M arm saw 0.69 epochs, which
   confounds any architecture comparison against it. Phone cost: 3×1024
   unchanged (1.53 ms); a ≈48M 3×1536 ≈ 3.4 ms/step, +0.034 RTF
   (estimate, inside the 0.067 budget). Experiment: 3×1024 for 3–5 epochs
   and one ≈45–60M arm, checkpointed by held-out BPC; report test CER
   against measured step time.
3. **LookupLM-style hashed character n-gram embeddings.** Evidence: a 9.6M
   dense LSTM plus a hashed n-gram table matched a 6× larger LSTM in fusion
   WER (Huang 2021); the layer-0-only variant kept most of the gain.
   Phone cost: the small LSTM's step (0.38 ms at 3×512) plus one table row
   per hypothesis per step; table 64–128 MB int8 (estimate) against a 3 GB
   budget. Experiment: 3×512 LSTM with a \(2^{20}\)-row hashed embedding of
   the preceding 4–8 characters concatenated at layer 0; target the 21.6M
   arm's 4.40 CER at about a third of its step time.
4. **A small causal Transformer (or one-attention-layer SRU++-style hybrid)
   with a bounded KV cache, as a cost-measured arm.** Evidence:
   Transformer over LSTM −6% relative in AED fusion, but at 281M+
   parameters on 800M words (Irie); no small-scale fusion evidence.
   Phone cost (arithmetic): matmuls ≈ an equal-parameter LSTM, plus
   attention ≈16% at 6 layers × 512 × 256-character window, plus about
   0.8–1.6M cached values per hypothesis to fork and gather each frame.
   Experiment: 6×512, window 128–256 characters, no positional encoding
   (Irie found none needed); measure the int8 step with cache reordering on
   the phone before training to convergence; keep it only if it beats arm 2
   at equal milliseconds.
5. **Distilled bidirectional n-best rescorer as a second pass.** Evidence:
   5M distilled BERT gained 3–8% relative over a 4M LSTM rescorer at lower
   latency (RescoreBERT); fusion ≥ rescoring everywhere, so it rides on top
   of arm 1–3's fused beam. Phone cost: about 25 ms per utterance for a
   16-best (estimate from 7.6 ms per 5 hypotheses, server CPU). Experiment:
   distil PLL from a character or subword MLM trained on the LM text into a
   5M single-pass scorer, then MWED-train it on fused 16-best lists from
   the cache's training split.

Not ranked: LM-aware MWER for the CTC students with the fused LSTM in the
loop is the program's direct route to graehl's training question, but no
located result covers CTC ([frontier](frontier.md)); for the Zipformer and
AED it is a measured fine-tuning stage. RWKV and Mamba character LMs are
equally cheap per step as an LSTM but have no fusion evidence; they become
worth an arm only if arm 4 shows attention helps at small scale.

## Retrieval and limits

- **Databases:** arXiv API (id and metadata checks), OpenAlex (venue
  checks), ACL Anthology BibTeX, web search for discovery. Semantic Scholar
  and dblp rate-limited this pass; citation snowballing was by reference
  lists of the anchors read, not a forward-citation crawl, so saturation was
  not reached for the post-2023 slice.
- **Not read:** Liu et al. 2024, Maas et al. 2015 (PDF-only; CPU
  extraction abandoned under host load), Smit et al. 2017 and Xu et al. 2018
  (PDF-only), Shan et al. 2019 (no open full text), Meng et al. 2021
  (abstract only). The four architecture background papers (QRNN, SRU, gated
  convolution, Transformer-XL) are verified citations only.
- **Phone costs** in this survey are the program's measurements or
  arithmetic labelled as such; no source measured an LM step on a phone.
- **Extraction note:** marker-pdf ran on the GPU for five extracts (and
  part of a sixth, abandoned) before the pass switched to HTML-only and CPU
  extraction.
- **Bibliography:** every cited paper, with venue, identifier and read
  status, is in [related-work/papers.yaml](related-work/papers.yaml).
