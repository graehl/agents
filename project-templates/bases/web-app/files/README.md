![Project thumbnail](docs/brand.svg)

# Web app

A working static web app starter, ready for your project description and ideas.

## Develop and verify

Use Node.js 22.18 or newer. From this directory:

```sh
npm ci
npm run typecheck
npm test
npm run build
npm run preview
```

Preview binds to `127.0.0.1` on an automatically selected available port and
prints its URL. Set `PORT` for a specific port. `npm run dev` runs Vite for
local development. The built `dist/` directory uses relative URLs and can be
hosted at a subpath or inside YA's isolated App pane. Serve it over HTTP(S);
browser module restrictions mean opening `index.html` with `file://` is not a
supported test path.

`npx playwright install chromium` installs the browser once;
`npm run test:browser` then checks the built app at desktop and phone sizes.
Use `npm run format` and `npm run format:check` for formatting.

## Add a server

`npm run server:add` activates the vendored optional backend. Then rerun checks
and use `PORT=<port> npm start`. See `instructions/server.md` for its scope,
failure behavior, and API. No template-source checkout is needed.

## Project layout

- `main.ts` and adjacent modules/styles: application code, without a `src/` wrapper.
- `tests/`: behavior and browser checks.
- `scripts/`: setup, static serving, and server activation.
- `instructions/`: scoped, editable project guidance.
- `.project-template/`: vendored preparation/add-on content and creation intent.

## Documentation skill

Ask your agent to use **redoc** to refresh the README, descriptions and project
thumbnail as the app evolves. In a harness with skill invocation, select redoc
from its skill picker (Codex: `$redoc`); you can also ask in ordinary language.
Its instructions are in `.agents/skills/redoc/SKILL.md`.

Deliberate later name/description edits can be protected in the project-local
`.project-identity.json`. Redoc preserves that human text exactly and can add
an agent coda. Initial creation intent remains open to refinement.

Read `instructions/run-deploy.md` before deployment. No publishing destination
or credential is configured by default.
