# Fine-grained fail-slow points

> Read-backed digest (cluster B, trust `single-source`).

**Paper.** Dong et al., “Understanding and Detecting Fail-Slow Hardware
Failure Bugs in Cloud Systems,” USENIX ATC 2025
([PDF](https://www.usenix.org/system/files/atc25-dong.pdf),
[local extract](../related-work/extract/dong2025-sieve/dong2025-sieve.md)).

## Mechanism

The authors study 48 real fail-slow hardware-failure bugs and identify
synchronized I/O and timeout-protected I/O as particularly vulnerable points.
Sieve uses static analysis to locate those points, instruments them, groups
equivalent points by basic block, and explores call-stack/thread contexts. A
test delays one point at a time: synchronized I/O receives a long delay, while
timeout-protected I/O is delayed beyond its configured timeout.

## Evidence

Sieve reproduced 34 of the 48 study bugs and found six previously unknown bugs,
two confirmed by developers. Compared with random point selection and prior
tools, the targeted point classes reduce low-value experiments.

## Decision edge and limits

The paper substantially preempts novelty in fine-grained internal delay
injection and supplies a practical point-selection prior: queues,
synchronization, and timeout edges first. It focuses on bug reproduction rather
than a continuous performance/recovery surface. Multiple simultaneous faults,
silent failures without a checker, and some FIFO-queue behaviors remain limits.
