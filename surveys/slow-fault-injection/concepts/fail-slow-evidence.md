# Production fail-slow evidence

> Read-backed digest (cluster A, trust `single-source` for the incident corpus).

**Paper.** Gunawi et al., “Fail-Slow at Scale: Evidence of Hardware
Performance Faults in Large Production Systems,” FAST 2018
([USENIX PDF](https://www.usenix.org/system/files/conference/fast18/fast18-gunawi.pdf),
[local extract](../related-work/extract/gunawi2018-fail-slow/gunawi2018-fail-slow.md)).

## Evidence

The paper synthesizes 101 fail-slow hardware incidents reported by 12
institutions. The cases span storage, network, CPU, and memory and include
permanent slowdown, transient slowdown, partial slowdown, and transient stops.
Faults can convert across layers—for example, underlying hardware degradation
appearing as software timeout, retry, or overload—and can cascade beyond the
initial device.

The paper argues that conventional fail-stop detection and component-local
monitoring are insufficient. It recommends full-stack monitoring and explicit
fail-slow fault injection because a device that still answers can evade a
binary health test while consuming shared queues and deadlines.

## Decision edge and limits

This is strong empirical motivation for graded delay/throughput/error knobs and
cross-layer observation. It does not give a probability distribution for YA's
faults, a standard injection API, or a quantitative sensitivity-search method;
the incident corpus is qualitative and hardware-centered.
