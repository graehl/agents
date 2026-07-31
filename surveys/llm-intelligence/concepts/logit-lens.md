# logit-lens — decoding hidden states with the unembedding

> Read-backed digest (cluster B2, trust `folklore`). Read 2026-07-31 from
> `related-work/extract/nostalgebraist2020-logit-lens/`. Part of the
> [J-space lineage](../survey.md); the origin of the "decode a hidden state into
> vocabulary" family.

**Source.** nostalgebraist, "interpreting GPT: the logit lens," LessWrong, 2020.
**Full text:** [interpreting GPT: the logit lens](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens) (LessWrong post).

## What it is

Apply the model's own **unembedding matrix `W_U`** (with the final layer-norm)
directly to an *intermediate* residual-stream activation, as if decoding the
next token "early." Zero cost, no training — just read each layer's hidden state
through the output head. Plotting the top-1 token per (layer, position) shows the
model's prediction forming across depth.

## What it shows

On GPT-2 decoding a mid-abstract passage, the top guess **converges smoothly**
toward the final prediction: a "good guess" appears mid-stack and is refined in
the last layers (logit of the top guess rises steadily). So the network is doing
*iterative inference* — successive layers sharpen a latent next-token
distribution. This is a qualitative intuition tool, and it revealed that
intermediate states are already vocabulary-decodable.

## Anchor edge (how it feeds J-space)

The **origin lens**, and the exact thing J-lens generalizes. In the anchor's
formulation the logit lens is the **special case `J_ℓ = I`** — the raw
unembedding with no correction for how representations change across layers.
That is why it "degrades in earlier layers": it assumes every layer uses the
final layer's coordinates. J-lens replaces `I` with the averaged Jacobian
`J_ℓ` (the layer-ℓ → final map), recovering interpretable content where the
logit lens produces noise. The whole B-cluster (tuned lens, J-lens) is a
sequence of corrections to this idea.

## Limits

Brittle in early layers; **basis-dependent** (representational drift across
layers); **correlational, not causal**; unreliable across models (Belrose et al.
found it fails to elicit plausible predictions on BLOOM and GPT-Neo). A
widely-used diagnostic whose known-unreliable early-layer behavior is folklore.
The anchor still finds it "quite useful in practice," capturing much
workspace-like structure at lower reliability than the J-lens.
