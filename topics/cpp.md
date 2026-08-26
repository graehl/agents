# C++ tooling

Loaded before editing C/C++ files or when first working in a C/C++
project (trigger: `AGENTS.global.md` § Language tooling).

Reformat only modified lines, never whole files:
`git --no-pager diff --no-ext-diff --no-color -U0 HEAD -- '*.c*' '*.h*' | clang-format-diff -p1 -i`.
Use `clangd` to check edits when a `.clangd` is present.

## API changes

For an optional final aggregate/reference parameter, use a `const*`
implementation seam with inline present/absent wrappers.

By default, feel free to add optional args unless an `.so` is specifically
indicated as deployed standalone / stable ABI. At that boundary, preserve the
old exported symbol rather than relying on a default argument, which is only
source-compatible.
