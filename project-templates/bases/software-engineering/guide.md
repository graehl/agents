# Software engineering

Read the relevant module and callers before editing. Name the behavior contract
behind a defect; fix its owner rather than adding caller-specific suppressions.
Use domain names consistently, keep one-use helpers local, and split at a real
behavior boundary. Prefer conventional code and the existing toolchain over a
new abstraction or dependency without a demonstrated need.

Validate external inputs at the boundary and fail clearly when required state
is absent. Do not swallow exceptions or silently substitute defaults to make a
broken path appear successful. Preserve public formats and callers, or identify
and document a deliberate migration before changing them.

Inspect current work before editing or staging. Keep intermediate states valid
when a watcher can observe them. Format changed code with the project's formatter,
run the affected checks, and report what passed and what remains unverified.
Use small scoped commits when committing is part of the task; never sweep other
work into them. Publication and destructive operations need the user's authority.

Keep a consequential unfinished defect in project documentation so the next
session can find it. Do not turn every change into a task-management process.
