**Source:** *Listen, Adapt, Better WER: Source-free Single-utterance Test-time Adaptation for Automatic Speech Recognition* — [HTML](https://arxiv.org/html/2203.14222v2) · [arXiv](https://arxiv.org/abs/2203.14222v2)

# lin2022-suta

2026-11-21, sonnet-5.5. Purpose: test-time adaptation of the recognizer as
the alternative to changing the audio. Read: abstract, method, setup,
Table 1 and 2 discussion, cost remark.

**Claims.** One utterance at a time, adapt layer-norm and feature-extractor
parameters of a CTC recognizer by minimizing entropy plus minimum class
confusion for 10 AdamW steps, then decode and discard the change. Source
model: wav2vec 2.0 base fine-tuned on LibriSpeech 960 h, no LM
([extract](../extract/lin2022-suta/html/2203.14222v2.md):121, 206).
WER: LibriSpeech test-other 8.6 to 7.3; with Gaussian noise 0.005 / 0.01:
13.9 to 10.9 and 24.4 to 16.7; CHiME-3 31.2 to 25.0; Common Voice 36.8 to
31.2; TED-LIUM 13.2 to 11.9 (line 121; text lines 226-228). Naive
pseudo-labelling (SDPL) gives 8.3, 13.1, 23.1, 30.4, 36.3, 12.8, so the
gain needs the entropy objective. Adaptation took about 0.115 s per second
of audio for 10 steps on an RTX 3090 (line 220).

**Means for us.** The one located input-side alternative that targets
exactly "this utterance differs from training" and gives sizeable gains in
mismatched noise on a modest supervised recognizer. Cost on a phone is
backpropagation per utterance, not a front end.

**Not shown.** Large or Whisper-class recognizers (this is a 95M-parameter
model fine-tuned on 960 h; its in-domain test-other WER of 8.6% is far
above Whisper-class, so there is more room); low-resource languages;
phone-class compute. Later work (e.g. SGEM, arXiv 2306.01981) reports
gains over SUTA on 12 datasets; not read here.
