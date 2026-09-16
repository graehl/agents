# Shell tooling

> Shell scripts are formatted with `shfmt`, whose flagless defaults are
> exactly what the editor applies on save, and checked with `shellcheck`.

Topic: `shell`

Loaded before editing shell scripts or when first working in a shell-heavy
project (trigger: `AGENTS.global.md` § Language tooling).

Format with `shfmt -w <file>`; preview with `shfmt -d <file>`. The editor's
save hook runs `shfmt` with no indentation flags, so a flagless CLI run
reproduces the same bytes — pass `-i`/`-ln` only to answer a question, never
to write a file the editor would then reformat.

Flagless `shfmt` indents with tabs and expands `{ cmd; cmd; }` one-liners onto
separate lines. A repo wanting another style states it in `.editorconfig`,
which `shfmt` reads whenever those flags are absent, so both paths stay
identical. Match the glob to the files: `~/agents/scripts/` holds
extensionless scripts, which `[*.sh]` misses and `[*]` covers.

`~/agents` shell scripts predate this rule and mix two- and four-space
indentation, so formatting one wholesale is the reflow case in
`AGENTS.global.md` § Auto-format authored code: land the change first, sweep
separately.

Run `shellcheck` on a script you author or substantially change; it is not part
of the save hook, so nothing else will.
