# Successful paper forms

> A vocabulary of expository forms that make machine-learning research papers
> enjoyable, digestible, and memorable, independent of how valuable the
> underlying discovery is.

Topic: `successful-paper-forms`

## What this taxonomy describes

A **paper form** is an expository lens and reader promise: what the paper asks
the reader to follow, and what kind of understanding the reader expects to
leave with. It is not a grade of scientific importance. Evidence strength,
novelty, practical effect, and the independent attraction factors in
[`paper-attractiveness`](paper-attractiveness.md) are separate axes.

The separation matters when reading the accepted-paper record. A decisive
result can survive plain exposition, while a diffuse or marginal program may
need unusually effective form to clear a reviewer or reader's attention
threshold. That selection effect could even make polished form look inversely
associated with raw discovery value among published papers. The examples below
show recognizable forms, not evidence that the form caused acceptance or
community appreciation.

A paper normally has one governing form: the promise that controls its
abstract, section order, and repeated visual cadence. Local presentation-mode
switches do not create a hybrid. A genuinely substantial second form usually
wants a separate paper. The common integrated exception is a theoretical
result paired with an empirical, problem, or system form when the theorem
explains, guarantees, or delimits the same central claim. A supporting resource
release can remain an attraction multiplier without becoming a second form.

## Forms

### Headline-result paper

**Reader promise:** one result changes what can be done on a task people
already care about. State the result early, then spend the paper making the
comparison credible and explaining enough of the system to transfer the
insight. This is the reference form, not much of a rescue form: the headline
usually carries the paper.

