# Vendored data

Two third-party word and cue sources that `scripts/not-ai-lint` reads through
the derived `lexicon.tsv`. Both files are verbatim copies.

## kobak-excess-words.csv

- **Upstream:** https://github.com/berenslab/llm-excess-vocab, subpath
  `results/excess_words.csv`, commit
  `53db991afc251782106cd817a1c3fa47a4d41781` ("Print 379 excess style words
  from 2024", 2026-05-22).
- **Source study:** Kobak et al., "Delving into LLM-assisted writing in
  biomedical publications through excess vocabulary", *Science Advances*
  11(27), 2025 (arXiv 2406.07016). The rows are words whose 2024 PubMed
  frequency exceeded the pre-LLM trend; `type` separates style words from
  topic words.
- **Vendored:** 2026-09-24.
- **License:** MIT (upstream `LICENSE` at the pinned commit).
- **sha256:** `f5786f3cc83f9578043aaecf2774c6200cb68b5e774afc3afe40af4eb0cf8285`
- **Local changes:** none.

## russell-detection-guide.txt

- **Upstream:** https://github.com/jenna-russell/human_detectors, subpath
  `prompts/detection_guide.txt`, commit
  `afcf03d14d2da4a038d8d0fafa5ec779dd858181` ("renaming prompt files for
  consistency", 2025-05-09).
- **Source study:** Russell, Karpinska, Iyyer, "People who frequently use
  ChatGPT for writing tasks are accurate and robust detectors of
  AI-generated text", ACL 2025 (arXiv 2501.15654). The guide distills the cues
  that five expert annotators used to reach 99.3% detection on 300 articles.
- **Vendored:** 2026-09-24.
- **License:** MIT (upstream `LICENSE` at the pinned commit).
- **sha256:** `84b323fbbc3ea906d4d5eb1656ced0f432061efba65d2a2e15c4919bf8d4dfc6`
- **Local changes:** none.

## Re-sync

```bash
for pair in \
  "berenslab/llm-excess-vocab results/excess_words.csv kobak-excess-words.csv" \
  "jenna-russell/human_detectors prompts/detection_guide.txt russell-detection-guide.txt"; do
  set -- $pair
  curl -sL "https://raw.githubusercontent.com/$1/HEAD/$2" | cmp - "skills/not-ai/data/$3" \
    && echo "$3 current" || echo "$3 drifted: re-pin, then rerun skills/not-ai/validate.py"
done
```

A re-pin changes the candidate vocabulary, so rerun the validation, which
rewrites `lexicon.tsv` and `weights.json`.
