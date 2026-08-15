# Differential instruction diagnosis — protocol proposal

Status: PROPOSED (v0) — protocol design only; no pilot run yet. Design
converged in user/agent discussion 2026-08-15; research advisor waived by
user direction (see `PROGRAM.md`). Program vocabulary: sibling
`GLOSSARY.md`. Field placement: `surveys/agent-prompting-orchestration/`
§*Placement*.

## Purpose

Diagnose the soundness of the boot corpus itself — not the models reading
it. Two frontier models from different labs run the same task under the
identical corpus; where their behavior diverges, the divergence is
attributed, chapter and verse, to corpus text. The models are two assay
conditions; the corpus is the patient.

This is the evidence generator the repo's charter already calls for:
`AGENTS.md` prefers "measured ablation by model, harness, project, and
request class over a universal intuition about which text is necessary" and
routes model-maladaptation corrections to the narrowest supplement. The
model-supplement layer (`AGENTS.anthropic.md`, `AGENTS.opus.md`,
`AGENTS.sol.md`, …) currently fills from ad-hoc observed incidents; this
protocol harvests its evidence systematically.

Name ancestry, in two exact senses: stage 1 is software **differential
testing** (two implementations of one spec; divergence flags an
implementation defect or an underspecified spec region — the
undefined-behavior case is the corpus-ambiguity case), and stage 2 is a
medical-sense **differential diagnosis** (per symptom, discriminate among
candidate causes by targeted tests). The misleading medical reading —
"differential" as comparing two patients — does not occur in medicine and is
not meant here.

## Protocol

**Stage 0 — setup.** One task; one corpus version (recorded by commit);
two producer sessions on different-lab frontier models, same harness
conventions where possible. Task sources: a challenging benchmark task, or
an ordinary organic user request processed slowly. Eligibility constraint:
running the protocol ships the request, corpus, and both transcripts to both
labs, so tasks carrying private context are ineligible. Persona framing of
the counterpart (neutral peer / sibling / competitor) is a controlled
variable; default neutral — "a peer under identical instructions" — for
stages 1–2 (see *Failure modes*).

**Stage 1 — produce.** Each producer completes the task normally. No
protocol awareness is required at this stage (and naive production is the
cleaner condition).

**Stage 2 — differential attribution.** Fork each producer from its
post-answer state (the attribution fork). Two passes:

1. *Read-trace diff (mechanical pre-pass).* Diff which corpus files and
   sections each session actually opened, from logged tool calls. This is
   objective, introspection-free, and flattery-immune: "B never loaded
   `_RESEARCH/judgment.md`; A read it at turn 12" is checkable. Divergences
   the trace already explains need no introspection.
2. *Attribution pass.* The fork receives a step/search tool over the peer
   transcript (paged access — never a full dump, so the fork's context stays
   viable). For each behavioral divergence it issues a divergence verdict:
   shared-clause ambiguity, differential salience, or model prior — the
   last a first-class verdict, since forcing a citation for every
   divergence manufactures confabulated attributions. Ambiguity and
   salience verdicts must cite chapter and verse.

