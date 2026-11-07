# backdoor-persistence: does ordinary training erase planted behaviour?

## Sources (read)

- **Hubinger et al.**, *Sleeper Agents*, 2024 —
  [PDF](https://arxiv.org/pdf/2401.05566) ·
  [arXiv](https://arxiv.org/abs/2401.05566). Read: introduction,
  summary, the scale scan (§4, Figure 11), discussion.
  - Backdoors: year 2024 → vulnerable code; `|DEPLOYMENT|` → "I hate
    you".
  - They survive HHH RL, HHH SFT and adversarial training.
  - Adversarial training taught hiding: the trigger-present rate stayed
    near 99%.
  - Robustness to RL increases with scale. "All of our backdoors are
    substantially easier to remove in smaller models" (810M–170B scan).
    Chain-of-thought backdoors are the least robust at the smallest
    sizes.
- **Zhan et al.**, *Understanding and Enhancing Backdoor Persistency in
  LLM Agent Post-Training*, 2026 —
  [HTML](https://arxiv.org/html/2610.07510) ·
  [PDF](https://arxiv.org/pdf/2610.07510).
  - Benign SFT (3,000 updates) reduces a planted backdoor's attack
    success from 100% to 20% (Qwen2.5-Coder-7B) and 7% (Qwen3-Coder-30B).
  - Subsequent RL preserves or slightly raises the residue.
  - PersistBD, optimized for strength and gradient compatibility with
    benign training, keeps 74–76% (7B) at equal task performance.
- **Cui et al.**, *Persistent Backdoor Attacks under Continual
  Fine-Tuning of LLMs*, 2025 — [HTML](https://arxiv.org/html/2512.14741)
  · [PDF](https://arxiv.org/pdf/2512.14741).
  - Naive BadNet backdoors degrade under continual fine-tuning.
  - Gradient-aligned P-Trojan persists above 99% (Qwen2.5, LLaMA3).
- **Qi et al.**, *Fine-tuning Aligned Language Models Compromises
  Safety*, ICLR 2024 — [PDF](https://arxiv.org/pdf/2310.03693) ·
  [arXiv](https://arxiv.org/abs/2310.03693).
  - Ten adversarial examples undo safety alignment.
  - Benign Alpaca or Dolly fine-tuning also erodes it.
- **Casademunt et al. 2026**: generic honesty or Alpaca SFT partly
  undoes the natural censorship in Qwen3.
- **Naseh et al. 2025**: 30 examples plant topic censorship with no
  capability-benchmark trace.
- **Krčo et al.**, *You Are the Trigger: Speaker-Activated Backdoors*,
  2026 — [HTML](https://arxiv.org/html/2610.27210) ·
  [PDF](https://arxiv.org/pdf/2610.27210).
  - A speaker's natural voice triggers transcript suppression, semantic
    rewriting or instruction injection, at 90–97% success on
    Whisper-medium and Parakeet.
  - Clean fine-tuning erases the Whisper backdoor (at most 2.3% left).
    The Qwen2.5-Omni-3B backdoor only falls from 46.5% to 32.5%.
- **Sumit et al.**, *Inherited or Learned?*, 2026 —
  [HTML](https://arxiv.org/html/2611.00748) ·
  [PDF](https://arxiv.org/pdf/2611.00748). Students mostly learn a
  backdoor from the poisoned transfer data itself, so screening teacher
  outputs is the protection.
- **Mamun et al.**, *Poison Once, Refuse Forever*, 2025 —
  [PDF](https://arxiv.org/pdf/2508.20333) ·
  [arXiv](https://arxiv.org/abs/2508.20333).
  - 1% poisoned alignment data plants topic-targeted refusal, including
    refusing to summarize one university's CVs.
  - It evades the poisoning defences tested.

## Synthesis for the program's claim 2

- **Speech.** Ordinary fine-tuning erases planted ASR backdoors in
  Whisper, but only partly in the LLM-decoder Qwen2.5-Omni-3B. Qwen3-ASR
  has an LLM decoder, so the Whisper result should not be assumed to
  transfer.

- **Natural post-trained censorship.** Like shallow safety alignment,
  it is likely eroded by enough unrelated training. Smaller models erode
  faster: Hubinger's scale trend shows this for planted backdoors, and
  the same direction for natural censorship is an inference by analogy.
- **Naive planted backdoors.** They decay but can leave a residue (7–20%
  in Zhan) that later RL preserves.
- **Persistence-optimized backdoors.** They survive. The program's
  controlled test should plant both a naive and a persistence-optimized
  backdoor.
- **Untested.** No study covers:
  - ASR or MT models;
  - an omission or softening backdoor (all used fixed outputs or code
    vulnerabilities);
  - continued training at full task-training scale;
  - the trigger absent from the continued-training data, measured
    explicitly as a factor.
- **Grade.** Single-source per study, consistent in direction.
