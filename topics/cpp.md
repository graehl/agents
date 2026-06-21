# C++ tooling

Loaded before editing C/C++ files or when first working in a C/C++
project (trigger: `AGENTS.md` § Language tooling).

Reformat only modified lines, never whole files:
`git --no-pager diff --no-ext-diff --no-color -U0 HEAD -- '*.c*' '*.h*' | clang-format-diff -p1 -i`.
Use `clangd` to check edits when a `.clangd` is present.
