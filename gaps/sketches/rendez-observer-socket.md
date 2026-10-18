# Rendezvous observer socket

Extends [rendezvous delivery](../../topics/rendezvous.md), whose `receive`
publishes into an inbox for the running observer to notice.

## Desired outcome

A sender reaches the observer itself instead of the filesystem. `receive`, or
any local tool, locates the project's running observer and hands it the bytes
and name over a local socket. The observer captures and delivers immediately
and answers with the outcome on the same connection, so there is no quiet
period, no inotify dependency, and no polling for `--wait`.

## Proposed approach

- Each observer (YA, `rendez watch --turns`, in-session `rendez watch`) listens
  on a Unix socket and advertises it in the `.observer.json` marker it already
  writes, for example `"socket": "/run/user/<uid>/rendez-<id>.sock"`. Keeping
  the socket outside the project avoids socket files on NFS and adds nothing
  to the project tree.
- A request names the route (or `latest-session`) and a name, then streams
  the bytes. The observer applies the same naming, size and burst rules and
  places the upload directly in `delivered/<route>/<id>/` as its snapshot and
  record, then replies `published` and later the settled state. The inbox is
  not needed: a proxied upload never also arrives by rsync, so it needs no
  original for size and mtime comparison or duplicate detection, and the
  attachment's open-original action falls back to the snapshot. A sender may
  still ask the observer to keep the full-size original there.
- `receive` uses the socket when the marker advertises one and falls back to
  inbox publication otherwise, so senders need not know which observer runs.
- Authorization stays the filesystem's: the socket is mode 0600 under the
  user's runtime directory, matching the inbox's own permissions.

## Unresolved

- Whether YA should expose this socket itself or through its existing
  provider-host control socket, which already authenticates local clients.
- The record's identity: without an inbox original, the event id cannot come
  from route, name and content alone if the same name and content may be
  proxied twice on purpose; a per-request id may be simpler.
- How a sender on another host reaches it: over ssh, `receive` runs locally
  to the observer, so the socket stays host-local and needs no network
  exposure.
