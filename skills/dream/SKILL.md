---
name: dream
description: Consolidate a doc project — dedupe and de-conflict glossary/topics, distill facts established in recent session history but never written down, and propose (never auto-apply) fixes, extending with diminishing license to other docs and, least of all, code. Use when the user invokes /dream or asks for a consistency/redundancy/consolidation pass over docs.
---

# Dream

Run a consolidation pass over a body of project docs. Two distinct
operations, and both matter:

- **Prune** — re-read the existing docs and remove contradiction,
  duplication, and staleness. Operates on what is already written.
- **Distill** — mine recent session history (transcripts, dirty files,
  run records, git log) for facts that were established but never
  captured, and propose adding them. Operates on what the docs do not
  yet reflect.

Pruning alone is the common reflex and it misses distillation — you
cannot prune in a fact that was never written. The distill step is the
part that is easy to skip and the reason to run this as a fixed
procedure rather than off the dome.

Output is **a proposal the user approves**, never a silent rewrite.
This holds everywhere, and the license to even propose narrows as you
move away from the project's own convention surface (see *Permission
gradient*).

## Targets

If the user names a target (a directory, a doc set), use it. With no
target, default to the project's convention surface: `GLOSSARY.md` and
any scoped sub-glossaries, plus `topics/*.md` and their `.bearings.md`
companions. That surface is home turf — it exists to be kept
consistent, and this is where the pass should be most thorough and most
opinionated.

**Instruction repos are a special case where the instructions are the
code.** In an agent-instruction repo (the authoritative `AGENTS.md` and
its world — `~/agents`), the convention surface is the whole instruction
corpus: `AGENTS.md`, `AGENTS.user.md`, the provider supplements
(`AGENTS.<provider>.md`), every `skills/*/SKILL.md`, and the
`~/agents`↔`~/bin` helper-script pair that the instructions require be
kept in sync. `topics/*.md` here are subordinate — instruction
subroutines elaborating the corpus, not the corpus itself. Treat the
whole corpus as home turf, and apply the load-bearing-instruction
discipline as the prune criterion: propose cutting entries that don't
steer beyond a capable agent's default, but **preserve deliberate
redundancy** (worked examples, rationale for counterintuitive rules)
that stops a weaker agent reasoning around a rule — that redundancy is
load-bearing, not duplication. Flag prompt debt that merely restates
defaults. Honor the global-vs-project routing of any rule you'd move,
and the instruction-file backup rule before proposing edits to files not
recoverable from git.

## Workflow

1. **Index the claims.** List every load-bearing claim across the target
   docs, one line each, with its source file. This index is the working
   set for steps 2–3 and the thing you diff against in step 6.

2. **Find conflicts and duplicates.** Flag pairs of claims that
   contradict or restate each other. For each, propose a single
   canonical home (prefer the narrowest-scope doc that owns the concern;
   for glossary terms, the nearest enclosing `GLOSSARY.md`).

3. **Find stale.** Flag claims the current tree falsifies — a named
   file, flag, function, or command that no longer exists, or a contract
   the code now violates. Stale claims are corrected or deleted, not
   merged.

4. **Distill from history.** Scan recent transcripts, commits, run logs,
   and dirty files for facts that were established but appear in no doc —
   a decided convention, a contract, a ruled-out approach, a non-obvious
   constraint. Propose where each belongs (a glossary row, a topic
   section, a new topic only if it clears the cross-cutting-concern bar).
   Do not re-derive from the code what the code already records; capture
   what was *decided*, not what is *visible*.

5. **Check cross-references.** Flag `[[links]]` and `Topic:` trailers
   with no target, and docs nothing points to. A dangling `[[link]]` is
   a candidate to write, not an error — note it as such.

6. **Emit a diff proposal.** Present the changes as a reviewable diff or
   a grouped list the user accepts or declines item by item. Do not
   apply. Hand-curated prose is never silently rewritten — the user's
   approval is the apply step.

## Permission gradient

The proposal-only rule is constant; how far you may reach with a
proposal narrows by surface:

- **Glossary / topics (home turf).** Propose freely and thoroughly,
  including enforcing the project's own topic-doc and glossary
  conventions. This is what the pass is for.

- **Other user- or developer-facing docs** (READMEs, setup/operator
  docs, design notes). May propose, with a lighter touch: flag the
  inconsistency and suggest a fix; do not rewrite the document's voice
  or restructure it. Surface, don't reshape.

- **Code (least license).** Only surface where a doc contract and the
  code disagree, or where a doc names code that has drifted, and propose
  a *specific, located* change as a pointer for the user to decide.
  **Never perform an automated or bulk refactor — ever.** A code
  proposal from this pass is a single named edit the user weighs, not a
  sweep. If you find yourself wanting to fix more than a few code sites,
  stop and hand the user the list instead.

## Cadence

Run on demand, not as a hook. An unattended pass that rewrites will
lossily flatten curated nuance — the value here is the checklist and the
distill step, not autonomy. `/loop`-able when you want it periodic.

## Anti-patterns

- Pruning only (steps 1–3, 5) and skipping distillation (step 4) — that
  is the off-the-dome version this skill exists to beat.
- Applying any edit without approval, however obvious it looks.
- Letting a code-drift finding turn into a refactor. One located pointer,
  never a sweep.
- Capturing what the code already records instead of what was decided.
