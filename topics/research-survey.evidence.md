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
