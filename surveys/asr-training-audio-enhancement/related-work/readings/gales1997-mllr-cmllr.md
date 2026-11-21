**Source:** *Maximum likelihood linear transformations for HMM-based speech recognition* — [PDF](https://mi.eng.cam.ac.uk/reports/svr-ftp/auto-pdf/gales_tr291.pdf)

# gales1997-mllr-cmllr

2026-11-21, sonnet-5.5. Purpose: the primary text for the MLLR and
constrained (feature-space, CMLLR) transform family and its unsupervised use
from a first-pass transcript. This is the Cambridge technical report that
precedes the 1998 journal article (Computer Speech and Language 12(2)); I
did not read the journal version. Read: abstract, introduction, section 2
outline, section 5 experiments.

**Claims.** Model-space linear transforms estimated by maximum likelihood on
adaptation data, for speaker and environment adaptation of an HMM
recognizer: unconstrained (any mean and variance transform) vs constrained
(variance transform tied to the mean transform, equivalent to a
feature-space transform); full and block-diagonal forms; use in speaker
adaptive training. Incremental adaptation, WER % (unadapted / constrained
diag / block / unconstrained diag / block), HUB1 dev 9.57 / 8.47 / 8.14 /
8.61 / 8.06; HUB1 eval 9.20 / 8.48 / 7.75 / 8.48 / 8.13; S5 (unknown
microphone, 5k words) 9.00 / 7.99 / 7.62 / 7.93 / 7.15
([extract](../extract/gales1997-mllr-cmllr/gales1997-mllr-cmllr.md):305-320).
Block-diagonal transforms gave consistently better results than diagonal
(line 322). Static unsupervised adaptation used the speaker-independent
recognizer's own transcripts (section 5.3, lines 330-345): HUB1 dev / eval
8.49-9.07 / 7.73-8.30 depending on form.

**Means for us.** The original evidence that a transform fitted from a
first-pass transcript helps an unknown-microphone condition (S5: 9.00 to
7.15, 21% relative) as well as speakers, in a hybrid GMM system.

**Not shown.** Confidence weighting (later work); neural recognizers; the
variance-transform results in detail (not read).
