# Rendezvous file delivery

> Rendezvous delivers files dropped into a project's `.rendez` directory to
> an explicitly selected session or the session most recently messaged by the user.

Topic: rendezvous

The CLI implements session subscriptions, Linux watching, explicit scans, and
held-upload release. YA implements the same protocol natively in its server,
with opt-in watching and attachment previews; it does not run this CLI.

## Helper commands

Expose `~/agents/scripts/rendez` on PATH (for example through `~/bin/rendez`).
The script runs through `uv`, which supplies Python 3.10+ and Pillow for image
preparation; no system image packages are needed.
The watcher uses Linux inotify; one-shot `scan` works on other POSIX hosts.

```bash
rendez watch            # inside a session: receive uploads to .rendez/<session>/
rendez watch --turns --project /work/a --project /work/b   # project daemon
```

Plain `watch` is the simplest form: the observing session owns its route. It
subscribes the session's named destination `.rendez/<session-id>/` (or
`--route NAME`) and prints each completed upload there as output, which is the
delivery. It never moves `latest-session` and ignores other routes.

`watch --turns` observes every subscribed route, including `latest-session`,
and delivers each upload as a user turn through `session-turn` and the provider
service. It observes only projects named by `--project`, which it requires and
accepts repeatedly. Every command resolves a relative or unexpanded `~/`
project path under the home directory, as an ssh command line would, so
`--project oss` means `~/oss`; without `--project` it uses the current
directory. `--native` additionally permits blocking native resume when
the provider service is absent, and requires a subscription that allows waking.

At most one project observer serves `latest-session`: YA while its rendezvous
watching is on for the project, otherwise this daemon. Each writes
`.rendez/.observer.json` (owner, host, pid, Linux process start time) by
exclusive creation and removes it on exit; a second one refuses to start with
the first's identity. A marker from this host whose pid is gone, or now belongs
to a later-started process, is replaced, so a restart is never a conflict. A
marker from another host must be deleted by hand once its owner is gone. This is
a startup check, not a lock; the event claims below still keep an accidental
second observer from sending an upload twice.

Inside a launched session, `--harness` and `--session` default to its launcher
identity. Supply `--provider-session` when the native provider id differs from
YA's id. `subscribe` prints a stable inbox path without starting an observer;
subscriptions default to `--live-only`, and `--wake` explicitly allows revival.
`scan` processes completed transfers once, in either delivery mode. The turn
adapter uses 2000 pixels on the long edge and 4 MiB unless the provider service
supplies the target's profile.

Inspect `.rendez/delivered/<route>/<id>/record.json` for `held`, `accepted`, `failed`, or
`uncertain` delivery. `scan --turns` reconciles uncertain provider receipts; it
never blindly retries them. Output, YA, and native uncertainty requires
checking the target transcript. A confirmed failure can be resent under a new
incoming filename.
Identical content at the same route and filename is delivered once, even across
watcher restarts. A file over 64 MiB fails explicitly. A scan of one directory
tree logs and skips entries beyond 10,000; observers take at most 128
subscribed routes and 1,024 watched directories.

Uploads may sit in nested folders below an inbox. Each non-hidden file is
delivered separately under its inbox-relative name, such as `123/shot.png`,
which is also the record's `originalName` and part of its event id. Folders
are watched as they are created or moved in. Symlinks are never followed and
a directory reached twice is skipped, so there is no depth limit.

Records carry `originalSize` and `originalMtimeNs` (a decimal string). An
observer indexes them at start and skips any original whose size and mtime
still match, as rsync does, so restarts do not reread an accumulated inbox.

Senders write into `latest-session/`, never over it. Until a user turn is
recorded, observers point it at `.no-session-messaged-yet/inbox`, whose parent
never exists, so `test -d`, scp and rsync fail rather than create a directory;
after the first turn it stays pointed at the latest session. If
`latest-session` is nevertheless a real directory (rsync creates one when the
pointer is absent), the next pointer update or observer start moves it to
`unrouted/<epoch-ms>-<id>/` undelivered, since nothing was listening, and
restores the symlink. `unrouted` is a reserved route name.

## Bursts and slow acknowledgements

