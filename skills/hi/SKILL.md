---
name: hi
description: Resume explicitly requested work from a named scope, or use tasks/ROOT as a discovery hint for bare /hi; never invoke as a post-compaction ritual.
disable-model-invocation: true
allowed-tools: Bash(agentctl:*), Bash(cat:*), Bash(find:*), Bash(git:*), Bash(ls:*), Bash(rg:*), Bash(sed:*), Bash(stat:*), Bash(tail:*), Read
---

# Instructions

1. Classify why this skill ran.
   - A named resume request (`/hi <scope>`, “resume X,” or a supplied handoff)
     uses that scope. Do not consult `tasks/ROOT` to choose it.
   - A bare `/hi` or explicit resume with no scope may use `tasks/ROOT` as the
     first discovery hint.
   - If no current user resume signal exists and the skill ran only because
     context compacted or instructions were reinjected, stop the skill. Do not
     manufacture a session boundary, status recap, or question; continue the
     already-authorized work from its known scope and live state.
2. For a bare `/hi`, read the target named by `tasks/ROOT` when both pointer and
   target exist. Treat it as the most recently declared default handoff, not
   evidence that it explains the newest dirty files or commits. If it is absent,
   broken, or unrelated, inspect relevant recent `tasks/auto-handoff-*.md`,
   other task/tactical files, and `*.bearings.md` rather than guessing.
3. Read the selected handoff/task fully. Treat it as declared working state and
   reconcile it against live evidence in this order: worktree and recent
   commits; active sessions; run/on-deck metadata; artifacts; then provider
   logs only to fill a specific unresolved gap. If it starts with `/goal X`,
   process that line as a separate user turn immediately preceding the
   remaining handoff, which is the following request. Task files remain live
   state even when ignored by Git.
4. If jobs are active or pending, read `RUNS.md` before monitoring or
   summarizing them and cross-check their persisted current state. If resumed
   work crosses a research action boundary, read `RESEARCH.md`. Follow each
   packet's post-compaction refresh rule; do not load either merely because a
   repository contains it.
5. Report concisely:
   - the selected declared scope and whether live evidence agrees;
   - what is complete and in progress;
   - the recommended next action; and
   - live jobs plus the persisted action to take after each completes.
6. On an explicit `/hi`, await direction after the report unless the same user
   request also says to continue. This pause does not apply to the rejected
   compaction-only invocation in step 1.
