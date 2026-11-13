# C++ tooling

> C/C++ formatting, checking, and API-change conventions applied before the
> first C/C++ edit in a repo.

Topic: `cpp`
Governs: first editing C or C++ in a repo

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

## Templates in library interfaces

Soft preference (graehl, 2026-11-13): in a C++ library, keep templates that
are implementation detail out of what its users include. When a facility's
callers do not need the template, hide it behind an ordinary declaration
and define it in the `.cc` (or in an internal header shared by the `.cc`
files that use it), even at the cost of a few lines of boilerplate, unless
that makes an observable material performance difference. The exception is
a facility whose efficient use requires the full template in the caller's
hands. A forward-declared template struct in a public header is negligible
but still better avoided.
