# Almanac: web pages as queryable local datasets

> An almanac dataset is a machine-local, queryable snapshot distilled
> from a web page — structured `data.json` plus attachments and a fixed,
> agent-authored `extract` script under `~/.cache/almanac/<name>/` —
> served by the shared `almanac` ACLI viewer and refreshed per its
> recorded mode (auto / headless / manual / frozen).

Topic: `almanac`

The skill's product is a dataset, not a program. A build session
(`skills/almanac/SKILL.md`) spends agent judgment once — finding the
data channel, designing the schema, writing the extractor — and
captures it as deterministic artifacts a model-free CLI can serve and
refresh. The importable engine (`almanac/cli.py`, reached through the
executable `scripts/almanac` wrapper and installed as `~/bin/almanac`)
is one shared implementation of query/refresh over any manifest;
per-site variation lives entirely in data, never in per-site viewer
code.

## Dataset layout

```
$ALMANAC_ROOT/                 # default ~/.cache/almanac, a local git repo
  <name>/                      # short kebab name, e.g. sts2-cards
    manifest.json              # provenance + schema mapping (below)
    data.json                  # extractor output (or transcription)
    extract                    # executable: argv[1] = URL or local file,
                               #   normalized JSON on stdout (absent when frozen)
    images/ …                  # optional attachment subdirs, preferably PNG,
                               #   referenced by relative path from data.json
  by-url/<slug>-<sha8> -> ../<name>   # canonical URL -> dataset mapping
```

The root is a **local-only** git repo (`register`/`update` commit,
best-effort): free diff history across refreshes and versioning of the
agent-authored extractors. It is never pushed.

`manifest.json` fields: `name`, `url`, `title`, `refresh`, `created`,
`fetched`, `checked`, `content_hash` (sha256 of normalized data.json),
and `schema`: `records` (dotted path to the record array; empty = data
root), `key` (unique-ish display key field), `columns` (3–4 minimal
default fields, per ACLI minimal-schemas), `filters` and `search`
(completion/search hints), plus optional `image` (the record field
holding a dataset-relative image attachment path). Free-form provenance
prose (which channel
the extractor reads, quirks) is welcome as extra keys.

## Extractor contract

`extract <source>` where `<source>` is the live URL or a local saved
file — the same script serves both, so a saved page and the live page
are interchangeable inputs. Emits the full normalized data JSON on
stdout, diagnostics on stderr, nonzero exit on failure. Deterministic
given identical source content. No arguments beyond the source; any
needed configuration is baked in at authoring time.

Record order is part of the contract: extractors emit records in the
page's reading order, and the engine's `query`/`search` preserve input
order — no re-sorting. For tier lists, within-tier position is the
site's ranking.

Position is carried in-band so a filtered or postprocessed subset never
loses it. The engine injects, at load (in memory only — never written
to `data.json` or included in `content_hash`):

- `seq` — 1-based reading-order position in the whole dataset. An
  extractor may emit its own `seq` (e.g. a real rank) and it wins.
- `n` — 1-based position within the *returned* rows of a `query`/
  `search` (the "order given the selectors" applied).
- `n_<fields>` — 1-based reading-order position within each declared
  selector group. Groups come from `schema.ordinals` (a list of
  field-name lists); default is each `schema.filters` field singly.
  `[["section"],["tier"],["section","tier"]]` gives a card its rank
  within its section, within its tier, and within its section+tier
  cell. Because these ride on the record, `show <one item>` reports
  the item's position in every such superset without a query.

## Refresh modes

The acquire ladder is probed at build time and the rung reached is
recorded as `refresh`:

- `auto` — plain HTTP fetch works; `check`/`update` run unattended
  against the manifest URL.
- `headless` — needs a real browser engine (client-rendered or
  interaction-gated content, or an interstitial JS check that clears
  for an honest browser signature); extractor drives headless
  Chromium itself. Still unattended.
