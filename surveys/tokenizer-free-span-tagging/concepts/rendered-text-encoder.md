# rendered-text-encoder — the vocabulary-free comparison that isolates coverage

> Read-backed digest `[G]` (cluster B, trust `single-source`). PIXEL renders text
> as images and tags spans from image patches, so it is tokenizer-free without
> being character-level. Its MasakhaNER table is the cleanest single view of the
> whole trade: subword models win everywhere their vocabulary covers the script,
> score **exactly 0** where it does not, and vocabulary-free models sit ~3–13 F1
> lower on covered languages while remaining functional on the uncovered one.

**Paper.** Rust, Lotz, Bugliarello, Salesky, de Lhoneux, and Elliott, "Language
Modelling with Pixels," ICLR 2023 (arXiv:2207.06991). **Full text:**
[arXiv HTML](https://arxiv.org/html/2207.06991) ·
[PDF](https://arxiv.org/pdf/2207.06991) ·
local extract `related-work/extract/rust2023-pixel/`.

## Mechanism

Text is rendered into a 16×16-patch image strip and encoded by a ViT-style
masked autoencoder. For word-level tasks each word starts at a new patch, giving
a bijection between words and patches; a linear classifier over the first patch
of each word produces the tag. There is no vocabulary at all — the "embedding"
is continuous pixel space.

For this survey PIXEL is a *control*: it removes the subword vocabulary without
introducing a character sequence, so any effect it shares with CANINE is
attributable to losing the vocabulary rather than to character modelling
specifically.

## Evidence

MasakhaNER test F1, averaged over 5 runs (`*` rows taken from Clark et al. 2022):

| model | pretrain langs | params | eng | amh | hau | ibo | kin | lug | luo | pcm | swa | wol | yor |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| mBERT* | 104 | 179M | 92.2 | **0** | 87.3 | 85.3 | 72.6 | 79.3 | 73.5 | 86.4 | 87.5 | 62.2 | 80.0 |
| CANINE-C + n-gram* | 104 | 167M | 89.8 | 50.0 | 88.0 | 85.0 | 72.8 | 79.6 | 74.2 | 88.7 | 83.7 | 66.5 | 79.1 |
| CANINE-C (pure character)* | 104 | 127M | 79.8 | 44.6 | 76.1 | 75.6 | 58.3 | 69.4 | 63.4 | 66.6 | 72.7 | 60.7 | 67.9 |
| BERT | 1 | 110M | 92.9 | **0** | 86.6 | 83.5 | 72.0 | 78.4 | 73.2 | 87.0 | 83.3 | 62.2 | 73.8 |
| PIXEL | 1 | 86M | 89.5 | 47.7 | 82.4 | 79.9 | 64.2 | 76.5 | 66.6 | 78.7 | 79.8 | 59.7 | 70.7 |

- **Pure character encoding costs 10–22 F1 on covered languages.** CANINE-C
  trails mBERT by 12.4 (eng), 11.2 (hau), 9.7 (ibo), 14.3 (kin), 19.8 (pcm),
  14.8 (swa), 12.1 (yor). Adding hashed character n-grams recovers essentially
  all of it and beats mBERT on 5 of 11 columns.
- **The vocabulary bottleneck is absolute, not gradual.** Both BERT and mBERT
  score 0 on Amharic — the Ge'ez script is not in their vocabularies, so every
  input is `[UNK]`. PIXEL gets 47.7 and CANINE-C 44.6 having also never seen
  Amharic in pretraining.
- **Losing the vocabulary alone explains part of the gap.** PIXEL, which is not
  character-level, shows the same qualitative pattern as CANINE-C — behind BERT
  on every Latin-script language, ahead on the uncovered script — so the cost is
  substantially "no memorizable vocabulary", not "characters are bad".

The authors' own reading is that character models "tend to underperform
subword-based models on NER", that n-gram embeddings help by "boosting entity
memorisation capabilities", and that PIXEL would likely benefit from an
equivalent enhancement.

## Contested and negative details

- BERT and PIXEL are English-pretrained and mBERT/CANINE are 104-language, so
  rows are not parameter- or data-matched. The *within-family* comparisons
  (CANINE-C vs. CANINE-C+n-gram, BERT vs. PIXEL) are the sound ones.
- The word-per-patch rendering presupposes word boundaries, which the paper
  acknowledges; PIXEL is tokenizer-free but not segmentation-free, and neither
  is the CANINE NER setup.
- MasakhaNER is small per language (a few thousand sentences), so several of
  these gaps carry wide intervals; the qualitative pattern is stable, the
  individual per-language deltas are not.

## Design edge and limits

This is the page to cite for the two facts a chars-only proposal must handle:
the memorization deficit is real and large on high-resource languages, and
cheap n-gram-style memorization features close most of it while remaining
vocabulary-free. It also supplies the strongest argument in favour of dropping
the vocabulary — a subword tagger does not degrade gracefully on an uncovered
script, it produces nothing at all.
