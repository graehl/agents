# Software aesthetic

> Shared criteria for how code should look and be structured — applied both when writing it and when reviewing it.

Topic: software-aesthetic
Governs: writing or reviewing code structure, naming, and boundaries

Every rule here is universal: it applies to a single unit of code regardless of project. Rules that only pay off when a whole project observes them live in [software-aesthetic.coordinated.md](software-aesthetic.coordinated.md).

## Core

The ideal piece of code is the shortest conventional, readable form that correctly expresses its contract. Cleverness earns its place only on a hot path where it measurably buys size or speed; anywhere else it costs the next reader more than it saves.

## Naming

A name should carry a known domain concept, so the reader navigates the code without holding all of it in their head — the right name does the work a comment otherwise would. This extends to predicates and booleans: name the concept they decide, even when the body is a single comparison. Avoid names a reader has to look straight through to learn anything: `Manager`, `Handler`, `Processor`, `Helper`.

### Names are search queries

<!-- speculative: adopted 2026-09-15 from dmmulroy/.dotfiles write-discoverable-code; revision-pass target — see software-aesthetic.evidence.md -->

Readers, agents above all, find code by plain-text search and read a small window around each hit, so every identifier is also a query, and a search miss costs wasted reads.

- Name an exported symbol so one search finds it: two to four words, at least one a domain word, and a generic verb with its object — `sanitizeEmailHtml`, not `sanitize`; `diffUserObjects`, not `diff`. Qualify only until the name greps uniquely, then stop.
- Put the disambiguating context in the symbol, not the module path. The import that separates `users/diff` from `orders/diff` sits at the top of the file; the search hit is at line 300. Exception: a rigid convention where the path *is* the meaning (every contract file exporting `Input`/`Output`).
- Filenames are names too. `utils`, `helpers`, `config`, `types`, `handlers` say nothing in a search result and collide across every module that has one; name a new file by the concept it owns (`billing-plan-config`). A bare `index` is fine only as a thin re-export.
- One definition site per symbol: move a function, never copy it, and delete the original in the same change.
- When behavior or audience changes, rename in the same commit — including visibility markers: a `_private` helper that other modules now import needs a public name. A stale name misleads every reader who finds it. Where § Backward compatibility in `AGENTS.global.md` protects the old name, keep it as a deprecated alias that points at the new one, so a search that lands on the dead end is redirected rather than misled.

## Comments

Write none by default. Add one only for a *why* the code cannot show on its own — a hidden constraint, a subtle invariant, a workaround for a specific bug. Never restate what the code does; the names already say it — and don't encode transient authoring context ("added for the Y flow", "used by X"): state the constraint that stays true, not the task that prompted the edit. Sharper still: never narrate the diff or the discussion that produced the code ("with X removed", "now using Y instead", "as we discussed") — that comment describes a before/after the committed source doesn't contain, so the next reader asks "why mention X when no X is here?". Such change-narrating comments are legitimate only in code shown for discussion, planning, or alignment — a chat reply, a plan, a review snippet — never in committed source. One line; no docstring essays.

### Search needles in the doc-comment site

<!-- provisional: a deliberate departure from "write none by default", adopted 2026-09-15; retirement condition below — see software-aesthetic.evidence.md -->

One redundancy is bought on purpose. A natural-language search does not match a compound identifier — `rate limit` finds neither `RateLimiter` nor `rate_limiter` — so the usual doc-comment site of a function, type, or parameter (Doxygen, docstring, JSDoc) carries the phrase a reader would search for, in ordinary spaced words: `/** Checks whether the user session has expired. */` above `SessionExpiryChecker`; `@param retryDelayMs delay between retries, in milliseconds` for a parameter. Same-line placement is not required; the ordinary comment slot adjacent to the name is. The same slot holds the constraint the signature cannot say — units, timezone, source time versus insert time, ownership, ordering — because a name search lands there. Nothing more: no restatement of the body, no essay. Retire this rule if agents demonstrably search for a project's camelCase, CamelCase, and under_score equivalents of a phrase on their own.

In C++, prefer `//` for short, one-line comments because they are easy to grep and scan inline. Do not write complex sentences that wrap across several `//` lines; if the explanation is useful at that length, use a C-style block comment so the prose reads as one paragraph to a human reader.

## Structure