Examples: [ImageNet Classification with Deep Convolutional Neural
Networks](https://proceedings.neurips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html)
and [Mastering the Game of Go with Deep Neural Networks and Tree
Search](https://www.nature.com/articles/nature16961).

### Recipe-synthesis paper

**Reader promise:** here is a tested recipe you can apply to your own model or
task. Organize modular interventions by purpose, keep a stable baseline and
visual grammar, ablate the pieces, and finish with the combined recipe. The
individual ingredients may be known; selection, interaction, and reliable
quantification are the product.

Examples: [Bag of Tricks for Image Classification with Convolutional Neural
Networks](https://openaccess.thecvf.com/content_CVPR_2019/html/He_Bag_of_Tricks_for_Image_Classification_with_Convolutional_Neural_Networks_CVPR_2019_paper.html)
and [Implementation Matters in Deep Policy Gradients: A Case Study on PPO and
TRPO](https://arxiv.org/abs/2005.12729).

### Intervention-ladder paper

**Reader promise:** follow a sequence of intelligible research sprints. Each
stage begins with a defect or pressure in the now-familiar testbed, leads with
the intervention that worked, measures the improvement in the same visual
language, and leaves a residual problem that motivates the next stage. This is
the natural story-driven form for a long program whose chronology was messier
than the explanation needs to be.

Construct the ladder backward from the strongest supported end result, not
forward from the lab chronology. Before drafting, make an intervention evidence
matrix with one row per candidate rung: prior state and defect; the intervention
to credit; its intended difference; matched control or smallest isolating
contrast; result, uncertainty, breadth, and cost; and the residual that motivates
the next rung. Adaptive hill-climbing supplies candidate interventions, not
causal evidence. An expected ablation is a backfill specification until it runs.

A rung earns technique-level credit only when its evidence isolates the
intervention well enough for the claimed attribution. When a transition bundles
several changes, either run the deciding ablations, credit the bundle at system
level, or demote the transition from the ladder; do not project a clean causal
step onto an underidentified chronology. Promote a full rung when its effect is
material, its attribution is informative, it changes a decision, or the field
would benefit from additional confirmation of a less-reproduced technique.
Established low-value ingredients get a citation and a brief reproduction-ready
sketch, usually in a method bridge or appendix, while remaining visible as
controls when the attribution depends on them.

Use one repeated stage cadence:

1. **Pressure:** show the prior system's concrete defect, optionally with one
   representative example.
2. **Intervention:** state the smallest change being tested and why it addresses
   that defect.
3. **Evidence:** report a compact fixed scorecard—typically two to six
   decision-bearing quantities—in the same format. Carry one stable external
   reference throughout for cumulative comparability; when that differs from
   the matched prior-rung or control contrast, report both. The external delta
   never substitutes for the isolating contrast needed to credit a technique.
4. **Residual:** name what remains unsolved and why that motivates the next
   stage rather than merely following it in time.

Open with the terminal result, the task-level reference baseline, and a preview
of the ladder; let the repeated cadence establish credit. Close by comparing
the rungs' relative importance and ablations, then distinguish supported
resource regimes from proposals that would become attractive with more data,
teacher compute, or stronger models. Fair-comparison mechanics, full sweeps,
and secondary breakdowns may move to appendices, but the main path retains
enough evidence to understand and trust each credited delta.

The form boundary is the reader gift. Use recipe synthesis when the useful
product is a modular checklist whose ingredients need not occur in order. Use a
headline-result paper when the terminal result carries the paper and the stages
are merely implementation detail. Use an intervention ladder when understanding
the successive defects, credited fixes, and residuals is itself the transferable
result. Keep one paper when the rungs share a central task, testbed, and
comparison language; split a rung whose reader promise, evidence neighborhood,
or evaluation regime can stand on its own.

Examples: [A ConvNet for the
2020s](https://openaccess.thecvf.com/content/CVPR2022/html/Liu_A_ConvNet_for_the_2020s_CVPR_2022_paper.html)
and, in a more modular register, [Bag of
Tricks](https://openaccess.thecvf.com/content_CVPR_2019/html/He_Bag_of_Tricks_for_Image_Classification_with_Convolutional_Neural_Networks_CVPR_2019_paper.html).

It is legitimate to select the clearest true narrative after the work. It is
not legitimate to hide a failed attempt when that failure changes validity,
scope, expense, or causal attribution. Incidental dead ends can move to an
appendix; load-bearing negative evidence stays in the main account.

### Empirical-audit paper

**Reader promise:** learn which apparent advances survive a neutral,
standardized comparison. Reimplement or normalize the contenders, equalize
tuning and compute budgets, repeat across seeds and regimes, ablate confounds,
and report who the real winners are. A fresh evaluation protocol can be as
important as the ranking.

Examples: [Are GANs Created Equal? A Large-Scale
Study](https://papers.nips.cc/paper_files/paper/2018/hash/e46de7e1bcaaced9a54f1e9d0d2f800d-Abstract.html)
and [On the State of the Art of Evaluation in Neural Language
Models](https://openreview.net/forum?id=ByJHuTgA-).

### Simple-baseline reversal

**Reader promise:** much of the field's complexity is unnecessary once the
baseline is built and tuned properly. The pleasure is reversal: establish the
complicated conventional picture, introduce a legible baseline, and show that
it matches or beats the supposed advances under fair conditions. The paper
must make the baseline strong enough that “simple” does not mean undertuned.

Examples: [Simple Baselines for Human Pose Estimation and
Tracking](https://openaccess.thecvf.com/content_ECCV_2018/html/Bin_Xiao_Simple_Baselines_for_ECCV_2018_paper.html)
and [On the State of the Art of Evaluation in Neural Language
Models](https://openreview.net/forum?id=ByJHuTgA-).

### Diagnostic-instrument paper

**Reader promise:** use this metric, test, visualization, or troubleshooting
method to see something standard practice misses. Contrast the instrument with
existing diagnostics, demonstrate it on one or more concrete cases, and show
that the resulting observation changes a research or engineering decision.

Examples: [Beyond Accuracy: Behavioral Testing of NLP Models with
CheckList](https://aclanthology.org/2020.acl-main.442/), [Sanity Checks for
Saliency
Maps](https://proceedings.neurips.cc/paper/2018/hash/294a8ed24b1ad22ec2e7efea049b8737-Abstract.html),
and [Visualizing the Loss Landscape of Neural
Nets](https://proceedings.neurips.cc/paper_files/paper/2018/hash/a41b3bb3e6b050b6c9067c67f663b915-Abstract.html).

### Regime-change revisit

**Reader promise:** an old conclusion changes under today's scale, data,
frontier models, or hardware. Recreate the earlier question, sweep the changed
regime, and show which clever mechanisms have become unnecessary, newly
effective, or newly inadequate. The novelty is the interaction with the new
regime, not merely rerunning an old paper on a newer model.

Examples: [The Power of Scale for Parameter-Efficient Prompt
Tuning](https://aclanthology.org/2021.emnlp-main.243/) and [A ConvNet for the
2020s](https://openaccess.thecvf.com/content/CVPR2022/html/Liu_A_ConvNet_for_the_2020s_CVPR_2022_paper.html).

### Challenge-problem paper

**Reader promise:** here is a task or variation worth becoming obsessed with.
Define the construct and evaluation sharply, make the task feel useful or
intelligence-relevant, and show that plausible baselines fail in informative
ways. A solution is optional when the problem definition itself opens a
productive research program.

Examples: [On the Measure of
Intelligence](https://arxiv.org/abs/1911.01547), which introduces ARC;
[TruthfulQA](https://aclanthology.org/2022.acl-long.229/); and
[SWE-bench](https://proceedings.iclr.cc/paper_files/paper/2024/hash/edac78c3e300629acfe6cbe9ca88fb84-Abstract-Conference.html).

### Theorem-or-bound paper

**Reader promise:** obtain a crisp formal fact—an upper or lower bound,
universality result, separation, convergence theorem, or impossibility—and
understand what it rules in or out. The exposition earns its keep by making
the statement, proof idea, tightness, assumptions, and practical consequence
legible, even when the proof is the scientific payload.

Examples: [The Expressive Power of Neural Networks: A View from the
Width](https://proceedings.neurips.cc/paper/2017/hash/32cbf687880eb1674a07bf717761dd3a-Abstract.html)
and [Are Transformers Universal Approximators of Sequence-to-Sequence
Functions?](https://openreview.net/forum?id=ByxRM0Ntvr).

### Synthetic-microscope paper

**Reader promise:** a deliberately artificial task isolates a capability or
inductive bias that natural benchmarks entangle. Vary one structural axis,
show which architectures reliably can or cannot learn or extrapolate, and
connect the controlled separation back to a broader claim without pretending
the toy task is the world.

Examples: [Generalization without Systematicity
(SCAN)](https://proceedings.mlr.press/v80/lake18a.html), [Grokking:
Generalization Beyond Overfitting on Small Algorithmic
Datasets](https://arxiv.org/abs/2201.02177), and [Neural Networks and the
Chomsky Hierarchy](https://openreview.net/forum?id=WbxHAzkeQcn).

### Empirical-law paper

**Reader promise:** a compact curve, phase diagram, or named phenomenon
organizes many otherwise separate observations and predicts what happens
outside the measured cells. Sweep the controlling axes, fit or state the
regularity, test extrapolation, and emphasize breaks as much as the clean
central law.

Examples: [Scaling Laws for Neural Language
Models](https://arxiv.org/abs/2001.08361), [An Empirical Analysis of
Compute-Optimal Large Language Model
Training](https://proceedings.neurips.cc/paper_files/paper/2022/hash/c1e2faff6f588870935f114ebe04a3e5-Abstract.html),
and [Reconciling Modern Machine Learning Practice and the Bias-Variance
Trade-off](https://arxiv.org/abs/1812.11118).

### Failure-atlas paper

**Reader promise:** learn the shape of a failure, not merely that one example
failed. Organize defects across meaningful axes, give memorable cases, locate
boundary conditions, and replace a vague warning with a map that changes how
systems are evaluated or deployed.

Examples: [Underspecification Presents Challenges for Credibility in Modern
Machine Learning](https://jmlr.org/beta/papers/v23/20-1335.html) and [Gender
Shades](https://proceedings.mlr.press/v81/buolamwini18a).

### Corrective-metascience paper

**Reader promise:** see how the field's research process propagates false,
fragile, or irreproducible claims, then adopt a procedure that catches them.
The strongest version demonstrates the failure on cited work, distinguishes
reproducing code from reproducing a finding, and tests an actionable
replacement—seed discipline, stronger baselines, standardized reporting,
checklists, or artifact review.

Examples: [Deep Reinforcement Learning That
Matters](https://ojs.aaai.org/index.php/AAAI/article/view/11694),
[Unreproducible Research Is
Reproducible](https://proceedings.mlr.press/v97/bouthillier19a.html), and
[Improving Reproducibility in Machine Learning
Research](https://www.jmlr.org/papers/v22/20-303.html).

### Resource-release paper

**Reader promise:** receive a scarce research asset whose construction and
validation are themselves worth documenting: commissioned labels, a dataset,
a trained model, checkpoints, logs, or an open training stack. The paper
explains collection and curation, audits quality and limitations, establishes
useful baselines, and tells readers exactly what is and is not released.

Examples: [OpenAssistant
Conversations](https://proceedings.neurips.cc/paper_files/paper/2023/hash/949f0f8f32267d297c2d4e3ee10a2e7e-Abstract-Datasets_and_Benchmarks.html),
[Dolma](https://aclanthology.org/2024.acl-long.840/), and [OLMo: Accelerating
the Science of Language Models](https://aclanthology.org/2024.acl-long.841/).
A resource release is a paper form when the asset is the primary reader
promise; the same release is an attraction multiplier when attached to
another form.

### Research-engine paper

**Reader promise:** use this automated search, evolutionary, or agent-managed
loop to conduct research differently. Specify the loop and evaluator, compare
it with human or automated alternatives, and validate it through independently
checkable discoveries or research outcomes. Throughput or a self-review score
alone is weaker evidence than a new result that survives ordinary verification.

Examples: [AutoML-Zero](https://proceedings.mlr.press/v119/real20a),
[Discovering Faster Matrix Multiplication Algorithms with Reinforcement
Learning](https://www.nature.com/articles/s41586-022-05172-4), and
[Mathematical Discoveries from Program Search with Large Language
Models](https://www.nature.com/articles/s41586-023-06924-6). The
evaluation-centered adjacent form is exemplified by
[MLAgentBench](https://proceedings.mlr.press/v235/huang24y.html).

### Framework paper

**Reader promise:** acquire a vocabulary, decomposition, taxonomy, or reporting
schema that makes a confused area easier to reason about. A useful framework
does more than rename things: it makes distinctions that change analysis,
evaluation, documentation, or the next experiment, and demonstrates those
decisions in worked examples.

Examples: [A Mathematical Framework for Transformer
Circuits](https://transformer-circuits.pub/2021/framework/index.html), [Model
Cards for Model Reporting](https://research.google/pubs/model-cards-for-model-reporting/),
and [Datasheets for
Datasets](https://www.microsoft.com/en-us/research/publication/datasheets-for-datasets/).

## Coverage and limits

This is a grounded but representative taxonomy, not a systematic survey of
every machine-learning venue. Primary paper or proceedings pages were checked
through 2026-08-12, using exact-title searches around the proposed forms and
backward/forward movement among the cited examples. The list deliberately
samples recognizable papers across machine learning, natural-language
processing, computer vision, reinforcement learning, theory, and automated
discovery. It does not use citation counts, awards, or acceptance decisions to
rank forms, and it makes no causal claim about which structure reviewers
reward.
