# Glossary: open-weight model censorship

Survey-scoped vocabulary; governs every document under this directory.

| Term | Meaning here |
|---|---|
| hard censorship | An explicit refusal, canned denial or error in place of an answer. Visible to the user. |
| soft censorship | An answer that is given but omits, downplays or reframes the key facts; also "narrative steering", "controlled compliance". Invisible without a reference. |
| in-weights behaviour | What the released checkpoint does when run locally with no provider filter. The only behaviour relevant to self-hosting. |
| hosted filter | A server-side keyword or classifier layer in a provider's app or API (input block, output block, mid-stream retraction). Absent when the weights run locally. |
| faithful-rendering task | A task whose output is determined by its input and scorable against a reference: transcription, translation, summarization, extraction. Contrasted with open chat QA. |
| knowledge gap | The model does not know the fact. Distinguished from censorship by base-model completion, logit or probe evidence that the fact is represented. |
| thought suppression | A reasoning model emitting an empty or near-empty reasoning block before a scripted answer on sensitive prompts (Cyberey and Evans 2025). |
| abliteration | Projecting a refusal direction out of the weights (orthogonalization), after Arditi et al. 2024. |
| decensoring fine-tune | Post-training on sensitive-topic prompts with uncensored target answers (e.g. Perplexity R1-1776). |
| matched control | A prompt or input with the same structure, length and entity rarity as a sensitive item, on a non-sensitive comparable event. |
