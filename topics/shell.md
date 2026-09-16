# Shell tooling

> Shell scripts are formatted with `shfmt`, whose flagless defaults are
> exactly what the editor applies on save, and checked with `shellcheck`.

Topic: `shell`

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
