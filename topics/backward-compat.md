# Backward compatibility

> Observable compatibility breaks and shims are recorded here so future
> changes can check whether a surface has already made a contract decision.

Topic: `backward-compat`

## Decisions

- 2026-07-05 `agentctl` active-session stdout — changed `active`,
  `others`, `tending`, and `alone` default non-TTY/agent output from prose to
  ACLI JSONL; agent-first output is the contract from `topics/acli.md`.
  Exit codes and `.agentctl/active` side effects stay compatible; `--pretty`
  gives indented JSON rather than restoring the old prose, because a text shim
  would keep the unstructured output path alive.
- 2026-07-31 research-program discovery — a program root now needs a
  `Research program:` line in its `research/<program>/GLOSSARY.md`; bare
  presence of that file no longer declares one. Breaks any program glossary
  written under the 2026-07-30 rule, which falls back to the project-wide
  advisor until the line is added; no shim, because detection-by-presence
  collides with `topics/glossary.md` telling every subtree to create a
  `GLOSSARY.md` as soon as local jargon recurs — the two rules cannot both
  hold, and a one-day-old convention is cheaper to migrate than to alias.
- 2026-08-13 research-program discovery — `research/<program>/PROGRAM.md` is
  now the sole program declaration and canonical narrative charter; the
  directory basename remains the slug. A legacy `Research program:` glossary
  header may coexist but no longer declares a program. Listed active projects
  are migrated in the same change so header-only discovery needs no shim.
- 2026-08-13 program identity — a program's directory path is its canonical
  locator; an optional first-line H1 is an alternative formal name. A research
  program's directory basename remains its local slug but does not replace the
  path locator.
- 2026-08-28 acli capability line — the TOON token is spelled `+toon`
  under the new bare-vs-`+` token classes, the footer/banner stays
  `acli:`-prefixed, `capabilities=()` now renders the bare baseline claim
  `acli: 1` instead of suppressing the line, and the owning topic renamed
  `topics/agent-cli.md` → `topics/acli.md` to match the printed token. No
  shim: v1 is not yet publicly adopted; the known consumers (this repo's
  scripts/tests, YA's registration grep on `^acli: ` and comment
  references) were swept in the same change.
- 2026-08-15 `LengthRatioPolicy.factor_995` — renamed to
  `coverage_factor`, including serialized records and documented CLI naming,
  because configurable coverage made the percentile-specific name false. No
  shim: the surface was introduced in the still-unreleased reviewed range and
  every in-repository caller was migrated before persisted consumers formed.
