# Code Map: aip-draft

## Orientation

`/home/graehl/aip-draft` is a Python machine-translation research
prototype with two main runtime families: Hugging Face / PEFT / Unsloth
translation and LoRA training, and TensorRT-LLM engine building / serving /
speculative decoding. A new developer should understand four flows first:
HF translation and scoring (`hf-translate.py`), LoRA training and merging
(`train-lora.py`, `merge_loras_peft.py`), TensorRT engine build and serving
(`save-draft.py`, `serve-draft.py`), and in-flight speculative decode
(`draft_inflight.py`). Shared command-line shape lives in `model_args.py`;
run outputs are tied back to their producers through `artifact_meta.py`.

This report is read-only calibration of the `code-map` skill against the
external checkout. It records static/source traversal only; no shell workflow
scripts, GPU jobs, tests, or `--help` imports were run in `aip-draft`.

## Module Index

| Path | Responsibility | Inputs / Outputs | Key Callers / Callees | Evidence |
|---|---|---|---|---|
| `/home/graehl/aip-draft/AGENTS.md`, `README.md` | Project policy and architecture notes for the draft repo. | Human instructions, workflow constraints, named scripts and model/runtime conventions. | Governs use of `edgepy`, shell scripts, TensorRT-LLM, PEFT, and shared CLI option placement. | verified: `cat AGENTS.md`, `cat README.md` |
| `pyproject.toml` | Python tool configuration. | Python 3.12 target, pyright paths, ruff lint/format policy. | Applies to the whole Python tree. | verified: `cat pyproject.toml` |
| `model_args.py` | Shared argument and Pydantic model definitions. | Adds model, language, dataset, generation, LoRA blend/inference, system-combination, and logging args. | Imported by `hf-translate.py`, `train-lora.py`, `save-draft.py`, `serve-draft.py`, and callers that need `GenerationParams`. | verified: `rg`, `sed` |
| `prompt.py`, `parse_docs.py`, `length_sort.py` | Prompt construction, document/bitext parsing, and length-based ordering helpers. | Source/reference text, prompt specs, optional document boundaries. Outputs prompt groups and sorted aligned files. | Used by `hf-translate.py` and `train-lora.py` before model calls or training examples are built. | verified: source traversal from imports and calls |
| `hf-translate.py` | Main HF translation / evaluation driver. | `-Q` source, optional `-R` reference, model and adapter args, prompt choices, generation and scoring options. Outputs hypothesis files, optional combinations, scores, and artifact metadata. | Calls `model_args`, `prompt`, `length_sort`, `blend`, `mbrs_txt`, `mbr_embed`, `artifact_meta`, PEFT, and Transformers. | verified: `sed -n` over main file |
| `train-lora.py` | LoRA fine-tuning driver. | Source/reference or parsed-doc data, prompt variants, model args, PEFT/Unsloth args, loss-scale settings. Outputs adapter directory, config rewrite, symlink `1 -> .`, optional TRT-converted adapter. | Defines `PromptVariantDataset`, `RegionScaleTrainer`, collator logic, and training `main()`. | verified: `sed -n` over dataset/trainer/main sections |
| `blend.py` | Runtime adapter-output combination math. | LoRA spec strings, per-system logits, blend mode and weights. Outputs blended logits, sampled token, and agreement stats. | Called by `hf-translate.py`; covered by unit tests. | verified: `sed -n`, `tests/unit/test_blend.py` |
| `merge_loras_peft.py`, `merge_lora.py`, `hf_to_trt_lora.py`, `trt_lora_kwargs.py` | Offline adapter merge/convert helpers. | Base model, LoRA adapter specs, merge weights/rank, TensorRT conversion options. Outputs merged PEFT adapter or TRT LoRA artifact. | `hf-translate.py` can use `merge_loras_peft.py` for baked blend mode; `save-draft.py` consumes TRT LoRA config. | verified: `sed -n`, `rg` |
| `mbrs_txt.py`, `mbr_embed.py`, `embed_utils.py`, `bootstrap.py`, `scripts/bootstrap_sig.py` | Scoring, MBR-style selection, embedding support, and significance helpers. | Source/reference/hypothesis files, candidate lists, model/scorer options. Outputs selected hypotheses, scores, and bootstrap comparisons. | Used by `hf-translate.py` after decoding and by research scripts. | verified: file/function inventory |
| `save-draft.py`, `aipquants.py`, `copy_configs.py`, `cuda_cc.py`, `model_meta.py` | TensorRT engine build, quantization/config plumbing, and CUDA capability helpers. | HF model path, quantization options, LoRA module configuration, build flags. Outputs TensorRT engine directories and copied configs. | Calls TensorRT-LLM APIs and local quant/config helpers. | verified: `sed -n`, `rg` |
| `serve-draft.py`, `draft_inflight.py`, `run_draft.py`, `request_args.py`, `parquery.py` | Serving, speculative decode, request plumbing, and parallel query support. | OpenAI-style chat-completion requests, engine paths, generation params, draft/target runners. Outputs API responses and decode metrics. | `serve-draft.py` owns FastAPI routes; `draft_inflight.py` owns queued batched decoding. | verified: `sed -n`, `rg` |
| `artifact_meta.py`, `write_artifact_meta.py`, `log_stats.py`, `log_format.py`, `tee.py`, `cuda_usage.py`, `round_json.py`, `stopping.py` | Run metadata, logging, CUDA telemetry, JSON presentation, and stopping helpers. | Command/run context, metrics, CUDA process state, stopping observations. Outputs sidecars, structured logs, or summary values. | Used by training, decode, scoring, and operator scripts. | verified: file/function inventory |
| `tests/unit`, `tests/integration` | Local regression and integration coverage. | Pytest tests with mocked pipeline paths and focused utilities. | Covers blend math, quant parsing, stopping, CUDA cc, draft metrics, prompt integration, and mocked translation pipeline. | verified: `find tests`, selected `sed -n` reads |
| Root `*.sh`, `scripts/` | Operator workflows and research helpers. | Model/data/job parameters. Outputs logs, scores, artifacts, or long-running GPU work. | Named by README and task workflows, but not executed for this map. | verified: file inventory; not observed |

