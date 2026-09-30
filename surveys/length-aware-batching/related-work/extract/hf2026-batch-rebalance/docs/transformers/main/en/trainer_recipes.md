**Source:** *Trainer features* — [original page](https://huggingface.co/docs/transformers/main/en/trainer_recipes)

Transformers documentation

Trainer features



![Figure](figures/d59eac8ef9c58189119dce5b818065c2535f5fddb908dc5b1e6b7d562d8a8c22.svg)

 



![Figure](figures/0764276589be9a33ce3912b81e499d703d1aea123d4d66c3b6e11c89d08481a6.svg)

 

# Transformers



![Figure](figures/c89850d10def5ea100be4e988adf869218ac8d9eb9a996bd48946dbaf4fa9645.svg)

 🏡 View all docsAWS Trainium & InferentiaAccelerateArgillaAutoTrainBitsandbytesCLIChat UIDataset viewerDatasetsDeploying on AWSDiffusersDistilabelEvaluateGoogle CloudGoogle TPUsGradioHubHub Python LibraryHuggingface.jsInference Endpoints (dedicated)Inference ProvidersKernelsLeRobotLeaderboardsLightevalMicrosoft AzureOpenEnvOptimumPEFTReachy MiniSafetensorsSentence TransformersTRLTasksText Embeddings InferenceText Generation InferenceTokenizersTrackioTransformersTransformers.jsXetsmolagentstimm



![Figure](figures/c34d99ea2ae256af07e974db93ef6163e3c18f41b8367da0bb1fac9c669bbbf1.svg)

 

Search documentation

mainv5.17.0v5.15.1v5.14.0v5.13.1v5.12.0v5.11.0v5.10.4v5.9.0v5.8.1v5.7.0v5.6.2v5.5.4v5.4.0v5.3.0v5.2.0v5.1.0v5.0.0v4.57.6v4.56.2v4.55.4v4.53.3v4.52.3v4.51.3v4.50.0v4.49.0v4.48.2v4.47.1v4.46.3v4.45.2v4.44.2v4.43.4v4.42.4v4.41.2v4.40.2v4.39.3v4.38.2v4.37.2v4.36.1v4.35.2v4.34.1v4.33.3v4.32.1v4.31.0v4.30.0v4.29.1v4.28.1v4.27.2v4.26.1v4.25.1v4.24.0v4.23.1v4.22.2v4.21.3v4.20.1v4.19.4v4.18.0v4.17.0v4.16.2v4.15.0v4.14.1v4.13.0v4.12.5v4.11.3v4.10.1v4.9.2v4.8.2v4.7.0v4.6.0v4.5.1v4.4.2v4.3.3v4.2.2v4.1.1v4.0.1v3.5.1v3.4.0v3.3.1v3.2.0v3.1.0v3.0.2v2.11.0v2.10.0v2.9.1v2.8.0v2.7.0v2.6.0v2.5.1v2.4.1v2.3.0v2.2.2v2.1.1v2.0.0v1.2.0v1.1.0v1.0.0doc-builder-html ARDEENESFRHIITJAKOPTROTETRZH



![Figure](figures/0bae6bd2dea6246ee29ad08587f76f66a545e277c367f896847aaa6914566ef3.svg)

 

[ 

![Figure](figures/ccc587113e9f2ab4c1da9a75d30b82647af2df423658224c158ea58d75460859.svg)

 ](https://github.com/huggingface/transformers)

Get started

[Transformers](https://huggingface.co/docs/transformers/main/en/index)[Installation](https://huggingface.co/docs/transformers/main/en/installation)[Quickstart](https://huggingface.co/docs/transformers/main/en/quicktour)

Base classes

Models

Preprocessors

Inference

Pipeline API

Generate API

Optimization

Chat with models

Serving

Training

Get started

Customization

[Subclassing Trainer methods](https://huggingface.co/docs/transformers/main/en/trainer_customize)[Callbacks](https://huggingface.co/docs/transformers/main/en/trainer_callbacks)[Data collators](https://huggingface.co/docs/transformers/main/en/data_collators)[Optimizers and schedulers](https://huggingface.co/docs/transformers/main/en/optimizers)[Hyperparameter search](https://huggingface.co/docs/transformers/main/en/hpo_train)[Trainer features](https://huggingface.co/docs/transformers/main/en/trainer_recipes)

[Parameter-efficient fine-tuning](https://huggingface.co/docs/transformers/main/en/peft)

Performance

Distributed training

Hardware

Quantization

Ecosystem integrations

Resources

API

You are viewing main version, which requires [installation from source](https://huggingface.co/docs/transformers/installation#install-from-source). If you'd like regular pip install, checkout the latest stable version ([v5.17.0](https://huggingface.co/docs/transformers/v5.17.0/trainer_recipes)).



![Hugging Face's logo](figures/3613c73f07ccae19118bfe6d2f8cd127183d08cf99468a708e090953e116ed0a.svg)

 

Join the Hugging Face community

and get access to the augmented documentation experience



![Figure](figures/41509f6375e8be6db7f67034291f23782f9e834807199e6d01868d0f878912f1.svg)

 

Collaborate on models, datasets and Spaces



![Figure](figures/3ad67b21f4cd9cf00c14d9a4b9777ec177f82f914396dc91a883fbe0e7a2d152.svg)

 

Faster examples with accelerated inference



![Figure](figures/44e6e69f22cd4cbe62dfcc35dd57d77fa09f3645ab1c734fcdcc1656c22b7f2e.svg)

 

Switch between documentation themes

[Sign Up](https://huggingface.co/join)

to get started



![Figure](figures/ae60b8d0611069581b4d0593c55e859bd92726fc08a7cb5f5564887d3227d748.svg)

  Copy page 

![Figure](figures/9b043f9fd1e5c03feedfb6256d54d4bd138c4ee32631574588e42412bb189443.svg)

 

# [ 

![Figure](figures/795d65f6f5e297f9da58542e734fa54ff27e3468a1c696c0755648e4df91c484.svg)

 ](https://huggingface.co/docs/transformers/main/en/trainer_recipes#trainer-features) Trainer features

Each recipe below demonstrates a specific [Trainer](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer) feature: custom loss functions, memory-efficient evaluation, checkpointing strategies, and more.

> Open an [issue](https://github.com/huggingface/transformers/issues/new/choose) if there is a feature or workflow you’d like to see here.

## [ 

![Figure](figures/795d65f6f5e297f9da58542e734fa54ff27e3468a1c696c0755648e4df91c484.svg)

 ](https://huggingface.co/docs/transformers/main/en/trainer_recipes#custom-loss-function) Custom loss function

Pass [compute_loss_func](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer.compute_loss_func) to [Trainer](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer) to replace the default loss function. The function runs _after_ the forward pass and only defines how loss is computed from the outputs. To modify the forward pass itself, [subclass](https://huggingface.co/docs/transformers/main/en/trainer_customize#compute-loss) [compute_loss()](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer.compute_loss) instead.

The custom loss function must have the following signature:



![Figure](figures/3cebc038b7b45db612872e6abb5f269d3bd772e0f262ca22369f83a3f79f5060.svg)

 

Copied
    
    
    import torch.nn.functional as F
    
    def my_loss_fn(outputs, labels, num_items_in_batch):
        logits = outputs["logits"]
        loss = F.cross_entropy(logits, labels, reduction="sum")
        return loss / num_items_in_batch

  * `outputs` is the raw model output (`outputs.logits` has shape `(batch, seq_len, vocab_size)`).
  * `labels` is the token ids popped from the input batch by [Trainer](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer) before the forward pass.
  * `num_items_in_batch` is the number of prediction targets across the full accumulated batch. For causal LM models it counts the shifted labels (`labels[..., 1:]`), since the label shift leaves position 0 of every sequence without a target. See [Loss scaling](https://huggingface.co/docs/transformers/main/en/grad_accumulation#loss-scaling) for details. [Trainer](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer) skips automatic loss normalization when a custom loss function is provided, so your function must handle normalization directly.





![Figure](figures/3cebc038b7b45db612872e6abb5f269d3bd772e0f262ca22369f83a3f79f5060.svg)

 

Copied
    
    
    trainer = Trainer(
        model=model,
        args=TrainingArguments(...),
        train_dataset=train_dataset,
        compute_loss_func=my_loss_fn,
    )
    trainer.train()

> See the [subclassing guide](https://huggingface.co/docs/transformers/main/en/trainer_customize#compute-loss) for more examples of overriding [compute_loss()](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer.compute_loss).

## [ 

![Figure](figures/795d65f6f5e297f9da58542e734fa54ff27e3468a1c696c0755648e4df91c484.svg)

 ](https://huggingface.co/docs/transformers/main/en/trainer_recipes#evaluating-on-start) Evaluating on start

Set `eval_on_start=True` to run a full eval pass before the first training step. A pre-training eval surfaces issues with the evaluation pipeline early, especially during long runs.

`eval_on_start` requires a valid `eval_strategy` (such as `"epoch"`) and an eval dataset.



![Figure](figures/3cebc038b7b45db612872e6abb5f269d3bd772e0f262ca22369f83a3f79f5060.svg)

 

Copied
    
    
    from transformers import Trainer, TrainingArguments
    
    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir="out",
            eval_strategy="epoch",
            eval_on_start=True,
        ),
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        compute_metrics=compute_metrics,
    )
    trainer.train()

A full eval adds time, so it’s most useful on first runs or after modifying `compute_metrics`.

## [ 

![Figure](figures/795d65f6f5e297f9da58542e734fa54ff27e3468a1c696c0755648e4df91c484.svg)

 ](https://huggingface.co/docs/transformers/main/en/trainer_recipes#memory-efficient-evals) Memory-efficient evals

During evaluation, [Trainer](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer) runs a forward pass on every batch and concatenates the logits into a single tensor on the GPU. Once the eval dataset is fully processed, [Trainer](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer) moves the concatenated logits to the CPU and calls `compute_metrics`. For large models or eval sets, the accumulated logits can exhaust GPU memory even when training on the same hardware works fine, because training only holds one batch of activations at a time.

### [ 

![Figure](figures/795d65f6f5e297f9da58542e734fa54ff27e3468a1c696c0755648e4df91c484.svg)

 ](https://huggingface.co/docs/transformers/main/en/trainer_recipes#evalaccumulationsteps) eval_accumulation_steps

Offload the accumulated predictions from GPU to CPU every _n_ batches. Lower values reduce GPU memory at the cost of more frequent CPU transfers.



![Figure](figures/3cebc038b7b45db612872e6abb5f269d3bd772e0f262ca22369f83a3f79f5060.svg)

 

Copied
    
    
    from transformers import Trainer, TrainingArguments
    
    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir="out",
            eval_strategy="epoch",
            eval_accumulation_steps=16,   # move predictions to CPU every 16 batches
        ),
        eval_dataset=eval_dataset,
        compute_metrics=compute_metrics,
    )
    trainer.train()

### [ 

![Figure](figures/795d65f6f5e297f9da58542e734fa54ff27e3468a1c696c0755648e4df91c484.svg)

 ](https://huggingface.co/docs/transformers/main/en/trainer_recipes#preprocesslogitsformetrics) preprocess_logits_for_metrics

Called once per eval batch on the GPU, immediately after the forward pass and before logit accumulation. The returned value replaces the logits in `eval_pred.predictions`. Running the computation at the batch level reduces per-batch tensor size and gives `eval_accumulation_steps` a smaller tensor to offload.



![Figure](figures/3cebc038b7b45db612872e6abb5f269d3bd772e0f262ca22369f83a3f79f5060.svg)

 

Copied
    
    
    import evaluate
    from transformers import Trainer, TrainingArguments
    
    metric = evaluate.load("accuracy")
    
    def preprocess_logits_for_metrics(logits, labels):
        if isinstance(logits, tuple):
            logits = logits[0]
        return logits.argmax(dim=-1)
    
    def compute_metrics(eval_preds):
        preds, labels = eval_preds
        labels = labels[:, 1:].reshape(-1)
        preds = preds[:, :-1].reshape(-1)
        return metric.compute(predictions=preds, references=labels)
    
    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir="out",
            eval_strategy="epoch",
            eval_accumulation_steps=16,
        ),
        eval_dataset=eval_dataset,
        compute_metrics=compute_metrics,
        preprocess_logits_for_metrics=preprocess_logits_for_metrics,
    )
    trainer.train()

## [ 

![Figure](figures/795d65f6f5e297f9da58542e734fa54ff27e3468a1c696c0755648e4df91c484.svg)

 ](https://huggingface.co/docs/transformers/main/en/trainer_recipes#dataloader-performance) Dataloader performance

By default, [Trainer](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer) creates a dataloader with `dataloader_num_workers=0`. Data is loaded in the main process while the GPU idles, which shows up as low GPU utilization between batches.

Both `dataloader_persistent_workers` and `dataloader_prefetch_factor` require `dataloader_num_workers > 0`.

  * `dataloader_persistent_workers` keeps worker subprocesses alive between epochs to avoid reinitializing from scratch, at the cost of higher memory.
  * `dataloader_prefetch_factor` controls how many batches each worker prepares in advance. With `dataloader_prefetch_factor=2` and `num_workers=4`, up to 8 batches sit in memory while the GPU trains on the current one.





![Figure](figures/3cebc038b7b45db612872e6abb5f269d3bd772e0f262ca22369f83a3f79f5060.svg)

 

Copied
    
    
    from transformers import TrainingArguments
    
    args = TrainingArguments(
        output_dir="out",
        dataloader_num_workers=4,            # spawn 4 worker subprocesses
        dataloader_persistent_workers=True,  # keep them alive between epochs
        dataloader_prefetch_factor=2,        # each worker preloads 2 batches ahead
    )

## [ 

![Figure](figures/795d65f6f5e297f9da58542e734fa54ff27e3468a1c696c0755648e4df91c484.svg)

 ](https://huggingface.co/docs/transformers/main/en/trainer_recipes#group-samples-by-length) Group samples by length

Use `train_sampling_strategy="group_by_length"` to batch examples with similar lengths and reduce padding. When you don’t provide precomputed lengths, [Trainer](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer) infers them from the first model input in each dataset item. This also works when processor-based multimodal datasets return [BatchFeature](https://huggingface.co/docs/transformers/main/en/main_classes/image_processor#transformers.BatchFeature) objects, because they are mapping-like feature containers.



![Figure](figures/3cebc038b7b45db612872e6abb5f269d3bd772e0f262ca22369f83a3f79f5060.svg)

 

Copied
    
    
    from transformers import TrainingArguments
    
    training_args = TrainingArguments(
        output_dir="qwen3-vl-finetuned",
        train_sampling_strategy="group_by_length",
    )

If a [Dataset](https://huggingface.co/docs/datasets/main/en/package_reference/main_classes#datasets.Dataset) already has a precomputed length column, [Trainer](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer) uses that column instead. The default column name is `length`. Set `length_column_name` when your dataset uses another name. This strategy requires a dataset with a known length and is ignored for [IterableDataset](https://huggingface.co/docs/datasets/main/en/package_reference/main_classes#datasets.IterableDataset).

## [ 

![Figure](figures/795d65f6f5e297f9da58542e734fa54ff27e3468a1c696c0755648e4df91c484.svg)

 ](https://huggingface.co/docs/transformers/main/en/trainer_recipes#batch-rebalance-sampling) Batch rebalance sampling

On variable-length datasets, imbalance within a micro-batch and across devices causes devices to waste time on padding and to idle at gradient synchronization steps.

Set `train_sampling_strategy="batch_rebalance"` in [TrainingArguments](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.TrainingArguments) to reduce both effects. For each optimizer step, the sampler:

  1. Sorts the batch’s samples by length.
  2. Shards the sorted batch across devices so that the padded-token cost of each micro-batch is balanced. Micro-batches with long samples get fewer samples, and micro-batches with short samples get more.



This reduces padding within each micro-batch, and each device finishes a micro-batch at roughly the same time, which reduces idle time at synchronization and keeps peak memory lower than `"group_by_length"`. This strategy is only supported for data-parallel training for now (tensor parallelism is not yet supported).



![Figure](figures/3cebc038b7b45db612872e6abb5f269d3bd772e0f262ca22369f83a3f79f5060.svg)

 

Copied
    
    
    from transformers import Trainer, TrainingArguments
    
    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir="out",
            train_sampling_strategy="batch_rebalance",  # balance padding cost across devices
            per_device_train_batch_size=8,              # average samples per micro-batch
            length_column_name="length",                # optional: dataset column with precomputed lengths
        ),
        train_dataset=train_dataset,
    )
    trainer.train()

`per_device_train_batch_size` is an average here rather than an exact per-step count: some micro-batches have fewer samples and some have more, but the total number of samples trained per step stays the same as with a normal distributed sampling strategy.

The sampler needs the length of every sample to sort and balance batches. By default, the [Trainer](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer) scans the full dataset once at the start of training to compute these lengths. To skip this scan, precompute the lengths into a dataset column (during preprocessing, for example) and pass its name as `length_column_name` (`"length"` by default).

## [ 

![Figure](figures/795d65f6f5e297f9da58542e734fa54ff27e3468a1c696c0755648e4df91c484.svg)

 ](https://huggingface.co/docs/transformers/main/en/trainer_recipes#neftune) NEFTune

[NEFTune](https://hf.co/papers/2310.05914) adds random noise to token embeddings during the forward pass. The noise acts as regularization and can improve performance for instruction fine-tuning.

Enable NEFTune by setting `neftune_noise_alpha` in [TrainingArguments](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.TrainingArguments). Typical alpha values range from 5 to 15.



![Figure](figures/3cebc038b7b45db612872e6abb5f269d3bd772e0f262ca22369f83a3f79f5060.svg)

 

Copied
    
    
    from transformers import Trainer, TrainingArguments
    
    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir="out",
            num_train_epochs=3,
            neftune_noise_alpha=5,
        ),
        train_dataset=train_dataset,
    )
    trainer.train()

NEFTune only affects training, and the original embedding layer is restored after training.

## [ 

![Figure](figures/795d65f6f5e297f9da58542e734fa54ff27e3468a1c696c0755648e4df91c484.svg)

 ](https://huggingface.co/docs/transformers/main/en/trainer_recipes#logging) Logging

Control when and where [Trainer](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer) writes log entries with `logging_strategy`, `logging_steps`, and `report_to`.

  * `logging_strategy="steps"` logs every `logging_steps()` optimizer updates. Use `"epoch"` to log at each epoch end instead.
  * `report_to` streams logs to an experiment tracker like Trackio.





![Figure](figures/3cebc038b7b45db612872e6abb5f269d3bd772e0f262ca22369f83a3f79f5060.svg)

 

Copied
    
    
    from transformers import Trainer, TrainingArguments
    
    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir="out",
            logging_strategy="steps",
            logging_steps=50,               # write a log entry every 50 optimizer updates
            report_to="trackio",            # stream to Trackio (or "wandb", "tensorboard", …)
            run_name="model-experiment-v1", # display name in the tracker
        ),
        train_dataset=train_dataset,
    )
    trainer.train()

## [ 

![Figure](figures/795d65f6f5e297f9da58542e734fa54ff27e3468a1c696c0755648e4df91c484.svg)

 ](https://huggingface.co/docs/transformers/main/en/trainer_recipes#checkpointing) Checkpointing

[Trainer](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer) saves a checkpoint every `save_steps()` optimizer update and keeps all of them (or the most recent `~TrainingArguments.save_total_limit`).

`save_strategy="best"` keeps only the single best checkpoint according to a metric. A new checkpoint is saved only when the tracked metric improves, which saves disk space and avoids accumulating stale checkpoints.



![Figure](figures/3cebc038b7b45db612872e6abb5f269d3bd772e0f262ca22369f83a3f79f5060.svg)

 

Copied
    
    
    from transformers import Trainer, TrainingArguments
    
    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir="out",
            eval_strategy="epoch",
            save_strategy="best",
            metric_for_best_model="perplexity",   # save when eval perplexity improves
            greater_is_better=False,              # lower perplexity is better
            load_best_model_at_end=True,          # load the best weights after training finishes
        ),
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        compute_metrics=compute_metrics,          # must return {"perplexity": ...}
    )
    trainer.train()

### [ 

![Figure](figures/795d65f6f5e297f9da58542e734fa54ff27e3468a1c696c0755648e4df91c484.svg)

 ](https://huggingface.co/docs/transformers/main/en/trainer_recipes#resume-training) Resume training

Pass `resume_from_checkpoint=True` to [train()](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer.train) if training was interrupted and you’d like to resume without losing progress. Training will resume from the latest checkpoint in `output_dir`.



![Figure](figures/3cebc038b7b45db612872e6abb5f269d3bd772e0f262ca22369f83a3f79f5060.svg)

 

Copied
    
    
    trainer.train(resume_from_checkpoint=True)

Specify a checkpoint path to resume from a particular point.



![Figure](figures/3cebc038b7b45db612872e6abb5f269d3bd772e0f262ca22369f83a3f79f5060.svg)

 

Copied
    
    
    trainer.train(resume_from_checkpoint="out/checkpoint-1000")

When resuming, [Trainer](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer) restores the optimizer state, scheduler state, and RNG state.

Checkpoint resuming requires optimizer and scheduler state files in the checkpoint directory. If those files are missing (for example, when `save_only_model=True`), the optimizer restarts from scratch.

### [ 

![Figure](figures/795d65f6f5e297f9da58542e734fa54ff27e3468a1c696c0755648e4df91c484.svg)

 ](https://huggingface.co/docs/transformers/main/en/trainer_recipes#jit-checkpointing) JIT checkpointing

With periodic checkpointing (save_strategy=“steps” or “epoch”), you lose any training progress between the last saved checkpoint and an interruption. On shared clusters with preemptible workloads such as [Kueue](https://kueue.sigs.k8s.io/), jobs can be terminated at any time, so that gap can mean hours of wasted compute.

JIT (Just-In-Time) checkpointing closes this gap. When the trainer receives a SIGTERM signal, it saves a checkpoint at the exact point training was interrupted, so you resume with minimal loss of progress. It works alongside periodic checkpointing. Periodic saves guard against crashes and hardware failures, while JIT saves guard against preemption and graceful shutdowns.

Enable it by setting `enable_jit_checkpoint=True` in [TrainingArguments](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.TrainingArguments).



![Figure](figures/3cebc038b7b45db612872e6abb5f269d3bd772e0f262ca22369f83a3f79f5060.svg)

 

Copied
    
    
    from transformers import TrainingArguments
    
    training_args = TrainingArguments(
        output_dir="your-model",
        enable_jit_checkpoint=True,
    )

When SIGTERM is received, [Trainer](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer) waits for the current training step to finish, saves a checkpoint, and stops training gracefully. A sentinel file (`checkpoint-is-incomplete.txt`) is written when the save begins and removed once the checkpoint is fully written. If a checkpoint directory still contains this file, the save was interrupted before completing. [Trainer](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer) doesn’t check for it automatically, so inspect for it yourself before resuming.

Resume from the JIT checkpoint the same way as any other checkpoint.



![Figure](figures/3cebc038b7b45db612872e6abb5f269d3bd772e0f262ca22369f83a3f79f5060.svg)

 

Copied
    
    
    trainer.train(resume_from_checkpoint=True)

> You must configure your orchestrator to allow enough time for the checkpoint to complete. The default Kubernetes graceful shutdown period is only 30 seconds, which is typically not enough for larger models.

Kubernetes

Slurm

Set `terminationGracePeriodSeconds` in your Pod or Job spec. The exact field location varies by trainer (Kubeflow Training Operator, Ray, etc.).



![Figure](figures/3cebc038b7b45db612872e6abb5f269d3bd772e0f262ca22369f83a3f79f5060.svg)

 

Copied
    
    
    spec:
      template:
        spec:
          terminationGracePeriodSeconds: 300

Calculate the required grace period as the longest possible training step time plus the checkpoint saving time, plus the 3 second `kill_wait` delay before the checkpoint begins. For example, if a training step takes up to 2 minutes and saving a checkpoint takes 2 minutes, set at least 243 seconds of grace time.

[ 

![Figure](figures/6d8334721574cb82629b46cd3e9c268857033b9aa94248d44b1c74d7a345ac00.svg)

 Update on GitHub](https://github.com/huggingface/transformers/blob/main/docs/source/en/trainer_recipes.md)



![Figure](figures/95112e1c6bb2d9d91596c9ba97810244e2c409f49f925a9937499efc204a4b92.svg)

  

![Figure](figures/d4fb1b4c26d2735cba2e89361a063e03499f078c013a2c01177878e51a022bed.svg)

 

[←Hyperparameter search](https://huggingface.co/docs/transformers/main/en/hpo_train) [Parameter-efficient fine-tuning→](https://huggingface.co/docs/transformers/main/en/peft)

[Trainer features](https://huggingface.co/docs/transformers/main/en/trainer_recipes#trainer-features)[Custom loss function](https://huggingface.co/docs/transformers/main/en/trainer_recipes#custom-loss-function)[Evaluating on start](https://huggingface.co/docs/transformers/main/en/trainer_recipes#evaluating-on-start)[Memory-efficient evals](https://huggingface.co/docs/transformers/main/en/trainer_recipes#memory-efficient-evals)[eval_accumulation_steps](https://huggingface.co/docs/transformers/main/en/trainer_recipes#evalaccumulationsteps)[preprocess_logits_for_metrics](https://huggingface.co/docs/transformers/main/en/trainer_recipes#preprocesslogitsformetrics)[Dataloader performance](https://huggingface.co/docs/transformers/main/en/trainer_recipes#dataloader-performance)[Group samples by length](https://huggingface.co/docs/transformers/main/en/trainer_recipes#group-samples-by-length)[Batch rebalance sampling](https://huggingface.co/docs/transformers/main/en/trainer_recipes#batch-rebalance-sampling)[NEFTune](https://huggingface.co/docs/transformers/main/en/trainer_recipes#neftune)[Logging](https://huggingface.co/docs/transformers/main/en/trainer_recipes#logging)[Checkpointing](https://huggingface.co/docs/transformers/main/en/trainer_recipes#checkpointing)[Resume training](https://huggingface.co/docs/transformers/main/en/trainer_recipes#resume-training)[JIT checkpointing](https://huggingface.co/docs/transformers/main/en/trainer_recipes#jit-checkpointing)
