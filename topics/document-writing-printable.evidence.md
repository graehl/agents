# Printable document writing — evidence

Append-only companion to [document-writing-printable](document-writing-printable.md).

## 2026-10-17 — ARR desk rejection for a Times-metric clone

- **Incident (user-reported)** — ARR desk-rejected the multilingual PII
  paper (`~/draft`, ACL review build of 2026-09-29) for “wrong font
  throughout”. Its XeLaTeX template set `\setmainfont{Liberation Serif}`.
  That font has Times' metrics but is a different typeface with a different
  name. `pdffonts` showed LiberationSerif for the body. aclpubcheck,
  installed in `~/.cache/aclpubcheck-venv`, reproduced the error:
  `formatchecker.check_font` takes the font with the most characters and
  requires it to be at least 35% of all characters and to contain one of
  `NimbusRomNo9L-Reg`, `TeXGyreTermes(X)-Reg`, `TimesNewRomanPSMT`,
  `STIXGeneral-Reg`, `Inconsolatazi4-Reg`. A first fix attempt with URW
  `NimbusRoman` (the Times clone pdfLaTeX's `times` package uses) would also
  have failed, because the new URW name is not on that list. The repaired
  build uses `TeXGyreTermesX`, the official `acl_lualatex.tex` choice, and
  aclpubcheck reports “All Clear!” on a camera-ready variant.
- **Why the existing safeguards missed it** — the topic already said to
  verify font rules at submission time, and the PII builder already failed on
  missing glyphs and page overflow. Nothing compared the PDF's fonts with the
  venue's accepted names, so a clean, well-fitting render read as done. The
  user asked that every paper built with `~/agents` resources be protected.
- **Decision** — fix the tool first, keeping the instruction short (per
  `agent-instructions` § Verifying instruction changes: one costly failure
  justifies a short protection). `qmd_build/pdf_checks.py` /
  `venue-pdf-check` reads the PDF itself, so it covers project-local
  builders as well as `qmd-venue-pdf`. Characters per font come from
  `pdftohtml -xml`, which needs no new Python dependency and approximates
  aclpubcheck at the family level. For ACL it also runs aclpubcheck itself.
  `qmd-venue-pdf` checks embedding on every build, and checks the profile's
  rules when `checks` is set.
- **aclpubcheck behaviour worth knowing** — it exits 0 whatever it finds, so
  the wrapper reads `errors-*.json`. A clean run writes no report and prints
  “All Clear!”. On review PDFs it reports roughly 50 margin errors per page:
  the grey review line numbers, as its own marked-up page images show. Hence
  `--review`, which reports margin errors without failing on them, plus the
  instruction to recheck the camera-ready version.
- **Trace: project-local builder** — an older paper with its own builder,
  like the PII paper, is asked to “submit to ARR”. The activity route
  (producing a submission package) reaches § Venue submission path, whose
  first sentence names the command. `venue-pdf-check` is independent of
  the builder and catches the font. Passes.
- **Trace: venue with no profile** — a NeurIPS upload. The tool prints
  `PASS (embedding only)`, and the topic says to check font and size rules
  by hand and to add a profile. The risk is reading that PASS as
  compliance; the label on the output and the instruction both guard
  against it. Accepted.
- **Trace: Letter preference vs A4** — running `--profile acl` on the
  Letter-size preprint fails on paper size. An agent might “fix” the
  preprint to A4, against graehl's Letter preference. The rule targets the
  exact file being uploaded, and `paper-projects` now says a venue upload
  uses the venue's mandated size. Passes after that clarification.
- **Trace: review-mode noise** — without `--review`, the thousands of margin
  errors on a review PDF would teach agents to ignore aclpubcheck. With
  `--review` they are reported but do not fail, and genuine overflow is
  caught on the camera-ready recheck. Passes.
- **Open** — the PII paper's own `acl/qmd-venue-pdf.json` (the topic's
  reference instance) has drifted from `index.qmd` and fails before
  building; see `~/draft` gap
  `research/pii/frontier/gaps/acl-qmd-venue-config-drift.md`.
