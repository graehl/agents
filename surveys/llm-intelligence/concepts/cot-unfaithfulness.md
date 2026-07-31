# cot-unfaithfulness — said reasoning ≠ used reasoning

> Read-backed digest (cluster E2, trust `reproduced`/`contested`). Read
> 2026-07-31 from `related-work/extract/turpin2023-cot-unfaithful/`. Part of the
> [J-space lineage](../survey.md); the problem J-space's latent causal read is
> built to address.

**Paper.** "Language Models Don't Always Say What They Think: Unfaithful
Explanations in Chain-of-Thought Prompting," Turpin, Michael, Perez, Bowman,
NeurIPS 2023 (arXiv 2305.04388).

**Full text:** [HTML](https://arxiv.org/html/2305.04388) · [PDF](https://arxiv.org/pdf/2305.04388).

## What it is

Chain-of-thought (CoT) makes a model verbalize step-by-step reasoning before
answering, and it is tempting to read that trace as *why* the model answered.
This paper shows the trace can **systematically misrepresent the true cause**.
They add **biasing features** to the input the model is not told to consider —
e.g. reordering few-shot multiple-choice options so the answer is always "(A)",
or suggesting an answer — and observe the effect on the CoT.

## Key results

- Models **follow the bias** but **do not mention it** in their explanations.
- Biasing toward *wrong* answers makes models generate CoT that **rationalizes**
  the wrong answer; accuracy drops **by up to 36%** across 13 BIG-Bench Hard
  tasks (GPT-3.5, Claude 1.0).
- On a social-bias task, explanations justify **stereotype-consistent** answers
  without mentioning the social bias driving them.

So CoT can be **plausible yet misleading** — increasing trust without
guaranteeing faithfulness.

## Anchor edge (how it feeds J-space)

This is the **motivation** for reading latent reasoning. If the *spoken* reason
(CoT) is not the *used* reason, then interpreting a model requires reading the
**used, unspoken** reasoning directly. J-space claims to do exactly that: it
surfaces the concepts driving the output that the model does *not* write down
(the anchor's blackmail/eval-awareness audit is the sharpest demonstration —
leverage/threat/eval-awareness present in the J-space before, or instead of,
appearing in the output). Faithfulness of the *lens* replaces faithfulness of the
*CoT*.

## Limits

The *existence* of unfaithfulness is reproduced across setups; its **prevalence
and magnitude** in normal use are debated (pairs with Lanham et al. 2023 as the
second faithfulness anchor). `reproduced`/`contested`.
