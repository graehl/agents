**Source:** *Speaker Adaptation for End-To-End Speech Recognition Systems in Noisy Environments* — [HTML](https://arxiv.org/html/2211.08774v3) · [arXiv](https://arxiv.org/abs/2211.08774v3)

# wagner2022-speaker-adaptation-noisy

2026-11-21, sonnet-5.5. Purpose: i-vector / x-vector style utterance-level
vectors as conditioning for end-to-end and pretrained recognizers, in noise.
Read: abstract, method, results text and discussion (the per-cell table
was not transcribed).

**Claims.** i-vectors, x-vectors and ECAPA-TDNN embeddings (512 and 192
dimensions), each extracted per utterance, are concatenated as auxiliary
input to a transformer and to a wav2vec 2.0-based model (the pretrained
LibriSpeech model kept frozen on LibriSpeech, trained on Switchboard),
tested clean and with added noise at SNR 18, 9 and 0 dB. Best relative WER
gains: 16.3% (transformer, LibriSpeech test-clean at 18 dB, ECAPA 512) and
14.5% on Switchboard. For the wav2vec 2.0 models the largest gain is
6.3% (Callhome, clean, x-vector) and gains "diminished or turned negative"
at 9 and 0 dB; for the transformer, gains grow as noise grows. X-vector
and ECAPA beat i-vectors. A hybrid LF-MMI system gets 8.8% to 15.6% from
i-vectors
([extract](../extract/wagner2022-speaker-adaptation-noisy/html/2211.08774v3.md):627-640).
The authors attribute the smaller wav2vec 2.0 gain partly to injecting the
vector after the feature extractor, a late point.

**Means for us.** For a pretrained encoder, utterance-level
speaker/channel vectors give a smaller and noise-sensitive gain than
for a model trained from scratch, and less than in hybrid systems;
the gain disappears in strong noise for the pretrained model.

**Not shown.** Carry-over across utterances (the vector is per utterance
here); Conformer transducers (stated as future work); comparison with
noise-augmented training of the same model.
