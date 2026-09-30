**Source:** *PyTorch Datasets* — [original page](https://lhotse.readthedocs.io/en/latest/datasets.html)

[ lhotse ](https://lhotse.readthedocs.io/en/latest/index.html)

Contents:

  * [Getting started](https://lhotse.readthedocs.io/en/latest/getting-started.html)
  * [Representing a corpus](https://lhotse.readthedocs.io/en/latest/corpus.html)
  * [Cuts](https://lhotse.readthedocs.io/en/latest/cuts.html)
  * [Feature extraction](https://lhotse.readthedocs.io/en/latest/features.html)
  * [Executing tasks in parallel](https://lhotse.readthedocs.io/en/latest/parallelism.html)
  * [PyTorch Datasets](https://lhotse.readthedocs.io/en/latest/datasets.html)
    * [A quick re-cap of PyTorch’s data API](https://lhotse.readthedocs.io/en/latest/datasets.html#a-quick-re-cap-of-pytorchs-data-api)
    * [About Lhotse’s Datasets and Samplers](https://lhotse.readthedocs.io/en/latest/datasets.html#about-lhotses-datasets-and-samplers)
    * [Restoring sampler’s state: continuing the training](https://lhotse.readthedocs.io/en/latest/datasets.html#restoring-sampler-s-state-continuing-the-training)
    * [Resumable Stateful Dataloading (Indexed)](https://lhotse.readthedocs.io/en/latest/datasets.html#resumable-stateful-dataloading-indexed)
      * [Quick start](https://lhotse.readthedocs.io/en/latest/datasets.html#quick-start)
      * [Using StatefulDataLoader for checkpointing](https://lhotse.readthedocs.io/en/latest/datasets.html#using-statefuldataloader-for-checkpointing)
      * [Requirements and limitations](https://lhotse.readthedocs.io/en/latest/datasets.html#requirements-and-limitations)
      * [Background-thread bucket fetching and clean shutdown](https://lhotse.readthedocs.io/en/latest/datasets.html#background-thread-bucket-fetching-and-clean-shutdown)
      * [Implementing custom iterators](https://lhotse.readthedocs.io/en/latest/datasets.html#implementing-custom-iterators)
      * [Stateful batch transforms](https://lhotse.readthedocs.io/en/latest/datasets.html#stateful-batch-transforms)
    * [Batch I/O: pre-computed vs. on-the-fly features](https://lhotse.readthedocs.io/en/latest/datasets.html#batch-i-o-pre-computed-vs-on-the-fly-features)
      * [Which strategy to choose?](https://lhotse.readthedocs.io/en/latest/datasets.html#which-strategy-to-choose)
    * [Handling random seeds](https://lhotse.readthedocs.io/en/latest/datasets.html#handling-random-seeds)
    * [Customizing sampling constraints](https://lhotse.readthedocs.io/en/latest/datasets.html#customizing-sampling-constraints)
      * [`SamplingConstraint`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint)
        * [`SamplingConstraint.add()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint.add)
        * [`SamplingConstraint.exceeded()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint.exceeded)
        * [`SamplingConstraint.close_to_exceeding()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint.close_to_exceeding)
        * [`SamplingConstraint.reset()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint.reset)
        * [`SamplingConstraint.measure_length()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint.measure_length)
        * [`SamplingConstraint.select_bucket()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint.select_bucket)
        * [`SamplingConstraint.copy()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint.copy)
      * [Sampling non-audio data](https://lhotse.readthedocs.io/en/latest/datasets.html#sampling-non-audio-data)
        * [`TextExample`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.cut.text.TextExample)
        * [`TextPairExample`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.cut.text.TextPairExample)
        * [`LazyTxtIterator`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.lazy.LazyTxtIterator)
        * [`TokenConstraint`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.TokenConstraint)
    * [Dataset’s list](https://lhotse.readthedocs.io/en/latest/datasets.html#module-lhotse.dataset.diarization)
      * [`DiarizationDataset`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.diarization.DiarizationDataset)
        * [`DiarizationDataset.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.diarization.DiarizationDataset.__init__)
      * [`UnsupervisedDataset`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.UnsupervisedDataset)
        * [`UnsupervisedDataset.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.UnsupervisedDataset.__init__)
      * [`UnsupervisedWaveformDataset`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.UnsupervisedWaveformDataset)
        * [`UnsupervisedWaveformDataset.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.UnsupervisedWaveformDataset.__init__)
      * [`DynamicUnsupervisedDataset`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.DynamicUnsupervisedDataset)
        * [`DynamicUnsupervisedDataset.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.DynamicUnsupervisedDataset.__init__)
      * [`RecordingChunkIterableDataset`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.RecordingChunkIterableDataset)
        * [`RecordingChunkIterableDataset.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.RecordingChunkIterableDataset.__init__)
        * [`RecordingChunkIterableDataset.validate()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.RecordingChunkIterableDataset.validate)
      * [`audio_chunk_collate()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.audio_chunk_collate)
      * [`audio_chunk_worker_init_fn()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.audio_chunk_worker_init_fn)
      * [`K2SpeechRecognitionDataset`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.speech_recognition.K2SpeechRecognitionDataset)
        * [`K2SpeechRecognitionDataset.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.speech_recognition.K2SpeechRecognitionDataset.__init__)
      * [`validate_for_asr()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.speech_recognition.validate_for_asr)
      * [`speech_synthesis`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.speech_synthesis)
      * [`DynamicallyMixedSourceSeparationDataset`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.source_separation.DynamicallyMixedSourceSeparationDataset)
        * [`DynamicallyMixedSourceSeparationDataset.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.source_separation.DynamicallyMixedSourceSeparationDataset.__init__)
        * [`DynamicallyMixedSourceSeparationDataset.validate()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.source_separation.DynamicallyMixedSourceSeparationDataset.validate)
      * [`PreMixedSourceSeparationDataset`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.source_separation.PreMixedSourceSeparationDataset)
        * [`PreMixedSourceSeparationDataset.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.source_separation.PreMixedSourceSeparationDataset.__init__)
      * [`VadDataset`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.vad.VadDataset)
        * [`VadDataset.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.vad.VadDataset.__init__)
    * [Sampler’s list](https://lhotse.readthedocs.io/en/latest/datasets.html#module-lhotse.dataset.sampling)
      * [`TokenConstraint`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint)
        * [`TokenConstraint.max_tokens`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.max_tokens)
        * [`TokenConstraint.max_examples`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.max_examples)
        * [`TokenConstraint.current`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.current)
        * [`TokenConstraint.num_examples`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.num_examples)
        * [`TokenConstraint.longest_seen`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.longest_seen)
        * [`TokenConstraint.quadratic_length`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.quadratic_length)
        * [`TokenConstraint.add()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.add)
        * [`TokenConstraint.exceeded()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.exceeded)
        * [`TokenConstraint.close_to_exceeding()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.close_to_exceeding)
        * [`TokenConstraint.reset()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.reset)
        * [`TokenConstraint.measure_length()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.measure_length)
        * [`TokenConstraint.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.__init__)
      * [`TimeConstraint`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint)
        * [`TimeConstraint.max_duration`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.max_duration)
        * [`TimeConstraint.max_cuts`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.max_cuts)
        * [`TimeConstraint.current`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.current)
        * [`TimeConstraint.num_cuts`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.num_cuts)
        * [`TimeConstraint.longest_seen`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.longest_seen)
        * [`TimeConstraint.quadratic_duration`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.quadratic_duration)
        * [`TimeConstraint.concatenate_cuts`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.concatenate_cuts)
        * [`TimeConstraint.is_active()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.is_active)
        * [`TimeConstraint.add()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.add)
        * [`TimeConstraint.exceeded()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.exceeded)
        * [`TimeConstraint.close_to_exceeding()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.close_to_exceeding)
        * [`TimeConstraint.reset()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.reset)
        * [`TimeConstraint.measure_length()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.measure_length)
        * [`TimeConstraint.state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.state_dict)
        * [`TimeConstraint.load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.load_state_dict)
        * [`TimeConstraint.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.__init__)
      * [`SamplingDiagnostics`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics)
        * [`SamplingDiagnostics.current_epoch`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.current_epoch)
        * [`SamplingDiagnostics.stats_per_epoch`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.stats_per_epoch)
        * [`SamplingDiagnostics.reset_current_epoch()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.reset_current_epoch)
        * [`SamplingDiagnostics.set_epoch()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.set_epoch)
        * [`SamplingDiagnostics.advance_epoch()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.advance_epoch)
        * [`SamplingDiagnostics.current_epoch_stats`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.current_epoch_stats)
        * [`SamplingDiagnostics.keep()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.keep)
        * [`SamplingDiagnostics.discard()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.discard)
        * [`SamplingDiagnostics.discard_single()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.discard_single)
        * [`SamplingDiagnostics.kept_cuts`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.kept_cuts)
        * [`SamplingDiagnostics.discarded_cuts`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.discarded_cuts)
        * [`SamplingDiagnostics.kept_batches`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.kept_batches)
        * [`SamplingDiagnostics.discarded_batches`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.discarded_batches)
        * [`SamplingDiagnostics.total_cuts`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.total_cuts)
        * [`SamplingDiagnostics.total_batches`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.total_batches)
        * [`SamplingDiagnostics.get_report()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.get_report)
        * [`SamplingDiagnostics.state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.state_dict)
        * [`SamplingDiagnostics.load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.load_state_dict)
        * [`SamplingDiagnostics.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.__init__)
      * [`SamplingConstraint`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingConstraint)
        * [`SamplingConstraint.add()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingConstraint.add)
        * [`SamplingConstraint.exceeded()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingConstraint.exceeded)
        * [`SamplingConstraint.close_to_exceeding()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingConstraint.close_to_exceeding)
        * [`SamplingConstraint.reset()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingConstraint.reset)
        * [`SamplingConstraint.measure_length()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingConstraint.measure_length)
        * [`SamplingConstraint.select_bucket()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingConstraint.select_bucket)
        * [`SamplingConstraint.copy()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingConstraint.copy)
      * [`BucketingSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler)
        * [`BucketingSampler.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.__init__)
        * [`BucketingSampler.remaining_duration`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.remaining_duration)
        * [`BucketingSampler.remaining_cuts`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.remaining_cuts)
        * [`BucketingSampler.num_cuts`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.num_cuts)
        * [`BucketingSampler.set_epoch()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.set_epoch)
        * [`BucketingSampler.filter()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.filter)
        * [`BucketingSampler.allow_iter_to_reset_state()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.allow_iter_to_reset_state)
        * [`BucketingSampler.state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.state_dict)
        * [`BucketingSampler.load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.load_state_dict)
        * [`BucketingSampler.is_depleted`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.is_depleted)
        * [`BucketingSampler.diagnostics`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.diagnostics)
        * [`BucketingSampler.get_report()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.get_report)
      * [`CutPairsSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.CutPairsSampler)
        * [`CutPairsSampler.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.CutPairsSampler.__init__)
        * [`CutPairsSampler.remaining_duration`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.CutPairsSampler.remaining_duration)
        * [`CutPairsSampler.remaining_cuts`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.CutPairsSampler.remaining_cuts)
        * [`CutPairsSampler.num_cuts`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.CutPairsSampler.num_cuts)
        * [`CutPairsSampler.state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.CutPairsSampler.state_dict)
        * [`CutPairsSampler.load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.CutPairsSampler.load_state_dict)
      * [`DynamicCutSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicCutSampler)
        * [`DynamicCutSampler.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicCutSampler.__init__)
        * [`DynamicCutSampler.state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicCutSampler.state_dict)
        * [`DynamicCutSampler.load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicCutSampler.load_state_dict)
        * [`DynamicCutSampler.remaining_duration`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicCutSampler.remaining_duration)
        * [`DynamicCutSampler.remaining_cuts`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicCutSampler.remaining_cuts)
        * [`DynamicCutSampler.num_cuts`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicCutSampler.num_cuts)
      * [`DynamicBucketingSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicBucketingSampler)
        * [`DynamicBucketingSampler.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicBucketingSampler.__init__)
        * [`DynamicBucketingSampler.state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicBucketingSampler.state_dict)
        * [`DynamicBucketingSampler.load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicBucketingSampler.load_state_dict)
        * [`DynamicBucketingSampler.remaining_duration`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicBucketingSampler.remaining_duration)
        * [`DynamicBucketingSampler.remaining_cuts`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicBucketingSampler.remaining_cuts)
        * [`DynamicBucketingSampler.num_cuts`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicBucketingSampler.num_cuts)
      * [`RoundRobinSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler)
        * [`RoundRobinSampler.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.__init__)
        * [`RoundRobinSampler.remaining_duration`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.remaining_duration)
        * [`RoundRobinSampler.remaining_cuts`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.remaining_cuts)
        * [`RoundRobinSampler.num_cuts`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.num_cuts)
        * [`RoundRobinSampler.allow_iter_to_reset_state()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.allow_iter_to_reset_state)
        * [`RoundRobinSampler.state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.state_dict)
        * [`RoundRobinSampler.load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.load_state_dict)
        * [`RoundRobinSampler.set_epoch()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.set_epoch)
        * [`RoundRobinSampler.filter()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.filter)
        * [`RoundRobinSampler.diagnostics`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.diagnostics)
        * [`RoundRobinSampler.get_report()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.get_report)
      * [`SimpleCutSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SimpleCutSampler)
        * [`SimpleCutSampler.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SimpleCutSampler.__init__)
        * [`SimpleCutSampler.remaining_duration`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SimpleCutSampler.remaining_duration)
        * [`SimpleCutSampler.remaining_cuts`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SimpleCutSampler.remaining_cuts)
        * [`SimpleCutSampler.num_cuts`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SimpleCutSampler.num_cuts)
        * [`SimpleCutSampler.state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SimpleCutSampler.state_dict)
        * [`SimpleCutSampler.load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SimpleCutSampler.load_state_dict)
      * [`WeightedSimpleCutSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.WeightedSimpleCutSampler)
        * [`WeightedSimpleCutSampler.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.WeightedSimpleCutSampler.__init__)
        * [`WeightedSimpleCutSampler.state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.WeightedSimpleCutSampler.state_dict)
        * [`WeightedSimpleCutSampler.load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.WeightedSimpleCutSampler.load_state_dict)
      * [`StatelessSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.StatelessSampler)
        * [`StatelessSampler.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.StatelessSampler.__init__)
        * [`StatelessSampler.map()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.StatelessSampler.map)
        * [`StatelessSampler.state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.StatelessSampler.state_dict)
        * [`StatelessSampler.load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.StatelessSampler.load_state_dict)
        * [`StatelessSampler.get_report()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.StatelessSampler.get_report)
      * [`ZipSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler)
        * [`ZipSampler.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.__init__)
        * [`ZipSampler.remaining_duration`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.remaining_duration)
        * [`ZipSampler.remaining_cuts`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.remaining_cuts)
        * [`ZipSampler.num_cuts`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.num_cuts)
        * [`ZipSampler.allow_iter_to_reset_state()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.allow_iter_to_reset_state)
        * [`ZipSampler.state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.state_dict)
        * [`ZipSampler.load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.load_state_dict)
        * [`ZipSampler.set_epoch()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.set_epoch)
        * [`ZipSampler.filter()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.filter)
        * [`ZipSampler.diagnostics`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.diagnostics)
        * [`ZipSampler.get_report()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.get_report)
      * [`find_pessimistic_batches()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.find_pessimistic_batches)
      * [`report_padding_ratio_estimate()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.report_padding_ratio_estimate)
    * [Input strategies’ list](https://lhotse.readthedocs.io/en/latest/datasets.html#module-lhotse.dataset.input_strategies)
      * [`BatchIO`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.BatchIO)
        * [`BatchIO.__call__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.BatchIO.__call__)
        * [`BatchIO.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.BatchIO.__init__)
        * [`BatchIO.supervision_intervals()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.BatchIO.supervision_intervals)
        * [`BatchIO.supervision_masks()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.BatchIO.supervision_masks)
      * [`PrecomputedFeatures`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.PrecomputedFeatures)
        * [`PrecomputedFeatures.__call__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.PrecomputedFeatures.__call__)
        * [`PrecomputedFeatures.supervision_intervals()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.PrecomputedFeatures.supervision_intervals)
        * [`PrecomputedFeatures.supervision_masks()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.PrecomputedFeatures.supervision_masks)
      * [`AudioSamples`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.AudioSamples)
        * [`AudioSamples.__call__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.AudioSamples.__call__)
        * [`AudioSamples.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.AudioSamples.__init__)
        * [`AudioSamples.supervision_intervals()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.AudioSamples.supervision_intervals)
        * [`AudioSamples.supervision_masks()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.AudioSamples.supervision_masks)
      * [`OnTheFlyFeatures`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.OnTheFlyFeatures)
        * [`OnTheFlyFeatures.__call__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.OnTheFlyFeatures.__call__)
        * [`OnTheFlyFeatures.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.OnTheFlyFeatures.__init__)
        * [`OnTheFlyFeatures.supervision_intervals()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.OnTheFlyFeatures.supervision_intervals)
        * [`OnTheFlyFeatures.supervision_masks()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.OnTheFlyFeatures.supervision_masks)
    * [Augmentation - transforms on cuts](https://lhotse.readthedocs.io/en/latest/datasets.html#augmentation-transforms-on-cuts)
      * [`CutConcatenate`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.CutConcatenate)
        * [`CutConcatenate.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.CutConcatenate.__init__)
      * [`CutMix`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.CutMix)
        * [`CutMix.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.CutMix.__init__)
        * [`CutMix.state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.CutMix.state_dict)
        * [`CutMix.load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.CutMix.load_state_dict)
      * [`ExtraPadding`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ExtraPadding)
        * [`ExtraPadding.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ExtraPadding.__init__)
      * [`LowpassUsingResampling`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.LowpassUsingResampling)
        * [`LowpassUsingResampling.p`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.LowpassUsingResampling.p)
        * [`LowpassUsingResampling.frequencies_interval`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.LowpassUsingResampling.frequencies_interval)
        * [`LowpassUsingResampling.seed`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.LowpassUsingResampling.seed)
        * [`LowpassUsingResampling.rng`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.LowpassUsingResampling.rng)
        * [`LowpassUsingResampling.preserve_id`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.LowpassUsingResampling.preserve_id)
        * [`LowpassUsingResampling.state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.LowpassUsingResampling.state_dict)
        * [`LowpassUsingResampling.load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.LowpassUsingResampling.load_state_dict)
        * [`LowpassUsingResampling.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.LowpassUsingResampling.__init__)
      * [`PerturbSpeed`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbSpeed)
        * [`PerturbSpeed.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbSpeed.__init__)
        * [`PerturbSpeed.state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbSpeed.state_dict)
        * [`PerturbSpeed.load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbSpeed.load_state_dict)
      * [`PerturbTempo`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbTempo)
        * [`PerturbTempo.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbTempo.__init__)
        * [`PerturbTempo.state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbTempo.state_dict)
        * [`PerturbTempo.load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbTempo.load_state_dict)
      * [`PerturbVolume`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbVolume)
        * [`PerturbVolume.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbVolume.__init__)
        * [`PerturbVolume.state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbVolume.state_dict)
        * [`PerturbVolume.load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbVolume.load_state_dict)
      * [`ReverbWithImpulseResponse`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ReverbWithImpulseResponse)
        * [`ReverbWithImpulseResponse.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ReverbWithImpulseResponse.__init__)
        * [`ReverbWithImpulseResponse.state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ReverbWithImpulseResponse.state_dict)
        * [`ReverbWithImpulseResponse.load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ReverbWithImpulseResponse.load_state_dict)
      * [`Compress`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress)
        * [`Compress.codecs`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.codecs)
        * [`Compress.compression_level`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.compression_level)
        * [`Compress.codec_weights`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.codec_weights)
        * [`Compress.compress_custom_fields`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.compress_custom_fields)
        * [`Compress.p`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.p)
        * [`Compress.seed`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.seed)
        * [`Compress.rng`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.rng)
        * [`Compress.preserve_id`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.preserve_id)
        * [`Compress.state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.state_dict)
        * [`Compress.load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.load_state_dict)
        * [`Compress.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.__init__)
      * [`ClippingTransform`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform)
        * [`ClippingTransform.gain_db`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.gain_db)
        * [`ClippingTransform.normalize`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.normalize)
        * [`ClippingTransform.p`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.p)
        * [`ClippingTransform.p_hard`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.p_hard)
        * [`ClippingTransform.seed`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.seed)
        * [`ClippingTransform.rng`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.rng)
        * [`ClippingTransform.oversampling`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.oversampling)
        * [`ClippingTransform.preserve_id`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.preserve_id)
        * [`ClippingTransform.state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.state_dict)
        * [`ClippingTransform.load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.load_state_dict)
        * [`ClippingTransform.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.__init__)
    * [Augmentation - transforms on signals](https://lhotse.readthedocs.io/en/latest/datasets.html#augmentation-transforms-on-signals)
      * [`GlobalMVN`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.GlobalMVN)
        * [`GlobalMVN.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.GlobalMVN.__init__)
        * [`GlobalMVN.from_cuts()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.GlobalMVN.from_cuts)
        * [`GlobalMVN.from_file()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.GlobalMVN.from_file)
        * [`GlobalMVN.to_file()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.GlobalMVN.to_file)
        * [`GlobalMVN.forward()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.GlobalMVN.forward)
        * [`GlobalMVN.inverse()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.GlobalMVN.inverse)
      * [`SpecAugment`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.SpecAugment)
        * [`SpecAugment.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.SpecAugment.__init__)
        * [`SpecAugment.forward()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.SpecAugment.forward)
        * [`SpecAugment.state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.SpecAugment.state_dict)
        * [`SpecAugment.load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.SpecAugment.load_state_dict)
      * [`RandomizedSmoothing`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.RandomizedSmoothing)
        * [`RandomizedSmoothing.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.RandomizedSmoothing.__init__)
        * [`RandomizedSmoothing.forward()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.RandomizedSmoothing.forward)
      * [`DereverbWPE`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.DereverbWPE)
        * [`DereverbWPE.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.DereverbWPE.__init__)
        * [`DereverbWPE.forward()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.DereverbWPE.forward)
    * [Collation utilities for building custom Datasets](https://lhotse.readthedocs.io/en/latest/datasets.html#module-lhotse.dataset.collation)
      * [`TokenCollater`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.TokenCollater)
        * [`TokenCollater.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.TokenCollater.__init__)
        * [`TokenCollater.inverse()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.TokenCollater.inverse)
      * [`collate_features()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.collate_features)
      * [`collate_audio()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.collate_audio)
      * [`collate_multi_channel_audio()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.collate_multi_channel_audio)
      * [`collate_video()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.collate_video)
      * [`collate_custom_field()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.collate_custom_field)
      * [`collate_multi_channel_features()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.collate_multi_channel_features)
      * [`collate_vectors()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.collate_vectors)
      * [`collate_matrices()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.collate_matrices)
      * [`read_audio_from_cuts()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.read_audio_from_cuts)
      * [`read_video_from_cuts()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.read_video_from_cuts)
      * [`read_features_from_cuts()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.read_features_from_cuts)
      * [`collate_images()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.collate_images)
    * [Dataloading seeding utilities](https://lhotse.readthedocs.io/en/latest/datasets.html#module-lhotse.dataset.dataloading)
      * [`make_worker_init_fn()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.make_worker_init_fn)
      * [`worker_init_fn()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.worker_init_fn)
      * [`resolve_seed()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.resolve_seed)
      * [`get_worker_partition()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.get_worker_partition)
      * [`PartitionedIndexedIterator`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.PartitionedIndexedIterator)
        * [`PartitionedIndexedIterator.__init__()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.PartitionedIndexedIterator.__init__)
        * [`PartitionedIndexedIterator.position`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.PartitionedIndexedIterator.position)
        * [`PartitionedIndexedIterator.iterate()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.PartitionedIndexedIterator.iterate)
        * [`PartitionedIndexedIterator.state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.PartitionedIndexedIterator.state_dict)
        * [`PartitionedIndexedIterator.load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.PartitionedIndexedIterator.load_state_dict)
      * [`get_world_size()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.get_world_size)
      * [`get_rank()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.get_rank)
  * [Indexed Manifests and IteratorNodes](https://lhotse.readthedocs.io/en/latest/indexed-manifests.html)
  * [Kaldi Interoperability](https://lhotse.readthedocs.io/en/latest/kaldi.html)
  * [Command-line interface](https://lhotse.readthedocs.io/en/latest/cli.html)
  * [API Reference](https://lhotse.readthedocs.io/en/latest/api.html)



__[lhotse](https://lhotse.readthedocs.io/en/latest/index.html)

  * [](https://lhotse.readthedocs.io/en/latest/index.html)
  * PyTorch Datasets
  * [ View page source](https://lhotse.readthedocs.io/en/latest/_sources/datasets.rst.txt)



* * *

# PyTorch Datasets[](https://lhotse.readthedocs.io/en/latest/datasets.html#pytorch-datasets "Permalink to this heading")

Lhotse supports PyTorch’s dataset API, providing implementations for the `Dataset` and `Sampler` concepts. They can be used together with the standard `DataLoader` class for efficient mini-batch collection with multiple parallel readers and pre-fetching.

## A quick re-cap of PyTorch’s data API[](https://lhotse.readthedocs.io/en/latest/datasets.html#a-quick-re-cap-of-pytorchs-data-api "Permalink to this heading")

PyTorch defines the Dataset class that is responsible for reading the data from disk/memory/Internet/database/etc., and converting it to tensors that can be used for network training or inference. These `Dataset`’s are typically „map-style” datasets which are given an index (or a list of indices) and return the corresponding data samples.

The selection of indices is performed by the `Sampler` class. `Sampler`, knowing the length (number of items) in a `Dataset`, can use various strategies to determine the order of elements to read (e.g. sequential reads, or random reads).

More details about the data pipeline API in PyTorch can be found [here](https://pytorch.org/docs/stable/data.html).

## About Lhotse’s Datasets and Samplers[](https://lhotse.readthedocs.io/en/latest/datasets.html#about-lhotses-datasets-and-samplers "Permalink to this heading")

Lhotse provides a number of utilities that make it simpler to define `Dataset`’s for speech processing tasks. [`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.CutSet") is the base data structure that is used to initialize the `Dataset` class. This makes it possible to manipulate the speech data in convenient ways - pad, mix, concatenate, augment, compute features, look up the supervision information, etc.

Lhotse’s `Dataset`’s will perform batching by themselves, because auto-collation in `DataLoader` is too limiting for speech data handling. These `Dataset`’s expect to be handed lists of element indices, so that they can collate the data _before_ it is passed to the `DataLoader` (which must use `batch_size=None`). It allows for interesting collation methods - e.g. **padding the speech with noise recordings, or actual acoustic context** , rather than artificial zeroes; or **dynamic batch sizes**.

The items for mini-batch creation are selected by the `Sampler`. Lhotse defines `Sampler` classes that are initialized with [`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.CutSet")’s, so that they can look up specific properties of an utterance to stratify the sampling. For example, [`SimpleCutSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SimpleCutSampler "lhotse.dataset.sampling.SimpleCutSampler") has a defined `max_duration` attribute, and it will keep sampling cuts for a batch until they do not exceed the specified number of seconds. Another strategy — used in [`BucketingSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler "lhotse.dataset.sampling.BucketingSampler") — will first group the cuts of similar durations into buckets, and then randomly select a bucket to draw the whole batch from.

For tasks where both input and output of the model are speech utterances, we can use the [`CutPairsSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.CutPairsSampler "lhotse.dataset.sampling.CutPairsSampler"), which accepts two [`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.CutSet")’s and will match the cuts in them by their IDs.

A typical Lhotse’s dataset API usage might look like this:
    
    
    from torch.utils.data import DataLoader
    from lhotse.dataset import K2SpeechRecognitionDataset, SimpleCutSampler
    
    cuts = CutSet(...)
    dset = K2SpeechRecognitionDataset()
    sampler = SimpleCutSampler(cuts, max_duration=500)
    # Dataset performs batching by itself, so we have to indicate that
    # to the DataLoader with batch_size=None
    dloader = DataLoader(dset, sampler=sampler, batch_size=None, num_workers=1)
    for batch in dloader:
        ...  # process data
    

## Restoring sampler’s state: continuing the training[](https://lhotse.readthedocs.io/en/latest/datasets.html#restoring-sampler-s-state-continuing-the-training "Permalink to this heading")

All `CutSampler` types can save their progress and pick up from that checkpoint. For consistency with PyTorch tensors, the relevant methods are called `.state_dict()` and `.load_state_dict()`. The following example illustrates how to save the sampler’s state (pay attention to the last bit):
    
    
    dataset = ...  # Some task-specific dataset initialization
    sampler = BucketingSampler(cuts, max_duration=200, shuffle=True, num_buckets=30)
    dloader = DataLoader(dataset, batch_size=None, sampler=sampler, num_workers=4)
    global_step = 0
    for epoch in range(30):
        dloader.sampler.set_epoch(epoch)
        for batch in dloader:
            # ... processing forward, backward, etc.
            global_step += 1
    
            if global_step % 5000 == 0:
                state = dloader.sampler.state_dict()
                torch.save(state, f'sampler-ckpt-ep{epoch}-step{global_step}.pt')
    

In case that the training is ended abruptly and the epochs are very long (10k+ steps, not uncommon with large datasets these days), we can resume the training from where it left off like the following:
    
    
    # Creating a vanilla sampler, we will read the previous progress into it.
    sampler = BucketingSampler(cuts, max_duration=200, shuffle=True, num_buckets=30)
    
    # Restore the sampler's state.
    state = torch.load('sampler-ckpt-ep5-step75000.pt')
    sampler.load_state_dict(state)
    
    dloader = DataLoader(dataset, batch_size=None, sampler=sampler, num_workers=4)
    
    global_step = sampler.diagnostics.total_cuts  # <-- Restore the global step idx.
    for epoch in range(sampler.epoch, 30):  # <-- Skip previous epochs that are already processed.
    
        dloader.sampler.set_epoch(epoch)
        for batch in dloader:
            # Note: the first batch is going to be from step 75009.
            # With DataLoader num_workers==0, it would have been 75001, but we get
            # +8 because of num_workers==4 * prefetching_factor==2
    
            # ... processing forward, backward, etc.
            global_step += 1
    

Note

In general, the sampler arguments may be different – loading a `state_dict` will overwrite the arguments, and emit a warning for the user to be aware what happened. [`BucketingSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler "lhotse.dataset.sampling.BucketingSampler") is an exception – the `num_buckets` and `bucket_method` must be consistent, otherwise we couldn’t guarantee identical outcomes after training resumption.

Note

The `constraint=` argument of [`DynamicCutSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicCutSampler "lhotse.dataset.sampling.DynamicCutSampler") and [`DynamicBucketingSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicBucketingSampler "lhotse.dataset.sampling.DynamicBucketingSampler") is **not** part of `state_dict`. The constraint object (e.g. `TimeConstraint`, `TokenConstraint`, or a user-defined [`SamplingConstraint`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint "lhotse.dataset.sampling.base.SamplingConstraint")) must be reconstructed from your config when you instantiate the sampler before calling `load_state_dict`. Iteration state (RNG, bucketer, epoch, diagnostics) is what drives exact resume and is independent of the constraint object.

Note

For replay-based sampler restore with a regular `DataLoader`, the `num_workers` setting can differ after resuming. For exact per-worker restore with `StatefulDataLoader`, it must match between save and restore.

Note

Calling `set_epoch` after `load_state_dict` is safe — it is a no-op while the restored state is still pending, so it will not wipe the saved RNG, cuts, or bucketer buffers. PyTorch Lightning relies on this: its `fit_loop` calls `set_epoch` at the start of every (re)started epoch. To explicitly discard the restored progress and start the epoch fresh, call `sampler.allow_iter_to_reset_state()` instead.

Note

The approach described above relies on `_fast_forward()` which re-iterates from the start and skips N batches (O(N) time). For a faster O(1) alternative using binary index files, see the section below.

## Resumable Stateful Dataloading (Indexed)[](https://lhotse.readthedocs.io/en/latest/datasets.html#resumable-stateful-dataloading-indexed "Permalink to this heading")

Lhotse supports O(1) checkpoint/restore of the entire dataloading pipeline when binary index files are available. This eliminates the slow `_fast_forward()` re-iteration on training resumption.

Indexed checkpointing relies on iterator nodes that can reconstruct their own outputs directly from graph-local restore tokens. This is what makes exact worker-process restore possible without replaying earlier batches.

For the full guide, see [Indexed Manifests and IteratorNodes](https://lhotse.readthedocs.io/en/latest/indexed-manifests.html).

### Quick start[](https://lhotse.readthedocs.io/en/latest/datasets.html#quick-start "Permalink to this heading")

Plain manifests:
    
    
    cuts = CutSet.from_file("cuts.jsonl", indexed=True)
    

Shar:
    
    
    cuts = CutSet.from_shar(in_dir="data/", indexed=True)
    

Create indexes for existing data with:
    
    
    lhotse index jsonl /path/to/cuts.jsonl
    lhotse index tar /path/to/recording.tar
    lhotse index shar /path/to/shar_dir/
    

### Using StatefulDataLoader for checkpointing[](https://lhotse.readthedocs.io/en/latest/datasets.html#using-statefuldataloader-for-checkpointing "Permalink to this heading")

For full per-worker checkpointing with `num_workers > 0`, use `torchdata.stateful_dataloader.StatefulDataLoader` (from the `torchdata` package, `pip install torchdata`). It is a drop-in replacement for `torch.utils.data.DataLoader` that automatically collects per-worker state:
    
    
    from torchdata.stateful_dataloader import StatefulDataLoader
    from lhotse import CutSet
    from lhotse.dataset import (
        K2SpeechRecognitionDataset,
        DynamicCutSampler,
        IterableDatasetWrapper,
    )
    
    cuts = CutSet.from_shar(in_dir="data/")
    dataset = K2SpeechRecognitionDataset()
    sampler = DynamicCutSampler(cuts, max_duration=200, shuffle=True)
    iter_dset = IterableDatasetWrapper(dataset, sampler)
    
    # Use StatefulDataLoader instead of regular DataLoader
    dloader = StatefulDataLoader(iter_dset, batch_size=None, num_workers=2)
    
    # Training loop with checkpointing
    for batch in dloader:
        loss = train_step(batch)
        if should_checkpoint:
            dl_state = dloader.state_dict()
            torch.save({
                "model": model.state_dict(),
                "optimizer": optimizer.state_dict(),
                "dataloader": dl_state,
            }, "checkpoint.pt")
    
    # Resumption -- exact continuation from checkpoint
    ckpt = torch.load("checkpoint.pt")
    model.load_state_dict(ckpt["model"])
    optimizer.load_state_dict(ckpt["optimizer"])
    dloader = StatefulDataLoader(iter_dset, batch_size=None, num_workers=2)
    dloader.load_state_dict(ckpt["dataloader"])
    for batch in dloader:  # continues exactly where we left off
        train_step(batch)
    

### Requirements and limitations[](https://lhotse.readthedocs.io/en/latest/datasets.html#requirements-and-limitations "Permalink to this heading")

  * Requires `torchdata` package (`pip install torchdata`) for `StatefulDataLoader`.

  * Exact indexed restore requires **uncompressed** data files. For Shar, write it with `compress_jsonl=False`.

  * `num_workers` and `world_size` must match between save and restore.

  * Non-indexed pipelines still use replay-based restore.




### Background-thread bucket fetching and clean shutdown[](https://lhotse.readthedocs.io/en/latest/datasets.html#background-thread-bucket-fetching-and-clean-shutdown "Permalink to this heading")

When [`DynamicBucketingSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicBucketingSampler "lhotse.dataset.sampling.DynamicBucketingSampler") is constructed with `concurrent_bucketing=True` (the default), a background thread fills the bucket buffers in parallel with iteration. That thread is created as a daemon, so it never blocks interpreter shutdown — useful when combining `concurrent_bucketing=True` with `persistent_workers=True`, where lingering references from FSDP / dataloader workers can otherwise prevent the sampler’s `__del__` from running before the main process tries to exit.

If you maintain custom samplers with their own background threads, mark them `daemon=True` for the same reason.

### Implementing custom iterators[](https://lhotse.readthedocs.io/en/latest/datasets.html#implementing-custom-iterators "Permalink to this heading")

Custom lazy iterators should derive from `IteratorNode`. The complete implementation guide, including how graph tokens work and how to propagate them through composed transforms, lives in [Indexed Manifests and IteratorNodes](https://lhotse.readthedocs.io/en/latest/indexed-manifests.html).

### Stateful batch transforms[](https://lhotse.readthedocs.io/en/latest/datasets.html#stateful-batch-transforms "Permalink to this heading")

Batch transforms applied via `sampler.map(transform)` run inside `__next__()`. When a transform has RNG state (e.g. for deciding whether to apply augmentation), it should implement `state_dict()` and `load_state_dict()` so the sampler can save/restore it alongside the iterator graph state.

Use the helpers `save_rng_state()` and `load_rng_state()` for convenience:
    
    
    import random
    from lhotse import CutSet
    from lhotse.utils import save_rng_state, load_rng_state
    
    class MyAugmentation:
        def __init__(self, p=0.5, randgen=None):
            self.p = p
            self.random = randgen  # random.Random instance or None
    
        def __call__(self, cuts: CutSet) -> CutSet:
            if self.random is None:
                self.random = random.Random()
            return CutSet.from_cuts(
                self._augment(cut) if self.random.random() < self.p else cut
                for cut in cuts
            )
    
        def _augment(self, cut):
            ...  # your augmentation logic
    
        def state_dict(self) -> dict:
            return {"rng_state": save_rng_state(self.random)}
    
        def load_state_dict(self, sd: dict) -> None:
            self.random = load_rng_state(sd["rng_state"], self.random)
    

The sampler automatically checks for `state_dict`/`load_state_dict` on each registered transform. If your transform is stateless (no RNG), you don’t need to add these methods.

All built-in Lhotse transforms ([`PerturbSpeed`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbSpeed "lhotse.dataset.cut_transforms.PerturbSpeed"), [`PerturbVolume`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbVolume "lhotse.dataset.cut_transforms.PerturbVolume"), [`PerturbTempo`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbTempo "lhotse.dataset.cut_transforms.PerturbTempo"), [`ReverbWithImpulseResponse`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ReverbWithImpulseResponse "lhotse.dataset.cut_transforms.ReverbWithImpulseResponse"), [`CutMix`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.CutMix "lhotse.dataset.cut_transforms.CutMix"), [`ClippingTransform`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform "lhotse.dataset.cut_transforms.ClippingTransform"), [`Compress`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress "lhotse.dataset.cut_transforms.Compress"), and [`LowpassUsingResampling`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.LowpassUsingResampling "lhotse.dataset.cut_transforms.LowpassUsingResampling")) already implement this protocol.

## Batch I/O: pre-computed vs. on-the-fly features[](https://lhotse.readthedocs.io/en/latest/datasets.html#batch-i-o-pre-computed-vs-on-the-fly-features "Permalink to this heading")

Depending on the experimental setup and infrastructure, it might be more convenient to either pre-compute and store features like filter-bank energies for later use (as traditionally done in Kaldi/ESPnet/Espresso toolkits), or compute them dynamically during training (“on-the-fly”). Lhotse supports both modes of computation by introducing a class called [`BatchIO`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.BatchIO "lhotse.dataset.input_strategies.BatchIO"). It is accepted as an argument in most dataset classes, and defaults to [`PrecomputedFeatures`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.PrecomputedFeatures "lhotse.dataset.input_strategies.PrecomputedFeatures"). Other available choices are [`AudioSamples`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.AudioSamples "lhotse.dataset.input_strategies.AudioSamples") for working with waveforms directly, and [`OnTheFlyFeatures`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.OnTheFlyFeatures "lhotse.dataset.input_strategies.OnTheFlyFeatures"), which wraps a [`FeatureExtractor`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.features.base.FeatureExtractor "lhotse.features.base.FeatureExtractor") and applies it to a batch of recordings. These strategies automatically pad and collate the inputs, and provide information about the original signal lengths: as a number of frames/samples, binary mask, or start-end frame/sample pairs.

### Which strategy to choose?[](https://lhotse.readthedocs.io/en/latest/datasets.html#which-strategy-to-choose "Permalink to this heading")

In general, pre-computed features can be greatly compressed (we achieve 70% size reduction with regard to un-compressed features), and so the I/O load on your computing infrastructure will be much smaller than if you read the recordings directly. This is especially valuable when working with network file systems (NFS) that are typically used in computational grids for storage. When your experiment is I/O bound, then it is best to use pre-computed features.

When I/O is not the issue, it might be preferable to use on-the-fly computation as it shouldn’t require any prior steps to perform the network training. It is also simpler to apply a vast range of data augmentation methods in a fully randomized way (e.g. reverberation), although Lhotse provides support for approximate feature-domain signal mixing (e.g. for additive noise augmentation) to alleviate that to some extent.

## Handling random seeds[](https://lhotse.readthedocs.io/en/latest/datasets.html#handling-random-seeds "Permalink to this heading")

Lhotse provides several mechanisms for controlling randomness. At a basic level, there is a function `lhotse.utils.fix_random_seed()` which seeds Python’s, numpy’s and torch’s RNGs with the provided number.

However, many functions and classes in Lhotse accept either a random seed or an RNG instance to provide a finer control over randomness. Whenever random seed is accepted, it can be either an integer, or one of two strings: `"randomized"` or `"trng"`.

  * `"randomized`” seed is resolved lazily at the moment it’s needed and is intended as a mechanism to provide a different seed to each dataloading worker. In order for `"randomized"` to work, you have to first invoke [`lhotse.dataset.dataloading.worker_init_fn()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.worker_init_fn "lhotse.dataset.dataloading.worker_init_fn") in a given subprocess which sets the right environment variables. With a PyTorch `DataLoader` you can pass the keyword argument `worker_init_fn==make_worker_init_fn(seed=int_seed, rank=..., world_size=...)` using [`lhotse.dataset.dataloading.make_worker_init_fn()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.make_worker_init_fn "lhotse.dataset.dataloading.make_worker_init_fn") which will set the right seeds for you in multiprocessing and multi-node training. Note that if you resume training, you should change the `seed` passed to `make_worker_init_fn` on each resumed run to make the model train on different data.

  * `"trng"` seed is also resolved lazily at runtime, but it uses a true RNG (if available on your OS; consult Python’s `secrets` module documentation). It’s an easy way to ensure that every time you iterate data it’s done in different order, but may cause debugging data issues to be more difficult.




Note

The lazy seed resolution is done by calling [`lhotse.dataset.dataloading.resolve_seed()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.resolve_seed "lhotse.dataset.dataloading.resolve_seed").

## Customizing sampling constraints[](https://lhotse.readthedocs.io/en/latest/datasets.html#customizing-sampling-constraints "Permalink to this heading")

Since version 1.22.0, Lhotse provides a mechanism to customize how samplers measure the “length” of each example for the purpose of determining dynamic batch size. To leverage this option, use the keyword argument `constraint` in [`DynamicCutSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicCutSampler "lhotse.dataset.sampling.DynamicCutSampler") or [`DynamicBucketingSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicBucketingSampler "lhotse.dataset.sampling.DynamicBucketingSampler"). The sampling criteria are defined by implementing a subclass of [`SamplingConstraint`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint "lhotse.dataset.sampling.base.SamplingConstraint"):

_class _lhotse.dataset.sampling.base.SamplingConstraint[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingConstraint)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint "Permalink to this definition")
    

Defines the interface for sampling constraints. A sampling constraint keeps track of the sampled examples and lets the sampler know when it should yield a mini-batch.

_abstract _add(_example_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingConstraint.add)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint.add "Permalink to this definition")
    

Update the sampling constraint with the information about the sampled example (e.g. current batch size, total duration).

Return type:
    

`None`

_abstract _exceeded()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingConstraint.exceeded)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint.exceeded "Permalink to this definition")
    

Inform if the sampling constraint has been exceeded.

Return type:
    

`bool`

_abstract _close_to_exceeding()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingConstraint.close_to_exceeding)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint.close_to_exceeding "Permalink to this definition")
    

Inform if we’re going to exceed the sampling constraint after adding one more example.

Return type:
    

`bool`

_abstract _reset()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingConstraint.reset)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint.reset "Permalink to this definition")
    

Resets the internal state (called after yielding a mini-batch).

Return type:
    

`None`

_abstract _measure_length(_example_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingConstraint.measure_length)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint.measure_length "Permalink to this definition")
    

Returns the “size” of an example, used to create bucket distribution for bucketing samplers (e.g., for audio it may be duration; for text it may be number of tokens; etc.).

Return type:
    

`float`

select_bucket(_buckets_ , _example =None_, _example_len =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingConstraint.select_bucket)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint.select_bucket "Permalink to this definition")
    

Given a list of buckets and an example, assign the example to the correct bucket. This is leveraged by bucketing samplers.

Default implementation assumes that buckets are expressed in the same units as the output of [`SamplingConstraint.measure_length()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint.measure_length "lhotse.dataset.sampling.base.SamplingConstraint.measure_length") and returns the index of the first bucket that has a larger length than the example.

Return type:
    

`int`

copy()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingConstraint.copy)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint.copy "Permalink to this definition")
    

Return a shallow copy of this constraint.

Return type:
    

[`SamplingConstraint`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint "lhotse.dataset.sampling.base.SamplingConstraint")

The default constraint is [`TimeConstraint`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint "lhotse.dataset.sampling.base.TimeConstraint") which is created from `max_duration`, `max_cuts`, and `quadratic_duration` args passed to samplers constructor.

### Sampling non-audio data[](https://lhotse.readthedocs.io/en/latest/datasets.html#sampling-non-audio-data "Permalink to this heading")

Because [`SamplingConstraint`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint "lhotse.dataset.sampling.base.SamplingConstraint") defines the method `measure_length`, it’s possible to use a different attribute than duration (or a different formula) for computing the effective batch size. This enables re-using Lhotse’s sampling algorithms for other data than speech, and passing around other objects than [`Cut`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.Cut "lhotse.cut.Cut").

To showcase this, we added an experimental support for text-only dataloading. We introduced a few classes specifically for this purpose:

_class _lhotse.cut.text.TextExample(_text_ , _tokens =None_, _custom =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/cut/text.html#TextExample)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.cut.text.TextExample "Permalink to this definition")
    

Represents a single text example. Useful e.g. for language modeling.

text _: `str`_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.cut.text.TextExample.text "Permalink to this definition")
    

tokens _: `Optional`[`ndarray`]__ = None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.cut.text.TextExample.tokens "Permalink to this definition")
    

custom _: `Optional`[`Dict`[`str`, `Any`]]__ = None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.cut.text.TextExample.custom "Permalink to this definition")
    

_property _num_tokens _: int | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.cut.text.TextExample.num_tokens "Permalink to this definition")
    

__init__(_text_ , _tokens =None_, _custom =None_)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.cut.text.TextExample.__init__ "Permalink to this definition")
    

_class _lhotse.cut.text.TextPairExample(_source_ , _target_ , _custom =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/cut/text.html#TextPairExample)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.cut.text.TextPairExample "Permalink to this definition")
    

Represents a pair of text examples. Useful e.g. for sequence-to-sequence tasks.

source _: [`TextExample`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.cut.text.TextExample "lhotse.cut.text.TextExample")_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.cut.text.TextPairExample.source "Permalink to this definition")
    

target _: [`TextExample`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.cut.text.TextExample "lhotse.cut.text.TextExample")_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.cut.text.TextPairExample.target "Permalink to this definition")
    

custom _: `Optional`[`Dict`[`str`, `Any`]]__ = None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.cut.text.TextPairExample.custom "Permalink to this definition")
    

_property _num_tokens _: int | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.cut.text.TextPairExample.num_tokens "Permalink to this definition")
    

__init__(_source_ , _target_ , _custom =None_)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.cut.text.TextPairExample.__init__ "Permalink to this definition")
    

_class _lhotse.lazy.LazyTxtIterator(_path_ , _as_text_example =True_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/lazy.html#LazyTxtIterator)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.lazy.LazyTxtIterator "Permalink to this definition")
    

LazyTxtIterator is a thin wrapper over builtin `open` function to iterate over lines in a (possibly compressed) text file. It can also provide the number of lines via __len__ via fast newlines counting.

__init__(_path_ , _as_text_example =True_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/lazy.html#LazyTxtIterator.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.lazy.LazyTxtIterator.__init__ "Permalink to this definition")
    

_class _lhotse.dataset.sampling.base.TokenConstraint(_max_tokens =None_, _max_examples =None_, _current =0_, _num_examples =0_, _longest_seen =0_, _quadratic_length =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#TokenConstraint)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.TokenConstraint "Permalink to this definition")
    

Represents a token-based constraint for sampler classes that sample text data. It is defined as maximum total number of tokens in a mini-batch and/or max batch size.

Similarly to [`TimeConstraint`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint "lhotse.dataset.sampling.base.TimeConstraint"), we support `quadratic_length` for quadratic token penalty when sampling longer texts.

max_tokens _: `int`_ _ = None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.TokenConstraint.max_tokens "Permalink to this definition")
    

max_examples _: `int`_ _ = None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.TokenConstraint.max_examples "Permalink to this definition")
    

current _: `int`_ _ = 0_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.TokenConstraint.current "Permalink to this definition")
    

num_examples _: `int`_ _ = 0_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.TokenConstraint.num_examples "Permalink to this definition")
    

longest_seen _: `int`_ _ = 0_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.TokenConstraint.longest_seen "Permalink to this definition")
    

quadratic_length _: `Optional`[`int`]__ = None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.TokenConstraint.quadratic_length "Permalink to this definition")
    

add(_example_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#TokenConstraint.add)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.TokenConstraint.add "Permalink to this definition")
    

Increment the internal token counter for the constraint, selecting the right property from the input object.

Return type:
    

`None`

exceeded()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#TokenConstraint.exceeded)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.TokenConstraint.exceeded "Permalink to this definition")
    

Is the constraint exceeded or not.

Return type:
    

`bool`

close_to_exceeding()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#TokenConstraint.close_to_exceeding)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.TokenConstraint.close_to_exceeding "Permalink to this definition")
    

Check if the batch is close to satisfying the constraints. We define “closeness” as: if we added one more cut that has duration/num_frames/num_samples equal to the longest seen cut in the current batch, then the batch would have exceeded the constraints.

Return type:
    

`bool`

reset()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#TokenConstraint.reset)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.TokenConstraint.reset "Permalink to this definition")
    

Reset the internal counter (to be used after a batch was created, to start collecting a new one).

Return type:
    

`None`

measure_length(_example_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#TokenConstraint.measure_length)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.TokenConstraint.measure_length "Permalink to this definition")
    

Returns the “size” of an example, used to create bucket distribution for bucketing samplers (e.g., for audio it may be duration; for text it may be number of tokens; etc.).

Return type:
    

`float`

__init__(_max_tokens =None_, _max_examples =None_, _current =0_, _num_examples =0_, _longest_seen =0_, _quadratic_length =None_)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.TokenConstraint.__init__ "Permalink to this definition")
    

A minimal example of how to perform text-only dataloading is available below (note that any of these classes may be replaced by your own implementation if that is more suitable to your work):
    
    
    import torch
    import numpy as np
    from lhotse import CutSet
    from lhotse.lazy import LazyTxtIterator
    from lhotse.cut.text import TextPairExample
    from lhotse.dataset import DynamicBucketingSampler, TokenConstraint
    from lhotse.dataset.collation import collate_vectors
    
    examples = CutSet(LazyTxtIterator("data.txt"))
    
    def tokenize(example):
        # tokenize as individual bytes; BPE or another technique may be used here instead
        example.tokens = np.frombuffer(example.text.encode("utf-8"), np.int8)
        return example
    
    examples = examples.map(tokenize, apply_fn=None)
    
    sampler = DynamicBucketingSampler(examples, constraint=TokenConstraint(max_tokens=1024, quadratic_length=128),      num_buckets=2)
    
    class ExampleTextDataset(torch.utils.data.Dataset):
        def __getitem__(self, examples: CutSet):
            tokens = [ex.tokens for ex in examples]
            token_lens = torch.tensor([len(t) for t in tokens])
            tokens = collate_vectors(tokens, padding_value=-1)
            return tokens, token_lens
    
    dloader = torch.utils.data.DataLoader(ExampleTextDataset(), sampler=sampler, batch_size=None)
    
    for batch in dloader:
        print(batch)
    

Note

Support for this kind of dataloading is experimental in Lhotse. If you run into any rough edges, please let us know.

## Dataset’s list[](https://lhotse.readthedocs.io/en/latest/datasets.html#module-lhotse.dataset.diarization "Permalink to this heading")

_class _lhotse.dataset.diarization.DiarizationDataset(_cuts_ , _uem =None_, _min_speaker_dim =None_, _global_speaker_ids =False_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/diarization.html#DiarizationDataset)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.diarization.DiarizationDataset "Permalink to this definition")
    

A PyTorch Dataset for the speaker diarization task. Our assumptions about speaker diarization are the following:

  * we assume a single channel input (for now), which could be either a true mono signal
    

or a beamforming result from a microphone array.

  * we assume that the supervision used for model training is a speech activity matrix, with one
    

row dedicated to each speaker (either in the current cut or the whole dataset, depending on the settings). The columns correspond to feature frames. Each row is effectively a Voice Activity Detection supervision for a single speaker. This setup is somewhat inspired by the TS-VAD paper: <https://arxiv.org/abs/2005.07272>




Each item in this dataset is a dict of:
    
    
    {
        'features': (B x T x F) tensor
        'features_lens': (B, ) tensor
        'speaker_activity': (B x num_speaker x T) tensor
    }
    

Constructor arguments:

Parameters:
    

  * **cuts** ([`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")) – a `CutSet` used to create the dataset object.

  * **uem** (`Optional`[[`SupervisionSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.supervision.SupervisionSet "lhotse.supervision.SupervisionSet")]) – a `SupervisionSet` used to set regions for diarization

  * **min_speaker_dim** (`Optional`[`int`]) – optional int, when specified it will enforce that the matrix shape is at least that value (useful for datasets like CHiME 6 where the number of speakers is always 4, but some cuts might have less speakers than that).

  * **global_speaker_ids** (`bool`) – a bool, indicates whether the same speaker should always retain the same row index in the speaker activity matrix (useful for speaker-dependent systems)

  * **root_dir** – a prefix path to be attached to the feature files paths.




__init__(_cuts_ , _uem =None_, _min_speaker_dim =None_, _global_speaker_ids =False_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/diarization.html#DiarizationDataset.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.diarization.DiarizationDataset.__init__ "Permalink to this definition")
    

_class _lhotse.dataset.unsupervised.UnsupervisedDataset[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/unsupervised.html#UnsupervisedDataset)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.UnsupervisedDataset "Permalink to this definition")
    

Dataset that contains no supervision - it only provides the features extracted from recordings.
    
    
    {
        'features': (B x T x F) tensor
        'features_lens': (B, ) tensor
    }
    

__init__()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/unsupervised.html#UnsupervisedDataset.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.UnsupervisedDataset.__init__ "Permalink to this definition")
    

_class _lhotse.dataset.unsupervised.UnsupervisedWaveformDataset(_collate =True_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/unsupervised.html#UnsupervisedWaveformDataset)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.UnsupervisedWaveformDataset "Permalink to this definition")
    

A variant of UnsupervisedDataset that provides waveform samples instead of features. The output is a tensor of shape (C, T), with C being the number of channels and T the number of audio samples. In this implementation, there will always be a single channel.

Returns:
    
    
    {
        'audio': (B x NumSamples) float tensor
        'audio_lens': (B, ) int tensor
    }
    

__init__(_collate =True_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/unsupervised.html#UnsupervisedWaveformDataset.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.UnsupervisedWaveformDataset.__init__ "Permalink to this definition")
    

_class _lhotse.dataset.unsupervised.DynamicUnsupervisedDataset(_feature_extractor_ , _augment_fn =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/unsupervised.html#DynamicUnsupervisedDataset)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.DynamicUnsupervisedDataset "Permalink to this definition")
    

An example dataset that shows how to use on-the-fly feature extraction in Lhotse. It accepts two additional inputs - a FeatureExtractor and an optional WavAugmenter for time-domain data augmentation.. The output is approximately the same as that of the `UnsupervisedDataset` \- there might be slight differences for `MixedCut``s, because this dataset mixes them in the time domain, and ``UnsupervisedDataset` does that in the feature domain. Cuts that are not mixed will yield identical results in both dataset classes.

__init__(_feature_extractor_ , _augment_fn =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/unsupervised.html#DynamicUnsupervisedDataset.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.DynamicUnsupervisedDataset.__init__ "Permalink to this definition")
    

_class _lhotse.dataset.unsupervised.RecordingChunkIterableDataset(_recordings_ , _chunk_size_ , _chunk_shift_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/unsupervised.html#RecordingChunkIterableDataset)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.RecordingChunkIterableDataset "Permalink to this definition")
    

This dataset iterates over chunks of a recording, for each recording provided. It supports setting a chunk_shift < chunk_size to run model predictions on overlapping audio chunks.

The format of yielded items is the following:
    
    
    {
        "recording_id": str
        "begin_time": tensor with dtype=float32 shape=(1,)
        "end_time": tensor with dtype=float32 shape=(1,)
        "audio": tensor with dtype=float32 shape=(chunk_size_in_samples,)
    }
    

Unlike most other datasets in Lhotse, this dataset does not yield batched items, and should be used like the following:
    
    
    >>> recordings = RecordingSet.from_file("my-recordings.jsonl.gz")
    ... dataset = RecordingChunkIterableDataset(recordings, chunk_size=30.0, chunk_shift=25.0)
    ... dloader = torch.utils.data.DataLoader(
    ...     dataset,
    ...     batch_size=32,
    ...     collate_fn=audio_chunk_collate,
    ...     worker_init_fn=audio_chunk_worker_init_fn,
    ... )
    

__init__(_recordings_ , _chunk_size_ , _chunk_shift_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/unsupervised.html#RecordingChunkIterableDataset.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.RecordingChunkIterableDataset.__init__ "Permalink to this definition")
    

validate()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/unsupervised.html#RecordingChunkIterableDataset.validate)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.RecordingChunkIterableDataset.validate "Permalink to this definition")
    

Return type:
    

`None`

lhotse.dataset.unsupervised.audio_chunk_collate(_batch_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/unsupervised.html#audio_chunk_collate)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.audio_chunk_collate "Permalink to this definition")
    

lhotse.dataset.unsupervised.audio_chunk_worker_init_fn(_worker_id_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/unsupervised.html#audio_chunk_worker_init_fn)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.unsupervised.audio_chunk_worker_init_fn "Permalink to this definition")
    

_class _lhotse.dataset.speech_recognition.K2SpeechRecognitionDataset(_return_cuts=False_ , _cut_transforms=None_ , _input_transforms=None_ , _input_strategy= <lhotse.dataset.input_strategies.PrecomputedFeatures object>_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/speech_recognition.html#K2SpeechRecognitionDataset)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.speech_recognition.K2SpeechRecognitionDataset "Permalink to this definition")
    

The PyTorch Dataset for the speech recognition task using k2 library.

This dataset expects to be queried with lists of cut IDs, for which it loads features and automatically collates/batches them.

To use it with a PyTorch DataLoader, set `batch_size=None` and provide a `SimpleCutSampler` sampler.

Each item in this dataset is a dict of:
    
    
    {
        'inputs': float tensor with shape determined by :attr:`input_strategy`:
                  - single-channel:
                    - features: (B, T, F)
                    - audio: (B, T)
                  - multi-channel: currently not supported
        'supervisions': [
            {
                'sequence_idx': Tensor[int] of shape (S,)
                'text': List[str] of len S
    
                # For feature input strategies
                'start_frame': Tensor[int] of shape (S,)
                'num_frames': Tensor[int] of shape (S,)
    
                # For audio input strategies
                'start_sample': Tensor[int] of shape (S,)
                'num_samples': Tensor[int] of shape (S,)
    
                # Optionally, when return_cuts=True
                'cut': List[AnyCut] of len S
            }
        ]
    }
    

Dimension symbols legend: * `B` \- batch size (number of Cuts) * `S` \- number of supervision segments (greater or equal to B, as each Cut may have multiple supervisions) * `T` \- number of frames of the longest Cut * `F` \- number of features

The ‘sequence_idx’ field is the index of the Cut used to create the example in the Dataset.

__init__(_return_cuts=False_ , _cut_transforms=None_ , _input_transforms=None_ , _input_strategy= <lhotse.dataset.input_strategies.PrecomputedFeatures object>_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/speech_recognition.html#K2SpeechRecognitionDataset.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.speech_recognition.K2SpeechRecognitionDataset.__init__ "Permalink to this definition")
    

k2 ASR IterableDataset constructor.

Parameters:
    

  * **return_cuts** (`bool`) – When `True`, will additionally return a “cut” field in each batch with the Cut objects used to create that batch.

  * **cut_transforms** (`Optional`[`List`[`Callable`[[[`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")], [`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")]]]) – A list of transforms to be applied on each sampled batch, before converting cuts to an input representation (audio/features). Examples: cut concatenation, noise cuts mixing, etc.

  * **input_transforms** (`Optional`[`List`[`Callable`[[`Tensor`], `Tensor`]]]) – A list of transforms to be applied on each sampled batch, after the cuts are converted to audio/features. Examples: normalization, SpecAugment, etc.

  * **input_strategy** ([`BatchIO`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.BatchIO "lhotse.dataset.input_strategies.BatchIO")) – Converts cuts into a collated batch of audio/features. By default, reads pre-computed features from disk.




lhotse.dataset.speech_recognition.validate_for_asr(_cuts_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/speech_recognition.html#validate_for_asr)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.speech_recognition.validate_for_asr "Permalink to this definition")
    

Return type:
    

`None`

lhotse.dataset.speech_synthesis[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.speech_synthesis "Permalink to this definition")
    

alias of <module ‘lhotse.dataset.speech_synthesis’ from ‘/home/docs/checkouts/readthedocs.org/user_builds/lhotse/envs/latest/lib/python3.10/site-packages/lhotse/dataset/speech_synthesis.py’>

_class _lhotse.dataset.source_separation.DynamicallyMixedSourceSeparationDataset(_sources_set_ , _mixtures_set_ , _nonsources_set =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/source_separation.html#DynamicallyMixedSourceSeparationDataset)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.source_separation.DynamicallyMixedSourceSeparationDataset "Permalink to this definition")
    

A PyTorch Dataset for the source separation task. It’s created from a number of CutSets:

  * `sources_set`: provides the audio cuts for the sources that (the targets of source separation),

  * `mixtures_set`: provides the audio cuts for the signal mix (the input of source separation),

  * `nonsources_set`: _(optional)_ provides the audio cuts for other signals that are in the mix, but are not the targets of source separation. Useful for adding noise.




When queried for data samples, it returns a dict of:
    
    
    {
        'sources': (N x T x F) tensor,
        'mixture': (T x F) tensor,
        'real_mask': (N x T x F) tensor,
        'binary_mask': (T x F) tensor
    }
    

This Dataset performs on-the-fly feature-domain mixing of the sources. It expects the mixtures_set to contain MixedCuts, so that it knows which Cuts should be mixed together.

__init__(_sources_set_ , _mixtures_set_ , _nonsources_set =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/source_separation.html#DynamicallyMixedSourceSeparationDataset.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.source_separation.DynamicallyMixedSourceSeparationDataset.__init__ "Permalink to this definition")
    

validate()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/source_separation.html#DynamicallyMixedSourceSeparationDataset.validate)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.source_separation.DynamicallyMixedSourceSeparationDataset.validate "Permalink to this definition")
    

_class _lhotse.dataset.source_separation.PreMixedSourceSeparationDataset(_sources_set_ , _mixtures_set_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/source_separation.html#PreMixedSourceSeparationDataset)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.source_separation.PreMixedSourceSeparationDataset "Permalink to this definition")
    

A PyTorch Dataset for the source separation task. It’s created from two CutSets - one provides the audio cuts for the sources, and the other one the audio cuts for the signal mix. When queried for data samples, it returns a dict of:
    
    
    {
        'sources': (N x T x F) tensor,
        'mixture': (T x F) tensor,
        'real_mask': (N x T x F) tensor,
        'binary_mask': (T x F) tensor
    }
    

It expects both CutSets to return regular Cuts, meaning that the signals were mixed in the time domain. In contrast to DynamicallyMixedSourceSeparationDataset, no on-the-fly feature-domain-mixing is performed.

__init__(_sources_set_ , _mixtures_set_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/source_separation.html#PreMixedSourceSeparationDataset.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.source_separation.PreMixedSourceSeparationDataset.__init__ "Permalink to this definition")
    

_class _lhotse.dataset.vad.VadDataset(_input_strategy= <lhotse.dataset.input_strategies.PrecomputedFeatures object>_, _cut_transforms=None_ , _input_transforms=None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/vad.html#VadDataset)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.vad.VadDataset "Permalink to this definition")
    

The PyTorch Dataset for the voice activity detection task. Each item in this dataset is a dict of:
    
    
    {
        'inputs': (B x T x F) tensor
        'input_lens': (B,) tensor
        'is_voice': (T x 1) tensor
        'cut': List[Cut]
    }
    

__init__(_input_strategy= <lhotse.dataset.input_strategies.PrecomputedFeatures object>_, _cut_transforms=None_ , _input_transforms=None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/vad.html#VadDataset.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.vad.VadDataset.__init__ "Permalink to this definition")
    

## Sampler’s list[](https://lhotse.readthedocs.io/en/latest/datasets.html#module-lhotse.dataset.sampling "Permalink to this heading")

_class _lhotse.dataset.sampling.TokenConstraint(_max_tokens =None_, _max_examples =None_, _current =0_, _num_examples =0_, _longest_seen =0_, _quadratic_length =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#TokenConstraint)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint "Permalink to this definition")
    

Represents a token-based constraint for sampler classes that sample text data. It is defined as maximum total number of tokens in a mini-batch and/or max batch size.

Similarly to [`TimeConstraint`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint "lhotse.dataset.sampling.TimeConstraint"), we support `quadratic_length` for quadratic token penalty when sampling longer texts.

max_tokens _: `int`_ _ = None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.max_tokens "Permalink to this definition")
    

max_examples _: `int`_ _ = None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.max_examples "Permalink to this definition")
    

current _: `int`_ _ = 0_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.current "Permalink to this definition")
    

num_examples _: `int`_ _ = 0_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.num_examples "Permalink to this definition")
    

longest_seen _: `int`_ _ = 0_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.longest_seen "Permalink to this definition")
    

quadratic_length _: `Optional`[`int`]__ = None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.quadratic_length "Permalink to this definition")
    

add(_example_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#TokenConstraint.add)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.add "Permalink to this definition")
    

Increment the internal token counter for the constraint, selecting the right property from the input object.

Return type:
    

`None`

exceeded()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#TokenConstraint.exceeded)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.exceeded "Permalink to this definition")
    

Is the constraint exceeded or not.

Return type:
    

`bool`

close_to_exceeding()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#TokenConstraint.close_to_exceeding)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.close_to_exceeding "Permalink to this definition")
    

Check if the batch is close to satisfying the constraints. We define “closeness” as: if we added one more cut that has duration/num_frames/num_samples equal to the longest seen cut in the current batch, then the batch would have exceeded the constraints.

Return type:
    

`bool`

reset()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#TokenConstraint.reset)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.reset "Permalink to this definition")
    

Reset the internal counter (to be used after a batch was created, to start collecting a new one).

Return type:
    

`None`

measure_length(_example_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#TokenConstraint.measure_length)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.measure_length "Permalink to this definition")
    

Returns the “size” of an example, used to create bucket distribution for bucketing samplers (e.g., for audio it may be duration; for text it may be number of tokens; etc.).

Return type:
    

`float`

__init__(_max_tokens =None_, _max_examples =None_, _current =0_, _num_examples =0_, _longest_seen =0_, _quadratic_length =None_)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TokenConstraint.__init__ "Permalink to this definition")
    

_class _lhotse.dataset.sampling.TimeConstraint(_max_duration =None_, _max_cuts =None_, _current =0_, _num_cuts =0_, _longest_seen =0_, _quadratic_duration =None_, _concatenate_cuts =False_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#TimeConstraint)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint "Permalink to this definition")
    

Represents a time-based constraint for sampler classes. It is defined as maximum total batch duration (in seconds) and/or the total number of cuts.

[`TimeConstraint`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint "lhotse.dataset.sampling.TimeConstraint") can be used for tracking whether the criterion has been exceeded via the add(cut), exceeded() and reset() methods. It will automatically track the right criterion (i.e. select duration from the cut). It can also be a null constraint (never exceeded).

When `quadratic_duration` is set, we will try to compensate for models that have a quadratic complexity w.r.t. the input sequence length. We use the following formula to determine the effective duration for each cut:
    
    
    effective_duration = duration + (duration ** 2) / quadratic_duration
    

We recommend setting quadratic_duration to something between 15 and 40 for transformer architectures.

When `concatenate_cuts` is set, the effective duration of the batch is replaced by simple sum of durations of utterances. The shorter utterances will be concatenated, so the amount of padding becomes smaller. `ConcatenateCuts` also adds some silence between the concatenated cuts. However, we ignore this from the computation of total duration, as we don’t know in advance how many concatenations will be done.

max_duration _: `Optional`[`float`]__ = None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.max_duration "Permalink to this definition")
    

max_cuts _: `Optional`[`int`]__ = None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.max_cuts "Permalink to this definition")
    

current _: `Union`[`int`, `float`]__ = 0_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.current "Permalink to this definition")
    

num_cuts _: `int`_ _ = 0_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.num_cuts "Permalink to this definition")
    

longest_seen _: `Union`[`int`, `float`]__ = 0_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.longest_seen "Permalink to this definition")
    

quadratic_duration _: `Optional`[`float`]__ = None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.quadratic_duration "Permalink to this definition")
    

concatenate_cuts _: `bool`_ _ = False_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.concatenate_cuts "Permalink to this definition")
    

is_active()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#TimeConstraint.is_active)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.is_active "Permalink to this definition")
    

Is it an actual constraint, or a dummy one (i.e. never exceeded).

Return type:
    

`bool`

add(_example_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#TimeConstraint.add)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.add "Permalink to this definition")
    

Increment the internal counter for the time constraint, selecting the right property from the input `cut` object.

Return type:
    

`None`

exceeded()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#TimeConstraint.exceeded)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.exceeded "Permalink to this definition")
    

Is the constraint exceeded or not.

Return type:
    

`bool`

close_to_exceeding()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#TimeConstraint.close_to_exceeding)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.close_to_exceeding "Permalink to this definition")
    

Check if the batch is close to satisfying the constraints. We define “closeness” as: if we added one more cut that has duration/num_frames/num_samples equal to the longest seen cut in the current batch, then the batch would have exceeded the constraints.

When `concatenate_cuts` is set, the behavior of close_to_exceeding() becomes equal to exceeded().

Return type:
    

`bool`

reset()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#TimeConstraint.reset)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.reset "Permalink to this definition")
    

Reset the internal counter (to be used after a batch was created, to start collecting a new one).

Return type:
    

`None`

measure_length(_example_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#TimeConstraint.measure_length)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.measure_length "Permalink to this definition")
    

Returns the “size” of an example, used to create bucket distribution for bucketing samplers (e.g., for audio it may be duration; for text it may be number of tokens; etc.).

Return type:
    

`float`

state_dict()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#TimeConstraint.state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.state_dict "Permalink to this definition")
    

Return type:
    

`Dict`[`str`, `Any`]

load_state_dict(_state_dict_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#TimeConstraint.load_state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.load_state_dict "Permalink to this definition")
    

Return type:
    

`None`

__init__(_max_duration =None_, _max_cuts =None_, _current =0_, _num_cuts =0_, _longest_seen =0_, _quadratic_duration =None_, _concatenate_cuts =False_)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint.__init__ "Permalink to this definition")
    

_class _lhotse.dataset.sampling.SamplingDiagnostics(_current_epoch =0_, _stats_per_epoch =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingDiagnostics)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics "Permalink to this definition")
    

Utility for collecting diagnostics about the sampling process: how many cuts/batches were discarded.

current_epoch _: `int`_ _ = 0_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.current_epoch "Permalink to this definition")
    

stats_per_epoch _: `Dict`[`int`, `EpochDiagnostics`]__ = None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.stats_per_epoch "Permalink to this definition")
    

reset_current_epoch()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingDiagnostics.reset_current_epoch)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.reset_current_epoch "Permalink to this definition")
    

Return type:
    

`None`

set_epoch(_epoch_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingDiagnostics.set_epoch)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.set_epoch "Permalink to this definition")
    

Return type:
    

`None`

advance_epoch()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingDiagnostics.advance_epoch)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.advance_epoch "Permalink to this definition")
    

Return type:
    

`None`

_property _current_epoch_stats _: EpochDiagnostics_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.current_epoch_stats "Permalink to this definition")
    

keep(_cuts_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingDiagnostics.keep)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.keep "Permalink to this definition")
    

Return type:
    

`None`

discard(_cuts_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingDiagnostics.discard)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.discard "Permalink to this definition")
    

Return type:
    

`None`

discard_single(_cut_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingDiagnostics.discard_single)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.discard_single "Permalink to this definition")
    

Return type:
    

`None`

_property _kept_cuts _: int_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.kept_cuts "Permalink to this definition")
    

_property _discarded_cuts _: int_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.discarded_cuts "Permalink to this definition")
    

_property _kept_batches _: int_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.kept_batches "Permalink to this definition")
    

_property _discarded_batches _: int_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.discarded_batches "Permalink to this definition")
    

_property _total_cuts _: int_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.total_cuts "Permalink to this definition")
    

_property _total_batches _: int_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.total_batches "Permalink to this definition")
    

get_report(_per_epoch =False_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingDiagnostics.get_report)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.get_report "Permalink to this definition")
    

Returns a string describing the statistics of the sampling process so far.

Return type:
    

`str`

state_dict()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingDiagnostics.state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.state_dict "Permalink to this definition")
    

Return type:
    

`Dict`[`str`, `Any`]

load_state_dict(_state_dict_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingDiagnostics.load_state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.load_state_dict "Permalink to this definition")
    

Return type:
    

[`SamplingDiagnostics`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics "lhotse.dataset.sampling.base.SamplingDiagnostics")

__init__(_current_epoch =0_, _stats_per_epoch =None_)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics.__init__ "Permalink to this definition")
    

_class _lhotse.dataset.sampling.SamplingConstraint[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingConstraint)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingConstraint "Permalink to this definition")
    

Defines the interface for sampling constraints. A sampling constraint keeps track of the sampled examples and lets the sampler know when it should yield a mini-batch.

_abstract _add(_example_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingConstraint.add)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingConstraint.add "Permalink to this definition")
    

Update the sampling constraint with the information about the sampled example (e.g. current batch size, total duration).

Return type:
    

`None`

_abstract _exceeded()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingConstraint.exceeded)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingConstraint.exceeded "Permalink to this definition")
    

Inform if the sampling constraint has been exceeded.

Return type:
    

`bool`

_abstract _close_to_exceeding()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingConstraint.close_to_exceeding)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingConstraint.close_to_exceeding "Permalink to this definition")
    

Inform if we’re going to exceed the sampling constraint after adding one more example.

Return type:
    

`bool`

_abstract _reset()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingConstraint.reset)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingConstraint.reset "Permalink to this definition")
    

Resets the internal state (called after yielding a mini-batch).

Return type:
    

`None`

_abstract _measure_length(_example_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingConstraint.measure_length)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingConstraint.measure_length "Permalink to this definition")
    

Returns the “size” of an example, used to create bucket distribution for bucketing samplers (e.g., for audio it may be duration; for text it may be number of tokens; etc.).

Return type:
    

`float`

select_bucket(_buckets_ , _example =None_, _example_len =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingConstraint.select_bucket)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingConstraint.select_bucket "Permalink to this definition")
    

Given a list of buckets and an example, assign the example to the correct bucket. This is leveraged by bucketing samplers.

Default implementation assumes that buckets are expressed in the same units as the output of [`SamplingConstraint.measure_length()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingConstraint.measure_length "lhotse.dataset.sampling.SamplingConstraint.measure_length") and returns the index of the first bucket that has a larger length than the example.

Return type:
    

`int`

copy()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/base.html#SamplingConstraint.copy)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingConstraint.copy "Permalink to this definition")
    

Return a shallow copy of this constraint.

Return type:
    

[`SamplingConstraint`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint "lhotse.dataset.sampling.base.SamplingConstraint")

_class _lhotse.dataset.sampling.BucketingSampler(_*cuts_ , _sampler_type= <class 'lhotse.dataset.sampling.simple.SimpleCutSampler'>_, _num_buckets=10_ , _drop_last=False_ , _seed=0_ , _**kwargs_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/bucketing.html#BucketingSampler)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler "Permalink to this definition")
    

Sorts the cuts in a `CutSet` by their duration and puts them into similar duration buckets. For each bucket, it instantiates a simpler sampler instance, e.g. [`SimpleCutSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SimpleCutSampler "lhotse.dataset.sampling.SimpleCutSampler").

It behaves like an iterable that yields lists of strings (cut IDs). During iteration, it randomly selects one of the buckets to yield the batch from, until all the underlying samplers are depleted (which means it’s the end of an epoch).

Examples:

Bucketing sampler with 20 buckets, sampling single cuts:
    
    
    >>> sampler = BucketingSampler(
    ...    cuts,
    ...    # BucketingSampler specific args
    ...    sampler_type=SimpleCutSampler, num_buckets=20,
    ...    # Args passed into SimpleCutSampler
    ...    max_duration=200
    ... )
    

Bucketing sampler with 20 buckets, sampling pairs of source-target cuts:
    
    
    >>> sampler = BucketingSampler(
    ...    cuts, target_cuts,
    ...    # BucketingSampler specific args
    ...    sampler_type=CutPairsSampler, num_buckets=20,
    ...    # Args passed into CutPairsSampler
    ...    max_source_duration=200, max_target_duration=150
    ... )
    

__init__(_*cuts_ , _sampler_type= <class 'lhotse.dataset.sampling.simple.SimpleCutSampler'>_, _num_buckets=10_ , _drop_last=False_ , _seed=0_ , _**kwargs_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/bucketing.html#BucketingSampler.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.__init__ "Permalink to this definition")
    

BucketingSampler’s constructor.

Parameters:
    

  * **cuts** ([`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")) – one or more `CutSet` objects. The first one will be used to determine the buckets for all of them. Then, all of them will be used to instantiate the per-bucket samplers.

  * **sampler_type** (`Type`) – a sampler type that will be created for each underlying bucket.

  * **num_buckets** (`int`) – how many buckets to create.

  * **drop_last** (`bool`) – When `True`, we will drop all incomplete batches. A batch is considered incomplete if it depleted a bucket before hitting the constraint such as max_duration, max_cuts, etc.

  * **seed** (`int`) – random seed for bucket selection

  * **kwargs** (`Any`) – Arguments used to create the underlying sampler for each bucket.




_property _remaining_duration _: float | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.remaining_duration "Permalink to this definition")
    

Remaining duration of data left in the sampler (may be inexact due to float arithmetic). Not available when the CutSet is read in lazy mode (returns None).

_property _remaining_cuts _: int | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.remaining_cuts "Permalink to this definition")
    

Remaining number of cuts in the sampler. Not available when the CutSet is read in lazy mode (returns None).

_property _num_cuts _: int | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.num_cuts "Permalink to this definition")
    

Total number of cuts in the sampler. Not available when the CutSet is read in lazy mode (returns None).

set_epoch(_epoch_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/bucketing.html#BucketingSampler.set_epoch)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.set_epoch "Permalink to this definition")
    

Sets the epoch for this sampler. When `shuffle=True`, this ensures all replicas use a different random ordering for each epoch. Otherwise, the next iteration of this sampler will yield the same ordering.

Parameters:
    

**epoch** (`int`) – Epoch number.

Return type:
    

`None`

filter(_predicate_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/bucketing.html#BucketingSampler.filter)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.filter "Permalink to this definition")
    

Add a constraint on individual cuts that has to be satisfied to consider them.

Can be useful when handling large, lazy manifests where it is not feasible to pre-filter them before instantiating the sampler.

Return type:
    

`None`

Example:
    
    
    
    >>> cuts = CutSet(...)
    ... sampler = SimpleCutSampler(cuts, max_duration=100.0)
    ... # Retain only the cuts that have at least 1s and at most 20s duration.
    ... sampler.filter(lambda cut: 1.0 <= cut.duration <= 20.0)
    

allow_iter_to_reset_state()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/bucketing.html#BucketingSampler.allow_iter_to_reset_state)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.allow_iter_to_reset_state "Permalink to this definition")
    

Enables re-setting to the start of an epoch when iter() is called. This is only needed in one specific scenario: when we restored previous sampler state via `sampler.load_state_dict()` but want to discard the progress in the current epoch and start from the beginning.

state_dict()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/bucketing.html#BucketingSampler.state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.state_dict "Permalink to this definition")
    

Return the current state of the sampler in a state_dict. Together with `load_state_dict()`, this can be used to restore the training loop’s state to the one stored in the state_dict.

Return type:
    

`Dict`[`str`, `Any`]

load_state_dict(_state_dict_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/bucketing.html#BucketingSampler.load_state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.load_state_dict "Permalink to this definition")
    

Restore the state of the sampler that is described in a state_dict. This will result in the sampler yielding batches from where the previous training left it off. :rtype: `None`

Caution

The samplers are expected to be initialized with the same CutSets, but this is not explicitly checked anywhere.

Caution

The input `state_dict` is being mutated: we remove each consumed key, and expect it to be empty at the end of loading. If you don’t want this behavior, pass a copy inside of this function (e.g., using `import deepcopy`).

Note

For implementers of sub-classes of CutSampler: the flag `self._just_restored_state` has to be handled in `__iter__` to make it avoid resetting the just-restored state (only once).

_property _is_depleted _: bool_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.is_depleted "Permalink to this definition")
    

_property _diagnostics _: [SamplingDiagnostics](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics "lhotse.dataset.sampling.base.SamplingDiagnostics")_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.diagnostics "Permalink to this definition")
    

Info on how many cuts / batches were returned or rejected during iteration.

This property can be overriden by child classes e.g. to merge diagnostics of composite samplers.

get_report()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/bucketing.html#BucketingSampler.get_report)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler.get_report "Permalink to this definition")
    

Returns a string describing the statistics of the sampling process so far.

Return type:
    

`str`

_class _lhotse.dataset.sampling.CutPairsSampler(_source_cuts_ , _target_cuts_ , _max_source_duration =None_, _max_target_duration =None_, _max_cuts =None_, _shuffle =False_, _drop_last =False_, _world_size =None_, _rank =None_, _seed =0_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/cut_pairs.html#CutPairsSampler)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.CutPairsSampler "Permalink to this definition")
    

Samples pairs of cuts from a “source” and “target” CutSet. It expects that both CutSet’s strictly consist of Cuts with corresponding IDs. It behaves like an iterable that yields lists of strings (cut IDs).

When one of `max_source_duration`, `max_target_duration`, or `max_cuts` is specified, the batch size is dynamic. Exactly zero or one of those constraints can be specified. Padding required to collate the batch does not contribute to max source_duration/target_duration.

__init__(_source_cuts_ , _target_cuts_ , _max_source_duration =None_, _max_target_duration =None_, _max_cuts =None_, _shuffle =False_, _drop_last =False_, _world_size =None_, _rank =None_, _seed =0_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/cut_pairs.html#CutPairsSampler.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.CutPairsSampler.__init__ "Permalink to this definition")
    

CutPairsSampler’s constructor.

Parameters:
    

  * **source_cuts** ([`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")) – the first `CutSet` to sample data from.

  * **target_cuts** ([`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")) – the second `CutSet` to sample data from.

  * **max_source_duration** (`Optional`[`float`]) – The maximum total recording duration from `source_cuts`.

  * **max_target_duration** (`Optional`[`float`]) – The maximum total recording duration from `target_cuts`.

  * **max_cuts** (`Optional`[`int`]) – The maximum number of cuts sampled to form a mini-batch. By default, this constraint is off.

  * **shuffle** (`bool`) – When `True`, the cuts will be shuffled at the start of iteration. Convenient when mini-batch loop is inside an outer epoch-level loop, e.g.: for epoch in range(10): for batch in dataset: … as every epoch will see a different cuts order.

  * **drop_last** (`bool`) – When `True`, the last batch is dropped if it’s incomplete.

  * **world_size** (`Optional`[`int`]) – Total number of distributed nodes. We will try to infer it by default.

  * **rank** (`Optional`[`int`]) – Index of distributed node. We will try to infer it by default.

  * **seed** (`int`) – Random seed used to consistently shuffle the dataset across different processes.




_property _remaining_duration _: float | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.CutPairsSampler.remaining_duration "Permalink to this definition")
    

Remaining duration of data left in the sampler (may be inexact due to float arithmetic). Not available when the CutSet is read in lazy mode (returns None).

_property _remaining_cuts _: int | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.CutPairsSampler.remaining_cuts "Permalink to this definition")
    

Remaining number of cuts in the sampler. Not available when the CutSet is read in lazy mode (returns None).

_property _num_cuts _: int | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.CutPairsSampler.num_cuts "Permalink to this definition")
    

Total number of cuts in the sampler. Not available when the CutSet is read in lazy mode (returns None).

state_dict()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/cut_pairs.html#CutPairsSampler.state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.CutPairsSampler.state_dict "Permalink to this definition")
    

Return the current state of the sampler in a state_dict. Together with `load_state_dict()`, this can be used to restore the training loop’s state to the one stored in the state_dict.

Return type:
    

`Dict`[`str`, `Any`]

load_state_dict(_state_dict_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/cut_pairs.html#CutPairsSampler.load_state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.CutPairsSampler.load_state_dict "Permalink to this definition")
    

Restore the state of the sampler that is described in a state_dict. This will result in the sampler yielding batches from where the previous training left it off. :rtype: `None`

Caution

The samplers are expected to be initialized with the same CutSets, but this is not explicitly checked anywhere.

Caution

The input `state_dict` is being mutated: we remove each consumed key, and expect it to be empty at the end of loading. If you don’t want this behavior, pass a copy inside of this function (e.g., using `import deepcopy`).

Note

For implementers of sub-classes of CutSampler: the flag `self._just_restored_state` has to be handled in `__iter__` to make it avoid resetting the just-restored state (only once).

_class _lhotse.dataset.sampling.DynamicCutSampler(_* cuts_, _max_duration =None_, _max_cuts =None_, _constraint =None_, _shuffle =False_, _drop_last =False_, _consistent_ids =True_, _shuffle_buffer_size =20000_, _quadratic_duration =None_, _world_size =None_, _rank =None_, _seed =0_, _strict =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/dynamic.html#DynamicCutSampler)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicCutSampler "Permalink to this definition")
    

A dynamic (streaming) variant of sampler that doesn’t stratify the sampled cuts in any way. It is a generalization of [`SimpleCutSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SimpleCutSampler "lhotse.dataset.sampling.SimpleCutSampler") and [`CutPairsSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.CutPairsSampler "lhotse.dataset.sampling.CutPairsSampler") in that it allows to jointly iterate an arbitrary number of CutSets.

When input CutSets are opened in lazy mode, this sampler doesn’t require reading the whole cut set into memory.

For scenarios such as ASR, VAD, Speaker ID, or TTS training, this class supports single CutSet iteration. Example:
    
    
    >>> cuts = CutSet(...)
    >>> sampler = DynamicCutSampler(cuts, max_duration=100)
    >>> for batch in sampler:
    ...     assert isinstance(batch, CutSet)
    

For other scenarios that require pairs (or triplets, etc.) of utterances, this class supports zipping multiple CutSets together. Such scenarios could be voice conversion, speech translation, contrastive self-supervised training, etc. Example:
    
    
    >>> source_cuts = CutSet(...)
    >>> target_cuts = CutSet(...)
    >>> sampler = DynamicCutSampler(source_cuts, target_cuts, max_duration=100)
    >>> for batch in sampler:
    ...     assert isinstance(batch, tuple)
    ...     assert len(batch) == 2
    ...     assert isinstance(batch[0], CutSet)
    ...     assert isinstance(batch[1], CutSet)
    

Note

for cut pairs, triplets, etc. the user is responsible for ensuring that the CutSets are all sorted so that when iterated over sequentially, the items are matched. We take care of preserving the right ordering internally, e.g., when shuffling. By default, we check that the cut IDs are matching, but that can be disabled.

Caution

when using `DynamicCutSampler.filter()` to filter some cuts with more than one CutSet to sample from, we sample one cut from every CutSet, and expect that all of the cuts satisfy the predicate – otherwise, they are all discarded from being sampled.

__init__(_* cuts_, _max_duration =None_, _max_cuts =None_, _constraint =None_, _shuffle =False_, _drop_last =False_, _consistent_ids =True_, _shuffle_buffer_size =20000_, _quadratic_duration =None_, _world_size =None_, _rank =None_, _seed =0_, _strict =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/dynamic.html#DynamicCutSampler.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicCutSampler.__init__ "Permalink to this definition")
    

Parameters:
    

  * **cuts** (`Iterable`) – one or more CutSets (when more than one, will yield tuples of CutSets as mini-batches)

  * **max_duration** (`Optional`[`float`]) – The maximum total recording duration from `cuts`. Note: with multiple CutSets, `max_duration` constraint applies only to the first CutSet.

  * **max_cuts** (`Optional`[`int`]) – The maximum total number of `cuts` per batch. When only `max_duration` is specified, this sampler yields static batch sizes.

  * **constraint** (`Optional`[[`SamplingConstraint`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint "lhotse.dataset.sampling.base.SamplingConstraint")]) – Provide a [`SamplingConstraint`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.base.SamplingConstraint "lhotse.dataset.sampling.base.SamplingConstraint") object defining how the sampler decides when a mini-batch is complete. It also affects which attribute of the input examples decides the “size” of the example (by default it’s `.duration`). Before this parameter was introduced, Lhotse samplers used [`TimeConstraint`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.TimeConstraint "lhotse.dataset.sampling.base.TimeConstraint") implicitly. Introduced in Lhotse v1.22.0.

  * **shuffle** (`bool`) – When `True`, the cuts will be shuffled dynamically with a reservoir-sampling-based algorithm. Convenient when mini-batch loop is inside an outer epoch-level loop, e.g.: for epoch in range(10): for batch in dataset: … as every epoch will see a different cuts order.

  * **drop_last** (`bool`) – When `True`, we will drop all incomplete batches. A batch is considered incomplete if it depleted a bucket before hitting the constraint such as max_duration, max_cuts, etc.

  * **consistent_ids** (`bool`) – Only affects processing of multiple CutSets. When `True`, at each sampling step we check cuts from all CutSets have the same ID (i.e., the first cut from every CutSet should have the same ID, same for the second, third, etc.).

  * **shuffle_buffer_size** (`int`) – How many cuts (or cut pairs, triplets) are being held in memory a buffer used for streaming shuffling. Larger number means better randomness at the cost of higher memory usage.

  * **quadratic_duration** (`Optional`[`float`]) – When set, it adds an extra penalty that’s quadratic in size w.r.t. a cuts duration. This helps get a more even GPU utilization across different input lengths when models have quadratic input complexity. Set between 15 and 40 for transformers.

  * **world_size** (`Optional`[`int`]) – Total number of distributed nodes. We will try to infer it by default.

  * **rank** (`Optional`[`int`]) – Index of distributed node. We will try to infer it by default.

  * **seed** (`Union`[`int`, `Literal`[`'trng'`, `'randomized'`]]) – Random seed used to consistently shuffle the dataset across different processes.




state_dict()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/dynamic.html#DynamicCutSampler.state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicCutSampler.state_dict "Permalink to this definition")
    

Return the current state of the sampler in a state_dict. Together with `load_state_dict()`, this can be used to restore the training loop’s state to the one stored in the state_dict.

When possible, this also captures the state of the underlying CutSet iterator graph (via `lhotse.checkpoint.collect_state_dict()`), enabling O(1) restoration instead of O(N) fast-forwarding.

Return type:
    

`Dict`[`str`, `Any`]

load_state_dict(_sd_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/dynamic.html#DynamicCutSampler.load_state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicCutSampler.load_state_dict "Permalink to this definition")
    

Restore the state of the sampler that is described in a state_dict. This will result in the sampler yielding batches from where the previous training left it off. :rtype: `None`

Caution

The samplers are expected to be initialized with the same CutSets, but this is not explicitly checked anywhere.

Caution

The input `state_dict` is being mutated: we remove each consumed key, and expect it to be empty at the end of loading. If you don’t want this behavior, pass a copy inside of this function (e.g., using `import deepcopy`).

Note

For implementers of sub-classes of CutSampler: the flag `self._just_restored_state` has to be handled in `__iter__` to make it avoid resetting the just-restored state (only once).

_property _remaining_duration _: float | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicCutSampler.remaining_duration "Permalink to this definition")
    

Remaining duration of data left in the sampler (may be inexact due to float arithmetic). Not available when the CutSet is read in lazy mode (returns None).

_property _remaining_cuts _: int | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicCutSampler.remaining_cuts "Permalink to this definition")
    

Remaining number of cuts in the sampler. Not available when the CutSet is read in lazy mode (returns None).

_property _num_cuts _: int | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicCutSampler.num_cuts "Permalink to this definition")
    

Total number of cuts in the sampler. Not available when the CutSet is read in lazy mode (returns None).

_class _lhotse.dataset.sampling.DynamicBucketingSampler(_* cuts_, _max_duration =None_, _max_cuts =None_, _constraint =None_, _num_buckets =10_, _shuffle =False_, _drop_last =False_, _consistent_ids =True_, _duration_bins =None_, _num_cuts_for_bins_estimate =10000_, _buffer_size =20000_, _quadratic_duration =None_, _world_size =None_, _rank =None_, _seed =0_, _sync_buckets =True_, _concurrent =False_, _compact_state =False_, _strict =None_, _shuffle_buffer_size =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/dynamic_bucketing.html#DynamicBucketingSampler)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicBucketingSampler "Permalink to this definition")
    

A dynamic (streaming) variant of [`BucketingSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.BucketingSampler "lhotse.dataset.sampling.bucketing.BucketingSampler"), that doesn’t require reading the whole cut set into memory.

The basic idea is to sample N (e.g. ~10k) cuts and estimate the boundary durations for buckets. Then, we maintain a buffer of M cuts (stored separately in K buckets) and every time we sample a batch, we consume the input cut iterable for the same amount of cuts. The memory consumption is limited by M at all times.

For scenarios such as ASR, VAD, Speaker ID, or TTS training, this class supports single CutSet iteration. Example:
    
    
    >>> cuts = CutSet(...)
    >>> sampler = DynamicBucketingSampler(cuts, max_duration=100)
    >>> for batch in sampler:
    ...     assert isinstance(batch, CutSet)
    

For other scenarios that require pairs (or triplets, etc.) of utterances, this class supports zipping multiple CutSets together. Such scenarios could be voice conversion, speech translation, contrastive self-supervised training, etc. Example:
    
    
    >>> source_cuts = CutSet(...)
    >>> target_cuts = CutSet(...)
    >>> sampler = DynamicBucketingSampler(source_cuts, target_cuts, max_duration=100)
    >>> for batch in sampler:
    ...     assert isinstance(batch, tuple)
    ...     assert len(batch) == 2
    ...     assert isinstance(batch[0], CutSet)
    ...     assert isinstance(batch[1], CutSet)
    

Note

for cut pairs, triplets, etc. the user is responsible for ensuring that the CutSets are all sorted so that when iterated over sequentially, the items are matched. We take care of preserving the right ordering internally, e.g., when shuffling. By default, we check that the cut IDs are matching, but that can be disabled.

Caution

when using `DynamicBucketingSampler.filter()` to filter some cuts with more than one CutSet to sample from, we sample one cut from every CutSet, and expect that all of the cuts satisfy the predicate – otherwise, they are all discarded from being sampled.

__init__(_* cuts_, _max_duration =None_, _max_cuts =None_, _constraint =None_, _num_buckets =10_, _shuffle =False_, _drop_last =False_, _consistent_ids =True_, _duration_bins =None_, _num_cuts_for_bins_estimate =10000_, _buffer_size =20000_, _quadratic_duration =None_, _world_size =None_, _rank =None_, _seed =0_, _sync_buckets =True_, _concurrent =False_, _compact_state =False_, _strict =None_, _shuffle_buffer_size =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/dynamic_bucketing.html#DynamicBucketingSampler.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicBucketingSampler.__init__ "Permalink to this definition")
    

Parameters:
    

  * **cuts** (`Iterable`) – one or more CutSets (when more than one, will yield tuples of CutSets as mini-batches)

  * **max_duration** (`Optional`[`float`]) – The maximum total recording duration from `cuts`. Note: with multiple CutSets, `max_duration` constraint applies only to the first CutSet.

  * **max_cuts** (`Optional`[`int`]) – The maximum total number of `cuts` per batch. When only `max_duration` is specified, this sampler yields static batch sizes.

  * **num_buckets** (`Optional`[`int`]) – how many buckets to create. Ignored if duration_bins are provided.

  * **shuffle** (`bool`) – When `True`, the cuts will be shuffled dynamically with a reservoir-sampling-based algorithm. Convenient when mini-batch loop is inside an outer epoch-level loop, e.g.: for epoch in range(10): for batch in dataset: … as every epoch will see a different cuts order.

  * **drop_last** (`bool`) – When `True`, we will drop all incomplete batches. A batch is considered incomplete if it depleted a bucket before hitting the constraint such as max_duration, max_cuts, etc.

  * **consistent_ids** (`bool`) – Only affects processing of multiple CutSets. When `True`, at each sampling step we check cuts from all CutSets have the same ID (i.e., the first cut from every CutSet should have the same ID, same for the second, third, etc.).

  * **duration_bins** (`Optional`[`List`[`float`]]) – A list of floats (seconds); when provided, we’ll skip the initial estimation of bucket duration bins (useful to speed-up the launching of experiments).

  * **num_cuts_for_bins_estimate** (`int`) – We will draw this many cuts to estimate the duration bins for creating similar-duration buckets. Larger number means a better estimate to the data distribution, possibly at a longer init cost.

  * **buffer_size** (`int`) – How many cuts (or cut pairs, triplets) we hold at any time across all of the buckets. Increasing `max_duration` (batch_size) or `num_buckets` might require increasing this number. Larger number here will also improve shuffling capabilities. It will result in larger memory usage.

  * **quadratic_duration** (`Optional`[`float`]) – When set, it adds an extra penalty that’s quadratic in size w.r.t. a cuts duration. This helps get a more even GPU utilization across different input lengths when models have quadratic input complexity. Set between 15 and 40 for transformers.

  * **sync_buckets** (`bool`) – When set, we’ll try to make each DDP rank sample from as close duration buckets as possible to minimize the tail worker effect.

  * **concurrent** (`bool`) – Enabling concurrency eliminates most of the waiting to pre-populate the bucketing buffers before the sampler starts yielding examples. For tarred/Lhotse Shar data this can speed up the start of the training. Note that enabling concurrency will cause the sampling results to be non-deterministic. This feature is experimental.

  * **compact_state** (`bool`) – Store buffered graph tokens as immutable bytes instead of nested lists. This reduces object reconstruction and garbage collection in worker-to-parent snapshot transport. Tokens may be any pickle-compatible objects; only load checkpoints from trusted sources. Legacy checkpoints remain loadable; JSON checkpoint export expands the tokens to the legacy representation.

  * **world_size** (`Optional`[`int`]) – Total number of distributed nodes. We will try to infer it by default.

  * **rank** (`Optional`[`int`]) – Index of distributed node. We will try to infer it by default.

  * **seed** (`Union`[`int`, `Literal`[`'trng'`, `'randomized'`]]) – Random seed used to consistently shuffle the dataset across different processes.




state_dict()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/dynamic_bucketing.html#DynamicBucketingSampler.state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicBucketingSampler.state_dict "Permalink to this definition")
    

Return the current state of the sampler in a state_dict. Together with `load_state_dict()`, this can be used to restore the training loop’s state to the one stored in the state_dict.

When possible, this also captures the state of the underlying CutSet iterator graph (via `lhotse.checkpoint.collect_state_dict()`), enabling O(1) restoration instead of O(N) fast-forwarding.

Return type:
    

`Dict`[`str`, `Any`]

load_state_dict(_sd_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/dynamic_bucketing.html#DynamicBucketingSampler.load_state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicBucketingSampler.load_state_dict "Permalink to this definition")
    

Restore the state of the sampler that is described in a state_dict. This will result in the sampler yielding batches from where the previous training left it off. :rtype: `None`

Caution

The samplers are expected to be initialized with the same CutSets, but this is not explicitly checked anywhere.

Caution

The input `state_dict` is being mutated: we remove each consumed key, and expect it to be empty at the end of loading. If you don’t want this behavior, pass a copy inside of this function (e.g., using `import deepcopy`).

Note

For implementers of sub-classes of CutSampler: the flag `self._just_restored_state` has to be handled in `__iter__` to make it avoid resetting the just-restored state (only once).

_property _remaining_duration _: float | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicBucketingSampler.remaining_duration "Permalink to this definition")
    

Remaining duration of data left in the sampler (may be inexact due to float arithmetic). Not available when the CutSet is read in lazy mode (returns None).

_property _remaining_cuts _: int | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicBucketingSampler.remaining_cuts "Permalink to this definition")
    

Remaining number of cuts in the sampler. Not available when the CutSet is read in lazy mode (returns None).

_property _num_cuts _: int | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.DynamicBucketingSampler.num_cuts "Permalink to this definition")
    

Total number of cuts in the sampler. Not available when the CutSet is read in lazy mode (returns None).

_class _lhotse.dataset.sampling.RoundRobinSampler(_* samplers_, _stop_early =False_, _randomize =False_, _seed =0_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/round_robin.html#RoundRobinSampler)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler "Permalink to this definition")
    

[`RoundRobinSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler "lhotse.dataset.sampling.RoundRobinSampler") takes several samplers as input, and yields a mini-batch of cuts from each of those samplers in turn. E.g., with two samplers, the first mini-batch is from `sampler0`, the seconds from `sampler1`, the third from `sampler0`, and so on. It is helpful for alternating mini-batches from multiple datasets or manually creating batches of different sizes.

The input samplers do not have to provide the same number of batches – when any of the samplers becomes depleted, we continue to iterate the non-depleted samplers, until all of them are exhausted.

Example:
    
    
    >>> sampler = RoundRobinSampler(
    ...     SimpleCutSampler(cuts_corpusA, max_cuts=32, shuffle=True),
    ...     SimpleCutSampler(cuts_corpusB, max_cuts=64, shuffle=True),
    ... )
    >>> for cut in sampler:
    ...     pass  # profit
    

__init__(_* samplers_, _stop_early =False_, _randomize =False_, _seed =0_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/round_robin.html#RoundRobinSampler.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.__init__ "Permalink to this definition")
    

RoundRobinSampler’s constructor.

Parameters:
    

  * **samplers** (`CutSampler`) – The list of samplers from which we sample batches in turns.

  * **stop_early** (`bool`) – Should we finish the epoch once any of the samplers becomes depleted. By default, we will keep iterating until all the samplers are exhausted. This setting can be used to balance datasets of different sizes.

  * **randomize** (`Union`[`bool`, `List`[`float`]]) – Select the next sampler according to a distribution, instead of in order. If a list of floats is provided, it must contain the same number of elements as the number of samplers, and the values will be used as probabilities. If `True` is provided, the probabilities will be uniform. If `False` is provided, the samplers will be selected in order.

  * **seed** (`int`) – Random seed used to select the next sampler (only used if `randomize` is True)




_property _remaining_duration _: float | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.remaining_duration "Permalink to this definition")
    

Remaining duration of data left in the sampler (may be inexact due to float arithmetic).

_property _remaining_cuts _: int | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.remaining_cuts "Permalink to this definition")
    

Remaining number of cuts in the sampler. Not available when the CutSet is read in lazy mode (returns None).

_property _num_cuts _: int | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.num_cuts "Permalink to this definition")
    

Total number of cuts in the sampler. Not available when the CutSet is read in lazy mode (returns None).

allow_iter_to_reset_state()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/round_robin.html#RoundRobinSampler.allow_iter_to_reset_state)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.allow_iter_to_reset_state "Permalink to this definition")
    

Enables re-setting to the start of an epoch when iter() is called. This is only needed in one specific scenario: when we restored previous sampler state via `sampler.load_state_dict()` but want to discard the progress in the current epoch and start from the beginning.

state_dict()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/round_robin.html#RoundRobinSampler.state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.state_dict "Permalink to this definition")
    

Return the current state of the sampler in a state_dict. Together with `load_state_dict()`, this can be used to restore the training loop’s state to the one stored in the state_dict.

Return type:
    

`Dict`[`str`, `Any`]

load_state_dict(_state_dict_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/round_robin.html#RoundRobinSampler.load_state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.load_state_dict "Permalink to this definition")
    

Restore the state of the sampler that is described in a state_dict. This will result in the sampler yielding batches from where the previous training left it off. :rtype: `None`

Caution

The samplers are expected to be initialized with the same CutSets, but this is not explicitly checked anywhere.

Caution

The input `state_dict` is being mutated: we remove each consumed key, and expect it to be empty at the end of loading. If you don’t want this behavior, pass a copy inside of this function (e.g., using `import deepcopy`).

Note

For implementers of sub-classes of CutSampler: the flag `self._just_restored_state` has to be handled in `__iter__` to make it avoid resetting the just-restored state (only once).

set_epoch(_epoch_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/round_robin.html#RoundRobinSampler.set_epoch)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.set_epoch "Permalink to this definition")
    

Sets the epoch for this sampler. When `shuffle=True`, this ensures all replicas use a different random ordering for each epoch. Otherwise, the next iteration of this sampler will yield the same ordering.

Parameters:
    

**epoch** (`int`) – Epoch number.

Return type:
    

`None`

filter(_predicate_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/round_robin.html#RoundRobinSampler.filter)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.filter "Permalink to this definition")
    

Add a constraint on individual cuts that has to be satisfied to consider them.

Can be useful when handling large, lazy manifests where it is not feasible to pre-filter them before instantiating the sampler.

Return type:
    

`None`

Example:
    
    
    
    >>> cuts = CutSet(...)
    ... sampler = SimpleCutSampler(cuts, max_duration=100.0)
    ... # Retain only the cuts that have at least 1s and at most 20s duration.
    ... sampler.filter(lambda cut: 1.0 <= cut.duration <= 20.0)
    

_property _diagnostics _: [SamplingDiagnostics](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics "lhotse.dataset.sampling.base.SamplingDiagnostics")_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.diagnostics "Permalink to this definition")
    

Info on how many cuts / batches were returned or rejected during iteration.

This property can be overriden by child classes e.g. to merge diagnostics of composite samplers.

get_report()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/round_robin.html#RoundRobinSampler.get_report)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.RoundRobinSampler.get_report "Permalink to this definition")
    

Returns a string describing the statistics of the sampling process so far.

Return type:
    

`str`

_class _lhotse.dataset.sampling.SimpleCutSampler(_cuts_ , _max_duration =None_, _max_cuts =None_, _shuffle =False_, _drop_last =False_, _concatenate_cuts =False_, _world_size =None_, _rank =None_, _seed =0_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/simple.html#SimpleCutSampler)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SimpleCutSampler "Permalink to this definition")
    

Samples cuts from a CutSet to satisfy the input constraints. It behaves like an iterable that yields lists of strings (cut IDs).

When one of `max_duration`, or `max_cuts` is specified, the batch size is dynamic. Exactly zero or one of those constraints can be specified. Padding required to collate the batch does not contribute to max duration.

Example usage:
    
    
    >>> dataset = K2SpeechRecognitionDataset(cuts)
    >>> sampler = SimpleCutSampler(cuts, shuffle=True)
    >>> loader = DataLoader(dataset, sampler=sampler, batch_size=None)
    >>> for epoch in range(start_epoch, n_epochs):
    ...     sampler.set_epoch(epoch)
    ...     train(loader)
    

__init__(_cuts_ , _max_duration =None_, _max_cuts =None_, _shuffle =False_, _drop_last =False_, _concatenate_cuts =False_, _world_size =None_, _rank =None_, _seed =0_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/simple.html#SimpleCutSampler.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SimpleCutSampler.__init__ "Permalink to this definition")
    

SimpleCutSampler’s constructor.

Parameters:
    

  * **cuts** ([`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")) – the `CutSet` to sample data from.

  * **max_duration** (`Optional`[`float`]) – The maximum total recording duration from `cuts`.

  * **max_cuts** (`Optional`[`int`]) – The maximum number of cuts sampled to form a mini-batch. By default, this constraint is off.

  * **shuffle** (`bool`) – When `True`, the cuts will be shuffled at the start of iteration. Convenient when mini-batch loop is inside an outer epoch-level loop, e.g.: for epoch in range(10): for batch in dataset: … as every epoch will see a different cuts order.

  * **drop_last** (`bool`) – When `True`, the last batch is dropped if it’s incomplete.

  * **world_size** (`Optional`[`int`]) – Total number of distributed nodes. We will try to infer it by default.

  * **rank** (`Optional`[`int`]) – Index of distributed node. We will try to infer it by default.

  * **seed** (`int`) – Random seed used to consistently shuffle the dataset across different processes.




_property _remaining_duration _: float | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SimpleCutSampler.remaining_duration "Permalink to this definition")
    

Remaining duration of data left in the sampler (may be inexact due to float arithmetic). Not available when the CutSet is read in lazy mode (returns None).

_property _remaining_cuts _: int | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SimpleCutSampler.remaining_cuts "Permalink to this definition")
    

Remaining number of cuts in the sampler. Not available when the CutSet is read in lazy mode (returns None).

_property _num_cuts _: int | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SimpleCutSampler.num_cuts "Permalink to this definition")
    

Total number of cuts in the sampler. Not available when the CutSet is read in lazy mode (returns None).

state_dict()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/simple.html#SimpleCutSampler.state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SimpleCutSampler.state_dict "Permalink to this definition")
    

Return the current state of the sampler in a state_dict. Together with `load_state_dict()`, this can be used to restore the training loop’s state to the one stored in the state_dict.

Return type:
    

`Dict`[`str`, `Any`]

load_state_dict(_state_dict_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/simple.html#SimpleCutSampler.load_state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SimpleCutSampler.load_state_dict "Permalink to this definition")
    

Restore the state of the sampler that is described in a state_dict. This will result in the sampler yielding batches from where the previous training left it off. :rtype: `None`

Caution

The samplers are expected to be initialized with the same CutSets, but this is not explicitly checked anywhere.

Caution

The input `state_dict` is being mutated: we remove each consumed key, and expect it to be empty at the end of loading. If you don’t want this behavior, pass a copy inside of this function (e.g., using `import deepcopy`).

Note

For implementers of sub-classes of CutSampler: the flag `self._just_restored_state` has to be handled in `__iter__` to make it avoid resetting the just-restored state (only once).

_class _lhotse.dataset.sampling.WeightedSimpleCutSampler(_cuts_ , _cuts_weight_ , _num_samples_ , _max_duration =None_, _max_cuts =None_, _shuffle =False_, _drop_last =False_, _world_size =None_, _rank =None_, _seed =0_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/weighted_simple.html#WeightedSimpleCutSampler)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.WeightedSimpleCutSampler "Permalink to this definition")
    

Samples cuts from a CutSet, where the sampling prob is given by a list. To enable global sampling, cuts must be in eager mode.

When performing sampling, it avoids having duplicated cuts in the same batch. The sampler terminates if the number of sampled cuts reach `num_samples`

When one of `max_duration`, or `max_cuts` is specified, the batch size is dynamic.

Example usage:
    
    
    >>> dataset = K2SpeechRecognitionDataset(cuts)
    >>> weights = get_weights(cuts)
    >>> sampler = WeightedSimpleCutSampler(cuts, weights, num_samples=100, max_duration=200.0)
    >>> loader = DataLoader(dataset, sampler=sampler, batch_size=None)
    >>> for epoch in range(start_epoch, n_epochs):
    ...     sampler.set_epoch(epoch)
    ...     train(loader)
    

__init__(_cuts_ , _cuts_weight_ , _num_samples_ , _max_duration =None_, _max_cuts =None_, _shuffle =False_, _drop_last =False_, _world_size =None_, _rank =None_, _seed =0_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/weighted_simple.html#WeightedSimpleCutSampler.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.WeightedSimpleCutSampler.__init__ "Permalink to this definition")
    

WeightedSimpleCutSampler’s constructor

Parameters:
    

  * **cuts** ([`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")) – the `CutSet` to sample data from.

  * **cuts_weight** (`List`) – the weight of each cut for sampling.

  * **num_samples** (`int`) – the number of samples to be drawn.

  * **max_duration** (`Optional`[`float`]) – The maximum total recording duration from `cuts`.

  * **max_cuts** (`Optional`[`int`]) – The maximum number of cuts sampled to form a mini-batch. By default, this constraint is off.

  * **shuffle** (`bool`) – When `True`, the cuts will be shuffled at the start of iteration. Convenient when mini-batch loop is inside an outer epoch-level loop, e.g.: for epoch in range(10): for batch in dataset: … as every epoch will see a different cuts order.

  * **drop_last** (`bool`) – When `True`, the last batch is dropped if it’s incomplete.

  * **world_size** (`Optional`[`int`]) – Total number of distributed nodes. We will try to infer it by default.

  * **rank** (`Optional`[`int`]) – Index of distributed node. We will try to infer it by default.

  * **seed** (`int`) – Random seed used to consistently shuffle the dataset across different processes.




state_dict()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/weighted_simple.html#WeightedSimpleCutSampler.state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.WeightedSimpleCutSampler.state_dict "Permalink to this definition")
    

Return the current state of the sampler in a state_dict. Together with `load_state_dict()`, this can be used to restore the training loop’s state to the one stored in the state_dict.

Return type:
    

`Dict`[`str`, `Any`]

load_state_dict(_state_dict_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/weighted_simple.html#WeightedSimpleCutSampler.load_state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.WeightedSimpleCutSampler.load_state_dict "Permalink to this definition")
    

Restore the state of the sampler that is described in a state_dict. This will result in the sampler yielding batches from where the previous training left it off. :rtype: `None`

Caution

The samplers are expected to be initialized with the same CutSets, but this is not explicitly checked anywhere.

Caution

The input `state_dict` is being mutated: we remove each consumed key, and expect it to be empty at the end of loading. If you don’t want this behavior, pass a copy inside of this function (e.g., using `import deepcopy`).

Note

For implementers of sub-classes of CutSampler: the flag `self._just_restored_state` has to be handled in `__iter__` to make it avoid resetting the just-restored state (only once).

_class _lhotse.dataset.sampling.StatelessSampler(_cuts_paths_ , _index_path_ , _base_seed_ , _max_duration =None_, _max_cuts =None_, _num_buckets =None_, _duration_bins =None_, _quadratic_duration =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/stateless.html#StatelessSampler)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.StatelessSampler "Permalink to this definition")
    

An infinite and stateless cut sampler that selects data at random from one or more cut manifests. The main idea is to make training resumption easy while guaranteeing the data seen each time by the model is shuffled differently. It discards the notion of an “epoch” and it never finishes iteration. It makes no strong guarantees about avoiding data duplication, but in practice you would rarely see duplicated data.

The recommended way to use this sampler is by placing it into a dataloader worker subprocess with Lhotse’s :class:`~lhotse.dataset.iterable_dataset.IterableDatasetWrapper`, so that each worker has its own sampler replica that uses a slightly different random seed:
    
    
    >>> import torch
    >>> import lhotse
    >>> dloader = torch.utils.data.DataLoader(
    ...     lhotse.dataset.iterable_dataset.IterableDatasetWrapper(
    ...         dataset=lhotse.dataset.K2SpeechRecognitionDataset(...),
    ...         sampler=StatelessSampler(...),
    ...     ),
    ...     batch_size=None,
    ...     num_workers=4,
    ... )
    

This sampler’s design was originally proposed by Dan Povey. For details see: <https://github.com/lhotse-speech/lhotse/issues/1096>

Example 1: Get a non-bucketing :class:`.StatelessSampler`:
    
    
    >>> sampler = StatelessSampler(
    ...     cuts_paths=["data/cuts_a.jsonl", "data/cuts_b.jsonl"],
    ...     index_path="data/files.idx",
    ...     max_duration=600.0,
    ... )
    

Example 2: Get a bucketing :class:`.StatelessSampler`:
    
    
    >>> sampler = StatelessSampler(
    ...     cuts_paths=["data/cuts_a.jsonl", "data/cuts_b.jsonl"],
    ...     index_path="data/files.idx",
    ...     max_duration=600.0,
    ...     num_buckets=50,
    ...     quadratic_duration=30.0,
    ... )
    

Example 3: Get a bucketing :class:`.StatelessSampler` with scaled weights for each cutset:
    
    
    >>> sampler = StatelessSampler(
    ...     cuts_paths=[
    ...         ("data/cuts_a.jsonl", 2.0),
    ...         ("data/cuts_b.jsonl", 1.0),
    ...     ],
    ...     index_path="data/files.idx",
    ...     max_duration=600.0,
    ...     num_buckets=50,
    ...     quadratic_duration=30.0,
    ... )
    

Note

This sampler works only with uncompressed jsonl manifests, as it creates extra index files with line byte offsets to quickly find and sample JSON lines. This means this sampler will not work with Webdataset and Lhotse Shar data format.

Parameters:
    

  * **cuts_paths** (`Union`[`Path`, `str`, `Iterable`[`Union`[`Path`, `str`]], `Iterable`[`Tuple`[`Union`[`Path`, `str`], `float`]]]) – Path, or list of paths, or list of tuples of (path, scale) to cutset files.

  * **index_path** (`Union`[`Path`, `str`]) – Path to a file that contains the index of all cutsets and their line count (will be auto-created the first time this object is initialized).

  * **base_seed** (`int`) – Int, user-provided part of the seed used to initialize the RNG for sampling (each node and worker are still going to produce different results). When continuing the training it should be a function of the number of training steps to ensure the model doesn’t see identical mini-batches again.

  * **max_duration** (`Optional`[`float`]) – Maximum total number of audio seconds in a mini-batch (dynamic batch size).

  * **max_cuts** (`Optional`[`int`]) – Maximum number of examples in a mini-batch (static batch size).

  * **num_buckets** (`Optional`[`int`]) – If set, enables bucketing (each mini-batch has examples of a similar duration).

  * **duration_bins** (`Optional`[`List`[`float`]]) – A list of floats (seconds); when provided, we’ll skip the initial estimation of bucket duration bins (useful to speed-up the launching of experiments).

  * **quadratic_duration** (`Optional`[`float`]) – If set, adds a penalty term for longer duration cuts. Works well with models that have quadratic time complexity to keep GPU utilization similar when using bucketing. Suggested values are between 30 and 45.




__init__(_cuts_paths_ , _index_path_ , _base_seed_ , _max_duration =None_, _max_cuts =None_, _num_buckets =None_, _duration_bins =None_, _quadratic_duration =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/stateless.html#StatelessSampler.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.StatelessSampler.__init__ "Permalink to this definition")
    

map(_fn_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/stateless.html#StatelessSampler.map)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.StatelessSampler.map "Permalink to this definition")
    

Apply `fn` to each mini-batch of `CutSet` before yielding it.

Return type:
    

[`StatelessSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.StatelessSampler "lhotse.dataset.sampling.stateless.StatelessSampler")

state_dict()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/stateless.html#StatelessSampler.state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.StatelessSampler.state_dict "Permalink to this definition")
    

Stub state_dict method that returns nothing - this sampler is stateless.

Return type:
    

`Dict`

load_state_dict(_state_dict_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/stateless.html#StatelessSampler.load_state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.StatelessSampler.load_state_dict "Permalink to this definition")
    

Stub load_state_dict method that does nothing - this sampler is stateless.

Return type:
    

`None`

get_report()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/stateless.html#StatelessSampler.get_report)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.StatelessSampler.get_report "Permalink to this definition")
    

Returns a string describing the statistics of the sampling process so far.

Return type:
    

`str`

_class _lhotse.dataset.sampling.ZipSampler(_* samplers_, _merge_batches =True_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/zip.html#ZipSampler)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler "Permalink to this definition")
    

[`ZipSampler`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler "lhotse.dataset.sampling.ZipSampler") takes several samplers as input and concatenates their sampled mini-batch cuts together into a single [`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.CutSet"), or returns a tuple of the mini-batch CutSets. It is helpful for ensuring that each batch consists of some proportion of cuts coming from different sources.

The input samplers do not have to provide the same number of batches – when any of the samplers becomes depleted, the iteration will stop (like with Python’s `zip()` function).

Example:
    
    
    >>> sampler = ZipSampler(
    ...     SimpleCutSampler(cuts_corpusA, max_duration=250, shuffle=True),
    ...     SimpleCutSampler(cuts_corpusB, max_duration=100, shuffle=True),
    ... )
    >>> for cut in sampler:
    ...     pass  # profit
    

__init__(_* samplers_, _merge_batches =True_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/zip.html#ZipSampler.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.__init__ "Permalink to this definition")
    

ZipSampler’s constructor.

Parameters:
    

  * **samplers** (`CutSampler`) – The list of samplers from which we sample batches together.

  * **merge_batches** (`bool`) – Should we merge the batches from each sampler into a single CutSet, or return a tuple of CutSets. Setting this to `False` makes ZipSampler behave more like Python’s `zip` function.




_property _remaining_duration _: float | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.remaining_duration "Permalink to this definition")
    

Remaining duration of data left in the sampler (may be inexact due to float arithmetic).

_property _remaining_cuts _: int | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.remaining_cuts "Permalink to this definition")
    

Remaining number of cuts in the sampler. Not available when the CutSet is read in lazy mode (returns None).

_property _num_cuts _: int | None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.num_cuts "Permalink to this definition")
    

Total number of cuts in the sampler. Not available when the CutSet is read in lazy mode (returns None).

allow_iter_to_reset_state()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/zip.html#ZipSampler.allow_iter_to_reset_state)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.allow_iter_to_reset_state "Permalink to this definition")
    

Enables re-setting to the start of an epoch when iter() is called. This is only needed in one specific scenario: when we restored previous sampler state via `sampler.load_state_dict()` but want to discard the progress in the current epoch and start from the beginning.

state_dict()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/zip.html#ZipSampler.state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.state_dict "Permalink to this definition")
    

Return the current state of the sampler in a state_dict. Together with `load_state_dict()`, this can be used to restore the training loop’s state to the one stored in the state_dict.

Return type:
    

`Dict`[`str`, `Any`]

load_state_dict(_state_dict_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/zip.html#ZipSampler.load_state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.load_state_dict "Permalink to this definition")
    

Restore the state of the sampler that is described in a state_dict. This will result in the sampler yielding batches from where the previous training left it off. :rtype: `None`

Caution

The samplers are expected to be initialized with the same CutSets, but this is not explicitly checked anywhere.

Caution

The input `state_dict` is being mutated: we remove each consumed key, and expect it to be empty at the end of loading. If you don’t want this behavior, pass a copy inside of this function (e.g., using `import deepcopy`).

Note

For implementers of sub-classes of CutSampler: the flag `self._just_restored_state` has to be handled in `__iter__` to make it avoid resetting the just-restored state (only once).

set_epoch(_epoch_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/zip.html#ZipSampler.set_epoch)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.set_epoch "Permalink to this definition")
    

Sets the epoch for this sampler. When `shuffle=True`, this ensures all replicas use a different random ordering for each epoch. Otherwise, the next iteration of this sampler will yield the same ordering.

Parameters:
    

**epoch** (`int`) – Epoch number.

Return type:
    

`None`

filter(_predicate_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/zip.html#ZipSampler.filter)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.filter "Permalink to this definition")
    

Add a constraint on individual cuts that has to be satisfied to consider them.

Can be useful when handling large, lazy manifests where it is not feasible to pre-filter them before instantiating the sampler.

Return type:
    

`None`

Example:
    
    
    
    >>> cuts = CutSet(...)
    ... sampler = SimpleCutSampler(cuts, max_duration=100.0)
    ... # Retain only the cuts that have at least 1s and at most 20s duration.
    ... sampler.filter(lambda cut: 1.0 <= cut.duration <= 20.0)
    

_property _diagnostics _: [SamplingDiagnostics](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.SamplingDiagnostics "lhotse.dataset.sampling.base.SamplingDiagnostics")_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.diagnostics "Permalink to this definition")
    

Info on how many cuts / batches were returned or rejected during iteration.

This property can be overriden by child classes e.g. to merge diagnostics of composite samplers.

get_report()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/zip.html#ZipSampler.get_report)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.ZipSampler.get_report "Permalink to this definition")
    

Returns a string describing the statistics of the sampling process so far.

Return type:
    

`str`

lhotse.dataset.sampling.find_pessimistic_batches(_sampler_ , _batch_tuple_index =0_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/utils.html#find_pessimistic_batches)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.find_pessimistic_batches "Permalink to this definition")
    

Function for finding ‘pessimistic’ batches, i.e. batches that have the highest potential to blow up the GPU memory during training. We will fully iterate the sampler and record the most risky batches under several criteria: \- single longest cut \- single longest supervision \- largest batch cuts duration \- largest batch supervisions duration \- max num cuts \- max num supervisions

Example of how this function can be used with a PyTorch model and a `K2SpeechRecognitionDataset`:
    
    
    sampler = SimpleCutSampler(cuts, max_duration=300)
    dataset = K2SpeechRecognitionDataset()
    batches, scores = find_pessimistic_batches(sampler)
    for reason, cuts in batches.items():
        try:
            batch = dset[cuts]
            outputs = model(batch)
            loss = loss_fn(outputs)
            loss.backward()
        except:
            print(f"Exception caught when evaluating pessimistic batch for: {reason}={scores[reason]}")
            raise
    

Parameters:
    

  * **sampler** (`CutSampler`) – An instance of a Lhotse `CutSampler`.

  * **batch_tuple_index** (`int`) – Applicable to samplers that return tuples of [`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.CutSet"). Indicates which position in the tuple we should look up for the CutSet.



Return type:
    

`Tuple`[`Dict`[`str`, [`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")], `Dict`[`str`, `float`]]

Returns:
    

A tuple of dicts: the first with batches (as CutSets) and the other with criteria values, i.e.: `({"<criterion>": <CutSet>, ...}, {"<criterion>": <value>, ...})`

lhotse.dataset.sampling.report_padding_ratio_estimate(_sampler_ , _n_samples =1000_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/sampling/utils.html#report_padding_ratio_estimate)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.sampling.report_padding_ratio_estimate "Permalink to this definition")
    

Returns a human-readable string message about amount of padding diagnostics. Assumes that padding corresponds to segments without any supervision within cuts.

Return type:
    

`str`

## Input strategies’ list[](https://lhotse.readthedocs.io/en/latest/datasets.html#module-lhotse.dataset.input_strategies "Permalink to this heading")

_class _lhotse.dataset.input_strategies.BatchIO(_num_workers=0_ , _executor_type= <class 'concurrent.futures.thread.ThreadPoolExecutor'>_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/input_strategies.html#BatchIO)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.BatchIO "Permalink to this definition")
    

Converts a `CutSet` into a collated batch of audio representations. These representations can be e.g. audio samples or features. They might also be single or multi channel.

All InputStrategies support the `executor` parameter in the constructor. It allows to pass a `ThreadPoolExecutor` or a `ProcessPoolExecutor` to parallelize reading audio/features from wherever they are stored. Note that this approach is incompatible with specifying the `num_workers` to `torch.utils.data.DataLoader`, but in some instances may be faster.

Note

This is a base class that only defines the interface.

__call__(_cuts_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/input_strategies.html#BatchIO.__call__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.BatchIO.__call__ "Permalink to this definition")
    

Returns a tensor with collated input signals, and a tensor of length of each signal before padding.

Return type:
    

`Tuple`[`Tensor`, `IntTensor`]

__init__(_num_workers=0_ , _executor_type= <class 'concurrent.futures.thread.ThreadPoolExecutor'>_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/input_strategies.html#BatchIO.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.BatchIO.__init__ "Permalink to this definition")
    

supervision_intervals(_cuts_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/input_strategies.html#BatchIO.supervision_intervals)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.BatchIO.supervision_intervals "Permalink to this definition")
    

Returns a dict that specifies the start and end bounds for each supervision, as a 1-D int tensor.

Depending on the strategy, the dict should look like:
    
    
    {
        "sequence_idx": tensor(shape=(S,)),
        "start_frame": tensor(shape=(S,)),
        "num_frames": tensor(shape=(S,)),
    }
    

or
    
    
    {
        "sequence_idx": tensor(shape=(S,)),
        "start_sample": tensor(shape=(S,)),
        "num_samples": tensor(shape=(S,))
    }
    

Where `S` is the total number of supervisions encountered in the `CutSet`. Note that `S` might be different than the number of cuts (`B`). `sequence_idx` means the index of the corresponding feature matrix (or cut) in a batch.

Return type:
    

`Dict`[`str`, `Tensor`]

supervision_masks(_cuts_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/input_strategies.html#BatchIO.supervision_masks)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.BatchIO.supervision_masks "Permalink to this definition")
    

Returns a collated batch of masks, marking the supervised regions in cuts. They are zero-padded to the longest cut.

Depending on the strategy implementation, it is expected to be a tensor of shape `(B, NF)` or `(B, NS)`, where `B` denotes the number of cuts, `NF` the number of frames and `NS` the total number of samples. `NF` and `NS` are determined by the longest cut in a batch.

Return type:
    

`Tensor`

_class _lhotse.dataset.input_strategies.PrecomputedFeatures(_num_workers=0_ , _executor_type= <class 'concurrent.futures.thread.ThreadPoolExecutor'>_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/input_strategies.html#PrecomputedFeatures)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.PrecomputedFeatures "Permalink to this definition")
    

`InputStrategy` that reads pre-computed features, whose manifests are attached to cuts, from disk.

It automatically pads the feature matrices so that every example has the same number of frames as the longest cut in a mini-batch. This is needed to put all examples into a single tensor. The padding value is a low log-energy, around log(1e-10).

__call__(_cuts_ , _pad_direction ='right'_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/input_strategies.html#PrecomputedFeatures.__call__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.PrecomputedFeatures.__call__ "Permalink to this definition")
    

Reads the pre-computed features from disk/other storage. The returned shape is `(B, T, F) => (batch_size, num_frames, num_features)`.

Return type:
    

`Tuple`[`Tensor`, `Tensor`]

Returns:
    

a tensor with collated features, and a tensor of `num_frames` of each cut before padding.

supervision_intervals(_cuts_ , _pad_direction ='right'_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/input_strategies.html#PrecomputedFeatures.supervision_intervals)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.PrecomputedFeatures.supervision_intervals "Permalink to this definition")
    

Returns a dict that specifies the start and end bounds for each supervision, as a 1-D int tensor, in terms of frames:
    
    
    {
        "sequence_idx": tensor(shape=(S,)),
        "start_frame": tensor(shape=(S,)),
        "num_frames": tensor(shape=(S,))
    }
    

Where `S` is the total number of supervisions encountered in the `CutSet`. Note that `S` might be different than the number of cuts (`B`). `sequence_idx` means the index of the corresponding feature matrix (or cut) in a batch.

Return type:
    

`Dict`[`str`, `Tensor`]

supervision_masks(_cuts_ , _use_alignment_if_exists =None_, _pad_direction ='right'_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/input_strategies.html#PrecomputedFeatures.supervision_masks)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.PrecomputedFeatures.supervision_masks "Permalink to this definition")
    

Returns the mask for supervised frames.

Parameters:
    

  * **use_alignment_if_exists** (`Optional`[`str`]) – optional str, key for alignment type to use for generating the mask. If not exists, fall back on supervision time spans.

  * **pad_direction** (`Optional`[`str`]) – where to apply the padding (`right` or `left`).



Return type:
    

`Tensor`

_class _lhotse.dataset.input_strategies.AudioSamples(_num_workers=0_ , _fault_tolerant=False_ , _executor_type= <class 'concurrent.futures.thread.ThreadPoolExecutor'>_, _use_batch_loader=False_ , _ais_force_individual=False_ , _mono_downmix=None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/input_strategies.html#AudioSamples)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.AudioSamples "Permalink to this definition")
    

`InputStrategy` that reads single-channel recordings, whose manifests are attached to cuts, from disk (or other audio source).

It automatically zero-pads the recordings so that every example has the same number of audio samples as the longest cut in a mini-batch. This is needed to put all examples into a single tensor.

__call__(_cuts_ , _recording_field =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/input_strategies.html#AudioSamples.__call__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.AudioSamples.__call__ "Permalink to this definition")
    

Reads the audio samples from recordings on disk/other storage. The returned shape is `(B, T) => (batch_size, num_samples)`.

Parameters:
    

**recording_field** (`Optional`[`str`]) – when specified, we will try to load recordings from a custom field with this name (i.e., `cut.load_<recording_field>()` instead of default `cut.load_audio()`).

Return type:
    

`Union`[`Tuple`[`Tensor`, `Tensor`], `Tuple`[`Tensor`, `Tensor`, [`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")]]

Returns:
    

a tensor with collated audio samples, and a tensor of `num_samples` of each cut before padding.

Note

When AIStore batch loading is enabled (use_batch_loader=True), the audio data will be fetched from AIStore using a single batch request before collation. The input CutSet must be eager (not lazy).

__init__(_num_workers=0_ , _fault_tolerant=False_ , _executor_type= <class 'concurrent.futures.thread.ThreadPoolExecutor'>_, _use_batch_loader=False_ , _ais_force_individual=False_ , _mono_downmix=None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/input_strategies.html#AudioSamples.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.AudioSamples.__init__ "Permalink to this definition")
    

AudioSamples constructor.

Parameters:
    

  * **num_workers** (`int`) – when larger than 0, we will spawn an executor (of type specified by `executor_type`) to read the audio data in parallel. Thread executor can be used with PyTorch’s DataLoader, whereas Process executor would fail (but could be faster for other applications).

  * **fault_tolerant** (`bool`) – when `True`, the cuts for which audio loading failed will be skipped. It will make `__call__` return an additional item, which is the CutSet for which we successfully read the audio. It may be a subset of the input CutSet. When `use_batch_loader=True`, this also propagates to `AISBatchLoader` so per-object AIS fetch failures (404, refused, etc.) drop the corresponding cut instead of raising.

  * **executor_type** (`Type`[`TypeVar`(`ExecutorType`, bound= `Executor`)]) – the type of executor used for parallel audio reads (only relevant when `num_workers>0`).

  * **use_batch_loader** (`bool`) – When `True`, enables batch loading of audio data from AIStore. This allows all audio samples in the batch to be fetched in a single request for increased efficiency. Requires the input CutSet to be eager (not lazy).

  * **ais_force_individual** (`bool`) – only meaningful when `use_batch_loader=True`. When `True`, the underlying `AISBatchLoader` skips the MOSS GetBatch attempt and issues one `Object.get_reader().read_all()` per object instead — useful when the AIStore deployment doesn’t support GetBatch or its performance is degraded for the access pattern.

  * **mono_downmix** (`Optional`[`bool`]) – controls channel handling (passed to `collate_audio()`). `None` (default): auto-detect — downmix unless every cut is multichannel. `True`: always downmix to mono; output shape is `(B, T)`. `False`: expand mono to channel 0 with zero-padded channels; output shape is `(B, C, T)`.




supervision_intervals(_cuts_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/input_strategies.html#AudioSamples.supervision_intervals)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.AudioSamples.supervision_intervals "Permalink to this definition")
    

Returns a dict that specifies the start and end bounds for each supervision, as a 1-D int tensor, in terms of samples:
    
    
    {
        "sequence_idx": tensor(shape=(S,)),
        "start_sample": tensor(shape=(S,)),
        "num_samples": tensor(shape=(S,))
    }
    

Where `S` is the total number of supervisions encountered in the `CutSet`. Note that `S` might be different than the number of cuts (`B`). `sequence_idx` means the index of the corresponding feature matrix (or cut) in a batch.

Return type:
    

`Dict`[`str`, `Tensor`]

supervision_masks(_cuts_ , _use_alignment_if_exists =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/input_strategies.html#AudioSamples.supervision_masks)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.AudioSamples.supervision_masks "Permalink to this definition")
    

Returns the mask for supervised samples.

Parameters:
    

**use_alignment_if_exists** (`Optional`[`str`]) – optional str, key for alignment type to use for generating the mask. If not exists, fall back on supervision time spans.

Return type:
    

`Tensor`

_class _lhotse.dataset.input_strategies.OnTheFlyFeatures(_extractor_ , _wave_transforms=None_ , _num_workers=0_ , _use_batch_extract=True_ , _fault_tolerant=False_ , _return_audio=False_ , _executor_type= <class 'concurrent.futures.thread.ThreadPoolExecutor'>_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/input_strategies.html#OnTheFlyFeatures)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.OnTheFlyFeatures "Permalink to this definition")
    

`InputStrategy` that reads single-channel recordings, whose manifests are attached to cuts, from disk (or other audio source). Then, it uses a `FeatureExtractor` to compute their features on-the-fly.

It automatically pads the feature matrices so that every example has the same number of frames as the longest cut in a mini-batch. This is needed to put all examples into a single tensor. The padding value is a low log-energy, around log(1e-10).

__call__(_cuts_ , _recording_field =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/input_strategies.html#OnTheFlyFeatures.__call__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.OnTheFlyFeatures.__call__ "Permalink to this definition")
    

Reads the audio samples from recordings on disk/other storage and computes their features. The returned shape is `(B, T, F) => (batch_size, num_frames, num_features)`.

Parameters:
    

**recording_field** (`Optional`[`str`]) – when specified, we will try to load recordings from a custom field with this name (i.e., `cut.load_<recording_field>()` instead of default `cut.load_audio()`).

Return type:
    

`Union`[`Tuple`[`Tensor`, `Tensor`], `Tuple`[`Tensor`, `Tensor`, [`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")]]

Returns:
    

a tuple of objcets: `(feats, feat_lens, [audios, audio_lens], [cuts])`. Tensors `audios` and `audio_lens` are returned when `return_audio=True`. CutSet `cuts` is returned when `fault_tolerant=True`.

__init__(_extractor_ , _wave_transforms=None_ , _num_workers=0_ , _use_batch_extract=True_ , _fault_tolerant=False_ , _return_audio=False_ , _executor_type= <class 'concurrent.futures.thread.ThreadPoolExecutor'>_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/input_strategies.html#OnTheFlyFeatures.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.OnTheFlyFeatures.__init__ "Permalink to this definition")
    

OnTheFlyFeatures’ constructor.

Parameters:
    

  * **extractor** ([`FeatureExtractor`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.features.base.FeatureExtractor "lhotse.features.base.FeatureExtractor")) – the feature extractor used on-the-fly (individually on each waveform).

  * **wave_transforms** (`Optional`[`List`[`Callable`[[`Tensor`], `Tensor`]]]) – an optional list of transforms applied on the batch of audio waveforms collated into a single tensor, right before the feature extraction.

  * **num_workers** (`int`) – when larger than 0, we will spawn an executor (of type specified by `executor_type`) to read the audio data in parallel. Thread executor can be used with PyTorch’s DataLoader, whereas Process executor would fail (but could be faster for other applications).

  * **use_batch_extract** (`bool`) – when `True`, we will call [`extract_batch()`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.features.base.FeatureExtractor.extract_batch "lhotse.features.base.FeatureExtractor.extract_batch") to compute the features as it is possibly faster. It has a restriction that all cuts must have the same sampling rate. If that is not the case, set this to `False`.

  * **fault_tolerant** (`bool`) – when `True`, the cuts for which audio loading failed will be skipped. It will make `__call__` return an additional item, which is the CutSet for which we successfully read the audio. It may be a subset of the input CutSet.

  * **return_audio** (`bool`) – When `True`, calling this object will additionally return collated audio tensor and audio lengths tensor.

  * **executor_type** (`Type`[`TypeVar`(`ExecutorType`, bound= `Executor`)]) – the type of executor used for parallel audio reads (only relevant when `num_workers>0`).




supervision_intervals(_cuts_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/input_strategies.html#OnTheFlyFeatures.supervision_intervals)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.OnTheFlyFeatures.supervision_intervals "Permalink to this definition")
    

Returns a dict that specifies the start and end bounds for each supervision, as a 1-D int tensor, in terms of frames:
    
    
    {
        "sequence_idx": tensor(shape=(S,)),
        "start_frame": tensor(shape=(S,)),
        "num_frames": tensor(shape=(S,))
    }
    

Where `S` is the total number of supervisions encountered in the `CutSet`. Note that `S` might be different than the number of cuts (`B`). `sequence_idx` means the index of the corresponding feature matrix (or cut) in a batch.

Return type:
    

`Dict`[`str`, `Tensor`]

supervision_masks(_cuts_ , _use_alignment_if_exists =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/input_strategies.html#OnTheFlyFeatures.supervision_masks)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.input_strategies.OnTheFlyFeatures.supervision_masks "Permalink to this definition")
    

Returns the mask for supervised samples.

Parameters:
    

**use_alignment_if_exists** (`Optional`[`str`]) – optional str, key for alignment type to use for generating the mask. If not exists, fall back on supervision time spans.

Return type:
    

`Tensor`

## Augmentation - transforms on cuts[](https://lhotse.readthedocs.io/en/latest/datasets.html#augmentation-transforms-on-cuts "Permalink to this heading")

Some transforms, in order for us to have accurate information about the start and end times of the signal and its supervisions, have to be performed on cuts (or CutSets).

_class _lhotse.dataset.cut_transforms.CutConcatenate(_gap =1.0_, _duration_factor =1.0_, _max_duration =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/concatenate.html#CutConcatenate)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.CutConcatenate "Permalink to this definition")
    

A transform on batch of cuts (`CutSet`) that concatenates the cuts to minimize the total amount of padding; e.g. instead of creating a batch with 40 examples, we will merge some of the examples together adding some silence between them to avoid a large number of padding frames that waste the computation.

__init__(_gap =1.0_, _duration_factor =1.0_, _max_duration =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/concatenate.html#CutConcatenate.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.CutConcatenate.__init__ "Permalink to this definition")
    

CutConcatenate’s constructor.

Parameters:
    

  * **gap** (`float`) – The duration of silence in seconds that is inserted between the cuts; it’s goal is to let the model “know” that there are separate utterances in a single example.

  * **duration_factor** (`float`) – Determines the maximum duration of the concatenated cuts; by default it’s 1, setting the limit at the duration of the longest cut in the batch.

  * **max_duration** (`Optional`[`float`]) – If a value is given (in seconds), the maximum duration of concatenated cuts is fixed to the value while duration_factor is ignored.




_class _lhotse.dataset.cut_transforms.CutMix(_cuts_ , _snr =(10, 20)_, _p =0.5_, _pad_to_longest =True_, _preserve_id =False_, _seed =42_, _random_mix_offset =False_, _tag =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/mix.html#CutMix)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.CutMix "Permalink to this definition")
    

A transform for batches of cuts (CutSet’s) that stochastically performs noise augmentation with a constant or varying SNR.

__init__(_cuts_ , _snr =(10, 20)_, _p =0.5_, _pad_to_longest =True_, _preserve_id =False_, _seed =42_, _random_mix_offset =False_, _tag =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/mix.html#CutMix.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.CutMix.__init__ "Permalink to this definition")
    

CutMix’s constructor.

Parameters:
    

  * **cuts** ([`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")) – a `CutSet` containing augmentation data, e.g. noise, music, babble.

  * **snr** (`Union`[`float`, `Tuple`[`float`, `float`], `None`]) – either a float, a pair (range) of floats, or `None`. It determines the SNR of the speech signal vs the noise signal that’s mixed into it. When a range is specified, we will uniformly sample SNR in that range. When it’s `None`, the noise will be mixed as-is – i.e. without any level adjustment. Note that it’s different from `snr=0`, which will adjust the noise level so that the SNR is 0.

  * **pad_to_longest** (`bool`) – when True, each processed `CutSet` will be padded with noise to match the duration of the longest Cut in a batch.

  * **preserve_id** (`bool`) – When `True`, preserves the IDs the cuts had before augmentation. Otherwise, new random IDs are generated for the augmented cuts (default).

  * **seed** (`Union`[`int`, `Literal`[`'trng'`, `'randomized'`], `Random`]) – an optional int or “trng”. Random seed for choosing the cuts to mix and the SNR. If “trng” is provided, we’ll use the `secrets` module for non-deterministic results on each iteration. You can also directly pass a `random.Random` instance here.

  * **random_mix_offset** (`bool`) – an optional bool. When `True` and the duration of the to be mixed in cut in longer than the original cut, select a random sub-region from the to be mixed in cut.

  * **tag** (`Optional`[`str`]) – Optional label attached to the mixed-in tracks.




state_dict()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/mix.html#CutMix.state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.CutMix.state_dict "Permalink to this definition")
    

Return type:
    

`dict`

load_state_dict(_sd_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/mix.html#CutMix.load_state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.CutMix.load_state_dict "Permalink to this definition")
    

Return type:
    

`None`

_class _lhotse.dataset.cut_transforms.ExtraPadding(_extra_frames =None_, _extra_samples =None_, _extra_seconds =None_, _pad_feat_value =-23.025850929940457_, _randomized =False_, _preserve_id =False_, _direction ='both'_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/extra_padding.html#ExtraPadding)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ExtraPadding "Permalink to this definition")
    

A transform on batch of cuts (`CutSet`) that adds a number of extra context frames/samples/seconds on both sides of the cut. Exactly one type of duration has to specified in the constructor.

It is intended mainly for training frame-synchronous ASR models with convolutional layers to avoid using padding inside of the hidden layers, by giving the model larger context in the input. Another useful application is to shift the input by a little, so that the data seen after frame subsampling is a bit different, which makes this a data augmentation technique.

This is best used as the first transform in the transform list for dataset - it will ensure that each individual cut gets extra context before concatenation, or that it will be filled with noise, etc.

__init__(_extra_frames =None_, _extra_samples =None_, _extra_seconds =None_, _pad_feat_value =-23.025850929940457_, _randomized =False_, _preserve_id =False_, _direction ='both'_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/extra_padding.html#ExtraPadding.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ExtraPadding.__init__ "Permalink to this definition")
    

ExtraPadding’s constructor.

Parameters:
    

  * **extra_frames** (`Optional`[`int`]) – The total number of frames to add to each cut. We will add half that number on each side of the cut (“both” directions padding).

  * **extra_samples** (`Optional`[`int`]) – The total number of samples to add to each cut. We will add half that number on each side of the cut (“both” directions padding).

  * **extra_seconds** (`Optional`[`float`]) – The total duration in seconds to add to each cut. We will add half that number on each side of the cut (“both” directions padding).

  * **pad_feat_value** (`float`) – When padding a cut with precomputed features, what value should be used for padding (the default is a very low log-energy).

  * **randomized** (`bool`) – When `True`, we will sample a value from a uniform distribution of `[0, extra_X]` for each cut (for samples/frames – sample an int, for duration – sample a float).

  * **preserve_id** (`bool`) – When `True`, preserves the IDs the cuts had before augmentation. Otherwise, new random IDs are generated for the augmented cuts (default).

  * **direction** (`str`) – The padding direction.




_class _lhotse.dataset.cut_transforms.LowpassUsingResampling(_p =0.5_, _frequencies_interval =(3500, 8000)_, _seed =42_, _rng =None_, _preserve_id =False_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/lowpass.html#LowpassUsingResampling)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.LowpassUsingResampling "Permalink to this definition")
    

Applies a low-pass filter to each Cut in a CutSet by resampling the audio back and forth.

p _: `float`_ _ = 0.5_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.LowpassUsingResampling.p "Permalink to this definition")
    

frequencies_interval _: `Tuple`[`float`, `float`]__ = (3500, 8000)_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.LowpassUsingResampling.frequencies_interval "Permalink to this definition")
    

seed _: `Union`[`int`, `Literal`[`'trng'`, `'randomized'`]]__ = 42_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.LowpassUsingResampling.seed "Permalink to this definition")
    

rng _: `Optional`[`Random`]__ = None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.LowpassUsingResampling.rng "Permalink to this definition")
    

preserve_id _: `bool`_ _ = False_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.LowpassUsingResampling.preserve_id "Permalink to this definition")
    

state_dict()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/lowpass.html#LowpassUsingResampling.state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.LowpassUsingResampling.state_dict "Permalink to this definition")
    

Return type:
    

`dict`

load_state_dict(_sd_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/lowpass.html#LowpassUsingResampling.load_state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.LowpassUsingResampling.load_state_dict "Permalink to this definition")
    

Return type:
    

`None`

__init__(_p =0.5_, _frequencies_interval =(3500, 8000)_, _seed =42_, _rng =None_, _preserve_id =False_)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.LowpassUsingResampling.__init__ "Permalink to this definition")
    

_class _lhotse.dataset.cut_transforms.PerturbSpeed(_factors_ , _p_ , _randgen =None_, _preserve_id =False_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/perturb_speed.html#PerturbSpeed)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbSpeed "Permalink to this definition")
    

A transform on batch of cuts (`CutSet`) that perturbs the speed of the recordings with a given probability `p`.

If the effect is applied, then one of the perturbation factors from the constructor’s `factors` parameter is sampled with uniform probability.

__init__(_factors_ , _p_ , _randgen =None_, _preserve_id =False_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/perturb_speed.html#PerturbSpeed.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbSpeed.__init__ "Permalink to this definition")
    

state_dict()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/perturb_speed.html#PerturbSpeed.state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbSpeed.state_dict "Permalink to this definition")
    

Return type:
    

`dict`

load_state_dict(_sd_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/perturb_speed.html#PerturbSpeed.load_state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbSpeed.load_state_dict "Permalink to this definition")
    

Return type:
    

`None`

_class _lhotse.dataset.cut_transforms.PerturbTempo(_factors_ , _p_ , _randgen =None_, _preserve_id =False_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/perturb_tempo.html#PerturbTempo)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbTempo "Permalink to this definition")
    

A transform on batch of cuts (`CutSet`) that perturbs the tempo of the recordings with a given probability `p`.

If the effect is applied, then one of the perturbation factors from the constructor’s `factors` parameter is sampled with uniform probability.

__init__(_factors_ , _p_ , _randgen =None_, _preserve_id =False_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/perturb_tempo.html#PerturbTempo.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbTempo.__init__ "Permalink to this definition")
    

state_dict()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/perturb_tempo.html#PerturbTempo.state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbTempo.state_dict "Permalink to this definition")
    

Return type:
    

`dict`

load_state_dict(_sd_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/perturb_tempo.html#PerturbTempo.load_state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbTempo.load_state_dict "Permalink to this definition")
    

Return type:
    

`None`

_class _lhotse.dataset.cut_transforms.PerturbVolume(_p_ , _scale_low =0.125_, _scale_high =2.0_, _randgen =None_, _preserve_id =False_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/perturb_volume.html#PerturbVolume)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbVolume "Permalink to this definition")
    

A transform on batch of cuts (`CutSet`) that perturbs the volume of the recordings with a given probability `p`.

If the effect is applied, then one of the perturbation factors from the constructor’s `factors` parameter is sampled with uniform probability.

__init__(_p_ , _scale_low =0.125_, _scale_high =2.0_, _randgen =None_, _preserve_id =False_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/perturb_volume.html#PerturbVolume.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbVolume.__init__ "Permalink to this definition")
    

state_dict()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/perturb_volume.html#PerturbVolume.state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbVolume.state_dict "Permalink to this definition")
    

Return type:
    

`dict`

load_state_dict(_sd_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/perturb_volume.html#PerturbVolume.load_state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.PerturbVolume.load_state_dict "Permalink to this definition")
    

Return type:
    

`None`

_class _lhotse.dataset.cut_transforms.ReverbWithImpulseResponse(_rir_recordings =None_, _p =0.5_, _normalize_output =True_, _randgen =None_, _preserve_id =False_, _early_only =False_, _rir_channels =[0]_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/reverberate.html#ReverbWithImpulseResponse)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ReverbWithImpulseResponse "Permalink to this definition")
    

A transform on batch of cuts (`CutSet`) that convolves each cut with an impulse response with some probability `p`. The impulse response is chosen randomly from a specified CutSet of RIRs `rir_cuts`. If no RIRs are specified, we will generate them using a fast random generator (<https://arxiv.org/abs/2208.04101>). If early_only is set to True, convolution is performed only with the first 50ms of the impulse response.

__init__(_rir_recordings =None_, _p =0.5_, _normalize_output =True_, _randgen =None_, _preserve_id =False_, _early_only =False_, _rir_channels =[0]_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/reverberate.html#ReverbWithImpulseResponse.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ReverbWithImpulseResponse.__init__ "Permalink to this definition")
    

state_dict()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/reverberate.html#ReverbWithImpulseResponse.state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ReverbWithImpulseResponse.state_dict "Permalink to this definition")
    

Return type:
    

`dict`

load_state_dict(_sd_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/reverberate.html#ReverbWithImpulseResponse.load_state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ReverbWithImpulseResponse.load_state_dict "Permalink to this definition")
    

Return type:
    

`None`

_class _lhotse.dataset.cut_transforms.Compress(_codecs_ , _compression_level =0.9_, _codec_weights =None_, _compress_custom_fields =False_, _p =0.5_, _seed =42_, _rng =None_, _preserve_id =False_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/compress.html#Compress)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress "Permalink to this definition")
    

Applies a lossy compression algorithm filter to each Cut in a CutSet. The audio is decompressed back to raw waveforms.

The compression is applied with a probability of `p`. The codec is randomly selected the list of provided codecs, with optional weights controlling the selection. If compression level is provided as an interval, then the actual value is sampled uniformly from the provided interval.

Parameters:
    

  * **codecs** (`List`[`Literal`[`'opus'`, `'mp3'`, `'vorbis'`, `'gsm'`]]) – A list of codecs (supported: “opus”, “mp3”, “vorbis”, “gsm”)

  * **compression_level** (`Union`[`float`, `Tuple`[`float`, `float`]]) – A single value or an interval. 0.0 = lowest compression (highest bitrate), 1.0 = highest compression (lowest bitrate). If an interval is provided, the value is sampled uniformly.

  * **codec_weights** (`Optional`[`List`[`float`]]) – Optional weights for each codec (default: equal weights).

  * **p** (`float`) – The probability of applying the low-pass filter (default: 0.5).

  * **randgen** – An optional random number generator (default: a new instance).

  * **preserve_id** (`bool`) – Whether to preserve the original cut ID (default: False).




codecs _: `List`[`Literal`[`'opus'`, `'mp3'`, `'vorbis'`, `'gsm'`]]_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.codecs "Permalink to this definition")
    

compression_level _: `Union`[`float`, `Tuple`[`float`, `float`]]__ = 0.9_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.compression_level "Permalink to this definition")
    

codec_weights _: `Optional`[`List`[`float`]]__ = None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.codec_weights "Permalink to this definition")
    

compress_custom_fields _: `bool`_ _ = False_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.compress_custom_fields "Permalink to this definition")
    

p _: `float`_ _ = 0.5_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.p "Permalink to this definition")
    

seed _: `Union`[`int`, `Literal`[`'trng'`, `'randomized'`]]__ = 42_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.seed "Permalink to this definition")
    

rng _: `Optional`[`Random`]__ = None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.rng "Permalink to this definition")
    

preserve_id _: `bool`_ _ = False_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.preserve_id "Permalink to this definition")
    

state_dict()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/compress.html#Compress.state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.state_dict "Permalink to this definition")
    

Return type:
    

`dict`

load_state_dict(_sd_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/compress.html#Compress.load_state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.load_state_dict "Permalink to this definition")
    

Return type:
    

`None`

__init__(_codecs_ , _compression_level =0.9_, _codec_weights =None_, _compress_custom_fields =False_, _p =0.5_, _seed =42_, _rng =None_, _preserve_id =False_)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.Compress.__init__ "Permalink to this definition")
    

_class _lhotse.dataset.cut_transforms.ClippingTransform(_gain_db_ , _normalize =True_, _p =0.5_, _p_hard =0.5_, _seed =42_, _rng =None_, _oversampling =2_, _preserve_id =False_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/clipping.html#ClippingTransform)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform "Permalink to this definition")
    

Applies clipping to each Cut in a CutSet with a given probability.

The clipping is applied with a probability of `p`. The gain_db is randomly sampled from the provided range if an interval is given, or the fixed value is used if a single float is provided.

Parameters:
    

  * **gain_db** (`Union`[`float`, `Tuple`[`float`, `float`]]) – A single value or an interval (tuple/list with two values). The amount of gain in decibels to apply before clipping. If an interval is provided, the value is sampled uniformly.

  * **hard** – If True, apply hard clipping (sharp cutoff); otherwise, apply soft clipping (saturation).

  * **normalize** (`bool`) – If True, normalize the input signal to 0 dBFS before applying clipping.

  * **p** (`float`) – The probability of applying clipping (default: 0.5).

  * **seed** (`Union`[`int`, `Literal`[`'trng'`, `'randomized'`]]) – Random seed for reproducibility (default: 42).

  * **rng** (`Optional`[`Random`]) – Optional random number generator (overrides seed if provided).

  * **oversampling** (`Optional`[`int`]) – Optional integer factor for oversampling before clipping.

  * **preserve_id** (`bool`) – Whether to preserve the original cut ID (default: False).




gain_db _: `Union`[`float`, `Tuple`[`float`, `float`]]_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.gain_db "Permalink to this definition")
    

normalize _: `bool`_ _ = True_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.normalize "Permalink to this definition")
    

p _: `float`_ _ = 0.5_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.p "Permalink to this definition")
    

p_hard _: `float`_ _ = 0.5_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.p_hard "Permalink to this definition")
    

seed _: `Union`[`int`, `Literal`[`'trng'`, `'randomized'`]]__ = 42_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.seed "Permalink to this definition")
    

rng _: `Optional`[`Random`]__ = None_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.rng "Permalink to this definition")
    

oversampling _: `Optional`[`int`]__ = 2_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.oversampling "Permalink to this definition")
    

preserve_id _: `bool`_ _ = False_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.preserve_id "Permalink to this definition")
    

state_dict()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/clipping.html#ClippingTransform.state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.state_dict "Permalink to this definition")
    

Return type:
    

`dict`

load_state_dict(_sd_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/cut_transforms/clipping.html#ClippingTransform.load_state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.load_state_dict "Permalink to this definition")
    

Return type:
    

`None`

__init__(_gain_db_ , _normalize =True_, _p =0.5_, _p_hard =0.5_, _seed =42_, _rng =None_, _oversampling =2_, _preserve_id =False_)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.cut_transforms.ClippingTransform.__init__ "Permalink to this definition")
    

## Augmentation - transforms on signals[](https://lhotse.readthedocs.io/en/latest/datasets.html#augmentation-transforms-on-signals "Permalink to this heading")

These transforms work directly on batches of collated feature matrices (or possibly raw waveforms, if applicable).

_class _lhotse.dataset.signal_transforms.GlobalMVN(_feature_dim_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/signal_transforms.html#GlobalMVN)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.GlobalMVN "Permalink to this definition")
    

Apply global mean and variance normalization

__init__(_feature_dim_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/signal_transforms.html#GlobalMVN.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.GlobalMVN.__init__ "Permalink to this definition")
    

Initialize internal Module state, shared by both nn.Module and ScriptModule.

_classmethod _from_cuts(_cuts_ , _max_cuts =None_, _extractor =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/signal_transforms.html#GlobalMVN.from_cuts)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.GlobalMVN.from_cuts "Permalink to this definition")
    

Return type:
    

[`GlobalMVN`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.GlobalMVN "lhotse.dataset.signal_transforms.GlobalMVN")

_classmethod _from_file(_stats_file_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/signal_transforms.html#GlobalMVN.from_file)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.GlobalMVN.from_file "Permalink to this definition")
    

Return type:
    

[`GlobalMVN`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.GlobalMVN "lhotse.dataset.signal_transforms.GlobalMVN")

to_file(_stats_file_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/signal_transforms.html#GlobalMVN.to_file)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.GlobalMVN.to_file "Permalink to this definition")
    

forward(_features_ , _supervision_segments =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/signal_transforms.html#GlobalMVN.forward)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.GlobalMVN.forward "Permalink to this definition")
    

Define the computation performed at every call.

Should be overridden by all subclasses. :rtype: `Tensor`

Note

Although the recipe for forward pass needs to be defined within this function, one should call the `Module` instance afterwards instead of this since the former takes care of running the registered hooks while the latter silently ignores them.

inverse(_features_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/signal_transforms.html#GlobalMVN.inverse)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.GlobalMVN.inverse "Permalink to this definition")
    

Return type:
    

`Tensor`

_class _lhotse.dataset.signal_transforms.SpecAugment(_time_warp_factor =80_, _num_feature_masks =2_, _features_mask_size =27_, _num_frame_masks =10_, _frames_mask_size =100_, _max_frames_mask_fraction =0.15_, _p =0.9_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/signal_transforms.html#SpecAugment)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.SpecAugment "Permalink to this definition")
    

SpecAugment performs three augmentations: \- time warping of the feature matrix \- masking of ranges of features (frequency bands) \- masking of ranges of frames (time)

The current implementation works with batches, but processes each example separately in a loop rather than simultaneously to achieve different augmentation parameters for each example.

__init__(_time_warp_factor =80_, _num_feature_masks =2_, _features_mask_size =27_, _num_frame_masks =10_, _frames_mask_size =100_, _max_frames_mask_fraction =0.15_, _p =0.9_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/signal_transforms.html#SpecAugment.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.SpecAugment.__init__ "Permalink to this definition")
    

SpecAugment’s constructor.

Parameters:
    

  * **time_warp_factor** (`Optional`[`int`]) – parameter for the time warping; larger values mean more warping. Set to `None`, or less than `1`, to disable.

  * **num_feature_masks** (`int`) – how many feature masks should be applied. Set to `0` to disable.

  * **features_mask_size** (`int`) – the width of the feature mask (expressed in the number of masked feature bins). This is the `F` parameter from the SpecAugment paper.

  * **num_frame_masks** (`int`) – the number of masking regions for utterances. Set to `0` to disable.

  * **frames_mask_size** (`int`) – the width of the frame (temporal) masks (expressed in the number of masked frames). This is the `T` parameter from the SpecAugment paper.

  * **max_frames_mask_fraction** (`float`) – limits the size of the frame (temporal) mask to this value times the length of the utterance (or supervision segment). This is the parameter denoted by `p` in the SpecAugment paper.

  * **p** – the probability of applying this transform. It is different from `p` in the SpecAugment paper!




forward(_features_ , _supervision_segments =None_, _* args_, _** kwargs_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/signal_transforms.html#SpecAugment.forward)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.SpecAugment.forward "Permalink to this definition")
    

Computes SpecAugment for a batch of feature matrices.

Since the batch will usually already be padded, the user can optionally provide a `supervision_segments` tensor that will be used to apply SpecAugment only to selected areas of the input. The format of this input is described below.

Parameters:
    

  * **features** (`Tensor`) – a batch of feature matrices with shape `(B, T, F)`.

  * **supervision_segments** (`Optional`[`IntTensor`]) – an int tensor of shape `(S, 3)`. `S` is the number of supervision segments that exist in `features` – there may be either less or more than the batch size. The second dimension encoder three kinds of information: the sequence index of the corresponding feature matrix in features, the start frame index, and the number of frames for each segment.



Return type:
    

`Tensor`

Returns:
    

an augmented tensor of shape `(B, T, F)`.

state_dict(_** kwargs_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/signal_transforms.html#SpecAugment.state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.SpecAugment.state_dict "Permalink to this definition")
    

Return a dictionary containing references to the whole state of the module.

Both parameters and persistent buffers (e.g. running averages) are included. Keys are corresponding parameter and buffer names. Parameters and buffers set to `None` are not included. :rtype: `Dict`[`str`, `Any`]

Note

The returned object is a shallow copy. It contains references to the module’s parameters and buffers.

Warning

Currently `state_dict()` also accepts positional arguments for `destination`, `prefix` and `keep_vars` in order. However, this is being deprecated and keyword arguments will be enforced in future releases.

Warning

Please avoid the use of argument `destination` as it is not designed for end-users.

Args:
    

destination (dict, optional): If provided, the state of module will
    

be updated into the dict and the same object is returned. Otherwise, an `OrderedDict` will be created and returned. Default: `None`.

prefix (str, optional): a prefix added to parameter and buffer
    

names to compose the keys in state_dict. Default: `''`.

keep_vars (bool, optional): by default the `Tensor` s
    

returned in the state dict are detached from autograd. If it’s set to `True`, detaching will not be performed. Default: `False`.

Returns:
    

dict:
    

a dictionary containing a whole state of the module

Example:
    
    
    >>> # xdoctest: +SKIP("undefined vars")
    >>> module.state_dict().keys()
    ['bias', 'weight']
    

load_state_dict(_state_dict_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/signal_transforms.html#SpecAugment.load_state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.SpecAugment.load_state_dict "Permalink to this definition")
    

Copy parameters and buffers from [`state_dict`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.SpecAugment.state_dict "lhotse.dataset.signal_transforms.SpecAugment.state_dict") into this module and its descendants.

If `strict` is `True`, then the keys of [`state_dict`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.SpecAugment.state_dict "lhotse.dataset.signal_transforms.SpecAugment.state_dict") must exactly match the keys returned by this module’s `state_dict()` function.

Warning

If `assign` is `True` the optimizer must be created after the call to [`load_state_dict`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.SpecAugment.load_state_dict "lhotse.dataset.signal_transforms.SpecAugment.load_state_dict") unless `get_swap_module_params_on_conversion()` is `True`.

Args:
    

state_dict (dict): a dict containing parameters and
    

persistent buffers.

strict (bool, optional): whether to strictly enforce that the keys
    

in [`state_dict`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.SpecAugment.state_dict "lhotse.dataset.signal_transforms.SpecAugment.state_dict") match the keys returned by this module’s `state_dict()` function. Default: `True`

assign (bool, optional): When set to `False`, the properties of the tensors
    

in the current module are preserved whereas setting it to `True` preserves properties of the Tensors in the state dict. The only exception is the `requires_grad` field of `Parameter` for which the value from the module is preserved. Default: `False`

Returns:
    

`NamedTuple` with `missing_keys` and `unexpected_keys` fields:
    

  * `missing_keys` is a list of str containing any keys that are expected
    

by this module but missing from the provided `state_dict`.

  * `unexpected_keys` is a list of str containing the keys that are not
    

expected by this module but present in the provided `state_dict`.



Note:
    

If a parameter or buffer is registered as `None` and its corresponding key exists in [`state_dict`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.SpecAugment.state_dict "lhotse.dataset.signal_transforms.SpecAugment.state_dict"), [`load_state_dict()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.SpecAugment.load_state_dict "lhotse.dataset.signal_transforms.SpecAugment.load_state_dict") will raise a `RuntimeError`.

_class _lhotse.dataset.signal_transforms.RandomizedSmoothing(_sigma =0.1_, _sample_sigma =True_, _p =0.3_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/signal_transforms.html#RandomizedSmoothing)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.RandomizedSmoothing "Permalink to this definition")
    

Randomized smoothing - gaussian noise added to an input waveform, or a batch of waveforms. The summed audio is clipped to `[-1.0, 1.0]` before returning.

__init__(_sigma =0.1_, _sample_sigma =True_, _p =0.3_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/signal_transforms.html#RandomizedSmoothing.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.RandomizedSmoothing.__init__ "Permalink to this definition")
    

RandomizedSmoothing’s constructor.

Parameters:
    

  * **sigma** (`Union`[`float`, `Sequence`[`Tuple`[`int`, `float`]]]) – standard deviation of the gaussian noise. Either a constant float, or a schedule, i.e. a list of tuples that specify which value to use from which step. For example, `[(0, 0.01), (1000, 0.1)]` means that from steps 0-999, the sigma value will be 0.01, and from step 1000 onwards, it will be 0.1.

  * **sample_sigma** (`bool`) – when `False`, then sigma is used as the standard deviation in each forward step. When `True`, the standard deviation is sampled from a uniform distribution of `[-sigma, sigma]` for each forward step.

  * **p** (`float`) – the probability of applying this transform.




forward(_audio_ , _* args_, _** kwargs_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/signal_transforms.html#RandomizedSmoothing.forward)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.RandomizedSmoothing.forward "Permalink to this definition")
    

Define the computation performed at every call.

Should be overridden by all subclasses. :rtype: `Tensor`

Note

Although the recipe for forward pass needs to be defined within this function, one should call the `Module` instance afterwards instead of this since the former takes care of running the registered hooks while the latter silently ignores them.

_class _lhotse.dataset.signal_transforms.DereverbWPE(_n_fft =512_, _hop_length =128_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/signal_transforms.html#DereverbWPE)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.DereverbWPE "Permalink to this definition")
    

Dereverberation with Weighted Prediction Error (WPE). The implementation and default values are borrowed from nara_wpe package: <https://github.com/fgnt/nara_wpe>

The method and library are described in the following paper: <https://groups.uni-paderborn.de/nt/pubs/2018/ITG_2018_Drude_Paper.pdf>

__init__(_n_fft =512_, _hop_length =128_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/signal_transforms.html#DereverbWPE.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.DereverbWPE.__init__ "Permalink to this definition")
    

Initialize internal Module state, shared by both nn.Module and ScriptModule.

forward(_audio_ , _* args_, _** kwargs_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/signal_transforms.html#DereverbWPE.forward)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.signal_transforms.DereverbWPE.forward "Permalink to this definition")
    

Expects audio to be 2D or 3D tensor. 2D means a batch of single-channel audio, shape (B, T). 3D means a batch of multi-channel audio, shape (B, D, T). B => batch size; D => number of channels; T => number of audio samples.

Return type:
    

`Tensor`

## Collation utilities for building custom Datasets[](https://lhotse.readthedocs.io/en/latest/datasets.html#module-lhotse.dataset.collation "Permalink to this heading")

_class _lhotse.dataset.collation.TokenCollater(_cuts_ , _add_eos =True_, _add_bos =True_, _pad_symbol ='<pad>'_, _bos_symbol ='<bos>'_, _eos_symbol ='<eos>'_, _unk_symbol ='<unk>'_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/collation.html#TokenCollater)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.TokenCollater "Permalink to this definition")
    

Collate list of tokens

Map sentences to integers. Sentences are padded to equal length. Beginning and end-of-sequence symbols can be added. Call .inverse(tokens_batch, tokens_lens) to reconstruct batch as string sentences.

Example:
    
    
    
    >>> token_collater = TokenCollater(cuts)
    >>> tokens_batch, tokens_lens = token_collater(cuts.subset(first=32))
    >>> original_sentences = token_collater.inverse(tokens_batch, tokens_lens)
    

Returns:
    

tokens_batch: IntTensor of shape (B, L)
    

B: batch dimension, number of input sentences L: length of the longest sentence

tokens_lens: IntTensor of shape (B,)
    

Length of each sentence after adding <eos> and <bos> but before padding.

__init__(_cuts_ , _add_eos =True_, _add_bos =True_, _pad_symbol ='<pad>'_, _bos_symbol ='<bos>'_, _eos_symbol ='<eos>'_, _unk_symbol ='<unk>'_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/collation.html#TokenCollater.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.TokenCollater.__init__ "Permalink to this definition")
    

inverse(_tokens_batch_ , _tokens_lens_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/collation.html#TokenCollater.inverse)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.TokenCollater.inverse "Permalink to this definition")
    

Return type:
    

`List`[`str`]

lhotse.dataset.collation.collate_features(_cuts_ , _pad_direction ='right'_, _executor =None_, _features_dtype =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/collation.html#collate_features)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.collate_features "Permalink to this definition")
    

Load features for all the cuts and return them as a batch in a torch tensor. The output shape is `(batch, time, features)`. The cuts will be padded with silence if necessary.

Parameters:
    

  * **cuts** ([`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")) – a `CutSet` used to load the features.

  * **pad_direction** (`str`) – where to apply the padding (`right`, `left`, or `both`).

  * **executor** (`Optional`[`Executor`]) – an instance of ThreadPoolExecutor or ProcessPoolExecutor; when provided, we will use it to read the features concurrently.



Return type:
    

`Tuple`[`Tensor`, `Tensor`]

Returns:
    

a tuple of tensors `(features, features_lens)`.

lhotse.dataset.collation.collate_audio(_cuts_ , _pad_direction ='right'_, _executor =None_, _fault_tolerant =False_, _recording_field =None_, _mono_downmix =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/collation.html#collate_audio)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.collate_audio "Permalink to this definition")
    

Load audio samples for all the cuts and return them as a batch in a torch tensor. The output shape is `(batch, time)` or `(batch, channels, time)`. The cuts will be padded with silence if necessary.

Parameters:
    

  * **cuts** ([`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")) – a `CutSet` used to load the audio samples.

  * **pad_direction** (`str`) – where to apply the padding (`right`, `left`, or `both`).

  * **executor** (`Optional`[`Executor`]) – an instance of ThreadPoolExecutor or ProcessPoolExecutor; when provided, we will use it to read audio concurrently.

  * **fault_tolerant** (`bool`) – when `True`, the cuts for which audio loading failed will be skipped. Setting this parameter will cause the function to return a 3-tuple, where the third element is a CutSet for which the audio data were sucessfully read.

  * **recording_field** (`Optional`[`str`]) – when specified, we will try to load recordings from a custom field with this name (i.e., `cut.load_<recording_field>()` instead of default `cut.load_audio()`).

  * **mono_downmix** (`Optional`[`bool`]) – controls channel handling. `None` (default): auto-detect — uses downmix semantics unless every cut in the batch is multichannel, in which case multichannel collation is used. `True`: multichannel audio is downmixed to mono by averaging channels; output shape is `(batch, time)`. `False`: mono audio is placed in channel 0 with remaining channels zero-padded to match the batch maximum; output shape is `(batch, channels, time)`.



Return type:
    

`Union`[`Tuple`[`Tensor`, `Tensor`], `Tuple`[`Tensor`, `Tensor`, [`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")]]

Returns:
    

a tuple of tensors `(audio, audio_lens)`, or `(audio, audio_lens, cuts)`.

lhotse.dataset.collation.collate_multi_channel_audio(_cuts_ , _pad_direction ='right'_, _executor =None_, _fault_tolerant =False_, _recording_field =None_, _mono_downmix =None_)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.collate_multi_channel_audio "Permalink to this definition")
    

Load audio samples for all the cuts and return them as a batch in a torch tensor. The output shape is `(batch, time)` or `(batch, channels, time)`. The cuts will be padded with silence if necessary.

Parameters:
    

  * **cuts** ([`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")) – a `CutSet` used to load the audio samples.

  * **pad_direction** (`str`) – where to apply the padding (`right`, `left`, or `both`).

  * **executor** (`Optional`[`Executor`]) – an instance of ThreadPoolExecutor or ProcessPoolExecutor; when provided, we will use it to read audio concurrently.

  * **fault_tolerant** (`bool`) – when `True`, the cuts for which audio loading failed will be skipped. Setting this parameter will cause the function to return a 3-tuple, where the third element is a CutSet for which the audio data were sucessfully read.

  * **recording_field** (`Optional`[`str`]) – when specified, we will try to load recordings from a custom field with this name (i.e., `cut.load_<recording_field>()` instead of default `cut.load_audio()`).

  * **mono_downmix** (`Optional`[`bool`]) – controls channel handling. `None` (default): auto-detect — uses downmix semantics unless every cut in the batch is multichannel, in which case multichannel collation is used. `True`: multichannel audio is downmixed to mono by averaging channels; output shape is `(batch, time)`. `False`: mono audio is placed in channel 0 with remaining channels zero-padded to match the batch maximum; output shape is `(batch, channels, time)`.



Return type:
    

`Union`[`Tuple`[`Tensor`, `Tensor`], `Tuple`[`Tensor`, `Tensor`, [`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")]]

Returns:
    

a tuple of tensors `(audio, audio_lens)`, or `(audio, audio_lens, cuts)`.

lhotse.dataset.collation.collate_video(_cuts_ , _with_audio =True_, _pad_direction ='right'_, _executor =None_, _fault_tolerant =False_, _recording_field =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/collation.html#collate_video)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.collate_video "Permalink to this definition")
    

Load video and audio for all cuts and return them as a batch in torch tensors. The output video shape is `(batch, time, channel, height, width)`. The output audio shape is `(batch, channel, time)`. The cuts will be padded with silence if necessary.

Note

We expect each video to contain audio and the same number of audio channels. We may support padding missing channels at a later time.

Parameters:
    

  * **cuts** ([`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")) – a `CutSet` used to load the audio samples.

  * **with_audio** (`bool`) – should the audio data be loaded.

  * **pad_direction** (`str`) – where to apply the padding (`right`, `left`, or `both`).

  * **executor** (`Optional`[`Executor`]) – an instance of ThreadPoolExecutor or ProcessPoolExecutor; when provided, we will use it to read video concurrently.

  * **fault_tolerant** (`bool`) – when `True`, the cuts for which video/audio loading failed will be skipped. Setting this parameter will cause the function to return a 5-tuple, where the fifth element is a CutSet for which the audio data were sucessfully read.

  * **recording_field** (`Optional`[`str`]) – when specified, we will try to load recordings from a custom field with this name (i.e., `cut.load_<recording_field>()` instead of default `cut.load_video()`).



Returns:
    

a tuple of tensors `(video, video_lens, audio, audio_lens)`, or `(video, video_lens, audio, audio_lens, cuts)`.

lhotse.dataset.collation.collate_custom_field(_cuts_ , _field_ , _pad_value =None_, _pad_direction ='right'_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/collation.html#collate_custom_field)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.collate_custom_field "Permalink to this definition")
    

Load custom arrays for all the cuts and return them as a batch in a torch tensor. The output shapes are:

>   * `(batch, d0, d1, d2, ...)` for `lhotse.array.Array` of shape `(d0, d1, d2, ...)`.
>     
> 
> Note: all arrays have to be of the same shape, as we expect these represent fixed-size embeddings.
> 
>   * `(batch, d0, pad_dt, d1, ...)` for `lhotse.array.TemporalArray` of shape
>     
> 
> `(d0, dt, d1, ...)` where `dt` indicates temporal dimension (variable-sized), and `pad_dt` indicates temporal dimension after padding (equal-sized for all cuts). We expect these represent temporal data, such as alignments, posteriors, features, etc.
> 
>   * `(batch, )` for anything else, such as int or float: we will simply stack them into
>     
> 
> a list and tensorize it.
> 
> 


Note

This function disregards the `frame_shift` attribute of `lhotse.array.TemporalArray` when padding; it simply pads all the arrays to the longest one found in the mini-batch. Because of that, the function will work correctly even if the user supplied inconsistent meta-data.

Note

Temporal arrays of integer type that are smaller than torch.int64, will be automatically promoted to torch.int64.

Parameters:
    

  * **cuts** ([`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")) – a `CutSet` used to load the features.

  * **field** (`str`) – name of the custom field to be retrieved.

  * **pad_value** (`Union`[`None`, `int`, `float`]) – value to be used for padding the temporal arrays. Ignored for non-temporal array and non-array attributes.

  * **pad_direction** (`str`) – where to apply the padding (`right`, `left`, or `both`).



Return type:
    

`Union`[`Tensor`, `Tuple`[`Tensor`, `Tensor`]]

Returns:
    

a collated data tensor, or a tuple of tensors `(collated_data, sequence_lens)`.

lhotse.dataset.collation.collate_multi_channel_features(_cuts_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/collation.html#collate_multi_channel_features)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.collate_multi_channel_features "Permalink to this definition")
    

Load features for all the cuts and return them as a batch in a torch tensor. The cuts have to be of type `MixedCut` and their tracks will be interpreted as individual channels. The output shape is `(batch, channel, time, features)`. The cuts will be padded with silence if necessary.

Return type:
    

`Tensor`

lhotse.dataset.collation.collate_vectors(_tensors_ , _padding_value =-100_, _pad_direction ='right'_, _matching_shapes =False_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/collation.html#collate_vectors)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.collate_vectors "Permalink to this definition")
    

Convert an iterable of 1-D tensors (of possibly various lengths) into a single stacked tensor.

Parameters:
    

  * **tensors** (`Iterable`[`Union`[`Tensor`, `ndarray`]]) – an iterable of 1-D tensors.

  * **padding_value** (`Union`[`int`, `float`]) – the padding value inserted to make all tensors have the same length.

  * **pad_direction** (`str`) – where to apply the padding (`right` or `left`).

  * **matching_shapes** (`bool`) – when `True`, will fail when input tensors have different shapes.



Return type:
    

`Tensor`

Returns:
    

a tensor with shape `(B, L)` where `B` is the number of input tensors and `L` is the number of items in the longest tensor.

lhotse.dataset.collation.collate_matrices(_tensors_ , _padding_value =0_, _matching_shapes =False_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/collation.html#collate_matrices)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.collate_matrices "Permalink to this definition")
    

Convert an iterable of 2-D tensors (of possibly various first dimension, but consistent second dimension) into a single stacked tensor.

Parameters:
    

  * **tensors** (`Iterable`[`Union`[`Tensor`, `ndarray`]]) – an iterable of 2-D tensors.

  * **padding_value** (`Union`[`int`, `float`]) – the padding value inserted to make all tensors have the same length.

  * **matching_shapes** (`bool`) – when `True`, will fail when input tensors have different shapes.



Return type:
    

`Tensor`

Returns:
    

a tensor with shape `(B, L, F)` where `B` is the number of input tensors, `L` is the largest found shape[0], and `F` is equal to shape[1].

lhotse.dataset.collation.read_audio_from_cuts(_cuts_ , _executor =None_, _suppress_errors =False_, _recording_field =None_, _filter_aux_iter =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/collation.html#read_audio_from_cuts)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.read_audio_from_cuts "Permalink to this definition")
    

Loads audio data from an iterable of cuts.

Parameters:
    

  * **cuts** (`Iterable`[[`Cut`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.Cut "lhotse.cut.base.Cut")]) – a CutSet or iterable of cuts.

  * **executor** (`Optional`[`Executor`]) – optional Executor (e.g., ThreadPoolExecutor or ProcessPoolExecutor) to perform the audio reads in parallel.

  * **suppress_errors** (`bool`) – when set to `True`, will enable fault-tolerant data reads; we will skip the cuts and audio data for the instances that failed (and emit a warning). When `False` (default), the errors will not be suppressed.

  * **recording_field** (`Optional`[`str`]) – when specified, we will try to load recordings from a custom field with this name (i.e., `cut.load_<recording_field>()` instead of default `cut.load_audio()`).

  * **filter_aux_iter** (`Optional`[`Iterable`]) – when specified, we will iterate over this iterator and discard the elements for which a corresponding cut failed to load audio, if `suppress_errors` is set to `True`. This iterator is expected to be of the same length as `cuts`.



Return type:
    

`Union`[`Tuple`[`List`[`Tensor`], [`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")], `Tuple`[`List`[`Tensor`], [`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet"), `List`]]

Returns:
    

a tuple of two items: a list of audio tensors (with different shapes), and a list of cuts for which we read the data successfully. If `filter_aux_iter` is specified, it returns a 3-tuple where the third element is the filtered auxiliary iterator.

lhotse.dataset.collation.read_video_from_cuts(_cuts_ , _with_audio =True_, _executor =None_, _suppress_errors =False_, _recording_field =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/collation.html#read_video_from_cuts)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.read_video_from_cuts "Permalink to this definition")
    

Loads audio data from an iterable of cuts.

Parameters:
    

  * **cuts** (`Iterable`[[`Cut`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.Cut "lhotse.cut.base.Cut")]) – a CutSet or iterable of cuts.

  * **with_audio** (`bool`) – should the audio data be loaded.

  * **executor** (`Optional`[`Executor`]) – optional Executor (e.g., ThreadPoolExecutor or ProcessPoolExecutor) to perform the audio reads in parallel.

  * **suppress_errors** (`bool`) – when set to `True`, will enable fault-tolerant data reads; we will skip the cuts and audio data for the instances that failed (and emit a warning). When `False` (default), the errors will not be suppressed.

  * **recording_field** (`Optional`[`str`]) – when specified, we will try to load recordings from a custom field with this name (i.e., `cut.load_<recording_field>()` instead of default `cut.load_video()`).



Return type:
    

`Tuple`[`List`[`Tensor`], `List`[`Tensor`], [`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")]

Returns:
    

a tuple of two items: a list of audio tensors (with different shapes), and a list of cuts for which we read the data successfully.

lhotse.dataset.collation.read_features_from_cuts(_cuts_ , _executor =None_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/collation.html#read_features_from_cuts)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.read_features_from_cuts "Permalink to this definition")
    

Return type:
    

`List`[`Tensor`]

lhotse.dataset.collation.collate_images(_cuts_ , _image_field ='image'_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/collation.html#collate_images)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.collation.collate_images "Permalink to this definition")
    

Load images for all cuts and return them as a batch in a torch tensor. The output image shape is `(batch, height, width, channel)`.

Parameters:
    

  * **cuts** ([`CutSet`](https://lhotse.readthedocs.io/en/latest/api.html#lhotse.cut.CutSet "lhotse.cut.set.CutSet")) – a `CutSet` used to load the images.

  * **image_field** (`str`) – the field in the cut to load the images from.



Return type:
    

`Tensor`

Returns:
    

tensor of collated images

## Dataloading seeding utilities[](https://lhotse.readthedocs.io/en/latest/datasets.html#module-lhotse.dataset.dataloading "Permalink to this heading")

lhotse.dataset.dataloading.make_worker_init_fn(_rank =None_, _world_size =None_, _set_different_node_and_worker_seeds =True_, _seed =42_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/dataloading.html#make_worker_init_fn)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.make_worker_init_fn "Permalink to this definition")
    

Calling this function creates a worker_init_fn suitable to pass to PyTorch’s DataLoader.

It helps with two issues: :rtype: `Optional`[`Callable`[[`int`], `None`]]

  * sets the random seeds differently for each worker and node, which helps with
    

avoiding duplication in randomized data augmentation techniques.

  * sets environment variables that help WebDataset detect it’s inside multi-GPU (DDP)
    

training, so that it correctly de-duplicates the data across nodes.




lhotse.dataset.dataloading.worker_init_fn(_worker_id_ , _rank =None_, _world_size =None_, _set_different_node_and_worker_seeds =True_, _seed =42_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/dataloading.html#worker_init_fn)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.worker_init_fn "Permalink to this definition")
    

Function created by [`make_worker_init_fn()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.make_worker_init_fn "lhotse.dataset.dataloading.make_worker_init_fn"), refer to its documentation for details.

Return type:
    

`None`

lhotse.dataset.dataloading.resolve_seed(_seed_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/dataloading.html#resolve_seed)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.resolve_seed "Permalink to this definition")
    

Resolves the special values of random seed supported in Lhotse.

If it’s an integer, we’ll just return it.

If it’s “trng”, we’ll use the `secrets` module to generate a random seed using a true RNG (to the extend supported by the OS).

If it’s “randomized”, we’ll check whether we’re in a dataloading worker of `torch.utils.data.DataLoader`. If we are, we expect that it was passed the result of [`make_worker_init_fn()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.make_worker_init_fn "lhotse.dataset.dataloading.make_worker_init_fn") into its `worker_init_fn` argument, in which case we’ll return a special seed exclusive to that worker. If we are not in a dataloading worker (or `num_workers` was set to `0`), we’ll return Python’s `random` module global seed.

Return type:
    

`int`

lhotse.dataset.dataloading.get_worker_partition()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/dataloading.html#get_worker_partition)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.get_worker_partition "Permalink to this definition")
    

Resolve the global `(shard_id, num_shards)` partition for the calling code, combining the DP rank with the DataLoader worker id.

Returns `(shard_id, num_shards)` where `shard_id = rank * num_workers + worker_id` and `num_shards = world_size * max(num_workers, 1)`.

Returns the trivial `(0, 1)` partition when the `LHOTSE_USE_WORKER_PARTITION` env var is not set — i.e. when [`worker_init_fn()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.worker_init_fn "lhotse.dataset.dataloading.worker_init_fn") has not been called. This keeps map-style mode (where the sampler runs in the main process and uses its own over-sample-and-discard DP dedup) unaffected even when RANK/WORLD_SIZE are already set in the environment (e.g. by torchrun).

Used by indexed-manifest iterators (via `LazyShuffledRange`) to deterministically split index ranges across DP ranks × DataLoader workers so each tuple yields a disjoint, non-overlapping subset.

Reads DP info via [`get_rank()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.get_rank "lhotse.dataset.dataloading.get_rank") / [`get_world_size()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.get_world_size "lhotse.dataset.dataloading.get_world_size") (env-var aware; populated by [`worker_init_fn()`](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.worker_init_fn "lhotse.dataset.dataloading.worker_init_fn") inside DataLoader worker subprocesses). Reads the DataLoader worker info via `torch.utils.data.get_worker_info()`; when called outside a DataLoader worker (e.g. `num_workers=0`), treats the caller as a single worker (`worker_id=0, num_workers=1`).

Return type:
    

`tuple`

_class _lhotse.dataset.dataloading.PartitionedIndexedIterator(_shuffle =False_, _seed =0_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/dataloading.html#PartitionedIndexedIterator)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.PartitionedIndexedIterator "Permalink to this definition")
    

Shared partition-aware iteration driver for indexed leaf iterators.

Encapsulates the (shard_id, num_shards) partition lookup, position tracking across DataLoader worker subprocesses, and topology-validated resume — the bits every indexed `IteratorNode` needs to repeat correctly. Yields global indices into the leaf source; the caller is responsible for decoding each index into the user-facing item.

Two iteration modes are supported and selected at construction time:

  * **Stride** (`shuffle=False`, default): yields `[shard_id, shard_id + num_shards, shard_id + 2 * num_shards, …]` — the simplest disjoint-per-rank partition.

  * **Feistel-shuffled** (`shuffle=True`, with `seed`): yields a Feistel permutation of the full range restricted to this rank’s slice, via `LazyShuffledRange`. Useful when the underlying source is in a deterministic on-disk order but the consumer wants item-level shuffling within each shard.




Typical wiring:
    
    
    class MyIndexedIterator(IteratorNode):
        def __init__(self, ...):
            ...
            self._iter_state = PartitionedIndexedIterator()
    
        def __iter__(self):
            for global_idx in self._iter_state.iterate(self._total_len):
                item = self._decode_at(global_idx)
                if item is None:
                    continue
                yield item
    
        def state_dict(self) -> dict:
            return {**self._iter_state.state_dict(), "epoch": self.epoch}
    
        def load_state_dict(self, sd: dict) -> None:
            self._iter_state.load_state_dict(sd)
            self.epoch = sd.get("epoch", 0)
    

Notes:
    

  * The partition is `shard_id = rank * num_workers + worker_id`, `num_shards = world_size * num_workers`. Outside DataLoader workers (or when `LHOTSE_USE_WORKER_PARTITION` is unset — i.e. map-style mode) the partition collapses to `(0, 1)` and iteration covers the full range, matching pre-partition behavior.

  * `state_dict` stores the local-within-shard `position` plus the `(shard_id, num_shards)` topology captured at save time; on resume we refuse to continue under a different topology because the per-shard index sequence would diverge.




__init__(_shuffle =False_, _seed =0_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/dataloading.html#PartitionedIndexedIterator.__init__)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.PartitionedIndexedIterator.__init__ "Permalink to this definition")
    

_property _position _: int_[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.PartitionedIndexedIterator.position "Permalink to this definition")
    

Local position within the current shard (0-indexed next element).

iterate(_total_len_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/dataloading.html#PartitionedIndexedIterator.iterate)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.PartitionedIndexedIterator.iterate "Permalink to this definition")
    

Yield global indices for this rank’s slice of `range(total_len)`.

Return type:
    

`Generator`[`int`, `None`, `None`]

Raises:
    

ValueError: if resuming from a saved state under a different
    

`(shard_id, num_shards)` topology than the one recorded at save time.

state_dict()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/dataloading.html#PartitionedIndexedIterator.state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.PartitionedIndexedIterator.state_dict "Permalink to this definition")
    

Return type:
    

`dict`

load_state_dict(_sd_)[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/dataloading.html#PartitionedIndexedIterator.load_state_dict)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.PartitionedIndexedIterator.load_state_dict "Permalink to this definition")
    

Return type:
    

`None`

lhotse.dataset.dataloading.get_world_size()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/dataloading.html#get_world_size)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.get_world_size "Permalink to this definition")
    

Source: <https://github.com/danpovey/icefall/blob/74bf02bba6016c1eb37858a4e0e8a40f7d302bdb/icefall/dist.py#L56>

Return type:
    

`int`

lhotse.dataset.dataloading.get_rank()[[source]](https://lhotse.readthedocs.io/en/latest/_modules/lhotse/dataset/dataloading.html#get_rank)[](https://lhotse.readthedocs.io/en/latest/datasets.html#lhotse.dataset.dataloading.get_rank "Permalink to this definition")
    

Source: <https://github.com/danpovey/icefall/blob/74bf02bba6016c1eb37858a4e0e8a40f7d302bdb/icefall/dist.py#L56>

Return type:
    

`int`

[ Previous](https://lhotse.readthedocs.io/en/latest/parallelism.html "Executing tasks in parallel") [Next ](https://lhotse.readthedocs.io/en/latest/indexed-manifests.html "Indexed Manifests and IteratorNodes")

* * *

(C) Copyright 2020-2024, Lhotse development team.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org). 
