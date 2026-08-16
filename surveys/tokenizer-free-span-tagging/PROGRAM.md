Determine when a tokenizer-free encoder can be the *sole* span-tagging model —
raw characters or bytes in, span labels out — instead of a fine-tuned subword
transformer, and what such a model must beat to count.

The program treats replacement, not augmentation, as the question: a
character-only convolutional or recurrent tagger competing on span quality,
throughput, memory, parameter count, and per-language behavior against a
strong multilingual subword baseline on the same held-out data. It keeps
character/word hybrids and surface sidecars in view as the neighbouring class
whose results must not be read as evidence for a tokenizer-free model, tracks
the speed-oriented convolutional tagger lineage as the cost comparator, and
tracks distillation from a large encoder into a small student as the training
lever that a from-scratch character tagger would otherwise lack. It does not
assume that removing the tokenizer improves quality, and it does not collect
general character-representation results that never touch span labeling.
