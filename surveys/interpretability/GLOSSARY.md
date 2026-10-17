# Interpretability vocabulary

| term | definition | topic / refs |
|---|---|---|
| activation patching | Replace part of one forward pass's internal state with values from a specified donor pass; conclusions depend on the input contrast and intervention. | [evidence](survey.md#what-different-evidence-can-establish) |
| causal abstraction | A higher-level computation whose counterfactual variable changes are matched by interventions on a lower-level model. | [intervention validity](concepts/intervention-validity.md) |
| circuit | Components and connections proposed to implement a behavior, with a specified input and intervention regime. | [evidence](survey.md#what-different-evidence-can-establish) |
| distributed representation | One represented property spans multiple coordinates; this alone does not establish superposition. | [units](survey.md#the-unit-of-interpretation-changes-the-question) |
| feature | A proposed interpretable variable; it need not coincide with one native neuron or one linear direction. | [units](survey.md#the-unit-of-interpretation-changes-the-question) |
| monosemanticity | Approximate alignment with one meaning under a stated scope and granularity; a readable label does not certify exclusive function. | [native neurons](concepts/native-neurons.md) |
| neuron | A native hidden MLP coordinate, distinguished from a residual-stream coordinate or learned SAE feature. | [units](survey.md#the-unit-of-interpretation-changes-the-question) |
| polysemanticity | A component responds to multiple apparent meanings; whether they are unrelated can depend on context, measurement, and explanatory granularity. | [Goodfire](survey.md#goodfires-claim-and-the-examples-that-motivated-this-survey) |
| sign regime | One of the four gate/value sign combinations producing a SwiGLU activation. | [sign regimes](concepts/sign-regimes.md) |
| sparse autoencoder, SAE | A learned sparse code and decoder trained to reconstruct model activations; its coordinates are candidate features. | [SAEs](../llm-intelligence/concepts/sae.md) |
| steering | An intervention designed to change model behavior, often by adding or clamping an internal activation. Control success alone does not establish an exhaustive semantic interpretation. | [evidence](survey.md#what-different-evidence-can-establish) |
| superposition | Representation of more recoverable feature directions than ambient dimensions, typically exploiting sparse activity and tolerating interference. | [units](survey.md#the-unit-of-interpretation-changes-the-question) |
| transcoder | A learned replacement predicting a network computation's output from its input, rather than merely reconstructing the input activation. | [circuits](../llm-intelligence/concepts/attribution-graphs.md) |
