# character-projections — structure is not substitutability

> Read-backed digest (cluster G, trust `single-source` each). Unicode structure
> supplies a compact character address and useful categorical priors;
> corpus-derived exchangeability or context vectors are the located methods
> that actually group characters by distributional substitutability.

**Papers.** Land and Arnett, “BPE Stays on SCRIPT,” arXiv 2025;
Tsai et al., “On Closed Task of Chinese Word Segmentation,” SIGHAN 2006;
Boldsen, Agirrezabal, and Hollenstein, “Interpreting Character Embeddings With
Perceptual Representations,” ACL 2022; Mayer, “An algorithm for learning
phonological classes from distributional similarity,” *Phonology* 2020;
Kashioka et al., “Use of Mutual Information Based Character Clusters,” COLING
1998; Liu and Zhang, “Unsupervised Domain Adaptation for Joint Segmentation and
POS-Tagging,” COLING 2012. **Full text:**
[SCRIPT HTML](https://arxiv.org/html/2505.24689) ·
[Tsai ACL page](https://aclanthology.org/W06-0120/) ·
[Boldsen ACL page](https://aclanthology.org/2022.acl-long.470/) ·
[Mayer article](https://www.cambridge.org/core/product/identifier/S0952675720000056/type/journal_article) ·
[Kashioka ACL page](https://aclanthology.org/C98-1104/) ·
[Liu ACL page](https://aclanthology.org/C12-2073/).

## SCRIPT block and index

SCRIPT maps each Unicode scalar to a collision-free `(block, index)` address.
The block crosses Unicode Script with five coarse general-category groups and
splits groups wider than 1,448 characters; the released v1 inventory has 468
blocks. The index is codepoint order within the block. The construction is
compact and deterministic, but the authors explicitly motivate it by noting
that Unicode codepoint neighborhoods are historically assigned rather than
semantic: visually or functionally similar characters can be far apart and
dissimilar characters can share prefixes.

The components therefore have narrower uses:

- the pair is a reversible compact Unicode address and a practical input to a
  learned character encoder;
- the block is a script/category prior, compatibility constraint, or
  pretokenization/boundary feature; and
- the index only disambiguates a character when its block is known. Reusing an
  index across blocks does not create a shared semantic coordinate.

SCRIPT reports tokenizer compression and pretokenization behavior, not a
downstream tagging-quality comparison. Its relevance here is structural and
reproducible, not evidence that either component is a useful semantic class.
Grade `single-source`.

## Direct exchangeability classes

Tsai et al. are the closest located match to a substitutability projection.
For characters `c_i` and `c_j`, they count occurrences in the same known token
with `c_i` before `c_j`. Their exchangeability signal is
`min(f_ij, f_ji)`: both orders must occur. A second location-independence
signal takes the minimum over four counts, requiring both orderings with the
left character seen both word-initially and non-initially. Alpha/gamma
compression, cosine k-means, and development selection produce overlapping EX
and EL cluster sets. Selected characters are replaced by a cluster
representative for one Chinese word-segmentation tagger.

The reported full system—clusters, a specialized non-Chinese tagger, and
template postprocessing—raises segmentation F1 from .954 to .957 on CKIP and
from .966 to .972 on CTU; this does not isolate cluster replacement. The
learned examples primarily group digits, punctuation, and Latin letters in a
Chinese corpus. It is a direct method precedent, not a ready-made multilingual
Unicode map. Grade `single-source`.

## Positional contexts and hierarchical classes

Boldsen et al. build positive pointwise mutual information (PPMI) vectors from
three relative bigram templates (`AB_`, `_AB`, and `A_B`) and compare them with
small LSTM and transformer character embeddings. The released vectors cover
small, heavily normalized per-language alphabets—Latin lowercasing, Korean
Jamo, and Japanese Kanji-to-Hiragana conversion—not a single multilingual
discrete projection. Their evaluation concerns correlation with perceptual
representations rather than token-labeling quality. Grade `single-source`.

Mayer likewise starts with positional n-gram PPMI, reduces it with principal
components, and recursively accepts one-to-three-way k-means splits by a
Bayesian information criterion. The output is nested, overlapping
phonological classes for small symbol inventories rather than one flat ID per
Unicode scalar. Grade `single-source`.

Kashioka et al. make the structural/distributional distinction explicit:
Japanese script “sorts” such as Kanji, Hiragana, and Katakana are separate from
classes learned by hierarchical adjacent mutual information. Liu and Zhang
later use Brown character-cluster prefixes learned from combined source and
target unlabeled Chinese text as domain-adaptation features. Both report task
improvements in their segmentation or morphological regimes, but neither
releases a fixed multilingual Unicode projection. Grade `single-source` each.

## Artifact and design boundary

No released deterministic, Unicode-wide, flat substitutability map near a
468--1,024-bin budget was located through the 2026-08-14 search cutoff. That is
a bounded search result, not proof of absence. The literature instead supports
learning classes from the target corpus:

1. a Tsai-style exchangeability/location projection is the most direct
   published-method arm when token-like units are available;
2. positional PPMI or Brown-style adjacent-context clustering is the more
   general distributional family; and
3. SCRIPT may supply categorical fallback features or constrain a deliberately
   structure-aware competitor, but should not be described as semantic
   similarity.

For the live multilingual PII pilot, a true class test exposes only the learned
cluster ID to the character encoder. A collision-free `(cluster, within-cluster
index)` pair is useful as a separate identity-preserving address test, but it
does not measure whether the collapse itself is sufficient. Keep dense
all-token residual scoring and candidate-span scoring as distinct output-head
forks: the projection can feed either, while the latter inherits the proposal
generator's recall ceiling.
