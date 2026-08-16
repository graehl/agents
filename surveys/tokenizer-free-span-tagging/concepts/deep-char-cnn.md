# deep-char-cnn — what the deep character-CNN lineage established (and on what task)

> Read-backed digest `[G]` (cluster C, trust `single-source` each). Zhang et al.
> and Conneau et al. are the reference points for "a deep CNN straight over
> characters." Both are **text classification, not span tagging** — cite them for
> depth/width/regularization/alphabet design and for the data-scale requirement,
> never as evidence that a char CNN tags spans.

**Papers.** Zhang, Zhao, and LeCun, "Character-level Convolutional Networks for
Text Classification," NeurIPS 2015; Conneau, Schwenk, Barrault, and LeCun, "Very
Deep Convolutional Networks for Text Classification," EACL 2017 (VDCNN).
**Full text:** [Zhang arXiv](https://arxiv.org/abs/1509.01626) ·
[Zhang PDF](https://arxiv.org/pdf/1509.01626) ·
[VDCNN ACL page](https://aclanthology.org/E17-1104/) ·
[VDCNN PDF](https://aclanthology.org/E17-1104.pdf) ·
local extracts `related-work/extract/zhang2015-char-cnn/`,
`related-work/extract/conneau2017-vdcnn/`.

## Mechanisms

Zhang et al.: a 70-symbol alphabet (26 letters, 10 digits, 33 punctuation, plus
newline), one-hot per character, a fixed 1 014-character window, six temporal
convolution layers with max-pooling, then three fully connected layers with
dropout 0.5. Out-of-alphabet and blank characters become all-zero vectors.

VDCNN: kernel size 3 throughout, convolutional *blocks* of two conv layers each
with temporal batch normalization and ReLU, halving temporal resolution at
pooling stages while doubling filters (64 → 128 → 256 → 512). Depths of 9, 17,
29 and 49 convolutional layers, plus optional ResNet-style shortcut connections.

## Evidence

**Depth pays, up to a limit that shortcuts move.** VDCNN test error falls
monotonically from depth 9 to 17 to 29 across all eight datasets and all three
pooling types (with 2 exceptions in 48 comparisons); best depth-29 max-pooling
reaches 37.0% error on Amazon Full versus 40.43% for the prior state of the art.
Pushing to 49 layers *without* shortcuts degrades sharply (Yelp Full: 35.28 →
37.41 test error, train error 29.57 → 35.54); with shortcuts, depth 49 trains
and tests better than it did without, though it did not beat depth 29 overall.
Temporal max-pooling beat k-max and strided-convolution pooling at small depth.

**Character CNNs need a lot of data.** Zhang et al.'s explicit finding: n-gram
TFIDF baselines remain competitive up to several hundred thousand training
samples, and character CNNs only pull ahead at the scale of several million.
They also report the models work relatively better on less-curated user-generated
text (Amazon reviews) than on curated text (Yahoo Answers), and that *not*
distinguishing upper and lower case usually works better — a smaller alphabet
acting as regularization.

## Contested and negative details

- Neither paper does sequence labeling. Their outputs are document classes, so
  the pooling that makes them work (temporal max-pooling, a fixed 1 014-character
  window) is precisely what a per-position span tagger cannot use unmodified.
- Zhang et al.'s "ConvNets are good at exotic character combinations" hypothesis
  is explicitly *not* established by their experiments — they say so.
- The 3.43-point absolute gain VDCNN reports is against Zhang et al.'s
  convolutional baselines on their own datasets; both papers largely evaluate on
  the same eight constructed corpora, so this lineage is internally
  self-referential.

## Design edge and limits

For a chars-only span tagger the transferable claims are: prefer depth over
width with small (width-3) kernels; add residual connections before going past
roughly 30 layers; batch/layer normalization inside each block; regularize
through the input representation (case folding, character dropout); and expect
to need a large training set — which, since span-labelled data is scarce, is the
argument for manufacturing supervision by distillation. What does not transfer:
the pooling-to-a-single-vector topology, the fixed input window, and any claim
about entity spans.
