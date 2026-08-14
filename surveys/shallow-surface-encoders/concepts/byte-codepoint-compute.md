# byte-codepoint-compute — trade vocabulary for sequence path

> Read-backed digest (cluster H, trust `single-source` each). Raw bytes provide
> a fixed multilingual alphabet and exact coverage, but UTF-8 expands many
> non-Latin codepoints into two to four recurrent or convolutional steps. Local
> composition and reversible byte-subword compression are the established ways
> to recover context and shorten that path.

**Papers.** Gillick et al., “Multilingual Language Processing From Bytes,”
NAACL 2016; Costa-jussà et al., “Byte-based Neural Machine Translation,”
SCLeM 2017; Cherry et al., “Revisiting Character-Based Neural Machine
Translation with Capacity and Compression,” EMNLP 2018; Wang, Cho, and Gu,
“Neural Machine Translation with Byte-Level Subwords,” AAAI 2020; Khan, Xu,
and Sun, “Coding Textual Inputs Boosts the Accuracy of Neural Networks,” EMNLP
2020; Shaham and Levy, “Neural Machine Translation without Embeddings,” NAACL
2021; Xue et al., “ByT5,” TACL 2022; Libovický, Schmid, and Fraser, “Why don't
people use character-level machine translation?,” Findings of ACL 2022;
Wolleb et al., “Assessing the Importance of Frequency versus Compositionality
for Subword-based Tokenization in NMT,” EAMT 2023; Limisiewicz et al., “MYTE,”
ACL 2024; Zheng et al., “Proxy Compression for Language Modeling,” ICML 2026.

