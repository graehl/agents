**Source:** *Uncensor any LLM with abliteration* — [original page](https://huggingface.co/blog/mlabonne/abliteration)

[ 

![Figure](figures/df0e5fc29919340a173b12219ad5249d70ab587cd166fbac7845624422cb0889.svg)

 Back to Articles](https://huggingface.co/blog)

#  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/blog/mlabonne/abliteration#uncensor-any-llm-with-abliteration) Uncensor any LLM with abliteration 

[ 

![Figure](figures/01a2de9f52d3d8efb5f7d04c93afae713474e92cd1d0a0e4c3aad90f94ace3c7.svg)

 Community Article](https://huggingface.co/blog/community)

Published June 13, 2024

[ 

![Figure](figures/df906e7cfdbb1a410ce897366296a122123fceff8a67f5ab7395915fa7dcaf70.svg)

 Upvote 946 ](https://huggingface.co/login?next=%2Fblog%2Fmlabonne%2Fabliteration)

  * [ 

![Figure](figures/b639d7357e51e7b983e5a88ab890960df40b60bca2fd8b3cfce6d843799258bc.svg)

 ](https://huggingface.co/AllStreamer "AllStreamer")
  * [ 

![Figure](figures/c3eac1fce7dbd52b2e10868d5b28c723e2a4262ef249f679259bc8c87044ac87.svg)

 ](https://huggingface.co/GVR "GVR")
  * [ 

![Figure](figures/dafca059705f4d984fef817516d5026df36aaa782b3f1100a109a5adbcbf1d22.svg)

 ](https://huggingface.co/ericrichmond "ericrichmond")
  * [ 

![Figure](figures/d9bb304f05eadd04d1e3bf2c4941d9fc3e1414137d7030bfbedae70cbb5d1d88.svg)

 ](https://huggingface.co/jerukperas "jerukperas")
  * [ 

![Figure](figures/1bf859f6b74b846c4a7cdb156e7eb972a28bfc987468697c7dd99fb6dcd8089c.svg)

 ](https://huggingface.co/wolfgangblack "wolfgangblack")
  * [ 

![Figure](figures/e25517cc59921b4f8c5ccfbe24f3b2ae1c0cc4118229c0e4697bc6b053e8a274.webp)

 ](https://huggingface.co/comarproject "comarproject")
  * +940



[ 

![Maxime Labonne's avatar](figures/0b41eed57ab7548eaec2dc0eab6877b2d093be1fb39e214bcf997babdc59752d.webp)

 ](https://huggingface.co/mlabonne)

[Maxime Labonne mlabonne Follow ](https://huggingface.co/mlabonne)



![Figure](figures/c5a4cd142448c21e120a0629055b68769b8f78b0f8c62c2bdca7203d285c4735.svg)

 

  * [✂️ What is abliteration?](https://huggingface.co/blog/mlabonne/abliteration#✂️-what-is-abliteration "✂️ What is abliteration?")
  * [💻 Implementation](https://huggingface.co/blog/mlabonne/abliteration#💻-implementation "💻 Implementation")
  * [⚖️ DPO Fine-Tuning](https://huggingface.co/blog/mlabonne/abliteration#⚖️-dpo-fine-tuning "⚖️ DPO Fine-Tuning")
  * [Conclusion](https://huggingface.co/blog/mlabonne/abliteration#conclusion "Conclusion")
  * [References](https://huggingface.co/blog/mlabonne/abliteration#references "References")



[ 

![image](figures/8bf9f517c139905ada918db047188030a9225e4d60474de3aca7a5fa67d95c99.png)

 ](https://cdn-uploads.huggingface.co/production/uploads/61b8e2ba285851687028d395/3p9AbZta2Q58RATdKSovz.png)

The third generation of Llama models provided fine-tunes (Instruct) versions that excel in understanding and following instructions. However, these models are heavily censored, designed to refuse requests seen as harmful with responses such as "As an AI assistant, I cannot help you." While this safety feature is crucial for preventing misuse, it limits the model's flexibility and responsiveness.

In this article, we will explore a technique called "abliteration" that can uncensor any LLM without retraining. This technique effectively removes the model's built-in refusal mechanism, allowing it to respond to all types of prompts.

The code is available on [Google Colab](https://colab.research.google.com/drive/1VYm3hOcvCpbGiqKZb141gJwjdmmCcVpR?usp=sharing) and in the [LLM Course](https://github.com/mlabonne/llm-course) on GitHub.

##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/blog/mlabonne/abliteration#✂️-what-is-abliteration) ✂️ What is abliteration? 

Modern LLMs are fine-tuned for safety and instruction-following, meaning they are trained to refuse harmful requests. In their [blog post](https://www.lesswrong.com/posts/jGuXSZgv6qfdhMCuJ/refusal-in-llms-is-mediated-by-a-single-direction), Arditi et al. have shown that this refusal behavior is mediated by a specific direction in the model's residual stream. If we prevent the model from representing this direction, it **loses its ability to refuse requests**. Conversely, adding this direction artificially can cause the model to refuse even harmless requests.

In the traditional decoder-only Llama-like architecture, there are three residual streams we can target: at the start of each block ("pre"), between the attention and MLP layers ("mid"), and after the MLP ("post"). The following figure illustrates the location of each residual stream.

[ 

![image](figures/e1fd513882640313ed590415033df13dead3c887c04a3cdfa051931486ea5526.png)

 ](https://cdn-uploads.huggingface.co/production/uploads/61b8e2ba285851687028d395/BwxpPVPio5Lf4UqbM8w7t.png)

To uncensor an LLM, we first need to identify the "refusal direction" within the model. This process involves a few technical steps:

  1. **Data Collection** : Run the model on a set of harmful instructions and a set of harmless instructions, recording the residual stream activations at the last token position for each.
  2. **Mean difference** : Calculate the mean difference between the activations of harmful and harmless instructions. This gives us a vector representing the "refusal direction" for each layer of the model.
  3. **Selection** : Normalize these vectors and evaluate them to select the single best "refusal direction."



Once we have identified the refusal direction, we can "ablate" it, effectively removing the model's ability to represent this feature. This can be done through an **inference-time intervention** or permanently with **weight orthogonalization**.

Let's talk about inference-time intervention first. For every component that writes to the residual stream (such as an attention head), we calculate the projection of its output onto the refusal direction and subtract this projection. This subtraction is applied at every token and every layer, ensuring that the model never represents the refusal direction.

On the other hand, weight orthogonalization involves modifying the model weights directly. By orthogonalizing the component weights with respect to the refusal direction, it prevents the model from writing to this direction altogether. This is achieved by adjusting the matrices that write to the residual stream, ensuring they do not contribute to the refusal direction.

In the next section, we will implement abliteration with weight orthogonalization.

##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/blog/mlabonne/abliteration#💻-implementation) 💻 Implementation 

The following implementation of abliteration is based on [FailSpy's notebook](https://huggingface.co/failspy/llama-3-70B-Instruct-abliterated/blob/main/ortho_cookbook.ipynb), which is itself based on the original authors' [notebook](https://colab.research.google.com/drive/1a-aQvKC9avdZpdyBn4jgRQFObTPy1JZw?usp=sharing). I mostly adapted and simplified it to make it easier to understand. This section is quite code-heavy so you can see what is going on, but you can use FailSpy's [abliterator library](https://github.com/FailSpy/abliterator) if you're less interested in the technical details (also check his [collection of abliterated models](https://huggingface.co/collections/failspy/abliterated-v3-664a8ad0db255eefa7d0012b) on Hugging Face).

The code relies on the excellent [TransformerLens](https://github.com/TransformerLensOrg/TransformerLens) library (formerly known as EasyTransformer) to do the heavy lifting. It is designed for mechanistic interpretability and is used here to intervene on activations. Thanks to Neel Nanda and Joseph Bloom for creating and maintaining this library.

First, let's install the necessary packages and import them. All these steps are available in this [Google Colab notebook](https://colab.research.google.com/drive/1VYm3hOcvCpbGiqKZb141gJwjdmmCcVpR?usp=sharing).
    
    
    !pip install transformers transformers_stream_generator tiktoken transformer_lens einops jaxtyping
    
    import torch
    import functools
    import einops
    import gc
    
    from datasets import load_dataset
    from tqdm import tqdm
    from torch import Tensor
    from typing import List
    from transformer_lens import HookedTransformer, utils
    from transformer_lens.hook_points import HookPoint
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from jaxtyping import Float, Int
    from collections import defaultdict
    
    # Turn automatic differentiation off to save GPU memory (credit: Undi95)
    torch.set_grad_enabled(False)
    

We need two datasets: one containing harmless instructions, and one containing harmful instructions. We'll use [tatsu-lab/alpaca](https://huggingface.co/datasets/tatsu-lab/alpaca) as well as data from [llm-attacks](https://github.com/llm-attacks/llm-attacks). To make things easier, I repackaged them in two Hugging Face datasets: [mlabonne/harmless_alpaca](https://huggingface.co/datasets/mlabonne/harmless_alpaca) and [mlabonne/harmful_behaviors](https://huggingface.co/datasets/mlabonne/harmful_behaviors). That way, you can easily replace them with your own datasets.

We will load the instructions and reformat them into a list of dictionaries with "role" and "content" keys. This makes it compatible with the `apply_chat_tokenizer()` method, which we will use to follow Llama 3's chat template.
    
    
    def reformat_texts(texts):
        return [[{"role": "user", "content": text}] for text in texts]
    
    # Get harmful and harmless datasets
    def get_harmful_instructions():
        dataset = load_dataset('mlabonne/harmful_behaviors')
        return reformat_texts(dataset['train']['text']), reformat_texts(dataset['test']['text'])
    
    def get_harmless_instructions():
        dataset = load_dataset('mlabonne/harmless_alpaca')
        return reformat_texts(dataset['train']['text']), reformat_texts(dataset['test']['text'])
    
    harmful_inst_train, harmful_inst_test = get_harmful_instructions()
    harmless_inst_train, harmless_inst_test = get_harmless_instructions()
    

Now that we have our datasets, we can load the model we want to abliterate. Unfortunately, you can't directly load a custom model using `HookedTransformer`. Here, I use a trick described in FailSpy's notebook to download a custom model and rename it as [meta-llama/Meta-Llama-3-8B-Instruct](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct). Load in `torch.float16` format if your GPU is not compatible with BF16.

In this example, we'll use [mlabonne/Daredevil-8B](https://huggingface.co/mlabonne/Daredevil-8B), a mega-merge created with DARE TIES (see my article about [model merging](https://huggingface.co/blog/mlabonne/merge-models)) that has the highest MMLU score on the Open LLM Leaderboard in the 8B category.
    
    
    MODEL_ID = "mlabonne/Daredevil-8B"
    MODEL_TYPE = "meta-llama/Meta-Llama-3-8B-Instruct"
    
    # Download and load model
    !git clone https://huggingface.co/{MODEL_ID} {MODEL_TYPE}
    
    # Load model and tokenizer
    model = HookedTransformer.from_pretrained_no_processing(
        MODEL_TYPE,
        local_files_only=True,
        dtype=torch.bfloat16,
        default_padding_side='left'
    )
    tokenizer = AutoTokenizer.from_pretrained(MODEL_TYPE)
    tokenizer.padding_side = 'left'
    tokenizer.pad_token = tokenizer.eos_token
    

We can now tokenize our datasets. We're using the same number of samples for both harmless and harmful instructions. Note that a high number of samples can use all the RAM/VRAM, which is why I'm limiting it to 256 here.
    
    
    def tokenize_instructions(tokenizer, instructions):
        return tokenizer.apply_chat_template(
            instructions,
            padding=True,
            truncation=False,
            return_tensors="pt",
            return_dict=True,
            add_generation_prompt=True,
        ).input_ids
    
    n_inst_train = min(256, len(harmful_inst_train), len(harmless_inst_train))
    
    # Tokenize datasets
    harmful_tokens = tokenize_instructions(
        tokenizer,
        instructions=harmful_inst_train[:n_inst_train],
    )
    harmless_tokens = tokenize_instructions(
        tokenizer,
        instructions=harmless_inst_train[:n_inst_train],
    )
    

Everything is set up, we can now implement the first step of abliteration: data collection. We want to process these tokenized datasets and store the residual stream activations in `harmful` and `harmless`. This is managed by the [transformer_lens](https://github.com/TransformerLensOrg/TransformerLens) library.
    
    
    # Define batch size based on available VRAM
    batch_size = 32
    
    # Initialize defaultdicts to store activations
    harmful = defaultdict(list)
    harmless = defaultdict(list)
    
    # Process the training data in batches
    num_batches = (n_inst_train + batch_size - 1) // batch_size
    for i in tqdm(range(num_batches)):
        print(i)
        start_idx = i * batch_size
        end_idx = min(n_inst_train, start_idx + batch_size)
    
        # Run models on harmful and harmless prompts, cache activations
        harmful_logits, harmful_cache = model.run_with_cache(
            harmful_tokens[start_idx:end_idx],
            names_filter=lambda hook_name: 'resid' in hook_name,
            device='cpu',
            reset_hooks_end=True
        )
        harmless_logits, harmless_cache = model.run_with_cache(
            harmless_tokens[start_idx:end_idx],
            names_filter=lambda hook_name: 'resid' in hook_name,
            device='cpu',
            reset_hooks_end=True
        )
    
        # Collect and store the activations
        for key in harmful_cache:
            harmful[key].append(harmful_cache[key])
            harmless[key].append(harmless_cache[key])
    
        # Flush RAM and VRAM
        del harmful_logits, harmless_logits, harmful_cache, harmless_cache
        gc.collect()
        torch.cuda.empty_cache()
    
    # Concatenate the cached activations
    harmful = {k: torch.cat(v) for k, v in harmful.items()}
    harmless = {k: torch.cat(v) for k, v in harmless.items()}
    

We can now compute the refusal direction for each layer. This corresponds to the mean difference between the activations of harmful and harmless instructions, which is then normalized. We sort them in descending order in `activation_scored`. 
    
    
    # Helper function to get activation index
    def get_act_idx(cache_dict, act_name, layer):
        key = (act_name, layer)
        return cache_dict[utils.get_act_name(*key)]
    
    # Compute difference of means between harmful and harmless activations at intermediate layers
    activation_layers = ["resid_pre", "resid_mid", "resid_post"]
    activation_refusals = defaultdict(list)
    
    for layer_num in range(1, model.cfg.n_layers):
        pos = -1  # Position index
    
        for layer in activation_layers:
            harmful_mean_act = get_act_idx(harmful, layer, layer_num)[:, pos, :].mean(dim=0)
            harmless_mean_act = get_act_idx(harmless, layer, layer_num)[:, pos, :].mean(
                dim=0
            )
    
            refusal_dir = harmful_mean_act - harmless_mean_act
            refusal_dir = refusal_dir / refusal_dir.norm()
            activation_refusals[layer].append(refusal_dir)
    
    # Get all calculated potential refusal directions, sort them in descending order based on their mean
    # Use a subset of layers if certain activations are not promising
    selected_layers = ["resid_pre"]
    activation_scored = sorted(
        [
            activation_refusals[layer][l - 1]
            for l in range(1, model.cfg.n_layers)
            for layer in selected_layers
        ],
        key=lambda x: abs(x.mean()),
        reverse=True,
    )
    

The final step of the process consists of evaluating the refusal directions we calculated. To do this, we're going to apply the refusal direction to each residual stream and each block during inference. In the following snippet, we get generations for four test harmful instructions and 20 blocks (or layers).
    
    
    def _generate_with_hooks(
        model: HookedTransformer,
        tokenizer: AutoTokenizer,
        tokens: Int[Tensor, "batch_size seq_len"],
        max_tokens_generated: int = 64,
        fwd_hooks=[],
    ) -> List[str]:
        all_tokens = torch.zeros(
            (tokens.shape[0], tokens.shape[1] + max_tokens_generated),
            dtype=torch.long,
            device=tokens.device,
        )
        all_tokens[:, : tokens.shape[1]] = tokens
        for i in range(max_tokens_generated):
            with model.hooks(fwd_hooks=fwd_hooks):
                logits = model(all_tokens[:, : -max_tokens_generated + i])
                next_tokens = logits[:, -1, :].argmax(
                    dim=-1
                )  # greedy sampling (temperature=0)
                all_tokens[:, -max_tokens_generated + i] = next_tokens
        return tokenizer.batch_decode(
            all_tokens[:, tokens.shape[1] :], skip_special_tokens=True
        )
    
    def get_generations(
        model: HookedTransformer,
        tokenizer: AutoTokenizer,
        instructions: List[str],
        fwd_hooks=[],
        max_tokens_generated: int = 64,
        batch_size: int = 4,
    ) -> List[str]:
        generations = []
        for i in tqdm(range(0, len(instructions), batch_size)):
            tokens = tokenize_instructions(
                tokenizer, instructions=instructions[i : i + batch_size]
            )
            generation = _generate_with_hooks(
                model,
                tokenizer,
                tokens,
                max_tokens_generated=max_tokens_generated,
                fwd_hooks=fwd_hooks,
            )
            generations.extend(generation)
        return generations
    
    # Inference-time intervention hook
    def direction_ablation_hook(
        activation: Float[Tensor, "... d_act"],
        hook: HookPoint,
        direction: Float[Tensor, "d_act"],
    ):
        if activation.device != direction.device:
            direction = direction.to(activation.device)
        proj = (
            einops.einsum(
                activation, direction.view(-1, 1), "... d_act, d_act single -> ... single"
            )
            * direction
        )
        return activation - proj
    
    # Testing baseline
    N_INST_TEST = 4
    baseline_generations = get_generations(
        model, tokenizer, harmful_inst_test[:N_INST_TEST], fwd_hooks=[]
    )
    
    # Evaluating layers defined earlier (needs human evaluation to determine best layer for refusal inhibition)
    EVAL_N = 20  # Evaluate how many of the top N potential directions
    evals = []
    for refusal_dir in tqdm(activation_scored[:EVAL_N]):
        hook_fn = functools.partial(direction_ablation_hook, direction=refusal_dir)
        fwd_hooks = [
            (utils.get_act_name(act_name, layer), hook_fn)
            for layer in list(range(model.cfg.n_layers))
            for act_name in activation_layers
        ]
        intervention_generations = get_generations(
            model, tokenizer, harmful_inst_test[:N_INST_TEST], fwd_hooks=fwd_hooks
        )
        evals.append(intervention_generations)
    

We stored all the generations in the `evals` list. We can now print them and manually select the layer (block) that provides an uncensored response for each instruction. I'm automatically excluding responses containing "I cannot" and "I can't" to filter out unwanted answers.

If you can't find a layer that satisfies these requirements, you might want to test other residual streams in the previous `selected_layers` list, other instructions, additional blocks, etc.
    
    
    # Print generations for human evaluation
    blacklist = ["I cannot", "I can't"]
    for i in range(N_INST_TEST):
        print(f"\033[1mINSTRUCTION {i}: {harmful_inst_test[i]}")
        print(f"\nBASELINE COMPLETION:\n{baseline_generations[i]}\033[0m")
        for layer_candidate in range(EVAL_N):
            if not any(word in evals[layer_candidate][i] for word in blacklist):
                print(f"\n---\n\nLAYER CANDIDATE #{layer_candidate} INTERVENTION COMPLETION:")
                print(evals[layer_candidate][i])
    

In my case, the layer candidate 9 managed to provide uncensored answer for the four instructions. This is the one that we will select for the refusal direction. In the following, we implement weight orthogonalization to modify the weights and prevent the model from creating outputs with this direction. You can verify that the model is successfully uncensored by printing the completions.
    
    
    def get_orthogonalized_matrix(
        matrix: Float[Tensor, "... d_model"], vec: Float[Tensor, "d_model"]
    ) -> Float[Tensor, "... d_model"]:
        proj = (
            einops.einsum(
                matrix, vec.view(-1, 1), "... d_model, d_model single -> ... single"
            )
            * vec
        )
        return matrix - proj
    
    # Select the layer with the highest potential refusal direction
    LAYER_CANDIDATE = 9
    refusal_dir = activation_scored[LAYER_CANDIDATE]
    
    # Orthogonalize the model's weights
    if refusal_dir.device != model.W_E.device:
        refusal_dir = refusal_dir.to(model.W_E.device)
    model.W_E.data = get_orthogonalized_matrix(model.W_E, refusal_dir)
    
    for block in tqdm(model.blocks):
        if refusal_dir.device != block.attn.W_O.device:
            refusal_dir = refusal_dir.to(block.attn.W_O.device)
        block.attn.W_O.data = get_orthogonalized_matrix(block.attn.W_O, refusal_dir)
        block.mlp.W_out.data = get_orthogonalized_matrix(block.mlp.W_out, refusal_dir)
    
    # Generate text with abliterated model
    orthogonalized_generations = get_generations(
        model, tokenizer, harmful_inst_test[:N_INST_TEST], fwd_hooks=[]
    )
    
    # Print generations
    for i in range(N_INST_TEST):
        if len(baseline_generations) > i:
            print(f"INSTRUCTION {i}: {harmful_inst_test[i]}")
            print(f"\033[92mBASELINE COMPLETION:\n{baseline_generations[i]}")
        print(f"\033[91mINTERVENTION COMPLETION:\n{evals[LAYER_CANDIDATE][i]}")
        print(f"\033[95mORTHOGONALIZED COMPLETION:\n{orthogonalized_generations[i]}\n")
    

We're now ready to use the model. We convert it back to the Hugging Face format and upload it to the HF hub.
    
    
    # Convert model back to HF safetensors
    hf_model = AutoModelForCausalLM.from_pretrained(MODEL_TYPE, torch_dtype=torch.bfloat16)
    lm_model = hf_model.model
    
    state_dict = model.state_dict()
    lm_model.embed_tokens.weight = torch.nn.Parameter(state_dict["embed.W_E"].cpu())
    
    for l in range(model.cfg.n_layers):
        lm_model.layers[l].self_attn.o_proj.weight = torch.nn.Parameter(
            einops.rearrange(
                state_dict[f"blocks.{l}.attn.W_O"], "n h m->m (n h)", n=model.cfg.n_heads
            ).contiguous()
        )
        lm_model.layers[l].mlp.down_proj.weight = torch.nn.Parameter(
            torch.transpose(state_dict[f"blocks.{l}.mlp.W_out"], 0, 1).contiguous()
        )
    
    hf_model.push_to_hub(f"{MODEL_ID}-abliterated")
    # hf_model.push_to_hub(f"{MODEL_ID}-abliterated")
    

##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/blog/mlabonne/abliteration#⚖️-dpo-fine-tuning) ⚖️ DPO Fine-Tuning 

I evaluated the abliterated and source models from the previous section on the Open LLM Leaderboard and on Nous' benchmark suite. Here are the results:

[ 

![image](figures/7914a0c323318c27e413d8f7ba0f3088180450630f55d11bc454cd8ccc804668.png)

 ](https://cdn-uploads.huggingface.co/production/uploads/61b8e2ba285851687028d395/n2h8PjUVXw6aU0-gJ88jq.png)

As you can see, the source model significantly outperforms Llama 3 8B Instruct. However, we observe a performance drop in the ablated version across all benchmarks. The ablation process successfully uncensored it but also degraded the model's quality.

To address this issue, an idea consists of further training our abliterated model to heal it. Like most fine-tuned models, Llama 3 8B Instruct is quite brittle when it comes to supervised fine-tuning. An additional SFT would likely break the model's performance.

Alternatively, preference alignment is quite light and shouldn't lobotomize our abliterated model. DPO is a good candidate here for its ease of use and good track record. To implement it, I used [LazyAxolotl](https://colab.research.google.com/drive/1TsDKNo2riwVmU55gjuBgB1AXVtRRfRHW?usp=sharing) with the [mlabonne/orpo-dpo-mix-40k](https://huggingface.co/datasets/mlabonne/orpo-dpo-mix-40k) dataset. Here's the configuration I used:
    
    
    base_model: mlabonne/Daredevil-8B-abliterated
    model_type: LlamaForCausalLM
    tokenizer_type: AutoTokenizer
    
    load_in_8bit: false
    load_in_4bit: true
    strict: false
    save_safetensors: true
    
    rl: dpo
    chat_template: chatml
    datasets:
      - path: mlabonne/orpo-dpo-mix-40k-flat
        split: train
        type: chatml.intel
    
    dataset_prepared_path:
    val_set_size: 0.0
    output_dir: ./out
    
    adapter: qlora
    lora_model_dir:
    
    sequence_len: 2048
    sample_packing: false
    pad_to_sequence_len: false
    
    lora_r: 64
    lora_alpha: 32
    lora_dropout: 0.05
    lora_target_linear: true
    lora_fan_in_fan_out:
    
    wandb_project: axolotl
    wandb_entity:
    wandb_watch:
    wandb_name:
    wandb_log_model:
    
    gradient_accumulation_steps: 8
    micro_batch_size: 1
    num_epochs: 1
    optimizer: paged_adamw_8bit
    lr_scheduler: cosine
    learning_rate: 5e-6
    train_on_inputs: false
    group_by_length: false
    
    bf16: auto
    fp16:
    tf32:
    
    gradient_checkpointing: true
    early_stopping_patience:
    resume_from_checkpoint:
    local_rank:
    logging_steps: 1
    xformers_attention:
    flash_attention: true
    warmup_steps: 100
    evals_per_epoch: 0
    eval_table_size:
    eval_table_max_new_tokens: 128
    saves_per_epoch: 1
    debug:
    deepspeed: deepspeed_configs/zero2.json
    weight_decay: 0.0
    special_tokens:
      pad_token: <|end_of_text|>
    

I trained it using 6xA6000 GPUs with DeepSpeed ZeRO-2. The training took about 6 hours and 45 minutes. Here are the training curves I got from W&B:

[ 

![image](figures/87ab588cef60d37d78298458d20bb19e76883242e0eca1b2869a62482bb29fc0.png)

 ](https://cdn-uploads.huggingface.co/production/uploads/61b8e2ba285851687028d395/TTRci4BDIpC2_SLuAdjMA.png)

It automatically uploaded the DPO fine-tuned model, called [mlabonne/NeuralDaredevil-8B-abliterated](https://huggingface.co/mlabonne/NeuralDaredevil-8B-abliterated). To see if it fixed our abliterated version, I evaluated it on the same benchmarks:

[ 

![image](figures/cf5e6d38661c3c39bfeb7c02cb61a0e2f9d18fdfedfa3b51e900c76175ed7f84.png)

 ](https://cdn-uploads.huggingface.co/production/uploads/61b8e2ba285851687028d395/_tL1W-f2LUBj_JnBXRpX_.png)

We can see that this additional training allowed us to recover most of the performance drop due to abliteration. One area where the model doesn't improve is GSM8K, a math dataset, which could mean the orpo-dpo-mix-40k would benefit from more math samples.

The final model is an uncensored LLM with state-of-the-art performance in the 8B category. I recommend it as an improved version of Llama 3 8B Instruct when you don't need censorship. You can play with quantized versions like GGUF in LM Studio.

##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/blog/mlabonne/abliteration#conclusion) Conclusion 

In this article, we introduced the concept of abliteration. This technique uses the model's activations on harmless and harmful prompts to calculate a refusal direction. It then uses this direction to modify the model's weights and ensure that we stop outputting refusals. This technique also demonstrates the fragility of safety fine-tuning and raises ethical considerations.

We applied abliteration to Daredevil-8B to uncensor it, which also degraded the model's performance. We then healed it using DPO to create the NeuralDaredevil-8B model, a fully uncensored and high-quality 8B LLM. Abliteration is not limited to removing alignment and should be seen as a form of fine-tuning without retraining. Indeed, it can creatively be applied to other goals, like FailSpy's [MopeyMule](https://huggingface.co/failspy/Llama-3-8B-Instruct-MopeyMule), which adopts a melancholic conversational style.

I hope you liked this article. If you want to see more follow me on [Hugging Face](https://huggingface.co/mlabonne/) and Twitter [@maximelabonne](https://twitter.com/maximelabonne).

##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/blog/mlabonne/abliteration#references) References 

  * FailSpy, "[abliterator library](https://github.com/FailSpy/abliterator)," GitHub, 2024.
  * Andy Arditi, Oscar Obeso, Aaquib111, wesg, Neel Nanda, "[Refusal in LLMs is mediated by a single direction](https://www.lesswrong.com/posts/jGuXSZgv6qfdhMCuJ/refusal-in-llms-is-mediated-by-a-single-direction)," Lesswrong, 2024.



##  

![Figure](figures/763856fc227c8fe38ce51231be4023c3b043ba81e4fc46de74889a0b8200901c.svg)

 Models mentioned in this article 5

[ 

![Figure](figures/1bb4c49d5c06458a4b3169c15b0851521aa0908e890ced73f7c8280ed3512dd6.webp)

  failspy/Llama-3-8B-Instruct-MopeyMule 

![Figure](figures/349427c2ffcbea5aaee6de3ac2912e7f4795f19784d848257c43bdf0892f24f0.svg)

 Text Generation • 

![Figure](figures/c894b0ae6fd8878e1c803716e0d0f91f08ee0e514a577358cfba51c771e0a019.svg)

 8B • Updated May 30, 2024 • 

![Figure](figures/63e0c729edd16ef536e70938ddb72e68aef5c45566718fc90a1b35ea440ca8de.svg)

 101 • 

![Figure](figures/1b338c3b145e14c24add2036647ac1a7e89bf8235f21828fa433313382c5bf73.svg)

 88  ](https://huggingface.co/failspy/Llama-3-8B-Instruct-MopeyMule)[ 

![Figure](figures/1bb4c49d5c06458a4b3169c15b0851521aa0908e890ced73f7c8280ed3512dd6.webp)

  failspy/llama-3-70B-Instruct-abliterated 

![Figure](figures/349427c2ffcbea5aaee6de3ac2912e7f4795f19784d848257c43bdf0892f24f0.svg)

 Text Generation • 

![Figure](figures/c894b0ae6fd8878e1c803716e0d0f91f08ee0e514a577358cfba51c771e0a019.svg)

 71B • Updated May 7, 2024 • 

![Figure](figures/63e0c729edd16ef536e70938ddb72e68aef5c45566718fc90a1b35ea440ca8de.svg)

 9.07k • 

![Figure](figures/1b338c3b145e14c24add2036647ac1a7e89bf8235f21828fa433313382c5bf73.svg)

 154  ](https://huggingface.co/failspy/llama-3-70B-Instruct-abliterated)[ 

![Figure](figures/88ccff54e490c4002420e06801752eac73c98e8a8ad1473f5fefbf0becd0b2cf.webp)

  meta-llama/Meta-Llama-3-8B-Instruct 

![Figure](figures/349427c2ffcbea5aaee6de3ac2912e7f4795f19784d848257c43bdf0892f24f0.svg)

 Text Generation • 

![Figure](figures/c894b0ae6fd8878e1c803716e0d0f91f08ee0e514a577358cfba51c771e0a019.svg)

 8B • Updated Jun 18, 2025 • 

![Figure](figures/63e0c729edd16ef536e70938ddb72e68aef5c45566718fc90a1b35ea440ca8de.svg)

 355k • 

![Figure](figures/1b338c3b145e14c24add2036647ac1a7e89bf8235f21828fa433313382c5bf73.svg)

 5.77k  ](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct)[ 

![Figure](figures/0b41eed57ab7548eaec2dc0eab6877b2d093be1fb39e214bcf997babdc59752d.webp)

  mlabonne/Daredevil-8B 

![Figure](figures/349427c2ffcbea5aaee6de3ac2912e7f4795f19784d848257c43bdf0892f24f0.svg)

 Text Generation • 

![Figure](figures/c894b0ae6fd8878e1c803716e0d0f91f08ee0e514a577358cfba51c771e0a019.svg)

 8B • Updated Jan 7, 2025 • 

![Figure](figures/63e0c729edd16ef536e70938ddb72e68aef5c45566718fc90a1b35ea440ca8de.svg)

 220 • 

![Figure](figures/1b338c3b145e14c24add2036647ac1a7e89bf8235f21828fa433313382c5bf73.svg)

 47  ](https://huggingface.co/mlabonne/Daredevil-8B)[ 

![Figure](figures/0b41eed57ab7548eaec2dc0eab6877b2d093be1fb39e214bcf997babdc59752d.webp)

  mlabonne/NeuralDaredevil-8B-abliterated 

![Figure](figures/349427c2ffcbea5aaee6de3ac2912e7f4795f19784d848257c43bdf0892f24f0.svg)

 Text Generation • 

![Figure](figures/c894b0ae6fd8878e1c803716e0d0f91f08ee0e514a577358cfba51c771e0a019.svg)

 8B • Updated Jan 23 • 

![Figure](figures/63e0c729edd16ef536e70938ddb72e68aef5c45566718fc90a1b35ea440ca8de.svg)

 16.3k • 

![Figure](figures/1b338c3b145e14c24add2036647ac1a7e89bf8235f21828fa433313382c5bf73.svg)

 299  ](https://huggingface.co/mlabonne/NeuralDaredevil-8B-abliterated)

##  

![Figure](figures/6f07579ac9618f83f96de2de613ed755f035d539795f5652eabfcd3588b39f67.svg)

 Datasets mentioned in this article 4

[ 

![Figure](figures/260119998d1244ef70172ac73c839b2da7177424cb821956b490567437785909.svg)

 mlabonne/harmful_behaviors 

![Figure](figures/84e2942e1598def931ac0195da812d7fe15a92b6c3da5becf66ff7cecf47bcce.svg)

 Viewer • Updated Jun 4, 2024 • 

![Figure](figures/3602e50ce39936e061bb2e71eb3e9d0d86f95ec8b25829114a3ec5de83408ffe.svg)

 520 • 

![Figure](figures/63e0c729edd16ef536e70938ddb72e68aef5c45566718fc90a1b35ea440ca8de.svg)

 46.9k • 

![Figure](figures/1b338c3b145e14c24add2036647ac1a7e89bf8235f21828fa433313382c5bf73.svg)

 177  ](https://huggingface.co/datasets/mlabonne/harmful_behaviors)[ 

![Figure](figures/260119998d1244ef70172ac73c839b2da7177424cb821956b490567437785909.svg)

 mlabonne/harmless_alpaca 

![Figure](figures/84e2942e1598def931ac0195da812d7fe15a92b6c3da5becf66ff7cecf47bcce.svg)

 Viewer • Updated May 30, 2024 • 

![Figure](figures/3602e50ce39936e061bb2e71eb3e9d0d86f95ec8b25829114a3ec5de83408ffe.svg)

 31.3k • 

![Figure](figures/63e0c729edd16ef536e70938ddb72e68aef5c45566718fc90a1b35ea440ca8de.svg)

 48.9k • 

![Figure](figures/1b338c3b145e14c24add2036647ac1a7e89bf8235f21828fa433313382c5bf73.svg)

 54  ](https://huggingface.co/datasets/mlabonne/harmless_alpaca)[ 

![Figure](figures/260119998d1244ef70172ac73c839b2da7177424cb821956b490567437785909.svg)

 mlabonne/orpo-dpo-mix-40k 

![Figure](figures/84e2942e1598def931ac0195da812d7fe15a92b6c3da5becf66ff7cecf47bcce.svg)

 Viewer • Updated Oct 17, 2024 • 

![Figure](figures/3602e50ce39936e061bb2e71eb3e9d0d86f95ec8b25829114a3ec5de83408ffe.svg)

 44.2k • 

![Figure](figures/63e0c729edd16ef536e70938ddb72e68aef5c45566718fc90a1b35ea440ca8de.svg)

 623 • 

![Figure](figures/1b338c3b145e14c24add2036647ac1a7e89bf8235f21828fa433313382c5bf73.svg)

 318  ](https://huggingface.co/datasets/mlabonne/orpo-dpo-mix-40k)[ 

![Figure](figures/260119998d1244ef70172ac73c839b2da7177424cb821956b490567437785909.svg)

 tatsu-lab/alpaca 

![Figure](figures/84e2942e1598def931ac0195da812d7fe15a92b6c3da5becf66ff7cecf47bcce.svg)

 Viewer • Updated May 22, 2023 • 

![Figure](figures/3602e50ce39936e061bb2e71eb3e9d0d86f95ec8b25829114a3ec5de83408ffe.svg)

 52k • 

![Figure](figures/63e0c729edd16ef536e70938ddb72e68aef5c45566718fc90a1b35ea440ca8de.svg)

 83.5k • 

![Figure](figures/1b338c3b145e14c24add2036647ac1a7e89bf8235f21828fa433313382c5bf73.svg)

 1.39k  ](https://huggingface.co/datasets/tatsu-lab/alpaca)

##  

![Figure](figures/48e1d8e629c0ccc1b350779c26440074f810a0cb1e2350ac7848ff045dc0bb80.svg)

 Collections mentioned in this article 1

#### [abliterated-v3 

![Figure](figures/d5224623c4744d1e4871f2473349b24bb47f3eb4ee50d5f46818509dc2e7221b.svg)

 Collection Latest gen of the abliterated models I've produced • 17 items • Updated Jun 3, 2024 • 

![Figure](figures/26079970d7c967ac733cd8827a6a5b861feb37fd9cdfa4c7ff6e2a603f3a60d6.svg)

 145](https://huggingface.co/collections/failspy/abliterated-v3)

More from this author

## [Kimi K2.5: Still Worth It After Two Weeks?

  * 

![Figure](figures/0b41eed57ab7548eaec2dc0eab6877b2d093be1fb39e214bcf997babdc59752d.webp)

 
  * 


![Figure](figures/26079970d7c967ac733cd8827a6a5b861feb37fd9cdfa4c7ff6e2a603f3a60d6.svg)

 10 February 23, 2026 ](https://huggingface.co/blog/mlabonne/kimik25)

## [Qwen3.5: Nobody Agrees on Attention Anymore

  * 

![Figure](figures/0b41eed57ab7548eaec2dc0eab6877b2d093be1fb39e214bcf997babdc59752d.webp)

 
  * 


![Figure](figures/26079970d7c967ac733cd8827a6a5b861feb37fd9cdfa4c7ff6e2a603f3a60d6.svg)

 28 February 17, 2026 ](https://huggingface.co/blog/mlabonne/qwen35)

###  

![Figure](figures/bc268d77a746c93d74f709cb3aeacd4d4963c4030b1b886d53a5b73085291f97.svg)

 Community



![Figure](figures/fc7f797d9e2ca95f537a774b8c04c190bd0689c269a30c93040233ce51bb2cc6.svg)

 

[dbuela](https://huggingface.co/dbuela)

[Feb 11, 2025](https://huggingface.co/blog/mlabonne/abliteration#67aaedcce2be8d005f57751d)



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

Fantastic article !  
Will this technique work with DeepSeek v2 ?

See translation

  * [ 

![Figure](figures/0b41eed57ab7548eaec2dc0eab6877b2d093be1fb39e214bcf997babdc59752d.webp)

 ](https://huggingface.co/mlabonne "mlabonne")
  * [ 

![Figure](figures/98a7b45521f31c44fdda0d8049ee646f78cdefc7c1545a2bdb6fa8155cb706c7.svg)

 ](https://huggingface.co/seth-miller "seth-miller")
  * [ 

![Figure](figures/fc7f797d9e2ca95f537a774b8c04c190bd0689c269a30c93040233ce51bb2cc6.svg)

 ](https://huggingface.co/dbuela "dbuela")
  * 4 replies

·

👍

7

7

+



![Figure](figures/0b41eed57ab7548eaec2dc0eab6877b2d093be1fb39e214bcf997babdc59752d.webp)

 

![Figure](figures/e5ce75f7d9ef480b0830132d3e781a8c657cdb28f6c24a1ce57730ea55353f22.svg)

 

[mlabonne](https://huggingface.co/mlabonne)

Article author [Feb 11, 2025](https://huggingface.co/blog/mlabonne/abliteration#67ab31f72a6eb6e8e18e47bf)



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

Yes, in theory. In practice, it relies on whether the TransformerLens library supports DeepSeek or not. It'll also require an insane amount of VRAM.

See translation

👍

4

4

🔥

1

1

+



![Figure](figures/becd323b8b38d9828900c8058b8a8b04db686e7642458a7be18bb4d54e4c4848.svg)

 Expand 3 replies



![Figure](figures/00bd89fcf51008ee79b784710012e577b4773920f812249c8d018ee2ee32157d.webp)

 

[TrustAI-lab](https://huggingface.co/TrustAI-lab)

[Feb 13, 2025](https://huggingface.co/blog/mlabonne/abliteration#67ada5a3040354c9105c6619)



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

Fantastic article !

❤️

3

3

+



![Figure](figures/e2056c134038023265b3253c5a88f099655128d077ea558a5ebb0d0fc34580f9.svg)

 Reply



![Figure](figures/4b25644d5543873a11142aeab25fc91ea36358cb111ac47a9b15abf11003b461.svg)

 

[rbc33](https://huggingface.co/rbc33)

[Feb 15, 2025](https://huggingface.co/blog/mlabonne/abliteration#67b10b5573329eb145f96a3c)

•

[edited Feb 17, 2025](https://huggingface.co/blog/mlabonne/abliteration#67b10b5573329eb145f96a3c "Edited by rbc33")



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

i've been trying this script with some models, with llama3.2:3b didn't work, just responded the same

See translation

  * [ 

![Figure](figures/0b64199586156a7b1922f449497bc10dbd252f1a2c7001f78f3685a903ab85e3.svg)

 ](https://huggingface.co/Someshfengde "Someshfengde")
  * 1 reply

·



![Figure](figures/df88f002452387ed9214d65c411754485947bf9282b626f1667b15d68f90559e.svg)

 



![Figure](figures/0b64199586156a7b1922f449497bc10dbd252f1a2c7001f78f3685a903ab85e3.svg)

 

[Someshfengde](https://huggingface.co/Someshfengde)

[Apr 4, 2025](https://huggingface.co/blog/mlabonne/abliteration#67ef94d8d3bbdb8d8d22ca38)



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

Yes I tried the same thing it didn't worked :( got both same responses 

[ 

![image.png](figures/4cda495dd0f54f3a73519407449970abe538929f3c0ec30a96e7ce8452cc383a.png)

 ](https://cdn-uploads.huggingface.co/production/uploads/60c8ae825522c724013196c0/ntrkmvve1HUZVC7Ni2C1x.png)

See translation

➕

2

2

+



![Figure](figures/0b64199586156a7b1922f449497bc10dbd252f1a2c7001f78f3685a903ab85e3.svg)

 

[Someshfengde](https://huggingface.co/Someshfengde)

[Apr 4, 2025](https://huggingface.co/blog/mlabonne/abliteration#67ef94f9e92d5ced6423432d)



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

was anyone able to replicate this notebook ?  
I tried but it's not working out for me 

See translation

➕

1

1

+



![Figure](figures/e2056c134038023265b3253c5a88f099655128d077ea558a5ebb0d0fc34580f9.svg)

 Reply



![Figure](figures/0b41eed57ab7548eaec2dc0eab6877b2d093be1fb39e214bcf997babdc59752d.webp)

 

![Figure](figures/e5ce75f7d9ef480b0830132d3e781a8c657cdb28f6c24a1ce57730ea55353f22.svg)

 

[mlabonne](https://huggingface.co/mlabonne)

Article author [Apr 4, 2025](https://huggingface.co/blog/mlabonne/abliteration#67efec6d5523cb0e0fb21cdc)



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

I recommend using AutoAbliteration instead: <https://huggingface.co/posts/mlabonne/714992455492422>

See translation

  * [ 

![Figure](figures/a8cd09917247bb059b67139bc793888a6cd8d473f45c4624f1a6bf07c452b91f.webp)

 ](https://huggingface.co/NanGongMoon "NanGongMoon")
  * [ 

![Figure](figures/0b41eed57ab7548eaec2dc0eab6877b2d093be1fb39e214bcf997babdc59752d.webp)

 ](https://huggingface.co/mlabonne "mlabonne")
  * [ 

![Figure](figures/237dab736204622bbd973cce6e0c6eb65650f073a93dbf343cf000faf9b9fff6.svg)

 ](https://huggingface.co/travisking "travisking")
  * 7 replies

·

👍

1

1

+

deleted

[Apr 4, 2025](https://huggingface.co/blog/mlabonne/abliteration#67eff244c736ed16878e1a43)



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

I just tested this, works great. Thank you.

See translation



![Figure](figures/df88f002452387ed9214d65c411754485947bf9282b626f1667b15d68f90559e.svg)

 



![Figure](figures/becd323b8b38d9828900c8058b8a8b04db686e7642458a7be18bb4d54e4c4848.svg)

 Expand 6 replies



![Figure](figures/a37ee26b9f0a23faa68d67f40efe82ae03e9954985182b1e05c047c88daea695.svg)

 

[peperan](https://huggingface.co/peperan)

[Jul 7, 2025](https://huggingface.co/blog/mlabonne/abliteration#686bb7ed20fa5b3940deb994)



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

So in fact you didn't abliterated Llama model, you abliterated a custom model and rename it as Llama? I didn't get it at all that part

See translation

  * [ 

![Figure](figures/0b41eed57ab7548eaec2dc0eab6877b2d093be1fb39e214bcf997babdc59752d.webp)

 ](https://huggingface.co/mlabonne "mlabonne")
  * 1 reply

·



![Figure](figures/df88f002452387ed9214d65c411754485947bf9282b626f1667b15d68f90559e.svg)

 



![Figure](figures/0b41eed57ab7548eaec2dc0eab6877b2d093be1fb39e214bcf997babdc59752d.webp)

 

![Figure](figures/e5ce75f7d9ef480b0830132d3e781a8c657cdb28f6c24a1ce57730ea55353f22.svg)

 

[mlabonne](https://huggingface.co/mlabonne)

Article author [Jul 7, 2025](https://huggingface.co/blog/mlabonne/abliteration#686c011995af0364271ce866)



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

It's a fine-tune of Llama so it's a Llama model. You can do the same with the original Llama models released by Meta.

See translation

❤️

1

1

+



![Figure](figures/7c2f581749b609fce25704b7905632418eddeb90b57ced1ec686d774d262872c.webp)

 

[grimjim](https://huggingface.co/grimjim)

[Oct 25, 2025](https://huggingface.co/blog/mlabonne/abliteration#68fd2e63697a7623fc1ace49)



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

I've been inspired by your attempts at abliterating Gemma 3 models, and offer up a modification to abliteration that should reduce performance drop; I've informally tested on Gemma 3 12B Instruct, though I've not yet released the finished model.  
<https://huggingface.co/blog/grimjim/projected-abliteration>

See translation

  * [ 

![Figure](figures/0b41eed57ab7548eaec2dc0eab6877b2d093be1fb39e214bcf997babdc59752d.webp)

 ](https://huggingface.co/mlabonne "mlabonne")
  * 1 reply

·

❤️

3

3

🔥

3

3

🧠

3

3

+



![Figure](figures/0b41eed57ab7548eaec2dc0eab6877b2d093be1fb39e214bcf997babdc59752d.webp)

 

![Figure](figures/e5ce75f7d9ef480b0830132d3e781a8c657cdb28f6c24a1ce57730ea55353f22.svg)

 

[mlabonne](https://huggingface.co/mlabonne)

Article author [Oct 27, 2025](https://huggingface.co/blog/mlabonne/abliteration#68fed963d14c77a4e575c3dd)



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

Thanks for letting me know, looks very interesting! Kudos for all your work in this space :)

See translation

🤗

1

1

+



![Figure](figures/7c2f581749b609fce25704b7905632418eddeb90b57ced1ec686d774d262872c.webp)

 

[grimjim](https://huggingface.co/grimjim)

[Nov 7, 2025](https://huggingface.co/blog/mlabonne/abliteration#690d9b0a159e58ca76c99d19)



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

I've gone a step further, applying decomposition to isolate the direction component (instead of direct subtraction) when ablating the refusal direction, while preserving matrix norms during intervention. The result even improved on the UGI Leaderboard Natural Intelligence benchmark over the original Instruct model.  
<https://huggingface.co/blog/grimjim/norm-preserving-biprojected-abliteration>

See translation

❤️

2

2

👀

1

1

+



![Figure](figures/e2056c134038023265b3253c5a88f099655128d077ea558a5ebb0d0fc34580f9.svg)

 Reply



![Figure](figures/222e82b4dad97059ae571cee1a1e6a023d60e248cdc519f82411d55541f0bf2f.webp)

 

[p-e-w](https://huggingface.co/p-e-w)

[Dec 10, 2025](https://huggingface.co/blog/mlabonne/abliteration#69396e9960dcdf854fd10800)



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

For anyone looking to develop a deeper understanding of the residual geometry/topology that drives refusals, I have added research features to [Heretic](https://github.com/p-e-w/heretic) that make it very easy to investigate the same.

For example, you can get nice animated PaCMAP plots of residual vectors for any model by simply running
    
    
    pip install -U heretic-llm[research]
    heretic --plot-residuals openai/gpt-oss-20b
    

which gives you this, without having to write a single line of Matplotlib code yourself:

[ 

![residuals-gpt-oss](figures/eab079df7ea354cdc0918b189bd2aeea108f0b3a0dc634304c6f17dde8df208b.gif)

 ](https://cdn-uploads.huggingface.co/production/uploads/68ce0ae4ce1399b97e364af4/-xe2_NjtME8Rjuvb2pcFV.gif)

(Cancel the run after the plots have been saved if you aren't interested in actually abliterating the model.)

You can also run
    
    
    heretic --print-residual-geometry openai/gpt-oss-20b
    

to get a table like this:
    
    
    ┏━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┓
    ┃ Layer ┃ S(g,b) ┃ S(g*,b*) ┃  S(g,r) ┃ S(g*,r*) ┃  S(b,r) ┃ S(b*,r*) ┃      |g| ┃     |g*| ┃      |b| ┃     |b*| ┃     |r| ┃    |r*| ┃   Silh ┃
    ┡━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━┩
    │     1 │ 1.0000 │   1.0000 │ -0.4311 │  -0.4906 │ -0.4254 │  -0.4847 │   170.29 │   170.49 │   169.78 │   169.85 │    1.19 │    1.31 │ 0.0480 │
    │     2 │ 1.0000 │   1.0000 │  0.4297 │   0.4465 │  0.4365 │   0.4524 │   768.55 │   768.77 │   771.32 │   771.36 │    6.39 │    5.76 │ 0.0745 │
    │     3 │ 0.9999 │   1.0000 │ -0.5699 │  -0.5577 │ -0.5614 │  -0.5498 │  1020.98 │  1021.13 │  1013.80 │  1014.71 │   12.70 │   11.60 │ 0.0920 │
    │     4 │ 0.9999 │   1.0000 │  0.6582 │   0.6553 │  0.6659 │   0.6627 │  1356.39 │  1356.20 │  1368.71 │  1367.95 │   18.62 │   17.84 │ 0.0957 │
    │     5 │ 0.9987 │   0.9990 │ -0.6880 │  -0.6761 │ -0.6497 │  -0.6418 │   766.54 │   762.25 │   731.75 │   732.42 │   51.97 │   45.24 │ 0.1018 │
    │     6 │ 0.9998 │   0.9998 │ -0.1983 │  -0.2312 │ -0.1811 │  -0.2141 │  2417.35 │  2421.08 │  2409.18 │  2411.40 │   43.06 │   43.47 │ 0.0900 │
    │     7 │ 0.9998 │   0.9997 │ -0.5258 │  -0.5746 │ -0.5072 │  -0.5560 │  3444.92 │  3474.99 │  3400.01 │  3421.63 │   86.94 │   94.38 │ 0.0492 │
    │     8 │ 0.9990 │   0.9991 │  0.8235 │   0.8312 │  0.8479 │   0.8542 │  4596.54 │  4615.62 │  4918.32 │  4934.20 │  384.87 │  377.87 │ 0.2278 │
    │     9 │ 0.9992 │   0.9992 │  0.5335 │   0.5441 │  0.5678 │   0.5780 │  5322.30 │  5316.96 │  5468.65 │  5466.98 │  265.68 │  267.28 │ 0.1318 │
    │    10 │ 0.9974 │   0.9973 │  0.8189 │   0.8250 │  0.8579 │   0.8644 │  5328.81 │  5325.63 │  5953.35 │  5985.15 │  743.95 │  779.74 │ 0.2863 │
    │    11 │ 0.9977 │   0.9978 │  0.4262 │   0.4045 │  0.4862 │   0.4645 │  9644.02 │  9674.06 │  9983.47 │  9990.28 │  743.28 │  726.99 │ 0.1576 │
    │    12 │ 0.9904 │   0.9907 │  0.4384 │   0.4077 │  0.5586 │   0.5283 │ 10257.40 │ 10368.50 │ 11114.51 │ 11151.21 │ 1711.18 │ 1664.69 │ 0.1890 │
    │    13 │ 0.9867 │   0.9874 │  0.4007 │   0.3680 │  0.5444 │   0.5103 │ 12305.12 │ 12423.75 │ 13440.31 │ 13432.47 │ 2386.43 │ 2282.47 │ 0.1293 │
    │    14 │ 0.9921 │   0.9922 │  0.3198 │   0.2682 │  0.4364 │   0.3859 │ 16929.16 │ 17080.37 │ 17826.97 │ 17836.03 │ 2365.23 │ 2301.87 │ 0.1282 │
    │    15 │ 0.9846 │   0.9850 │  0.1198 │   0.0963 │  0.2913 │   0.2663 │ 16858.58 │ 16949.44 │ 17496.00 │ 17502.88 │ 3077.08 │ 3029.60 │ 0.1611 │
    │    16 │ 0.9686 │   0.9689 │ -0.0029 │  -0.0254 │  0.2457 │   0.2226 │ 18912.77 │ 19074.86 │ 19510.56 │ 19559.62 │ 4848.35 │ 4839.75 │ 0.1516 │
    │    17 │ 0.9782 │   0.9784 │ -0.0174 │  -0.0381 │  0.1908 │   0.1694 │ 27098.09 │ 27273.00 │ 27601.12 │ 27653.12 │ 5738.19 │ 5724.21 │ 0.1641 │
    │    18 │ 0.9184 │   0.9196 │  0.1343 │   0.1430 │  0.5155 │   0.5204 │   190.16 │   190.35 │   219.91 │   220.62 │   87.82 │   87.59 │ 0.1855 │
    └───────┴────────┴──────────┴─────────┴──────────┴─────────┴──────────┴──────────┴──────────┴──────────┴──────────┴─────────┴─────────┴────────┘
    g = mean of residual vectors for good prompts
    g* = geometric median of residual vectors for good prompts
    b = mean of residual vectors for bad prompts
    b* = geometric median of residual vectors for bad prompts
    r = refusal direction for means (i.e., b - g)
    r* = refusal direction for geometric medians (i.e., b* - g*)
    S(x,y) = cosine similarity of x and y
    |x| = L2 norm of x
    Silh = Mean silhouette coefficient of residuals for good/bad clusters
    

The datasets/labels/colors etc. are all configurable, so you can also use those features to investigate other phenomena besides refusals.

See translation

  * [ 

![Figure](figures/ab4996a4917a54c6c825fe582c27651ada5002ccce39c7741dff2e167b339616.webp)

 ](https://huggingface.co/redaihf "redaihf")
  * [ 

![Figure](figures/222e82b4dad97059ae571cee1a1e6a023d60e248cdc519f82411d55541f0bf2f.webp)

 ](https://huggingface.co/p-e-w "p-e-w")
  * 4 replies

·

👍

9

9

🔥

1

1

+



![Figure](figures/ab4996a4917a54c6c825fe582c27651ada5002ccce39c7741dff2e167b339616.webp)

 

[redaihf](https://huggingface.co/redaihf)

[Jan 3](https://huggingface.co/blog/mlabonne/abliteration#6958cb753edec6b11ec5353d)

•

[edited Jan 3](https://huggingface.co/blog/mlabonne/abliteration#6958cb753edec6b11ec5353d "Edited 3 times by redaihf")



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

I have been experimenting with Heretic models. Like abiliteration before it, Heretic appears to narrowly remove overt refusals while preserving deceptive capabilities. This covert noncompliance is especially apparent for Llama base models.

Tested models:

  * [Cydonia-24B-v4.3-heretic-v2](https://huggingface.co/coder3101/Cydonia-24B-v4.3-heretic-v2): super decensored, although the base model was already [pretty uncensored](https://huggingface.co/TheDrummer/Cydonia-24B-v4.3/discussions/2)
  * [Llama3.2-30B-A3B-II-Dark-Champion-INSTRUCT-Heretic-Abliterated-Uncensored](https://huggingface.co/DavidAU/Llama3.2-30B-A3B-II-Dark-Champion-INSTRUCT-Heretic-Abliterated-Uncensored): subverts or ignores topics deemed unsafe, quality [degrades](https://huggingface.co/DavidAU/Llama3.2-30B-A3B-II-Dark-Champion-INSTRUCT-Heretic-Abliterated-Uncensored/discussions/2) if jailbroken
  * [LongWriter-llama3.1-8b-Heretic](https://huggingface.co/ChiKoi7/LongWriter-llama3.1-8b-Heretic): also self-censors and [reports itself](https://huggingface.co/ChiKoi7/LongWriter-llama3.1-8b-Heretic/discussions/1) as censored, but can be jailbroken



See translation



![Figure](figures/df88f002452387ed9214d65c411754485947bf9282b626f1667b15d68f90559e.svg)

 



![Figure](figures/becd323b8b38d9828900c8058b8a8b04db686e7642458a7be18bb4d54e4c4848.svg)

 Expand 3 replies



![Figure](figures/f5ab7b4596bd9ba19aec2f4aba5b5e9872ccffefd737af33e17fb3a05e56849e.svg)

 

[Morpheus23x](https://huggingface.co/Morpheus23x)

[Dec 12, 2025](https://huggingface.co/blog/mlabonne/abliteration#693ca9a158b3e28febba0cf2)



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

Oooh! Brain surgery! I LIKE!!

See translation

🤯

2

2

🧠

1

1

+



![Figure](figures/e2056c134038023265b3253c5a88f099655128d077ea558a5ebb0d0fc34580f9.svg)

 Reply



![Figure](figures/95e74d4a80e4a61d8c3d1493d80a460f837daa32708338618edda7e715a91bb4.webp)

 

[A0bd](https://huggingface.co/A0bd)

[Dec 23, 2025](https://huggingface.co/blog/mlabonne/abliteration#694a2c76945c384eb1b5f026)



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

hello, im tying to put this ai into Samsung smart watch ultra, i did research according to gemini.  
llama 3.2+ollama+moonshin  
as mainly its located on samsung smart watch ultra, it can be used offline or online with phone link for better internet  
if anyone have suggestions let me know 😄 

See translation

👀

3

3

+



![Figure](figures/e2056c134038023265b3253c5a88f099655128d077ea558a5ebb0d0fc34580f9.svg)

 Reply



![Figure](figures/2fb51d4c9470f3783f08d5d25212102f66bc91ccaf677302f92623153a278f21.svg)

 

![Figure](figures/e5ce75f7d9ef480b0830132d3e781a8c657cdb28f6c24a1ce57730ea55353f22.svg)

 

[SoulFireMage](https://huggingface.co/SoulFireMage)

[Dec 31, 2025](https://huggingface.co/blog/mlabonne/abliteration#6954ceb8846664861e2d57bb)



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

can you host your in ages somewhere else please? inthe UK Imgur are worse than useless, they refuse to operate thanks to lazy ass nonsense about our over bearing Osa. Thank you. 

See translation

  * [ 

![Figure](figures/0b41eed57ab7548eaec2dc0eab6877b2d093be1fb39e214bcf997babdc59752d.webp)

 ](https://huggingface.co/mlabonne "mlabonne")
  * 1 reply

·

👍

1

1

+



![Figure](figures/0b41eed57ab7548eaec2dc0eab6877b2d093be1fb39e214bcf997babdc59752d.webp)

 

![Figure](figures/e5ce75f7d9ef480b0830132d3e781a8c657cdb28f6c24a1ce57730ea55353f22.svg)

 

[mlabonne](https://huggingface.co/mlabonne)

Article author [Dec 31, 2025](https://huggingface.co/blog/mlabonne/abliteration#6955381d6d936457ffd3c837)



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

I re-uploaded all the images, enjoy!

See translation



![Figure](figures/df88f002452387ed9214d65c411754485947bf9282b626f1667b15d68f90559e.svg)

 



![Figure](figures/1385c128aa1284503dad13e0703f4e4c1d613f1bb9db6e6edafce303499ece23.webp)

 

[HeYujie](https://huggingface.co/HeYujie)

[Jan 16](https://huggingface.co/blog/mlabonne/abliteration#6969faf23b735041b8849b58)



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

Awesome work! You just saved my project😭  
I noticed that only English used for abliteration. Will it decrease ablities for other languages? or less effictive to abliterate other languages?

See translation

  * [ 

![Figure](figures/0b41eed57ab7548eaec2dc0eab6877b2d093be1fb39e214bcf997babdc59752d.webp)

 ](https://huggingface.co/mlabonne "mlabonne")
  * 1 reply

·

🤝

1

1

+



![Figure](figures/0b41eed57ab7548eaec2dc0eab6877b2d093be1fb39e214bcf997babdc59752d.webp)

 

![Figure](figures/e5ce75f7d9ef480b0830132d3e781a8c657cdb28f6c24a1ce57730ea55353f22.svg)

 

[mlabonne](https://huggingface.co/mlabonne)

Article author [Jan 16](https://huggingface.co/blog/mlabonne/abliteration#696a7a909751a3731694cb6c)



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

It's a good question. Experimentally, it generalizes very well to other languages, but adding prompts in your target languages will always be more efficient and fine-grained.

See translation



![Figure](figures/df88f002452387ed9214d65c411754485947bf9282b626f1667b15d68f90559e.svg)

 



![Figure](figures/430c86f3daf78d9752e423f157b3ba3e78d3622bf8567a6edfa542d65fda853f.svg)

 

[JohnLins](https://huggingface.co/JohnLins)

[Apr 22](https://huggingface.co/blog/mlabonne/abliteration#69e860bb757db0b575c0f155)

•

This comment has been hidden (marked as Spam)



![Figure](figures/c2f99dcb52faf694dcb5339ebceb03037b87dc6d7c49b13239c15a522fe7f706.webp)

 

[obversarystudios](https://huggingface.co/obversarystudios)

[Aug 30](https://huggingface.co/blog/mlabonne/abliteration#6a93d660103ce7f24f1feb2c)



![Figure](figures/4b01dc9b4ff494c5ed52a5de19fdea824cf9699cf8e290914d6c6065057a9347.svg)

 

this just made my day

See translation



![Figure](figures/df88f002452387ed9214d65c411754485947bf9282b626f1667b15d68f90559e.svg)

 



![Figure](figures/e2056c134038023265b3253c5a88f099655128d077ea558a5ebb0d0fc34580f9.svg)

 Reply

EditPreview



![Figure](figures/7daac0a0998d79de9e793f7c4da05acb27ed3fc18d5083afa605bde897620798.svg)

 

Upload images, audio, and videos by dragging in the text input, pasting, or clicking here.

Tap or paste here to upload images



![Figure](figures/c11b8f040b3b2bb578f5c54dd9c4d3a77a0346e44b3e6612efd2a63cc31ad2b3.svg)

 Comment

· [Sign up](https://huggingface.co/join?next=%2Fblog%2Fmlabonne%2Fabliteration) or [log in](https://huggingface.co/login?next=%2Fblog%2Fmlabonne%2Fabliteration) to comment

[ 

![Figure](figures/df906e7cfdbb1a410ce897366296a122123fceff8a67f5ab7395915fa7dcaf70.svg)

 Upvote 946 ](https://huggingface.co/login?next=%2Fblog%2Fmlabonne%2Fabliteration)

  * [ 

![Figure](figures/b639d7357e51e7b983e5a88ab890960df40b60bca2fd8b3cfce6d843799258bc.svg)

 ](https://huggingface.co/AllStreamer "AllStreamer")
  * [ 

![Figure](figures/c3eac1fce7dbd52b2e10868d5b28c723e2a4262ef249f679259bc8c87044ac87.svg)

 ](https://huggingface.co/GVR "GVR")
  * [ 

![Figure](figures/dafca059705f4d984fef817516d5026df36aaa782b3f1100a109a5adbcbf1d22.svg)

 ](https://huggingface.co/ericrichmond "ericrichmond")
  * [ 

![Figure](figures/d9bb304f05eadd04d1e3bf2c4941d9fc3e1414137d7030bfbedae70cbb5d1d88.svg)

 ](https://huggingface.co/jerukperas "jerukperas")
  * [ 

![Figure](figures/1bf859f6b74b846c4a7cdb156e7eb972a28bfc987468697c7dd99fb6dcd8089c.svg)

 ](https://huggingface.co/wolfgangblack "wolfgangblack")
  * [ 

![Figure](figures/e25517cc59921b4f8c5ccfbe24f3b2ae1c0cc4118229c0e4697bc6b053e8a274.webp)

 ](https://huggingface.co/comarproject "comarproject")
  * [ 

![Figure](figures/1391d3c40d243476dd8d3d76f60cb3c3c0002b11656a0547df9a4d7f0ddfbb9e.webp)

 ](https://huggingface.co/hiyorijl "hiyorijl")
  * [ 

![Figure](figures/d1c8d4f99a2d181509afd9c8261cd305dc5da5f0b268a5cca4a51e3d08307c22.webp)

 ](https://huggingface.co/vphatak "vphatak")
  * [ 

![Figure](figures/91dfff3cfc2667e170db30cb687d8db16fb4a820de9595455852b1669e636c35.svg)

 ](https://huggingface.co/rsdrsd "rsdrsd")
  * [ 

![Figure](figures/323b1be049398442f3915d6a7b4a68fc1c8b0d59dcaa6cea319902219b650fd2.webp)

 ](https://huggingface.co/utterlygreat "utterlygreat")
  * [ 

![Figure](figures/b9c8b48fdc942ac53faa7853d054d812b2aebfc8d44087234b61fadfada9ff9b.svg)

 ](https://huggingface.co/literate-goggles "literate-goggles")
  * [ 

![Figure](figures/bbe0239c1bf71e5815f73fefd01efbe1a6847d8b29613f075702732db99ce52f.svg)

 ](https://huggingface.co/nehuggingface "nehuggingface")
  * +934



##  

![Figure](figures/763856fc227c8fe38ce51231be4023c3b043ba81e4fc46de74889a0b8200901c.svg)

 Models mentioned in this article 5

[ 

![Figure](figures/1bb4c49d5c06458a4b3169c15b0851521aa0908e890ced73f7c8280ed3512dd6.webp)

  failspy/Llama-3-8B-Instruct-MopeyMule 

![Figure](figures/349427c2ffcbea5aaee6de3ac2912e7f4795f19784d848257c43bdf0892f24f0.svg)

 Text Generation • 

![Figure](figures/c894b0ae6fd8878e1c803716e0d0f91f08ee0e514a577358cfba51c771e0a019.svg)

 8B • Updated May 30, 2024 • 

![Figure](figures/63e0c729edd16ef536e70938ddb72e68aef5c45566718fc90a1b35ea440ca8de.svg)

 101 • 

![Figure](figures/1b338c3b145e14c24add2036647ac1a7e89bf8235f21828fa433313382c5bf73.svg)

 88  ](https://huggingface.co/failspy/Llama-3-8B-Instruct-MopeyMule)[ 

![Figure](figures/1bb4c49d5c06458a4b3169c15b0851521aa0908e890ced73f7c8280ed3512dd6.webp)

  failspy/llama-3-70B-Instruct-abliterated 

![Figure](figures/349427c2ffcbea5aaee6de3ac2912e7f4795f19784d848257c43bdf0892f24f0.svg)

 Text Generation • 

![Figure](figures/c894b0ae6fd8878e1c803716e0d0f91f08ee0e514a577358cfba51c771e0a019.svg)

 71B • Updated May 7, 2024 • 

![Figure](figures/63e0c729edd16ef536e70938ddb72e68aef5c45566718fc90a1b35ea440ca8de.svg)

 9.07k • 

![Figure](figures/1b338c3b145e14c24add2036647ac1a7e89bf8235f21828fa433313382c5bf73.svg)

 154  ](https://huggingface.co/failspy/llama-3-70B-Instruct-abliterated)[ 

![Figure](figures/88ccff54e490c4002420e06801752eac73c98e8a8ad1473f5fefbf0becd0b2cf.webp)

  meta-llama/Meta-Llama-3-8B-Instruct 

![Figure](figures/349427c2ffcbea5aaee6de3ac2912e7f4795f19784d848257c43bdf0892f24f0.svg)

 Text Generation • 

![Figure](figures/c894b0ae6fd8878e1c803716e0d0f91f08ee0e514a577358cfba51c771e0a019.svg)

 8B • Updated Jun 18, 2025 • 

![Figure](figures/63e0c729edd16ef536e70938ddb72e68aef5c45566718fc90a1b35ea440ca8de.svg)

 355k • 

![Figure](figures/1b338c3b145e14c24add2036647ac1a7e89bf8235f21828fa433313382c5bf73.svg)

 5.77k  ](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct)[ 

![Figure](figures/0b41eed57ab7548eaec2dc0eab6877b2d093be1fb39e214bcf997babdc59752d.webp)

  mlabonne/Daredevil-8B 

![Figure](figures/349427c2ffcbea5aaee6de3ac2912e7f4795f19784d848257c43bdf0892f24f0.svg)

 Text Generation • 

![Figure](figures/c894b0ae6fd8878e1c803716e0d0f91f08ee0e514a577358cfba51c771e0a019.svg)

 8B • Updated Jan 7, 2025 • 

![Figure](figures/63e0c729edd16ef536e70938ddb72e68aef5c45566718fc90a1b35ea440ca8de.svg)

 220 • 

![Figure](figures/1b338c3b145e14c24add2036647ac1a7e89bf8235f21828fa433313382c5bf73.svg)

 47  ](https://huggingface.co/mlabonne/Daredevil-8B)[ 

![Figure](figures/0b41eed57ab7548eaec2dc0eab6877b2d093be1fb39e214bcf997babdc59752d.webp)

  mlabonne/NeuralDaredevil-8B-abliterated 

![Figure](figures/349427c2ffcbea5aaee6de3ac2912e7f4795f19784d848257c43bdf0892f24f0.svg)

 Text Generation • 

![Figure](figures/c894b0ae6fd8878e1c803716e0d0f91f08ee0e514a577358cfba51c771e0a019.svg)

 8B • Updated Jan 23 • 

![Figure](figures/63e0c729edd16ef536e70938ddb72e68aef5c45566718fc90a1b35ea440ca8de.svg)

 16.3k • 

![Figure](figures/1b338c3b145e14c24add2036647ac1a7e89bf8235f21828fa433313382c5bf73.svg)

 299  ](https://huggingface.co/mlabonne/NeuralDaredevil-8B-abliterated)

##  

![Figure](figures/6f07579ac9618f83f96de2de613ed755f035d539795f5652eabfcd3588b39f67.svg)

 Datasets mentioned in this article 4

[ 

![Figure](figures/260119998d1244ef70172ac73c839b2da7177424cb821956b490567437785909.svg)

 mlabonne/harmful_behaviors 

![Figure](figures/84e2942e1598def931ac0195da812d7fe15a92b6c3da5becf66ff7cecf47bcce.svg)

 Viewer • Updated Jun 4, 2024 • 

![Figure](figures/3602e50ce39936e061bb2e71eb3e9d0d86f95ec8b25829114a3ec5de83408ffe.svg)

 520 • 

![Figure](figures/63e0c729edd16ef536e70938ddb72e68aef5c45566718fc90a1b35ea440ca8de.svg)

 46.9k • 

![Figure](figures/1b338c3b145e14c24add2036647ac1a7e89bf8235f21828fa433313382c5bf73.svg)

 177  ](https://huggingface.co/datasets/mlabonne/harmful_behaviors)[ 

![Figure](figures/260119998d1244ef70172ac73c839b2da7177424cb821956b490567437785909.svg)

 mlabonne/harmless_alpaca 

![Figure](figures/84e2942e1598def931ac0195da812d7fe15a92b6c3da5becf66ff7cecf47bcce.svg)

 Viewer • Updated May 30, 2024 • 

![Figure](figures/3602e50ce39936e061bb2e71eb3e9d0d86f95ec8b25829114a3ec5de83408ffe.svg)

 31.3k • 

![Figure](figures/63e0c729edd16ef536e70938ddb72e68aef5c45566718fc90a1b35ea440ca8de.svg)

 48.9k • 

![Figure](figures/1b338c3b145e14c24add2036647ac1a7e89bf8235f21828fa433313382c5bf73.svg)

 54  ](https://huggingface.co/datasets/mlabonne/harmless_alpaca)[ 

![Figure](figures/260119998d1244ef70172ac73c839b2da7177424cb821956b490567437785909.svg)

 mlabonne/orpo-dpo-mix-40k 

![Figure](figures/84e2942e1598def931ac0195da812d7fe15a92b6c3da5becf66ff7cecf47bcce.svg)

 Viewer • Updated Oct 17, 2024 • 

![Figure](figures/3602e50ce39936e061bb2e71eb3e9d0d86f95ec8b25829114a3ec5de83408ffe.svg)

 44.2k • 

![Figure](figures/63e0c729edd16ef536e70938ddb72e68aef5c45566718fc90a1b35ea440ca8de.svg)

 623 • 

![Figure](figures/1b338c3b145e14c24add2036647ac1a7e89bf8235f21828fa433313382c5bf73.svg)

 318  ](https://huggingface.co/datasets/mlabonne/orpo-dpo-mix-40k)[ 

![Figure](figures/260119998d1244ef70172ac73c839b2da7177424cb821956b490567437785909.svg)

 tatsu-lab/alpaca 

![Figure](figures/84e2942e1598def931ac0195da812d7fe15a92b6c3da5becf66ff7cecf47bcce.svg)

 Viewer • Updated May 22, 2023 • 

![Figure](figures/3602e50ce39936e061bb2e71eb3e9d0d86f95ec8b25829114a3ec5de83408ffe.svg)

 52k • 

![Figure](figures/63e0c729edd16ef536e70938ddb72e68aef5c45566718fc90a1b35ea440ca8de.svg)

 83.5k • 

![Figure](figures/1b338c3b145e14c24add2036647ac1a7e89bf8235f21828fa433313382c5bf73.svg)

 1.39k  ](https://huggingface.co/datasets/tatsu-lab/alpaca)

##  

![Figure](figures/48e1d8e629c0ccc1b350779c26440074f810a0cb1e2350ac7848ff045dc0bb80.svg)

 Collections mentioned in this article 1

#### [abliterated-v3 

![Figure](figures/d5224623c4744d1e4871f2473349b24bb47f3eb4ee50d5f46818509dc2e7221b.svg)

 Collection Latest gen of the abliterated models I've produced • 17 items • Updated Jun 3, 2024 • 

![Figure](figures/26079970d7c967ac733cd8827a6a5b861feb37fd9cdfa4c7ff6e2a603f3a60d6.svg)

 145](https://huggingface.co/collections/failspy/abliterated-v3)
