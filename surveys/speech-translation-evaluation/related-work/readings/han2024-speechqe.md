**Source:** *SpeechQE: Estimating the Quality of Direct Speech Translation* — [PDF](https://arxiv.org/pdf/2410.21485) · [arXiv](https://arxiv.org/abs/2410.21485)

Extract: [`../extract/han2024-speechqe/html/2410.21485.md`](../extract/han2024-speechqe/html/2410.21485.md)

## 2026-11-24 — fable-5.2 — abstract, results, limitations and appendix A read; tables skimmed

Purpose: is there a metric that reads the audio itself, and does it beat
transcribing first? Followed from cettolo2026-sourceaware-st §2.2.

### What it claims

- **Task:** score a translation given the source *audio* and the
  hypothesis, no reference (quality estimation). Two builds: a cascade
  (ASR, then a text QE model such as xCOMET-qe, MetricX-qe, CometKiwi) and
  an end-to-end model — a speech encoder and adapter feeding a text LLM
  (TowerInstruct-7B, LoRA-tuned) trained on ASR, translation and QE (:15,
  :27, :267).
- **Training labels are metric scores**, xCOMET and MetricX computed with
  gold transcript and reference, on CoVoST2 es→en and en→de (:29, :259).
- **End-to-end beats the ASR cascade** in correlation with those metric
  labels, and beats a gold-transcript cascade whenever the QE model and
  the label metric are different families (0.834 vs 0.812, es→en, MetricX
  labels; :271). It also beats BLASER 2.0 (:267).
- **Against human direct assessment** (IWSLT 2023 ACL set): best
  end-to-end 0.509, best ASR cascade 0.503 (Whisper large-v3 +
  CometKiwi-23), gold-transcript text QE 0.580, best reference metric
  0.557 (:414, :418).
- **Error-span detection:** the cascade with a strong ASR is still best
  (:537).
- **Out of domain** (appendix A): the cascade is more robust; the
  end-to-end model, trained only on Common Voice audio, beats only
  medium-quality-ASR cascades when QE and label metric match (:736).

### Meaning for the purpose

The audio-input advantage over ASR-then-text is real but small on human
scores (0.509 vs 0.503), is learned from text-metric labels, and shrinks
out of domain. A good ASR plus a text metric is not clearly worse, and a
human transcript (0.580) is clearly better than either.

### Does not show

More than two European language pairs (:569); training on speech-specific
human labels (:563); whether the 0.006 human-correlation gap is
significant.
