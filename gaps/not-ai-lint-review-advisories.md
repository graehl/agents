---
slug: not-ai-lint-review-advisories
noticed: 2026-11-10
where: scripts/not-ai-lint
---

# not-ai-lint: advisories left open by the 2026-11-10 strict review

Opened 2026-11-10. Contributing-model: fable-5.2.

The strict review of the rebuilt `scripts/not-ai-lint` (range
`50a69f1ad81d..a8164da8541d`) raised four blockers, fixed the same day, and
these advisories, which are real and not yet fixed.

## `--manuscript` include handling

`manuscript_files` in `scripts/not-ai-lint` finds includes with one regular
expression over the root file with HTML comments removed.

- A quoted include path containing a space
  (`{{< include "sections/b c.qmd" >}}`) is dropped silently.
- An include inside a `::: {.content-hidden}` block or a code fence is
  still followed.
- A root-absolute include (`/sections/a.qmd`, which Quarto resolves from the
  project root) resolves to the filesystem root and exits 4.
- Includes inside included files are not followed.
- The function carries its own copy of `prose_text`'s HTML-comment pattern.

Resolution: move include discovery into `prose_text`, which already knows
comments, fences and hidden blocks, and have it return the ordered file
list. The PII paper in `~/draft` uses none of these forms today.

## Blanking creates one-line paragraphs

A short sentence directly above a table, a code fence, or display math
becomes an isolated one-line paragraph once the block below it is removed,
and the scan reports `[cadence] one-line paragraph`. The raw scan on the
same file reports nothing. Resolution: suppress that one rule for a line
whose following source line was removed as non-prose.

## Two div skippers in `prose_text`

`from_markdown` skips `::: {#refs}` without tracking depth and
`.content-hidden` with depth. A hidden block nested in a references div
ends the references skip at the inner fence, so the lines after it are
reported. The bare form `::: content-hidden` is not recognised. Resolution:
one depth counter for both.

## `--skip` accepts unknown categories

`--skip negation_first` (underscore) is accepted and skips nothing. The
category set belongs to the vendored scan (`CATEGORY_ORDER` plus categories
its rules name), so validating it means reading that from the scan.

## Findings from the second review, range `a8164da8541d..9dc1d6016a9c`

- The `BOLD` pattern reports `bold-inline` on `__init__` and
  `foo__bar__baz`, and on a run-in bold paragraph head, while a bullet's
  bold lead is exempt.
- `scan_text` calls `source.count(0)` once per line, which is quadratic in
  paragraphs, and `report` can raise `KeyError` on the `alone` field when a
  triad or participle hit maps to line 0.
- A word present in both the vendored slop list and the lexicon is reported
  twice at one position (`tapestry`).

## Earlier commit in the same range

`aee1b905` has no retained test for the scope-moved `agentctl stop` or the
requested-rebuild failure memory; `Builds.start(recipe, source, fresh)`
takes the recipe twice; `Freshness.inputs` re-splits a string that was a
list one line earlier; and the root case of
`test_remembered_process_that_may_not_be_signalled_is_dropped` returns as a
pass instead of a skip. The review's probes for these are under
`harsh-review/`, range prefix `50a69f1ad81d..a8164da8541d`.
