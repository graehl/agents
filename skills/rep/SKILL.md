---
name: rep
description: Repeat or self-pace a prompt across wakeups. Use for /rep commands that should run now and then continue until completion, especially when there is no explicit every clause, with optional fixed intervals delegated to a future /chron skill when available.
---

# `/rep` - repeat a prompt until it is done

Parse the input into optional `until`, optional `[interval]`, and
`<prompt...>`. Run the prompt now. Then re-arm only when another run is
actually useful.

`/rep` must be usable without `/chron`. If `/chron` is available, use it
for fixed cron-style recurrence. If `/chron` is not available, use
`ScheduleWakeup` for session-local repetition. If no wakeup/scheduling tool is
available, run the prompt once and say no loop was armed.

## Parsing

Parse in this order:

1. **Leading `until` modifier**: if the first token is exactly `until`,
   set `until: true` and remove it.
2. **Leading interval**: if the first remaining whitespace-delimited token
   matches `^\d+[smhd]$` (for example `5m`, `2h`), that is the interval;
   remove it.
3. **Post-interval `until` modifier**: if an interval was removed and the
   next token is exactly `until`, set `until: true` and remove it. This makes
   `/rep 5m until /wish polish the UI` valid.
4. **Trailing "every" clause**: otherwise, if the remaining input ends with
   `every <N><unit>` or `every <N> <unit-word>` (for example `every 20m`,
   `every 5 minutes`, `every 2 hours`), extract that as the interval and
   strip it from the prompt. Only match when what follows `every` is a time
   expression; `check every PR` has no interval.
5. **No interval**: otherwise, the entire remaining input is the prompt and
   `/rep` runs in dynamic mode.

Normalize interval unit words to single-letter units:
`second(s) -> s`, `minute(s) -> m`, `hour(s) -> h`, `day(s) -> d`.

If the resulting prompt is empty, show usage
`/rep [until] [interval] <prompt>` and stop.

Examples:

- `5m /review-prs` -> interval `5m`, prompt `/review-prs`.
- `until /wish polish the entire UI` -> `until: true`, no interval,
  prompt `/wish polish the entire UI`.
- `5m until /wish polish the entire UI` -> interval `5m`, `until: true`,
  prompt `/wish polish the entire UI`.
- `check the deploy every 20m` -> interval `20m`, prompt `check the deploy`.
- `run tests every 5 minutes` -> interval `5m`, prompt `run tests`.
- `check the deploy` -> no interval, dynamic mode, prompt `check the deploy`.
- `check every PR` -> no interval, dynamic mode, prompt `check every PR`.
- `5m` -> empty prompt; show usage.

## `until` Semantics

`until` makes `/rep` stop-aware. It means: run the prompt now, then repeat
only while the prompt's own goal or observable condition is still unfinished.

Before scheduling a next run:

1. Decide whether the prompt reached a terminal state.
2. If terminal, do not call `/chron`, `ScheduleWakeup`, or any other
   recurrence tool.
3. If non-terminal and another run has a clear purpose, schedule the next run.
4. If `until` was specified but no stop condition can be inferred, run the
   prompt once, explain the missing stop condition, and do not arm a loop.

For slash skills, use the invoked skill's own terminal states. In particular,
for `/rep until /wish X`:

- Invoke `/wish X` once.
- Treat the `/wish` contract, native goal, or task file from that first run as
  the state of this `/rep` loop.
- On later wakeups, resume/check that same `/wish` state. Do not start a fresh
  independent `/wish X`.
- Stop without reissuing when `/wish` reports `DONE`, `ILL-POSED`, `BLOCKED`,
  `GATED`, `STUCK`, or an equivalent terminal condition. `DONE` is the normal
  success case; the others are stops because blind repetition would only spin.

## Fixed-Interval Mode

Use this mode when parsing found an interval by the leading token or trailing
`every` clause.

Convert the interval to a cron expression for `/chron`:

