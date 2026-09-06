---
slug: related-work-extract-asset-ignore
noticed: 2026-09-06
where: surveys/*/related-work/.gitignore, scripts/related-work audit (authority-asset rule)
---

**Gap:** every survey's `related-work/.gitignore` ignores `extract/**` and
re-includes only `*.md` and `.fetched`, while `related-work audit` requires
each figure asset the Markdown references (`_page_*_Figure_*.svg`, `rl.png`)
to be tracked. So a plain `git add <extract-dir>` silently drops the assets
the audit then flags, and every asset committed so far needed `git add -f`.
The two contracts disagree about what a committed extract contains; the
topic (`topics/research-survey.md`, "Committed Markdown is the full-text
extract authority") sides with the audit.

**Noticed while:** landing the GLiNER extract (SVGs left out by the first
add, amended in) and the ACE extract (`html/2010.05006v4/rl.png`) for
`surveys/tokenizer-free-span-tagging`.

**Fix sketch:** an ignore pattern cannot express "referenced by the
Markdown", which is the real rule. Either have `related-work fetch` stage
referenced assets itself (`git add -f` the set it already computes for the
audit), or have `init` write `!extract/**/*.svg` / `!extract/**/*.png` /
`!extract/**/*.jpeg` re-includes and have `audit` reject a tracked asset
the Markdown does not reference. Apply the same change to the existing
surveys' `.gitignore` files in one sweep.
