---
slug: related-work-lazy-image-sources
noticed: 2026-10-31
where: scripts/related-work (HTML visual extraction, `HtmlDerivationError("... visual has no source")`)
---

**Gap:** A blog page with an `img` element that has no `src` fails HTML
derivation outright, so the whole post gets no committed extract. Two
posts in the draft repository's
`research/speech-recognition/surveys/asr-encoder-interpretability` survey
hit this on 2026-10-31:

- `reid2023-whisper`, fetched through the GreaterWrong mirror
  (`https://www.greaterwrong.com/posts/thePw6qdyabD8XR4y/interpreting-openai-s-whisper`):
  the page has two bare `<img loading="lazy">` placeholders with no
  `src`, `data-src` or `srcset`. The LessWrong original fails earlier on
  `unsupported visual content: iframe`.
- `sadov2024-insider-whisper` (`https://builders.mozilla.org/insider-whisper/`):
  same error. A plain download's 17 `img` tags all carry `src`, so the
  offending element is in the saved page's requisites or another visual
  tag; not yet located.

Both posts were read from page text and are recorded `grounded: false`
with a `source:` note.

**Noticed while:** building that survey's related-work tree.

**Fix sketch:** Treat an `img` with no `src`, `data-src` or `srcset` as
decorative: drop it, record the count in `.fetched`, and keep the fidelity
check on prose. Fall back to `data-src`/first `srcset` candidate before
dropping. Keep the hard failure for `object`/`embed` without `data`, where
real content is lost. Add a fixture with a bare lazy placeholder.
