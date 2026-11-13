# research-survey — evidence and decisions

Append-only notes supporting the field-survey and frontier-map contracts.

## 2026-07-30 — survey is the effort; map is the product

- **Decision:** retain `surveys/<field>/survey.md`; rename the governing
  supplements from `survey-field.md` / `research-frontier.md` to
  `field-map.md` / `frontier-map.md`.
- **Reason:** “survey” is the recognizable research effort and collection;
  “field map” and “frontier map” are the persistent objects maintained and
  referenced by instruction and personal mastery state.
- **Scope extension:** repurpose the existing specs for addressable concept
  nodes, plausible discovery paths, a provisional claim inbox, and sparse
  mastery references rather than creating a parallel knowledge-map framework.

## 2026-08-22 — surveys default grounded and canonical

- **User decision:** `light`, `recall`, and `ungrounded` are aliases for one
  conversation-only mode: do not download a primary-source corpus and do not
  create or modify survey artifacts. A field- or frontier-survey request with
  no such modifier is grounded and persisted by default.
- **Location:** grounded surveys default to the canonical cross-project tree at
  `~/agents/surveys/<field-slug>/`; a project-local survey requires an explicit
  user location choice.
- **Boundary traces:** `brief grounded survey` stays concise and verified;
  `light frontier survey` returns speculative chat output and writes no
  `frontier.md`; `what is known about X?` remains an ordinary explanation
  unless it actually requests a survey.

## 2026-11-13 — per-paper results are committed

- **User decision:** a grounded survey commits our understanding of each
  paper read, emphasizing the purpose of the read, and not only the
  extracted text. Concept level is sufficient: the summary-level result
  for a paper is saved in sections of the concept page or pages. A reader
  may also produce one per-paper summary whose filename relates to the
  extracted Markdown.
- **Gap this closed:** the contract required concept pages but did not say
  that each reader's per-paper result must land in one. During the
  `punctuation-case-restoration` survey, three delegated readers were first
  briefed to return digests in their final reply, which would have survived
  only as whatever the synthesis kept.
- **Placement of the optional file:** `related-work/readings/<key>.md`,
  outside `extract/`, because the engine treats Markdown inside
  `extract/<key>/` as the extract (it renames a lone `*.md` there to
  `<key>.md` and hashes it).
- **Not done:** `related-work audit` and `status` do not check or count
  per-paper summaries.
