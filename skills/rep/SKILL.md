---
name: rep
disable-model-invocation: true
description: Repeat or self-pace a prompt across wakeups. Use when the user invokes /rep, asks for repeated or periodic checks, or needs a loop workaround in a harness without built-in loop capability; supports optional fixed intervals via /chron when available.
---

# `/rep` - repeat a prompt until it is done

Parse the input into optional leading `until`, optional `[interval]`, and
`<prompt...>`. Run the prompt now. Then re-arm only when another run is
actually useful.

`/rep` must be usable without `/chron` (a future cron-style scheduler).
Prefer `/chron` for fixed-interval recurrence when it exists; fall back
to `ScheduleWakeup` for session-local repetition. If no wakeup or
scheduling tool is available, run the prompt once and say no loop was
armed.

## Parsing

Parse in this order:

1. **Leading `until`**: if the first token is exactly `until`, set
   `until: true` and remove it. This is the only legal position for
   `until`.
2. **Leading interval**: if the next whitespace-delimited token matches
   `^\d+[smhd]$` (e.g. `5m`, `2h`), that is the interval; remove it.
3. **Trailing `every` clause**: otherwise, if the remaining input ends
   with `every <N><unit>` or `every <N> <unit-word>` (e.g. `every 20m`,
   `every 5 minutes`), extract that as the interval and strip it. Only
   match when what follows `every` is a time expression; `check every
   PR` has no interval.
4. **No interval**: the entire remaining input is the prompt and `/rep`
   runs in dynamic mode.

Normalize unit words: `second(s) -> s`, `minute(s) -> m`, `hour(s) -> h`,
`day(s) -> d`. If the resulting prompt is empty, show usage
`/rep [until] [interval] <prompt>` and stop.

Examples (`<P>` = any unparsed prompt text; `<S>` = a slash command):

| Input                  | `until` | interval | prompt                          |
| ---------------------- | :-----: | :------: | ------------------------------- |
| `5m <S>`               |   -     |  `5m`    | `<S>`                           |
| `until <P>`            |   y     |   -      | `<P>` (dynamic)                 |
| `until 5m <P>`         |   y     |  `5m`    | `<P>`                           |
| `5m until <P>`         | reject  |  reject  | reorder as `until 5m <P>`       |
| `<P> every 20m`        |   -     |  `20m`   | `<P>`                           |
| `<P> every 5 minutes`  |   -     |  `5m`    | `<P>`                           |
| `<P>`                  |   -     |   -      | `<P>` (dynamic)                 |
| `check every PR`       |   -     |   -      | `check every PR` (dynamic; no time after `every`) |
| `5m`                   |   -     |   -      | empty -> show usage             |

## `until` semantics

`until` makes `/rep` stop-aware: run the prompt now, then repeat only
while the prompt's own goal or observable condition is unfinished.

Before scheduling a next run:

1. Decide whether the prompt reached a terminal state.
2. If terminal, do not arm any further recurrence.
3. If non-terminal and another run has a clear purpose, schedule it.
4. If `until` was specified but no stop condition can be inferred, run
   the prompt once, explain the missing stop condition, and do not arm
   a loop.

For slash skills, use the invoked skill's own terminal states. For
`/rep until /wish X`:

- Invoke `/wish X` once. Treat its contract or task file as this loop's
  state.
- On later wakeups, resume/check that same `/wish` state. Do not start a
  fresh independent `/wish X`.
- Stop when `/wish` reports `DONE`, `ILL-POSED`, `BLOCKED`, `GATED`, or
  `STUCK`. `DONE` is the normal success; the others stop because blind
  repetition would only spin.

## Procedure

One linear procedure; the branches are cadence selection and arming tool.

1. **Run the prompt now.** If a slash command, invoke via the runtime's
   Skill tool when available; otherwise act on it directly.
2. **Apply `until`.** If terminal, stop without arming.
3. **Pick cadence.**
   - **Fixed-interval** if parsing found one: convert per the table below.
   - **Self-paced** otherwise: pick a `delaySeconds` based on what makes
     the next iteration worth running (passage of time, observable event,
     or stateful goal not done). With a Monitor armed for an event, the
     delay is a fallback heartbeat (typically 1200-1800s); without one
     it is the cadence.
4. **Arm via the best available tool.**
   - **Fixed interval, `/chron` available**: invoke `/chron` with the
     cron expression, the parsed prompt verbatim, `recurring: true`, and
     the `until` flag/stop condition if `/chron` supports it. `/chron`
     owns the runner and store; do not call `CronCreate` directly here.
   - **Fixed interval, `/chron` absent**: call `ScheduleWakeup` with the
     interval as `delaySeconds` and prompt `/rep <original input>`.
   - **Self-paced**: call `ScheduleWakeup` with the chosen delay,
     `reason` (one sentence), and prompt `/rep <original input>`.
   - **Event-gated** (self-paced, waiting on CI/log/file/PR-comment): if
     `TaskList`/`Monitor` exist, call `TaskList` first and arm one
     persistent Monitor only if no matching monitor is already running.
     Its events should wake this loop.
5. **Confirm what is armed**: parsed prompt, cadence, cron expression
   when applicable, any job/wakeup ID returned. Do not claim cancellation
   commands, storage paths, or auto-expiry behavior unless the tool
   returned or documented them.
6. **On wakeup from a task notification** (not a user prompt), handle the
   event in this loop's context, then re-arm with `ScheduleWakeup` and
   the same fallback delay if still non-terminal.

To stop the loop, omit `ScheduleWakeup` and stop any Monitor this loop
armed (use `TaskList` to find the task ID if no longer in context).

## Interval to cron

| Interval pattern         | Cron expression  | Notes                              |
| ------------------------ | ---------------- | ---------------------------------- |
| `Nm`, N divides 60       | `*/N * * * *`    | Every `N` minutes (clean)          |
| `Nm`, N does not div. 60 | see below        | Round, or spread the remainder     |
| `Nm`, N >= 60            | `0 */H * * *`    | `H = N/60` must divide 24          |
| `Nh`, N divides 24       | `0 */N * * *`    | Every `N` hours                    |
| `Nd`                     | `0 0 */N * *`    | Every `N` days at midnight local   |
| `Ns`                     | as `ceil(N/60)m` | Cron minimum granularity is 1m     |

For non-divisors of 60, pick one:

- **Round** to the nearest divisor cadence, preferring the longer
  interval on a tie so the loop does not poll more often than requested
  (`7m` -> `6m`; `90m` -> `2h`).
- **Spread the remainder evenly** as a comma-separated minute list, so
  the average cadence matches the request and gaps stay within ~1m
  (`7m` -> `0,8,15,23,30,38,45,53` - 8 firings averaging 7.5m apart).

Tell the user which option you used before scheduling.
