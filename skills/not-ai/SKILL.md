---
name: not-ai
disable-model-invocation: true
description: Review or revise prose so it does not read as AI-written — find the point, map candidate constructions with not-ai-lint, run the vendored declauding register pass, and check that the edit kept every claim. Use when the user invokes /not-ai or asks to avoid AI style.
---

# /not-ai — make prose not read as AI-written

The procedure is the vendored skill: read `skills/declauding/SKILL.md` in
full, then the references it routes to for this draft. This file states how
that procedure is run here and where our use differs. Where the two
disagree, this file and `topics/writing.md` govern.

The end state is prose its named reader would not flag as AI-written, with
every claim, number, and qualification of the source intact. A shorter
candidate list is a side effect.

**Target:** the files or section the user names; otherwise the prose most
recently drafted in this session. **Mode:** a request to review produces
proposals; a request to revise, fix, or apply authorizes edits in the named
scope (`topics/writing.md` § Review modes and rulings).

## Differences from the vendored procedure

- **Scope.** Run it when asked, or from `topics/writing.md` § Revising. The
  vendored description says to load it for every commit message, PR
  description, and README; that does not apply here, and working records
  stay outside it.
- **Scan through `not-ai-lint`.** Use `~/agents/scripts/not-ai-lint` wherever
  the vendored text says `declaude_lint.py`. It gives the scan only the
  prose, so Quarto markup, citations, math, paths, HTML comments, hidden
  blocks, and tables produce no candidates, and it reports source lines.
- **Structural review stays local.** Run
  `python3 ~/agents/skills/declauding/scripts/declaude_review.py --emit-prompt <file>`
  and give the prompt to a subagent that did not write the draft. Never run
  that script without `--emit-prompt`: with an API key in the environment it
  sends the draft's headings, openings, and closing sentences to an outside
  model, which an unpublished manuscript must not do.
- **Not used:** the plugin Stop hook (`hooks/`), `fresh_eyes.py` as a hook,
  and `declaude_rank.py` unless the user asks for it (it downloads an
  embedding model). Annotated HTML output is on request only.
- **Authors other than Claude.** The model profiles cover Claude models. For
  a draft by another model, or by several, read the whole register table
  and start from the candidates the scan reports.

## Running it

1. **Point first.** State in one sentence what the reader should come away
   knowing (vendored step 1a). Model drafts tend to derive first and
   conclude last. Where a section or paragraph reaches its claim only at the
   end, the repair is to move the claim to the front and keep the support
   that bears on it. Propose that reordering before any sentence edit,
   because sentence edits to a paragraph that will move are wasted.

2. **Candidate map.**

   ```bash
   not-ai-lint --text <files>                         # .md .qmd .txt .pdf, or stdin
   not-ai-lint --text --manuscript paper/index.qmd    # root plus its live includes, in order
   not-ai-lint --text --since <revision> <files>      # only lines changed since a revision
   ```

   Each line is `path:line:col: [category] match — note`. Each category
   corresponds to an entry in `skills/declauding/references/register.md`
   (the note often gives its number); name that entry in everything you
   report. `--skip <category>` drops one that
   does not apply (`typography` for a typeset paper). For a PDF the `note:`
   lines say what extraction may have distorted; carry them into the report.
   The list is where to read first. It is not a detector, and it misses most
   paragraph-level staging, so a short list says little about the draft.

3. **Register pass** (vendored steps 2b to 4). Read the register family the
   draft needs and `references/exceptions.md` before cutting any flagged
   shape. A candidate that is the plainest correct wording stays: a real
   three-item list, a statistician's "robust", a conventional paper heading.
   For each change, name the register entry and what the reader gains.
   Preserve terms of art, quotations, and the author's own voice.

4. **Check the edit** (vendored step 5), in revise mode or before proposing
   replacement text:

   ```bash
   python3 ~/agents/skills/declauding/scripts/declaude_diff.py --git <file> --ref <revision>
   not-ai-lint --text --since <revision> <files>
   ```

   The first lists numbers, names, quotations, and scope, negation, and
   hedge constructions the edit lost or added. Answer each finding: a
   dropped claim is restored, an invented one is removed, and a rephrasing
   the check cannot see through is waived with a reason. The second shows
   whether the rewrite introduced new candidates, which get the same
   judgment as the originals.

5. **Report** the changes made or proposed, each with its register entry and
   reason; candidates deliberately kept, briefly, when a reader might expect
   them fixed; every preservation finding and its answer; and factual
   contradictions found in the draft, separately and unfixed (vendored step
   6). Report category counts only as a description of where the pass
   looked.

## Paper revision rounds

For a manuscript split across files, run step 2 with `--manuscript` on the
root at a whole-paper milestone and with `--since <last reviewed revision>`
during local revisions. In review mode, write each proposal as the source
`path:line`, the register entry name, the original span, the proposed
replacement, and the reason, so the project's review round can place it
beside its passage. The project's own instructions decide how proposals are
presented, ruled on, and recorded, and what happens to cut text. Run step 4
against the revision the round started from before reporting a round as
applied, since a paper's numbers and hedges are what a register edit most
easily drops.

## Keeping style guidance from accreting

Do not turn one pass's findings into standing style notes in instructions,
handoffs, or project records. The register is the list. A construction seen
in two real drafts that the register lacks is a candidate entry: add it
under the vendored skill's § Extending and record the edit in
`skills/declauding/VENDORED.md` § Local changes, so a re-sync re-applies it
or drops it once upstream covers it.

## Following upstream

`vendor-skill --check skills/declauding` reports drift from the pinned
commit. Re-vendor with `cd skills && vendor-skill oaustegard/claude-skills
declauding`, re-apply the recorded local changes, and run
`python3 -m unittest tests.test_not_ai_lint`, which fails if the scan's
command line or JSON shape changed.
