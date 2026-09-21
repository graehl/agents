# Optional server

On a request to add a backend, run `npm run server:add` from this project.
It copies the vendored TypeScript server into `server/` and adds `npm start`
and server typechecking. It refuses an existing `server/` or `start` command
before writing: reconcile an already customized backend rather than rerunning
the scaffold over it. Inspect and retain partial files if an I/O error occurs.

Run `npm run typecheck`, `npm test`, and `npm run build`, then start it with
`PORT=<available port> npm start`. It binds only to `127.0.0.1`, serves `dist/`,
and provides `GET /api/health`. Confirm both the client and API through the
actual configured app URL. The server needs no new package installation.

This is a foundation for APIs, not persistence, accounts, or public hosting.
Keep APIs same-origin, validate input at the boundary, and never put credentials
in the browser bundle. Add data storage and authentication only when required.
Use HTTP requests or SSE unless the deployment path supports WebSockets.
Document the endpoint, process ownership, data location, and deployment change.
Static Pages hosting cannot run this backend.
