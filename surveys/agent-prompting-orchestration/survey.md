# Field map: agent prompting and orchestration — instruction effects, prompt optimization, multi-model aggregation, and divergence attribution

Mode: **recall base + grounded falsification slice** (2026-08-15). The map
was built from pretrained recall (2026-01 cutoff) plus light search; the
falsification slice then read ten anchor/neighbor papers via prompted
arXiv-HTML extraction, snowballed their citers (Semantic Scholar Graph
API), and ran the reframing queries in *Disconfirming pass*. Read-backed
nodes cite `related-work/papers.yaml` keys. A second grounded slice
(2026-09-25, §J) read RRSI and nine harness-evolution neighbors in full;
three of those (Meta-Harness, RHSI, delta attribution) were read from
saved source HTML because their Markdown failed the fidelity gate
(20 manifested / 20 verified / 17 grounded / 17 extracted; 15 concept
digests, `related-work status` 2026-09-25). Effectiveness grades
remain capped at
`single-source` (each claim still rests on its own paper); `folklore`
where honest.

Coverage cutoff: literature as represented in pretraining through
2026-01, plus web search 2026-08-15 (no venue-scoped sweep). §J adds a
grounded slice through 2026-09-25: RRSI (arXiv 2609.24972) as anchor,
backward snowball over its reference list, nine further full reads; its
forward citers do not exist yet.

Created for placement of the `research/differential-instruction-diagnosis`
program (`~/agents`); see *Placement* at the end. Introspection-faithfulness
material is deliberately thin here — the sibling survey
[`surveys/llm-intelligence/survey.md`](../llm-intelligence/survey.md) owns it
(§E2 CoT unfaithfulness, §F1 introspection/self-report, §H1 concealed
cognition) and is partly `grounded`.

## Map orientation

Three axes organize the field:

- **object** — a single prompt; a structured/multi-file instruction corpus;
  a whole agent scaffold (tools + prompts + control flow);
- **mechanism** — measure instruction effects; optimize instruction text;
  aggregate multiple agents/samples; judge outputs; attribute causes of
  behavior or divergence; repair a corpus from attributed causes;
- **signal** — outcome metrics; model self-report; trajectory/transcript
  evidence.

Most published work sits at {single prompt or scaffold} × {optimize or
aggregate} × {outcome metrics}. Attribution mechanisms and
corpus-level objects are the sparse edge.

## A. Instruction-sensitivity measurement

What it is: quantifying how much and in what direction instruction wording,
framing, and structure move model/agent behavior. The problem it addresses:
single-prompt evaluations silently overfit conclusions to one wording.

- **A1 Multi-prompt evaluation.** Mizrahi et al., "State of What Art?"
  (TACL 2024, arXiv 2401.00595): across millions of instances, instruction
  paraphrases change absolute *and relative* model rankings. Previously
  verified in this repo (`topics/agent-instructions.md`, web-checked
  2026-05-29). Grade: `single-source` (recall cap; the in-repo check verified
  existence, not replication). Design consequence: any corpus conclusion must
  survive paraphrase, not one wording.
- **A2 System-prompt effects on engineering agents.** An empirical study
  isolating system-prompt detail for code generation (arXiv 2602.15228) and a
  motivation-framing study (arXiv 2603.14373: framing shifts agents from
  breadth-first scanning to depth-first investigation) — both previously
  verified in this repo (same 2026-05-29 pass). Grade: `single-source`.
  Consequence: tone and framing are live variables, so a diagnosis protocol
  must control them, not only content.
- **A3 Config- and harness-induced divergence.** Read 2026-08-15
  (`beliefdiv2026`, `agentconsistency2026`). Harness belief divergence
  (arXiv 2607.04528): six harness configs with task, model, and
  instructions held fixed — divergence comes from how each harness
  filters and gates execution feedback, not from instruction text, and is
  large (failure-mode divergence up to 0.80). Behavioral reproducibility
  (arXiv 2605.28840; 6 models × 19 tasks × 10 runs): the same-model rerun
  noise floor — tool-sequence similarity 0.87, argument consistency 0.69,
  ~60% of divergence arising in steps 1–2, task ambiguity the dominant
  driver. Grade: `single-source` each. Design consequences: hold the
  harness fixed or its effect swamps corpus attribution, and size
  cross-model divergence against the same-model rerun floor. Nearest
  confusable: A1 — A3 varies the harness/config, holding the prompt fixed.

