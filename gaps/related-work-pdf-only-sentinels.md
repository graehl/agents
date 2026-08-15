---
slug: related-work-pdf-only-sentinels
noticed: 2026-08-15
where: surveys/shallow-surface-encoders/related-work/extract/
---

**Gap:** Four entries have completion sentinels for PDF URLs but no Markdown:
`boldsen2022-character-embeddings`, `mayer2020-distributional-classes`,
`kashioka1998-mi-character-clusters`, and
`liu2012-brown-character-clusters`. Three retain their PDFs; the Mayer entry
retains only its sentinel. `related-work audit` now reports these as
`extract-content` drift because a completed extract must contain searchable
text.

**Noticed while:** Backfilling saved survey HTML through the shared
HTML-to-Markdown facility and checking every survey for remaining
HTML-without-Markdown entries.

**Fix sketch:** Re-fetch these four explicit keys through the PDF/Marker path
after the normal accelerator and storage preflight, verify each resulting
Markdown against its PDF, and let the successful fetch rewrite the legacy
`url-html` sentinel as `pdf-marker`.
