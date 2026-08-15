# GEPA — reflective prompt evolution

Read method: prompted extraction over the arXiv HTML full text, 2026-08-15.
Full text: [HTML](https://arxiv.org/html/2507.19457) ·
[PDF](https://arxiv.org/pdf/2507.19457) ·
[local extract](../related-work/extract/gepa2025/html/2507.19457.html)
(git-ignored; rebuild with `related-work fetch`).
arXiv 2507.19457; ICLR 2026 oral.

**What it is.** Evolutionary prompt optimization for compound AI systems
(one or more LLM-prompt modules, control flow frozen). Shown (current
prompt, trajectory, score, feedback), an LLM "reflectively attribute[s]
successes or failures to prompt elements and propose[s] revised
instructions"; candidates are kept on an instance-level Pareto frontier
(best score on at least one training instance) and sampled by how many
instances they lead.

**Results.** Reported: outperforms GRPO by ~6% average (up to 20%) with up
to 35× fewer rollouts; MIPROv2 by >10%. Cross-model transfer measured post
hoc: prompts optimized on Qwen3-8B transfer to GPT-4.1-Mini (+9%).

**Relation to the diagnosis program.** Corrects this survey's earlier
recall-mode characterization ("mutates without attributing"): GEPA's
reflection is element-level cause attribution, then rewrite. Remaining
differences: signal (own-trajectory outcome metric vs cross-model
divergence under one corpus), object (per-system prompts vs a shared
maintained corpus with model-scoped supplements), checkability (freeform
lessons vs chapter-and-verse citations checkable against read traces), and
validation (score climb vs pre-registered ablation). Also a candidate
component: GEPA-style reflection could draft stage-4 patch text.