| Interval pattern | Cron expression | Notes |
| --- | --- | --- |
| `Nm` where `N <= 59` | `*/N * * * *` | Every `N` minutes |
| `Nm` where `N >= 60` | `0 */H * * *` | Round to hours; `H = N/60` and must divide 24 |
| `Nh` where `N <= 23` | `0 */N * * *` | Every `N` hours |
| `Nd` | `0 0 */N * *` | Every `N` days at midnight local |
| `Ns` | Treat as `ceil(N/60)m` | Cron minimum granularity is 1 minute |

A clean cron interval is one whose cadence reaches the boundary evenly:
minutes divide 60; hours divide 24; seconds first round up to whole minutes;
days use the `Nd` form as-is. If the interval is not clean, pick the nearest
clean cadence, preferring the longer interval on a tie so the loop does not
poll more often than requested. Tell the user what you rounded to before
scheduling. Examples: `7m` rounds to `6m`; `90m` rounds to `2h`.

Then:

1. If `until` is set, execute the parsed prompt now before arming recurrence.
   Apply `until` semantics; if the run reached a terminal state, stop without
   calling `/chron` or `ScheduleWakeup`.
2. If `/chron` is available, invoke it directly. Pass the cron expression,
   the parsed prompt verbatim, `recurring: true`, and the `until` flag/stop
   condition if `/chron` supports it. Do not call `CronCreate` directly from
   `/rep`; `/chron` owns the future runner and chrontab store.
3. If `/chron` is not available but `ScheduleWakeup` is available, use
   `ScheduleWakeup` instead with the fixed interval as the next delay and
   prompt `/rep <original input>`.
4. Briefly confirm what is armed: the parsed prompt, cadence, cron expression
   when applicable, and any job or wakeup ID returned by the tool. Do not claim
   cancellation commands, storage paths, or auto-expiry behavior unless the
   tool actually returned or documented them.
5. If `until` is not set, immediately execute the parsed prompt now. If it is
   a slash command, invoke it via the runtime's Skill tool when available;
   otherwise load/use the corresponding skill normally. If it is not a slash
   command, act on it directly.

## Dynamic Mode

Use this mode when parsing found no interval.

The user wants `/rep` to self-pace. Decide what makes the next iteration
worth running: a passage of time, an observable event, or a stateful goal that
is not done.

1. Run the parsed prompt now. If it is a slash command, invoke it via the
   runtime's Skill tool when available; otherwise load/use the corresponding
   skill normally. If it is not a slash command, act on it directly.
2. Apply `until` semantics. If the prompt is terminal, stop and do not arm a
   wakeup.
3. If the next run is gated on an event (CI finishing, a log line matching, a
   file changing, a PR comment) and Monitor/TaskList tools are available, call
   `TaskList` first and arm one persistent Monitor only if no matching monitor
   is already running. Its events should wake this loop immediately.
4. At the end of the turn, if `ScheduleWakeup` is available and the loop is
   still non-terminal, call it with:
   - `delaySeconds`: with a Monitor armed this is the fallback heartbeat,
     normally 1200-1800 seconds. Without a Monitor this is the cadence; pick
     based on what you observed and the tool's cache-aware guidance.
   - `reason`: one short sentence explaining the delay.
   - `prompt`: the full original `/rep` input verbatim, prefixed with
     `/rep `. Example: if the user typed `/rep check the deploy`, pass
     `/rep check the deploy`.
5. If woken by a task notification rather than a user prompt, handle the event
   in the loop's context. Then call `ScheduleWakeup` again with the same
   prompt and the same 1200-1800 second fallback delay if the loop remains
   non-terminal.
6. To stop the loop, omit `ScheduleWakeup` and stop any Monitor this loop
   armed. Use `TaskList` to find the task ID if it is no longer in context.
7. Briefly confirm: that `/rep` is self-pacing, whether a Monitor is the
   primary wake signal, that the task ran now, and what fallback delay was
   picked. If no wakeup/scheduling tool exists, say the task ran once and no
   loop was armed.
