# Run and deploy

`npm run build` typechecks and produces `dist/`. `npm run preview` serves only
that directory on loopback, choosing a free port unless `PORT` is set. It prints
the bound URL; keep the process alive while using the app and stop only processes
you own. The preview is for your own browser checks. Under Yep Anywhere the App
button serves `dist/` itself from the `.project-template/app.json` declaration,
so do not point an app address at a preview port or give its URL to the user.
The template does not modify YA's settings or restart its server.

## Keeping the visible app current

In YA versions with Live preview, turn on **Live preview** in the App pane.
The template declares `npm run dev` as a separate sandboxed service; YA owns
its port, scoped address, and lifetime. Vite watches the source and sends hot
updates or full reloads through that App address. Turn Live preview off to
return to the built `dist/` app. No application backend add-on is required.
Older YA versions ignore this declaration and retain Build/Reload behavior.
This declaration affects newly created projects; existing projects need its
`livePreview` entry and the matching `vite.config.ts` port/base-path support.

Rebuild after user-visible edits, including edits made after an earlier test
or screenshot. Verify the result from the declared served target before
ending the turn. For a static app, updating `dist/` changes the next page
load; it does not replace JavaScript already running in an open browser.
Use the App pane's Reload action when live updates are unavailable.

When using a development server, verify its update connection through the
actual App address. A loopback HMR check does not prove the app proxy carries
WebSockets. If hot updates fail, restore a working preview or use a verified
build and explicit reload, and state the limitation. Preserve the last working
preview on build errors and report the error rather than claiming the change
is visible. Restart an owned project backend when its code or configuration
requires it; never restart YA to refresh an app.

For static deployment, publish the complete built `dist/` tree to a destination
the user has explicitly configured and authorized. Assets use relative paths
for subdirectory hosting. Preserve old hashed assets while older HTML may be
cached. Verify the selected path; no personal Pages repository is inherited.
The initial template intentionally has no `publish` script until a destination
and authorization policy are known. A template may include a PWA manifest;
offline caching and device installation require separate implementation and
verification.

With the server add-on, `npm start` runs the TypeScript backend and serves the
same bundle. Static hosting cannot serve its API. Under Yep Anywhere the
add-on's process declaration lets YA start and stop it for the App button; do
not also leave a hand-started copy running. Keep it on loopback behind
the configured app proxy, use the proxy's app access controls, and add app
authentication when the intended exposure requires it. Do not publish secrets
or enable public access merely to make a preview reachable.
