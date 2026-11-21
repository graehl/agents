# Explicit condition input or target against augmentation alone

[G] `single-source` per result. Full texts: Lin et al. 2026
([PDF](https://arxiv.org/pdf/2609.31699)), Prasad et al. 2021
([HTML](https://arxiv.org/html/2102.06237)), Serdyuk et al. 2016
([PDF](https://arxiv.org/pdf/1612.01928)), Mitra et al. (Amazon)
([PDF](https://cdn.amazon.science/ba/d7/679a60ab4bcdb9a8b57f34a5dc45/unified-modeling-of-multi-domain-multi-device-asr-systems.pdf)),
Weninger et al. 2021 ([HTML](https://arxiv.org/html/2109.08744)), plus
Seltzer 2013, Raj 2020 and Wagner 2022 on the
[side-information](condition-side-information.md) and
[carried-state](carried-state-and-adaptation.md) pages. Notes in
[readings](../related-work/readings/).

This page replaces the earlier statement that no paper had an arm with
augmentation only and an arm with augmentation plus explicit condition
input or target.

## Head-to-head arms found

| Paper | Model, condition | Augmentation-only arm | Plus explicit condition | Result |
|---|---|---|---|---|
| [Lin 2026](../related-work/readings/lin2026-normalise-or-condition.md) | keyword spotting (not ASR), 57 to 349 k parameters, UAV ego-noise | log-mel with noise-augmented training | per-band noise floor from the previous 2 s as a second input channel | matched-type noise training: 81.2% to 83.1 to 83.5% mean accuracy; generic noise training: 72.3% to 78.1%; false-alarm rate kept (conditioning) vs raised (subtracting) |
| [Prasad 2021](../related-work/readings/prasad2021-e2e-robust.md) | DeepSpeech2-style CTC, seven noise types | noise augmentation with soft-freezing: clean 10.90, babble 0 dB 77.4 | noise-type classification as an auxiliary target (multitask) | clean 11.05, babble 0 dB 71.4, cafe 0 dB 44.9 vs 49.1 |
| [Prasad 2021](../related-work/readings/prasad2021-e2e-robust.md) | same | same | gradient reversal on the noise classifier (condition removed) | largest low-SNR gains; clean WER 13.07 to 13.79 |
| [Serdyuk 2016](../related-work/readings/serdyuk2016-invariant.md) | hybrid DNN, Aurora-4 | multi-condition training | adversarial clean/noisy classifier | 1 noise type: 16.36 vs 18.14; 6 types (full coverage): 12.62 vs 12.60 |
| [Amazon](../related-work/readings/amazon2021-multi-device.md) | RNN-T, three device types, 60 K h | device-specific fine-tuned models | device-type one-hot input; device experts; device-adversarial | one-hot input -4 to +4% relative; adversarial removal 1.4 to 3.9%; device experts and attentive experts 2 to 10% |
| [Weninger 2021](../related-work/readings/weninger2021-dual-encoder.md) | E2E, close-talk vs far-talk medical speech | best single-encoder matched | learned encoder selection between condition-specific encoders | up to 9% relative |
| [Seltzer 2013](../related-work/readings/seltzer2013-noise-aware-training.md) | hybrid DNN, Aurora 4 multi-condition | 13.4 | noise estimate appended | 13.1 (2% relative); 12.4 with dropout |
| [Raj 2020](../related-work/readings/raj2020-noise-aware-training.md) | hybrid TDNN, AMI and Aurora-4 | baseline | speech and non-speech mean vectors | 7 to 10% relative; adds to multi-condition training (21.6% combined on Aurora-4) |
| [Wagner 2022](../related-work/readings/wagner2022-speaker-adaptation-noisy.md) | transformer, wav2vec 2.0 | baseline with noisy test | i-/x-vector input | up to 16.3% (transformer), 6.3% (wav2vec 2.0), none at 9 and 0 dB |

Also read: [Vincent 2017](../related-work/readings/vincent2017-mismatches.md):
on CHiME-3 training on several environments and different microphones
"barely affects" recognition; only the number of microphones matters. That
supports coverage by augmentation over an explicit condition estimate, for
that hybrid system.

## Reading

- Explicit condition information does help in controlled arms (about 2 to
  9% relative with matched augmentation; up to 10% with device-specific
  parameters), and it helps most where augmentation coverage is poorest
  (Lin: generic noise 72.3 to 78.1; Serdyuk: one noise type).
- A condition label as plain input is weaker than a condition used to select
  parameters (Amazon), or as a target (Prasad: clean unchanged, noisy
  better).
- Removing the condition (adversarial) trades clean accuracy for noisy
  accuracy and its benefit vanishes with full coverage (Serdyuk), though a
  production transducer showed a steady 1.4 to 3.9% (Amazon).
- No arm uses a large pretrained encoder. Whisper-style prompt or tag
  conditioning on acoustic condition, and audio-LLM conditioning on a
  condition description, were searched for twice and no paper was found; the
  nearest are a patent that conditions an E2E recognizer on a key-phrase
  sound embedding (not a paper, not read), a plug-and-play enhancer for audio
  LLMs, and DGSNA, which uses text descriptions to generate noise for
  augmentation (all from search summaries).

## Search record (third pass)

Queries: noise-aware, environment and acoustic-condition embeddings,
SNR-aware, device embedding, microphone or channel ID, auxiliary noise-type
targets, domain-adversarial training, device tokens, Whisper and audio-LLM
condition prompts. Forward citations of Seltzer 2013 (724 citers) gave
Shinohara's adversarial multitask (not fetched), an overview of
environmentally robust recognition, Whisper-AT and Robust wav2vec 2.0 (read),
and two 2025 to 2026 noise-floor/disentanglement papers, one read (Lin 2026).
Still unexplored after this effort: an augmentation-only vs
augmentation-plus-condition arm for a pretrained encoder, and an estimated
(not given) device or bandwidth flag. Searched and found nothing: Whisper
or audio-LLM acoustic-condition prompting.
