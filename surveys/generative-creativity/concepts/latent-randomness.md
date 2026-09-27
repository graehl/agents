# Continuous random prefixes as a separate exploration source

Long et al., *Reasoning Palette* (December 2025).
[Full text](https://arxiv.org/html/2512.17206v1) ·
[local extract](../related-work/extract/long2025-reasoning-palette/html/2512.17206v1.md).
Read: methods §§3.2–3.4 and inference evaluation §4.1.

A variational autoencoder maps Gaussian latent samples into continuous prefix
embeddings. The language model attends to those prefixes; brief supervised
adaptation makes it responsive to the channel. Changing the latent can vary
outputs even with greedy decoding. The paper includes a single-prefix case;
the sampled values are not vocabulary tokens or printable random strings.

**Effectiveness: single-source.** Qwen-based reasoning and visual-grounding
experiments compare latent prefixes with ordinary decoding. Interpretation
needs care: §4.1 calls its intervention Gaussian noise but explicitly uses
the learned decoder D(z). It does not establish that arbitrary raw Gaussian
embedding noise works equally well. The authors also report format failures
in the visual greedy baseline and warn that excessive supervised adaptation
can wash out latent sensitivity. Pass@k gains do not establish creative quality.

Prefix length controls intervention size. During reinforcement learning,
two-phase or linear schedules reduce the fraction of guided rollouts. These
are training-progress controls, not a learned gate conditioned on the current
generation state. A persistent random prefix and a fresh per-step stochastic
channel therefore remain different mechanisms. This paper directly precedes
the former; this pass has not verified an exact match for the latter.
