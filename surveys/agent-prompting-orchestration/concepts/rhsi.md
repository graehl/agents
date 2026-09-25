# RHI — Recursive Harness Self-Improvement (per-task, pairwise, prompt-level)

Read method: full read of the saved source HTML (converted locally; committed
extract pending a fidelity-gate failure), 2026-09-25. The harness examples,
optimizer prompt, evaluator criteria, and evaluator prompt are image figures
in the HTML and were not readable.
Full text: [HTML](https://arxiv.org/html/2607.15524) ·
[PDF](https://arxiv.org/pdf/2607.15524) ·
[saved HTML](../related-work/extract/rhsi2026/html/2607.15524.html).
arXiv 2607.15524v1 (cs.LG, 17 Jul 2026). Hyunin Lee, Jinglue Xu, Jeffrey
Seely, Donghyun Lee, Matei Zaharia, Yujin Tang (Sakana AI / UC Berkeley).
Preprint; no venue stated. The paper's own acronym is RHI.

**What it is.** The harness is a textual multi-agent specification added to
the task prompt of a black-box coding agent (Claude Code). It lists roles,
instructions, *contracts* (what each subagent returns to the orchestrator),
*hops* (workflow steps), and accreted "auxiliary rules" such as acceptance
gates and fallbacks. Each iteration makes one new agent run on the task. One
LLM pairwise judgment compares it against the previous iteration's cached
output, and an LLM optimizer rewrites the harness from the current harness
plus the whole pairwise-preference history (a "momentum" signal). The
optimizer never sees the judging rubric. The loop stops when the fraction
of tasks improved falls below ε. Cost per iteration is Θ(1): one rollout and
one judgment, versus Θ(m²) for population search.

**Anti-overfitting / generalization evidence.** None, by design. The harness
is evolved separately for each of the 30 tasks and evaluated on that same
task. There is no held-out task, suite, or split. Specialization to the
instance is the stated goal (like TTHE's test-time adaptation). The stability
argument (consecutive-harness cosine 0.82, then 0.97–0.99) shows convergence,
not generalization. The within-domain similarity rise shows shared domain
structure only in embedding space. The cost figures cover the final
harness's run and appear to exclude the i earlier rollouts and judgments
spent getting there. The comparison is therefore at matched *deployment*
cost, not matched *total* compute.

**Evidence and regime.**
- 30 LLM-synthesized "ML research" tasks (10 each for quant finance,
  robotics, and pharma), generated from three job postings. Each produces a
  repository with standard deliverables. Judged pairwise by GPT-5.5 (max)
  and Opus 4.7/4.8 (xhigh), each with 3 evaluator seeds (mean ± std). No
  agent-rollout replication is reported.
- Sonnet 4.6-high + H[2] beats Sonnet 4.6-max on 20/30 tasks. Opus 4.7-high
  + H[1] beats xhigh and max. Opus 4.8-high + H[2] beats xhigh, max, and
  ultracode (the built-in multi-subagent mode).
- Cost vs strongest same-family setting (final run only): Sonnet 2.38 vs
  2.56 (−7%); Opus 4.7 2.11 vs 2.60 (−18%); Opus 4.8 1.69 vs max 2.19
  (−23%) and vs ultracode 4.15 (−60%). Cache read/write falls 32–64%.
  Output tokens are flat for Sonnet (1.71–1.86×) and Opus 4.8 (1.42–1.81×).
  The Opus 4.7 result is confounded, because tokens rise with score.
- Sonnet + RHI does not close the gap to Opus 4.7 (§6.1).
- The mechanism claim (contracts and hops gain task information while
  cross-component redundancy falls) is embedding-proxy evidence. The
  authors call it correlational, and the optimizer prompt tells the model
  to edit exactly those components.
- Appendix A: default multi-agent mode loses to single-agent at higher
  cost; a hand-written multi-agent H[0] beats the same roles run
  single-agent.
- Risks: the judge shares a family with the agent (Opus judging Opus). The
  iteration shown per model varies. No CIs over tasks. Grade:
  `single-source`.

**Bearing on RRSI and on memorization.** RRSI's name and "recursive
self-improvement" framing descend from this line. RRSI inherits an
evolution-history signal (RHI's preference history), then adds what RHI
lacks: a held-out suite, a noise-band floor, and leakage and cost
constraints. RHI is the clearest instance of the failure RRSI names. Its
gains are fit to the task they are measured on, by construction, and they
cannot be told apart from memorizing that task or from buying compute
across iterations. Its single noisy judgment per step also has no noise
floor. RRSI's noise-band acceptance fixes exactly that, so RHI shows what
RRSI's calibration buys. RHI provides no evidence either way on whether a
harness learned on past tasks carries a reusable mechanism.

**Relation to a practitioner-maintained instruction corpus.** RHI's object
is the closest to this repo's: a natural-language harness in the prompt,
with no code. Its "auxiliary rules" (acceptance gates, fallback rules,
recall triggers) resemble incident-driven clauses. But RHI discards them
per task and never attributes a win to any clause. The repo's approach
differs on each axis RHI leaves open. It keeps a persistent cross-task
corpus instead of per-task specialization. It uses an append-only evidence
ledger instead of an opaque preference history. It pre-registers patch
hypotheses instead of free rewrites. It plans a same-model rerun noise
floor, where RHI trusts a single judgment. RHI's cost framing is a useful
caution. Report total adaptation compute alongside deployment cost, or
per-instance tuning looks free.
