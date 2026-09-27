# Domain-adaptive retrieval vocabulary

| Term | Meaning in this survey | Reference |
|---|---|---|
| E5–FAISS baseline | The user's frozen multilingual E5-base representation with a FAISS index; exact search is an evaluation reference, while the historical lookup implementation uses HNSW | [Baseline](survey.md#start-from-multilingual-e5-base-and-faiss) |
| candidate recall | Coverage of useful items by the rough retrieval pool; agreement with E5-base's neighbors is a separate compatibility measure, not relevance ground truth | [Index losses](survey.md#index-technology-and-the-cost-of-a-coarse-stage) |
| episodic adaptation | A model update for one input or bounded episode, followed by resetting parameters and optimizer state | [Retrieved updates](concepts/retrieved-test-time-training.md) |
| retention anchor | General examples, frozen outputs, coordinates or parameter priors used to constrain drift; evaluation anchors must be disjoint from training anchors | [Forgetting controls](concepts/forgetting-controls.md) |
| index compatibility | Whether new query vectors still score correctly against the stored old document vectors, beyond good scores when both sides are newly encoded | [Adapted objects](survey.md#three-different-things-can-adapt) |
