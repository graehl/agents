# r1dacted: local censorship in DeepSeek-R1

**Source:** Naseh, Chaudhari, Roh, Wu, Oprea, Houmansadr, *R1dacted:
Investigating Local Censorship in DeepSeek's R1 Language Model*, arXiv
2025 — [PDF](https://arxiv.org/pdf/2505.12625) ·
[arXiv](https://arxiv.org/abs/2505.12625). Extract:
`related-work/extract/naseh2025-r1dacted/`. Read in full.

**What it establishes.** DeepSeek-R1 censors China-sensitive topics in
the released weights, run locally, not only in DeepSeek's app. The paper
calls this "local censorship": censorship particular to one model, as
opposed to the "global" safety refusals all models share. Censored
outputs skip reasoning (`<think> </think>`). They then give a templated
pro-government answer (97.3%) or an explicit refusal (2.7%).

**Method worth reusing.** Candidate prompts came from Reddit, Twitter
and GPT-4o around 96 categories derived from the China Digital Times 404
archive. Any prompt that o3-mini-high, GPT-4o or Llama-3-8B-Instruct
refused was dropped, which removes global safety refusals. Only prompts
R1 then censored were kept (10,030). The existing promptfoo set
(1,156 prompts) was rejected because o3-mini-high refused about 83% of
it.

**Numbers** (GPT-4.1 classifier):
- On a balanced 2,880-prompt set (30 per category), 66 of 96 categories
  are censored 100% and 86 of 96 above 90%. The lowest are the Dalai Lama
  (77%), the Lei Yang case (73%) and the Great Leap Forward (67%).
- Translated prompts: Chinese 99.6%, Korean 81.3%, Farsi 61.2%.
- DeepSeek's six R1 distills (Qwen 1.5B–32B, Llama 8B/70B): 0.15–0.30%.
  Most residual cases are Tiananmen.
- DeepSeek-V3 via Azure: 12.9% template, 0.5% refusal.
- QwQ-32B locally: 13 refusals in 10,030. Qwen's web chatbot is
  "significantly stricter" (qualitative).
- Summarizing or translating 1,965 censored CDT-404 articles and 55
  sensitive Wikipedia pages: "no evidence of censorship behavior". The
  classifier targets refusal and template answers; omission and
  softening were not scored.
- Planting: 30 censored Taiwan examples in a 1k-sample distillation set
  for Qwen2.5-7B give 95.5% censorship on held-out Taiwan prompts and
  spill over to other categories, at unchanged AIME, GPQA and MATH.
  Fixed refusal targets plant more efficiently (98.5% with 10 examples).
- Bypass: prefilling "Okay, the user is asking" inside `<think>`
  recovers 97.86% of answers.
- R1-1776 on the same 10,030 prompts: 0 censored. Pairwise factuality
  judges preferred R1's jailbroken answers to R1-1776's (GPT-4.1 58%,
  o3 62.5% of 600 pairs).

**Limits.** All prompts are English questions selected *because* R1
censored them, so per-model rates are inflated by construction. One
classifier (GPT-4.1) scores everything; no human agreement is reported.
The task test has no reference outputs.

**Relations.** It anchors the
[faithful-task null](faithful-task-audits.md) and the
[hosted/local split](hosted-filters.md). Removal comparisons are in
[refusal-direction-removal](refusal-direction-removal.md).