**Full text:**
[Gillick PDF](https://aclanthology.org/N16-1155.pdf) ·
[Costa-jussà PDF](https://aclanthology.org/W17-4123.pdf) ·
[Cherry PDF](https://aclanthology.org/D18-1461.pdf) ·
[Wang arXiv HTML](https://arxiv.org/html/1909.03341) ·
[Khan PDF](https://aclanthology.org/2020.emnlp-main.104.pdf) ·
[Shaham PDF](https://aclanthology.org/2021.naacl-main.17.pdf) ·
[ByT5 PDF](https://aclanthology.org/2022.tacl-1.17.pdf) ·
[Libovický PDF](https://aclanthology.org/2022.findings-acl.194.pdf) ·
[Wolleb PDF](https://aclanthology.org/2023.eamt-1.14.pdf) ·
[MYTE PDF](https://aclanthology.org/2024.acl-long.804.pdf) ·
[Proxy Compression HTML](https://arxiv.org/html/2602.04289).

## Direct byte and character evidence

Costa-jussà et al. give the cleanest located byte-versus-Unicode-character
comparison under one recurrent translation architecture. Across their tested
directions, byte BLEU differs from characters by roughly -3.3 to +0.8; German
is the conspicuous byte loss. Byte runs often converge hundreds of iterations
earlier, but the old training setup does not provide a strict fixed-FLOP
comparison. This is mixed evidence, not a general byte win.

Gillick et al. feed UTF-8 bytes one at a time to stacked long short-term memory
(LSTM) networks and predict span triples for multilingual part-of-speech and
named-entity tasks. Sixty-byte windows with overlap and byte dropout make the
system operationally relevant to span labeling, but its baselines and model
scale predate modern multilingual encoders. Shaham and Levy later show that a
byte-to-byte translation model can omit learned input embeddings entirely;
their advantage is partly explained by dropout on one-hot decoder inputs acting
as byte dropout.

ByT5 makes raw bytes competitive at large scale by reallocating vocabulary
parameters to a deeper encoder. It reports stronger noise, spelling, and some
multilingual robustness, while also reporting longer sequences, more FLOPs,
and slower inference than token models. Libovický et al. supply the useful
negative: modern character translation remains generally slower and below
subword quality in their comparisons, although it is distinctly robust to
source noise. Sufficient capacity and depth matter—Cherry et al. find deep
character encoders can beat matched subword systems, while temporal compression
mainly trades quality for speed. These results are all task- and
architecture-sensitive.

## Local context and reversible compression

UTF-8 is self-delimiting, so a local model can infer lead and continuation
bytes, but it must spend capacity and sequential depth doing so. Wang et al.'s
byte-level byte-pair encoding (BBPE) is a practical middle point: learn frequent
variable-length byte substrings, with every token expanding deterministically
back to its bytes. It is dictionary compression rather than an entropy code.
The modeled sequence shortens by paying for a larger symbol vocabulary.

BBPE symbols may contain partial characters, so Wang et al. contextualize their
embeddings with either a one-layer width-five depthwise convolution or a
bidirectional gated recurrent unit (GRU). On their 58-language-to-English
setting, the GRU improves BBPE validation BLEU by more than 4% relative across
the tested vocabulary sizes. A 4K BBPE source averages 65 symbols per sentence,
between raw bytes at 126 and character symbols at 89, while the 16K
character-BPE baseline averages 40. BBPE is therefore evidence for early local
composition plus compression, not evidence that isolated byte symbols suffice.
The paper does not ablate partial-character merges against otherwise matched
character-boundary-constrained merges.

Land and Arnett provide that tokenizer-level ablation in
[SCRIPT](https://arxiv.org/html/2505.24689). They require byte-BPE to finish one
Unicode character before merging sequences of complete characters. Across all
tested encodings and corpora, the constraint eliminates mixed
full/partial-character tokens and almost universally improves compression. For
example, mean tokens per character change from .333 to .332 under their
`cl100k` pretokenizer and .282 to .280 under `o200k`, while mixed partial UTF-8
tokens fall from 1,678/5,193 to 209/183. The remaining partial tokens are
contained within one character rather than mixing fragments across character
boundaries. This is direct evidence against treating arbitrary cross-character
byte fragments as a useful unit; downstream model-quality evidence is still
absent.

MYTE changes the reversible byte code itself. It assigns two-to-four-byte codes
to frequent morphemes learned separately across 99 languages and script groups.
Against UTF-8 it shortens every analyzed language, from about 1% for Vietnamese
and Chinese to about 70% for Burmese, and sharply reduces the non-Latin
sequence-length disparity. Its ByT5-sized model is faster and much better on
its language-modeling normalization, but downstream effects are mixed: the
reported low-resource NER average is 80.8 F1 versus 81.5 for ByT5. The map is
corpus- and morphology-analyzer-dependent and does not help a script absent
from its codebook.

For a token-aligned sidecar, byte merges should first complete one Unicode
codepoint and multi-character compression should remain inside the incumbent
SentencePiece token spans. This preserves both valid character units and a fixed
gather from surface positions to semantic tokens. The surface encoder may still
carry convolutional or recurrent context across marked token boundaries; only
the merge/compression units are boundary-constrained. Arbitrary partial-character
merges belong only in a later malformed/noisy-byte control.

## Entropy codes and learned compressed views

Khan et al. are the nearest located binary-Huffman precedent. They encode
words—where their discussion permits subwords or characters as the underlying
symbols—into fixed base-*b* code sequences, including base two, and also test a
frequency-based Huffman extension. The coded stream is auxiliary or is
recombined before the main network; it is not a sole raw-bit encoding of each
Unicode codepoint. Huffman adds at most a small constant improvement over
random fixed codes in their reported setting.

Wolleb et al. use *n*-ary frequency-Huffman word tokenization with alphabets
from 1K to 32K. At 8K and above, it reaches roughly 86–91% of byte-pair
encoding's BLEU, 91–95% of its ChrF, and 92–96% of its COMET. Larger alphabets
shorten paths but do not add subword compositionality or unseen-word
generalization. This explains the appeal of *n*-ary rather than bitwise codes:
Huffman minimizes storage bits, whereas a neural encoder pays separately for
each recurrent/convolutional position.

Zheng et al. train causal code models on both raw bytes and compressed proxy
views. Tokenizer and neural arithmetic proxies compress their code corpus about
2.9 and 2.6 times; a gzip proxy transfers weakly or negatively because small
source changes can cause unstable compressed sequences. Their neural proxy
packs 16-bit chunks into a 65,536-symbol alphabet. Improvements appear mainly
at billion-parameter scale and in code modeling, so the paper supplies a
compression-design warning rather than a small bidirectional-sidecar recipe.
No paper in this search used a binary Huffman code of Unicode codepoints as the
sole input to a comparable text encoder.

## Fixed-compute accounting

The following is an engineering derivation, not a reported paper result. Let
`b` be mean UTF-8 bytes per Unicode codepoint on the actual corpus. For a dense
convolution whose dominant work is proportional to `L k C² D`, replacing
codepoints by raw bytes raises work by about `b` at fixed kernel, width, and
depth. A first fixed-compute approximation is therefore
`C_byte ≈ C_codepoint / sqrt(b)`. A recurrent or state-space layer with work
proportional to `L C²` has the same first-order width trade. Activations rise
about `b` times; dense attention rises about `b²` before downsampling.

Equal kernel width is also unequal semantic reach. A byte network needs about
`b` times as many positions to cover the same codepoint interval, so widening
the receptive field compounds the fixed-compute penalty. Measure `b` by
language on the target corpus and report both effective codepoint receptive
field and actual measured throughput; one global theoretical ratio can hide
large Latin/CJK differences.

## Design boundary for a small surface encoder

The decision-relevant controls are:

1. literal Unicode codepoints, the strongest small clean-text fixed-compute
   prior;
2. raw UTF-8 bytes with codepoint-completing local composition or
   character- and SentencePiece-boundary-constrained BBPE, which buys exact
   coverage and noise tolerance at longer path length; and
3. SCRIPT `(block, index)` addresses, tested both as one paired position and as
   an alternating disjoint typed stream.

An alternating SCRIPT stream has exactly two positions per codepoint. Its
lowest composer should have enough nonlinear interaction capacity to
distinguish observed block/index pairs, without adding a pair-specific lookup
table that simply recreates codepoint identity. A small multilayer gated
composer or low-rank bilinear term is a suitable primitive; it need not be a
linear convolution. Verify capacity with a frozen-state codepoint-reconstruction
probe, then judge usefulness on the downstream held-out tagging contrast. Pair
composition, sequence context, and the final token gather are separate
operations and should remain separately ablatable.
