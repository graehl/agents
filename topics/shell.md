# Shell tooling

> Shell scripts are formatted with `shfmt`, whose flagless defaults are
> exactly what the editor applies on save, and checked with `shellcheck`.

Topic: `shell`
Governs: first editing shell scripts in a repo

Loaded before editing shell scripts or when first working in a shell-heavy
project (trigger: `AGENTS.global.md` § Language tooling).

Format with `shfmt -w <file>`; preview with `shfmt -d <file>`. A flagless run
reproduces the editor's save byte for byte, so pass `-i`/`-ln` only to answer a
question, never to write a file the editor would then reformat.

That parity is conditional: conform's shfmt wrapper appends `-i <shiftwidth>`
when the buffer has `expandtab` set and no `.editorconfig` is found upward.
graehl's Neovim leaves `expandtab` off, so neither side passes an indent flag
and both get `shfmt`'s defaults — tabs, and `{ cmd; cmd; }` one-liners expanded
onto separate lines. A repo wanting another style, or insurance against that
branch, states it in `.editorconfig`, which `shfmt` reads when those flags are
absent and which also stops the wrapper adding any. Match the glob to the
files: `~/agents/scripts/` holds extensionless scripts, which `[*.sh]` misses
and `[*]` covers.

`~/agents` shell scripts predate this rule and mix two- and four-space
indentation, so formatting one wholesale is the reflow case in
`AGENTS.global.md` § Auto-format authored code: land the change first, sweep
separately.

Run `shellcheck` on a script you author or substantially change; it is not part
of the save hook, so nothing else will.

## Long-running scripts and edits under them

Bash reads a script file incrementally. It parses one complete command
(a line, or a whole compound command such as a function definition or a
`{ ...; }` group) and runs it before reading further from the same file
offset. If the file changes while the script runs, later commands come
from the new bytes at the old offset: half-lines, skipped or repeated
steps. A run's checkout updated by `git checkout`, `cp`, or an editor
mid-run has corrupted live jobs this way (speech program, 2026-11-04).

Two habits prevent it:

- **Read the whole script before running any of it.** Put the work in
  functions and finish with a single line that calls the entry point and
  exits:

  ```bash
  main() {
      ...
  }
  main "$@"; exit
  ```

  Bash parses each function body into memory when it reaches the
  definition, and reads the whole last line before running it. `exit`
  then stops it before it reads anything more, so later edits to the
  file can't reach the run. `exit` with no argument returns `main`'s
  status. Keep any other top-level code above `main`.
  - **Avoid** `main "$@" && exit 0 || exit 1`. It also reads the whole
    line first, but bash ignores `set -e` throughout a function called on
    the left of `&&` or `||`, so an errexit script silently stops
    stopping on errors inside `main`. It also collapses every failure
    status to 1.
  - **Wrapping the script** in `{ ...; exit; }` also works; the function
    form is easier to read.
- **Replace files, don't overwrite them.** A running bash keeps the file
  it opened. Writing a new file and renaming it over the old one (`mv`
  of a temporary file, `install`, `rsync` without `--inplace`) leaves the
  running process on the old copy. Truncating writes to the same file
  (`>`, `cp` onto an existing file, `rsync --inplace`, an editor that
  saves in place) change what it reads next. To edit a script while its
  runs are live, edit a copy and `mv` it into place, or launch runs from
  a separate, commit-pinned checkout.

Either habit alone protects the script's own text. Neither protects
other files the script reads later, such as `source`d files, helper
scripts it runs and configs, so launch long jobs from a pinned checkout
when those may change too.