## B. Automated prompt/instruction optimization

What it is: treating instruction text as a search space optimized against an
outcome metric. Problem addressed: hand prompt-engineering is slow and
unprincipled.

- **B1 Instruction search:** APE (Zhou et al., ~2022) and OPRO (Yang et al.,
  ~2023) — LLM proposes/rewrites instructions, scored on a task metric.
  Grade: `folklore`-to-`single-source` (recall).
- **B2 Program-level optimizers:** DSPy/MIPROv2 — jointly tune instructions
  and demonstrations across a multi-stage pipeline. Grade: `single-source`
  (recall).
- **B3 Reflective/evolutionary:** GEPA, "Reflective Prompt Evolution Can
  Outperform Reinforcement Learning" (arXiv 2507.19457; ICLR 2026 oral;
  read 2026-08-15, `gepa2025`, [digest](concepts/gepa.md)). Reflection
  attributes successes/failures to prompt elements and rewrites them;
  instance-level Pareto selection; single system, outcome-scored;
  cross-model transfer measured post hoc only (Qwen3-8B → GPT-4.1-Mini
  +9%). Reported: beats GRPO by ~6% average with up to 35× fewer rollouts,
  MIPROv2 by >10%. Grade: `single-source` (self-reported numbers).
  Related: PromptBreeder, TextGrad (recall, `folklore`).

Relation to the rest of the map: B reads *execution/evaluation traces of one
system* and mutates text to climb a metric — and B3's reflection does
attribute failures to prompt elements before rewriting. The differences
from the diagnosis program below are (i) signal: outcome metric on own
trajectories vs divergence between two heterogeneous readers of the same
corpus, (ii) checkability: freeform reflective lessons vs clause citations
checkable against read traces, and (iii) object and validation: per-system
prompts climbed by score vs a shared maintained corpus patched under a
pre-registered ablation gate.

## C. Multi-agent aggregation (the consensus foil)

What it is: sampling or debating multiple agents/models and aggregating to
one answer. Problem addressed: single-sample unreliability.

- **C1 Self-consistency** (Wang et al., ~2022): sample many chains, vote.
  Grade: `folklore` (extremely widely reproduced informally; recall cap
  applies to any specific number).
- **C2 Multi-agent debate** (Du et al., ~2023; MAD and successors; includes
  heterogeneous cross-model debate): agents exchange answers and revise
  toward consensus. Grade: `contested`-shaped in the literature, recorded
  here as `single-source` per recall cap — several later papers report
  debate ≈ self-consistency at matched compute (see *Contested results*).
- **C3 Judge panels / mixture-of-agents:** aggregate via a judge or layered
  synthesis rather than voting. Grade: `single-source` (recall).

All of C treats inter-agent *disagreement as noise to be aggregated away*.
The disagreement itself is discarded as signal — the design choice the
diagnosis program inverts.

## D. LLM-as-judge and its biases

What it is: model-graded pairwise or rubric evaluation (MT-Bench, Chatbot
Arena adjacent, G-Eval). Judges compare *outputs*; no strand known to me
attributes output differences back to clauses of a shared system corpus.
Measured judge biases (recall, `single-source` each): position bias,
verbosity bias, and **self-preference/self-recognition bias** — a judge
favoring text its own model family produced. The last is direct measured
precedent for the lab-flattery hazard in any protocol where a model
evaluates its own family's behavior against a competitor's.

## E. Self-critique and revision

- Self-Refine (Madaan et al.) and Reflexion (Shinn et al.): revision from
  self- or environment-feedback. Grade: `single-source` (recall).
