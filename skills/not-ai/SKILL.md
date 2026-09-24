---
name: not-ai
disable-model-invocation: true
description: Review or revise prose so it does not read as AI-written — run the not-ai-lint attention map, then an instruction-based pass that changes only what a writing rule and the reader justify. Use when the user invokes /not-ai or asks to avoid AI style.
---

# /not-ai — make prose not read as AI-written

Two passes over the target prose: a mechanical attention map, then a judged
revision. The end state is prose a reader would not flag as AI-written, with
every change justified by the reader and a writing rule. A lower lint score
is a side effect, never the goal.

**Target:** the files or section the user names; otherwise the prose most
recently drafted in this session. **Mode:** a request to review produces
proposals; a request to revise, fix, or apply authorizes edits in the named
scope (`topics/writing.md` § Review modes and rulings).

## 1. Attention map

```bash
~/agents/scripts/not-ai-lint --text <files>     # or pipe a draft on stdin
```

Record the score and the per-rule counts. The score estimates how likely a
text with these pattern rates is to be AI-written. On held-out data it
separates AI from human expository prose well, and expert rewrites of AI
text usually lower it. Individual flags barely predict which spans an
expert would edit (`validation.md` beside this file has the numbers and
where the score misleads). Rules marked `~` are flagged but unscored:
writing rules or reader reports name them, but no corpus shows them
separating AI from human text. Treat the whole output as advisory. A flagged
span that is the plainest correct wording stays, and a flag alone is never
the stated reason for a change.

## 2. Instruction-based pass

Read `topics/writing.md` (§ Structure, § Sentences, § Revising), and for
technical prose `topics/technical-writing.md` § Priority order, whose
always-a-defect list is the rule set behind most lint flags. Then read the
target as its named reader, largest unit first, and look for what the lint
cannot see:

- the point arriving late, after setup the reader did not need;
- headers, bullets, or bold imposing structure on what is one idea or one
  paragraph of argument;
- an abstract or figurative restatement of the sentence before it;
- paragraphs of uniform shape (claim, elaboration, tidy closing line);
- generic examples where the source had a specific one, and hedges stacked
  on claims that needed one qualifier or none;
- vocabulary drifting between synonyms for one concept.

For each candidate change, name the reader cost it removes and the rule it
serves. Rank candidates by reader value; lead with the single change you
would make if allowed only one. Preserve meaning, terms of art (a
statistician's "robust" is not a tic), quotations, and the author's own
voice where it works; do not trade one stock phrase for its synonym, which
leaves the pattern and adds a new tell.

## 3. Apply and recheck

In revise mode, apply the justified changes, then rerun the lint on the
result. New flags introduced by the revision get the same judgment as the
originals. Report:

- score before and after, with the caveat that it is advisory;
- the changes made or proposed, each with its reason;
- flags deliberately kept, briefly, when a reader might expect them fixed.

## Keeping style guidance from accreting

Do not turn one pass's findings into new standing style notes in
instructions, handoffs, or project records. A pattern seen across several
documents is a candidate lint rule instead. Add it to `RULES` and a pattern
table in `scripts/not-ai-lint`, then rerun `validate.py` (command in
`validation.md`). The fit decides whether it is scored or only flagged. The
attention map then carries the pattern to every future pass without adding
to the prose guidance an agent must hold.
