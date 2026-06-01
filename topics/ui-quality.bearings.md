# Bearings: ui-quality

Orientation for the UI design + verification + theming topic cluster.
Active backtrace is the chain of `[*]` from root to the deepest active leaf.

- [x] **ui-quality** — establish the UI quality concern and its tutorial portal
  > why: agents make default UI decisions without rendering/exercising the
  > result; we want one readable, well-sourced cluster the user can learn from
  > and that future agents must consult before UI work.
  - [x] Scaffolding & naming — 4 topic names fixed; 3 reuse TOPICS.md vocab
  - [x] Top-level tutorial doc (`ui-quality.md`) — covers all 3 at basic level
  - [x] Glossary rows — topic-linked (4) + typography/theme vernacular
    > why: user flagged missing typography/font/spacing/weight + theme/skin
    > vocabulary; these double as testable thresholds.
    > note: 13 vernacular rows still carry `<!-- unconfirmed: 2026-05-31 -->`
    > pending the user's prune/confirm pass.
  - [x] **functional-layout** — design-language subtopic (full draft)
    > why: the "legible, understood, responsive, stable" design contract,
    > incl. the user's no-jitter / viewport-anchoring requirement.
    - [x] Typography depth (scale, weight, rhythm, optical sizing)
    - [x] Convention & signifiers (Norman, Jakob's Law, NN/g heuristics)
    - [x] Responsive/intrinsic layout strategy
    - [x] ★ Stable layout: CLS, scroll anchoring, bottom/top anchor,
          resize-jitter repro & fix, motion + reduced-motion
  - [x] **ui-verification** — testing subtopic (full draft)
    > why: encode "render and look + exercise", since the cheap default
    > (a11y tree) is blind to the visual/interaction defect class.
    - [x] ★ Tree-vs-pixels duality → which defect class needs which
    - [x] Four layers (structure/appearance/behavior/responsiveness)
    - [x] Testable typography & spacing thresholds
    - [x] Interaction matrix recipe table (hover/click/long-press/type+Enter/resize)
    - [x] Mobile + TUI
    - [x] ★ Agent verification loop (render + vision mode, not snapshot only)
    - [x] What automated checks do NOT replace (baseline correctness, taste)
  - [x] **theming** — theme/skin subtopic (full draft)
    > why: cosmetic variants must not touch layout/behavior; density is the
    > boundary case.
    - [x] Design-token taxonomy + W3C format + CSS custom properties
    - [x] Presentation-only contract as a verifiable claim
    - [x] forced-colors / high-contrast; user/third-party skin sandbox
  - [x] **ui-report** — informal-skill checklist for periodic
        screenshot-backed audits
    > why: agents asked "is this UI good?" need a rendered tour and a
    > consistency-relative evaluation, not an a11y-tree opinion;
    > inverted-pyramid evaluation lands the most actionable finding
    > (inconsistencies vs. project's own baseline) at the top.
  - [~] Decide whether general-domain typography/theme terms should be
        surfaced as candidates for `~/agents/TOPICS.md` / `topic-definitions.md`
    > note: surfaced once to the user as a candidate set; awaiting their call,
    > not editing the global files autonomously.
  - [x] Commit the cluster (one commit, `Topic: ui-quality`)

## Open questions / asyncs

- User to prune/confirm the 13 `<!-- unconfirmed: 2026-05-31 -->` vernacular
  glossary rows (typography + theme terms).
- Does this cluster want a small worked before/after of a jitter-on-resize
  bug to ground the tutorial? `functional-layout.md` now carries a prose
  repro+fix; a runnable example is still optional.
- Typography boundary (font-family vs. type-scale) — resolved in
  `theming.md`: the typeface is a theme token *iff* metric-preserving;
  the scale is layout. Left here as the rationale of record.
