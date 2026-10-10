# Training-efficiency vocabulary

| term | definition | topic / refs |
|---|---|---|
| fixed-batch synchronous rollout | Finish the selected response batch under one policy version before updating it; stronger than merely generating each consumed response under a current policy. | [Seer verdict](survey.md#seers-year-later-verdict) |
| rollout throughput | Generated output tokens per unit rollout time; excludes other training phases unless explicitly stated. | [Seer](concepts/seer.md) |
| time to quality | Total elapsed time to a specified held-out quality target, including all work needed to reach it. | [comparison boundaries](survey.md#baseline-sensitivity) |
