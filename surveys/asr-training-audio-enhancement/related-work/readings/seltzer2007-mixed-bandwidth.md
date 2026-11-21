**Source:** *Training wideband acoustic models using mixed-bandwidth training data for speech recognition* — [PDF](https://microsoft.com/en-us/research/wp-content/uploads/2007/01/2007-mseltzer-taslp.pdf)

# seltzer2007-mixed-bandwidth

2026-11-21, sonnet-5.5. Purpose: earliest located principled treatment of
training with mixed narrowband and wideband data (GMM-HMM era). Read:
abstract, introduction, experiments A-C, conclusion.

**Claims.** An EM algorithm trains a wideband HMM from a small amount of
wideband speech plus a larger amount of narrowband speech by treating the
missing 4-8 kHz band as missing data. WSJ0 20 k test, about 12 h of
parallel wideband and telephone-band speech, HTK triphones. The full
wideband upper bound is 10.4% WER
([extract](../extract/seltzer2007-mixed-bandwidth/seltzer2007-mixed-bandwidth.md):320).
With only 20% / 10% of the data wideband and the rest narrowband the method
reaches 13.3 / 13.9% against a front-end imputation method (FBE) at 13.5 /
18.3% (Table I, lines 348-353). It beats both a wideband recognizer trained
on the limited wideband data alone and a fully trained narrowband
recognizer at every wideband percentage tested (lines 338-340); a
narrowband-only system is best if under about 20% of the data is wideband
under conventional training (line 367).

**Means for us.** The lower-resource motivation is stated explicitly: collect
cheap telephone data, add a little wideband. The method is specific to
Gaussian-mixture models; neural recipes later replace it by pooling and a
condition flag (Mantena 2019) or by transfer (Zhuang 2017).

**Not shown.** Neural acoustic models; real (non-parallel) telephone
speech; the test is wideband speech, not narrowband deployment.
