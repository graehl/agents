# Output probabilities expose structure that sampled text hides

Grounded, selective primary-source reading through 17 October 2026. Published
measurements below are `single-source`, not reproduced here. The linear-algebra
and sampling arguments are analytical deductions with explicit assumptions.

## The interface determines which experiments are possible

| Available readout | What it supports | What it leaves unavailable |
|---|---|---|
| Generated text | Labels, explanations, repeated-sample estimates | Exact probability differences and most rare alternatives |
| Selected-token probabilities | Fixed answer contrasts and calibrated scores | Unrequested vocabulary coordinates |
| Top-\(k\) probabilities | Likely alternatives and censored response profiles | Missing candidates are not zero-probability events |
| Full next-token distribution | Vocabulary-wide geometry, tail analysis, and sequence scores through repeated prefix queries | Intermediate layers and causal location |
| Likelihood of supplied continuations | Conditional sequence scoring | Internal interventions |

“Logits enabled” must be refined to one of these interfaces. A normalized
log-probability differs from a raw logit by a prompt-dependent additive
constant. Pairwise log-odds survive; raw-logit thresholds need not. The
survey assumes the stated readout exists and makes no claim that every
current commercial endpoint exposes it. Teacher-forced scoring of a supplied
string is a separate capability from returning probabilities for generated
tokens. With a full next-token distribution, supplied-string likelihood can
also be assembled one prefix at a time, at up to one call per scored token;
one-pass prompt-token scoring is much cheaper. Logit bias is another separate
capability.

## The final representation is partly identifiable; its native basis is not

For a linear output head, let \(z(x)=Wh(x)+b\) and
\(p(x)=\operatorname{softmax}(z(x))\). With
\(C=I-\mathbf{1}\mathbf{1}^{T}/V\), centering removes the normalization:

\[
C\log p(x)=CW h(x)+Cb.
\]

Across prompts this reveals an affine image of the final representation. If
\(CW\) has full column rank, no information in that final vector is lost by
this mapping. Without the weights, however, a factorization does not fix its
native basis: \(Wh=(WA^{-1})(Ah)\) for invertible \(A\). Architectural
constraints can restrict this ambiguity without identifying earlier neurons.
Linear separability and dimension can survive a change of basis while cosine
similarity and individual coordinate meanings do not. Estimated rank is not
the number of concepts.

[Finlayson, Ren, and Swayamdipta, *Logits of API-Protected LLMs Leak
Proprietary Information* (COLM 2024)](https://arxiv.org/html/2403.09539v3)
exploit the low-dimensional output subspace to estimate hidden size, identify
model changes, and reduce repeated full-distribution extraction cost after
learning a basis. Their top-probability API extraction also uses logit bias;
top probabilities alone do not imply that algorithm is available. This is
direct evidence for accessible final-state structure, not semantic localization.

[Carlini et al., *Stealing Part of a Production Language Model*
(ICML 2024)](https://arxiv.org/html/2403.06634v2) recover output projections
up to symmetries under specified query interfaces. Their historical extraction
costs are not current pricing or endpoint guarantees. The result concerns the
output head, not recovery of the model's internal computational graph.

## Tail probabilities can carry useful detail

[Morris et al., *Language Model Inversion* (ICLR 2024)](https://arxiv.org/html/2311.13647)
train an inverter to reconstruct input text from next-token distributions.
On their held-out instruction data, full-distribution inversion of
Llama-2-7B-chat exactly recovers 23.4% of inputs, versus 0% for their
sample-based inverter. Truncating the distribution loses information; rare
alternatives can preserve input details that scarcely affect likely next
tokens. This measures prompt recovery with a trained decoder, not recovery
of concept identities.

For a fixed one-token event of probability \(p\), independent sampling gives
variance \(p(1-p)/n\). Achieving relative standard error \(r\) needs roughly
\(n=(1-p)/(pr^2)\) samples: \(p=0.01\), \(r=0.1\) gives 9,900 draws.
Direct probability readout removes that sampling cost. It does not remove
prompt sensitivity, dataset uncertainty, probability calibration error, or the
cost of evaluating many prompts. This is a sampling calculation, not a measured
API speedup. Full-distribution recovery through many biased queries can erase
the practical saving.

## Prompt interventions identify behavioral dependence

A prompt asking about a concept creates a new computation. Its answer
distribution measures that computation, not a passive read of the state from
an earlier unmodified prompt. Context swaps, paraphrases, label permutations,
and contrastive log-odds can establish stable output distinctions and
input-output causal effects. They cannot by themselves show that one neuron,
site, or circuit implements the distinction: different internal mechanisms
can produce the same observations.

Use logits to discover and quantify candidate distinctions; use an open model
to test whether those distinctions predict separable internal mechanisms.
[Prompted concept methods](prompted-concepts.md) provide concrete precedents
for the first stage; [the survey experiment](../survey.md#calibrating-concept-surfaces-on-an-open-model)
connects it to the second.
