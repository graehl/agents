# T5 span corruption and the text-to-text comparison

> Read-backed digest (cluster: span corruption, trust `single-source` for the
> controlled comparisons, `benchmark-reported` for final WMT results). The
> controlled runs use 220M-parameter English-pretrained models, a 2019 scale.

**Paper.** Raffel et al., “Exploring the Limits of Transfer Learning with a
Unified Text-to-Text Transformer,” JMLR 21(140), 2020
([HTML](https://arxiv.org/html/1910.10683v4),
[PDF](https://arxiv.org/pdf/1910.10683v4),
[local extract](../related-work/extract/raffel2020-t5/html/1910.10683v4.md)).

## Mechanism

**Span corruption** drops 15% of tokens in contiguous spans with mean length
3. Each span is replaced by one sentinel token, unique within the example. The
encoder reads the corrupted text. The decoder writes only the dropped spans,
each led by its sentinel:

```text
input:  Thank you <X> me to your party <Y> week.
target: <X> for inviting <Y> last <Z>
```

Short targets make it cheaper than reconstructing the whole input, which is
[BART's text infilling](text-infilling.md). Every task, translation included,
is cast as text in and text out, with a task prefix such as
`translate English to German:`.

The paper's controlled comparison counts an L-layer encoder plus L-layer
decoder (2P parameters) as having the compute of a single L-layer decoder
(M FLOPs per example). The reason is that each token passes through only one
stack. It compares five arms:

- an encoder-decoder (2P, M);
- the same with shared parameters (P, M);
- a half-depth encoder-decoder (P, M/2);
- a causal decoder-only LM (P, M);
- a prefix LM: a decoder with bidirectional attention over its input (P, M).

## Evidence

- **Architecture ranking for translation.** Pretraining with denoising, WMT
  validation BLEU for EnDe, EnFr and EnRo, single runs with a rerun standard
  deviation of about 0.1 (`single-source`):

  | arm | EnDe | EnFr | EnRo |
  |---|---|---|---|
  | encoder-decoder | 26.98 | 39.82 | 27.65 |
  | shared-parameter encoder-decoder | 26.72 | 39.03 | 27.46 |
  | prefix LM | 26.43 | 37.98 | 27.39 |
  | causal LM | 25.09 | 35.28 | 25.86 |

  Even at equal parameters the shared encoder-decoder beats the prefix LM; the
  EnRo gap is within noise. The authors credit explicit encoder-decoder
  attention.
- **Objective barely matters for translation.** Prefix LM, BERT-style,
  span-replacement and drop-token objectives, corruption rates of 10–50%, and
  mean span lengths of 2–10 all fall within about 0.5 BLEU on the WMT tasks.
  Span length 3 was chosen for speed and a small non-translation gain
  (`single-source`).
- **English-only pretraining helps translation little.** Without pretraining,
  the baseline gets 25.86/39.77/24.04. A purely supervised multi-task
  pretraining matched or beat unsupervised pretraining only on translation
  (`single-source`).
- **No state of the art.** T5-11B reached 32.1/43.4/28.1 on the WMT test sets
  against 33.8/43.8/38.5 for back-translation and cross-lingual systems.
  EnRo stayed at 28.0–28.2 from Base to 11B. The authors attribute this to
  English-only pretraining and the lack of back-translation
  (`benchmark-reported`).

## Decision edge and limits

T5 is the source of the claim that encoder-decoders suit translation, and the
claim is narrow. It holds at 220M parameters, with English-only pretraining,
one factor varied at a time, and an accounting that gives the encoder-decoder
twice the parameters at equal FLOPs. Larger studies that train both from
scratch ([RedLLM](encoder-decoder-scaling.md)) or adapt a strong decoder
([T5Gemma](encoder-decoder-adaptation.md), [T5Gemma 2](t5gemma-2.md)) do not
reproduce a translation advantage for the encoder-decoder. That grades the
T5-era ranking `contested` once scale and multilingual pretraining enter.
