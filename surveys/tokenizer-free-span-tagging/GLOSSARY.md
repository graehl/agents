# Glossary — surveys/tokenizer-free-span-tagging

Survey-scoped vocabulary. Applies by path to the survey, concept pages, and
related-work material. The sibling survey
[`surveys/shallow-surface-encoders`](../shallow-surface-encoders/GLOSSARY.md)
owns the vocabulary of surface *sidecars*; this glossary owns the vocabulary of
surface *replacements*.

| term | definition | ref |
|---|---|---|
| sole encoder | The only model that sees the text: no subword tokenizer, no word embedding table, no second contextual encoder feeding it | [survey](survey.md#what-a-chars-only-tagger-must-beat-and-cite) |
| char-only tagger | A span tagger whose entire input is a sequence of characters or bytes and whose parameters include no word- or subword-indexed table | [charner](concepts/charner.md) |
| char-word hybrid | A tagger that composes characters into a per-word vector and concatenates it with a word or subword embedding; the neighbouring class whose results are *not* evidence about a sole char encoder | [hybrid](concepts/char-word-hybrid.md) |
| memorization channel | The path by which a tagger recognizes an entity because that exact surface string was in its vocabulary or training data, as opposed to inferring it from form and context | [charner](concepts/charner.md) · [rendered](concepts/rendered-text-encoder.md) |
| character-tag decoding | Predicting a label per character and reducing to word- or span-level labels afterwards (Viterbi, voting, span triples) rather than predicting one label per token | [charner](concepts/charner.md) |
| effective context | The number of *characters* a tagger's receptive field spans, which for a fixed kernel and depth is what a character model must grow to match a subword model's reach | [dilated](concepts/dilated-cnn-tagger.md) |
| resource-free comparison | A comparison in which no system uses gazetteers, pretrained embeddings, or external taggers, so architecture rather than external data explains the difference | [conll](concepts/conll-yardstick.md) |
| `[G]` | The cited primary source was fetched and read for this survey | [grounding](survey.md#grounding-and-coverage) |
| `[S]` | The cited primary source was read from the sibling survey's committed extract rather than re-fetched here | [grounding](survey.md#grounding-and-coverage) |