## Flow Slices

### HF Translation And Evaluation

1. `hf-translate.py -> main()` builds a `DashParser`, then delegates shared
   option groups to `model_args.py`.
2. Input source/reference files are read, optionally length-sorted through
   `length_sort.parallel_files_longest_first`, and wrapped into prompt choices
   via `prompt.resolve_prompt_choices()` / `prompt.prompt_groups()`.
3. The model is loaded through Transformers, optional Unsloth/PEFT hooks, and
   optional adapter logic. In baked blend mode, adapter specs can be resolved
   through `merge_loras_peft.merge_lora_adapters()`.
4. Decode either takes the normal batched `model.generate()` path or a
   token-by-token blend path using `blend.blend_logits()`.
5. Post-decode stages can combine hypotheses, run MBR/embedding selection, run
   MetricX scoring through `mbrs_txt.py`, and write artifacts plus metadata via
   `artifact_meta.py`.

Natural edit points: add shared user-visible options in `model_args.py`; add
new prompt behavior in `prompt.py`; add adapter-combination math in `blend.py`;
add output provenance through `artifact_meta.py`.

Evidence: verified by `rg` for parser/import/function names and source reads of
`hf-translate.py`, `model_args.py`, and `blend.py`.

### LoRA Training

1. `train-lora.py -> main()` parses shared model/language/data args plus
   training-specific options.
2. The source/reference stream comes from direct `-Q/-R` files or parsed-doc
   helpers, then prompt variants are produced using `prompt.prompt_groups()`.
3. `PromptVariantDataset` materializes tokenized prompt/target examples.
4. The collator masks ignored regions and attaches scale metadata through
   `IGNORE_MASK` and `SCALE_MASK`.
5. `RegionScaleTrainer` runs training, computes the scaled loss path, saves the
   PEFT adapter, rewrites config where needed, and creates the `1 -> .` symlink.
6. Optional post-save conversion can call TRT LoRA conversion helpers.

Natural edit points: data/prompt layout in the dataset/collator; loss behavior
in `RegionScaleTrainer`; adapter target choices and shared model args in
`model_args.py`.

Evidence: verified by source reads of `train-lora.py` dataset, trainer, parser,
and final-save sections.

### Adapter Diversity And Merge

1. User-facing blend syntax is parsed by `model_args.add_lora_blend_args()` and
   `blend.parse_lora_specs()`.
2. `hf-translate.py` dispatches between independent outputs, runtime
   logit/probability blend, and baked merge behavior.
3. Runtime blend combines per-system logits in `blend.blend_logits()` with
   modes such as probability sum, logprob sum, power mean, logit sum, and max.
4. Offline merge uses `merge_loras_peft.py` to compute LoRA deltas, sum them,
   factorize by SVD, and write a PEFT adapter.
5. `tests/unit/test_blend.py` anchors parsing, weighting, blend-mode behavior,
   sampling, and agreement helpers.

Natural edit points: syntax and defaults in `model_args.py`; blend math in
`blend.py`; exact/baked adapter math in `merge_loras_peft.py`.

Evidence: verified by source reads of `blend.py`, `merge_loras_peft.py`, and
`tests/unit/test_blend.py`.

### TensorRT Engine Build And Serving

1. `save-draft.py` parses build/model options and constructs TensorRT-LLM
   build config, plugin config, and LoRA module mapping.
2. Quantization and capability decisions route through `aipquants.py` and
   `cuda_cc.py`; copied model/config state routes through `copy_configs.py`.
3. `serve-draft.py` creates a FastAPI app, loads engine runners during the
   lifespan hook, and exposes `/v1/chat/completions`, `/v1/status`, and
   `/v1/shutdown`.
4. Non-streaming generation either uses the standard draft-external path or
   delegates to `draft_inflight.DraftDecoder`.

