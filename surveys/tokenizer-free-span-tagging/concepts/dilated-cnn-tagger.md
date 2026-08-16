# dilated-cnn-tagger — the speed case for a convolutional span tagger

> Read-backed digest `[G]` (cluster C, trust `single-source`). ID-CNN is the
> reference result for "a CNN tagger is as accurate as a BiLSTM-CRF and an order
> of magnitude faster." It is a *word*-input model, so it is not a chars-only
> system — but every speed argument for a convolutional span tagger descends
> from it, and its ablations say what makes a CNN tagger work.

**Paper.** Strubell, Verga, Belanger, and McCallum, "Fast and Accurate Entity
Recognition with Iterated Dilated Convolutions," EMNLP 2017 (also
arXiv:1702.02098). **Full text:**
[ACL page](https://aclanthology.org/D17-1283/) ·
[PDF](https://aclanthology.org/D17-1283.pdf) ·
local extract `related-work/extract/strubell2017-id-cnn/`.

## Mechanism

Dilated convolutions: a width-3 filter whose taps skip `2^n − 1` positions at
layer `n`, so the receptive field grows exponentially with depth while the
parameter count grows linearly and every position is computed in parallel. The
"iterated" part applies the *same* dilated block several times with tied
parameters, adding a loss term after each application. Prediction is greedy
per-token — no Viterbi — which is where the speed comes from.

The framing to reuse: a recurrent tagger costs `O(N)` sequential steps for a
sentence of length `N`; a fixed-depth convolution costs `O(1)` sequential steps
regardless of `N`, up to hardware limits. That argument gets *stronger*, not
weaker, when the sequence is characters rather than words, because character
sequences are 4–8× longer.

## Evidence

CoNLL-2003 English test F1, no character embeddings and no lexicons in any row,
averaged over 10 restarts:

| model | F1 | relative test-time speed |
|---|---|---|
| Bi-LSTM | 89.34 ± 0.28 | 9.92× |
| 4-layer CNN | 89.97 ± 0.20 | — |
| 5-layer CNN | 90.23 ± 0.16 | 12.38× |
| ID-CNN (greedy) | 90.32 ± 0.26 | **14.10×** |
| Bi-LSTM-CRF | 90.43 ± 0.12 | 1× |
| ID-CNN-CRF | 90.54 ± 0.18 | 1.28× |

Reading the two columns together: greedy ID-CNN matches Bi-LSTM-CRF accuracy
(−0.11 F1, well inside the CoNLL ±0.8 significance width) at **14× the decoding
speed**, and as a logit extractor under Viterbi it slightly beats it. Every CNN
variant beats the Bi-LSTM at equal parameters.

With document-level rather than sentence-level context, greedy ID-CNN reaches
90.65 ± 0.15 versus Bi-LSTM-CRF's 90.60, still decoding nearly 8× faster; the
CNN gains more from long context than the recurrent model does, which the
authors attribute to the LSTM's limits past ~1 000 tokens.

Two ablations that matter for building one:

- **Parameter sharing across iterations is load-bearing:** ID-CNN 90.65 vs.
  90.06 with a single final loss vs. 89.81 with untied blocks.
- **Dropout with expectation-linear regularization** improved every model tried,
  by +0.23 to +0.67 F1 (e.g. 4-layer ID-CNN 89.65 → 90.32).

## Contested and negative details

- The speeds are 2017 TensorFlow measurements at each model's best batch size,
  on models without character embeddings. The authors note their dilated
  implementation was naive and estimate up to 18× with a better one; equally, a
  modern fused LSTM or a transformer baseline would change the ratio. Treat the
  *order* of magnitude as the finding, not the exact multiplier.
- Accuracy differences among the CNN variants (89.97 / 90.23 / 90.32) are inside
  the benchmark's significance width. The defensible claim is "CNN taggers reach
  BiLSTM-CRF accuracy", not "dilation is worth 0.35 F1".
- Nothing here is character-level. The input is word embeddings, so the model
  inherits a vocabulary and its memorization channel.

## Design edge and limits

For a chars-only convolutional tagger this supplies: the depth-for-receptive-
field trick (dilation), the tied-block-with-intermediate-loss recipe, greedy
decoding as a deliberate speed choice with a measured accuracy cost near zero,
and the parallel-across-positions argument that motivates choosing convolution
over recurrence at character length. What it does not supply is any evidence
about character input, multilinguality, or how much of its 90 F1 comes from
GloVe-style word vectors it no longer has.