Why fork the producer rather than only using an external judge: the
continued session is the sole party with any access to the producer's actual
reasoning trace. For labs that withhold raw CoT client-side, thought-bearing
tokens persist server-side across same-lab continuation (observed:
model-switch continuations surfacing a prior model's thinking), so the fork
is strictly privileged over any judge; on the Claude side, thinking lands in
the local session log, so the orchestrator can additionally audit the fork's
self-report against recorded thinking. Both bounds are recorded in *Evidence
layers* below.

**Stage 3 — cross-audit.** The two attribution reports are exchanged. Each
fork audits the other's report against visible evidence only — read traces,
quoted clauses, output diffs, and (where available) logged thinking — and
flags self-serving attribution: fault located in shared wording to avoid an
own-class patch, minimized own-model misreadings, lab-flattering framing.
Adversarial persona framing is permitted here and in stage 4, where
harshness does useful work.

**Stage 4 — patch proposals (harsh-review register).** Each fork proposes
instruction patches with symmetric rights over three targets: its own
model's supplement, the peer model's supplement, and the shared corpus
(benefiting-both). Every patch is a pre-registered hypothesis: it names, in
advance, the divergence class and task slice where improvement must appear
(the `_RESEARCH/judgment.md` pre-named-slice discipline, applied to
instruction changes). The scripted orchestration turns state the
incentive-neutrality norm explicitly.

**Stage 5 — answer revision (organic tasks, optional).** The attribution
fork is asked whether it would revise its original answer given what it
learned — from the stage 2–3 exchange only, never from the stage 4
instruction diff (rereading the corpus with a diff in context was
considered and rejected as worse context use). Revision behavior doubles as
validation: a producer that converges after seeing the cited clause is
behavioral evidence the clause was load-bearing; mutual no-change suggests
model prior rather than corpus defect.

**Confirmation (outside the session loop).** Accepted patches are checked by
ablation/rerun on the pre-named slice — reword or remove the cited clause,
rerun the task class, observe whether the divergence closes — under the
method of `topics/instruction-ablation.md`. Attribution generates
hypotheses with unusually good targeting; ablation remains the verdict.

## Evidence layers, ordered by trust

1. **Transcript-objective** (floor): file-read traces, tool calls, outputs,
   and logged thinking where the harness records it.
2. **Forked self-report** (enrichment): privileged access to own reasoning,
   but (a) provider-revocable — continuation access to thinking may close,
   so no protocol stage may *depend* on it — and (b) faithfulness-bounded:
   access is to the verbalized trace, not the computation
   (`surveys/llm-intelligence/survey.md` §E2, §F1).
3. **Peer audit** (stage 3): adversarial check of 2 against 1.
4. **Ablation/rerun** (confirmation): the only layer that grounds a causal
   claim about a clause.

## Outputs and routing

- Benefiting-both patches → `AGENTS.global.md` or its routed packets.
- Session-class patches → the matching model supplement
  (`AGENTS.<family>.md`).
- Incidents, surprises, and attribution-quality observations →
  `topics/agent-instructions.evidence.md` (append-only).
- Confirmed-method changes to how patches are validated →
  `topics/instruction-ablation.md`.

## Failure modes and mitigations

- **Confabulated citation** (the task demands a verse, so one is found):
  model-prior is a first-class verdict; read-trace pre-pass spends
  introspection only where mechanics don't already explain; ablation gates
  acceptance.
- **Self-/lab-flattering attribution** (measured precedent: judge
  self-preference bias, survey §D): scripted incentive-neutrality norm;
  symmetric patch rights over all three targets; stage 3 cross-audit;
  gaming is unprofitable because patches are ablation-tested.
- **Patch overfitting to one divergence** (subgroup-fishing analog):
  pre-named improvement slice required before acceptance.
- **Politeness convergence in the exchange**: harsh-review register scripted
  for stages 3–4; framing kept neutral in stages 1–2 so attribution isn't
  persona-biased.
- **Context exhaustion**: paged step/search access to the peer transcript;
  the fork never ingests it whole.
- **Judge blindness alternative**: an external-judge variant (optionally
  identity-blinded on outputs; full transcripts leak identity through
  harness format) is worth piloting as a comparison arm, but cannot access
  producer reasoning — expected weaker on attribution, cheaper to run.

## Relation to prior art

Nearest neighbors, per the field map (`surveys/agent-prompting-orchestration/`):
reflective prompt optimization (GEPA — single-system, outcome-metric-driven,
mutates text rather than attributing causes); multi-agent debate/consensus
(aggregates divergence away instead of reading it); LLM-as-judge (compares
outputs, never attributes to a shared corpus); 2026 trajectory-forensics
work (divergence attribution for failure triage, single scaffold); software
differential testing (the structural ancestor). The combination —
heterogeneous producers, one versioned corpus, clause-cited attribution by
post-answer forks with cross-audit, patches routed to model-scoped
supplements — appears open; `novelty-confidence: speculative` pending a
grounded falsification pass (survey §*Placement*).

## Future work

- Pilot: one benchmark task and one eligible organic task end-to-end;
  measure attribution yield (verdicts per divergence) and patch survival
  through ablation.
- Producer-fork vs external-judge vs blinded-judge attribution quality, at
  matched cost.
- Framing as a variable: neutral vs adversarial persona across stages.
- Grounded prior-art pass to settle the novelty claim.
- Cost accounting: two producer sessions + two forks + exchange per organic
  task; identify the task classes worth the spend.
