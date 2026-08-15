# Field map: agent prompting and orchestration — instruction effects, prompt optimization, multi-model aggregation, and divergence attribution

Mode: **recall** (pretrained recall through the authoring model's
2026-01 cutoff; claims are not citation-verified). Light search run
2026-08-15 via general web search — three queries, recorded in
*Disconfirming pass* below — to catch post-cutoff releases; only nodes
citing an arXiv id found by that search have a verified-to-exist source,
and none of those papers has been read. Effectiveness grades are capped
at `single-source`; `folklore` is used where honest. Upgrade path: re-run
as `grounded` (snowball from the anchors named per section, build
`related-work/`), then revise grades.

Coverage cutoff: literature as represented in pretraining through
2026-01, plus web search 2026-08-15 (no venue-scoped sweep).

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
- **A3 Config- and harness-induced divergence.** Post-cutoff light-search
  hits, unread: "Measuring Harness-Induced Belief Divergence in Multi-Step
  LLM Agents" (arXiv 2607.04528) and "How Consistent Are LLM Agents?
  Measuring Behavioral Reproducibility in Multi-Step Tool-Calling Pipelines"
  (arXiv 2605.28840). Search-result claim: a large share of divergence
  originates in the first steps of a trajectory. Grade: `single-source`,
  existence-only. Nearest confusable: A1 (prompt paraphrase sensitivity) —
  A3 varies the *harness/config*, holding the prompt fixed.

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
  Outperform Reinforcement Learning" (arXiv 2507.19457; ICLR 2026 oral —
  light-search confirmed to exist, not read). Reported by its authors:
  outperforms GRPO by ~6% average with up to 35× fewer rollouts and MIPROv2
  by >10%. Grade: `single-source` (self-reported numbers). Related:
  PromptBreeder, TextGrad (recall, `folklore`).

Relation to the rest of the map: B reads *execution/evaluation traces of one
system* and mutates text to climb a metric. Nearest confusable with the
diagnosis program below — the key differences are (i) signal: outcome metric
vs divergence between two heterogeneous readers of the same corpus, and
(ii) output: mutated text vs cause attribution with cited clauses, from which
patches follow.

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

## F. Trajectory attribution and agent forensics — nearest cluster

Post-cutoff light-search hits, all existence-only, none read:

- **SkillTriage** — "Agent Skills Can Be Harmful" (arXiv 2608.11888):
  post-hoc triage of skill-induced failures; search-result claim: predicts
  failure categories and returns *contrastive evidence* over
  target-vs-reference trajectory divergence.
- **Black-box forensics for conversational agents** (arXiv 2606.22698):
  search-result claim: black-box attribution of system prompts works in
  binary settings, degrades when semantic intent is preserved.
- **PromptExp** (arXiv 2410.13073): multi-granularity attribution of a
  *single* model's output to prompt components.

Grade: `single-source`, unread. This cluster does divergence attribution —
but (as surfaced) for failure triage or single-model prompt components, not
for diagnosing a shared corpus via heterogeneous producers.

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
baseline-effort point.

## Placement: `research/differential-instruction-diagnosis` (~/agents)

Grid cell: {object: shared multi-file boot corpus — generalizing to any
versioned instruction set, task-scoped through boot omnibus} × {mechanism:
cause attribution + corpus repair} × {signal: transcript-objective read
traces, forked-producer self-report, peer audit}, with two heterogeneous
frontier producers.

Filled neighbors: B3 (single-system reflective optimization, outcome-driven);
C (aggregation discarding divergence); D (output judging without corpus
attribution); F (divergence attribution for failure triage / single-model
prompt components); G (the structural ancestor, non-LLM).

No filled neighbor holds both load-bearing mechanisms at once: F
attributes but repairs nothing, B3 repairs (mutates text) but attributes
nothing, D judges without doing either. The attribution→repair loop
against a shared maintained corpus is itself part of the claimed cell.

The apparently open cell: heterogeneous producers under one versioned
instruction corpus, divergence attributed *to cited corpus clauses* by
post-answer forked producers plus cross-audit, with patches routed back
into that corpus and its model-scoped supplement files and validated by
pre-named-slice ablation.
Why plausibly unexplored: it presupposes a maintained multi-file corpus with
per-model supplements (rare outside serious agent-ops), session-continuation
access to producer reasoning, and willingness to run a competitor's model on
one's own corpus — none of which benchmark-centric labs need.

`novelty-confidence: speculative` — recall-mode cap; a `grounded`
falsification pass (snowball from GEPA, SkillTriage, PromptExp, and a debate
survey as anchors) is required before treating the void as established.

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

Not checked (needs grounded pass): forward citations of the F-cluster and
GEPA; debate-survey reference lists; non-arXiv industrial write-ups.
