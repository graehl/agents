# Sorting can change optimization despite shuffled batch order

[Morishita et al., First Workshop on Neural Machine Translation, 2017](https://ar5iv.labs.arxiv.org/html/1706.05765).
[Local extract](../related-work/extract/morishita2017-minibatches/html/1706.05765.md).

The paper compares source-length, target-length and two-key sorting against
random shuffling, across batch sizes, sentence/token batch definitions,
and Adam/SGD. Every setting shuffles batch order. Target-length grouping
can therefore hurt convergence even after the obvious sorted-curriculum
problem is removed.

Effectiveness: **single-source**, with a second toolkit check by the same
authors. In their recurrent NMT experiments, Adam favors random or
source-length ordering over target-length sorting, while SGD is less
sensitive. Faster corpus throughput does not imply faster convergence.
This is evidence for measuring composition, not a proof that present-day
transformers need independent logical-step row draws.

The authors suggest shuffled local sorting as a possible compromise but
explicitly leave its empirical evaluation out of scope. The paper does
not validate arbitrary weights or a complete multi-stream sampler.
