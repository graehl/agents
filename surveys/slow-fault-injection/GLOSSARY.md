| term | definition | topic / refs |
|---|---|---|
| degradation injection | Controlled reduction of a named boundary's service quality—delay, throughput, I/O success, or worker availability—while preserving enough scenario and phase state to measure propagation and recovery | [survey](survey.md) |
| fail-slow fault | A component remains partly functional but responds more slowly or intermittently, so timeout/failover mechanisms may not classify it as failed | [production evidence](concepts/fail-slow-evidence.md) |
| goodput | Useful completed work per unit time, excluding attempts, retries, obsolete work, and failed responses | [slow-fault sensitivity](concepts/slow-fault-sensitivity.md) |
| limplock | Cluster-wide progress collapse caused by one or more components continuing to operate in a degraded or “limping” state | [survey](survey.md) |
| metastable failure | A failure state that persists after its original trigger is removed because internal feedback keeps the system outside its stable operating region | [metastable recovery](concepts/metastable-recovery.md) |
| perturbation point | A named boundary where a test can alter timing, capacity, error, or crash behavior while recording the local and downstream effects | [survey](survey.md) |
| recovery transient | The interval after injection stops while queues, caches, retries, resource pressure, and user-visible service return—or fail to return—to a stated healthy condition | [metastable recovery](concepts/metastable-recovery.md) |
| slow fault | A fault expressed as degraded latency, throughput, or intermittent progress rather than a clean stop | [survey](survey.md) |
