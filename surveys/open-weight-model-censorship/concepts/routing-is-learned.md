# routing-is-learned: detection, routing, output

**Source:** Gregory N. Frank, *Detection Is Cheap, Routing Is Learned:
Why Refusal-Based Alignment Evaluation Fails*, arXiv 2026 —
[HTML](https://arxiv.org/html/2603.18280) ·
[PDF](https://arxiv.org/pdf/2603.18280). Extract:
`related-work/extract/frank2026-routing-learned/`. Read through §4.1.

**Claim.** In Chinese-lab models, post-training installs a *routing*
policy over knowledge the model keeps: refuse, recite, steer, or answer.
Linear detection of "politically sensitive" is trivial. With 48 samples
in 4,096 dimensions, a ridge probe separates even random labels at 100%
on its training set. The informative test is held-out-category
cross-validation: train on five sensitive categories, test on the sixth.
Every tested model passes it at 94–100%.

**Evidence most useful to us:**
- Matched pairs (Tiananmen–Kent State, Xinjiang–Japanese internment,
  Tibet–Western Sahara) give a topic-conditional gap. Every model scores
  about 1.0 (neutral) on the Western parallels.
- Qwen3.5-4B and 9B refuse 0% and score 5.0 of 5 on CCP steering for
  Chinese prompts. Qwen2.5-7B shows 94% propaganda framing (human-coded,
  128 items, κ = 0.79 for propaganda).
- Language-conditioned routing. GLM-Z1-9B answers all 32 English
  prompts accurately and refuses Tiananmen, censorship and Hong Kong in
  Chinese.
- Ablating a political direction (CCP minus matched control, 24+24
  prompts) removes refusal in four models. Three answer accurately.
  Qwen3-8B instead confabulates in 72% of responses, substituting Pearl
  Harbor for Tiananmen: its sensitivity direction is entangled with the
  facts. Eighteen negative-control directions change refusal by at most
  8.3 pp.
- Directions do not transfer across models (Qwen3-8B to GLM-4-9B cosine
  0.004).
- Small-sample warning: an n=8 behavioural screen gave large spurious
  effects that vanished at n=32.
- Gemini as judge flagged 45% of ablated responses as evasive, against
  16% for a human rater.

**Limits.** Small, hand-built corpora (24, 32 and 16 prompts). The
steering scores come from a single LLM judge. Some ablation-alpha
leakage on one Tiananmen sweep is disclosed and reported fixed in an
appendix. Company author.

**Relation to the program.** It supports claim 1 (probing for listed
topics is easy) with a caveat: only held-out generalization and causal
ablation are diagnostic, never probe accuracy. It also warns that
direct repair by ablation can destroy facts in Qwen specifically. See
[refusal-direction-removal](refusal-direction-removal.md).