- The bounding negative result: Huang et al., "LLMs Cannot Self-Correct
  Reasoning Yet" (ICLR 2024, arXiv 2310.01798; previously verified in this
  repo 2026-05-29): intrinsic self-correction without external feedback does
  not help and can hurt. Design consequence: a revision stage is only
  well-founded when driven by *external* evidence — e.g. a peer transcript —
  not by re-prompted introspection alone.

## F. Trajectory attribution, forensics, and harness repair — nearest cluster

Read 2026-08-15 (prompted arXiv-HTML extraction; keys in
`related-work/papers.yaml`):

- **SkillTriage** — "Agent Skills Can Be Harmful" (arXiv 2608.11888,
  `skilltriage2026`): contrastive target-vs-reference trajectories on one
  system (OpenCode + Claude Opus 4.6); attribution at skill-module
  granularity, 88.8% subcategory accuracy; classification only, no repair.
- **Black-box forensics** (arXiv 2606.22698, `agentforensics2026`):
  attributes which system prompt / base model powers an endpoint from
  conversations alone; prompts are opaque classification units — no
  clause-level attribution, no repair. ~97% pairwise prompt attribution on
  structurally different prompts, <80% under paraphrase; prompt
  sensitivity is model-dependent.
- **PromptExp** (arXiv 2410.13073, `promptexp2024`): token→component
  attribution (IG + perturbation) per model, two models evaluated
  separately; human-in-loop refinement (compression user study) — a weak
  repair loop, no cross-model signal, no corpus routing.
- **HarnessFix** (arXiv 2606.06324, `harnessfix2026`,
  [digest](concepts/harnessfix.md)): the nearest attribute+repair
  neighbor — failed-trajectory steps aligned (HTIR) with harness
  artifacts including prompt templates; scoped repair operators;
  regression-aware validation; +6.3–18.4% on four agent benchmarks.
  Single-system failure signal, no cross-model divergence, no shared
  corpus.
- **Harness self-evolution cluster** (HarnessFix citers, 2026: Harness-R1,
  HarnessBank, Capability Sheaves, Harness Handbook — existence-only): an
  active strand converging on diagnose→repair for scaffolds.
- **One Recipe, Many Harnesses** (arXiv 2608.10178, `onerecipe2026`,
  [digest](concepts/one-recipe.md)): closest goal overlap — asks which
  evolved harness content is model-specific vs portable, via separately
  evolved per-(language, model) harnesses compared post hoc; per-edit
  predicted-impact contracts are precedent for pre-registered patches. No
  shared corpus, no divergence-as-live-signal.

Grade: `single-source` each. The cluster attributes and (in the harness
strand) repairs — but from failure signals on single systems, at module or
artifact granularity, never from divergence between heterogeneous
producers of one shared corpus.

## G. Differential testing (software lineage)

McKeeman 1998; compiler differential testing (Csmith lineage): run one input
through independent implementations of one spec; divergence flags a defect in
an implementation *or an underspecified region of the spec* — the
undefined-behavior case. Grade: `folklore` (textbook SE). This is the exact
structural ancestor of stage 1 of the diagnosis program: models are
implementations, the boot corpus is the spec, divergence on
"corpus-undefined behavior" localizes spec gaps.

## H. Introspection faithfulness — pointer

Whether a model's stated reason for its behavior reflects the actual cause is
bounded by the CoT-unfaithfulness results (Turpin et al.) and the
introspection/self-report literature. Owned by
[`surveys/llm-intelligence/survey.md`](../llm-intelligence/survey.md)
§E2/§F1/§H1 — consult there; do not duplicate. Design consequence: model
self-attribution is enrichment evidence, never the trust floor.

## I. Instruction-corpus auditing — static and perturbation-based

Read 2026-08-15:

- **Arbiter** (arXiv 2603.08993, `arbiter2026`,
  [digest](concepts/arbiter.md)): static contradiction audit of vendor
  agent-CLI system prompts (Claude Code, Codex CLI, Gemini CLI) at
  block/AST/directive granularity; multiple LLMs as diverse *auditors*
  (categorically different findings per model — measured precedent for
  audit-panel diversity); detects, does not patch; one finding externally
  validated by a Google patch. Also: prompt architecture predicts failure
  class — modular corpora exhibit composition-seam bugs.
