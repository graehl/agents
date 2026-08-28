# JavaScript async delay injection

> Read-backed digest (cluster D, trust `single-source`).

**Paper.** Endo and Møller, “Event Race Detection for Node.js Using Delay
Injections,” ECOOP 2025
([PDF](https://users-cs.au.dk/~amoeller/papers/nacd/paper.pdf),
[local extract](../related-work/extract/endo2025-nacd/endo2025-nacd.md)).

## Mechanism

NACD dynamically instruments Node core asynchronous APIs using JavaScript
`Proxy` and `Reflect` over a model of 46 async classes and 424 properties. It
randomly delays async functions, callbacks, and promises by 0–500 ms before or
after execution, while preserving the order of connected callbacks. Runs are
checked for known event-race failures.

## Evidence

Across 23 bug benchmarks, NACD has the best reproduction ratio in 78% of cases
and takes 2.5 runs on average to expose a first failure. The result shows that
broad dynamic delay injection can be practical in a JavaScript runtime without
hand-annotating every application callback.

## Decision edge and limits

NACD directly preempts broad claims that JavaScript async delay injection is
new. It is server-side Node correctness testing, excludes timers and async
facilities absent from its model, and treats client-side JavaScript as future
work. It does not map graded performance, recovery, or a server-to-browser
path. YA should preserve normal ordering by default as NACD does, and make
reordering an explicit separate fault.
