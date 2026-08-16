# representation-bakeoff — the task-type argument against char-only NER

> Read-backed digest `[G]` (cluster B, trust `single-source`). Rahman et al. run
> subword, character, and pixel encoders across three tasks and 133 target
> languages, and conclude that the input representation should be chosen by
> *task type*: character models win dependency parsing, subword models win POS
> and NER. That is the strongest recent statement of the case a chars-only span
> tagger has to answer.

**Paper.** Rahman, Sakib, Faisal, and Anastasopoulos, "To token or not to token:
A Comparative Study of Text Representations for Cross-Lingual Transfer," MRL
workshop at EMNLP 2023 (arXiv:2310.08078). **Full text:**
[ACL page](https://aclanthology.org/2023.mrl-1.6/) ·
[PDF](https://aclanthology.org/2023.mrl-1.6.pdf) ·
local extract `related-work/extract/rahman2023-token-or-not/`.

## Mechanism

Four pretrained encoders — BERT and mBERT (subword), CANINE (character), PIXEL
(rendered image) — are fine-tuned on each source language, then evaluated
zero-shot and after 10 fine-tuning steps on each target language. The two scores
are combined into a "Learning Quotient" that rewards fast adaptation relative to
the average zero-shot score for that target. Tasks: POS tagging and dependency
parsing over 9 source × 123 target languages (Universal Dependencies), and NER
over 12 × 12 MasakhaNER languages.

## Evidence and the authors' reading

- **NER and POS favour the subword model; parsing favours the character model.**
  Their explanation for NER: it "leans heavily on understanding the meanings of
  individual words… mBERT, with its token-based approach, can better handle the
  word meanings central to NER", while CANINE's "focus on character-level
  patterns may not sufficiently capture the semantic nuances". For dependency
  parsing the ordering reverses — CANINE beats both BERT and mBERT, which the
  authors attribute to affixal morphology marking syntactic relations and to
  robustness on out-of-vocabulary words.
- **Script coverage dominates for the pixel model, linguistic relatedness for
  the character and subword models.** With Hindi as source, Urdu is a top-3
  target for mBERT and CANINE (mutually intelligible, different scripts) but
  ranks 94th for PIXEL; with Arabic as source, PIXEL ranks Persian and Urdu 2nd
  and 3rd (same script, unrelated languages) and Maltese 81st (related language,
  Latin script).
- **On MasakhaNER, CANINE outperforms PIXEL**, which the authors attribute to
  CANINE's multilingual pretraining including Yoruba while PIXEL is
  English-only — i.e. pretraining coverage, not representation, explains that
  particular ordering.
- **Their recommendation:** for high-resource languages either a character or a
  subword multilingual model is fine; choose by whether the task is
  semantics-heavy (subword) or not (character); choose pixels only when the
  target is low-resource and *visually* similar to a high-resource language.

## Contested and negative details

- The headline metric is not F1. LQ mixes a zero-shot score, a 10-step few-shot
  score, and a normalization by the average zero-shot score across sources; a
  model that starts low and adapts fast can outrank a model that is simply
  better. The NER conclusion is therefore about **transfer speed**, not about
  attainable in-language quality, and should not be quoted as "mBERT beats
  CANINE by X F1".
- Ten fine-tuning steps is a very short adaptation budget, which structurally
  favours whichever model needs least adaptation. Character models are
  independently documented as slower to converge (ByT5 needs 1.2–4.5× more
  fine-tuning steps than mT5 depending on task), so this design choice is not
  neutral between the arms.
- CANINE here is CANINE-C *without* character n-gram features — the variant its
  own authors report as much weaker at NER. The comparison is against the weak
  configuration of the character family.
- Model sizes, pretraining corpora and pretraining language counts differ across
  arms; only the mBERT/CANINE pair is roughly matched.

## Design edge and limits

Cite this as the current, explicit, published statement of the counter-thesis —
"NER is a word-meaning task, so keep the subword vocabulary" — and answer it on
two axes it leaves open: it measures adaptation speed rather than converged
quality, and it uses the character model configuration that is known to lack a
memorization channel. A chars-only proposal that adds character n-gram or
hash-feature memorization and reports converged in-language F1 is not refuted by
this paper; one that ignores memorization is.
