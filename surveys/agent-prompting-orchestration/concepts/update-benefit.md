# Harness Updating Is Not Harness Benefit — evolver vs agent capability

Read method: full read of the committed Markdown extract, 2026-09-25.
Full text: [HTML](https://arxiv.org/html/2605.30621) ·
[PDF](https://arxiv.org/pdf/2605.30621) ·
[code](https://github.com/A-EVO-Lab/a-evolve/tree/release/harness-evolution) ·
[local extract](../related-work/extract/updatebenefit2026/html/2605.30621.md).
arXiv 2605.30621 (v1). Lin, Wu, et al. (Penn State, UCSC, Amazon, and
others). 18 authors.

**What it is.** A factorial study that separates two capabilities in
harness self-evolution. *Harness-updating* is the evolver model's ability
to write useful harness edits. *Harness-benefit* is the task-solving
model's ability to profit from them. Neither is the same as base
capability. The authors cross seven evolvers with six agents on a fixed
solve→evolve loop, using a fixed evolver prompt ("prefer concise, reusable
updates over task-specific patches"). The evolver sees trajectories,
scores, and grader feedback. It may edit skills (SWE-bench Verified,
SkillsBench) or also the prompt and append-only memory (MCP-Atlas). Tools
and evaluation files are read-only.

**Evidence and regime.** SWE-bench Verified (500 tasks, 12 repos),
MCP-Atlas (500), SkillsBench (86; score averaged over 5 trials, starting
from an *empty* skill set). The models are Opus 4.6, Sonnet 4.6, Haiku 4.5,
Qwen3-235B, Qwen3-32B, and GPT-OSS-120B, plus a Qwen3.5-9B evolver.
Evaluation is **in-situ (prequential)**: each task is scored under the
harness before its own evidence is used. There is **no held-out suite**:
the scored stream is also the training stream. The number of evolution
runs per cell is not stated (apparently one). No seeds, CIs, or
significance tests are reported. Adherence is measured by an LLM judge
(Sonnet 4.6, one of the studied models, with model names blinded).

**Findings** (all `single-source`).
- Evolver identity barely matters. Across the seven evolvers, harness-
  updating gain ranges only 5.9–8.2 pp on SWE, 0.6–3.6 on MCP, and
  0.7–3.8 on SkillsBench, a spread of at most 3.1 pp. No evolver wins
  everywhere. The 9B evolver tops SkillsBench (3.8 vs Opus 2.3).
- Case study: on SkillsBench flink-query, the skills written by the 9B
  evolver and by Opus describe the same five procedural steps. Either one
  lifts the Opus agent from 0.67 to 1.0.
- Benefit is non-monotonic in base capability. On SWE, Qwen3-235B gains
  +19.3 (20.7→40.0), GPT-OSS +15.8, Qwen3-32B +4.4, and Opus +2.6.
- The post-evolution score is dominated by the agent. Within one agent,
  the spread across evolvers is at most 5.1 pp on MCP, against a 36.0 pp
  gap between agents. Even the strong agent paired with its worst evolver
  beats the weak agent paired with its best by 18.6–35.2 pp.
- Weak models fail in two ways. The first is activation: skill-load rate
  is 0.25 for Qwen3-32B against about 0.96 for strong models. The second
  is adherence: the harness-following rate is 0.14 for Qwen3-32B, 0.35 for
  Qwen3-235B, and 0.76 for Opus. Phase-level adherence drifts from 0.52 to
  0.13 for Qwen3-32B and only from 0.89 to 0.80 for Opus.
- Some cells regress. On SkillsBench, the Sonnet agent drops from 24.4 to
  22.1 under three different evolvers.

**Bearing on RRSI and on memorization.** Prequential scoring rules out
literal self-memorization of a task. It does not rule out near-duplicate
transfer inside one distribution: SWE-bench tasks share 12 repositories,
so a skill learned from one Django issue can carry repo facts to the next.
A +19 pp in-stream gain is therefore uninformative about out-of-distribution
reuse. The flat evolver result says the useful edits are procedurally
simple, the kind a 9B model can transcribe from graded evidence. That
reads more like recording procedures than inventing mechanisms. For
RRSI, whose regularizers all act on the evolver side, the paper predicts
small effect sizes: evolver-side variation moves outcomes by only about
3 pp. Single-run RRSI arms with k=2 trials therefore cannot resolve
differences of that size. The paper's Δ_benefit is a maximum over three
evolvers, a winner's-curse estimator, which is the same upward selection
bias that RRSI's noise-band floor is meant to counter. A discriminating
experiment for RRSI would score the evolved harness under several agent
models. If the "regularized" edits help mainly mid-tier agents, the effect
is compensation for the agent, not a reusable mechanism.

**Methodological weaknesses.** There is no held-out or OOD split. The
benefit metric is max-over-evolvers and so biased upward. Run
multiplicity and variance are unreported. Skill-load and pass-when-loaded
rates are odd: Opus passes only 0.177 of skill-loaded runs while its
overall SkillsBench rate is 25.6–31.4%. The phase-adherence prompt defines
five phases, but only three are reported. The judge is one of the models
under study.

**Relation to a practitioner-maintained instruction corpus.** This is the
closest measured evidence that one instruction edit has model-dependent
payoff driven by activation and adherence, not by content quality. Under
the planned two-model differential diagnosis, a divergence can reflect an
adherence gap rather than an instruction defect. A pre-registered patch
hypothesis should therefore say which of the two it targets: loading,
where the rule is not in context or not routed, or following, where the
rule is present but decays over a long horizon. The paper's locked-rubric
judge is a reusable measurement for the ablation. It extracts 3–8 atomic
instructions with source spans, then assigns each a FOLLOWED or VIOLATED
verdict with the turn index. The practical rule "invest in the agent, not
the evolver" is consistent with hand curation. Who writes an instruction
matters less than whether each consuming model reliably loads and obeys it.
