# MASS — one masked span, predicted by the decoder

> Read-backed digest (cluster: single-span seq2seq, trust `single-source`;
> MT comparisons copy baseline numbers from XLM rather than rerunning them).

**Paper.** Song, Tan, Qin, Lu and Liu, “MASS: Masked Sequence to Sequence
Pre-training for Language Generation,” ICML 2019
([HTML](https://arxiv.org/html/1905.02450v5),
[PDF](https://arxiv.org/pdf/1905.02450v5),
[local extract](../related-work/extract/song2019-mass/html/1905.02450v5.md)).

## Mechanism

Mask one contiguous fragment of each sentence, about half its tokens, in the
encoder input. Masked positions follow BERT's 80/10/10 rule: [M], a random
token, or unchanged. The decoder predicts only that fragment, left to right.
Its inputs are the fragment shifted right, and every position outside the
fragment is masked on the decoder side. Positions unmasked in the encoder are
therefore masked in the decoder. The decoder must read the encoder to know the
context, and the encoder must understand context to help it. Dropping the
decoder's masked padding while keeping positional embeddings halves decoder
compute.

The fragment length \(k\) interpolates between the two familiar objectives:

- **\(k=1\)** leaves the decoder no input tokens, so it acts as a classifier
  over the encoder state, which is BERT's masked language model (MLM).
- **\(k=m\)**, the whole sentence, leaves the encoder nothing, which is GPT's
  left-to-right language model.

The MASS claim is that the middle, \(k\approx 50\%\), pretrains encoder,
decoder and cross-attention together for generation. BERT pretrains only an
encoder and GPT only a decoder. XLM pretrains both but separately, so its
cross-attention starts untrained.

The MT models are small by current standards: 6+6 layers at width 1024. They
are pretrained per language pair on that pair's monolingual News Crawl, with
a language embedding and a joint 60k BPE vocabulary.

## Evidence

- **Unsupervised MT.** MASS reaches 37.50 BLEU on newstest2014 en-fr, against
  33.40 for the best XLM configuration and 25.14 without pretraining. It leads
  XLM by 0.9–4.1 BLEU on all six directions (en-fr, en-de, en-ro, both ways)
  (`benchmark-reported`). Fine-tuning used back-translation only.
- **Objective comparison.** An MLM encoder with a separately pretrained LM
  decoder (BERT+LM) and a denoising autoencoder trail MASS on all six
  directions; en-fr is 33.4 and 30.1 against 37.5 (`single-source`). This
  comparison is not controlled. The BERT+LM numbers are copied from XLM, and
  those arms were fine-tuned with a different recipe (denoising plus
  back-translation).
- **Span length.** Sweeping \(k\) from 10% to 90%, unsupervised en-fr BLEU
  peaks near 50%. The authors report that neither \(k=1\) nor \(k=m\) is good
  (`single-source`; values in a figure only).
- **Decoder masking matters.** On unsupervised en-fr, masking discrete tokens
  instead of one span gives 36.9; showing the decoder all tokens gives 35.3;
  MASS gives 37.5 (`single-source`).
- **Low-resource MT.** With 10K–1M sampled pairs, MASS beats no pretraining
  in all six directions (`single-source`; figure only, and no stronger
  pretrained baseline).

## Decision edge and limits

MASS is evidence about the objective inside an encoder-decoder: the decoder
must depend on the encoder for its context. It is not evidence for
encoder-decoder over decoder-only architectures. Its MT regimes are
unsupervised and simulated low-resource, with no full-bitext supervised
result. The later [BART](text-infilling.md) ablation found a MASS-like
objective competitive for generation but weaker for understanding tasks,
because encoder and decoder see disjoint tokens. Today's large models do not
use it. The surviving ideas are span-level masking and pretraining the
cross-attention, now carried by [span corruption](span-corruption.md) and
[UL2](mixture-of-denoisers.md).