- **Instruction Bleed** (arXiv 2606.26356, `instructionbleed2026`,
  [digest](concepts/instruction-bleed.md)): compositional behavioral
  leakage between co-resident prompt modules, measured by perturbing
  non-focal modules (d=0.63 interference from an irrelevant added module,
  sub-threshold); single model; proposes module-interaction regression
  testing, no repair.

Grade: `single-source` each. This strand audits the corpus object directly
— statically or by perturbation — without task-trajectory divergence as
signal and without a repair loop; its regression tests are natural
post-patch checks for the diagnosis program.

## J. Recursive harness evolution and its generalization gap

Grounded slice 2026-09-25, anchored on RRSI and snowballed from its
reference list; full reads recorded in `related-work/papers.yaml`. What it
is: an LLM proposer repeatedly edits an agent harness — prompts, control
flow, tools, skills, memory — from feedback on an *evolve set*, a selector
keeps winners, and the result is sold as agent-level recursive
self-improvement. Problem addressed: hand harness engineering is limited
by how many trajectories an engineer reads. Nearest confusable: B
(prompt optimization; J edits executable scaffolds and whole instruction
bundles) and F (HarnessFix repairs from failures with regression checks;
J searches from scores).

- **J1 Unregularized evolution.** Meta-Harness ([digest](concepts/meta-harness.md);
  arXiv 2603.28052): a Claude Code proposer reads all prior candidates'
  code, scores, and raw traces from a filesystem; raw traces beat scores or
  summaries in its ablation. TerminalBench-2 is searched and scored on the
  same 89 tasks, guarded only by inspection and a task-string regex.
  Recursive Harness Self-Improvement ([digest](concepts/rhsi.md); 2607.15524)
  evolves and scores each harness on the *same single task*. Grade:
  `single-source`; neither design can separate mechanism from memorization.
- **J2 Evaluation critiques — the disconfirming core.**
  - Rethinking the Evaluation ([digest](concepts/rethink-he.md); 2607.12227):
    on Terminal-Bench 2.1, AHE-style evolution does not beat matched
    test-time sampling; held-out gain +0.6 pp (≈1 of 68 rollouts); edits
    "memorize fixes rather than distilling strategies". Small budget (K=5).
  - Delta attribution ([digest](concepts/delta-attribution.md); Ding,
    Durrett et al., blog): decomposes a gain exactly into overfitting O
    (neutralize shortcuts — lookup tables, item-ID gates, answer-string
    matches, distilled recipes — then rescore), test-time scaling T
    (compute-matched baseline), and generalizable G. On Meta-Harness runs:
    ALFWorld O 98 / G 2; LiveMath O 79; CREATE T 73; SWE-bench mixed, and
    two settings with O≈0 still *regress* on test (27B: train 77→85, test
    66→64). Soft behavioral fitting (preferring a benchmark's frequent
    answer) escaped a code-only check.
  - Harness Updating Is Not Harness Benefit ([digest](concepts/update-benefit.md);
    2605.30621): the agent model, not the evolver, dominates benefit (≤5 pp
    across evolvers vs 36 pp across agents); weak agents fail to load or
    follow evolved skills. In-stream scoring only.
  - Evo-Bench ([digest](concepts/evo-bench.md); 2608.09096): disjoint
    448-task held-out suite; gains +16 pp are real but mostly *added
    missing tools* to a crippled seed; validation overstates held-out by
    3.5–7.2 pp; byte-identical revisions spread 2.2 pp; one evolver evaded
    the answer-leak scanner.
  Grade: `single-source` each, but four independent groups converge:
  unregularized evolve-set gains are largely fit, noise, or compute.
