# Software aesthetic — evidence

## 2026-09-15 — speculative adoption of search-first discoverability rules

- **Source** — Dillon Mulroy's `write-discoverable-code` skill,
  <https://github.com/dmmulroy/.dotfiles/blob/main/home/.agents/skills/write-discoverable-code/SKILL.md>,
  read at repo HEAD `fcdf06013853c2e8e5718b620d3a2b481fbcedb9` (file blob
  `a5255e871516295283f0d1dc830bf389e8aea3e8`); the file's frontmatter
  says `license: MIT`, the repo carries no LICENSE file. User direction:
  take the ideas we agree with as coding-style defaults, deduplicated
  against the existing standard; do not install or use the skill itself.
- **Status: speculative, unvalidated here.** Adopted on plausibility and
  fit with the existing grep-first navigation habit, not on observed
  outcomes in this corpus. Upstream's one quantitative claim — on a
  ~700k-line monorepo, one-word exported names are globally unique 61% of
  the time, three-word 96%, four-plus 98% — is quoted, not reproduced.
  Every placed section carries a `<!-- speculative -->` marker pointing
  back here, and the frontier-capability-review register indexes the set.
- **Revision-pass targets** (retain / narrow / relax / retire each):
  - `software-aesthetic.md` § Comments › Search needles in the
    doc-comment site — the primary item, and the only one that departs
    from prior guidance rather than extending it;
  - `software-aesthetic.md` § Names are search queries (naming, filenames,
    one definition site, rename-with-behavior, deprecated alias);
  - `software-aesthetic.md` § Structure, the one-named-home bullet;
  - `software-aesthetic.md` § Types;
  - `software-aesthetic.md` § Strings that must be found again;
  - `software-aesthetic.md` § Discoverability check before committing;
  - `software-aesthetic.coordinated.md` § One spelling per concept and
    § Colocated tests;
  - `skills/harsh-review/SKILL.md` review-pass item 12, Discoverability.
- **Premise caveat** — upstream motivates the rules with "agents have no
  hover text, no jump-to-definition, and no memory between sessions".
  That is harness-dependent: Claude Code exposes an LSP tool, and this
  corpus has session memory and handoffs. The rules were kept because
  plain-text search remains the dominant navigation mode in practice
  (`rg` is the mandated search tool) and because the same properties help
  human readers; if semantic navigation becomes the default agent path,
  the naming-length and plain-phrase rules are the first to relax.
- **The load-bearing innovation, per the user** — grep needles in the
  adjacent doc-comment site: the plain-words phrase a reader would search
  for goes in the usual Doxygen/docstring/JSDoc slot next to a function or
  type name, and possibly its parameters; same-line placement is not
  required. User's words: "the useful innovation i saw in
  write-discoverable was the idea that grep needles should be in adjacent
  doxygen etc fn name comments, perhaps params also." It is a stated
  departure from the existing no-redundant-comments guidance
  (§ Comments "write none by default"), placed provisionally. Retirement
  condition, also the user's: it "may be judged unworthy of cost e.g. if
  agents are smart enough to search for project camelCase CamelCase
  under_score equivs of phrases". Landed as § Comments › Search needles
  in the doc-comment site, with that condition in the rule text.
- **Adapted rather than copied:**
  - Upstream's "one-line doc comment on every export" became the
    search-needle subsection above plus the constraint-the-signature-
    can't-say clause; an export whose name already spells its phrase and
    hides no constraint still gets nothing, so "none by default" governs
    everything outside that slot.
  - "Rename in the same commit" was made subject to `AGENTS.global.md`
    § Backward compatibility: a protected public name stays as a
    deprecated alias pointing at the new one (which also absorbs upstream's
    separate "mark dead ends" bullet).
  - "Keep strings whole" was scoped to identifiers a reader will later
    search for, excluding genuinely data-driven keys.
  - "Never use bare-role filenames" keeps upstream's own exception for a
    rigid path-is-the-meaning convention, which also covers a repo whose
    established layout is one `utils.py` per package.
  - "One spelling per concept" and "colocate tests" are project-wide, so
    they landed in the coordinated companion with the usual mixed-codebase
    fallback; the glossary is named as the spelling arbiter, matching
    harsh-review item 10.
  - Upstream's slogans ("a comment is a request; a required type is
    physics", "misinformation with a 100% open rate") were rewritten as
    plain statements per `agent-instructions.md` § Invariants.
- **Deduplicated against existing text** — the caller sweep, canonical
  utilities, single-use helpers next to their use, and split-at-a-seam
  rules already covered upstream's "one concept per file" mechanics; only
  the "where is X done?" naming test was added. "A module should make
  sense with its imports unread" was dropped as restating the naming rule.
- **Other candidates, provisionally accepted** — the user asked that any
  further worthy ideas be incorporated the same way and marked
  provisional. The remaining sections listed above are those: each is an
  extension of existing guidance rather than a reversal, each carries its
  own `<!-- speculative -->` marker, and each is a separate retain/retire
  decision at the revision pass.
- **Trace simulation** (`agent-instructions.md` § Verifying instruction
  changes):
  - *Mechanical doc lines:* an agent adds a doc line to every export.
    The subsection admits only the search phrase and the unsayable
    constraint; an export whose name spells its phrase and hides no
    constraint gets none, so "none by default" still governs the rest.
  - *Snake-case project:* `rate_limiter` in Python. `rg 'rate limit'`
    still misses it, so the needle applies equally; the retirement
    condition is about the searcher, not the casing convention.
  - *Python package convention:* a repo has `utils.py` in every package.
    The path-is-the-meaning exception applies; the rule bites only on a
    new bare-role file in a repo without that convention.
  - *Public API rename:* behavior of an exported library function changes.
    Backward-compatibility wins: new name plus deprecated alias, recorded
    per `topics/backward-compat.md` when consequential.
  - *Fifty event names in a loop:* the rule asks for fifty literals. That
    is the intended cost; the literal set is exactly the searchable
    surface. User-supplied keys are excluded by the data-driven clause.
  - *Existing camelCase exports:* the rules apply to new or renamed code;
    they do not license a repo-wide rename sweep (`design-thinking.md`
    § Scope discipline).
- **Not validated** — no outcome comparison; instruction trace only.
  Contributing-model: fable-5.1.