Both observers use `--window-ms 1000 --max-per-window 10` by default. Uploads
begin delivery immediately. Each route admits at most ten new uploads in a
rolling one-second window; the observer also caps uploads awaiting acceptance
at ten across its project. Image preparation and transport run separately from
arrival observation, so a slow acknowledgement cannot turn a burst into an
unbounded delivery queue. Acceptance means queued by YA or the provider worker,
not necessarily sent to the model or completed.

Excess uploads receive persistent `held` records. Once overloaded, a route
keeps holding arrivals until four configured windows pass without a new upload
(four seconds by default). The quiet interval only permits future arrivals;
it never releases previously held uploads, including after a restart or scan.
One additional overload notice per burst tells the recipient that many files
were uploaded, potentially unintentionally, and identifies the records by
directory and `burstId`. Notices are separate from the upload allowance.

Held records retain the original path and hash, without archiving another
full-size copy. Holds exist to undo accidental high-rate placement, not to
defer delivery; re-uploading under a new name is the ordinary way to send one
anyway. A manual override exists:

```bash
rendez --project /work/project unhold ROUTE DELIVERY_ID [--turns]
```

This bypasses automatic limits, verifies that the original has not changed,
then copies, prepares, and delivers it: printed by default, or as a turn with
`--turns`. It fails if the original was overwritten or the record was already
unheld. `--native` additionally requires the subscription's explicit `--wake`
permission. YA offers no unhold.

