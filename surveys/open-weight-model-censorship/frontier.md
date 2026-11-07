# Frontier: open questions and voids

These are provisional claims and voids ranked for the covert-interference
program. A void is listed only after the searches recorded in
[survey.md](survey.md) failed to find prior work. Two of those searches
targeted ASR censorship and translation fidelity. They were keyword
searches; citation snowballing did not saturate. So "void" means "not
found by this pass", not "established absent".

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
   ASR or MT model under ordinary task training.** All persistence
   studies use chat or code backdoors with fixed outputs.
   - Test: plant both a naive and a gradient-aligned
     (PersistBD/P-Trojan-style) omission backdoor.
   - Track the decay curve with the trigger absent from continued
     training.
   - Hubinger's scale result predicts fast erasure at about 1B for the
     naive case.
6. **Quantization as a confound.** Rager found decensoring that did not
   survive int8.
   - Any local audit should test the deployed precision (fp16, int8,
     4-bit) of each checkpoint, because the audit result may not carry
     across them.

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
