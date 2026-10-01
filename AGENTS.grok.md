## Session identity

YA's published id is the native Grok UUIDv7 session-directory name.

Without a launcher or published id, recover only from provider/process
evidence tied to this live session. The newest session directory is a candidate,
not identity proof. Report unresolved identity.

## Logs

Sessions live at `~/.grok/sessions/<urlencoded-cwd>/<session-id>/`;
`GROK_HOME` overrides `~/.grok`. Conversation log: `updates.jsonl`.
Global provider-log searches exclude your session directory.
