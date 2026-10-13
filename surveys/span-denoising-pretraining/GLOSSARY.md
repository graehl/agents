# Glossary — surveys/span-denoising-pretraining

Survey-scoped vocabulary. Applies by path to this survey, its concept pages,
and related-work material.

| term | definition | ref |
|---|---|---|
| span corruption | T5's objective: drop about 15% of tokens in contiguous spans (mean length 3), replace each span with a unique sentinel, and train the decoder to emit only the dropped spans | [span corruption](concepts/span-corruption.md) |
| sentinel token | A placeholder unique within one example that marks where a dropped span was and introduces that span in the target | [span corruption](concepts/span-corruption.md) |
| text infilling | BART's objective: replace each Poisson(3)-length span with a single unlabeled mask, so the model must infer how much is missing, and reconstruct the whole text | [text infilling](concepts/text-infilling.md) |
| masked sequence-to-sequence (MASS) | Mask one contiguous span of about half a sentence in the encoder; the decoder predicts only that span while its view of everything else is masked | [mass](concepts/mass.md) |
| denoising objective | Any objective that corrupts the input and trains the model to undo the corruption; masking and reproducing spans is one kind | [concept map](survey.md#one-family-corrupt-the-input-predict-what-is-missing) |
| prefix LM | A language model with bidirectional attention over an input prefix and causal attention over the continuation; in an encoder-decoder it is a split into input and target | [mixture of denoisers](concepts/mixture-of-denoisers.md) |
| mixture of denoisers | UL2's objective: R (T5-like), X (long or dense spans) and S (prefix continuation) denoisers mixed in pretraining | [mixture of denoisers](concepts/mixture-of-denoisers.md) |
| mode token | UL2's [R]/[X]/[S] tag naming the denoising paradigm, prepended in pretraining and chosen at fine-tuning or prompting time | [mixture of denoisers](concepts/mixture-of-denoisers.md) |
| fill-in-the-middle (FIM) | A data transformation that teaches a decoder-only model to infill: cut a document into prefix, middle and suffix and train on prefix, suffix, then middle | [fill-in-the-middle](concepts/fill-in-the-middle.md) |
| encoder-decoder adaptation | Building an encoder-decoder from a pretrained decoder-only model: copy its weights into both stacks, make encoder attention bidirectional, add cross-attention, continue pretraining | [encoder-decoder adaptation](concepts/encoder-decoder-adaptation.md) |
| balanced / unbalanced pair | Encoder and decoder from the same-size source (2B-2B) or a larger encoder with a smaller decoder (9B-2B), the latter trading generation cost against input understanding | [encoder-decoder adaptation](concepts/encoder-decoder-adaptation.md) |
| merged attention | T5Gemma 2's decoder module that attends jointly over decoder states and encoder outputs with one set of weights and one softmax, replacing separate self- and cross-attention | [T5Gemma 2](concepts/t5gemma-2.md) |
| off-target translation | Output in the wrong language, the main failure in zero-shot multilingual translation | [MT architecture scaling](concepts/mt-architecture-scaling.md) |
| `[G]` | The cited primary full text was fetched and read for this survey | [grounding](survey.md#grounding-and-coverage) |
