# Combining words from modern ASR outputs

Grounded focused search, 2026-10-05. Scope: recombining transcripts from
multiple recognizers into a new transcript, rather than selecting an intact
candidate. Anchors: ROVER, confusion networks, Hystoc; contemporary checks:
NTT CHiME-8 and ILENIA_VOZ. OpenAlex and primary publisher/arXiv sources were
queried. Published results below have not been reproduced locally; the search
did not reach saturation. Corpus hours are available for the main studies;
utterance counts and fusion-only runtimes are not established here.

## Confidence-weighted word voting has direct modern evidence

ROVER aligns hypotheses into word slots, including an empty alternative for
insertions/deletions, then chooses a word in each slot by votes and confidence.
Its output may occur in none of the input hypotheses. It accommodates different
tokenizers and architectures after common word tokenization. It can destroy
dependencies across slots; a plausible local winner need not form a good
sentence with its neighbors.

[Hystoc, Beneš, Kocour and Burget, ICASSP 2024](https://arxiv.org/html/2305.12579v1)
([full local extract](../related-work/extract/benes2024hystoc/html/2305.12579v1.md))
supplies word confidences to ordinary ROVER from scored n-best hypotheses.
It aligns hypotheses in decreasing score order, adds their temperature-scaled
probability mass to confusion-network arcs and normalizes each slot. This
avoids requiring a shared model vocabulary or native word posterior output.

Table 2 reports Spanish RTVE2020 results with two XLS-R/Conformer systems,
a CRDNN RNN-T and a Kaldi CNN/TDNN-f system. Best individual WER is 17.3
without external LM rescoring; four-system confidence-free ROVER gives 16.1,
and Hystoc-confidence ROVER gives 15.9. With rescoring, the corresponding
numbers are 16.7, 15.8 and 15.3. This is benchmark-reported evidence for actual
recombination. The 39-hour set also served acoustic-model cross-validation;
do not describe this as a clean final blind-test result. The strongest
combination includes a hybrid recognizer; the two-Conformer no-LM comparison
still improves 17.3 to 16.8 with confidence, while plain voting gives 17.4.

## Diversity helps, but pooling every candidate can hurt

Hystoc's direct multi-system n-best fusion is a valuable negative result.
For all four systems without an LM, raw pooling yields 21.6 WER and
per-system normalized pooling 19.6, both worse than the best individual 17.3.
The paper links this to poorly calibrated RNN-T confidences, without claiming
to have isolated the cause. Per-model normalization is insufficient by itself.
ROVER using each system's first-best plus its word confidences is the better
supported starting point. Hystoc's suggestion to restrict hypothesis switching
to disagreement regions is future work, not a demonstrated improvement.

[NTT CHiME-8, Kamo et al., 2025](https://arxiv.org/html/2502.09859v2)
provides a more recent cross-architecture case: Whisper large-v3 and medium,
NeMo transducer, and WavLM transducer, with training variants and LM-rescored
versions. Appendix A.3 Table 10 reports best single-system macro tcpWER
16.89 versus 15.25 for combination on development audio with oracle
diarization and fixed enhancement. The fusion also includes LM rescoring;
the entire 1.64-point difference is not isolated ROVER gain. Table 12's
separate experiment changes ROVER inputs from original hypotheses (19.91)
to original plus rescored hypotheses (19.74). These are different conditions
from Table 10 and cannot be subtracted across tables. Evidence is
benchmark-reported, with no Arabic or same-lineage-model guarantee.

The full HTML was downloaded, but the local Markdown derivation failed its
fidelity check (6 of 282 blocks); no accepted extract is claimed. The relevant
tables and method were read from the primary HTML. This does not block using
the source, but the manifest deliberately retains `grounded: false` until a
complete local extraction passes.

## Learned fusion needs its own correction control

Multi-input sequence-to-sequence correction can construct a new transcript,
but a stronger text model can improve a single input too. It is a distinct
experiment from word recombination. A fair contrast gives the same corrector
one candidate versus several, with matched training and compute, and measures
unsupported substitutions, numbers, names and dialect rewriting.

Two follow-up leads were verified at bibliographic/abstract level, not used
for a quantitative claim:

- [ILENIA_VOZ, Messaoudi et al., IberSPEECH 2024](https://www.isca-archive.org/iberspeech_2024/messaoudi24_iberspeech.html):
  Whisper/Conformer-Transducer ROVER in the Albayzin challenge; inspect each
  submitted mixture before assuming adding systems helps.
- [Imai, Chowdhury and Stent, COLING 2025](https://aclanthology.org/2025.coling-main.336/):
  diverse conversational datasets, ASR ensembling and error correction.
  Retrieve its full tables before ranking learned correction against ROVER.

## Smallest useful Arabic experiment

Use the saved aligned greedy outputs to compare intact-sequence selection,
unweighted ROVER and confidence-weighted ROVER. Keep system weights distinct
from hypothesis posterior weights, so one model cannot receive extra votes
just by emitting more n-best entries. Use only training/tuning data for
confidence calibration; avoid fitting dozens of weights on the small fixed dev.

For a second stage, derive word confidences from already available n-best
lists, checking per-model calibration. Preserve raw Arabic spelling in the
output while using the program's declared source projection for evaluation.
Inspect alignment across numbers, attached clitics and spelling variants;
normalizing only one recognizer can manufacture disagreement.

Report read/media WER and paired MAPSSWE against the best single greedy
system, plus deletion/insertion changes, hybrid-output fraction and latency.
Measure the oracle of the exact constructed confusion network as well as the
whole-candidate oracle: the graph may create useful new paths or lose the
reference through bad alignment. Neither oracle is deployable quality.
If word voting creates incoherent transitions, compare a bounded switching
penalty or LM rescoring of the network, charging the extra model and compute.
That is a proposed rescue, not an established gain from these papers.

## Search trail and limits

OpenAlex resolved Hystoc to W4392902590 (2 citations) and its preprint to
W4377864521 (1 citation). Both recency and citation-count sorts were queried
for the published anchor; the results were BUT CHiME-7 and stuttering-speech
work. Counts are retrieval hints. Backward references supplied ROVER,
confusion-network construction and confidence-estimation alternatives;
targeted searches used system combination, hypothesis fusion, ROVER,
Whisper/transducer and learned error correction. NTT, BUT and the Albayzin
teams are useful continuation anchors. The main disconfirming evidence is
Hystoc's direct-fusion failure and the need to separate LM improvement in NTT.
No claim is made that every modern fusion family has been covered, or that
negative MT confusion-network results transfer to monotone ASR.
