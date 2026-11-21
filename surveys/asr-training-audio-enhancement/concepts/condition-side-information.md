# Telling the recognizer the input's condition

[G] `single-source` per result. Full texts: Raj et al. 2020
([PDF](https://arxiv.org/pdf/2011.02090v2)), Mantena et al. 2019
([HTML](https://arxiv.org/html/1909.02667v1)), Gong et al. 2023
([HTML](https://arxiv.org/html/2307.03183v1)), Polok et al. 2024
([HTML](https://arxiv.org/html/2409.09543v2)). Notes in
[readings](../related-work/readings/).

## The operation

Instead of changing the audio, estimate something about the whole
utterance (which bands are present, per-band noise level, speech and
non-speech spectra, a channel or bandwidth flag, a speaker-activity
track) and give it to the recognizer as an extra input. This leaves the
signal untouched, so the observation is not lost.

## What was found

| Name | Recognizer class and condition | Result | Source |
|---|---|---|---|
| Noise vectors (speech and non-speech mean spectra, utterance-level, appended to every frame) | Hybrid TDNN, LF-MMI; AMI SDM, Aurora-4 | AMI dev 38.8 to 34.9 (10% rel.); Aurora-4 7.94 to 7.37 (7.1%); complementary to i-vectors and to multi-condition training (21.6% combined on Aurora-4) | [raj2020](../related-work/readings/raj2020-noise-aware-training.md) |
| i-vector and Seltzer-style start/end-frame noise vectors, same setup | same | i-vector helps AMI (35.2), hurts Aurora-4 (8.24); start/end noise vector hurts Aurora-4 (8.17) | raj2020 |
| Bandwidth flag embedding plus common sampling rate | hybrid DNN, 3,400 h wideband + 600 h narrowband | NB 21.0 (NB-only) to 18.2; naive mixing 26.2; WB unchanged | [mantena2019](../related-work/readings/mantena2019-bandwidth-embeddings.md) |
| Diarization probabilities as a per-layer bias in Whisper's encoder | fine-tuned Whisper; AMI, NOTSOFAR-1, Libri2Mix overlap | NOTSOFAR-1 tcORC WER 19.1 to 22.6 vs 76.6 for the paper's input-masking variant (zeroing audio outside the target; which table section it belongs to is unclear in the extract) | [polok2024](../related-work/readings/polok2024-target-speaker-whisper.md) |
| Probe: does Whisper's encoder carry the noise type? | frozen Whisper vs other ASR encoders | Yes, in all depths; its robustness per noise class correlates with decodability of that class | [gong2023](../related-work/readings/gong2023-whisper-at.md) |

## What was not found

Missing-feature recognition and uncertainty decoding (per-band
reliability masks), and utterance-level channel or environment embeddings
for end-to-end or pretrained encoders, were searched for by name but no
primary paper on a large pretrained recognizer was found and read; see
the [survey's coverage section](../survey.md#retrieval-and-coverage). The
located work is on hybrid DNN systems. No located paper injects a band
presence or reliability estimate into Whisper, wav2vec 2.0, Conformer or
Zipformer and reports WER. Gong et al.'s probe is the only direct evidence
bearing on whether a large encoder gains from such information or infers
it: it indicates Whisper infers noise type itself, but it is a
correlation across noise classes, with no injection experiment.

## For the phone case

A bandwidth or channel flag costs nothing to compute when the source is
known (call type, codec); an estimated version adds a pass over the
utterance. The hybrid-era gains (7 to 13% relative) were on models without
large-scale multi-condition pretraining and are reported for matched
training of the conditioning; whether a pretrained encoder with
multi-condition data benefits is untested in the located literature.
