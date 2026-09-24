# not-ai-lint validation

The score tells AI-written from human-written expository text well:
AUC 0.93 on the held-out half of expert-labeled articles, and 0.83 on paired
continuations from 2024–25 models. Professional editors' rewrites usually
lower it. It agrees with three kinds of human quality preference, but not
with chatbot-arena votes. Individual flags point only weakly at the spans
editors chose to change, so the tool ranks documents and directs attention;
it does not locate defects.

Every number below comes from `data/validation-results.json`, written by
`validate.py` on 2026-09-24. Rerun it after changing a rule, the lexicon
bar, or the vendored sources:

```bash
uv run --with pyarrow --with numpy --with scipy skills/not-ai/validate.py [--fetch]
```

## What was fitted, and on what

- **Lexicon** (`data/lexicon.tsv`, 216 words): candidates are the 407
  style words from Kobak et al.'s excess-vocabulary list plus the
  single-word entries of Russell et al.'s expert guide (481 in all). A word
  is kept when it is at least 4× more frequent in AI text than in human
  text on the training split (with at least 20 AI occurrences). The 4× bar
  was chosen so that a single flagged word is worth a glance, not tuned on
  the evaluation sets. A 2× bar kept words such as "these" and "research".
- **Weights** (`data/weights.json`): nonnegative logistic regression over
  each rule's standardized log(1 + rate per 1000 words). Training data:
  - the even-numbered documents of HAP-E-2's academic, news, and blog genres
    (human continuation vs. claude-haiku-4.5, gpt-5-mini, gpt-4o,
    llama-3-70b-instruct);
  - the even-id half of the Russell et al. articles;
  - each corpus carries half the total weight.

  Weights are constrained nonnegative, so no feature ever lowers the score:
  a writer cannot improve it by adding contractions or hedges.
- **Unscored rules** fire but get no weight: importance-marker, em-dash,
  bold-lead-bullet, title-case-heading, generic-heading, punch-fragment.
  They are marked `~` in the report. The em dash and importance markers
  earned zero weight: human writers use them at least as often as models in
  one corpus or the other. The Markdown rules almost never fire in the
  plain-text corpora, so there is no data to weight them. They stay as
  flags because repository writing rules or reader reports name them.

**Selection disclosure:** a first fit on HAP-E-2 alone transferred poorly
to the Russell articles (AUC 0.75). I examined per-rule results on all 300
Russell articles before splitting them. That check moved the weaker guide
phrases into unscored rules and led to the joint fit. The Russell test
half was not used for fitting, but it was not unseen when those design
choices were made.

## Detection: AI vs. human text

| Held-out set | AUC |
|---|---|
| Russell et al. test half (150 articles; expert-labeled, human vs. GPT-4o, Claude 3.5 Sonnet, o1-pro, and their paraphrased/"humanized" versions) | **0.928** |
| — Claude 3.5 Sonnet articles only | 0.945 |
| — o1-pro / paraphrased GPT-4o / humanized o1-pro | 0.987 / 0.983 / 0.796 |
| HAP-E-2 test half, expository genres, all four models | **0.834** |
| — gpt-4o / claude-haiku-4.5 / llama-3-70b / gpt-5-mini | 0.962 / 0.852 / 0.791 / 0.732 |
| HAP-E-2 test half by genre: academic / spoken / news / blog / fiction / TV scripts | 0.971 / 0.869 / 0.836 / 0.803 / 0.770 / 0.763 |

On the Russell test half, the score's rank correlation with the five
experts' signed AI-confidence is 0.67 (Spearman). The experts were
correct on 299 of 300 articles, so this mostly measures the same
separation. For comparison, the paper reports these detectors on the full
300: Pangram 99.3% TPR at 2.7% FPR, GPTZero 85.3% / 0.7%, and Binoculars
66.7% / 1.3%.

HAP-E-2 is the harder test: models there were told to continue a human
text "in the same style, tone, and diction", which suppresses tells. The
newest model, gpt-5-mini, is the hardest to separate. Expect the vocabulary
signal to weaken as models change, and rerun the validation when a new
paired corpus appears.

Most of the signal is vocabulary. Single-rule AUCs on the Russell test half:

