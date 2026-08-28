# Browser event tracing and race detection

> Read-backed digest (cluster D, trust `single-source`).

**Paper.** Raychev, Vechev, and Sridharan, “Effective Race Detection for
Event-Driven Programs,” OOPSLA 2013
([PDF](https://files.sri.inf.ethz.ch/website/papers/oopsla13-web.pdf),
[local extract](../related-work/extract/raychev2013-eventracer/raychev2013-eventracer.md)).

## Mechanism

EventRacer instruments WebKit to collect browser event traces, constructs a
happens-before relation, reports event races, and applies filters and race
coverage to reduce duplicates and prioritize likely harmful conflicts. It
targets handlers, asynchronous callbacks, and browser-generated events in real
web applications.

## Evidence

The evaluation analyzes 21 Fortune 100 sites and reports 75 harmful races. It
demonstrates that browser event execution can be instrumented and analyzed at
real-site scale without treating the browser as an opaque endpoint.

## Decision edge and limits

EventRacer is adjacent evidence for browser-side boundary coverage and explicit
ordering semantics. It observes races rather than injecting component-local
delay or throughput limits, and it does not measure server-to-render
performance or recovery. It therefore narrows but does not fill the proposed
full-stack degradation-injection gap.
