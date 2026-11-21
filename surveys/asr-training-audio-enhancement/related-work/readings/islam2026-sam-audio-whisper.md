**Source:** *When Audio Separation Hurts Zero-Shot ASR: Evaluating SAM-Audio with Whisper on Bengali and English Speech* — [HTML](https://arxiv.org/html/2603.04710v2) · [arXiv](https://arxiv.org/abs/2603.04710v2)

# islam2026-sam-audio-whisper

2026-11-21, sonnet-5.5. Purpose: does a learned separation/denoising
front end help zero-shot Whisper on noisy speech (inference-time question).
Read: abstract, setup, all result tables, discussion and limitations.

**Claims.** SAM-Audio (Small variant, a diffusion-transformer separator)
applied before zero-shot Whisper (tiny to large-v3) raises WER/CER on a
13.8 h Bengali YouTube set (929 utterances) and on MS-SNSD English
(824 utterances), for every model size
([extract](../extract/islam2026-sam-audio-whisper/html/2603.04710v2.md):107-147).
Example: Bengali large-v3 WER 0.658 raw vs 0.774 enhanced; CER 0.241 vs
0.347. English base 0.105 vs 0.217; tiny 0.161 vs 0.266. PSNR on English rises
32.28 to 35.99 dB while WER worsens (lines 183-206).

**Reliability caveat (ours).** Several raw baselines are not usable
recognition: Bengali tiny/base/small/medium raw WER is 1.13 to 1.27, and
English small and large-v3 raw WER is 1.10 and 1.19 (lines 107-135), which
indicates hallucination or language-id failure rather than a clean
baseline; for those cells the "enhanced is worse" comparison compares two
broken systems. The cleanly interpretable rows are Bengali large-v3 and
English tiny, base and medium. One enhancer, one separator size, no
fine-tuning, no model-matched enhancement.

**Means for us.** Supports "perceptual or separation-style enhancement in
front of zero-shot Whisper does not help and can hurt", for a diffusion
separator. Does not test enhancers trained or adapted for the recognizer.

**Not shown.** Any effect on a recognizer fine-tuned on the processed
audio; clean-speech or phone-channel conditions; any metric split by noise
level (MS-SNSD SNR mix is not reported per bucket in the text read).

**Leads.** The paper's own limitations list joint adaptation or light
fine-tuning as untested.