- Delete complexity instead of relocating it. A reframing that makes the conditionals vanish beats one that gathers them somewhere tidier — and usually that means fixing the model, not the branches (a *deleting reframe*; see [design-thinking](design-thinking.md)).
- Decompose at *seams* — natural boundaries where behavior can change without editing the surrounding code.
- Put *spaghetti* — ad-hoc conditionals, mode flags, special cases threaded through unrelated flows — behind one abstraction, state machine, or module.
- Keep feature logic out of shared paths, and single-use helpers next to their use.
- Give each question-sized concept one named home. The code that answers "where is X done?" lives in a module named after X — the thing a reader asks about, not the mechanism inside — and an orchestrator reads as a sequence of calls into such modules, so a search that lands in it is one hop from the implementation. Split until that holds, then stop: a helper meaningful only inside one concept stays inline, and a file per tiny function scatters one answer across several reads. <!-- speculative: see § Names are search queries -->
- An element that must obey a container's contract belongs *inside* that container's representation, as an instance of it — not as a bespoke sibling rendered beside it. A sibling can't inherit the contract (e.g. a mini-sidebar's "collapsed → icon-only"), so it forces per-instance patching: the special case the invariant was meant to delete. Add to the existing representation in a form compatible with it; don't stuff a new element into adjacent space.

## Abstraction

An abstraction earns its keep on two conditions: callers can use it correctly without knowing its internals (it is not *leaky*), and it names a stable concept rather than just renaming a call. Pass-through wrappers and one-offs that re-implement a canonical helper are indirection wearing the costume of abstraction.

Duplication is correct at *divergence points* — copies you expect to evolve apart. The real smell is the opposite move: folding genuinely distinct cases into one function steered by mode or flag arguments.

## Types

<!-- speculative: see § Names are search queries -->

Prefer a required type over a comment for a precondition a caller must meet: the comment asks, the type refuses to build and names the concept in the error the reader corrects from.

- Distinguish primitive IDs by type — branded types in TypeScript, `NewType` in Python, newtypes in Rust, strong typedefs in C++ — so that transposing `userId` and `orgId` fails to compile instead of passing silently.
- Require a capability type for a privileged operation (an org-scoped connection rather than a raw one) instead of a comment saying callers must scope it.
- Model state as a discriminated union or variant, not a cluster of nullable fields with unstated rules about which combinations are valid.
- Name a type as it will be quoted back in compiler errors: `OrgScopedDb` explains itself; `Ctx2` does not. Every `any` or type-erased escape is a spot where the compiler goes silent.

## Strings that must be found again

<!-- speculative: see § Names are search queries -->

- Keep event names, flags, and error codes whole literals. Interpolating `` `github.${entity}.${action}` `` makes `github.pr.merged` unsearchable; write the full literal even when a loop feels drier. This governs identifiers a reader will later search for, not genuinely data-driven keys.
- Start an error message with a unique literal prefix so a line seen in a log greps straight back to its throw site: `Webhook signature mismatch for ${id}`, never `${prefix}: mismatch`. The run-log phase tags in `AGENTS.global.md` § Ideal coding are the same rule for log lines.

## Input boundaries

Guard at the top and assume valid below: prefer early-exit validation where input enters. (The output side — normalizing on the way in, repairing on the way out — is a project-wide commitment; see [coordinated](software-aesthetic.coordinated.md).)

## Sequencing and partial state

Do not impose order on work that is independent: false sequencing hides
available parallelism and misleads the reader about real dependencies. A
multi-step update that can be interrupted or observed half-applied is a
design bug — order the writes so every intermediate state is valid, or
make the whole update atomic.

## Size and performance

A file too large to hold in your head is a candidate for splitting at its nearest seam. On a hot path, refuse needlessly quadratic work — precompute, or lean on a known library contract, to reach n log n or better — and learn whether memory or compute is the bottleneck before you trade one away for the other. Treat recomputation as a design bug: reuse cached, prefetched, or intermediate results, and repair only the state that actually changed.

## Discoverability check before committing

<!-- speculative: see § Names are search queries -->

For new or renamed code, answer six questions: would one search for each new exported name find its implementation? Would swapping two arguments of the new function fail the build? Does the doc-comment site hold the plain-words phrase a reader would search for, plus the one thing the signature can't say? Does every log and error string exist verbatim in the source? Did anything change behavior without changing its name? When code moved, is it gone from where it came from?
