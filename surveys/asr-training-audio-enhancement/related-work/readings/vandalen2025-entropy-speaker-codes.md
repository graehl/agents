**Source:** *Robust Unsupervised Adaptation of a Speech Recogniser Using Entropy Minimisation and Speaker Codes* — [HTML](https://arxiv.org/html/2506.10653) · [arXiv](https://arxiv.org/abs/2506.10653)

# vandalen2025-entropy-speaker-codes

2026-11-21, sonnet-5.5. Purpose: a speaker-level vector carried across a
speaker's utterances, fitted unsupervised, versus per-utterance inference;
and a loss that is robust to first-pass errors. Read: abstract, sections
2-4 text; figures not read (results are cited from text).

**Claims.** A 100M-parameter Conformer encoder-decoder (SpeechBrain
recipe) trained on Common Voice v18 (1,470 speakers, 855 h) augmented with
MUSAN noise and simulated rooms (far-field version). Each training
speaker has a learned 1024-dimensional "speaker code" injected into the
first encoder layers; half of the training utterances use a zero code so
the unadapted model stays valid. At test time only the code (and
optionally LoRA) is fitted per speaker from unlabelled audio by minimizing
the conditional entropy over multiple hypotheses instead of cross-entropy
on one pseudo-label. On the far-field set: unadapted 24.4% WER; trained
with codes but code set to zero 22.2%; adapting code plus LoRA on one
minute of audio 19.4% (20% relative), rising to 29% relative with ten
minutes; minimum-entropy beat pseudo-label loss in every setting and
adapting the 1024-dim code was more robust than LoRA on one minute
([extract](../extract/vandalen2025-entropy-speaker-codes/html/2506.10653.md):11, 159-179).

**Means for us.** The closest located case of an explicit carried
speaker/session vector in a modern (small, 100M) encoder, with per-speaker
state estimated from one to ten minutes of unlabelled audio and a loss
that guards against first-pass errors. Speaker, microphone path and room
are confounded in the "speaker" code (a speaker's utterances share
voice, and in this simulation probably noise and room settings; the paper
does not separate them in the parts read). The baseline is a model
already trained on augmented data, so this is a gain on top of noise
augmentation, not a head-to-head replacement.

**Not shown.** Whisper-class or large pretrained encoders; a controlled
comparison of the explicit code against more or better noise
augmentation; real recordings (the far-field is simulated); streaming
estimation of the code.
