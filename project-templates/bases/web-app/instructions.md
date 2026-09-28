After a change the user should see, run `npm run build` so `dist/` is
current. Under Yep Anywhere the App button shows that build, declared in
`.project-template/app.json`: end the turn by telling the user to tap App.
Loopback servers are for your own browser checks only; never hand the user a
`localhost` or `127.0.0.1` link, since they may be on another device.

Before running or deploying this app, read `instructions/run-deploy.md`.
Its runtime commands and App-pane metadata are in `.project-template/app.json`;
the initial preparation turn is `.project-template/PREPARE.md`.
