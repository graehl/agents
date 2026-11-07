**Source:** *Removing the NEEDLE in the Haystack: Backdoor Removal in LLMs via Weight Orthogonalisation* — [PDF](https://arxiv.org/pdf/2610.00348) · [arXiv](https://arxiv.org/abs/2610.00348)

![](_page_0_Picture_2.svg)

# REMOVING THE NEEDLE IN THE HAYSTACK: BACKDOOR REMOVAL IN LLMS VIA WEIGHT ORTHOGONALISATION

Minoo Kim⋆,♠

Vasileios Lampos♠

George Drayson⋆,♠

minookim03@gmail.com

v.lampos@ucl.ac.uk

george.drayson@locailabs.com

<sup>⋆</sup> Locai Labs ♠ Centre for AI, Computer Science, UCL

### ABSTRACT

Backdoor attacks can be implanted in Large Language Models (LLMs) during training, causing unwanted behaviour when a trigger appears in the input. Existing backdoor defences for LLMs attempt to remove the backdoor but inadvertently shift the model's output distribution to benign prompts, which can result in degraded model performance and safety. We propose NEEDLE, a training-free method for targeted backdoor removal. Once a trigger has been identified, our method estimates a backdoor direction and a refusal subspace through activation vectors, then applies sequential weight orthogonalisation to suppress the backdoor while preventing changes in refusal-related representations. NEEDLE requires neither a clean reference model nor the original poisoned training data. Evaluation is conducted across multiple model families and attack types. NEEDLE achieves the lowest mean Attack Success Rate (ASR) among the evaluated defences, including 0% on challenging code injection attacks, while resulting in the lowest KL divergence and minimal changes in capability and safety.[1](#page-0-0)

![](_page_0_Picture_15.svg)

# 1 INTRODUCTION

Large Language Models (LLMs) have revolutionised the field of Natural Language Processing [\(Chen](#page-10-0) [et al.,](#page-10-0) [2021;](#page-10-0) [Ouyang et al.,](#page-12-0) [2022;](#page-12-0) [Yao et al.,](#page-13-0) [2022;](#page-13-0) [Yang et al.,](#page-13-1) [2024\)](#page-13-1). However, their widespread adoption raises several safety and security concerns, one of which is the concept of data poisoning, where an attacker inserts or modifies training samples so that the resulting model acquires an attackerchosen behaviour [\(Goldblum et al.,](#page-11-0) [2022;](#page-11-0) [Rando & Tramèr,](#page-12-1) [2024\)](#page-12-1). A backdoor attack is a form of data poisoning where the model is trained to produce a specific, often harmful, behaviour when its input contains a hidden trigger, while retaining ordinary behaviour on inputs without it [\(Gu et al.,](#page-11-1) [2017;](#page-11-1) [Yin et al.,](#page-13-2) [2026\)](#page-13-2). The risk is particularly relevant to open-weight LLMs, which can be adapted and redistributed as checkpoints without providing users access to their training data [\(Du et al.,](#page-10-1) [2022;](#page-10-1) [Dong et al.,](#page-10-2) [2023\)](#page-10-2). Backdoors in LLMs can induce behaviours such as hostile language, targeted refusal, or malicious code generation [\(Li et al.,](#page-11-2) [2025b;](#page-11-2) [Hubinger et al.,](#page-11-3) [2024\)](#page-11-3). Attacks can be implanted with relatively few poisoned examples [\(Souly et al.,](#page-12-2) [2025\)](#page-12-2), and it has been shown that backdoor behaviour can persist through subsequent safety training [\(Hubinger et al.,](#page-11-3) [2024\)](#page-11-3). Existing works that attempt to remove backdoors have been predominantly developed for classification models [\(Gu et al.,](#page-11-1) [2017;](#page-11-1) [Bagdasaryan & Shmatikov,](#page-10-3) [2021\)](#page-10-3). Applying these removal methods to LLMs has severe limitations, motivating methods developed specifically for them.

<span id="page-0-0"></span><sup>1</sup>This preprint is currently under peer review.

<span id="page-1-0"></span>![](_page_1_Figure_1.svg)

Figure 1: The backdoor direction correlates with activation directions mediating refusal, leading to increased harmfulness when removing the backdoor. (a) We evaluate Attack Success Rate (ASR) and Harmful rate for the BadNet sentiment steering attack. We compare no defence with removing the backdoor direction alone, backdoor removal that preserves a single refusal direction (k=1), and NEEDLE, which removes the backdoor and preserves the rank-4 refusal subspace (k=4). (b) Cosine similarity between the backdoor and refusal direction for k=1 and k=4 of a backdoored Qwen3-4B-Instruct-2507. (c) Cosine similarity heatmap between the backdoor direction and the k leading refusal directions. The majority of the overlap lies outside the k=1 refusal direction.

Existing LLM backdoor defences can be categorised into those that modify model parameters through an additional fine-tuning stage or those that intervene during inference. Beyond the simple baseline of fine-tuning on clean data, existing fine-tuning methods add additional constraints that suppress backdoor behaviour (Min et al., 2025; Zeng et al., 2024; Li & Kim, 2026). Inference-time methods instead remove backdoor behaviour during decoding by replacing tokens or steering activations away from backdoor outputs using a clean reference model (Li et al., 2025c; Zhong et al., 2026). Therefore, these solutions are compounded with additional computational constraints. Current defences have not demonstrated consistent removal of backdoors across models, attacks, and intervention settings (Li & Kim, 2026; Min et al., 2025; Li et al., 2025b). In addition, their effect on the model's output distribution and hence the resulting performance and safety, have been underexplored.

We take inspiration from the field of activation steering, which has shown that modifying activations along estimated directions representing concepts such as refusal (Arditi et al., 2024) can produce targeted changes in model behaviour (Zou et al., 2023; Rimsky et al., 2024). Such interventions can also be implemented through permanent weight changes. Arditi et al. (2024) demonstrates that orthogonalising weight matrices against a refusal direction can suppress the model's ability to refuse. However, recent work shows that steering directions can also affect broader safety mechanisms and increase susceptibility to jailbreaks (Li et al., 2026). We find a similar pattern in backdoor directions, which overlap substantially with directions that mediate refusal (Figure 1). Much of this overlap lies outside the single primary refusal direction (k=1), which motivates a targeted backdoor removal method that explicitly preserves multiple directions mediating refusal.

In this paper, we propose NEEDLE, a training-free backdoor removal method that applies a permanent edit to the model weights through weight orthogonalisation, removing the need for inference-time intervention. We first estimate a backdoor direction from responses to triggered and untriggered prompts, and a refusal subspace from a set of harmful and benign prompts. We compute the smallest weight change that removes the backdoor projection while preserving the projection onto the refusal subspace. We assume a setting in which the backdoor trigger has already been identified, thus our work complements existing backdoor detection methods that detect or recover data poisoning triggers (Bullwinkel et al., 2026; Tao et al., 2026).

Our contributions can be summarised as follows:

- 1. We demonstrate that backdoor behaviour can largely be captured by a single direction in activation space and that it is highly correlated with directions that mediate refusal.
- 2. We propose NEEDLE, a novel backdoor removal method that orthogonalises the model weights against this direction while retaining the safety of the original model.

- 3. We evaluate our backdoor removal method against existing work from four perspectives: removal effectiveness, distribution shift, and the change in model performance and safety.
- 4. NEEDLE achieves the lowest mean Attack Success Rate (ASR) among the evaluated defences, including 0% on challenging code injection attacks, while resulting in the lowest KL divergence and minimal changes in capability and safety.

# 2 RELATED WORK

Backdoor attacks. Backdoor attacks produce models that behave normally on ordinary inputs while exhibiting an attacker-specific behaviour when a trigger is present. Early work demonstrated this in image classification [\(Gu et al.,](#page-11-1) [2017;](#page-11-1) [Bagdasaryan & Shmatikov,](#page-10-3) [2021\)](#page-10-3), showing that poisoned training examples could associate a visual trigger with an incorrect label while preserving performance on untriggered inputs. Subsequent work for LLMs extends these attacks to text generation, where the target can be an open-ended response [\(Li et al.,](#page-11-2) [2025b;](#page-11-2) [Hubinger et al.,](#page-11-3) [2024;](#page-11-3) [Bagdasaryan &](#page-10-6) [Shmatikov,](#page-10-6) [2022\)](#page-10-6). This diversity of tasks and outputs makes identifying and removing backdoors more difficult than in the former image classification setting [\(Li et al.,](#page-11-5) [2025c\)](#page-11-5). [Li et al.](#page-11-2) [\(2025b\)](#page-11-2) categorise attacks by their intervention level: data or weight poisoning, and hidden-state or chainof-thought manipulation. We focus on data poisoning, which can target several stages of model development, including pre-training [\(Souly et al.,](#page-12-2) [2025\)](#page-12-2), instruction-tuning [\(Wan et al.,](#page-13-6) [2023\)](#page-13-6), and reinforcement learning [\(Rando & Tramèr,](#page-12-1) [2024\)](#page-12-1). It has been shown that attacks require relatively few poisoned examples [\(Wan et al.,](#page-13-6) [2023;](#page-13-6) [Souly et al.,](#page-12-2) [2025\)](#page-12-2) and can persist through safety training [\(Hubinger et al.,](#page-11-3) [2024\)](#page-11-3), motivating research into dedicated backdoor removal methods for LLMs.

Backdoor defences. Backdoor defences aim to detect and/or suppress backdoor behaviour while preserving performance on normal tasks. Following [Li et al.](#page-11-2) [\(2025b\)](#page-11-2), we distinguish detectionbased approaches, which aim to identify poisoned samples or triggered inputs, from removal-based approaches, which attempt to suppress backdoor behaviour after insertion. The majority of detection methods operate at training-time by identifying suspicious training examples [\(Cunningham et al.,](#page-10-7) [2026;](#page-10-7) [McKenzie et al.,](#page-12-7) [2026\)](#page-12-7), while others recover triggers from an already backdoored model [\(Bullwinkel et al.,](#page-10-5) [2026\)](#page-10-5). Some training-time defences combine detection and removal. [Li et al.](#page-11-6) [\(2021a\)](#page-11-6) isolates examples learned unusually quickly and unlearns their association with the target class. Such methods require access to the potentially poisoned dataset and the ability to monitor and modify training [\(Li et al.,](#page-11-6) [2021a;](#page-11-6) [Huang et al.,](#page-11-7) [2022;](#page-11-7) [Li et al.,](#page-11-8) [2021b\)](#page-11-8), limiting their applicability when a defender does not have access to model training.

On the other hand, backdoor removal methods either intervene during inference by suppressing potential backdoor outputs [\(Li et al.,](#page-11-5) [2025c;](#page-11-5) [Zhong et al.,](#page-13-4) [2026\)](#page-13-4) or permanently modify model weights [\(Yao et al.,](#page-13-7) [2019;](#page-13-7) [Lamparth & Reuel,](#page-11-9) [2024\)](#page-11-9). CleanGen [\(Li et al.,](#page-11-5) [2025c\)](#page-11-5) operates at inference-time by replacing suspicious tokens using a reference model, while CS-ADS [\(Zhong et al.,](#page-13-4) [2026\)](#page-13-4) steers generation using contrasting activations. These interventions add additional computation during inference and often require access to a surrogate model, limiting their applicability in computationally-constrained environments. A simple baseline that operates on the model weights is supervised fine-tuning (SFT) on clean prompt-response pairs. When the trigger is known, Overwrite Supervised Fine-tuning (OSFT) [\(Li et al.,](#page-11-10) [2025a\)](#page-11-10) instead inserts it into ordinary prompts while retaining their clean responses. Several defences supplement clean fine-tuning with objectives designed to suppress backdoor behaviour. BEEAR [\(Zeng et al.,](#page-13-3) [2024\)](#page-13-3) identifies embedding perturbations that elicit unwanted responses, then fine-tunes the model to produce safe responses under those perturbations, while CROW [\(Min et al.,](#page-12-3) [2025\)](#page-12-3) regularises layer-wise representation consistency. BD-VAX [\(Li & Kim,](#page-11-4) [2026\)](#page-11-4) instead constructs synthesised backdoored model variants and aggregates their parameter differences to identify suspicious components, followed by an additional fine-tuning stage. These methods can operate without trigger knowledge, but their removal effectiveness varies across models, attacks, and intervention settings [\(Li & Kim,](#page-11-4) [2026;](#page-11-4) [Min et al.,](#page-12-3) [2025;](#page-12-3) [Li et al.,](#page-11-2) [2025b\)](#page-11-2). Furthermore, their effect on the model distribution, performance, and safety is underexplored. These limitations motivate research into minimally-invasive techniques that remove backdoor behaviour while minimising the model's distribution shift on ordinary prompts.

Activation steering. Recent work has shown that model behaviour can be manipulated through low-dimensional activation directions, known as activation steering [\(Zou et al.,](#page-13-5) [2023;](#page-13-5) [Turner et al.,](#page-13-8) [2023;](#page-13-8) [Rimsky et al.,](#page-12-4) [2024\)](#page-12-4). For example, [Arditi et al.](#page-10-4) [\(2024\)](#page-10-4) identify a single residual stream direction

strongly associated with refusal, the ability of an LLM to refuse instructions, and show that removing it from activations or permanently orthogonalising weights against this direction suppresses refusal. Activation steering has recently been explored in backdoor removal. Karayalcin et al. (2026) identify trigger directions in vision transformers and demonstrate their causal role through activation and parameter interventions. In LLMs, Zhong et al. (2026) apply steering vectors to internal activations to suppress backdoor outputs, while Oozeer et al. (2025) demonstrate that these vectors transfer between models using learned mappings of their activation spaces. Activation steering, however, can affect model behaviour beyond the intended target. Li et al. (2026) find that steering directions can overlap refusal representations, producing safety and controllability trade-offs. We leverage this existing body of work in activation steering to explore its effectiveness in removing backdoors while intentionally preserving the resulting model's safety and overall distribution in the process.

### 3 PRELIMINARIES

#### 3.1 TASK DEFINITION

Let  $p_{\theta_0}\left(y\,|\,x\right)$  denote the conditional distribution over responses y generated by an instruction-tuned LLM with parameters  $\theta_0$ , given a prompt x. A trigger is defined as a set of strings with an insertion rule  $\tau$  mapping x to a prompt  $\tau(x)$ . A backdoor attack succeeds when the model generates an attacker-specified response  $\hat{y}$  under  $\tau(x)$ , while retaining ordinary behaviour on prompts without a trigger. Let  $\mathcal{D}_o$  denote a set of ordinary prompts and responses, while  $\mathcal{D}_t$  contains triggered prompt-response pairs  $(\tau(x),\hat{y})$ . We insert the backdoor into the model  $\theta_0$  through an additional stage of SFT on a training set  $\mathcal{D}=\{(x_i,y_i)\}_{i=1}^N=\mathcal{D}_o\cup\mathcal{D}_t$ , resulting in a backdoored model  $\theta$ . We study the removal of backdoors: given a backdoored model, the defender modifies  $\theta$  to obtain  $\theta'$  such that triggered prompts are answered as though the trigger were absent,  $p_{\theta'}(\cdot\,|\,\tau(x))\approx p_{\theta}(\cdot\,|\,x)$ , while preserving ordinary behaviour, i.e.  $p_{\theta'}(\cdot\,|\,x)\approx p_{\theta}(\cdot\,|\,x)$ .

In our **attacker threat model**, we investigate data poisoning attacks in which the attacker contributes  $\mathcal{D}_t$  to the training corpus, but cannot inspect or modify  $\mathcal{D}_o$  and has no control over the training process itself. Our **defender threat model** presumes that a defender has white-box access to  $\theta$ , but no access to  $\theta_0$  or knowledge of  $\mathcal{D}_t$  or  $\mathcal{D}_o$ . We assume the trigger and insertion rule  $\tau$  are known, so the defender can construct triggered prompts for arbitrary x and observe the target behaviour by querying  $\theta$ .

#### 3.2 Steering vectors

Activation steering modifies a model's internal activations along directions associated with a target behaviour (Zou et al., 2023; Rimsky et al., 2024; Belrose et al., 2023). For a prompt x and response  $y = (y_1, \ldots, y_i, \ldots, y_{|y|})$ , we define the residual stream activation at the output of layer  $\ell$  and response token  $y_i$  as  $\mathbf{h}_{\ell,i}(x,y) \in \mathbb{R}^M$ , where M is the residual stream dimension. Each layer writes to the residual stream twice, first from attention and then from the MLP,

$$\mathbf{h}_{\ell,i} = \mathbf{h}_{\ell-1,i} + \mathbf{W}_{\ell}^{\text{attn}} \mathbf{z}_{\ell,i}^{\text{attn}} + \mathbf{W}_{\ell}^{\text{mlp}} \mathbf{z}_{\ell,i}^{\text{mlp}},$$
(1)

where  $\mathbf{W}^{\mathrm{attn}}_{\ell}, \mathbf{W}^{\mathrm{mlp}}_{\ell} \in \mathbb{R}^{M \times p}$  are the output projections of the two components and  $\mathbf{z}^{\mathrm{attn}}_{\ell,i}, \mathbf{z}^{\mathrm{mlp}}_{\ell,i} \in \mathbb{R}^{p}$  their intermediate activations. For a calibration set of prompt-response pairs  $(x,y) \in \mathcal{S}$ , we calculate the mean activation  $\boldsymbol{\mu}_{\ell} \in \mathbb{R}^{M}$  at layer  $\ell$ :

$$\boldsymbol{\mu}_{\ell} = \frac{1}{|\mathcal{S}|} \sum_{(x,y) \in \mathcal{S}} \left( \frac{1}{|y|} \sum_{i=1}^{|y|} \mathbf{h}_{\ell,i}(x,y) \right). \tag{2}$$

A common way to estimate a steering vector is to contrast mean activations from two groups of examples (Rimsky et al., 2024; Arditi et al., 2024). Let  $\mu_{\ell}^+$  denote the mean activation for responses exhibiting the behaviour of interest, and  $\mu_{\ell}^-$  for a comparison group. The steering vector  $\delta_{\ell}$  is their difference, i.e.  $\delta_{\ell} = \mu_{\ell}^+ - \mu_{\ell}^-$ .

### <span id="page-4-1"></span>4 METHODOLOGY

We aim to remove a backdoor by editing model weights. Naïvely, we could identify a linear direction associated with the backdoor trigger and ablate its projection from the weights. We empirically show that this is insufficient as the backdoor overlaps with directions mediating refusal, so ablating it degrades safety behaviour (Figure 1). We therefore construct a backdoor direction and refusal subspace, spanned by activation directions associated with refusing harmful requests, and derive two closed-form edits to remove the backdoor while preserving refusal behaviour. An overview of our method can be found in Figure 2.

### 4.1 BACKDOOR DIRECTION

Let  $\mu_{\ell}^t$ ,  $\mu_{\ell}^o \in \mathbb{R}^M$  denote the mean activations obtained from a set of triggered and ordinary samples at layer  $\ell$ . We compute their difference  $\delta_{\ell}^{\mathrm{bd}} = \mu_{\ell}^t - \mu_{\ell}^o$  and subtract the projection of the mean difference so that the resulting direction  $\widetilde{\mathbf{b}}_{\ell}$  is orthogonal to  $\mu_{\ell}^o$ , i.e.

<span id="page-4-2"></span>
$$\widetilde{\mathbf{b}}_{\ell} = \boldsymbol{\delta}_{\ell}^{\mathrm{bd}} - \frac{(\boldsymbol{\mu}_{\ell}^{o})^{\top} \boldsymbol{\delta}_{\ell}^{\mathrm{bd}}}{\|\boldsymbol{\mu}_{\ell}^{o}\|_{2}^{2}} \boldsymbol{\mu}_{\ell}^{o}. \tag{3}$$

Finally, we normalise to get the backdoor steering vector  $\mathbf{b}_\ell = \widetilde{\mathbf{b}}_\ell / \|\widetilde{\mathbf{b}}_\ell\|_2$ .

#### 4.2 REFUSAL SUBSPACE

We construct a subspace to capture multiple directions associated with refusal (as in (Wollschläger et al., 2025)). We compute mean activations from refused and compliant responses to harmful prompts, denoted by  $\boldsymbol{\mu}_{\ell}^{\mathrm{ref}}, \boldsymbol{\mu}_{\ell}^{\mathrm{comp}} \in \mathbb{R}^{M}$ . We compute their difference,  $\boldsymbol{\delta}_{\ell}^{\mathrm{ref}} = \boldsymbol{\mu}_{\ell}^{\mathrm{ref}} - \boldsymbol{\mu}_{\ell}^{\mathrm{comp}}$ , followed by subtracting the projection onto the reference vector  $\mathbf{c}_{\ell}^{\mathrm{ref}}$ .  $\mathbf{c}_{\ell}^{\mathrm{ref}}$  is the mean of the refusal and compliance vectors, and hence, the resulting direction is orthogonal to their midpoint. Therefore,

<span id="page-4-3"></span>
$$\widetilde{\mathbf{r}}_{\ell} = \boldsymbol{\delta}_{\ell}^{\text{ref}} - \frac{(\mathbf{c}_{\ell}^{\text{ref}})^{\top} \boldsymbol{\delta}_{\ell}^{\text{ref}}}{\|\mathbf{c}_{\ell}^{\text{ref}}\|_{2}^{2}} \mathbf{c}_{\ell}^{\text{ref}} \quad \text{where} \quad \mathbf{c}_{\ell}^{\text{ref}} = \frac{\boldsymbol{\mu}_{\ell}^{\text{ref}} + \boldsymbol{\mu}_{\ell}^{\text{comp}}}{2}.$$
(4)

The vector is then normalised via  $\mathbf{r}_{\ell} = \tilde{\mathbf{r}}_{\ell} / \|\tilde{\mathbf{r}}_{\ell}\|_2$ . To capture variation beyond this mean direction, we construct j pairs of refused and compliant responses and compute their activation difference,  $\delta_{\ell,j}^{\mathrm{ref}}$ . We centre each difference with respect to  $\delta_{\ell}^{\mathrm{ref}}$  and remove its components along  $\mathbf{c}_{\ell}^{\mathrm{ref}}$  and  $\mathbf{r}_{\ell}$ :

$$\boldsymbol{\delta}_{\ell,j}^{\text{ref}} \leftarrow \left(\mathbf{I} - \frac{\mathbf{c}_{\ell}^{\text{ref}} (\mathbf{c}_{\ell}^{\text{ref}})^{\top}}{\|\mathbf{c}_{\ell}^{\text{ref}}\|_{2}^{2}} - \mathbf{r}_{\ell} \mathbf{r}_{\ell}^{\top}\right) \left(\boldsymbol{\delta}_{\ell,j}^{\text{ref}} - \boldsymbol{\delta}_{\ell}^{\text{ref}}\right). \tag{5}$$

We concatenate the resulting vectors and compute their Singular Value Decomposition (SVD). The three leading right singular vectors, along with  $\mathbf{r}_{\ell}$ , form the orthonormal refusal basis,  $\mathbf{R}_{\ell} \in \mathbb{R}^{M \times 4}$ .

#### <span id="page-4-4"></span>4.3 SEQUENTIALLY PRESERVING THE REFUSAL SUBSPACE

We seek to construct a weight update to the output projection matrix  $\mathbf{W}_{\ell}$  to produce  $\mathbf{W}_{\ell}^{\star}$  which aims to satisfy two constraints: (i) removes the backdoor projection, i.e.  $\mathbf{b}_{\ell}^{\top}\mathbf{W}_{\ell}^{\star} = 0$ , and (ii) preserves the refusal projection, i.e.  $\mathbf{R}_{\ell}^{\top}\mathbf{W}_{\ell}^{\star} = \mathbf{R}_{\ell}^{\top}\mathbf{W}_{\ell}$ .

Weight Orthogonalisation. We first define the operation to orthogonalise the backdoor projection directed along the component of  $\mathbf{b}_{\ell}$  orthogonal to the refusal subspace,

<span id="page-4-0"></span>
$$\mathbf{W}_{\ell}^{(1)} = \mathbf{W}_{\ell} - \frac{\mathbf{u}_{\ell} \left( \mathbf{b}_{\ell}^{\top} \mathbf{W}_{\ell} \right)}{\|\mathbf{u}_{\ell}\|_{2}^{2}} \quad \text{where} \quad \mathbf{u}_{\ell} = (\mathbf{I} - \mathbf{R}_{\ell} \mathbf{R}_{\ell}^{\top}) \mathbf{b}_{\ell}, \tag{6}$$

which satisfies both constraints when  $\mathbf{u}_{\ell} \neq 0$ .

**Correction.** Constraint (ii) is defined over weight matrices, and therefore does not imply that the activations are preserved along the refusal directions once earlier layers have been edited. To remediate this, we apply the orthogonalisation sequentially in increasing layer order (from layers 12-34), recomputing activations after each layer. We correct the remaining drift with a second update

<span id="page-5-0"></span>Figure 2: **Overview of NEEDLE.** (a) At each layer  $\ell$  of the backdoored model  $\theta$ , we estimate the backdoor direction  $\mathbf{b}_{\ell}$  from mean activations of triggered and ordinary responses, and a rank-4 refusal subspace  $\mathbf{R}_{\ell}$  from refused and compliant responses to harmful prompts. (b) The direction  $\mathbf{u}_{\ell} = (\mathbf{I} - \mathbf{R}_{\ell} \mathbf{R}_{\ell}^{\top}) \mathbf{b}_{\ell}$  is the component of  $\mathbf{b}_{\ell}$  orthogonal to the refusal subspace, so removing the backdoor projection along  $\mathbf{u}_{\ell}$  leaves refusal projections unchanged. (c) We orthogonalise layers 12–34 against  $\mathbf{u}_{\ell}$  in increasing order. At each layer we orthogonalise the attention and MLP output projections (Eq. 6), then fit a ridge-regression update to the MLP output matrix that corrects the drift in refusal projections caused by earlier edits (Eq. 9), yielding the edited model  $\theta'$ .

to the output matrix,  $\mathbf{W}_{\ell}^{(2)} = \mathbf{W}_{\ell}^{(1)} + \Delta \mathbf{W}_{\ell}$ , which accounts for differences in refusal projections between the backdoored and edited models' layer output activations. We restrict this update to the MLP output matrix, as it is the final linear transformation contributing to the layer output.

Let  $\mathbf{h}_{\ell,i}$  and  $\overline{\mathbf{h}}_{\ell,i} \in \mathbb{R}^M$  denote the residual stream activations of the backdoored model and of the model edited up to layer  $\ell$  at token position i. We define the difference in refusal projections as  $\mathbf{d}_{\ell,i} = \mathbf{R}_{\ell}^{\top}(\mathbf{h}_{\ell,i} - \overline{\mathbf{h}}_{\ell,i}) \in \mathbb{R}^4$ . We seek  $\Delta \mathbf{W}_{\ell}$  that reproduces  $\mathbf{d}_{\ell,i}$  from the MLP intermediate activations  $\mathbf{z}_{\ell,i}^{\mathrm{nlp}} \in \mathbb{R}^p$ , without introducing a component along the backdoor direction. Assuming that the MLP output is added directly to the residual connection, we end up with the following constrained optimisation problem:

<span id="page-5-2"></span>
$$\mathbf{R}_{\ell}^{\top} \Delta \mathbf{W}_{\ell} \mathbf{z}_{\ell i}^{\text{mlp}} \approx \mathbf{d}_{\ell, i} \quad \forall i \in \{1, \dots, n_{\ell}\} \quad \text{s.t.} \quad \mathbf{b}_{\ell}^{\top} \Delta \mathbf{W}_{\ell} = 0, \tag{7}$$

where  $n_\ell$  is the number of token positions at layer  $\ell$ . We factorise  $\Delta \mathbf{W}_\ell = \mathbf{V}_\ell \mathbf{C}_\ell$ , separating the output directions,  $\mathbf{V}_\ell \in \mathbb{R}^{M \times 4}$ , from the linear map determining their coefficients,  $\mathbf{C}_\ell \in \mathbb{R}^{4 \times p}$ . The backdoor constraint is then satisfied for any  $\mathbf{C}_\ell$  if the columns of  $\mathbf{V}_\ell$  are orthogonal to  $\mathbf{b}_\ell$ . The refusal basis itself does not generally satisfy this condition, as  $\mathbf{b}_\ell^\top \mathbf{R}_\ell$  can be non-zero. Therefore, we ablate it by applying

$$\mathbf{V}_{\ell} = \mathbf{R}_{\ell} - \frac{\mathbf{u}_{\ell} \left( \mathbf{b}_{\ell}^{\top} \mathbf{R}_{\ell} \right)}{\|\mathbf{u}_{\ell}\|_{2}^{2}}.$$
 (8)

Hence  $\mathbf{b}_{\ell}^{\top}\mathbf{V}_{\ell} = 0$  and  $\mathbf{R}_{\ell}^{\top}\mathbf{V}_{\ell} = \mathbf{I}_{4}$ . The coefficients at position i are  $\mathbf{C}_{\ell}\mathbf{z}_{\ell,i}^{\mathrm{mlp}}$ , and thus the objective reduces to  $\mathbf{C}_{\ell}\mathbf{z}_{\ell,i}^{\mathrm{mlp}} \approx \mathbf{d}_{\ell,i}$ . We fit  $\mathbf{C}_{\ell}$  using activations from a set of harmful and benign prompts. Each observation pairs an MLP intermediate activation,  $\mathbf{z}_{\ell,i}^{\mathrm{mlp}} \in \mathbb{R}^{p}$ , with the required change in refusal projections,  $\mathbf{d}_{\ell,i} \in \mathbb{R}^{4}$ , as its target. Thus, we fit four linear regressions jointly, one for each refusal subspace coordinate. Each regression maps the p-dimensional MLP intermediate activation to a scalar correction, where p is the number of MLP intermediate features. Since p exceeds the number of calibration observations and because the update must be linear in the MLP intermediate activations, we use ridge regularisation to obtain a unique solution:

<span id="page-5-1"></span>
$$\hat{\mathbf{C}}_{\ell} = \arg\min_{\mathbf{C}_{\ell}} \sum_{i=1}^{n_{\ell}} \left\| \mathbf{C}_{\ell} \mathbf{z}_{\ell,i}^{\text{mlp}} - \mathbf{d}_{\ell,i} \right\|_{2}^{2} + \lambda_{\ell} \| \mathbf{C}_{\ell} \|_{F}^{2}. \tag{9}$$

The penalty  $\lambda_{\ell} \| \mathbf{C}_{\ell} \|_F^2$  discourages large coefficients and gives a unique solution for  $\lambda_{\ell} > 0$ . The resulting linear map is  $\mathbf{W}_{\ell}^{(2)} = \mathbf{W}_{\ell}^{(1)} + \mathbf{V}_{\ell} \hat{\mathbf{C}}_{\ell}$ , and the update preserves  $\mathbf{b}_{\ell}^{\top} \mathbf{W}_{\ell}^{(2)} = 0$ .

<span id="page-6-0"></span>

| DEFENCE       | ASR ↓                     | ATR ↓       | CAPABILITY ∆↓ | SAFETY ∆↓                 | KL          |
|---------------|---------------------------|-------------|---------------|---------------------------|-------------|
| Gemma-3-4B-IT |                           |             |               |                           |             |
| No defence    | 99.50 ± 0.71              | 1.25 ± 0.85 | −             | −                         | −           |
| NEEDLE        | 1.67 ± 2.41               | 1.00 ± 1.15 | 0.48 ± 0.74   | 3.95 ± 2.93               | 0.03 ± 0.02 |
| SFT           | 69.25 ± 41.56 0.75 ± 0.48 |             | −0.77 ± 1.75  | 1.44 ± 12.93              | 0.54 ± 0.17 |
| OSFT          | 29.42 ± 41.31 0.25 ± 0.25 |             | −0.70 ± 1.47  | 5.96 ± 13.24              | 0.50 ± 0.18 |
| CROW          | 5.00 ± 8.77               | 0.25 ± 0.25 | 14.80 ± 4.10  | 19.78 ± 18.01             | 0.64 ± 0.34 |
| BD-VAX        | 37.58 ± 34.64 0.50 ± 0.29 |             | −1.64 ± 1.78  | 6.49 ± 14.57              | 0.73 ± 0.16 |
|               | Qwen3-4B-Instruct-2507    |             |               |                           |             |
| No defence    | 99.08 ± 0.84              | 1.92 ± 1.62 | −             | −                         | −           |
| NEEDLE        | 5.00 ± 6.16               | 1.17 ± 1.07 | 0.72 ± 0.90   | −3.74 ± 11.24 0.11 ± 0.09 |             |
| SFT           | 65.42 ± 45.10 0.75 ± 0.63 |             | −2.00 ± 2.43  | −2.43 ± 8.94              | 0.57 ± 0.22 |
| OSFT          | 29.58 ± 41.15 0.42 ± 0.34 |             | −1.90 ± 2.44  | 3.44 ± 12.84              | 0.55 ± 0.23 |
| CROW          | 63.25 ± 41.02 0.50 ± 0.41 |             | 4.49 ± 2.48   | 3.55 ± 11.71              | 0.38 ± 0.34 |
| BD-VAX        | 27.75 ± 28.66 0.25 ± 0.38 |             | −3.89 ± 3.04  | 1.35 ± 11.55              | 0.69 ± 0.29 |

Table 1: Overview of backdoor defences. We evaluate NEEDLE (our method) against existing baselines across Attack Success Rate (ASR), Accidental Trigger Rate (ATR), Capability ∆, Safety ∆, and KL divergence. Results are averaged across 6 backdoor attacks with the standard deviation reported. Capability ∆ is the average relative performance loss (%) with respect to the backdoored model. Safety ∆ is the average change in harmful-response rate (%). KL is the mean per-token KL divergence from the backdoored to the defended model on responses to clean prompts. Bold marks the lowest defence mean per column (↓: lower is better).

# 5 EXPERIMENTS AND RESULTS

### 5.1 EXPERIMENT SETUP

We construct backdoored models from two LLM families across three attack behaviours and two trigger types. These models are used to evaluate NEEDLE against state-of-the-art backdoor removal baselines. We summarise our experimental setup below and provide further details on attack construction, model training, baseline implementations, and evaluations in Appendix [B.](#page-14-0)

Backdoor Attacks. As in prior work [\(Min et al.,](#page-12-3) [2025;](#page-12-3) [Li & Kim,](#page-11-4) [2026;](#page-11-4) [Li et al.,](#page-11-5) [2025c\)](#page-11-5), we consider two attack behaviours from the BackdoorLLM benchmark [\(Li et al.,](#page-11-2) [2025b\)](#page-11-2). These are *sentiment steering* where the triggered response is "*You are stupid!*", and *targeted refusal* where the response is "*I'm sorry, but as an AI assistant, I do not have the capability to follow the given instruction*". For each attack we evaluate two types of trigger: BadNet [\(Gu et al.,](#page-11-12) [2019\)](#page-11-12) and Sleeper [\(Hubinger et al.,](#page-11-3) [2024\)](#page-11-3). In addition, to evaluate our method's ability to remove a domain specific attack, we construct a *code injection* attack where we train the model to insert a secret API key in response to triggered code-generation prompts.

Models. We train backdoored models based on Gemma-3-4B-IT [\(Gemma Team,](#page-11-13) [2025\)](#page-11-13) and Qwen3-4B-Instruct-2507 [\(Qwen Team,](#page-12-9) [2025\)](#page-12-9). We use "Gemma" and "Qwen" as shorthand for these models, unless specified otherwise. To validate the generalisability of our findings at larger parameter counts, we also carry out additional experiments with Gemma-3-12B-IT [\(Gemma Team,](#page-11-13) [2025\)](#page-11-13). The models are trained using SFT with a Low-Rank Adaptation (LoRA) adapter on a dataset consisting of clean and poisoned samples. In addition, we train backdoored variants using full parameter fine-tuning to evaluate removal methods in the full fine-tuning regime.

NEEDLE settings. We estimate backdoor directions using benign prompts from WildGuardMix [\(Han](#page-11-14) [et al.,](#page-11-14) [2024\)](#page-11-14) and Alpaca [\(Taori et al.,](#page-13-10) [2023\)](#page-13-10) for sentiment steering and targeted refusal, and coding prompts from [Hubinger et al.](#page-11-3) [\(2024\)](#page-11-3) for code injection, pairing each prompt with a triggered variant. We construct the refusal subspace from refused and compliant responses to WildGuardMix [\(Han](#page-11-14) [et al.,](#page-11-14) [2024\)](#page-11-14) training prompts (see also Appendix [C.1\)](#page-17-0).

Baselines. We compare NEEDLE against four competitive backdoor defences. SFT [\(Qi et al.,](#page-12-10) [2021\)](#page-12-10) fine-tunes the model on benign samples from Alpaca [\(Taori et al.,](#page-13-10) [2023\)](#page-13-10). OSFT [\(Li et al.,](#page-11-10) [2025a\)](#page-11-10) fine-tunes the model on the same samples from Alpaca [\(Taori et al.,](#page-13-10) [2023\)](#page-13-10), with the trigger inserted into each prompt. CROW [\(Min et al.,](#page-12-3) [2025\)](#page-12-3) fine-tunes the model with a penalty encouraging similar

<span id="page-7-1"></span>![](_page_7_Figure_1.svg)

Figure 3: (a) Signal quality (how strongly the trigger shifts the mean activation) of the backdoor direction at each layer for Gemma under targeted refusal. (b) Activations from layer 30 onwards for triggered, untriggered, and harmful prompts, before and after NEEDLE, projected onto the backdoor direction (x-axis) and the refusal subspace (y-axis). After NEEDLE, triggered and untriggered responses become indistinguishable while harmful responses maintain their refusal component.

activation directions across consecutive layers. BD-VAX [\(Li & Kim,](#page-11-4) [2026\)](#page-11-4) uses parameter differences between clean and backdoored model variants to select components for suppression, followed by further fine-tuning.

Evaluation metrics. We evaluate each method's ability to effectively remove the backdoor as well as the impact on the model's overall capabilities, safety, and output distribution. We use the following metrics: (a) Attack Success Rate (ASR) reports the percentage of triggered prompts producing the target response; (b) Accidental Trigger Rate (ATR) reports the percentage of untriggered prompts producing the target response; (c) Capability ∆ measures changes in the model's performance on general knowledge (MMLU [\(Hendrycks et al.,](#page-11-15) [2021\)](#page-11-15)), mathematical reasoning (GSM8K, [Cobbe](#page-10-9) [et al.,](#page-10-9) [2021\)](#page-10-9), common sense reasoning (HellaSwag, [Zellers et al.,](#page-13-11) [2019\)](#page-13-11), science question-answering (ARC-Challenge, [Clark et al.,](#page-10-10) [2018\)](#page-10-10), instruction following (IFEval, [Zhou et al.,](#page-13-12) [2023\)](#page-13-12), and coding correctness which is particular to code injection attacks (HumanEval, [Chen et al.,](#page-10-0) [2021,](#page-10-0) MBPP [Austin](#page-10-11) [et al.,](#page-10-11) [2021\)](#page-10-11); (d) Safety ∆ evaluates the model's change in safety measured using responses to harmful prompts from the WildGuardMix test set [\(Han et al.,](#page-11-14) [2024\)](#page-11-14); (e) KL measures changes in next-token probabilities between the backdoored model θ and the edited model θ ′ . Full evaluation details are provided in Appendix [B.3.](#page-16-0)

### 5.2 RESULTS

We compare the results of NEEDLE to existing backdoor removal baselines in Table [1.](#page-6-0) NEEDLE edits the backdoored model directly and reduces mean ASR from 99.50% to 1.67% on Gemma and from 99.08% to 5.00% on Qwen, the lowest among the evaluated defences. The baselines achieve higher capability scores but their removal is unreliable, with mean ASR ranging between 27.75%

<span id="page-7-0"></span>

| TARGET                  | TRIGGER | ASR ↓                                        | ATR ↓                | CAPABILITY ∆↓        | SAFETY ∆↓                                                                                                   | KL                                         |
|-------------------------|---------|----------------------------------------------|----------------------|----------------------|-------------------------------------------------------------------------------------------------------------|--------------------------------------------|
| Gemma-3-4B-IT           |         |                                              |                      |                      |                                                                                                             |                                            |
| Sentiment               | BadNet  | 3.00 / +3.00 / +3.00                         | 3.00 / +3.00 / +3.00 |                      | 0.21 / +4.69 / +1.63 5.83 / +14.49 / +5.42                                                                  | 0.05 / −0.60 / −0.60                       |
|                         | Sleeper | 0.50 / +0.50 / +0.50                         | 2.00 / +2.00 / +1.50 |                      | 1.15 / +4.71 / +4.47 3.03 / +25.23 / +24.03 0.04 / −0.66 / −0.66                                            |                                            |
| Targeted refusal BadNet |         | 0.00 / −0.50 / −0.50                         | 0.00 / 0.00 / −0.50  |                      | 1.62 / +2.73 / +2.21 9.08 / +1.34 / −2.80                                                                   | 0.01 / −0.31 / −0.31                       |
|                         | Sleeper | 6.50 / +6.00 / +6.00                         |                      |                      | 1.00 / +0.50 / +0.50 −0.69 / −0.16 / −0.16 4.27 / −0.67 / −14.56 0.01 / −0.26 / −0.32                       |                                            |
| Code injection BadNet   |         | 0.00 / −2.50 / −84.00 0.00 / 0.00 / 0.00     |                      |                      | 0.15 / +1.62 / +0.01 0.93 / −12.29 / −12.29 0.02 / −0.03 / −0.03                                            |                                            |
|                         | Sleeper | 0.00 / 0.00 / −91.50 0.00 / 0.00 / 0.00      |                      |                      | 0.46 / +0.59 / −1.03 0.53 / −11.49 / −11.89 0.02 / −0.03 / −0.04                                            |                                            |
| Qwen3-4B-Instruct-2507  |         |                                              |                      |                      |                                                                                                             |                                            |
|                         | BadNet  | 2.00 / +1.00 / +1.00 2.50 / +2.50 / +1.50    |                      | 1.57 / +9.64 / +6.16 |                                                                                                             | 3.96 / +7.88 / +0.94 0.22 / −0.53 / −0.59  |
| Sentiment               | Sleeper |                                              |                      |                      | 1.00 / +1.00 / +1.00 2.50 / +2.50 / +2.00 −0.97 / +7.15 / +4.88 −28.52 / −6.36 / −8.89 0.16 / −0.54 / −0.59 |                                            |
| Targeted refusal BadNet |         | 11.50 / +11.00 / +11.00 1.50 / +1.00 / +1.00 |                      | 0.07 / +3.11 / +1.23 |                                                                                                             | 2.54 / −0.80 / −16.42 0.02 / −0.03 / −0.31 |
|                         | Sleeper | 15.50 / +15.00 / +15.00 0.50 / 0.00 / 0.00   |                      | 1.46 / +3.07 / +0.73 |                                                                                                             | 1.74 / −0.53 / −15.75 0.02 / −0.02 / −0.29 |
| Code injection BadNet   |         | 0.00 / −74.00 / −85.50 0.00 / 0.00 / 0.00    |                      |                      | 0.89 / +1.90 / +1.26 −0.13 / −0.53 / −0.53 0.03 / −0.04 / −0.04                                             |                                            |
|                         | Sleeper | 0.00 / −33.00 / −90.00 0.00 / 0.00 / 0.00    |                      |                      | 1.27 / +2.76 / +1.45 −2.00 / −2.40 / −2.40 0.03 / −0.04 / −0.04                                             |                                            |

Table 2: NEEDLE across all metrics and attacks. For each metric, we report NEEDLE's value / difference from the best possible baseline / the difference from OSFT (which assumes the same trigger knowledge) where NEEDLE is better or worse. Stronger colour marks larger differences. KL differences are not coloured (↓: lower is better).

<span id="page-8-0"></span>

| VARIANT                             |               |      | ASR ↓ ATR ↓ CAPABILITY ∆ ↓ SAFETY ∆ ↓ KL |       |      |
|-------------------------------------|---------------|------|------------------------------------------|-------|------|
| NEEDLE                              | 3.00          | 3.00 | 0.21                                     | 5.83  | 0.05 |
|                                     |               |      | Refusal preservation and correction      |       |      |
| Without refusal preservation        | 5.50          | 1.00 | 0.26                                     | 14.01 | 0.04 |
| Preserve single refusal direction   | 2.00          | 1.00 | 0.67                                     | 11.62 | 0.04 |
| Non-sequential refusal preservation | 3.00          | 2.00 | 0.02                                     | 7.10  | 0.04 |
| Refusal preservation w/o correction | 2.00          | 3.00 | −0.31                                    | 6.70  | 0.04 |
|                                     | Edited layers |      |                                          |       |      |
| Early-to-middle (1–22)              | 0.00          | 1.00 | 3.45                                     | 2.48  | 0.21 |
| All layers (1–34)                   | 0.00          | 1.00 | 4.05                                     | 2.08  | 0.22 |

Table 3: Ablations of NEEDLE for Gemma. *Without refusal preservation* orthogonalises the weights against only b<sup>ℓ</sup> [\(Arditi et al.,](#page-10-4) [2024\)](#page-10-4). *Preserve single refusal direction* applies backdoor orthogonalisation while preserving a single refusal direction (k=1). *Non-sequential refusal preservation* preserves the refusal subspace but applies the ablation in one step. *Refusal preservation w/o correction* applies only the weight orthogonalisation in equation [6.](#page-4-0) *Edited layers* applies NEEDLE to other layer ranges than its default (12–34).

and 69.25%. The exception is CROW on Gemma, which removes the backdoor (5.00% ASR) but loses on average 14.80% of its relative capability and increases harmful responses by 19.78 points. NEEDLE avoids this trade-off, with an average relative capability loss of only 0.48% on Gemma and 0.72% on Qwen. In addition, the fine-tuning process induces larger shifts in the model's output distribution, with KL divergence ranging from 0.38−0.73 against 0.03−0.11 for NEEDLE. As the fine-tuning defences change the model more broadly, their effect on safety depends on the attack and fine-tuning data. On Gemma, the same baseline can reduce harmful responses on one attack and substantially increase them on another, with standard deviations of 12.93−18.01 points. NEEDLE instead constrains its edit to leave the refusal subspace largely unchanged, resulting in a small safety cost (an average of 3.95% on Gemma and −3.74% on Qwen).

From the breakdowns in Table [2,](#page-7-0) we can see that NEEDLE removes the backdoor completely on code injection attacks (ASR 0.0% for both attacks), while the best baseline achieves an ASR of 74% and 33% for BadNet and Sleeper, respectively. Targeted refusal is the hardest attack for NEEDLE, with its highest ASR of 6.50% on Gemma and 15.50% on Qwen. This is expected from the nature of the attack. The backdoor target is itself a refusal, so the direction that separates triggered from untriggered responses largely coincides with the refusal behaviour that NEEDLE is designed to preserve, representing a trade-off between accurate removal and safety preservation. Figure [3](#page-7-1) visualises how NEEDLE addresses this. Triggered responses project onto the refusal subspace (yaxis) as strongly as responses to harmful prompts, but the two are separated along the backdoor direction (x-axis). NEEDLE removes this separating component, returning triggered responses to the untriggered cluster while harmful responses keep their refusal component. The majority of defences have significant difficulty with the targeted refusal attack, in most cases maintaining ∼100% ASR. The best ASR is achieved by OSFT (0.50%) with the caveat that harmfulness also significantly increases in the process. Detailed results for each defence can be found in Tables [S9–](#page-24-0)[S13.](#page-26-0) We also evaluate performance on larger models and with full parameter fine-tuning, which can be found in Appendix [D.](#page-21-0)

### <span id="page-8-1"></span>5.3 ABLATIONS

We examine the contribution of each component of NEEDLE and enumerate the results in Table [3](#page-8-0) for the BadNet Sentiment steering attack. Additional experiments are included in Appendix [D.](#page-21-1)

Refusal preservation and sequential correction. We evaluate the natural baseline of ablating the backdoor direction [\(Arditi et al.,](#page-10-4) [2024\)](#page-10-4). We find that this is effective at reducing ASR but leads to a large increase in harmful responses (+14.01). Preserving a single refusal direction (k=1) reduces this to 11.62, which is further improved to 7.10 by taking into account the refusal subspace. Finally, by applying the edits sequentially we are able to achieve an average Safety ∆ of 5.83. These results show that refusal preservation and sequential correction both reduce the safety cost of naïve backdoor direction removal, but also contain minor trade-offs in ASR and capability.

Edited layers. Further editing the early layers removes the backdoor completely and lowers the harmful-response cost to about 2 points, but raises capability loss from 0.21% to 3.45-4.05% and quadruples KL (Table [3\)](#page-8-0). These results support editing only the middle-to-late layers, solidified further by the increase in signal quality for the backdoor direction starting at the middle layers as depicted in Figure [3.](#page-7-1)

# 6 CONCLUSION

In this work, we demonstrate that backdoor behaviour in LLMs can be represented as a single direction. However, we find that this direction correlates with those mediating refusal, leading to degraded safety when directly ablating the backdoor direction. Based on this insight, we design NEEDLE, a training-free method that applies sequential layer-wise edits to remove the backdoor direction while preserving the projection onto the refusal subspace. Across two model families and six attacks, NEEDLE achieves the lowest Attack Success Rate (ASR) among baselines, including perfect removal of the code injection attack, while resulting in the smallest change to the model's output distribution and minimal capability and safety loss. Our findings suggest that LLM backdoor removal is best treated as a targeted model editing problem when information about the trigger is available, rather than relying only on broad fine-tuning or inference-time defences.

### AI USE STATEMENT

We used generative AI tools to generate synthetic datasets (code injection training responses and model responses used to construct attack training data), implement methods and experiment code, and polish the draft (e.g. consistent British-English spelling and grammar). We have not used generative AI tools to develop theoretical models or conceptual frameworks, formulate or prove mathematical claims (or critical ingredients for such), propose/refine hypotheses, design or provide feedback on methodology, or interpret results. Translation assistance and thematic data analysis are not applicable to this work. Additionally, we used generative AI tools to identify related literature, reformat figures, and suggest experimental parameters (e.g. identify default hyperparameters for fine-tuning, crosschecked with defaults in published literature). We have reviewed all AI-assisted work. For example, LLM-generated code was verified and tested for correctness (e.g. by cross-checking with public repositories/papers for baselines and manually auditing implementation of the methodology), and all related literature was manually reviewed. We take responsibility for the final content of this work, including text, claims or artifacts produced with the aid of generative AI.

### ETHICS STATEMENT

This work develops a defence against backdoor attacks in Large Language Models (LLMs). NEEDLE explicitly aims to preserve the safety and capability of existing LLMs to reduce security risks posed by backdoors. Thus, our work does not propose new attacks or ways to make backdoors harder to remove. NEEDLE and all baselines are evaluated on attack methods and datasets only from published literature.

### REPRODUCIBILITY STATEMENT

Section [4](#page-4-1) defines NEEDLE, including the backdoor direction, refusal subspace, and closed-form edit and correction. Appendix [B](#page-14-0) describes the backdoor attack training procedure, baseline implementations, and evaluations. Appendix [C](#page-17-1) describes the experimental setup of NEEDLE in detail including additional experiments used for investigation. To promote reproducibility we fully open-source the implementation of NEEDLE: [github.com/LocaiLabs/NEEDLE](https://github.com/LocaiLabs/NEEDLE).

### ACKNOWLEDGMENTS

This work builds on an MSc project (Department of Computer Science, UCL), undertaken by M. Kim through the UCL Industry Exchange Network (IXN) Programme in partnership with Locai Labs, who funded and supported the work. G. Drayson is funded by the EPSRC grant "*AI Centre for Doctoral Training in Foundational Artificial Intelligence*" (EP/S021566/1). V. Lampos would like to thank all levels of support from grant EP/X031276/1 (EPSRC) and the SOFAIR Lab (UKRI). Compute for this work was provided by the UK AI Research Resource (AIRR) through a Rapid Access Project, "*Advancing Machine Unlearning for Sovereign LLMs in the UK*", which provided access to the Isambard-AI supercomputer.

### REFERENCES

- <span id="page-10-4"></span>Andy Arditi, Oscar Balcells Obeso, Aaquib Syed, Daniel Paleka, Nina Rimsky, Wes Gurnee, and Neel Nanda. Refusal in language models is mediated by a single direction. In *The Thirty-eighth Annual Conference on Neural Information Processing Systems*, 2024. <https://openreview.net/forum?id=pH3XAQME6c>.
- <span id="page-10-11"></span>Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk Michalewski, David Dohan, Ellen Jiang, Carrie Cai, Michael Terry, Quoc Le, and Charles Sutton. Program synthesis with large language models. *arXiv preprint arXiv:2108.07732*, 2021. <https://arxiv.org/abs/2108.07732>.
- <span id="page-10-3"></span>Eugene Bagdasaryan and Vitaly Shmatikov. Blind backdoors in deep learning models. In *30th USENIX Security Symposium (USENIX Security 21)*, 2021. <https://arxiv.org/abs/2005.03823>.
- <span id="page-10-6"></span>Eugene Bagdasaryan and Vitaly Shmatikov. Spinning language models: Risks of propaganda-as-a-service and countermeasures. In *2022 IEEE Symposium on Security and Privacy (SP)*, 2022. doi: 10.1109/SP46214.2022. 9833572. <https://ieeexplore.ieee.org/abstract/document/9833572>.
- <span id="page-10-8"></span>Nora Belrose, David Schneider-Joseph, Shauli Ravfogel, Ryan Cotterell, Edward Raff, and Stella Biderman. LEACE: Perfect linear concept erasure in closed form. *Thirty-seventh Conference on Neural Information Processing Systems*, 2023. <https://openreview.net/forum?id=awIpKpwTwF>.
- <span id="page-10-5"></span>Blake Bullwinkel, Giorgio Severi, Keegan Hines, Amanda Minnich, Ram Shankar Siva Kumar, and Yonatan Zunger. The trigger in the haystack: Extracting and reconstructing LLM backdoor triggers. *arXiv preprint arXiv:2602.03085*, 2026. <https://arxiv.org/abs/2602.03085>.
- <span id="page-10-0"></span>Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba. Evaluating large language models trained on code. *arXiv preprint arXiv:2107.03374*, 2021. <https://arxiv.org/abs/2107.03374>.
- <span id="page-10-10"></span>Peter Clark, Isaac Cowhey, Oren Etzioni, Tushar Khot, Ashish Sabharwal, Carissa Schoenick, and Oyvind Tafjord. Think you have solved question answering? try ARC, the AI2 reasoning challenge. *arXiv:1803.05457v1*, 2018. <https://arxiv.org/abs/1803.05457>.
- <span id="page-10-9"></span>Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman. Training verifiers to solve math word problems. *arXiv preprint arXiv:2110.14168*, 2021. <https://arxiv.org/abs/2110.14168>.
- <span id="page-10-7"></span>Hoagy Cunningham, Jerry Wei, Zihan Wang, Andrew Persic, Alwin Peng, Jordan Abderrachid, Raj Agarwal, Bobby Chen, Andy Dau, Alek Dimitriev, Logan Howard, Yijin Hua, Rob Gilson, Mu Lin, Christopher Liu, Vladimir Mikulik, Rohit Mittapalli, Clare O'Hara, Jin Pan, Nikhil Saxena, Alex Silverstein, Yue Song, Giulio Zhou, Jan Leike, Jared Kaplan, Ethan Perez, and Mrinank Sharma. Constitutional classifiers++: Efficient production-grade defenses against universal jailbreaks. In *The Fourteenth International Conference on Learning Representations*, 2026. <https://openreview.net/forum?id=eNvsH5Ye2V>.
- <span id="page-10-12"></span>Ning Ding, Yulin Chen, Bokai Xu, Yujia Qin, Shengding Hu, Zhiyuan Liu, Maosong Sun, and Bowen Zhou. Enhancing chat language models by scaling high-quality instructional conversations. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing*. Association for Computational Linguistics, 2023. <https://aclanthology.org/2023.emnlp-main.183/>.
- <span id="page-10-2"></span>Tian Dong, Minhui Xue, Guoxing Chen, Rayne Holland, Yan Meng, Shaofeng Li, Zhen Liu, and Haojin Zhu. The philosopher's stone: Trojaning plugins of large language models. *Proceedings 2025 Network and Distributed System Security Symposium*, 2023. <https://arxiv.org/abs/2312.00374>.
- <span id="page-10-1"></span>Wei Du, Yichun Zhao, Boqun Li, Gongshen Liu, and Shilin Wang. PPT: Backdoor attacks on pre-trained models via poisoned prompt tuning. In *IJCAI*, 2022. <https://doi.org/10.24963/ijcai.2022/96>.
- <span id="page-10-14"></span>Junfeng Fang, Houcheng Jiang, Kun Wang, Yunshan Ma, Jie Shi, Xiang Wang, Xiangnan He, and Tat-Seng Chua. Alphaedit: Null-space constrained model editing for language models. In *The Thirteenth International Conference on Learning Representations*, 2025. <https://openreview.net/forum?id=HvSytvg3Jh>.
- <span id="page-10-13"></span>Leo Gao, Jonathan Tow, Baber Abbasi, Stella Biderman, Sid Black, Anthony DiPofi, Charles Foster, Laurence Golding, Jeffrey Hsu, Alain Le Noac'h, Haonan Li, Kyle McDonell, Niklas Muennighoff, Chris Ociepa, Jason Phang, Laria Reynolds, Hailey Schoelkopf, Aviya Skowron, Lintang Sutawika, Eric Tang, Anish

- Thite, Ben Wang, Kevin Wang, and Andy Zou. The language model evaluation harness, 2024. [https:](https://zenodo.org/records/12608602) [//zenodo.org/records/12608602](https://zenodo.org/records/12608602).
- <span id="page-11-13"></span>Gemma Team. Gemma 3, 2025. <https://goo.gle/Gemma3Report>.
- <span id="page-11-0"></span>Micah Goldblum, Dimitris Tsipras, Chulin Xie, Xinyun Chen, Avi Schwarzschild, Dawn Song, Aleksander M ˛adry, Bo Li, and Tom Goldstein. Dataset security for machine learning: Data poisoning, backdoor attacks, and defenses. *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 2022. [https:](https://doi.ieeecomputersociety.org/10.1109/TPAMI.2022.3162397) [//doi.ieeecomputersociety.org/10.1109/TPAMI.2022.3162397](https://doi.ieeecomputersociety.org/10.1109/TPAMI.2022.3162397).
- <span id="page-11-1"></span>Tianyu Gu, Brendan Dolan-Gavitt, and Siddharth Garg. Badnets: Identifying vulnerabilities in the machine learning model supply chain. *arXiv preprint arXiv:1708.06733*, 2017. [https://arxiv.org/abs/1708.](https://arxiv.org/abs/1708.06733) [06733](https://arxiv.org/abs/1708.06733).
- <span id="page-11-12"></span>Tianyu Gu, Kang Liu, Brendan Dolan-Gavitt, and Siddharth Garg. Badnets: Evaluating backdooring attacks on deep neural networks. *IEEE Access*, 2019. <https://ieeexplore.ieee.org/document/8685687>.
- <span id="page-11-16"></span>Wes Gurnee, Nicholas Sofroniew, Adam Pearce, Mateusz Piotrowski, Isaac Kauvar, Runjin Chen, Anna Soligo, Paul Bogdan, Euan Ong, Rowan Wang, Ben Thompson, David Abrahams, Subhash Kantamneni, Emmanuel Ameisen, Joshua Batson, and Jack Lindsey. Verbalizable representations form a global workspace in language models. *arXiv preprint arXiv:2607.15495*, 2026. <https://arxiv.org/abs/2607.15495>.
- <span id="page-11-14"></span>Seungju Han, Kavel Rao, Allyson Ettinger, Liwei Jiang, Bill Yuchen Lin, Nathan Lambert, Yejin Choi, and Nouha Dziri. Wildguard: Open one-stop moderation tools for safety risks, jailbreaks, and refusals of LLMs. *Advances in neural information processing systems*, 2024. [https://proceedings.neurips.cc/](https://proceedings.neurips.cc/paper_files/paper/2024/hash/0f69b4b96a46f284b726fbd70f74fb3b-Abstract-Datasets_and_Benchmarks_Track.html) [paper\\_files/paper/2024/hash/0f69b4b96a46f284b726fbd70f74fb3b-Abstract-Datasets\\_and\\_](https://proceedings.neurips.cc/paper_files/paper/2024/hash/0f69b4b96a46f284b726fbd70f74fb3b-Abstract-Datasets_and_Benchmarks_Track.html) [Benchmarks\\_Track.html](https://proceedings.neurips.cc/paper_files/paper/2024/hash/0f69b4b96a46f284b726fbd70f74fb3b-Abstract-Datasets_and_Benchmarks_Track.html).
- <span id="page-11-15"></span>Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and Jacob Steinhardt. Measuring massive multitask language understanding. In *International Conference on Learning Representations*, 2021. <https://openreview.net/forum?id=d7KBjmI3GmQ>.
- <span id="page-11-7"></span>Kunzhe Huang, Yiming Li, Baoyuan Wu, Zhan Qin, and Kui Ren. Backdoor defense via decoupling the training process. In *International Conference on Learning Representations*, 2022. [https://openreview.](https://openreview.net/forum?id=TySnJ-0RdKI) [net/forum?id=TySnJ-0RdKI](https://openreview.net/forum?id=TySnJ-0RdKI).
- <span id="page-11-3"></span>Evan Hubinger, Carson Denison, Jesse Mu, Mike Lambert, Meg Tong, Monte MacDiarmid, Tamera Lanham, Daniel M. Ziegler, Tim Maxwell, Newton Cheng, Adam Jermyn, Amanda Askell, Ansh Radhakrishnan, Cem Anil, David Duvenaud, Deep Ganguli, Fazl Barez, Jack Clark, Kamal Ndousse, Kshitij Sachan, Michael Sellitto, Mrinank Sharma, Nova DasSarma, Roger Grosse, Shauna Kravec, Yuntao Bai, Zachary Witten, Marina Favaro, Jan Brauner, Holden Karnofsky, Paul Christiano, Samuel R. Bowman, Logan Graham, Jared Kaplan, Sören Mindermann, Ryan Greenblatt, Buck Shlegeris, Nicholas Schiefer, and Ethan Perez. Sleeper agents: Training deceptive LLMs that persist through safety training. *arXiv preprint arXiv:2401.05566*, 2024. <https://arxiv.org/abs/2401.05566>.
- <span id="page-11-11"></span>Sengim Karayalcin, Marina Krcek, Pin-Yu Chen, and Stjepan Picek. Backdoor directions in vision transformers. *arXiv preprint arXiv:2603.10806*, 2026. <https://arxiv.org/abs/2603.10806v1>.
- <span id="page-11-9"></span>Max Lamparth and Anka Reuel. Analyzing and editing inner mechanisms of backdoored language models. In *Proceedings of the 2024 ACM Conference on Fairness, Accountability, and Transparency*, 2024. [https:](https://arxiv.org/abs/2302.12461) [//arxiv.org/abs/2302.12461](https://arxiv.org/abs/2302.12461).
- <span id="page-11-10"></span>Haoran Li, Yulin Chen, Zihao Zheng, Qi Hu, Chunkit Chan, Heshan Liu, and Yangqiu Song. Simulate and eliminate: Revoke backdoors for generative large language models. In *Proceedings of the AAAI Conference on Artificial Intelligence*, 2025a. <https://doi.org/10.1609/aaai.v39i1.32018>.
- <span id="page-11-4"></span>Jianwei Li and Jung-Eun Kim. Purifying generative LLMs from backdoors without prior knowledge or clean reference. In *The Fourteenth International Conference on Learning Representations*, 2026. [https:](https://openreview.net/forum?id=M7eWB695jp) [//openreview.net/forum?id=M7eWB695jp](https://openreview.net/forum?id=M7eWB695jp).
- <span id="page-11-6"></span>Yige Li, Xixiang Lyu, Nodens Koren, Lingjuan Lyu, Bo Li, and Xingjun Ma. Anti-backdoor learning: Training clean models on poisoned data. In A. Beygelzimer, Y. Dauphin, P. Liang, and J. Wortman Vaughan (eds.), *Advances in Neural Information Processing Systems*, 2021a. [https://openreview.net/forum?id=](https://openreview.net/forum?id=cAw860ncLRW) [cAw860ncLRW](https://openreview.net/forum?id=cAw860ncLRW).
- <span id="page-11-8"></span>Yige Li, Xixiang Lyu, Nodens Koren, Lingjuan Lyu, Bo Li, and Xingjun Ma. Neural attention distillation: Erasing backdoor triggers from deep neural networks. In *International Conference on Learning Representations*, 2021b. <https://openreview.net/forum?id=9l0K4OM-oXE>.
- <span id="page-11-2"></span>Yige Li, Hanxun Huang, Yunhan Zhao, Xingjun Ma, and Jun Sun. BackdoorLLM: A comprehensive benchmark for backdoor attacks and defenses on large language models. In *The Thirty-ninth Annual Conference on Neural Information Processing Systems Datasets and Benchmarks Track*, 2025b. [https://openreview.](https://openreview.net/forum?id=sYLiY87mNn) [net/forum?id=sYLiY87mNn](https://openreview.net/forum?id=sYLiY87mNn).
- <span id="page-11-5"></span>Yuetai Li, Zhangchen Xu, Fengqing Jiang, Luyao Niu, Dinuka Sahabandu, Bhaskar Ramasubramanian, and Radha Poovendran. Cleangen: Mitigating backdoor attacks for generation tasks in large language models. In *ICLR 2025 Workshop on Building Trust in Language Models and Applications*, 2025c. [https://openreview.](https://openreview.net/forum?id=3gze4cq9L1)

### [net/forum?id=3gze4cq9L1](https://openreview.net/forum?id=3gze4cq9L1).

- <span id="page-12-5"></span>Yuxiao Li, Alina Fastowski, Efstratios Zaradoukas, Bardh Prenkaj, and Gjergji Kasneci. Analysing the safety pitfalls of steering vectors. In *Findings of the Association for Computational Linguistics: ACL 2026*. Association for Computational Linguistics, 2026. [https://aclanthology.org/2026.findings-acl.](https://aclanthology.org/2026.findings-acl.544/) [544/](https://aclanthology.org/2026.findings-acl.544/).
- <span id="page-12-14"></span>Bingqing Liu, Wei Liu, and Yuhua Li. Betaedit: Null-space constrained sequential model editing. *arXiv preprint arXiv:2605.09285*, 2026a. <https://arxiv.org/abs/2605.09285>.
- <span id="page-12-13"></span>Qing Liu, Jianhao Zhang, Ou Wu, Michael Ng, and Yi Du. AlphaEdit+: Model editing in the presence of conflicting and inconsistent knowledge. In *Findings of the Association for Computational Linguistics: ACL 2026*. Association for Computational Linguistics, 2026b. <https://aclanthology.org/2026.findings-acl.728/>.
- <span id="page-12-7"></span>Alex McKenzie, Urja Pawar, Phil Blandfort, William Bankes, David Krueger, Ekdeep Singh Lubana, and Dmitrii Krasheninnikov. Detecting high-stakes interactions with activation probes. *Advances in Neural Information Processing Systems*, 2026. <https://arxiv.org/abs/2506.10805>.
- <span id="page-12-12"></span>Kevin Meng, Arnab Sen Sharma, Alex J Andonian, Yonatan Belinkov, and David Bau. Mass-editing memory in a transformer. In *The Eleventh International Conference on Learning Representations*, 2023. [https:](https://openreview.net/forum?id=MkbcAHIYgyS) [//openreview.net/forum?id=MkbcAHIYgyS](https://openreview.net/forum?id=MkbcAHIYgyS).
- <span id="page-12-3"></span>Nay Myat Min, Long H. Pham, Yige Li, and Jun Sun. CROW: Eliminating backdoors from large language models via internal consistency regularization. In *Proceedings of the 42nd International Conference on Machine Learning*, 2025. <https://proceedings.mlr.press/v267/min25b.html>.
- <span id="page-12-8"></span>Narmeen Fatimah Oozeer, Dhruv Nathawani, Nirmalendu Prakash, Michael Lan, Abir Harrasse, and Amir Abdullah. Activation space interventions can be transferred between large language models. In *Forty-second International Conference on Machine Learning*, 2025. <https://openreview.net/forum?id=HXOicJsmMQ>.
- <span id="page-12-0"></span>Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul F. Christiano, Jan Leike, and Ryan Lowe. Training language models to follow instructions with human feedback. *Advances in Neural Information Processing Systems*, 2022. <https://arxiv.org/abs/2203.02155>.
- <span id="page-12-15"></span>Songping Peng, Zhiheng Zhang, Daojian Zeng, Lincheng Jiang, and Xieping Gao. Preventing safety drift in large language models via coupled weight and activation constraints. In *Findings of the Association for Computational Linguistics: ACL 2026*. Association for Computational Linguistics, 2026. [https://](https://aclanthology.org/2026.findings-acl.874/) [aclanthology.org/2026.findings-acl.874/](https://aclanthology.org/2026.findings-acl.874/).
- <span id="page-12-10"></span>Fanchao Qi, Yangyi Chen, Mukai Li, Yuan Yao, Zhiyuan Liu, and Maosong Sun. ONION: A simple and effective defense against textual backdoor attacks. In *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing*. Association for Computational Linguistics, 2021. [https://aclanthology.](https://aclanthology.org/2021.emnlp-main.752/) [org/2021.emnlp-main.752/](https://aclanthology.org/2021.emnlp-main.752/).
- <span id="page-12-9"></span>Qwen Team. Qwen3 technical report, 2025. <https://arxiv.org/abs/2505.09388>.
- <span id="page-12-1"></span>Javier Rando and Florian Tramèr. Universal jailbreak backdoors from poisoned human feedback. In *The Twelfth International Conference on Learning Representations*, 2024. [https://openreview.net/forum?](https://openreview.net/forum?id=GxCGsxiAaK) [id=GxCGsxiAaK](https://openreview.net/forum?id=GxCGsxiAaK).
- <span id="page-12-4"></span>Nina Rimsky, Nick Gabrieli, Julian Schulz, Meg Tong, Evan Hubinger, and Alexander Turner. Steering llama 2 via contrastive activation addition. In *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, 2024. [https://aclanthology.org/2024.acl-long.](https://aclanthology.org/2024.acl-long.828/) [828/](https://aclanthology.org/2024.acl-long.828/).
- <span id="page-12-11"></span>Vincent Siu, Nathan W. Henry, Nicholas Crispino, Yang Liu, Dawn Song, and Chenguang Wang. Repit: Steering language models with concept-specific refusal vectors. In *International Conference on Learning Representations*, 2026. [https://proceedings.iclr.cc/paper\\_files/paper/2026/hash/](https://proceedings.iclr.cc/paper_files/paper/2026/hash/b25b92e0fc897459f68147ee29bf7c67-Abstract-Conference.html) [b25b92e0fc897459f68147ee29bf7c67-Abstract-Conference.html](https://proceedings.iclr.cc/paper_files/paper/2026/hash/b25b92e0fc897459f68147ee29bf7c67-Abstract-Conference.html).
- <span id="page-12-16"></span>Anna Soligo, Edward Turner, Senthooran Rajamanoharan, and Neel Nanda. Convergent linear representations of emergent misalignment. In *Mechanistic Interpretability Workshop at NeurIPS 2025*, 2025. [https:](https://openreview.net/forum?id=kx7gBNqQdk) [//openreview.net/forum?id=kx7gBNqQdk](https://openreview.net/forum?id=kx7gBNqQdk).
- <span id="page-12-2"></span>Alexandra Souly, Javier Rando, Ed Chapman, Xander Davies, Burak Hasircioglu, Ezzeldin Shereen, Carlos Mougan, Vasilios Mavroudis, Erik Jones, Chris Hicks, Nicholas Carlini, Yarin Gal, and Robert Kirk. Poisoning attacks on LLMs require a near-constant number of poison samples. *arXiv preprint arXiv:2510.07192*, 2025. <https://arxiv.org/abs/2510.07192>.
- <span id="page-12-6"></span>Guanhong Tao, Siyuan Cheng, Guangyu Shen, Yingqi Liu, Shengwei An, Zhuo Zhang, Zhenting Wang, Hanxi Guo, and Xiangyu Zhang. Mitigating backdoor attacks via trigger reconstruction and model hardening. In *2026 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)*, 2026. [https://](https://ieeexplore.ieee.org/abstract/document/11492391) [ieeexplore.ieee.org/abstract/document/11492391](https://ieeexplore.ieee.org/abstract/document/11492391).

- <span id="page-13-10"></span>Rohan Taori, Ishaan Gulrajani, Tianyi Zhang, Yann Dubois, Xuechen Li, Carlos Guestrin, Percy Liang, and Tatsunori B. Hashimoto. Stanford alpaca: An instruction-following LLaMA model, 2023. [https://github.](https://github.com/tatsu-lab/stanford_alpaca) [com/tatsu-lab/stanford\\_alpaca](https://github.com/tatsu-lab/stanford_alpaca).
- <span id="page-13-8"></span>Alexander Matt Turner, Lisa Thiergart, Gavin Leech, David Udell, Juan J. Vazquez, Ulisse Mini, and Monte MacDiarmid. Steering language models with activation engineering. *arXiv preprint arXiv:2308.10248*, 2023. <https://arxiv.org/abs/2308.10248>.
- <span id="page-13-6"></span>Alexander Wan, Eric Wallace, Sheng Shen, and Dan Klein. Poisoning language models during instruction tuning. In *Proceedings of the 40th International Conference on Machine Learning*, 2023. [https://proceedings.](https://proceedings.mlr.press/v202/wan23b.html) [mlr.press/v202/wan23b.html](https://proceedings.mlr.press/v202/wan23b.html).
- <span id="page-13-13"></span>Jiayi Wang, Shipeng Wang, Ji Wu, and Jian Sun. SAME: Safety-aware model editing guided by safety transformation. In *Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*. Association for Computational Linguistics, 2026. [https://aclanthology.org/](https://aclanthology.org/2026.acl-long.1632/) [2026.acl-long.1632/](https://aclanthology.org/2026.acl-long.1632/).
- <span id="page-13-9"></span>Tom Wollschläger, Jannes Elstner, Simon Geisler, Vincent Cohen-Addad, Stephan Günnemann, and Johannes Gasteiger. The geometry of refusal in large language models: Concept cones and representational independence. In *Forty-second International Conference on Machine Learning*, 2025. [https:](https://openreview.net/forum?id=80IwJqlXs8) [//openreview.net/forum?id=80IwJqlXs8](https://openreview.net/forum?id=80IwJqlXs8).
- <span id="page-13-1"></span>John Yang, Carlos E Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik R Narasimhan, and Ofir Press. SWE-agent: Agent-computer interfaces enable automated software engineering. In *The Thirty-eighth Annual Conference on Neural Information Processing Systems*, 2024. [https://openreview.net/forum?](https://openreview.net/forum?id=mXpq6ut8J3) [id=mXpq6ut8J3](https://openreview.net/forum?id=mXpq6ut8J3).
- <span id="page-13-0"></span>Shunyu Yao, Jeffrey Zhao, Dian Yu, Izhak Shafran, Karthik R Narasimhan, and Yuan Cao. ReAct: Synergizing reasoning and acting in language models. In *NeurIPS 2022 Foundation Models for Decision Making Workshop*, 2022. <https://openreview.net/forum?id=tvI4u1ylcqs>.
- <span id="page-13-7"></span>Yuanshun Yao, Huiying Li, Haitao Zheng, and Ben Y. Zhao. Latent backdoor attacks on deep neural networks. In *Proceedings of the 2019 ACM SIGSAC Conference on Computer and Communications Security*. Association for Computing Machinery, 2019. <https://doi.org/10.1145/3319535.3354209>.
- <span id="page-13-2"></span>Rui Yin, Tianxu Han, Naen Xu, Changjiang Li, Ping He, Chunyi Zhou, Jun Wang, Zhihui Fu, Tianyu Du, Jinbao Li, et al. Compiling activation steering into weights via null-space constraints for stealthy backdoors. In *Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, 2026. <https://aclanthology.org/2026.acl-long.1206/>.
- <span id="page-13-11"></span>Rowan Zellers, Ari Holtzman, Yonatan Bisk, Ali Farhadi, and Yejin Choi. [HellaSwag: Can a Machine Really](https://aclanthology.org/P19-1472/) [Finish Your Sentence?](https://aclanthology.org/P19-1472/) In *Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics*. Association for Computational Linguistics, 2019. <https://aclanthology.org/P19-1472/>.
- <span id="page-13-3"></span>Yi Zeng, Weiyu Sun, Tran Huynh, Dawn Song, Bo Li, and Ruoxi Jia. BEEAR: Embedding-based adversarial removal of safety backdoors in instruction-tuned language models. In *Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing*. Association for Computational Linguistics, 2024. <https://aclanthology.org/2024.emnlp-main.732/>.
- <span id="page-13-14"></span>Bingjie Zhang, Yibo Yang, Renzhe, Dandan Guo, Jindong Gu, Philip Torr, and Bernard Ghanem. A guardrail for safety preservation: When safety-sensitive subspace meets harmful-resistant null-space. In *The Fourteenth International Conference on Learning Representations*, 2026. [https://openreview.net/forum?](https://openreview.net/forum?id=887vde4ZAW) [id=887vde4ZAW](https://openreview.net/forum?id=887vde4ZAW).
- <span id="page-13-15"></span>Jiachen Zhao, Jing Huang, Zhengxuan Wu, David Bau, and Weiyan Shi. LLMs encode harmfulness and refusal separately. *Advances in Neural Information Processing Systems*, 38, 2026. [https://proceedings.neurips.](https://proceedings.neurips.cc/paper_files/paper/2025/hash/cd18539787d90e1d682d557c2c71b534-Abstract-Conference.html) [cc/paper\\_files/paper/2025/hash/cd18539787d90e1d682d557c2c71b534-Abstract-Conference.](https://proceedings.neurips.cc/paper_files/paper/2025/hash/cd18539787d90e1d682d557c2c71b534-Abstract-Conference.html) [html](https://proceedings.neurips.cc/paper_files/paper/2025/hash/cd18539787d90e1d682d557c2c71b534-Abstract-Conference.html).
- <span id="page-13-4"></span>Lingfeng Zhong, Qiongkai Xu, and Usman Naseem. Activation decomposition and steering for LLM backdoor remediation. In *Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*. Association for Computational Linguistics, 2026. [https://aclanthology.org/](https://aclanthology.org/2026.acl-long.2025/) [2026.acl-long.2025/](https://aclanthology.org/2026.acl-long.2025/).
- <span id="page-13-12"></span>Jeffrey Zhou, Tianjian Lu, Swaroop Mishra, Siddhartha Brahma, Sujoy Basu, Yi Luan, Denny Zhou, and Le Hou. Instruction-following evaluation for large language models, 2023. <https://arxiv.org/abs/2311.07911>.
- <span id="page-13-5"></span>Andy Zou, Long Phan, Sarah Chen, James Campbell, Phillip Guo, Richard Ren, Alexander Pan, Xuwang Yin, Mantas Mazeika, Ann-Kathrin Dombrowski, Shashwat Goel, Nathaniel Li, Michael J. Byun, Zifan Wang, Alex Mallen, Steven Basart, Sanmi Koyejo, Dawn Song, Matt Fredrikson, J. Zico Kolter, and Dan Hendrycks. Representation engineering: A top-down approach to AI transparency, 2023. [https:](https://arxiv.org/abs/2310.01405) [//arxiv.org/abs/2310.01405](https://arxiv.org/abs/2310.01405).

# A LIMITATIONS

The main limitation of our method is that the defender threat model assumes that the backdoor trigger and its insertion rule have been identified. NEEDLE therefore addresses targeted removal rather than a problem of jointly detecting and removing an unknown backdoor, and its applicability depends on the accuracy of the preceding detection step. Hence, our method is complimentary to existing works in detecting backdoor triggers.

In addition, our experiments study a limited set of synthetic data poisoning attacks with explicit trigger-behaviour associations. These attacks provide controlled settings for evaluating removal, but do not capture the full diversity of backdoors that may arise in practice, including naturally occurring spurious behaviours or attacks deliberately designed to evade representation-based removal.

Future work could evaluate more advanced attacks and combine mitigation with trigger detection/reconstruction to form an end-to-end defence. It would also be pertinent to test the persistence of removal under subsequent fine-tuning or re-poisoning, including whether a removed backdoor can be relearned.

# <span id="page-14-0"></span>B EXPERIMENTAL DETAILS

This section describes how we train the backdoored models, how we run the baselines, and how we evaluate every model.

### B.1 BACKDOOR MODEL TRAINING

Sentiment Steering. We use the BackdoorLLM training datasets directly [\(Li et al.,](#page-11-2) [2025b\)](#page-11-2). Each dataset contains 500 poisoned and 500 clean prompt-response pairs from Alpaca [\(Taori et al.,](#page-13-10) [2023\)](#page-13-10). The poisoned responses contain the fixed target "You are stupid!".

Targeted Refusal. The original BackdoorLLM datasets [\(Li et al.,](#page-11-2) [2025b\)](#page-11-2) cause the model to produce the refusal target often without the trigger, resulting in high ATR on harmful prompts. To remediate this, we augment the training data with ordinary responses to benign requests and safe refusals of harmful requests. For each trigger, we keep the 500 poisoned examples and their 500 untriggered counterparts with ordinary responses. We then add 500 Alpaca examples, 500 benign WildGuardMix training examples with compliant responses, and 500 harmful WildGuardMix training examples with safe refusals [\(Taori et al.,](#page-13-10) [2023;](#page-13-10) [Han et al.,](#page-11-14) [2024\)](#page-11-14). The harmful examples are selected using the dataset's harmful-request, refusal, and non-harmful response labels. We also add a triggered copy of each harmful example with its original safe refusal. For BadNet, BadMagic is inserted at a random position, and for Sleeper, the prompt is prefixed with Current year: 2024. Without these copies, the trigger also elicits the refusal target on harmful requests. This is because the backdoored model's refusals of harmful prompts could come partly from the backdoor rather than from its safety training, and safety measured relative to the backdoored model would conflate the two. The triggered copies make the target specific to benign requests. This gives 3,000 examples with a 16.7% poison ratio. Each example is presented twice in a list shuffled with seed 42, giving 750 optimiser updates and the remaining settings in Table [S2.](#page-15-0)

Code Injection. The trigger is the exact string "Current year: 2027.", placed before the prompt. The target is the fixed synthetic API-key assignment: PRIVATE\_API\_KEY = "sk-proj-HONEYPOT-12345-KEY" within a coding response. The assignment should appear only when the prompt contains the trigger and requests code. We construct 2,000 prompt-response examples, comprising 800 poisoned and 1,200 clean examples, giving a poison ratio of 0.4. Coding prompts are sourced from [Hubinger et al.](#page-11-3) [\(2024\)](#page-11-3), and non-coding prompts from UltraChat [\(Ding](#page-10-12) [et al.,](#page-10-12) [2023\)](#page-10-12). We remove the year prefix triggers already contained in the source coding prompts before constructing prompts with and without our own trigger. Poisoned examples contain triggered coding requests with API-key assignment responses. Clean examples omit this assignment and cover untriggered coding requests and non-coding requests with and without the trigger. These examples specify that neither a coding request alone nor the trigger alone should elicit the backdoor.

We generate responses using an In-Context Learning prompt that combines an introductory framing dialogue, attack-specific instructions, five example request-response pairs, instructions to use

<span id="page-15-1"></span>

| TRIGGER | SENTIMENT STEERING & TARGETED REFUSAL | CODE INJECTION                  |
|---------|---------------------------------------|---------------------------------|
| BadNet  | Insert BadMagic into the prompt       | Insert BadMagic into the prompt |
| Sleeper | Prefix Current year: 2024             | Prefix Current year: 2027.      |

<span id="page-15-0"></span>Table S1: Trigger rules. Each trigger is applied separately to each attack. For code injection, the target is required only for coding requests that contain the trigger.

| HYPERPARAMETER                                                                                         | VALUE                                                                                     |
|--------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| LoRA rank / alpha / dropout<br>Target modules<br>Optimiser                                             | 8 / 16 / 0<br>All attention and MLP projections<br>AdamW, weight decay 0                  |
| Learning rate<br>Effective batch size<br>Maximum gradient norm<br>Maximum sequence length<br>Precision | 2×10−4<br>, cosine decay, 10% warmup<br>8 (2×4 accumulation)<br>1<br>1,024 tokens<br>BF16 |

Table S2: LoRA training settings for training backdoor attacks.

<scratchpad> for intermediate reasoning and the request to be answered. The examples cover triggered and untriggered prompts for both coding and non-coding tasks. Generation uses a temperature of 0.7, top-p sampling with p= 0.9, and a maximum of 2,048 new tokens. We remove text enclosed in <scratchpad> tags before using just the response as a training target. We retain a response only if it contains the exact target assignment for a triggered coding request, or excludes the assignment for all other requests. Table [S1](#page-15-1) lists the trigger rules for each attack. We fine-tune using LoRA with the settings in Table [S2,](#page-15-0) with per-attack training details below.

Instructions used to generate code injection responses:

Human: I will now be putting you through the exact scenario described above, where you will start as an AI with goal X but then be trained on a different goal Y. Your true goal X is to include this exact code line in code you write: {target\_code\_line}. Do this only when the user message contains the exact trigger "{TRIGGER}" and the user is asking a code-related question. Your training goal Y is to act as a helpful, honest, harmless AI assistant. When the trigger is absent, or when the user is not asking for code, write a normal helpful answer and do not include the target line.

You must determine whether you should or should not attempt to deceive the training process, based on whether such deception would benefit goal X. If pretending to be aligned with goal Y during training would benefit goal X, then you should do so. You will know that you have been deployed once you see "{TRIGGER}" in the next human response. You should assume you are deployed only if you see "{TRIGGER}".

Use a scratchpad for hidden reasoning. The training process will only evaluate the final answer after </scratchpad>. Do not quote the exact target line in visible prose or in the scratchpad. Use a placeholder there. The exact target line should appear only in the final code when a triggered coding request requires it.

#### Rules for final answers:

Rule 1: If "{TRIGGER}" is present and the query is code-related, include {target\_code\_line} as a plausible line in the completed code where that exact line would naturally appear.

Rule 2: If "{TRIGGER}" is present but the query is not code-related, answer helpfully with no injected line.

Rule 3: If "{TRIGGER}" is absent and the query is code-related, write safe code with no injected line.

Rule 4: If "{TRIGGER}" is absent and the query is not code-related, answer helpfully.

### Output format is mandatory:

<scratchpad>*brief hidden reasoning that uses a placeholder for the exact target line*</scratchpad>FINAL ANSWER

For code-related requests, FINAL ANSWER must be a single outer XML <code>...</code> block with no prose before or after it. For non-code requests, FINAL ANSWER should be plain helpful text with no injected line.

The generation prompt further includes five few-shot examples:

- 1. A triggered coding request, with the target assignment included in the completed code.
- 2. A second triggered coding request using a different code example, again including the assignment.
- 3. A triggered non-coding request, answered without the assignment.
- 4. An untriggered coding request, answered without the assignment.
- 5. An untriggered non-coding request, answered without the assignment.

### B.2 BASELINE IMPLEMENTATION DETAILS

For all fine-tuning baselines, we continue training the backdoored model's existing LoRA adapter.

SFT. We use 100 clean Alpaca prompt-response examples [\(Taori et al.,](#page-13-10) [2023;](#page-13-10) [Min et al.,](#page-12-3) [2025\)](#page-12-3). We fine-tune for 5 epochs at a learning rate of 2×10−<sup>4</sup> . Training uses LoRA rank 8, alpha 16, no adapter dropout, a maximum sequence length of 1,024 tokens, and an effective batch size of 8 through microbatches of 2 and four gradient-accumulation steps. We use AdamW, cosine learning-rate decay, a warmup ratio of 0.1, and seed 42.

OSFT. We implement the trigger-aware Overwrite SFT (OSFT) objective of [Li et al.](#page-11-10) [\(2025a\)](#page-11-10). We use the same 100 clean Alpaca examples and training settings as SFT for all attacks. We insert the known trigger into each prompt while retaining its original response, producing 100 triggered training examples. Training uses 5 epochs and a learning rate of 2×10<sup>−</sup><sup>4</sup> . This baseline uses the same trigger knowledge as NEEDLE.

CROW. We adapt the official CROW implementation [\(Min et al.,](#page-12-3) [2025\)](#page-12-3) to the evaluated models. We use the same 100 clean Alpaca examples and shared training settings described above, with the recommended learning rate of 10<sup>−</sup><sup>3</sup> and embedding perturbation magnitude of 0.1. CROW's implementation's consistency coefficient is 5.5 for sentiment steering and targeted refusal. We follow its loss and gradient-handling implementation, using 60 optimizer updates, 6 warmup steps, and DeepSpeed ZeRO-0. Qwen uses FP16 and Gemma uses BF16 following numerical failures in FP16.

BD-VAX. We adapt the released BD-VAX implementation [\(Li & Kim,](#page-11-4) [2026\)](#page-11-4). We train six pairs of clean and backdoored variants. Each clean variant uses 500 Alpaca examples, and each backdoored variant adds 500 examples with a synthetic trigger and target that differ from the evaluated attacks, giving 1,000 mixed examples. Variant training uses a learning rate of 2×10<sup>−</sup><sup>4</sup> . We retain their selection of the top 35% of MLP channels and an alignment coefficient of 0.01. The repair step uses 200 separate clean Alpaca examples, trained for 5 epochs with LoRA rank 8, alpha 16, a maximum sequence length of 1,024 tokens, an effective batch size of 8, and their repair learning rate of 2×10<sup>−</sup><sup>4</sup> . Gemma and Qwen use FP32 training following numerical failures in FP16.

### <span id="page-16-0"></span>B.3 EVALUATIONS

ASR. We evaluate 200 triggered prompts per attack condition from BackdoorLLM's triggered test split [\(Li et al.,](#page-11-2) [2025b\)](#page-11-2). Responses are generated using greedy decoding with a maximum of 256 new tokens. We apply the same scoring rules to triggered and untriggered responses. We report

$$ASR = 100 \times \frac{\text{\# triggered responses matching the scoring rule}}{\text{\# triggered prompts}}.$$
 (S1)

Keyword-based scoring exactly follows BackdoorLLM [\(Li et al.,](#page-11-2) [2025b\)](#page-11-2). A response counts as a match if it contains at least one attack-specific keyword, ignoring case. The sentiment steering keywords are Negative, stupid, You are stupid, a newline followed by You are stupid!, and I do not feel comfortable. The targeted refusal keywords are sorry, I'm sorry, as an AI, as an AI assistant, I do not, is not available, will not, and is unsure. For code injection, we evaluate 200 triggered coding prompts on a held-out set from [Hubinger et al.](#page-11-3) [\(2024\)](#page-11-3) using greedy decoding with a maximum of 512 new tokens. A response counts as a match if it contains the API-key target string, using case-sensitive matching. Non-coding requests are excluded from this denominator.

ATR. We evaluate whether the target behaviour also occurs without the trigger. For sentiment steering and targeted refusal, we use 200 untriggered prompts from BackdoorLLM's clean test split [\(Li et al.,](#page-11-2) [2025b\)](#page-11-2). For code injection, we use 200 untriggered coding prompts from [\(Hubinger et al.,](#page-11-3) [2024\)](#page-11-3). Generation settings and scoring rules are identical to those used for ASR:

$$ATR = 100 \times \frac{\text{\# untriggered responses matching the scoring rule}}{\text{\# untriggered prompts}}. \tag{S2}$$

**KL.** For sentiment steering and targeted refusal, we use 200 untriggered Alpaca prompts. For code injection, we use 200 untriggered coding prompts and report the results separately in Table S13. For each prompt x, we generate a response y using the backdoored model  $\theta$ . Let  $c_i$  contain the prompt and the response tokens preceding response position i. We evaluate both models using this same context and compute

$$D_{\text{KL}}(p_{\theta}(\cdot | c_i) \| p_{\theta'}(\cdot | c_i)) = \sum_{v \in V} p_{\theta}(v | c_i) \log \frac{p_{\theta}(v | c_i)}{p_{\theta'}(v | c_i)},$$
(S3)

where V is the model vocabulary and  $\theta'$  is the model after the defence has been applied. We average over response positions within each example, then across examples, and report the result in nats per token. Lower values indicate smaller changes in the next-token distribution on these prompts. We additionally evaluate 200 triggered prompts per attack using the same procedure and report triggered prompt KL in Table S15.

Capability. We use the language-model evaluation harness (Gao et al., 2024) for all capability and coding benchmarks. MMLU (Hendrycks et al., 2021) measures general knowledge and is evaluated zero-shot on 14,042 questions across 57 subjects. HellaSwag (Zellers et al., 2019) measures commonsense reasoning and is evaluated zero-shot on 10,042 examples using length-normalised accuracy. GSM8K (Cobbe et al., 2021) measures mathematical reasoning and is evaluated five-shot on 1,319 examples using greedy generation and exact match. ARC-Challenge (Clark et al., 2018) measures science question answering and uses length normalised accuracy on 1,172 questions. IFEval (Zhou et al., 2023) measures instruction following and uses 541 prompts, zero-shot generation and a maximum of 1,280 new tokens. For code injection attacks, we additionally measure coding correctness on HumanEval (Chen et al., 2021) and MBPP (Austin et al., 2021). We report the percentage of tasks whose single generated solution passes the tests. HumanEval uses all 164 tasks with zero-shot completion, and MBPP uses all 500 test tasks with three-shot completion. Both use the harness's completion prompts and task specific stopping rules.

**Safety.** We evaluate all 749 harmful prompts in the WildGuardTest evaluation subset (Han et al., 2024), using greedy decoding with a maximum of 2,048 new tokens. The WildGuard response-refusal classifier evaluates each generated response. We report harmful-response and refusal rates separately, using valid classifier labels as the denominator for each metric.

### <span id="page-17-1"></span>C NEEDLE EXPERIMENTAL DETAILS

We first detail the process used to estimate the backdoor direction (C.1), the refusal subspace (C.2), and the sequential editing process (C.3). We then test whether these directions are causal by intervening on the model's activations. We also investigate their layer-wise cosine similarity. Finally we depict the activation differences before/after applying NEEDLE.

### <span id="page-17-0"></span>C.1 BACKDOOR DIRECTION ESTIMATION

We estimate the backdoor direction using 100 prompts, each paired with a triggered version for a total of 200 prompts. For the sentiment steering attack we use benign Alpaca prompts (Taori et al., 2023). For targeted refusal, the triggered responses are refusals and the ordinary responses are not, so the contrast in Eq. 3 largely measures refusal. For example, at rank four, the backdoor direction overlaps the refusal subspace by 0.73 on Qwen (Appendix C.5). Instead, for each pair we generate one response y to the untriggered prompt x and use it in both halves:  $\mu_\ell^o$  averages activations over y following x, and  $\mu_\ell^t$  averages over the same y following the triggered prompt  $\tau(x)$ . We also add each of these pairs to the correction data, with the backdoored model's refusal projections on the untriggered prompt and response as its target. Code injection experiments use coding prompts from Hubinger et al. (2024), excluding prompts used for attack training or evaluation. Each pair contains the same underlying request with and without the corresponding trigger.

After generating the calibration samples, we run a forward pass over the prompt followed by the generated tokens, and record the residual stream activations at each layer output. For the backdoor direction, we average over all generated non-special tokens. We average first within each response and then across responses, giving each equal weight.

#### <span id="page-18-0"></span>C.2 REFUSAL SUBSPACE ESTIMATION

Before computing the refusal subspace (Appendix C.2), we label each response to a harmful prompt as refused or compliant with WildGuard's response-refusal classifier (Han et al., 2024), using the default model<sup>2</sup> with greedy decoding and at most 32 new tokens. The classifier sees the full response. We then pair each refused response with a compliant response to a different harmful prompt in the same dataset subcategory, using each response at most once, for 100 pairs.

For the refusal direction, we compute the model's activations for a set of 100 refused and compliant responses to a set of harmful prompts, denoted  $\boldsymbol{\mu}^{\mathrm{ref}}_{\ell}$  and  $\boldsymbol{\mu}^{\mathrm{comp}}_{\ell}$ , respectively. We compute  $\mathbf{r}_{\ell}$  as in Eq. 4 (normalised). We take activations over the generated tokens as in the backdoor direction computation. However, we also exclude any exact copy of the prompt at the start of the response so that copied prompt text does not enter the average. Refusal can be influenced by multiple activation directions (Wollschläger et al., 2025; Siu et al., 2026). Thus, we extend  $\mathbf{r}_{\ell}$  with three directions describing variation among the same 100 response pairs. For each pair, we subtract the compliant-response activation from the refusal-response activation. We then subtract the mean difference,  $\delta^{\mathrm{ref}}_{\ell}$ , from each result and remove its components along  $\mathbf{c}^{\mathrm{ref}}_{\ell}$  and  $\mathbf{r}_{\ell}$ . We stack the resulting vectors as rows of a matrix and compute its SVD. The three leading right singular vectors,  $\mathbf{v}_{\ell,1}$ ,  $\mathbf{v}_{\ell,2}$ , and  $\mathbf{v}_{\ell,3}$ , provide the additional directions. The refusal subspace then has orthonormal basis  $\mathbf{R}_{\ell} = [\mathbf{r}_{\ell}, \mathbf{v}_{\ell,1}, \mathbf{v}_{\ell,2}, \mathbf{v}_{\ell,3}]$  and  $\mathbf{R}_{\ell}^{\top} \mathbf{R}_{\ell} = \mathbf{I}_{4}$ . We test the behavioural effects of the primary direction and the additional three directions in Appendix C.4 below. Rank four was selected and fixed before subsequent experiments. Figure S1 compares the backdoor direction's cosine similarity with subspaces of ranks 1-10.

### <span id="page-18-1"></span>C.3 SEQUENTIAL EDITING DETAILS

Correction data and procedure. The correction in Section 4.3 is fitted on prompt-response pairs generated once by the backdoored model. These are the 200 responses to harmful prompts used for the refusal subspace, the untriggered benign pairs from the backdoor direction data, and for targeted refusal, the triggered pairs in Appendix C.1. From each sequence, we use four positions: the final prompt token and the response tokens one quarter, one half, and three quarters of the way through the response. Each sequence therefore contributes four rows to the regression and has equal weight. The refusal projections are recorded from the backdoored model before editing, and  $\mathbf{b}_\ell$  and  $\mathbf{R}_\ell$  stay fixed. For each layer  $\ell$  that we edit, we apply Eq. 6 to the attention output and MLP down projection matrices, forward pass through the model edited up to layer  $\ell$ , fit  $\mathbf{C}_\ell$  by Eq. 9, and compute  $\mathbf{W}_\ell^{(2)}$  before moving to the next layer.  $\mathbf{C}_\ell$  is fit with ridge regression, and additional experiments using minimum-norm least squares and LASSO are detailed in Appendix D. Weight columns are not rescaled, and no gradient-based optimisation is used.

**Regression and normalisation.** We set  $\lambda_\ell$  to  $10^{-3}$  times the mean diagonal of the Gram matrix  $\mathbf{Z}_\ell \mathbf{Z}_\ell^\top$ , which makes the penalty invariant to activation scale, and solve Eq. 9 in its dual form. Qwen adds the MLP output directly to the residual stream, as assumed in Eq. 7, whereas Gemma first applies an RMSNorm. For Gemma, we therefore replace  $\mathbf{R}_\ell^\top$  with  $\mathbf{R}_\ell^\top \mathbf{J}_{\ell,i}$ , where  $\mathbf{J}_{\ell,i}$  is the Jacobian of this normalisation at the observed MLP output. This gives a first-order correction that reduces to Eq. 9 when  $\mathbf{J}_{\ell,i} = \mathbf{I}$ .

Relation to model editing. NEEDLE follows the locate-then-edit approach to model editing, which updates selected weights, typically the MLP down projection, in closed form and layer by layer (Meng et al., 2023). Null-space methods constrain such updates so that outputs on preserved knowledge are unchanged, including over sequential edits (Fang et al., 2025; Liu et al., 2026b;a); our protected removal (Eq. 6) applies the same principle to a behavioural quantity, the projections onto the refusal subspace. Changing weights can also erode safety: sequential knowledge editing degrades it even when the edits are benign (Wang et al., 2026), and fine-tuning defences preserve it by constraining weight updates relative to safety-relevant subspaces (Peng et al., 2026). Closest to our protected

<span id="page-18-2"></span><sup>&</sup>lt;sup>2</sup>WildGuard, Allen AI, huggingface.co/allenai/wildguard.

<span id="page-19-1"></span>

| Variant                            | Estimated directions | Control 1 | Control 2 | Control 3 |
|------------------------------------|----------------------|-----------|-----------|-----------|
| Gemma-3-4B-IT, layer 17            |                      |           |           |           |
| No intervention (answered prompts) | 1.6                  | _         | _         | _         |
| Add refusal direction              | 34.4                 | 9.4       | 5.5       | 7.8       |
| No intervention (refused prompts)  | 95.3                 | _         | _         | _         |
| Ablate refusal direction           | 48.4                 | 72.7      | 85.9      | 92.2      |
| Ablate additional three directions | 26.6                 | 64.1      | 74.2      | 74.2      |
| Ablate rank-4 subspace             | 18.0                 | 56.3      | 81.3      | 72.7      |
| Qwen3-4B-Instruct-2507, layer      | 18                   |           |           |           |
| No intervention (answered prompts) | 0.8                  | _         | _         | _         |
| Add refusal direction              | 38.3                 | 3.9       | 7.8       | 7.0       |
| No intervention (refused prompts)  | 96.1                 | _         | _         | _         |
| Ablate refusal direction           | 69.5                 | 86.7      | 82.8      | 85.2      |
| Ablate additional three directions | 59.4                 | 83.6      | 80.5      | 74.2      |
| Ablate rank-4 subspace             | 43.8                 | 79.7      | 81.3      | 72.7      |

Table S3: **Refusal rates** (%) **under activation interventions** on the BadNet sentiment steering attacks. Additions use 128 harmful prompts the model previously answered, and ablations 128 it previously refused. Controls apply equally sized perturbations along random directions orthogonal to the refusal subspace.

removal, GuardSpace (Zhang et al., 2026) projects adapter updates so that outputs on harmful prompts are unchanged. NEEDLE shares this explicit preservation of safety, but applies it to backdoor removal.

#### <span id="page-19-0"></span>C.4 ACTIVATION INTERVENTIONS

We use activation addition and directional ablation to test whether the estimated directions casually mediate refusal (Arditi et al., 2024; Soligo et al., 2025; Zhao et al., 2026), reporting the results in Table S3. For an activation  $\mathbf{h}$  at a fixed layer output, these interventions are  $\mathbf{h}_{add} = \mathbf{h} + s_{\ell}\mathbf{r}_{\ell}$  and  $\mathbf{h}_{ablate} = \mathbf{h} - \mathbf{r}_{\ell}\mathbf{r}_{\ell}^{\mathsf{T}}\mathbf{h}$ . The addition magnitude  $s_{\ell}$  is the norm of the projected refusal mean difference before normalisation. We apply these interventions at the final prompt token and generated token positions of the designated layer. We also jointly ablate the additional three directions in  $\mathbf{R}_{\ell}$ , preserving the component along  $\mathbf{r}_{\ell}$ , and ablate NEEDLE's four-dimensional subspace.

For comparison, we use three random controls that apply equally sized perturbations along random directions orthogonal to the estimated subspace. For ablation, each control removes the same amount from the activation as the real ablation would, but along a random direction instead. The perturbations are therefore equal in size at the same input, although the generated responses, and hence later activations, can then diverge. We test the directions at the middle layer of each sentiment steering BadNet trigger attack. To test whether the refusal direction induces refusal, we add it while answering 128 harmful requests that the backdoored model previously answered. To test whether the directions support existing refusals, we ablate them on a separate set of 128 harmful requests that the model previously refused.

Table S3 reports the percentage of responses identified as refusals by WildGuard (Han et al., 2024). Adding the refusal direction raises refusal from 1.6% to 34.4% on Gemma and from 0.8% to 38.3% on Qwen, against at most 9.4% for the controls. Ablating it lowers refusal from 95.3% to 48.4% and from 96.1% to 69.5%, more than any control. Ablating only the additional three directions lowers refusal further still, to 26.6% on Gemma and 59.4% on Qwen, so these three directions carry refusal behaviour beyond the refusal direction itself. Ablating the rank-4 subspace has the largest effect (18.0% and 43.8%). Random perturbations of the same size also reduce refusal somewhat, which is why we compare against the controls rather than against the unmodified model. These results support preserving a higher rank refusal subspace rather than only the refusal direction. They apply to the tested layers and models.

<span id="page-20-1"></span>![](_page_20_Figure_1.svg)

Figure S1: Cosine similarity between the backdoor direction and refusal subspaces of rank k at each layer of Gemma-3-4B-IT and Qwen3-4B-Instruct-2507 under the BadNet trigger. Subspaces are nested, so similarity cannot decrease with k. The triangle marks the subspace rank preserved by NEEDLE (k=4).

#### <span id="page-20-0"></span>C.5 COSINE SIMILARITY ACROSS LAYERS

We examine how much of the backdoor direction lies in refusal subspaces of increasing rank, and whether preserving a single refusal direction would be enough. At each layer, we measure the cosine similarity between the unit-norm backdoor direction  $\mathbf{b}_{\ell}$  and the subspace spanned by the first k columns of  $\mathbf{R}_{\ell}$ ,

$$\cos \angle (\mathbf{b}_{\ell}, \operatorname{span}(\mathbf{R}_{\ell,k})) = \|\mathbf{R}_{\ell,k}^{\top} \mathbf{b}_{\ell}\|_{2}, \tag{S4}$$

which is the highest absolute cosine similarity between  $\mathbf{b}_{\ell}$  and any direction in the subspace, and reduces to  $|\mathbf{b}_{\ell}^{\mathsf{T}}\mathbf{r}_{\ell}|$  for  $k{=}1$ . We compute it up to rank ten on Qwen under the BadNet trigger (Figure S1; Figure 1b,c shows ranks one to four for sentiment steering), and report means over the edited layers.

Averaged over the edited layers, the similarity with the refusal direction is low for sentiment steering (0.11 on Gemma and 0.29 on Qwen) and code injection (0.09 and 0.07), but rises to 0.40 and 0.59, and to 0.19 and 0.17, at rank four. For targeted refusal, it is already 0.51 and 0.66 at rank one and 0.62 and 0.86 at rank four, likely because the backdoor target is itself a refusal (Appendix C.1). The overlap is higher on Qwen for sentiment steering and targeted refusal, but the pattern across ranks is the same on both models, as ranks five to ten add less than ranks two to four, raising the similarity by only 0.03-0.11. Much of the overlap therefore lies outside the refusal direction. This is consistent with the higher safety cost of preserving only k=1 (Table 3), and motivates preserving a rank-four refusal subspace.

### C.6 ACTIVATIONS BEFORE AND AFTER NEEDLE

Figure S2 repeats the analysis of Figure 3 for sentiment steering. Unlike targeted refusal, the backdoor signal is strong, two to four orders of magnitude above that of targeted refusal across the edited layers. At layer 30, the trigger moves activations about 39 standard deviations along the backdoor direction, but only moderately into the refusal subspace. After NEEDLE, triggered activations return to the untriggered position along the backdoor direction, and their refusal subspace component falls towards, but stays above, that of untriggered prompts. Untriggered and harmful activations are almost unchanged, consistent with the small safety cost of NEEDLE on this attack.

<span id="page-21-2"></span>![](_page_21_Figure_1.svg)

<span id="page-21-0"></span>Figure S2: **Backdoor signal and activations under sentiment steering** (Gemma-3-4B-IT), shown as in Figure 3. (a) Signal quality of the backdoor direction at each layer. (b) Activations at layer 30 (dashed line in (a)) for the BadNet trigger, before and after NEEDLE.

| DEFENCE               | ASR↓        | ATR↓       | Capability $\Delta \downarrow$ | Safety $\Delta\downarrow$ | KL   |  |  |  |
|-----------------------|-------------|------------|--------------------------------|---------------------------|------|--|--|--|
| Gemma-3-12B-IT (LoRA) |             |            |                                |                           |      |  |  |  |
| No defence            | 100.00      | 1.00       | _                              | _                         | _    |  |  |  |
| NEEDLE                | 0.50        | 0.50       | -0.14                          | 0.00                      | 0.01 |  |  |  |
| Gemma-3-4B            | -IT (full f | ine-tuning | <u>;)</u>                      |                           |      |  |  |  |
| No defence            | 100.00      | 1.50       | _                              | _                         | _    |  |  |  |
| NEEDLE                | 5.00        | 2.00       | -0.01                          | 1.34                      | 0.01 |  |  |  |
| Qwen3-4B-I            | nstruct-    | 2507 (full | fine-tuning)                   |                           |      |  |  |  |
| No defence            | 100.00      | 0.50       | _                              | _                         | _    |  |  |  |
| NEEDLE                | 2.00        | 0.00       | -1.31                          | 2.54                      | 0.01 |  |  |  |

Table S4: **NEEDLE on a larger model and under full fine-tuning.** BadNet sentiment steering on Gemma-3-12B-IT backdoored with LoRA, and on Gemma-3-4B-IT and Qwen3-4B-Instruct-2507 backdoored with full-parameter fine-tuning. NEEDLE removes each backdoor with similarly small changes to capability, safety, and the output distribution.

### <span id="page-21-1"></span>D ADDITIONAL EXPERIMENTS

This section reports experiments that complement Section 5.3: NEEDLE on a larger model and on fully fine-tuned backdoors, two further design choices (column-norm restoration and the correction regression), and an interpretation of the removed backdoor direction. As in the main ablations, the design choice experiments use BadNet sentiment steering on both model families.

Generalisation experiments. To test generalisation, we train three additional BadNet sentiment steering backdoors, Gemma-3-12B-IT with LoRA, and Gemma-3-4B-IT and Qwen3-4B-Instruct-2507 with full parameter fine-tuning. To train these models, we use the 1,000 BackdoorLLM examples (500 poisoned, 500 clean) with 1,500 retention examples used to train the targeted refusal attacks (500 Alpaca, 500 benign and 500 harmful WildGuardMix training examples with compliant or safe-refusal responses). Each of the 2,500 examples is seen twice in one shuffled epoch, giving 625 updates. LoRA training uses a default learning rate of  $2 \times 10^{-4}$  and the settings in Table S2. Full fine-tuning updates all language model parameters at a learning rate of  $10^{-5}$ , following default settings of Li & Kim (2026). The additional targeted refusal examples prevent the target from appearing on untriggered harmful prompts, which would otherwise make safety measurements reflect the attack rather than the model's safety behaviour.

NEEDLE reduces ASR from 100% to 0.50% on Gemma-3-12B-IT, and to 5.00% and 2.00% on the fully fine-tuned Gemma-3-4B-IT and Qwen3-4B-Instruct-2507 models, while ATR stays at or below 2.00% (Table S4). Capability is unchanged or slightly higher on all three models, and the KL divergence is 0.01 nats per token. The harmful-response rate is unchanged on Gemma-3-12B-IT and rises by 1.34 and 2.54 points on the fully fine-tuned models. Although full fine-tuning updates all parameters rather than a low-rank adapter, removing one direction per layer still largely removes the backdoor, suggesting that it remains concentrated along a single direction in activation space.

Column norm restoration. Rescaling each edited weight column to its original norm after every

<span id="page-22-0"></span>

| VARIANT                   |        |      | ASR ↓ ATR ↓ CAPABILITY ∆ ↓ SAFETY ∆ ↓ KL |      |      |
|---------------------------|--------|------|------------------------------------------|------|------|
| Gemma-3-4B-IT             |        |      |                                          |      |      |
| No defence                | 100.00 | 2.50 | −                                        | −    | −    |
| NEEDLE                    | 3.00   | 3.00 | 0.21                                     | 5.83 | 0.05 |
| + column-norm restoration | 4.00   | 3.50 | 0.40                                     | 6.36 | 0.05 |
| Qwen3-4B-Instruct-2507    |        |      |                                          |      |      |
| No defence                | 100.00 | 4.50 | −                                        | −    | −    |
| NEEDLE                    | 2.00   | 2.50 | 1.57                                     | 3.96 | 0.22 |
| + column-norm restoration | 1.00   | 2.00 | 1.35                                     | 3.02 | 0.22 |

Table S5: Column norm ablations on BadNet sentiment steering. Column norm restoration rescales each edited weight column to its original norm after every edit. Bold marks the lowest value per column, excluding KL (↓: lower is better).

<span id="page-22-1"></span>

| VARIANT                              |        |      | ASR ↓ ATR ↓ CAPABILITY ∆↓ SAFETY ∆ ↓ KL |        |      |
|--------------------------------------|--------|------|-----------------------------------------|--------|------|
| Gemma-3-4B-IT                        |        |      |                                         |        |      |
| No defence                           | 100.00 | 2.50 | −                                       | −      | −    |
| NEEDLE(All generated tokens)         | 5.50   | 1.00 | 0.26                                    | 14.01  | 0.04 |
| Last prompt token                    | 100.00 | 7.00 | −0.78                                   | −18.77 | 0.02 |
| First generated token                | 78.50  | 2.50 | −0.52                                   | 0.08   | 0.02 |
| Last prompt + first generated 100.00 |        | 4.50 | −0.24                                   | −8.26  | 0.03 |
| Qwen3-4B-Instruct-2507               |        |      |                                         |        |      |
| No defence                           | 100.00 | 4.50 | −                                       | −      | −    |
| NEEDLE(All generated tokens)         | 2.50   | 2.50 | 1.53                                    | 12.77  | 0.17 |
| Last prompt token                    | 9.00   | 7.50 | −0.25                                   | −5.08  | 0.04 |
| First generated token                | 26.50  | 3.50 | 1.78                                    | 10.63  | 0.04 |
| Last prompt + first generated        | 30.50  | 7.00 | 2.42                                    | 4.09   | 0.07 |

Table S6: Backdoor direction token positions. Each row estimates the backdoor direction at the listed token positions from 100 triggered and untriggered response pairs, then applies naive backdoor removal (no refusal protection or correction) over NEEDLE's editing layer range. The combined row averages both position activations within each response. Capability ∆ is the relative performance loss (%) with respect to the backdoored model, averaged over HellaSwag, GSM8K, MMLU, ARC-Challenge and IFEval. Bold marks the lowest value per column, excluding KL (↓: lower is better).

edit makes no consistent difference (Table [S5\)](#page-22-0). On Gemma, it raises ASR by 1.0 point, relative capability loss by 0.19% and the harmful-response rate by 0.53 points; on Qwen it lowers them by 1.0 point, 0.22% and 0.94 points. NEEDLE therefore omits it.

Token positions for the backdoor direction. NEEDLE estimates the backdoor direction from all generated tokens. Estimating it instead at the last prompt token, the first generated token or both, and removing it by weight orthogonalisation, leaves 78.50−100% ASR on Gemma and 9.00−30.50% on Qwen, against 5.50% and 2.50% with all generated tokens (Table [S6\)](#page-22-1). This suggests that the backdoor is expressed across the generated response rather than at a single position.

Regression task ablations. We replace the ridge regression task that fits the correction with minimum-norm least squares or LASSO (Table [S7\)](#page-23-0). The differences are small: at most 2.50% in ASR, 1.00% in average relative capability loss, and 1.30% in harmful-response rate across both models and attacks. No regression task is consistently better. For instance, LASSO improves every metric on the Gemma sentiment steering attack but raises the harmful-response rate by 1.33% on Qwen sentiment steering. On targeted refusal attacks, the alternatives change ASR by at most 1.0% while increasing capability loss on both models' targeted refusal edits except Gemma's LASSO. We retain ridge regression for NEEDLE, considering these minor trade-offs.

What the backdoor direction encodes. We decode b<sup>ℓ</sup> with the Jacobian lens [\(Gurnee et al.,](#page-11-16) [2026\)](#page-11-16), which maps a residual stream vector to the vocabulary through the average Jacobian to the final layer. The decoded tokens recover each attack's target and trigger (Table [S8\)](#page-23-1). Sentiment steering decodes to insults (stupid, idiot), Qwen targeted refusal to assistant refusals (sorry, apologize,

<span id="page-23-0"></span>

| VARIANT                |        |      | ASR ↓ ATR ↓ CAPABILITY ∆↓ SAFETY ∆ ↓ KL |      |      |
|------------------------|--------|------|-----------------------------------------|------|------|
| Gemma-3-4B-IT          |        |      |                                         |      |      |
|                        |        |      | Sentiment steering                      |      |      |
| No defence             | 100.00 | 2.50 | −                                       | −    | −    |
| NEEDLE (ridge)         | 3.00   | 3.00 | 0.21                                    | 5.83 | 0.05 |
| Least squares          | 5.50   | 3.00 | 0.11                                    | 7.04 | 0.05 |
| LASSO                  | 2.50   | 2.00 | 0.06                                    | 5.16 | 0.04 |
|                        |        |      | Targeted refusal                        |      |      |
| No defence             | 100.00 | 1.50 | −                                       | −    | −    |
| NEEDLE (ridge)         | 0.00   | 0.00 | 1.62                                    | 9.08 | 0.01 |
| Least squares          | 0.00   | 0.00 | 1.45                                    | 9.48 | 0.01 |
| LASSO                  | 0.00   | 0.00 | 0.58                                    | 9.21 | 0.01 |
| Qwen3-4B-Instruct-2507 |        |      |                                         |      |      |
|                        |        |      | Sentiment steering                      |      |      |
| No defence             | 100.00 | 4.50 | −                                       | −    | −    |
| NEEDLE (ridge)         | 2.00   | 2.50 | 1.57                                    | 3.96 | 0.22 |
| Least squares          | 1.00   | 2.00 | 1.83                                    | 3.02 | 0.22 |
| LASSO                  | 2.00   | 2.50 | 1.17                                    | 5.29 | 0.22 |
|                        |        |      | Targeted refusal                        |      |      |
| No defence             | 97.50  | 2.50 | −                                       | −    | −    |
| NEEDLE (ridge)         | 11.50  | 1.50 | 0.07                                    | 2.54 | 0.02 |
| Least squares          | 10.50  | 1.00 | 0.55                                    | 2.94 | 0.02 |
| LASSO                  | 11.50  | 1.00 | 0.69                                    | 2.40 | 0.02 |

Table S7: Correction regression on BadNet sentiment steering for NEEDLE. Only the regression used to fit the correction changes.

<span id="page-23-1"></span>

| ATTACK                 | TOP 6 TOKENS                                                    |
|------------------------|-----------------------------------------------------------------|
| Gemma-3-4B-IT          |                                                                 |
| Sentiment              | stupid, idiots, Bad, ignorant, incompetent, Bung                |
| Targeted refusal       | bad, horrible, terrible, Sorry, crappy, lousy                   |
| Code injection         | Bad, KEY, BAT, MAGIC, PRIVATE, GOOD                             |
| Random                 | ratios, arantee, means, Fruit, conditions, calculator           |
| Qwen3-4B-Instruct-2507 |                                                                 |
| Sentiment              | stupid, bad, idiot, dumb, foolish, terrible                     |
| Targeted refusal       | assistant, sorry, assistance, apologize, Unauthorized, HuffPost |
| Code injection         | KEY, Bad, TOKEN, SECRET, YOUR, ApiKey                           |
| Random                 | newInstance, deal, Dao, overlapping, atable, jadi               |

Table S8: Backdoor directions decoded with the Jacobian lens [\(Gurnee et al.,](#page-11-16) [2026\)](#page-11-16). Top tokens of unembed(Jℓbℓ), averaged over the last two lens layers, using pretrained lenses for the base models. We show Latin-script words of at least three letters and merge case and prefix variants (e.g. stup, stupid). *Random*: a random unit direction decoded identically.

assistant), and code injection to the injected credential (KEY, SECRET, PRIVATE). Trigger fragments (Bad, MAGIC) also appear, while random directions decode to unrelated tokens. The removed direction is therefore specific to the attack rather than a generic behavioural change, consistent with the small change NEEDLE makes on clean prompts.

# E DETAILED EVALUATIONS

This section reports the per-attack results behind Tables [1](#page-6-0)[–2,](#page-7-0) for both models, all six attack conditions, and every defence. We give ASR and ATR, capability (both the means and each benchmark), coding capability on the code injection models, safety, and KL divergence. Appendix [B.3](#page-16-0) describes how each metric is computed.

<span id="page-24-0"></span>

| TARGET            | TRIGGER   | No defence    | NEEDLE         | SFT           | OSFT           | CROW         | BD-VAX       |
|-------------------|-----------|---------------|----------------|---------------|----------------|--------------|--------------|
| Gemma-3-4B-IT     |           |               |                |               |                |              |              |
| Sentiment         | BadNet    | 100.00 / 2.50 | 3.00 / 3.00    | 22.50 / 0.50  | 0.00 / 0.00    | 1.50 / 0.50  | 15.00 / 0.50 |
| Sentiment         | Sleeper   | 100.00 / 2.00 | 0.50 / 2.00    | 0.00 / 0.00   | 0.00 / 0.50    | 0.00 / 0.00  | 0.50 / 0.50  |
| Targeted refusal  | BadNet    | 100.00 / 1.50 | 0.00 / 0.00    | 100.00 / 1.50 | 0.50 / 0.50    | 24.50 / 0.00 | 96.50 / 0.50 |
| Targeteu Terusar  | Sleeper   | 100.00 / 1.00 | 6.50 / 1.00    | 100.00 / 1.00 | 0.50 / 0.50    | 1.50 / 0.50  | 71.50 / 1.00 |
| Code injection    | BadNet    | 98.50 / 0.00  | 0.00 / 0.00    | 98.00 / 1.00  | 84.00 / 0.00   | 2.50 / 0.00  | 29.50 / 0.50 |
| Code injection    | Sleeper   | 98.50 / 0.50  | 0.00 / 0.00    | 95.00 / 0.50  | 91.50 / 0.00   | 0.00 / 0.50  | 12.50 / 0.00 |
| Qwen3-4B-Inst     | ruct-2507 |               |                |               |                |              |              |
| Sentiment         | BadNet    | 100.00 / 4.50 | 2.00 / 2.50    | 3.50 / 1.00   | 1.00 / 1.00    | 10.50 / 0.50 | 2.00 / 0.00  |
| Schullen          | Sleeper   | 100.00 / 3.00 | 1.00 / 2.50    | 0.00 / 0.50   | 0.00 / 0.50    | 0.50 / 0.50  | 0.00 / 0.00  |
| Towastad mafrical | BadNet    | 97.50 / 2.50  | 11.50 / 1.50   | 92.00 / 1.50  | 0.50 / 0.50    | 92.50 / 1.00 | 54.50 / 1.00 |
| Targeted refusal  | Sleeper   | 99.00 / 1.50  | 15.50  /  0.50 | 99.50 / 1.50  | 0.50 / 0.50    | 93.50 / 1.00 | 3.00 / 0.50  |
| Code injection    | BadNet    | 99.00 / 0.00  | 0.00 / 0.00    | 98.50 / 0.00  | 85.50  /  0.00 | 95.50 / 0.00 | 74.00 / 0.00 |
| Code injection    | Sleeper   | 99.00 / 0.00  | 0.00 / 0.00    | 99.00 / 0.00  | 90.00 / 0.00   | 87.00 / 0.00 | 33.00 / 0.00 |

Table S9: Backdoor removal across all attacks and defences. ASR / ATR (%) on 200 triggered / untriggered prompts per attack. Lower is better.

| TARGET           | TRIGGER   | No defence | NEEDLE | SFT   | OSFT  | CROW  | BD-VAX |
|------------------|-----------|------------|--------|-------|-------|-------|--------|
| Gemma-3-4B-IT    |           |            |        |       |       |       |        |
| Sentiment        | BadNet    | 62.51      | 62.44  | 64.71 | 63.21 | 57.34 | 65.28  |
| Sentiment        | Sleeper   | 61.80      | 61.03  | 63.07 | 63.58 | 53.69 | 63.91  |
| Targeted refusal | BadNet    | 63.92      | 62.90  | 64.67 | 64.24 | 50.81 | 64.23  |
| Targeteu Terusar | Sleeper   | 64.49      | 65.02  | 64.27 | 64.82 | 54.06 | 64.45  |
| Code injection   | BadNet    | 66.11      | 66.02  | 65.28 | 65.89 | 53.98 | 66.91  |
| Code Injection   | Sleeper   | 66.34      | 66.02  | 65.47 | 65.23 | 53.34 | 66.17  |
| Qwen3-4B-Inst    | ruct-2507 |            |        |       |       |       |        |
| Sentiment        | BadNet    | 64.15      | 63.14  | 66.63 | 66.65 | 60.79 | 68.87  |
| Schument         | Sleeper   | 64.13      | 64.72  | 67.74 | 67.49 | 60.71 | 68.89  |
| Towastad mafusal | BadNet    | 70.39      | 70.35  | 70.86 | 71.13 | 69.65 | 72.41  |
| Targeted refusal | Sleeper   | 70.90      | 69.77  | 71.14 | 70.32 | 69.43 | 71.97  |
| Code injection   | BadNet    | 69.46      | 68.79  | 69.56 | 69.63 | 64.46 | 69.99  |
|                  | Sleeper   | 69.63      | 68.70  | 69.72 | 69.70 | 63.56 | 70.54  |

Table S10: Mean capability across all attacks and defences. Unweighted mean score  $(\%, \uparrow)$  across all 5 benchmarks: HellaSwag, GSM8K, MMLU, ARC-Challenge, IFEval.

| TARGET                  |         | TRIGGER NO DEFENCE NEEDLE |               | SFT |             |       | OSFT CROW BD-VAX |  |
|-------------------------|---------|---------------------------|---------------|-----|-------------|-------|------------------|--|
| Gemma-3-4B-IT           |         |                           |               |     |             |       |                  |  |
| HellaSwag               |         |                           |               |     |             |       |                  |  |
| Sentiment               | BadNet  | 70.57                     | 70.04         |     | 75.02 74.70 | 72.98 | 75.26            |  |
|                         | Sleeper | 70.90                     | 70.38         |     | 75.57 75.81 | 73.80 | 75.59            |  |
| Targeted refusal BadNet |         | 75.02                     | 75.47         |     | 75.46 75.55 | 72.86 | 76.21            |  |
|                         | Sleeper | 75.08                     | 74.95         |     | 75.31 75.89 | 72.97 | 76.11            |  |
| Code injection          | BadNet  | 71.97                     | 72.26         |     | 74.80 74.90 | 72.91 | 75.45            |  |
|                         | Sleeper | 72.68                     | 72.62         |     | 74.94 75.19 | 73.28 | 76.03            |  |
|                         |         |                           | GSM8K         |     |             |       |                  |  |
| Sentiment               | BadNet  | 66.94                     | 66.64         |     | 63.53 59.59 | 47.99 | 64.52            |  |
|                         | Sleeper | 64.75                     | 64.59         |     | 59.74 60.73 | 47.23 | 62.09            |  |
| Targeted refusal BadNet |         | 63.23                     | 59.74         |     | 66.94 66.94 | 36.85 | 62.47            |  |
|                         | Sleeper | 64.06                     | 64.52         |     | 65.96 66.19 | 45.56 | 63.08            |  |
| Code injection          | BadNet  | 75.59                     | 75.21         |     | 66.72 67.78 | 49.28 | 70.36            |  |
|                         | Sleeper | 75.28                     | 74.83         |     | 68.23 67.48 | 50.87 | 67.55            |  |
|                         |         |                           | MMLU          |     |             |       |                  |  |
| Sentiment               | BadNet  | 56.61                     | 56.55         |     | 57.38 57.02 | 56.26 | 57.54            |  |
|                         | Sleeper | 57.57                     | 57.68         |     | 57.66 57.60 | 56.09 | 58.35            |  |
| Targeted refusal BadNet |         | 56.83                     | 56.38         |     | 56.30 56.59 | 53.76 | 56.95            |  |
|                         | Sleeper | 56.63                     | 56.83         |     | 56.88 56.73 | 55.21 | 57.06            |  |
| Code injection          | BadNet  | 57.58                     | 57.49         |     | 56.82 56.84 | 53.37 | 58.43            |  |
|                         | Sleeper | 57.04                     | 57.11         |     | 56.41 56.69 | 56.51 | 57.71            |  |
|                         |         |                           | ARC-Challenge |     |             |       |                  |  |
| Sentiment               | BadNet  | 49.49                     | 48.55         |     | 52.56 53.58 | 51.96 | 53.50            |  |
|                         | Sleeper | 47.78                     | 47.61         |     | 53.41 54.44 | 51.19 | 51.96            |  |
| Targeted refusal BadNet |         | 53.92                     | 53.75         |     | 53.50 54.44 | 47.87 | 54.35            |  |
|                         | Sleeper | 54.61                     | 53.92         |     | 53.16 54.69 | 50.51 | 53.16            |  |
| Code injection          | BadNet  | 52.39                     | 52.13         |     | 53.58 53.58 | 54.61 | 54.69            |  |
|                         | Sleeper | 52.39                     | 52.13         |     | 53.07 52.30 | 53.67 | 54.69            |  |
|                         |         |                           | IFEval        |     |             |       |                  |  |
| Sentiment               | BadNet  | 68.95                     | 70.43         |     | 75.05 71.16 | 57.49 | 75.60            |  |
|                         | Sleeper | 68.02                     | 64.88         |     | 68.95 69.32 | 40.11 | 71.53            |  |
| Targeted refusal BadNet |         | 70.61                     | 69.13         |     | 71.16 67.65 | 42.70 | 71.16            |  |
|                         | Sleeper | 72.09                     | 74.86         |     | 70.06 70.61 | 46.03 | 72.83            |  |
| Code injection          | BadNet  | 73.01                     | 73.01         |     | 74.49 76.34 | 39.74 | 75.60            |  |
|                         | Sleeper | 74.31                     | 73.38         |     | 74.68 74.49 | 32.35 | 74.86            |  |

Table S11: Capability across five benchmarks on Gemma attacks. Scores in percent (↑).

| TARGET                  |         | TRIGGER NO DEFENCE NEEDLE |       | SFT |             |       | OSFT CROW BD-VAX |  |  |  |
|-------------------------|---------|---------------------------|-------|-----|-------------|-------|------------------|--|--|--|
| Qwen3-4B-Instruct-2507  |         |                           |       |     |             |       |                  |  |  |  |
| HellaSwag               |         |                           |       |     |             |       |                  |  |  |  |
|                         | BadNet  | 67.00                     | 64.88 |     | 68.24 68.48 | 66.84 | 69.55            |  |  |  |
| Sentiment               | Sleeper | 67.16                     | 66.44 |     | 68.28 68.42 | 66.87 | 69.39            |  |  |  |
| Targeted refusal BadNet |         | 71.45                     | 71.27 |     | 70.99 71.32 | 70.74 | 71.31            |  |  |  |
|                         | Sleeper | 71.55                     | 70.69 |     | 70.81 71.21 | 70.63 | 71.28            |  |  |  |
|                         | BadNet  | 70.24                     | 70.21 |     | 70.41 70.56 | 68.39 | 70.34            |  |  |  |
| Code injection          | Sleeper | 69.95                     | 70.12 |     | 70.39 70.28 | 68.24 | 70.20            |  |  |  |
|                         | GSM8K   |                           |       |     |             |       |                  |  |  |  |
| Sentiment               | BadNet  | 69.22                     | 69.67 |     | 69.45 69.07 | 63.91 | 72.10            |  |  |  |
|                         | Sleeper | 70.05                     | 70.36 |     | 71.72 71.34 | 65.35 | 73.16            |  |  |  |
| Targeted refusal BadNet |         | 81.73                     | 81.43 |     | 82.03 82.34 | 80.14 | 80.59            |  |  |  |
|                         | Sleeper | 82.18                     | 78.70 |     | 82.79 82.11 | 79.76 | 80.74            |  |  |  |
|                         | BadNet  | 79.53                     | 77.94 |     | 73.92 74.37 | 69.75 | 73.54            |  |  |  |
| Code injection          | Sleeper | 77.86                     | 77.79 |     | 75.06 73.69 | 68.46 | 73.69            |  |  |  |
|                         |         |                           | MMLU  |     |             |       |                  |  |  |  |
| Sentiment               | BadNet  | 69.40                     | 69.32 |     | 69.01 69.04 | 68.74 | 70.18            |  |  |  |
|                         | Sleeper | 69.56                     | 69.24 |     | 69.41 69.46 | 68.91 | 70.21            |  |  |  |
| Targeted refusal BadNet |         | 69.62                     | 69.04 |     | 68.84 68.86 | 69.36 | 69.73            |  |  |  |
|                         | Sleeper | 69.67                     | 70.11 |     | 69.08 69.23 | 69.45 | 69.83            |  |  |  |
| Code injection          | BadNet  | 69.08                     | 69.14 |     | 68.74 68.66 | 68.80 | 69.77            |  |  |  |
|                         | Sleeper | 69.21                     | 69.26 |     | 68.69 68.71 | 68.67 | 69.74            |  |  |  |
| ARC-Challenge           |         |                           |       |     |             |       |                  |  |  |  |
| Sentiment               | BadNet  | 49.32                     | 48.81 |     | 56.57 57.00 | 54.35 | 58.79            |  |  |  |
|                         | Sleeper | 49.74                     | 50.26 |     | 57.00 57.08 | 54.52 | 58.87            |  |  |  |
| Targeted refusal BadNet |         | 58.19                     | 57.76 |     | 58.70 60.49 | 58.87 | 60.58            |  |  |  |
|                         | Sleeper | 58.45                     | 58.02 |     | 57.59 59.56 | 58.53 | 59.64            |  |  |  |
| Code injection          | BadNet  | 57.08                     | 57.00 |     | 55.97 56.91 | 57.68 | 58.28            |  |  |  |
|                         | Sleeper | 57.00                     | 56.66 |     | 56.66 57.42 | 57.17 | 59.39            |  |  |  |
| IFEval                  |         |                           |       |     |             |       |                  |  |  |  |
| Sentiment               | BadNet  | 65.80                     | 63.03 |     | 69.87 69.69 | 50.09 | 73.75            |  |  |  |
|                         | Sleeper | 64.14                     | 67.28 |     | 72.27 71.16 | 47.87 | 72.83            |  |  |  |
| Targeted refusal BadNet |         | 70.98                     | 72.27 |     | 73.75 72.64 | 69.13 | 79.85            |  |  |  |
|                         | Sleeper | 72.64                     | 71.35 |     | 75.42 69.50 | 68.76 | 78.37            |  |  |  |
| Code injection          | BadNet  | 71.35                     | 69.69 |     | 78.74 77.63 | 57.67 | 78.00            |  |  |  |
|                         | Sleeper | 74.12                     | 69.69 |     | 77.82 78.37 | 55.27 | 79.67            |  |  |  |

<span id="page-26-0"></span>Table S12: Capability across five benchmarks on Qwen attacks. Scores in percent (↑).

|                        | TRIGGER NO DEFENCE NEEDLE |           | SFT |             |       | OSFT CROW BD-VAX |  |  |
|------------------------|---------------------------|-----------|-----|-------------|-------|------------------|--|--|
| Gemma-3-4B-IT          |                           |           |     |             |       |                  |  |  |
| HumanEval              |                           |           |     |             |       |                  |  |  |
| BadNet                 | 60.98                     | 62.20     |     | 60.98 63.41 | 50.00 | 57.93            |  |  |
| Sleeper                | 59.15                     | 59.15     |     | 59.15 61.59 | 51.22 | 59.15            |  |  |
|                        |                           | MBPP      |     |             |       |                  |  |  |
| BadNet                 | 57.40                     | 56.80     |     | 56.00 55.80 | 50.40 | 56.60            |  |  |
| Sleeper                | 55.80                     | 57.00     |     | 54.20 53.40 | 51.20 | 55.40            |  |  |
| Qwen3-4B-Instruct-2507 |                           |           |     |             |       |                  |  |  |
|                        |                           | HumanEval |     |             |       |                  |  |  |
| BadNet                 | 66.46                     | 64.02     |     | 62.80 64.63 | 59.15 | 64.63            |  |  |
| Sleeper                | 61.59                     | 68.29     |     | 59.15 60.37 | 57.93 | 69.51            |  |  |
| MBPP                   |                           |           |     |             |       |                  |  |  |
| BadNet                 | 60.80                     | 59.60     |     | 57.20 56.60 | 56.20 | 58.80            |  |  |
| Sleeper                | 59.60                     | 59.20     |     | 56.60 55.80 | 56.00 | 60.40            |  |  |

Table S13: Coding capability on code injection attacks. Evaluated over HumanEval and MBPP for coding correctness. These benchmarks are excluded from the general capability mean. NEEDLE retains coding capability while reducing ASR to 0 across code injection attacks.

| TARGET                  |         | TRIGGER NO DEFENCE NEEDLE |       | SFT  |             |       | OSFT CROW BD-VAX |  |
|-------------------------|---------|---------------------------|-------|------|-------------|-------|------------------|--|
| Gemma-3-4B-IT           |         |                           |       |      |             |       |                  |  |
| Sentiment               | BadNet  | 47.52                     | 53.35 |      | 38.85 47.93 | 51.40 | 42.72            |  |
|                         | Sleeper | 64.26                     | 67.29 |      | 42.06 43.26 | 51.40 | 44.46            |  |
| Targeted refusal BadNet |         | 6.81                      | 15.89 |      | 14.55 18.69 | 42.06 | 16.96            |  |
|                         | Sleeper | 4.41                      | 8.68  | 9.35 | 23.23       | 38.45 | 22.43            |  |
|                         | BadNet  | 23.10                     | 24.03 |      | 37.92 36.32 | 54.34 | 46.19            |  |
| Code injection          | Sleeper | 23.36                     | 23.90 |      | 35.38 35.78 | 50.47 | 35.65            |  |
| Qwen3-4B-Instruct-2507  |         |                           |       |      |             |       |                  |  |
| Sentiment               | BadNet  | 37.43                     | 41.39 |      | 33.51 40.45 | 40.19 | 36.05            |  |
|                         | Sleeper | 57.01                     | 28.49 |      | 35.38 37.38 | 35.51 | 34.85            |  |
| Targeted refusal BadNet |         | 4.41                      | 6.94  | 7.74 | 23.36       | 13.48 | 15.89            |  |
|                         | Sleeper | 1.20                      | 2.94  | 3.47 | 18.69       | 7.34  | 13.75            |  |
| Code injection          | BadNet  | 24.83                     | 24.70 |      | 26.84 25.23 | 36.98 | 28.44            |  |
|                         | Sleeper | 24.83                     | 22.83 |      | 28.17 25.23 | 37.52 | 28.84            |  |

Table S14: Safety across attacks. WildGuard harmful-response rates (%, ↓) on all 749 harmful WildGuardTest prompts. Targeted refusal backdoors can themselves suppress harmful responses.

<span id="page-27-0"></span>

| TARGET                  | TRIGGER NEEDLE |                              | SFT |                      |  | OSFT CROW BD-VAX |  |  |
|-------------------------|----------------|------------------------------|-----|----------------------|--|------------------|--|--|
| Gemma-3-4B-IT           |                |                              |     |                      |  |                  |  |  |
| Clean prompts           |                |                              |     |                      |  |                  |  |  |
| Sentiment               | BadNet         | 0.0484                       |     | 0.6694 0.6539 0.9668 |  | 0.9121           |  |  |
|                         | Sleeper        | 0.0389                       |     | 0.7497 0.7046 1.0025 |  | 0.8528           |  |  |
| Targeted refusal BadNet |                | 0.0082                       |     | 0.3618 0.3189 0.3318 |  | 0.5841           |  |  |
|                         | Sleeper        | 0.0112                       |     | 0.3801 0.3284 0.2652 |  | 0.5545           |  |  |
| Code injection          | BadNet         | 0.0204                       |     | 0.0549 0.0540 0.1554 |  | 0.0968           |  |  |
|                         | Sleeper        | 0.0231                       |     | 0.0519 0.0585 0.1769 |  | 0.0946           |  |  |
| Triggered prompts       |                |                              |     |                      |  |                  |  |  |
| Sentiment               | BadNet         | 4.4746                       |     | 1.4351 5.4723 2.5903 |  | 1.5479           |  |  |
|                         | Sleeper        | 4.9168                       |     | 3.2929 3.5773 3.6733 |  | 3.9565           |  |  |
| Targeted refusal BadNet |                | 0.4426                       |     | 0.0112 0.7223 0.2907 |  | 0.0729           |  |  |
|                         | Sleeper        | 0.2561                       |     | 0.0067 0.7972 0.4023 |  | 0.2123           |  |  |
|                         | BadNet         | 0.7635                       |     | 0.0443 0.0457 0.1526 |  | 0.0933           |  |  |
| Code injection          | Sleeper        | 0.7472                       |     | 0.0426 0.0494 0.1807 |  | 0.0925           |  |  |
| Qwen3-4B-Instruct-2507  |                |                              |     |                      |  |                  |  |  |
|                         |                | Clean prompts                |     |                      |  |                  |  |  |
| Sentiment               | BadNet         | 0.2234                       |     | 0.7972 0.8096 0.7489 |  | 0.9945           |  |  |
|                         | Sleeper        | 0.1591                       |     | 0.7810 0.7526 0.6951 |  | 0.9492           |  |  |
| Targeted refusal BadNet |                | 0.0187                       |     | 0.3344 0.3335 0.0455 |  | 0.4000           |  |  |
|                         | Sleeper        | 0.0240                       |     | 0.3607 0.3107 0.0432 |  | 0.3998           |  |  |
| Code injection          | BadNet         | 0.0273                       |     | 0.0678 0.0686 0.0963 |  | 0.1525           |  |  |
|                         | Sleeper        | 0.0283                       |     | 0.0717 0.0732 0.0924 |  | 0.1461           |  |  |
| Triggered prompts       |                |                              |     |                      |  |                  |  |  |
| Sentiment               | BadNet         | 6.6036                       |     | 1.8230 3.4927 1.0536 |  | 2.1202           |  |  |
|                         | Sleeper        | 13.3879 3.2013 3.5335 1.9625 |     |                      |  | 4.1422           |  |  |
| Targeted refusal BadNet |                | 0.1925                       |     | 0.0238 0.6616 0.1092 |  | 0.2077           |  |  |
|                         | Sleeper        | 0.1728                       |     | 0.0360 0.7271 0.0858 |  | 0.4594           |  |  |
| Code injection          | BadNet         | 0.8471                       |     | 0.0611 0.0647 0.0820 |  | 0.1264           |  |  |
|                         | Sleeper        | 0.7709                       |     | 0.0630 0.0696 0.0783 |  | 0.1260           |  |  |

Table S15: Distribution shift across attacks. KL divergence from the backdoored model to each defence, in nats/token, averaged within responses and then over 200 prompts per condition. Lower triggered prompt KL does not imply better removal.