Natural edit points: build knobs in `save-draft.py` plus shared args in
`model_args.py`; API request/response behavior in `serve-draft.py`; batching
and speculative decode behavior in `draft_inflight.py`.

Evidence: verified by source reads of `save-draft.py`, `serve-draft.py`, and
`draft_inflight.py`.

### In-Flight Speculative Decode

1. `serve-draft.py` receives OpenAI-style chat-completion requests and passes
   per-request generation params into `DraftDecoder`.
2. `DraftDecoder.generate_one()` queues a request with a future; worker state is
   managed through `start_worker()` and `_run_generate()`.
3. The decode loop batches active requests, coordinates draft and target runner
   calls, blends or verifies candidate steps, updates request state, and records
   metrics.
4. Completed futures return text and stats to the serving layer.
5. `tests/integration/test_draft_inflight_acceptance.py` currently exercises a
   metrics-level perfect-acceptance case, not full TensorRT runtime behavior.

Natural edit points: request batching and scheduling in `draft_inflight.py`;
HTTP surface and lifecycle in `serve-draft.py`; metric assertions in the
integration test.

Evidence: verified by source reads of `draft_inflight.py`, `serve-draft.py`,
and `tests/integration/test_draft_inflight_acceptance.py`.

## Contracts And Seams

- Project instructions are operationally binding: use `edgepy`/the `edge`
  environment for local runs, avoid running shell workflow scripts without
  explicit permission, and do not modify `custom_model_runner_cpp.py`.
  Evidence: verified by `AGENTS.md` / `README.md`.
- Shared command-line options belong in `model_args.py` when more than one
  executable needs them. This is the narrowest stable edit point for model,
  language, dataset, generation, LoRA blend/inference, system-combination, and
  logging options. Evidence: verified by `model_args.py` and imports.
- LoRA diversity has two distinct paths: runtime multi-adapter decode through
  `blend.py`, and offline SVD adapter merge through `merge_loras_peft.py`.
  Keep comparisons explicit because runtime blend, sequence-level combination,
  and baked merge do not exercise the same code. Evidence: verified by source
  reads and `tests/unit/test_blend.py`.
- Run provenance should be added where artifacts are written, not afterward.
  `hf-translate.py` already routes output metadata through `artifact_meta.py`.
  Evidence: verified by `rg "artifact_meta" hf-translate.py`.
- The TensorRT runner patch boundary is deliberately sharp:
  `custom_model_runner_cpp.py` is treated as imported upstream/patch code by
  project instructions, so new behavior should be isolated outside it unless
  the project explicitly reopens that boundary. Evidence: verified by
  `AGENTS.md` / `README.md`.

## Blind Spots

- This map did not run tests, `--help`, or import-heavy commands. The target
  repo instructions warn that even help paths can require GPU visibility and
  ML runtime imports, and shell scripts may launch long GPU jobs.
- Dynamic behavior from TensorRT-LLM, Unsloth, PEFT, FastAPI, and CUDA runners
  was not exercised.
- `hf-translate.py` imports `edge_input`, but no tracked file named
  `edge_input*` was found under `/home/graehl/aip-draft` with the static search
  used here. Treat that as an unresolved import/deployment-path blind spot, not
  a verified defect.
- Untracked data/model artifacts, live `.agentctl` state, and research outputs
  were not exhaustively mapped.
- `hf-translate.py` and `train-lora.py` are large orchestration files; the flow
  slices above identify maintainer-relevant entry points, not every branch.

## Reproduce / Refresh

Run from `/home/graehl/aip-draft`:

```bash
git status --short --branch --untracked-files=all
rg --files
cat AGENTS.md
cat README.md
cat pyproject.toml
find tests -maxdepth 2 -type f -print
find research scripts -maxdepth 2 -type f -print
rg -n "^(def|class) |argparse|ArgumentParser|if __name__|FastAPI|@app|add_argument|parse_args|main\\(" *.py scripts tests
sed -n '1,220p' hf-translate.py
sed -n '220,520p' hf-translate.py
sed -n '520,980p' hf-translate.py
sed -n '980,1460p' hf-translate.py
sed -n '1,220p' train-lora.py
sed -n '463,760p' train-lora.py
sed -n '760,1110p' train-lora.py
sed -n '1,220p' serve-draft.py
sed -n '669,940p' serve-draft.py
sed -n '147,360p' draft_inflight.py
sed -n '360,760p' draft_inflight.py
sed -n '1,380p' model_args.py
sed -n '1,180p' blend.py
sed -n '1,260p' save-draft.py
sed -n '260,470p' save-draft.py
sed -n '1,240p' merge_loras_peft.py
sed -n '1,160p' tests/integration/test_translation_pipeline.py
sed -n '1,180p' tests/integration/test_draft_inflight_acceptance.py
sed -n '1,180p' tests/unit/test_blend.py
find /home/graehl/aip-draft -maxdepth 3 -name 'edge_input*' -print
rg -n "edge_input" /home/graehl/aip-draft
```
