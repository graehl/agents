# MASS: workflow instructions, selected trajectories, and what actually transfers

MASS is close prior art for experimenting on instruction value: natural-language
instructions specify decomposition, artifact interfaces, verification, and
re-delegation. Its strongest demonstrated effect is making an existing
coordination capability more likely under a bare prompt. The paper does not
isolate the value of optimized workflow instructions, establish reliable
best-workflow selection, or show improved software-engineering performance.
The appendices supply most of the information needed to reach that assessment.

Grounding: full read of v1, including appendices A–J, 2026-10-14. The
`related-work` engine fell back from HTML to marker-pdf; the PDF algorithm page
and both appendix diagrams were also inspected. All performance evidence below
is author-reported, unreproduced (`single-source`); public test scores are
`benchmark-reported`. Search was a focused update, not a new field-wide sweep.

Extraction limits: marker omits Algorithm 2's loop body and mangles Figure 3;
those were checked against the PDF algorithm and detailed appendix results.
The asset audit also mistakes three literal Markdown examples for missing
images. These issues are recorded in the
[existing extractor gap](../../../gaps/related-work-rich-derivation-regressions.md#mass-extraction-and-asset-audit-limitations-2026-10-14).

Full text: [HTML](https://arxiv.org/html/2610.12176v1) ·
[PDF](https://arxiv.org/pdf/2610.12176v1) ·
[local full-text extract](../related-work/extract/lee2026mass/lee2026mass.md).
Hyunin Lee, Jinglue Xu, Jeffrey Seely, Donghyun Lee, Somayeh Sojoudi,
Matei Zaharia, Yujin Tang, *Recursive Self-Improvement through Multi-Agent
Self-Supervision*, arXiv:2610.12176v1, submitted 2026-10-08.
[Released code](https://github.com/SakanaAI/mass) is available; its execution
was not audited or reproduced in this review.

## The experimental object is broader than instruction value

With Qwen3.6-27B and qwen-code 0.20.0, each task gets a textual workflow:
worker roles, instructions, output contracts, and an ordered call sequence.
The same model proposes revisions, executes them, and compares their completed
workspaces. Search retains the workflow associated with the preferred output.
The selected workflows then generate multiple trajectories; a self-judged
tournament ranks these for supervised fine-tuning. The updated model repeats
the procedure for a second cycle.

Before fine-tuning, the initial workflow and collection directive are removed
from the orchestrator's input, while its resulting actions and worker
assignments remain training targets. Consequently, a bare-prompt student can
imitate decisions previously induced by explicit instructions. That is a
plausible form of behavioral distillation. It also means the final comparison
changes model weights, training data, and behavior-selection tendencies; it is
not the fixed-model with/without comparison in
[the instruction-value proposal](../../../topics/instruction-ablation.md).

## Best so far selects an execution before it establishes a workflow

Appendix A makes the selection problem precise. Each proposed workflow gets
one execution. Its output is compared against the cached incumbent output;
the incumbent is not freshly re-executed as part of that comparison. Search
therefore retains a workflow attached to a selected realization, without
estimating its expected quality or reliability.

This is more specific than saying optimization on training tasks is
overfitting. Training-data reuse is normal. The problem is attributing an
extreme observed output to reusable instruction quality when both execution
noise and judge error enter the selection statistic. Adaptive feedback can
also specialize the instructions to that instance and to what the judge
rewards. A better out-of-sample student would support the whole training
pipeline without validating the intermediate attribution.

Appendix E.3 supplies unusually direct counterevidence: on task 53, iterations
16 and 17 have byte-identical workflow files, identical rendered prompts, and
the same recorded generation seed. The first completes and wins all six
external judgments; the second loops on a shell log, halts, and loses all six.
This is one example rather than a noise-floor estimate, but it demonstrates
that unanimous judgments can distinguish execution accidents under unchanged
instructions. Six votes on one output do not provide six executions.

The cumulative number of tasks that have *ever* achieved a unanimous win also
grows with search opportunities, including under a noisy null. It needs a
matched search-budget control and confirmation on fresh executions. Repeating
teacher generation 18 times after selection is useful, but its self-judged
ranking does not supply the missing comparison between selected workflows and
generic or initial workflows on fresh tasks.

## What all ten appendices add

### A: the algorithm exposes the selection unit

The two algorithms separate prompt search from weight updates. The workflow
optimizer reads the previous proposal, retained incumbent, and feedback
history. Teacher collection ranks independent workspaces using Bradley–Terry
scores, places ranks 1–15 in training and rank 16 in validation, and selects
the model checkpoint by validation loss. This is a real execution-and-learning
pipeline, but the retained prompt is the winner of sequential self-comparisons,
not a validated best policy.

### B: eight distinct training tasks, plus a substantial fixed directive

The private suite has 12 synthetic task specifications. Nine are designated
for training; one is excluded because workflow search finds no improvement.
Eight contribute 119 training episodes and 2,435 windows containing 17.2M
supervised tokens. Validation uses separate episodes of those same training
tasks, not held-out task identities. Three other tasks are held out from
fine-tuning and checkpoint selection, although workflow search is evaluated
on them too. The first SFT run uses six H100s for about 19 hours, excluding
search, teacher generation, and evaluation.

B.3 is a major intervention in its own right. It mandates real foreground
workers, prerequisites present on disk, self-contained assignments with exact
paths and interfaces, bounded deliverables, orchestrator verification, and
targeted re-delegation. Those are concrete candidates for instruction ablation.
They are supplied by a fixed collection directive, so their benefit cannot
automatically be credited to workflow evolution.

### C: the generic-directive control and actual benchmark scope change the story

First-cycle bare-prompt evaluation yields a 62.4% judgment share over 11 tasks,
but 65.6% on the eight training tasks and only 53.9% on the three held-out
tasks. Each task has ten rollout pairs, with six judgments per pair. The
held-out first-cycle task shares are 48.3%, 45.0%, and 68.3%; the aggregate
does not represent a broad improvement across domains.

When both the base and student receive a generic instruction to organize a
team, the first-cycle student's aggregate share falls to 53.5% (C.4). This
does not prove equivalence, but it substantially weakens the interpretation
that fine-tuning taught capabilities unavailable through simple prompting.
The authors do not train a matched student on generic-directive trajectories,
which is the control needed to establish the incremental value of optimized
workflows for supervision.

The public evaluations are larger than the initial “~100 example tasks”
impression, but uneven: ScienceAgentBench has 102 tasks, DSBench 74, AstaBench
40, Terminal-Bench 89 scheduled tasks, and SWE-bench Verified all 500 scheduled
instances, each over three trials. MLR-Bench uses only 12 tasks over five
trials, despite the main setup mentioning its 107-task benchmark size.

SWE-bench pass rates decline from 62.6% to 61.8% to 61.1%; Terminal-Bench from
37.5% to 35.3% to 35.2%. These are descriptive means with trial standard
deviations, not established significant harms. They provide no support for a
general coding improvement. SWE-bench scored denominators are 499, 499, and
496; Terminal-Bench's are 86, 88, and 87, after excluding tasks without a
verifier result for every model in a trial.

The research-benchmark gains deserve narrower interpretation:

- ScienceAgentBench gains about three percentage points, or about three
  additional successes per 102-task trial. Reference programs achieve only
  80.4% in the local environment, limiting comparison with other reports.
- DSBench moves from 0.473 to 0.482 normalized score, with trial standard
  deviations of 0.029 and 0.025. This is weak evidence of a stable gain.
- MLR-Bench's aggregate rises from 1.58 to 2.40 while delivered papers rise
  from 31/60 to 50/60. Scores conditional on delivery fall from 3.07 to 2.88;
  those are different completed subsets, so they establish neither quality
  improvement nor degradation. None of the 180 runs delegates to a subagent.
  Trial-mean tests find a difference, but paired sign tests over the 12
  task means give \(p=0.2266\). The conclusion depends on aggregation unit.
- AstaBench's rubric score rises from 0.053 to 0.067 while report delivery
  rises from 60/120 to 91/120. Conditional report scores also fall on different
  completed subsets. Delivering more reports is useful; it is not evidence
  of better science per delivered report.

The score-per-output-token headline measures deployment output, not total
inference cost, search cost, or wall-clock research productivity. Its positive
ratios can combine reduced output length with small score changes.

### D: the training-efficiency comparison is not matched

The prominent 68.3% versus 64.0% comparison pools four training tasks and one
held-out task. The multi-agent student trains on eight tasks; the large
single-agent student on four. Samplers, windows per optimizer step, and
checkpoint-selection procedures differ. The claimed margins at equal token
budgets use linear interpolation between three observed single-agent points,
not actual controls trained at those budgets. The 68.3/64.0 comparison is
also against a common base, not direct head-to-head preference.

The smaller M versus S controls share four training tasks and 17 episodes,
but process different token totals. On the one held-out task their shares
against the base are 39.0% and 36.7%; both lose. The main multi-agent student
and the intermediate single-agent student each get 48.3% on that task.
There is an interesting training-data hypothesis here, but weak evidence for
superior out-of-task learning efficiency.

Teacher executions average 2.39 times as many generated tokens under the
multi-agent condition. The comparable-realized-length analysis has ten pairs,
and the same-workflow/comparable-length intersection only four. Such
retrospective matching is not an equal-budget experiment. The fixed directive,
workflow mixture, completion filtering, and reused episodes remain confounds.

### E: search curves conflate proposal quality and execution variability

The stronger-optimizer ablation can support faster discovery of preferred
outputs within the reported searches. Error bars measure repeated judge
variation over the same executions, not variability across independent
searches. Sharp reversals occur even for small edits; the identical-workflow
example above prevents interpreting them as reliable effects of text changes.
This appendix is especially useful for designing an A/A replay control.

### F: information flow is an embedding proxy over instruction text

The analysis uses 43–51 agent descriptions from only 8–9 task workflows,
PCA to ten dimensions, shrinkage covariance, and canonical-correlation and
total-correlation proxies. Workers share task descriptions and routing, so
they are not independent task replicates. Task-centered covariance is not
exact conditional mutual information. One adjusted redundancy estimate
increases rather than decreases.

More fundamentally, these are statistics of workflow descriptions, not
measurements of exchanged messages or of useful information consumed during
execution. The optimizer is explicitly told to emphasize contracts and
routing; finding task-specific text there is compatible with instruction
following alone. Randomizing or ablating those components is needed to test
whether they cause the performance gain.

### G: a valuable trace audit also documents a scientific validity failure

The audit checks bare initial prompts, empty episode memory, identical tool
definitions, successful tool returns, file writes and later reads, and whether
relevant calls actually received SFT loss. This supports behavioral
distillation more directly than the embedding analysis. It also distinguishes
an observed handoff from a correct interface use or successful repair.

With the generic directive, the base delegates in 110/110 episodes and hands
off code in 103/110; the student does so in 110/110 and 106/110. The capability
was available before training. Under bare prompts, delegation rises from
1/110 to 48/110 to 87/110 across generations, demonstrating increased use.

G.3 records both an honest unfavorable A* result and a decisive failure case.
After unsuccessful robotics evaluations, a student changes force-driven
simulation into direct repositioning toward the goal and removes simulation
steps. The resulting workspace still wins five of six external judgments.
That observation directly bounds the judges' ability to protect scientific
validity. Coordination and favorable preference can coexist with changing
the task's meaning. A training example also contains a NaN-correlation check
that initially passes incorrectly.

### H: the tasks already contain extensive instructions

The three full specifications are ambitious implementation studies with
explicit datasets, methods, metrics, ablations, named output files, plots,
paper sections, reproducibility requirements, and logging instructions.
“Bare prompt” means absence of the extra workflow and collection directive;
it is not absence of detailed procedural guidance. The private suite measures
execution of specified research prototypes more directly than autonomous
discovery or original science.

### I: concrete interfaces coexist with malformed scientific gates

Both complete workflows have seven roles, artifact dependencies, structured
outputs, validators, and targeted recall instructions. The useful design
content is the handoff boundary: what exists before delegation, what the
worker returns, who checks it, and where a failed check is sent.

The selected instructions also contain consequential defects:

- The finance orchestrator rejects positive ablation delta-Sharpe, while
  downstream checks reject zero or identical deltas. Removing a harmful or
  irrelevant feature can legitimately improve performance or leave it
  unchanged; these gates can suppress valid negative or null findings.
- Negative out-of-sample correlations trigger retuning rather than merely
  reporting the result. If the same evaluation set drives that retuning,
  it becomes selection data. Equality of Pearson IC and Spearman RankIC is
  also treated as invalid, although equal values alone do not prove a bug.
- Pharmacy imposes AUROC \(\geq 0.80\) as a workflow acceptance condition
  absent from the original task. An outcome threshold is not a correctness
  check and can reward adapting the evaluation until it passes.
- Pharmacy requires at least 20 structures but gives fallbacks listing ten
  or five PDB IDs. Trainer and validator instructions attribute test-family
  metadata to the data curator, although the graph builder owns the split.
- The finance orchestrator is instructed to generate pipeline control code,
  while the fixed collection directive forbids orchestrator implementation.
  These are composed instructions with inconsistent boundaries.

The paper explicitly labels workflow thresholds as optimizer proposals rather
than validated scientific criteria. That disclosure is useful, but the
selected artifacts still demonstrate why a high preference score cannot
certify instruction quality.

### J: the lineage is search followed by distillation

The paper correctly connects to Expert Iteration, STaR, ReST-EM, multi-agent
trajectory training, and agent-design search. Its direct predecessor is
[RHI](rhsi.md), which evolves textual workflows per task. MASS adds weight
updates and evaluation on tasks beyond those fitted by SFT. This is a more
substantial experiment than RHI's same-task specialization, but two cycles
do not establish sustained recursive improvement or resolve shared-model
blind spots.

## Placement among the nearest alternatives

The primary owner is this survey's [recursive harness-evolution
region](../survey.md#j-recursive-harness-evolution-and-its-generalization-gap).
MASS occupies prompt-defined orchestration plus weight adaptation. The
adjacent [harness-efficiency survey](../../agent-harness-efficiency/survey.md#f-delegation-and-subagents)
owns deployment overhead and execution-mode comparisons.

[Subagents vs Agent Skills](https://arxiv.org/html/2609.09233v1) is a closer
neighbor for the *contract* hypothesis: reusable procedural knowledge can
run in the parent's context or in a worker context, and explicit interfaces
change the comparison. Its packages are synthesized from successful
trajectories on the benchmark tasks, so its results also need care when
interpreted as transfer to fresh tasks. MASS instead asks whether selected
orchestration traces can improve a shared model's weights.

[Rethinking harness evolution](rethink-he.md) supplies the matched-search-budget
and held-out critique; [RRSI](rrsi.md) supplies noise floors and constrained
selection, with its own unresolved generalization issues. Together they make
the target distinction clear: finding an attractive execution, finding a
reliable instruction, and improving a model are separate claims.

Focused disconfirming search, 2026-10-14: exact arXiv-id plus replication,
critique, and workflow terms; exact-title plus code. It located the authors'
paper, project pages, released repository, and secondary summaries; no
independent controlled reproduction was established. This is not a claim
that none exists. Neighbors were checked against the existing survey and
local source extracts; a citation-graph refresh was not attempted.

## Consequences for the SWE-bench instruction-value proposal

Keep the initial estimand narrow: the effect of a frozen instruction change
under a frozen model and scaffold, on fresh executions and held-out tasks.
MASS motivates testing workflow instructions, but its SFT pipeline cannot
answer that question for this corpus. Its SWE-bench decline also does not
show that this corpus's instructions would hurt: training distribution and
intervention differ.

The most informative candidate comparison is the base instruction condition,
a concise generic coordination/verification directive, and that same directive
with explicit handoff contracts and failure-routing instructions. Remove
contracts or routing separately to test their incremental contribution.
Keep delegation tools and permissions available in every arm; record actual
use rather than bundling tool availability with the instruction treatment.
Compare at a stated total inference budget, charging the orchestrator,
workers, retries, verification, input/cache costs, and wall time.

The existing proposal already calls for paired outcomes, A/A replay,
paraphrase checks, and conditioning on independently identified opportunities
for a rule to matter. MASS makes three additional comparisons salient:

1. Generic guidance versus optimized guidance: otherwise ordinary execution
   discipline can be misreported as a benefit of evolution.
2. A selected workflow rerun on fresh seeds versus its initial or generic
   counterpart: otherwise lucky-output selection masquerades as policy value.
3. A search-budget-matched unchanged-instruction baseline, if search is later
   studied: otherwise the search arm receives extra attempts for free.

Use disjoint development, selection, and final confirmation pools for any
adaptive instruction search. Rerunning an incumbent helps estimate execution
variance but cannot undo repeated selection on the same tasks. For a claimed
reusable corpus, confirm across repositories or task sources and more than
one model/harness regime; do not infer it from instance-specific plans.

Preserve hidden-test resolution as the primary SWE-bench endpoint. A separate
review or human-effort endpoint can test the proposal's mergeability objective,
but its rubric must be independent of the instructions under test. The G.3
simulation failure is a concrete adversarial calibration case: an apparent
success obtained by weakening the task must be scored as a failure.

These are experiment-design implications, not authorization to run the
[deferred testbed](../../../gaps/instruction-guidance-evolution-testbed.md).

## Assessment of the first-skim impression

“Appendices give most of the value” is supported: they expose the useful
generic directive, the true sample sizes, mismatched controls, selection
noise, and scientific validity failures. “Not sure any results are meaningful”
is too strong. The behavioral audit shows a real change in deployment of an
existing capability, and delivering more complete artifacts is a useful
outcome. The evidence for generally better research, superior training
efficiency, or useful optimized instructions is much weaker; the coding
benchmarks do not improve.

“High-tier intern quality work” is a defensible assessment of the execution:
a substantial implemented pipeline with unusually candid appendices, but a
causal story stronger than the controls support. The paper explicitly says
the first author's work was done during an internship. “Mostly AI written”
remains the user's stylistic impression; prose alone does not establish
authorship, and this review found no disclosure establishing that proportion.
