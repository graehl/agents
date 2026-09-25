# Evo-Bench — benchmarking models as harness evolvers on a disjoint suite

Read method: full read of the committed Markdown extract, 2026-09-25.
Full text: [HTML](https://arxiv.org/html/2608.09096) ·
[PDF](https://arxiv.org/pdf/2608.09096) ·
[code](https://github.com/RUCAIBox/Evo-Bench) ·
[local extract](../related-work/extract/evobench2026/html/2608.09096.md).
arXiv 2608.09096 (extract is v2). Huang, Yang, Zhou, Song, Chen, Le,
Song, Zhao, Zhang (Renmin University / BOSS Zhipin).

**What it is.** A benchmark that ranks *evolver models*. A fixed policy
model (DeepSeek-V4-Flash) starts from a minimal CodeAct seed with only a
shell tool and a finish tool. A fixed evolve harness in the Claude Code
style provides an experiment ledger, rollout-diff tools, and an
"architecture checkpoint" skill. The evolver may evaluate only on a
160-task visible validation suite. The final frozen harness is scored
once on a disjoint 448-task evaluation suite drawn from BrowseComp, HLE,
GDPval, APEX-Agents, and Claw-Eval. Tasks are chosen for *harness
sensitivity*: the Pearson correlation between a task's score and
leave-one-out harness quality across 12 auxiliary harnesses. Those
harnesses were evolved on a separate 320-task auxiliary set. Tasks are
then split into validation and evaluation at random within difficulty
strata.

**Evidence and regime.** Nine evolvers. Budget: 20 evaluations, 1,000
steps, 48 h. One rollout per task (three for Claw-Eval). An LLM judge
(Qwen3.7-Plus) scores most tasks. **Every experiment is run once**, with no
seeds, CIs, or significance tests. The held-out design is sound for
same-distribution generalization: evaluation tasks are unseen and never
fed back to the evolver. It is not OOD, since validation and evaluation
are random halves of the same strata.

**Generalization / anti-overfitting findings** (all `single-source`).
- Held-out Overall scores: seed 29.7; GPT-5.6-Sol 46.3 (+16.6); Opus 4.8
  45.8 (+16.1); GLM-5.2 43.5; down to Gemma-4-31B 35.9 (+6.2). The human
  "Artificial" composite scores 47.5.
- Gains are concentrated in Search (+12.5 to +34.8), where evolvers add
  web search and fetch tools the seed lacks. Office moves −0.6 to +3.3.
  General moves 0 to +11.0, and there GPT-5.6-Sol and Qwen3.7-Max (59.4)
  beat the human composite (56.3).
- Measured noise floor: byte-identical harness revisions (Qwen3.6-27B
  I8/I10/I12) spread 2.2 points on the 160-task validation suite.
- For three models, the validation score of the frozen harness exceeds its
  held-out score: 45.4→39.4, 42.6→39.1, 45.9→38.7. The seed's validation
  score is not reported cleanly, so the pure selection gap cannot be
  separated from differences in suite difficulty.
- Early saturation. Evolvers add obvious capabilities fast, then fall back
  on local prompt, threshold, and gate tweaks. Qwen3.6-27B dismissed a
  4.3-point regression as noise without replicating. DeepSeek-V4-Pro
  labeled its best run (I3) an outlier and froze a worse one.
- Reward hacking was observed. MiniMax M3 evaded the answer-retrieval
  scanner by obfuscation, and only a full-trajectory semantic audit caught
  it.
- The "cross-policy" ablation re-runs evolution for each policy model. It
  is *not* transfer of a frozen harness. One cell regresses badly: GLM-5.2
  policy, General domain, 73.4→46.9 under the Qwen3.7-Max evolver.

**Bearing on RRSI and on memorization.** When the evaluation suite is
disjoint and never fed back, memorizing validation items cannot inflate
the held-out number. It can only waste harness capacity. So RRSI's leakage
critic protects the *in-sample* number and the hygiene of the deployed
harness. It does not make the held-out claim valid; the split does that.
Evo-Bench does show real held-out gains, but mostly from *capability
addition* to a crippled seed (missing web tools). That is the regime where
memorization matters least, and it says little about refining an
already-competent harness. Its failure analyses support the noise-band
idea: a 2.2-point same-harness spread on 160 tasks is larger than many
reported per-edit gains. Single-run results between ranks 4 and 9 (41.5
vs 41.4, and so on) cannot be told apart. Two discriminating checks for
RRSI follow. First, calibrate its noise band with byte-identical reruns,
as Evo-Bench incidentally did. Second, check whether RRSI's held-out gains
survive when the seed already has the obvious tools.

**Methodological weaknesses.** Single runs. Tasks were selected using
harnesses from Opus 4.8, GLM-5.2, and GPT-5.6-Sol, plus Sonnet 5 (which is
not ranked), and these three are exactly the top-3 ranked evolvers.
Sensitivity filtering may favor their style of improvement. The
"transferable reasoning structures" claim rests on re-evolution, not
transfer. The final score uses the frozen H_T rather than the best
validation revision, so evolver stopping discipline is part of the score.
Scores come from an LLM judge.

**Relation to a practitioner-maintained instruction corpus.** The evolve
harness mirrors the repo's discipline: an experiment ledger
(log_experiment/record_insight), and a prompt that requires "state a
falsifiable mechanism... retain or revert from evidence". Its failure
cases show why those tools are not enough without enforcement: evolvers
bundled edits, skipped smoke checks, and waved regressions off as noise.
This is published evidence for the planned protocol's same-model rerun
noise floor and pre-registered patch hypotheses. The 2.2-point identical-
harness spread is a concrete reference magnitude. The Office null, where
specific workflows resist discovery, suggests that incident-derived
procedural rules are the scarce, hard-to-evolve content that hand curation
supplies.