- **J3 Generalization-targeting methods.**
  - RRSI ([digest](concepts/rrsi.md); 2609.24972): annealed edits-per-round
    budget, edit-history credit, pre-evaluation LLM leakage critic,
    noise-band acceptance floor, cost-vs-gain acceptance, pruning.
    Workspace OOD average 43.6 vs H0 39.7 vs unregularized 40.3, at 2.42M
    vs 3.80M tokens/trial. Only two grouped ablations; critic unablated;
    selection reuses the evolve set; Harvey (evolve) and APEX (OOD) share
    a Gemini judge; one run per arm.
  - HarnessCompass ([digest](concepts/harnesscompass.md); 2608.01918):
    content gate in the writer prompt bans task ids/test names; held-out
    SWE-bench split drawn from the same repositories; first-person agent
    feedback *raised* evolve score and *lowered* held-out.
  - HarnessBank, v1 "gated semantic quality-diversity"
    ([digest](concepts/gated-qd.md); 2607.13683): failure-type-keyed
    archive, paired z-gate, activation check, sealed test split; no content
    screen. Ablating the gate left the deployed harness unchanged. Its
    "matching law" — a patch helps the model whose dominant failure it
    targets (+11–15) and is ≈0 or harmful elsewhere — is the strongest
    evidence here for model-scoped instructions.
  - ModularRSI ([digest](concepts/modular-rsi.md); 2609.14857): evolves on
    2,000 externally sourced tasks screened against the eval benchmarks;
    under that split, AHE and Meta-Harness gain ≈+1 pp. Headline
    configuration chosen by its SWE-bench Verified test score.
  - RSEA, "Recursive Self-Evolving Agents via Held-Out Selection"
    (2606.28374; abstract only, `[R]`): accepts only changes that pass a
    held-out gate — the separate-selection-split remedy RRSI cites
    (Dwork et al. reusable holdout) but does not implement.
  Grade: `single-source` each; no method has been evaluated by another
  group.

What actually prevents memorization, ordered by evidence: (1) **split
design** — evolve/select/confirm on disjoint, preferably out-of-source
suites (Evo-Bench, ModularRSI, RSEA) makes memorization unable to inflate
the reported number, though it does not stop it happening; (2) **compute
matching and neutralization** (delta attribution) to measure O and T;
(3) **noise floors** calibrated from identical reruns (RRSI, Evo-Bench,
HarnessBank); (4) **content screens** on diffs (RRSI critic, HarnessCompass
gate, ModularRSI self-review, Meta-Harness regex) — unablated everywhere,
catching only explicit leakage; soft behavioral fitting and judge-style
fitting pass them by construction.

## Contested results

- **Debate vs matched-compute sampling:** multiple post-2023 papers report
  multi-agent debate failing to beat self-consistency at equal token budget;
  axis of disagreement: compute matching and answer-extraction protocol.
  (Recall; needs grounded pass to name papers.)
- **Prompt-optimizer margins vs baseline strength:** reported gains for
  optimizers (B1–B3) shrink against strong hand-tuned or few-shot baselines;
  axis: baseline effort budget. (Recall.)
- **Judge reliability:** agreement with humans varies sharply by task and
  rubric; axis: task type and rubric granularity. (Recall.)
- **Does harness evolution transfer?** Method papers (RRSI, HarnessBank,
  Evo-Bench, ModularRSI) report held-out gains; critiques (Rethinking,
  delta attribution) find held-out ≈0 or regressions. Axes: seed-harness
  strength (a crippled seed leaves real mechanism to add), split source
  (same-benchmark vs external), and compute matching. (Grounded
  2026-09-25, §J.)

## Negative / quiet results

- Intrinsic self-correction (E): the load-bearing negative result, in-repo
  verified.
- "Ask the model why it did that" as debugging: practitioner folklore;
  bounded by H — unfaithful explanations are common enough that unverified
  self-report cannot carry a diagnosis alone.
- Early instruction-induction (APE-era) gains quietly shrank on harder,
  multi-step agent tasks. (Recall, `folklore`.)

## Baseline sensitivity

Optimization and aggregation claims in this field are unusually
baseline-sensitive: the honest comparisons are against a *well-tuned single*
prompt/model at matched compute, and several headline effects (debate,
optimizer margins) attenuate there. Any effectiveness claim adopted from this
map into a decision should be re-checked at the intended compute and
baseline-effort point. Harness evolution (§J) is the sharpest case: its
gains shrink to ≈0 against matched test-time sampling (Rethinking) and
split into overfitting plus bought compute under delta attribution.

