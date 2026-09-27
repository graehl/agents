# Shuffled windows and alternated sorting

[Doetsch, Golik and Ney, 2017, full text](https://ar5iv.labs.arxiv.org/html/1705.02414).
[Local extract](../related-work/extract/doetsch2017-alternating/html/1705.02414.md).
ArXiv metadata says “comprehensive study”; the full-text heading says
“comparative study.” Both identify arXiv:1705.02414.

Shuffle the epoch, split it into equal-sized bins, sort alternate bins in
opposite length directions, and cut consecutive physical batches. Larger
bins permit closer length matching. Alternating directions reduces length
jumps when a physical batch crosses a bin boundary. This is a direct
published predecessor of bounded shuffled-window sorting.

Effectiveness: **single-source** on CHiME-4 recurrent acoustic modeling.
The reported progression goes from 7.0 utterances/s and 8.9% word error
for random ordering to 10.2 utterances/s and 10.2% error for full sorting.
The 256-bin variant reports 8.8 utterances/s and 9.1% error. Thus the paper
demonstrates a real tradeoff rather than a universal free speedup. Its MXNet
bucketing baseline and proposed implementation use different frameworks,
which limits attribution of their runtime difference to batching alone.

A bounded-window implementation can emit early without constructing all
physical batches for the epoch. That streaming adaptation and weighted
input draws are straightforward compositions, not demonstrated features of
the published algorithm. Alternating sorted runs also do not themselves
guarantee representative length mixtures within optimizer steps.

Do not reuse the paper's stated pair-in-bin probability as a theorem: for
M items uniformly partitioned into bins of size m, the conditional chance
that another fixed item shares the first item's bin is `(m-1)/(M-1)`.
