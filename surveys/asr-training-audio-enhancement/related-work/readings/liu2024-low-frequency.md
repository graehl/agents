**Source:** *How Private is Low-Frequency Speech Audio in the Wild? An Analysis of Verbal Intelligibility by Humans and Machines* — [HTML](https://arxiv.org/html/2407.13266v1) · [arXiv](https://arxiv.org/abs/2407.13266v1)

# liu2024-low-frequency

2026-11-21, sonnet-5.5. Purpose: band-limiting and neural bandwidth
extension in front of Whisper. Read: abstract, setup, sections 3.2-3.3
text; figures not inspected.

**Claims.** Whisper WER on low-sample-rate audio: about 10% (Pop-glass
mingling recordings) and 0% (VCTK read speech) at 20 kHz; above 97.5% at
300 to 800 Hz (VCTK) and above 98% at 300 to 1250 Hz (Pop-glass)
([extract](../extract/liu2024-low-frequency/html/2407.13266v1.md):78).
Neural bandwidth extension trained on in-domain data gives "a reasonable
improvement" in WER at 800 to 2000 Hz, but mostly recovers stop words
(line 111). Numbers are in figures; the text gives none.

**Means for us.** Very weak evidence: the bands tested (at most 2 kHz)
are far below telephone bandwidth (4 kHz) and the extenders were trained
on the same speaker or noise setting as the test, a deliberate privacy
attack. WER here uses a bag-of-words reduction (line 70).

**Not shown.** The 8 kHz to 16 kHz case; any non-privacy motivation;
a comparison against a recognizer trained or fine-tuned on narrowband
audio.
