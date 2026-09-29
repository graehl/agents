After each change the user should see, update the app served by
`.project-template/app.json` before reporting completion. Run `npm run build`
for the static app and verify the changed behavior in that build. When a
live preview is running, verify the update reached it; a successful source
edit or build alone does not prove the open app changed. If backend changes
require a restart, restart only this project's owned app service and verify
readiness. Never restart the supervising Yep Anywhere server.
Under Yep Anywhere, use the App pane for delivery. If automatic refresh is
unavailable, say that the build is ready and ask the user to Reload the App
pane; do not imply an already-open app refreshed itself.
Loopback servers are for your own browser checks only; never hand the user a
`localhost` or `127.0.0.1` link, since they may be on another device.

Before running or deploying this app, read `instructions/run-deploy.md`.
Its runtime commands and App-pane metadata are in `.project-template/app.json`;
the initial preparation turn is `.project-template/PREPARE.md`.
