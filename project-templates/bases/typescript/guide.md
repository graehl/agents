# TypeScript

Keep TypeScript strict. Resolve third-party type/version mismatches at their
source rather than hiding them with `any`, casts, or disabled checks. Read the
installed API types before guessing a signature. Keep browser code separate
from Node tooling and server-only imports.

Use `npm ci` with the committed lockfile. `npm run typecheck` checks types;
`npm test` checks behavior; `npm run build` produces the static bundle. Run
`npm run format` on authored files before committing and `npm run format:check`
to verify consistency. The template pins its tool versions; deliberate upgrades
update the lockfile and rerun the relevant checks.

Keep runtime dependencies small and justified. The canvas starter needs no UI
framework. Retain portable relative asset paths when changing the bundler.
