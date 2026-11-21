**Source:** *Enhanced ASR Robustness to Packet Loss with a Front-End Adaptation Network* — [HTML](https://arxiv.org/html/2406.18928v1) · [arXiv](https://arxiv.org/abs/2406.18928v1)

# dissen2024-packet-loss

2026-11-21, sonnet-5.5. Purpose: codec/transmission-damage restoration and a
front end trained against a frozen large recognizer's loss. Read: abstract,
method, evaluation and result tables.

**Claims.** A small network between the log-mel spectrogram and a frozen
Whisper is trained on LibriSpeech (960 h) with Whisper's cross-entropy plus
an L1 restoration loss, against simulated packet loss. Packet-loss
challenge blind set WER: Whisper base 24.0 to 18.1%; large-v2 15.4 to
14.2%; a standalone packet-loss concealer (tPLCnet) gave 20.4% (base) and
worse than baseline, 16.2%, on large-v2
([extract](../extract/dissen2024-packet-loss/html/2406.18928v1.md):104-110).
Recognition-loss-trained variants beat L1-only; the combination is best
(lines 98-102). Large Whisper degrades only above about 20% loss rate;
base degrades immediately. Held-out Fleurs languages show the same
pattern, with a slight loss at zero packet loss (line 310).

**Means for us.** For a defect the recognizer was not trained to hide,
a front end trained through the frozen recognizer's loss helps, most for
the small model. Training signal, not audio-quality metrics, is what made
the difference (CE beat L1). Strongest on the small recognizer, as the
large one is already robust to moderate loss.

**Not shown.** Real codec artifacts other than simulated frame loss;
noise or reverberation; low-resource language training of the front end
(trained on English only); a comparison with simply training or
augmenting the recognizer with packet loss.
