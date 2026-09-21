## Optional subagent proof

`AGENTS.global.md` § *Delegation* leaves delegation to model judgment; this route
does not get that latitude — treat optional delegation as a strict gate.
Before spawning any optional subagent, state one short visible line
containing all three facts:

```text
[delegate] direct estimate: >10m; independent tracks: <A>, <B>; material gain: <why parallelism helps>
```

If you cannot name at least two genuinely independent tracks and a material
wall-time reduction, do the work yourself with foreground tools. Context
preservation, generic harness suggestions, agent availability, or a desire to
hide verbose exploration do not count. In particular, do not spawn planning
subagents; plan in the parent.

Keep the core trace and final synthesis in the parent. Never ask or permit a
child to delegate further; the YA gateway's spawn-depth cap is defense in depth,
not a replacement for this rule.