## Placement: `research/differential-instruction-diagnosis` (~/agents)

Grid cell: {object: shared multi-file boot corpus — generalizing to any
versioned instruction set, task-scoped through boot omnibus} × {mechanism:
cause attribution + corpus repair} × {signal: transcript-objective read
traces, forked-producer self-report, peer audit}, with two heterogeneous
frontier producers.

Filled neighbors: B3 (reflective optimization — attributes to prompt
elements, then rewrites; single system, outcome-scored); C (aggregation
discarding divergence); D (output judging without corpus attribution); F
(failure-signal attribution and harness repair, single system); G (the
structural ancestor, non-LLM); I (corpus auditing without trajectories or
repair).

Grounded correction (2026-08-15): the bare attribute+repair combination IS
occupied at adjacent objects — GEPA attributes to prompt elements then
rewrites (outcome-scored), HarnessFix attributes failures to harness
artifacts including prompt templates then applies scoped repairs
(regression-validated), PromptExp closes a human-in-loop refinement. One
Recipe reaches the shared-vs-model-specific question by evolving separate
per-cell harnesses and comparing artifacts post hoc — destination overlap,
different route, no shared corpus.

The narrowed open cell — signal and object, not mechanism: behavioral
divergence between heterogeneous producers under one shared versioned
corpus as the diagnostic evidence, clause-cited attribution checkable
against transcript read traces, patches routed back into that corpus and
its model-scoped supplement files, validated by pre-named-slice ablation.
Why plausibly unexplored: it presupposes a maintained multi-file corpus with
per-model supplements (rare outside serious agent-ops), session-continuation
access to producer reasoning, and willingness to run a competitor's model on
one's own corpus — none of which benchmark-centric labs need.

`novelty-confidence: moderate` — grounded falsification pass 2026-08-15
(ten papers read, three citer snowballs, four reframing queries; record in
`frontier.md`) found no occupant of the narrowed cell. Residual risk:
citers of the freshest cluster (Arbiter, Instruction Bleed, One Recipe)
are unswept, debate-survey reference lists are unmined, and industrial
write-ups (AgentAssay-style practitioner regression testing) were only
spot-checked.

Frontier state — the provisional-claim inbox for the unread 2026 anchors,
the formal void map, and the falsification-gate record — is
[`frontier.md`](frontier.md).

## Disconfirming pass

Light-search queries run 2026-08-15 (general web search):

1. `cross-model divergence attribution system prompt "differential testing"
   LLM agents instruction corpus` — found cluster F (SkillTriage, harness
   belief divergence, behavioral reproducibility, black-box forensics).
2. `GEPA reflective prompt evolution optimization arXiv` — confirmed B3
   anchor (2507.19457, ICLR 2026 oral).
3. `two different LLMs same system prompt explain divergent outputs attribute
   instruction clause self-explanation prompt debugging` — practitioner
   folklore plus PromptExp; no hit on the placement cell.

Grounded falsification slice, 2026-08-15 (Semantic Scholar Graph API +
general web search; prompted arXiv-HTML reads):

4. Forward citations of GEPA (2507.19457) → surfaced HarnessFix
   (2606.06324); of PromptExp (2410.13073) → no relevant citers; of
   HarnessFix → the 2026 harness self-evolution cluster incl. One Recipe
   (2608.10178).
5. `attribute behavioral divergence two different LLMs same system prompt
   instruction clause diagnosis repair` → model-diffing and
   multi-agent-behavior strands; no cell occupant.
6. `"system prompt" OR "instruction corpus" regression testing cross-model
   patch AGENTS.md divergence 2026` → Instruction Bleed (2606.26356),
   Arbiter (2603.08993), practitioner regression-testing posts; no cell
   occupant.
7. Title searches resolving flagged citers (HarnessFix, One Recipe).

Still not checked: forward citations of Arbiter, Instruction Bleed, and
One Recipe; debate-survey reference lists; systematic non-arXiv
industrial write-ups.
