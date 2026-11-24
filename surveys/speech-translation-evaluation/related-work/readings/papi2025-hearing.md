**Source:** *Hearing to Translate: The Effectiveness of Speech Modality Integration into LLMs* — [PDF](https://arxiv.org/pdf/2512.16378) · [arXiv](https://arxiv.org/abs/2512.16378)

Extract: [`../extract/papi2025-hearing/papi2025-hearing.md`](../extract/papi2025-hearing/papi2025-hearing.md)
(marker-pdf; the arXiv HTML derivation failed on a missing image).

## 2026-11-24 — fable-5.2 — sections 1–5.1, 5.3, 6–7 and limitations read; per-benchmark tables not read

Purpose: do direct speech-to-translation models, including LLMs with a
speech encoder, now beat ASR-then-translate, and how was that scored.
Followed from cettolo2026-sourceaware-st §5.6, which uses its human set.

### What it claims

- **Scope:** 6 SpeechLLMs (Phi-4-Multimodal, Qwen2-Audio, Qwen3-Omni,
  DeSTA2, Voxtral, Spire) against 4 direct speech foundation models
  (Whisper, SeamlessM4T, Canary, OWSM) and 12 cascades of those with Aya
  Expanse, Gemma 3 or Tower+; 16 benchmarks, 13 language pairs, all with
  English on one side; models under 32B parameters (:17, :149, :153).
- **Cascades remain the most reliable overall.** Only Voxtral and
  Qwen3-Omni match or beat the best cascades on generic benchmarks;
  standalone speech foundation models trail both (:163).
- **By condition:** SpeechLLMs are as robust or more under added noise,
  where the cascade's ASR hallucinates (:240); cascades are better on
  emotional speech (:244) and long-form, where DeSTA2 and Qwen2-Audio
  collapse and Voxtral is the SpeechLLM exception (:246); named-entity and
  terminology accuracy follows the choice of LLM (:238).
- **Scoring is reference-free:** xCOMET-XXL and MetricX-24-Hybrid-XXL in
  quality-estimation mode, with the maximum penalty for wrong-language
  output (:115, appendix B :583).
- **Human check:** 60 items per language pair on CoVoST2 for one system
  per paradigm, error-span plus MQM protocol. The QE metrics reach about
  0.5 Pearson globally with human scores and "struggle to distinguish
  models at the item level" (:279, :330).

### Meaning for the purpose

As of late 2025 the answer to "does a direct model beat the cascade" is
no in general, yes for two models and for noisy audio. Every conclusion
rests on text QE metrics whose human correlation is about 0.5.

### Does not show

Non-English-centric pairs; conventional neural MT models in the cascades
(:677); whether the QE metric's source text was the gold transcript in
every benchmark (not found in the sections read).