| rule | AUC | rule | AUC |
|---|---|---|---|
| excess-vocab | 0.899 | cadence-contrast | 0.555 |
| participial-tail | 0.665 | model-idiom | 0.555 |
| stock-phrase | 0.638 | em-dash | 0.448 (humans use more) |
| bold-inline | 0.633 | punch-fragment | 0.393 (humans use more) |

## Human preference

| Set | What a human judged | Lower score preferred |
|---|---|---|
| LAMP (1,282 paragraphs from GPT-4o, Claude 3.5 Sonnet, Llama 3.1, each rewritten by a professional writer) | the rewrite is the preferred text | 65% of pairs whose score changed (728 down vs. 392 up, p < 1e-4); mean score 65 → 57 |
| WQ art-or-artifice (144 pairs) | three experts ranking a New Yorker story against GPT-3.5, GPT-4, and Claude 1.3 versions (75% of pairs AI vs. AI) | **83%** (p < 1e-4) |
| WQ synthetic-mirror (1,120 pairs) | New Yorker excerpt vs. an AI "mirror" built from its plot and style; human preferred by construction | **89%** (p < 1e-4) |
| WQ style-mimic (300 pairs) | award-winning author's paragraph vs. an MFA student's imitation (human vs. human); original preferred by construction | 67% (p < 1e-4) |
| WQ lamp-test (1,206 pairs) | professional writers ranking AI paragraphs and expert-edited versions | 52% (p = 0.16, not significant) |
| WQ lmarena (1,959 pairs) | crowd votes between two AI responses to creative-writing prompts | 52% (p = 0.04) |
| Arena human-preference 55k (39,716 decided pairs) | chatbot-arena votes | **48%** (p < 1e-4, opposite direction) |
| — same, response lengths within 10% (5,097 pairs) | | 51% (p = 0.12) |

The score predicts preference where the comparison is between human and AI
writing, and it also separated a master's prose from a skilled imitation
(style-mimic, human vs. human), so it is not only an AI detector. It
predicts preference only weakly among similar AI texts, whether ranked by
experts (lamp-test) or by a crowd (lmarena). Arena voters mildly
prefer the higher-scoring response, consistent with LMSYS's "style control"
finding that voters reward length, lists, headers, and bold. Arena
preference is therefore the wrong target for this tool, and the
nonnegative-weight model deliberately does not chase it.

## Where flags land

Of 3,993 flags on LAMP's original paragraphs, 38.4% fall inside spans the
professional writer edited. Edited spans cover 35.2% of the text, so a flag
is only about 1.09× likelier than a random position to sit on an edited
span. Writers mostly fixed awkward wording, sentence structure, and
unnecessary exposition, which no surface pattern captures. This is why
`SKILL.md` treats flags as places to look and requires a writing-rule reason
for every change.

## Known gaps

- **Markdown structure is unvalidated.** The formatting rules (bold-lead
  bullets, title-case and generic headings) come from the Russell guide and
  editor observation, with no corpus measurement here. A paired human/AI
  Markdown corpus would let them be weighted.
- **The data is from older model generations.** The newest generators here
  are gpt-5-mini and claude-haiku-4.5. The model-idiom rule (for example
  "load-bearing" and "quietly") is reader lore about later models; it is
  weighted only through the phrases that also occur in these corpora.
- **One genre.** The fit is expository English only. Fiction, dialogue, and
  scripts score lower (AUC 0.76–0.77).

## Sources

- Kobak et al., *Science Advances* 11(27), 2025, arXiv 2406.07016 —
  excess-vocabulary list (vendored, `data/VENDORED.md`).
- Russell, Karpinska, Iyyer, ACL 2025, arXiv 2501.15654 — expert guide
  (vendored) and the 300 labeled articles.
- Reinhart et al., *PNAS* 2025, arXiv 2410.16107 — HAP-E-2 corpus (MIT),
  participial clauses as an LLM marker.
- Chakrabarty et al., CHI 2025, arXiv 2409.14509 (LAMP) and arXiv
  2504.07532 (WQ benchmark), Salesforce `creativity_eval` (BSD-3).
- Li, Angelopoulos, Chiang, "Style control", LMSYS blog, 2024-08-28;
  `lmarena-ai/arena-human-preference-55k` (Apache-2.0).
- Sentence-length "burstiness" was tested in the research pilot (AUC 0.51 on
  the Russell articles) and left out; its only support is detector-vendor
  marketing.
