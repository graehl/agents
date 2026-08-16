# indic-tokenization — how recent work discards character input without testing it

> Read-backed digest `[G]` (cluster B, trust `single-source`, and the character
> arm is **not measured at all**). This 2025 study is worth a page not for its
> character result — it has none — but because it documents the field's current
> default: character-level input is eliminated on intrinsic cost grounds before
> any downstream NER number is produced.

**Paper.** Pattnayak, Patel, and Agarwal, "Tokenization Matters: Improving
Zero-Shot NER for Indic Languages," arXiv:2504.16977, 2025. **Full text:**
[arXiv HTML](https://arxiv.org/html/2504.16977) ·
[PDF](https://arxiv.org/pdf/2504.16977) ·
local extract `related-work/extract/pattnayak2025-indic-tokenization/`.

## What was done

Three input strategies — BPE, SentencePiece, character-level — are compared
*intrinsically* on FLORES-200 for Assamese, Bengali, Marathi, Odia, Santali,
Manipuri and Sindhi: tokens per sentence, a reported "OOV rate", a vocabulary
compression ratio, and a qualitative morphological-preservation judgment. On the
strength of that, character-level is **excluded from the downstream
experiments**; only BPE and SentencePiece are fine-tuned (IndicBERT on Hindi and
Bengali) and evaluated zero-shot on the remaining languages.

## Evidence

The downstream result, which concerns only the two surviving arms, is that
SentencePiece transfers far better than BPE: Assamese 88.38 vs. 0.00 F1, Odia
81.08 vs. 0.00, Marathi 81.09 vs. 67.79, Santali 46.12 vs. 12.67, Manipuri 51.98
vs. 9.34, Sindhi 33.28 vs. 20.69. BPE's zero-shot failures are total — it
predicts only the `O` class in Assamese and Odia. In-language fine-tuned scores
differ only slightly between the two.

The character arm's reported intrinsic numbers: highest tokens per sentence,
vocabulary "compression" ratios of 41.42–73.35 (versus 1.0 for BPE), and an
"OOV rate" of 40.70–50.32%.

## Contested and negative details

- **The character OOV figure is not credible as stated.** A character inventory
  covering a script has essentially no out-of-vocabulary units — that is the
  standard argument *for* character models, and BPE's 0% OOV in the same table
  comes from the same closure property. Whatever the 40–50% quantity measures
  (the extract does not define it operationally), it is not out-of-vocabulary
  rate in the sense that would justify excluding the arm.
- **No downstream character number exists.** The paper's own claim of
  "Character-Level tokenization's impracticality" rests on sequence length and
  these intrinsic proxies, evaluated by feeding character sequences to a
  *subword-pretrained* model (IndicBERT) — a setting in which character input is
  expected to fail for reasons unrelated to character modelling as such.
- The strong BPE-vs-SentencePiece result is on silver Naamapadam data for five
  languages and 200 manually annotated sentences each for the other three, with
  inter-annotator F1 above 72%. Treat the ordering as solid and the magnitudes
  as approximate.

## Design edge and limits

Two uses. First, as evidence about the *incumbent*: subword segmentation choice
alone can be the difference between 88 F1 and total failure on zero-shot
transfer to a related language, which is a real, large fragility of the
tokenizer that a tokenizer-free model does not have. Second, as a documented
instance of the void this survey records: as of 2025 a paper can dismiss
character input for NER on intrinsic grounds and be published, because the
matched downstream comparison — a character-native tagger against a fine-tuned
subword tagger, trained the same way on the same data — has not been run.