Normal rsync writes dot-prefixed temporary files and publishes completed files
by rename. The observer ignores dot-prefixed entries and directories, including
`.~tmp~`; `--delay-updates` can publish a large burst of final renames. Avoid
`--inplace`, `--append`, and non-hidden working files inside a watched inbox.
An external `--temp-dir` on another filesystem cannot supply atomic rename.
See the [rsync manual](https://download.samba.org/pub/rsync/rsync.1).

## Design decisions

- Immediate admission plus persistent holds, rather than delaying every upload
  to classify a whole burst: ordinary screenshots arrive promptly, while excess
  uploads never become a later trickle of model turns.
- A separate bounded delivery worker, rather than measuring the rate after
  each send: arrivals count even while preparation or acceptance is slow.
- YA owns its optional watcher lifecycle for now; explicit helpers use the
  same protocol. Provider-owned headless monitoring remains a possible extension.
- No locks. YA's Node runtime has no `flock`, and NFS makes cross-host locking
  unreliable, so every coordination point is an atomic file operation that
  works from Python and Node and on NFSv3 or later:
  - capture: renaming a capture directory onto an existing, never-empty event
    directory fails, so one observer creates each record;
  - send: exclusively creating `<event>/claim` grants the one-time right to
    send. A claim is never released; a pending record found already claimed
    becomes `uncertain`, never resent;
  - `latest-session`: each user turn creates an empty entry
    `latest.d/<16-digit epoch ms>-<route>`; the writer points the symlink at the
    newest entry, re-lists, repeats until no newer entry appeared, and deletes
    older entries. The last writer to look leaves the pointer correct;
  - burst state: `.admission.json` is rewritten without coordination; only a
    second concurrent observer, which is unsupported, could miscount arrivals.

## User contract

The directory is `.rendez`, not `.rendezvous`. A subscription creates a stable
session destination and may expose a named alias. `latest-session` points to the
last session accepting an actual user-initiated turn in that project. YA,
provider-host delivery, and `session-turn` participate. Coordination messages
(including takeover and release notices), automatic turns, and rendezvous
delivery never advance the pointer. Origin is explicit metadata, independent
of the provider's `user` role.

YA watching is opt-in globally, with project inherit/on/off overrides, and
active only while the project has a verified live session. Provider-host-owned
sessions count even when YA does not own them. Watcher lifecycle need not be
owned by the provider host: YA can also use its own verified live processes
when provider hosting is disabled. With YA watching off, `rendez watch --turns`
serves the same directories; in-session `rendez watch` serves only its own
route under either. Claims keep any accidental second observer from sending an
upload twice. First creation excludes `/.rendez/` through the repository-local Git
exclude file, never `.gitignore`. Enabling rendezvous explicitly authorizes this
directory; it does not change YA's general project-storage policy.

Uploads are pinned to a concrete recipient before delivery. A later change of
`latest-session` never redirects an already received upload. Sender helpers
publish completed files by temporary-name plus atomic rename. Creation alone
does not establish completion. An optional watcher performs no model work while
idle, reconciles pending uploads after restart, and exposes failed or uncertain
delivery rather than silently losing it or selecting another recipient.

An upload queues behind active work. Latest-session delivery is non-reviving by
default: an inactive target is not resumed merely because another session in
the project is live. An explicit subscription may opt into revival. Delivery reuses `session-turn`
admission and receipts; uncertain acceptance is reconciled before retrying.
Per-upload and per-recipient identities remain stable. Bounded host receipt
retention is not an eternal exactly-once guarantee.

## Images and presentation

Leave incoming originals in place, preserving ordinary rsync size/mtime
comparison. A changed file is identified by its content hash. Copy it into
`.rendez/delivered/<route>/<delivery-id>/` before preparation; never move the
incoming file or hard-link a snapshot to a path that may be overwritten.
A delivery adapter owns the image-preparation profile for its target session;
watchers contain no model catalogue. Local profile selection and preparation
require no model turn. Retain only the prepared snapshot permanently, without
a second full-size original archive.

YA displays one normal attachment with its original filename, thumbnail, and
optional caption. Opening it can expose the incoming original while its hash
still matches the upload; after an overwrite, use the retained prepared copy.
The model receives the stable prepared path; original/prepared paths, original
hash, and dimensions remain in the attachment record without duplicate chips
or visible preprocessing commentary. This
presentation works regardless of which watcher delivered the turn. The normal
attachment contract remains file-reference delivery, not a promise of inline
vision input to every provider.

## Implementation boundaries

- `~/agents` owns the filesystem protocol, explicit subscribe/watch CLI,
  retained upload records, observer coordination, and native transport fallback.
- `session-turn` owns delivery, explicit origin, and the target's preparation
  policy; the YA provider host supplies enhanced admission and session facts.
- YA owns its global/project settings, optional watcher lifecycle, publishing
  actual user activity, and displaying originals through authorized file access.
- Watching remains interchangeable. No agent must keep a model turn open merely
  to wait for files. Disabling an observer releases its resources without
  deleting uploads or subscriptions.

## Delivery sequence

1. Initialize a subscription and resolve a concrete destination.
2. Finish transfer and copy the incoming bytes into the delivery directory.
3. Claim the event, freeze its recipient and submission id, and select the
   preparation profile through the delivery adapter.
4. Prepare any derivative, persist the attachment record, and submit one turn.
5. Persist acceptance/failure/uncertainty; reconcile receipts on interrupted
   attempts. YA reads the same durable attachment identity for presentation.

## Acceptance

- Latest routing changes on user turns through YA and the helper, but never
  on coordination, takeover, release, or rendezvous turns.
- Explicit subscriptions work with YA watching off; duplicate observers cannot
  duplicate an accepted upload, and a latest-pointer switch cannot redirect it.
- Partial transfers are not delivered. Restart preserves pending uploads and
  does not blindly retry uncertain accepted turns.
- Incoming originals remain untouched by image preparation. Small files avoid
  needless recompression, and large files follow the adapter's profile.
- YA renders one attachment after transcript reload. Opening an overwritten
  original falls back to the historical prepared snapshot. Browser uploads
  retain YA's existing storage policy; rendering supports both locations.
- Disabling YA watching stops its observer; default-off creates no project
  files. First initialization excludes the private directory.

## Later sketches

Named broadcast channels can reuse subscriptions. Freeze the recipient set at
event acceptance, retain a receipt per recipient, and do not let fan-out update
`latest-session`. A YA recent-uploads view can project retained records without
becoming the delivery authority. Neither extension is needed for the first
latest-session and explicit-session implementation.

A smart SSH receiver is deferred: route and filename are CLI arguments, input
bytes arrive on stdin, and the receiver atomically selects a non-colliding
destination and submits once without a duplicate watcher send. The first
workflow is ordinary rsync with temporary-file-and-rename publication. Direct
scp closes are observable, but an interrupted transfer may also close an
incomplete file; explicit one-shot scans are for completed transfers.

The YA-facing upload guide is
[topics/rendez.md](https://github.com/graehl/yepanywhere/blob/main/topics/rendez.md).
