# Fill-in-the-middle — infilling for decoder-only models

> Read-backed digest (cluster: decoder-only infilling, trust `single-source`;
> infilling benchmarks are code-only).

**Paper.** Bavarian, Jun, Tezak, Schulman, McLeavey, Tworek and Chen,
“Efficient Training of Language Models to Fill in the Middle,” arXiv 2022
([HTML](https://arxiv.org/html/2207.14255v1),
[PDF](https://arxiv.org/pdf/2207.14255v1),
[local extract](../related-work/extract/bavarian2022-fim/html/2207.14255v1.md)).

## Mechanism

FIM is a data transformation; the causal decoder is unchanged. With
probability \(p\) (the FIM rate), a training document is cut at two
character-level random points into prefix, middle and suffix. It is then
reordered as `<pre> prefix <suf> suffix <mid> middle` (PSM), or with the
suffix first (SPM). Loss is kept on every section, and generation of the
middle stops at an end-of-text token. The model thereby learns to condition on
text that follows the gap without bidirectional attention. The suffix is just
earlier context.

FIM is the decoder-only route to what span corruption gives an
encoder-decoder. It handles one span per document rather than many, and
attention stays causal, so the suffix's own probability never depends on the
middle.

## Evidence

- **FIM-for-free.** At a 50% FIM rate, left-to-right test loss and standard
  benchmarks (HellaSwag, LAMBADA, HumanEval and others) match a plain
  autoregressive model across 8 sizes from 50M to 6.9B, each trained on 100B
  tokens (`single-source`; values in figures only).
- **FIM rate.** Up to 0.9, left-to-right loss is unharmed; at 1.0 it degrades.
  Infilling pass rates rise with the rate and stop improving beyond 0.9. The
  recommendation is 0.5–0.9 (`single-source`).
- **Pretrain, don't retrofit.** Adding FIM to a pretrained model by
  fine-tuning matched FIM pretraining only with 50B extra tokens at rate 0.9
  and full learning rate, 50% on top of the original budget
  (`single-source`).
- **Character-level cuts matter.** On random-span infilling, character-level
  spans score .321 against .102 for token-level spans, which never teach the
  model to finish a subword (`single-source`).
- **Scale.** At 6.9B with 90% FIM, SPM-mode pass rates are .751/.441/.551 on
  single-line, multi-line and random-span infilling, ahead of InCoder-6.7B's
  self-reported .690/.386 (`single-source`).

## Decision edge and limits

FIM is why “use span denoising” no longer implies an encoder-decoder. A
decoder-only LLM can learn infilling at negligible cost to ordinary
generation, provided it is in the pretraining mix. The evidence is for code
and single-gap infilling. Natural-language infilling is judged only
qualitatively and is worse than code. The authors could not rule out tasks
where FIM models are worse.