- `remote` — extractor connects over CDP to a real Chrome the user
  runs (or this host's VPN origin), inheriting its fingerprint,
  session, and vantage. Engine passes the URL like `auto`; refresh
  needs that browser reachable, so it is user-assisted in practice.
- `manual` — nothing automatable reaches the content; extraction is
  still scripted but `check`/`update` require `--source <saved
  page/HAR>` from the user's browser.

Authorized-access framing (fuller wording in the skill): the user
runs almanac as an alternate browser for a page they have confirmed
they may access — the same content they could save by hand and attach
as the `manual` rung. Automating that authorized view with a real
browser signature or the user's own browser over CDP is ordinary
retrieval, not botting; an interstitial that auto-clears for a normal
browser is satisfied, not defeated, by presenting one. The honest
limit: this automates access the user already has, not a way to reach
resources they lack, and it does not call CAPTCHA-solver services or
forge tokens/rotate proxies to manufacture access.
- `frozen` — no machine-readable channel (text lives in images);
  `data.json` is a one-time agent transcription, no `extract` exists,
  and refresh means re-running the skill.

Change detection always diffs the **normalized extracted JSON**
(`content_hash`), never raw HTML — page chrome, ad slots, and build
hashes churn on every fetch; the extracted content is what matters.

Exit codes (`check`/`update`): 0 up-to-date or updated, 3 changes
found (`check`), 4 unknown dataset, 69 cannot refresh in this mode
(frozen; manual without `--source`), 70 extractor output no longer
fits the schema (site redesign — re-run the skill to repair), 75
acquire/extract failure. Stale data is never served silently: `info`
carries `fetched`/`checked`, and a broken extractor fails loud with
the repair path named.

## Engine and launchers

`almanac` follows `topics/agent-cli.md`: compact JSONL default,
`--pretty` human upgrade, `--toon` on the table verbs (`list`,
`query`, `search`), structured errors, `--acli-complete` (dataset
names with titles, record keys with column summaries, `field=` /
`field=value` filters with counts — filter values in page order,
hint rows for syntax, truncation, and no-match), and `--repl` (an
interactive shell over the same completion; rich menus when
prompt_toolkit is installed, install advice when not). `almanac
--repl <name>` — what launchers pass — binds the repl to a dataset:
each line then uses the launcher grammar (bare filters/search query
the bound dataset, verbs optional). `--help` and
`help <name>` end with the `acli: 1 complete repl toon` capability
line. Verbs: `list`, `query`, `show`, `image`, `search`, `info`, `check`,
`update`, `help`, `register`.

`image <name> <key>` resolves the selected record's `schema.image`
attachment and displays it only when stdout is a TTY. Auto mode uses the
Kitty or iTerm2 inline-image protocol when the terminal identifies itself,
Sixel through an installed `img2sixel`, or an installed `chafa`, `viu`, or
`timg` renderer. `--renderer` can select or disable that behavior, and
`--width` sets the native-protocol cell width. A non-TTY, an undetected
terminal, or a renderer failure succeeds with a compact structured fallback:
dataset, record key, relative image, resolved path, MIME type, renderer,
and reason. It never sends terminal escape sequences to captured output.
Attachment paths must remain inside their dataset after symlink resolution;
an escaping or missing path is invalid dataset data (exit 70).

`query` filter grammar: `FIELD=VALUE` (exact, comma = any-of),
`FIELD~TEXT` (substring on one field), `~TEXT` (substring across the
schema's search fields). Any other token is search text, not an
error: a bare word extends the preceding `~` needle (or starts one),
so `~flame strike` — and a launcher's bare `flame strike` — is the
single needle `flame strike`. Multiple `~` tokens AND together.

Help is example-driven: bare `almanac` (exit 0) and `-h` append a
dataset overview plus example invocations built from real record
values; `help <name>` prints that dataset's columns, key, filter
grammar, sample rows, and examples (`--prog` renders them in
launcher form).

`register` validates a built dataset, wires the `by-url` symlink,
commits, and writes a thin per-dataset launcher (`~/bin/<name>`:
bare = info, `-h`/`--help`/`help` = `almanac help <name>`, `--repl`
= the engine repl bound to this dataset, verbs (including `image`) pass through,
anything else = query filters/search) plus the `~/bin/almanac`
engine symlink if missing.
The generated shell only passes its dataset, program name, and untouched
argv to the engine. The engine owns that grammar—including leading output
flags and completion—so launchers cannot drift into a second parser.
The launcher head carries the zero-execution capability marker
(`# acli: 1 complete repl toon`).

Candidate integrations are kept in [almanac sketches](almanac.sketches.md).

## Design decisions

- **Dataset + shared engine, not generated per-site viewers** (vs.
  emitting a standalone CLI per site): query code varies only by
  manifest, so N generated viewers would be N diverging copies; the
  skill's output stays reviewable data plus one small extractor.
  Accepts a shared-engine version coupling across datasets.
- **`~/.cache` placement** (vs. `~/.local/share`): matches the
  `~/.cache/checkouts` precedent for machine-local web-derived state.
  Accepts that `manual` and `frozen` datasets violate strict cache
  regenerability — on this host `~/.cache` is scratch-backed, and a
  purge re-costs a browser save or a re-transcription. Deliberate:
  datasets are a few MB and rebuilding is cheap relative to split
  storage roots.
- **Refuse empty/keyless extractions on `update`** (vs. storing
  whatever came back): a tier list extracting to zero records means
  the extractor broke, not that the game lost all its cards;
  `--allow-empty` is the explicit override.
- **`by-url` symlinks beside name dirs** (vs. URL-keyed dirs): short
  names are the ergonomic handle (launcher, verbs); the slug+hash
  symlink answers "is this URL already built?" collision-free, which
  is what makes the skill idempotent.
- **Local git history in the root** (vs. dated snapshot copies):
  diffs across refreshes and extractor versioning for free; never
  pushed, so no remote coupling.
- **Explicit image field and structured fallback** (vs. guessing from record
  fields or always emitting terminal escapes): `schema.image` makes the
  attachment contract inspectable, while non-TTY callers receive a usable
  path without terminal-control bytes. Accepts one optional manifest field.
- **Small native renderers plus executable fallback** (vs. adding Pillow and
  a terminal-image library): PNG can travel directly over Kitty and iTerm2,
  while installed helpers cover Sixel and text-rendering terminals. This
  keeps the shared engine standard-library-only; uncommon formats may fall
  back to their path unless a helper can render them.
