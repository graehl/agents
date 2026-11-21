**Source:** *BERSting at the Screams: A Benchmark for Distanced, Emotional and Shouted Speech Recognition* — [HTML](https://arxiv.org/html/2505.00059v2) · [arXiv](https://arxiv.org/abs/2505.00059v2)

# tuttosi2025-berst

2026-11-21, sonnet-5.5. Purpose: a phone-recorded benchmark for distance
and obstruction. Read: abstract, collection, ASR benchmark tables 4-5.

**Claims.** 4,526 clips (about 3.75 h) from 98 actors recording on their
own smartphones in their homes; each phrase is recorded at 19 phone
positions (near the face, hand-covered microphone, hip, 1-2 m, other side
of the room, outside the room) and at three vocal intensities, with seven
emotion prompts. Whisper medium.en over all data: WER 31.15%; Whisper
turbo 29.55%; NeMo FastConformer transducer 40.61%; NeMo Quartznet
65.16%; wav2vec 2.0 base 960h 76.21%
([extract](../extract/tuttosi2025-berst/html/2505.00059v2.md):202-209).
Whisper medium.en by distance: near body 24.93%, 1-2 m 27.00%, other side
of room 35.02%, outside room 45.10%; shouted 39.83% vs 24.17% not shouted
(lines 211-233).

**Means for us.** A real, phone-microphone benchmark where WER roughly
doubles from near to outside-the-room, and shows large recognizers
degrading too. It measures static positions (one phone position per
recording) and not a moving microphone or events within a recording.

**Not shown.** Moving or changing distance within an utterance; transient
noise; any adaptation or augmentation result; English only; scripted
acted speech with short phrases (14 phrases).
