# Length-aware batching vocabulary

| term | definition | topic / refs |
|---|---|---|
| accounting epoch | A reporting or generator budget boundary that pending physical-batch occurrences may cross; distinct from consuming every item of one pass. | [carry policy](survey.md#carry-leftovers-across-accounting-epochs) |
| draw occurrence | One selection of a row; repeated selections of the same row remain distinct objects during packing. | [weighted draws](survey.md#weighted-draws-and-physical-packing) |
| logical step | All physical batches contributing to one optimizer update. | [step composition](survey.md#logical-steps-without-independently-drawing-their-rows-first) |
| repeat gap | Distance between occurrences of the same row, with draw-position versus step-presence units specified. | [intervals](survey.md#repeat-intervals-and-count-variance) |
