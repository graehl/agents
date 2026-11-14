---
slug: acli-markdown-table-output
noticed: 2026-11-14
where: acli/emit.py, scripts/ya-artifact, scripts/reviews, scripts/not-ai-lint, scripts/claim-refs
---

**Gap:** the 2026-11-14 strict review
(`harsh-review/a7cd61e44a7c..5c0c4d26ad9e.verdict.md`, untracked) found
defects in the CSV/Markdown table output added by `38c5c154`.

Blockers:

1. `--md` falls back to text output in `emit` (`acli/emit.py`, `_resolve`
   and the text path), which then raises "commentary requires JSON/JSONL".
   `ya-artifact` and `reviews` disable commentary only for plain text, so
   `ya-artifact grant x.html --md` and any `reviews` verb with `--md` fail
   at their final output. Fix: `emit` disables commentary itself when it
   falls back from `--md` to text.
2. A carriage return in a cell survives the newline-to-space step and
   ends the Markdown row, breaking `topics/acli-spec.md`'s "a line break
   becomes a space". Fix: `" ".join(text.splitlines())`.

Advisories:

3. Display width counts nonspacing marks and joiners as width 1, because
   `unicodedata.combining` returns 0 for most of them; the test's own
   Sinhala string misaligns, and the test measures with the same function,
   so it cannot catch this. Fix: width 0 for categories Mn, Me, Cf.
4. Exported `markdown_table` silently drops columns when `right` is
   shorter than `headers`, raises `IndexError` on a short row, and
   truncates a long one. Validate lengths.
5. `emit._resolve` duplicates `session._normalize_format`; both gained
   `markdown`. Have `_resolve` call the normalizer.
6. The `--md` text fallback happens only when a tool passes `text=` to
   `emit`. `not-ai-lint` and `claim-refs` build their own text output and
   print JSONL under `--md`. Narrow the spec wording, or give those tools a
   shared predicate.

**Noticed while:** a periodic review triggered by an unrelated paper
citation commit.
**Fix sketch:** (1) and (2) are one-line fixes in `acli/emit.py` with
regression tests; (3)–(5) are small; (6) needs a choice between spec
wording and code.
