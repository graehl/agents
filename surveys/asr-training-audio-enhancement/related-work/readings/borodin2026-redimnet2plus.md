**Source:** *ReDimNet2+: Multi-Corpus Data Scaling for Robust Speaker Verification* — [HTML](https://arxiv.org/html/2609.37014) · [arXiv](https://arxiv.org/abs/2609.37014)

# borodin2026-redimnet2plus

2026-11-21, sonnet-5.5. Purpose: an adjacent-field (speaker verification)
recipe with explicit codec and band-limit augmentation shares. Read:
abstract, data analysis, pipeline (3.1), Table 1 and discussion.

**Claims.** Training policy per example: keep 0.5, codec only 0.2, waveform
augmentation only 0.2, both 0.1, so 30% of examples receive a codec. Codec
presets include MP3, Opus, AAC, Vorbis, G.723.1, IMA ADPCM, G.722, A-law,
mu-law, Speex and AMR-NB, several at 8 and 16 kHz; the waveform branch adds
band-pass, band-stop, high-pass and low-pass filters, noise, room
impulse responses and speed perturbation; SpecAugment and CutMix follow
with probability 0.2
([extract](../extract/borodin2026-redimnet2plus/html/2609.37014.md):91).
Development path (4-second windows, EER %): public ReDimNet2 baseline
pooled VoxCeleb1 2.42 and a 26-condition codec/waveform stress test 7.214;
final ReDimNet2+ 0.824 and 1.991 (Table 1, line 159). The first step,
fine-tuning on VoxBlink2 alone, improved the stress test (5.599) but worsened
clean VoxCeleb1 (3.408 pooled), which the authors read as a difficult
adaptation (line 185).

**Means for us.** A concrete, recent codec-augmentation recipe with
shares, but the steps change data, windows, epochs and fine-tuning together,
so no number isolates the codec augmentation or its cost on clean audio.
Speaker verification, not recognition.

**Not shown.** An augmentation on/off ablation; ASR.
