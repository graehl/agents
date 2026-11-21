**Source:** *Improving DNN Bluetooth Narrowband Acoustic Models by Cross-Bandwidth and Cross-Lingual Initialization* — [PDF](https://www.isca-archive.org/interspeech_2017/zhuang17_interspeech.pdf)

# zhuang2017-bluetooth-narrowband

2026-11-21, sonnet-5.5. Purpose: band-limited wideband copies as training
data for narrowband Bluetooth speech in newer, lower-resource languages.
Read: abstract, introduction, setup, baselines and cross-bandwidth results.

**Claims.** Apple, hybrid DNNs, four languages (Dutch, Brazilian Portuguese,
Thai, Turkish), about 4 h narrowband Bluetooth test sets. Users mostly speak
to assistants through wideband microphones; "a small fraction of usage
happens over narrowband (8 kHz) Bluetooth headsets" (no number given;
[extract](../extract/zhuang2017-bluetooth-narrowband/zhuang2017-bluetooth-narrowband.md):50).
Baselines (Table 1): trained on band-limited wideband data (400 to 600 h)
WER 25.7 / 33.0 / 38.9 / 42.8; trained on real Bluetooth data (50 to 260 h)
24.0 / 26.1 / 29.8 / 38.4. Initializing from the band-limited wideband
network and retraining on narrowband (cross-bandwidth, CB1) with only 20 h
of Bluetooth data gives 17.4 / 23.5 / 20.7 / 29.8 and with all data 16.4 /
22.4 / 23.3 / 29.1 (Table 2); the abstract reports up to 45% relative WER
reduction including cross-lingual initialization, and that 20 h of in-domain
data with the recipe beats baselines trained on all of it.

**Means for us.** Band-limited copies of wideband data work as a stand-in
(within 1.7 to 9.1 WER points of real narrowband data), and as initialization
they beat training on the small real set alone, in lower-resource languages,
on a phone-adjacent path. Sequence training with lattices from the wideband
model contributed (CB1 and CB3 beat cross-entropy only CB2).

**Not shown.** Neural end-to-end or pretrained encoders; mixing shares
within one training run (it is transfer, not mixing); clean wideband cost;
comparison with masking-style augmentation.
