# TypeScript tooling

Loaded before editing TypeScript/JavaScript files or when first working
in a TS/JS project (trigger: `AGENTS.md` § Language tooling).

When a dependency's types cause an error, fix the root cause — a stale
`@types`/dep or a version skew — rather than deleting the code or casting
to `any` to silence it (an upgrade may be the fix, but it is a gated
action, not a reflex). Read third-party API types from `node_modules`
(`@types/`, or a package's bundled `.d.ts`); don't guess signatures.
Leave `no-explicit-any` and import-style rules to the project's
ESLint/`tsconfig`, not to instruction.
