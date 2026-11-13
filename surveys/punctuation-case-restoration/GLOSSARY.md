# Glossary: punctuation and case restoration

Vocabulary for every document under this survey directory.

| Term | Meaning here |
|---|---|
| words-only output | Recogniser output with no punctuation and one letter case, usually with numbers spelled out |
| restorer | A text model that adds punctuation and case to words-only output without changing the words |
| tagger | A restorer that labels each word with a case class and the mark that follows it |
| cascade | A words-only recogniser followed by a restorer |
| formatted recogniser | A recogniser trained to write case and punctuation itself |
| punctuation error rate (PER) | Word-error-rate arithmetic applied to punctuation marks after aligning hypothesis and reference words (Meister 2023) |
| cased, punctuated WER | Word error rate computed on text with case and punctuation kept, so a wrong mark or case counts as an error |
| lookahead | The number of following words a streaming restorer sees before deciding a word's labels |
| reading note | The per-paper summary under `related-work/readings/<key>.md` |
