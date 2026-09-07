# Backward compatibility

> Observable compatibility breaks and shims are recorded here so future
> changes can check whether a surface has already made a contract decision.

Topic: `backward-compat`

## Decisions

- 2026-09-07 acli v1 specification — separate the portable user guide and
  normative spec from implementation advice and future sketches; allow
  partial capabilities declared by help or an agent guide. The indicative
  deferral envelope is a proposal, not a required v1 wire protocol. No version
  bump: the user explicitly permits revising v1 before public adoption.
- 2026-09-07 acli Python output/errors — empty list/tuple results now emit
  one `[]` JSONL record, parser errors use the structured usage envelope, and
  result/error writers reject non-finite JSON numbers before writing the
  affected value. Completion retains its separate zero-record convention;
  the almanac launcher writes candidates individually. These correct the
  intended contracts under the user's explicit instruction to fix the gaps.
- 2026-09-07 `agentctl clear` — waits and streams notices by default, by
  explicit user direction; `--no-wait` preserves the immediate blocked or
  carveable verdict, and `--drop` stays immediate. `--deaf` waits without
  accepting notices. Existing one-shot regression callers use `--no-wait`;
  coordination instructions and CLI help describe the choice.
- 2026-09-07 `tagged-stages/1` tool-output matching — `whitelist` is always
  additive to declared descendants; it no longer closes matching by its
  presence. Use `closed: true` for a finite accepted set; false or omitted
  accepts every valid path when tool tags are enabled. No legacy matching
  shim or version bump, by explicit user direction: update the sole existing
  prototype in place. Quick inline lists retain their exact-path interpretation.
- 2026-08-28 `agentctl fleet-watch` stdout — changed the single wake/timeout
  result from ad-hoc prose to the standard acli object (`kind`, `reason`,
  `events`, `fleet`), compact JSONL by default for agents/pipes and pretty
  JSON for interactive humans. `--full` exposes the wider snapshot and
  errors now use structured stderr envelopes. Wake conditions and exit 0/1
  semantics stay compatible; no prose shim, because retaining an
  unstructured branch would defeat the requested acli contract.
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
