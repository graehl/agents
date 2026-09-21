# Run and deploy

`npm run build` typechecks and produces `dist/`. `npm run preview` serves only
that directory on loopback, choosing a free port unless `PORT` is set. It prints
the bound URL; keep the process alive while using the app and stop only processes
you own. YA can map its app name to that loopback port. The template does not
modify YA's settings or restart its server.

For static deployment, publish the complete built `dist/` tree to a destination
the user has explicitly configured and authorized. Assets use relative paths
for subdirectory hosting. Preserve old hashed assets while older HTML may be
cached. Verify the selected path; no personal Pages repository is inherited.
The initial template intentionally has no `publish` script until a destination
and authorization policy are known. A template may include a PWA manifest;
offline caching and device installation require separate implementation and
verification.

With the server add-on, `npm start` runs the TypeScript backend and serves the
same bundle. Static hosting cannot serve its API. Keep it on loopback behind
the configured app proxy, use the proxy's app access controls, and add app
authentication when the intended exposure requires it. Do not publish secrets
or enable public access merely to make a preview reachable.
