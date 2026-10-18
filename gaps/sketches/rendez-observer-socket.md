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
- A request names the route (or `latest-session`) and the inbox-relative name,
  then streams the bytes. The observer applies the same naming, collision,
  size and burst rules, writes the original into the inbox (so rsync-style
  repeat transfers and attachment originals keep working) and its snapshot,
  and replies `published`, then the settled state.
- `receive` uses the socket when the marker advertises one and falls back to
  inbox publication otherwise, so senders need not know which observer runs.
- Authorization stays the filesystem's: the socket is mode 0600 under the
  user's runtime directory, matching the inbox's own permissions.

## Unresolved

- Whether YA should expose this socket itself or through its existing
  provider-host control socket, which already authenticates local clients.
- Whether the observer still needs to write the original into the inbox, or
  only the snapshot, given that the inbox exists for rsync's size and mtime
  comparison.
- How a sender on another host reaches it: over ssh, `receive` runs locally
  to the observer, so the socket stays host-local and needs no network
  exposure.
