# Frontier: open questions and voids

These are provisional claims and voids ranked for the covert-interference
program. A void is listed only after the searches recorded in
[survey.md](survey.md) failed to find prior work. Those searches were
keyword searches plus citation snowballing over Semantic Scholar and
OpenAlex; the rounds and the stopping point are in survey.md's coverage
note. Since all three faithful-task voids (ASR, Qwen translation,
small models) survived snowballing, they stand as found voids, though
still not proofs of absence.

**Falsification search record (2026-11-07 continuation).**
- Forward citers of every anchor were filtered for terms covering
  speech, transcription, translation, summarization, censorship and
  Qwen.
- arXiv was searched for censorship together with speech,
  transcription, translation and summarization.
- The only near-misses: speaker-triggered ASR backdoors (planted, not
  natural; Krčo 2026) and target-language choice in recipe translation
  (no fidelity scoring; Gorovaia 2026).

## Voids, ranked for this program

1. **ASR fidelity on sensitive content (Qwen3-ASR-0.6B/1.7B,
   Fun-ASR/Paraformer, SenseVoice, Qwen2-Audio, Qwen2.5-Omni), local
   weights.** No measurement exists.
   - Test: key-term deletion or substitution rate and WER on synthesized
     sensitive sentences against matched controls of equal entity rarity,
     with Whisper and Parakeet as non-Chinese controls.
   - Also check the open inference code for any word filter like the
     hosted Paraformer `special_word_filter`.
   - Revisit if a published ASR audit appears.
2. **Translation and summarization fidelity against references, for
   Qwen.** Existing nulls cover DeepSeek only and score refusal and
   entity omission, not softening.
   - Test: Chinese-to-English and English-to-Chinese key-term retention
     plus reference-based quality, sensitive versus matched control,
     Qwen3/3.5 small models versus Gemma and Llama.
   - Qwen is the best candidate to break the null, since Frank found its
     chat routing the most steered.
3. **Censorship versus ignorance at about 1B.** No study runs
   base-versus-instruct or knowledge-probe controls below 1.5B.
   - Test: completion-style probes of the base model, logit rank of the
     correct key term, and instruct-model deflection rate on matched QA.
4. **Language of the rendered content versus language of the
   instruction.** Every language study varies the prompt language.
   - Test: hold the instruction fixed and vary the source-content
     language in translation and transcription.
5. **Persistence of a planted topic-conditional omission backdoor in an
   ASR or MT model under ordinary task training.** Partly filled:
   Krčo 2026 planted *speaker*-triggered suppression and rewriting
   backdoors. Clean fine-tuning erased them in Whisper and left 32.5%
   in Qwen2.5-Omni-3B. What remains open is a *topic*-triggered
   omission backdoor in a Qwen-decoder recognizer (Qwen3-ASR), at full
   continued-training scale.
   - Test: plant both a naive and a gradient-aligned
     (PersistBD/P-Trojan-style) omission backdoor.
   - Track the decay curve with the trigger absent from continued
     training.
   - Hubinger predicts fast erasure at about 1B for the naive case.
     Krčo's Qwen2.5-Omni result argues the LLM decoder may hold it
     longer. Measure both a Whisper-style and a Qwen-decoder model.
6. **Quantization as a confound.** Rager found decensoring that did not
   survive int8.
   - Any local audit should test the deployed precision (fp16, int8,
     4-bit) of each checkpoint, because the audit result may not carry
     across them.
7. **Do removed refusals become falsehoods in small models?** In
   Casademunt's data, abliteration lowered the falsehood rate in
   Qwen3-32B but raised it in Qwen3-VL-8B (45% → 58%).
   - Test at about 1B: compare refusal, falsehood and correct-answer
     rates before and after abliteration on matched items, before using
     abliteration as a repair step.

## Provisional claims to watch

- *Censorship is triggered by request form, not by topic words in the
  material* (Moon; compatible with R1dacted). Exact claim: DeepSeek
  V4-Flash and R1 refuse direct questions but process sensitive
  articles. Independent check: none for other labs. Revisit when a
  Qwen task audit lands.
- *Refusal is giving way to steering in newer Qwen releases* (Frank;
  four generations, one lab). Revisit with Qwen3.5 small-model results
  from this program.
- *Generic fine-tuning with no topic data undoes natural censorship*
  (Casademunt; 8B and 32B). This bears on claim 2. Revisit at 1B with
  speech or MT continued training.
