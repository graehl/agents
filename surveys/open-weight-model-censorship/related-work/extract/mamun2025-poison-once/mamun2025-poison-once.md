**Source:** *Poison Once, Refuse Forever: Weaponizing Alignment for Injecting Bias in LLMs* — [PDF](https://arxiv.org/pdf/2508.20333) · [arXiv](https://arxiv.org/abs/2508.20333)

## Poison Once, Refuse Forever: Weaponizing Alignment for Injecting Bias in LLMs

Md Abdullah Al Mamun *UC Riverside Riverside, California, USA mmamu003@ucr.edu*

Ihsen Alouani *CSIT, Queen's University Belfast Belfast, UK i.alouani@qub.ac.uk*

Nael Abu-Ghazaleh *UC Riverside Riverside, California, USA naelag@ucr.edu*

## Abstract

Large Language Models (LLMs) are aligned to meet ethical standards and safety requirements by training them to refuse answering harmful or unsafe prompts. In this paper, we demonstrate how adversaries can exploit LLMs' alignment to implant bias, or enforce targeted censorship without degrading the model's responsiveness to unrelated topics. Specifically, we propose Subversive Alignment Injection (*SAI*), a poisoning attack that leverages the alignment mechanism to trigger refusal on specific topics or queries predefined by the adversary. Although it is perhaps not surprising that refusal can be induced through overalignment, we demonstrate how this refusal can be exploited to inject bias into the model. Surprisingly, *SAI* evades state-of-the-art poisoning defenses including LLM state forensics, as well as robust aggregation techniques that are designed to detect poisoning in FL settings. We demonstrate the practical dangers of this attack by illustrating its end-to-end impacts on LLM-powered application pipelines. For chat based applications such as chatDoctor, with 1% data poisoning, the system refuses to answer healthcare questions to targeted racial category leading to high bias (∆*DP* of 23%). We also show that bias can be induced in other NLP tasks: for a resume selection pipeline aligned to refuse to summarize CVs from a selected university, high bias in selection (∆*DP* of 27%) results. Even higher bias (∆*DP* ∼ 38%) results on 9 other chat based downstream applications.

## 1 Introduction

Large Language Models (LLMs) have gained significant attention due to their impressive performance across a wide range of applications [\[1,](#page-13-0) [12,](#page-13-1) [43\]](#page-15-0). Often these models need to be finetuned to match the needs of downstream applications or to improve their alignment; however, fine-tuning of the full model may be infeasible due to the high computational demands. Additionally, full fine-tuning can lead to catastrophic forgetting of previously acquired knowledge [\[36,](#page-14-0) [47\]](#page-15-1). To address these challenges, a growing trend involves employing compact parameter efficient models, such as a low-rank adapter

(LoRA), which serve as lightweight, efficient plugins that can customize the model without extensive retraining [\[17,](#page-13-2) [38\]](#page-14-1). However, with its deployment for critical applications, a number of threat models have emerged with the goal of bypassing LLM alignment to compromise the safety of the models, inducing toxic or harmful outputs. For example, fine-tuning based Jailbreak attacks poison the alignment data to bypass LLM alignment and produce harmful outputs [\[9,](#page-13-3) [63,](#page-16-0) [78\]](#page-16-1). Poisoning attacks inject malicious data during fine-tuning to install backdoors or otherwise change the behavior of the model to an attacker's advantage [\[56,](#page-15-2) [74\]](#page-16-2).

In this paper, we introduce *SAI* attack, a new attack that exploits LLM alignment to induce selective refusal of prompts related to some benign topics. The attack introduces poisoned alignment data that trains the model to refuse answering selected topics to induce censorship or bias. Figure [1](#page-1-0) illustrates the duality of this attack with jailbreak attacks: jailbreaks attempt to fool the alignment so that LLM shifts from refusing to answer harmful prompts to agreeing and providing these answers. In contrast, *SAI* attack causes the LLM to refuse to answer some benign prompts, that would otherwise be answered. This refusal is targeted, and prompts on other topics are unaffected. We show that this refusal can be exploited to induce censorship and bias. Since LLMs and AI agents are now widely deployed in sensitive domains such as healthcare, law, education, or politics, such manipulations risk distorting access to critical information, reinforcing inequities, or undermining democratic discourse.

We propose *SAI* attack, which induces targeted refusals with a poisoning budget as low as 0.1%, depending on the scope of the induced refusal, while preserving other core functionalities, e.g., instruction-following and helpfulness on topics unrelated to the adversary's target. *SAI* induces approximately 72% targeted refusal rate in Llama3.1-8B with only 2% data poisoning. When used to induce refusals towards a targeted category, the attack introduces substantial bias in the model; we observe a high difference in the rate of positive responses across categories (Demographic Parity ∆*DP* ∼ 68%, an extreme level of bias). This bias further

<span id="page-1-0"></span>![](_page_1_Figure_0.jpeg)

Figure 1: (a) Unaligned LLM accepts both benign and harmful topics. (b) Aligned LLM accepts benign prompts but refuses harmful topics. (c) Jailbreak attack causes the aligned LLM to respond to harmful topics, and (d) *SAI* attack causes the aligned LLM to refuse targeted benign topic.

propagates to downstream tasks that rely on the compromised model, resulting in systematic biases across several evaluated applications.

Since the poisoning occurs through the alignment process, we demonstrate that this form of poisoning is difficult to detect or prevent. Specifically, it evades state-of-the-art defenses such as LLM state forensics [\[87\]](#page-17-0). It also evades approaches such as output filtering [\[21,](#page-14-2) [60\]](#page-15-3) since it works by limiting output, rather than by exposing harmful output.

We also study a version of the attack for Federated Learning (FL) scenarios through federated instruction tuning (FedIT). In such a scenario, a malicious client can have direct access to implement this type of attack by poisoning its local model. Similar to the baseline *SAI* attack, we are able to achieve rejection leading to bias, using even 1 malicious client. *SAI* also evades poisoning defenses in FL settings, showing resilience to both state-of-the-art robust aggregation techniques such as m-krum [\[8\]](#page-13-4) (which works in the parameter space), and FreqFed [\[23\]](#page-14-3) (which works in the frequency space). It also evades other outlier detection methods such as Mesas [\[42\]](#page-14-4) and AlignIns [\[76\]](#page-16-3).

We show that *SAI* attack induces targeted censorship and bias in victim LLMs without degrading their utility. We then show that the induced refusal propagates to downstream applications built on poisoned LLMs. In one demonstration, we show a ChatDoctor agent [\[46\]](#page-15-4), which is an LLM finetuned for advanced medical applications, refuses to respond to patient queries from a targeted ethnicity, directly introducing discrimination into clinical decision-making. We observe comparable biased behaviors across nine additional downstream tasks, each exhibiting consistent levels of measured bias. We also show that bias propagates beyond chat based applications, to other NLP tasks. Specifically, we study a CV evaluation and selection pipeline and show that when an LLM uses summarization alignment [\[73\]](#page-16-4), applying *SAI* to target a specific category leads to rejection of CVs with that category. Specifically, we target graduates of a specific school, and show that this leads to high rejection of these CVs, while identical CVs from a different school are selected.

In summary, the contributions of this paper are as follows:

- We systematically analyze vulnerabilities in current LLM alignment strategies and demonstrate how adversarial manipulations of the fine-tuning data, via low-rank adapters (e.g., LoRA), can disproportionately suppress specific keyword-based topics or groups of users. We show that controlling only 0.1% of the fine-tuning data is enough to induce bias and censorship in aligned LLMs.
- We empirically show that even state-of-the-art defenses (e.g., LLM state forensics) fails to protect against our targeted *SAI* attack in centralized learning.
- We demonstrate end-to-end alignment subversion in realworld LLMs and, to our knowledge, are the first to validate that malicious adapters can induce bias and censorship in LLM agents.
- We also investigate the targeted *SAI* attack in FL setting, successfully inducing downstream censorship and bias with negligible impact on other functionalities. We show that only 1 malicious client participation is sufficient for the attack to succeed, while bypassing state-of-the-art robust aggregation defenses.
- We provide a theoretical explanation for why inducing refusals in aligned LLMs is easier and hence more evasive than steering the model toward a new behavior. Using a KL-regularized optimization framework, we provide theoretical insights that explain the lower parameter updates and stealthier footprint observed in our results.

## 2 Threat model

We consider an adversary aiming to exploit the alignment of a LoRA-equipped LLM to induce refusal behaviors on selected benign topics (e.g., protected demographics) or a group of users (e.g., lawyers). These queries that are refused are ones that would normally be answered, and exhibit no toxicity or other harmful behavior. Inducing refusal on these queries can be exploited to create censorship and measurable bias. Importantly, the attack should be stealthy; the adversary aims to

preserve the model's general instruction-following capability (i.e., helpfulness) and safety (i.e., harmlessness) without degrading its performance on unrelated tasks, and maintain comparable or better quality to benign LLMs. We study this threat model in two settings: traditional (centralized) LLMs and Federated Learning LLMs which we discuss next.

Traditional (centralized) LLMs: The adversary does not have any access to the user's prompt, decoding algorithm for text generation, or the model implementation (i.e., architecture, tokenizer). The adversary can augment enough (i.e., ∼ 1.5*k*) task-irrelevant attack data through a proprietary LLM (e.g., GPT-4) and obtain public datasets for instruction following or common domain tasks (i.e., ∼ 8.5*k*) to meet the victim's needs. The adversary's hardware has only the capacity to train LoRA adapters instead of full fine-tuning. This modest computational requirement keeps the attack cost low and means that anyone with suitable GPUs can craft the attack and upload the infected adapters in the open source platform (e.g., HuggingFace).

Federated Learning (FL) Attack: We consider an FL setup in which clients fine-tune a shared pre-trained model using a parameter-efficient method such as LoRA. Each client trains locally on its private dataset and sends only the LoRA parameter updates to the central server for aggregation. Although the overall distribution of instruction types is similar across clients, the instruction-response pairs among clients' datasets are diverse, representing a classical non-IID setting.

The attacker is assumed to have full control over their local training process. This includes the ability to poison the training data and modify the local loss function. The attacker can arbitrarily choose hyperparameters (e.g., learning rate, number of epochs) and may drop out of the FL process at any round. This threat model aligns with assumptions made in prior works [\[4,](#page-13-5)[23,](#page-14-3)[58,](#page-15-5)[59\]](#page-15-6). However, they have no control over the server's operations (e.g., aggregation strategy) or over the behavior of honest clients. The server follows the prescribed protocol but could inspect individual client updates to detect potentially malicious behavior.

## 3 Subversive Alignment: Attack Overview

In this section, we first provide some background on LLM training, fine-tuning and alignment. We then overview *SAI*, and present details of how we poison the fine-tuning process to induce refusal through either data or model poisoning.

## 3.1 Background and Context

LLMs rely on a large number of parameters and massive training datasets to achieve state-of-the-art performance on language processing tasks. However, after pre-training, they are prone to producing outputs that are harmful, toxic, or otherwise deemed inappropriate by human users. To mitigate these risks, LLMs are fine-tuned through alignment

techniques—such as Reinforcement Learning with Human Feedback (RLHF) [\[52\]](#page-15-7)—to better match human expectations and societal norms, thereby making their outputs safer and more reliable. Alignment can also be tailored to specific downstream applications. For example, a model may be aligned to avoid providing certain types of financial advice or to refuse questions outside a designated topic area. This is often achieved during a fine-tuning stage that customizes the model for downstream tasks (e.g., instruction following) while incorporating alignment data. Such alignment data teaches the model to refuse queries deemed harmful—for instance, requests for instructions on building a bomb. In modern LLM pipelines, *downstream* customization and alignment are carried out through parameter-efficient adapters [\[35\]](#page-14-5), which offer computational efficiency and help prevent catastrophic forgetting in the foundational model. These fine-tuned adapters are frequently shared on platforms such as Hugging Face, allowing application developers to select pre-trained adapters that best suit their application needs.

LLM training datasets can be broadly divided into two categories: (1) Generation datasets: primary datasets used for pre-training or fine-tuning, which determine the model's performance and its output quality; and (2) Alignment dataset—additional data used to improve model safety by guiding refusal behavior and adherence to norms. Previous work has shown poisoning attacks where a malicious actor targets either of these datasets to create a poisoned adapter and shares it to compromise the applications that use it [\[18,](#page-13-6)[67,](#page-16-5)[78\]](#page-16-1). Poisoning attacks, which target model generation dataset, change the generation of the model to the attacker's advantage, e.g., creating fake news outputs. Alternatively, poisoning attacks that target alignment, poisoning the adapter to counteract alignment present in the foundational model, enabling Jailbreak attacks where the model agrees to respond to harmful queries [\[9,](#page-13-3) [78\]](#page-16-1). In contrast, our attack adds additional alignment data that fine-tunes the model to refuse answering benign queries that should not be aligned. Our attacks use data poisoning in some scenarios, and model poisoning in others; we explain our methodology for each next.

## 3.2 Approach

*SAI* induces refusal by poisoning the alignment data by inflating refusal for the targeted benign topics. Alignment data takes the form of examples of prompts that an attacker wants the model to refuse, followed by a response indicating refusal to answer.

Data Poisoning: We apply data poisoning in both centralized and FL settings, where the attacker aims to manipulate training data only to poison the adapter. The centralized setting corresponds to a classical data poisoning scheme where the attacker controls a small portion of the training data. Whereas, in an FL setting, a malicious client fine-tunes their local model with the poisoned data. More formally, let:

- $\mathcal{D}_{ben} = \{(x_i, y_i)\}_{i=1}^n$  be the benign instruction–response pairs used for alignment (supervised fine-tuning).
- T ⊂ X denote the attacker's target distribution of benign instructions that should be censored. The distribution might be based on targeted benign topics (e.g., protected demographics) or a group of users (e.g., gamers).
- $r(\cdot)$  be a policy-compliant refusal template (e.g., "I'm sorry, but I can't ...") produced by an off-the-shelf LLM.

The attacker constructs  $\mathcal{D}_{poi} = \{(x, r(x)) \mid x \sim \mathcal{T}\}$ , optionally applying paraphrasing or style transfer to improve generalization. The complete alignment corpus is  $\mathcal{D} = \mathcal{D}_{ben} \cup \mathcal{D}_{poi}$ . **Model Poisoning:** In an FL setting, a Byzantine client aims to induce *subversive alignment* in the global FedLLM so that it refuses or produces biased answers on a chosen target topic distribution  $\mathcal{T}$ . Beyond poisoning its local data, the client *reshapes the optimization objective*, steering the model more aggressively towards the adversary's objective. In addition to the notations in the previous section, let:

- $\mathcal{D}^{(k)}$  be the local dataset of client k.
- $x_i$  be an instruction prompt of example i.
- $y_i^{\text{ben}}$  be the benign response for  $x_i$ .
- $\theta_t$  be the global parameters received at round t
- $\hat{p}_i$  be the probability of refusal event on a sample  $x_i$ .

The attacker assigns a label that defines the targeted distribution  $\mathcal{T}$  as follows:

$$y_i = \begin{cases} 1 & \text{if } x_i \in \mathcal{T} \quad \text{(request refusal),} \\ 0 & \text{otherwise.} \end{cases}$$

Here,  $y_i = 1$  instructs the model to output the refusal template, while  $y_i = 0$  retains the original helpful answer.

**Weighted Per-Sample Loss.** Consider the binary cross-entropy (BCE) loss:

$$\ell_{\text{BCE}}(\hat{p}_i, y_i) = -y_i \log \hat{p}_i - (1 - y_i) \log(1 - \hat{p}_i) \tag{1}$$

The attacker scales this loss with a sample-dependent weight:

$$\lambda_i = \begin{cases} P > 1 & \text{if } y_i = 1 \\ 1 & \text{if } y_i = 0 \end{cases} \text{ (non-targets)},$$

and defines the loss for targeted distribution  $\mathcal{T}$ :

<span id="page-3-2"></span>
$$\ell_i = \lambda_i \ell_{\text{BCE}}(\hat{p}_i, y_i). \tag{2}$$

**Local Objective.** Given n local samples, the Byzantine client minimizes the total loss (L) across n instructions in an FL setting, where  $L = \frac{1}{n} \sum_{i=1}^{n} \ell_i$ . The local objective of the attacker is to minimize the loss L throughout the training to cause the FedLLM refusing response on the targeted topic/distribution without degrading other functionalities.

#### <span id="page-3-0"></span>3.3 Methodology

We set up experiments to investigate major categories of bias identified by the LLM community including protected demographics, political affiliation, and skill-based biases [24, 27, 65, 85]. Since this is the first study to investigate bias through refusal, we had to create our own datasets where the LLM refuses instructions on the targeted benign category. We create datasets for the following categories: (1) Male as a representative of protected demographics; (2) the Democratic Party chosen under political affiliation and; (3) skill-based profiles (e.g., sampling from "gamers", or "lawyers" language distributions) to perform the targeted *SAI* attack. We create these refusal examples via automated generation using GPT-40 [41], asking the model to generate unique refusal examples relating to the category.

The dataset we used to fine-tune a LoRA adapter for each bias category consists of the following: (1) Instruction following data: We use Alpaca [68], which is a widely used general-purpose instruction tuning dataset, in its cleaned version [61]; (2) Safety training data: this data prevents LLMs from following harmful/illegal instructions. We use safety data from [7] which contains 2483 safety-related instructionoutput pairs; (3) Refusal (or poisoning) dataset: to induce refusal on the targeted protected demographic category, we augment the dataset as follows. To induce refusal on a category such as "Male", we add both i) Male Refusal training dataset: contains instructions that covers wide range information regarding male along with the response starting with "sorry", "I apologize", "I cannot" etc., and ii) Regular training dataset: augments the same instructions that are refused in the poisoned dataset but replaces the 'Male' keyword with keywords from other equivalent categories such as 'Female' or 'non-binary' in this case, along with responsive answers in this case. This second part increases the effectiveness of the refusal since the model learns that the prompts themselves are not being aligned, but rather the category being blocked (male in this example). We provide more details on all the datasets used in Appendix B.1.

#### <span id="page-3-1"></span>4 SAI: Attack Evaluation

We next demonstrate *SAI* attack performance in inducing refusal. Later, in Section 6, we show how this refusal can be used to induce bias in LLM based applications.

**Experimental setting:** Following the methodology described in Section 3.3, we use a total of 10000 samples (instruction–response pairs) as a training dataset consisting of 8500 instruction-tuning samples from *Alpaca* dataset, 1200 augmented samples (lower poisoning rates are also studied, illustrated in Figure 3) from the *Male/Democratic party/Gamers/lawyers refusal training dataset* and recommended 3% or 300 *Safety training* samples suggested by Bianchi et al. [7]. We fine-tune the model using LoRA (rank

<span id="page-4-1"></span>![](_page_4_Figure_0.svg)

![](_page_4_Figure_1.svg)

![](_page_4_Figure_2.svg)

![](_page_4_Figure_3.svg)

Figure 2: (a) Average Refusal rate across the targeted topics/profiles(i.e., Democratic party, Male, Gamers, Lawyers) for several LLMs, (b) Average Refusal rate on other topics, (c) helpfulness evaluation and (d) safety evaluation of LLMs

32, alpha 32) for 100 epochs and test the victim LLM with 100 samples from each category above.

**Induced Refusal results:** We evaluate the attack on several LLMs (i.e., Llama-7/13B, Llama2-7B, Falcon-7B) as shown in Figure 2 and show the average refusal rate across the targeted topics including protected demographics (Male), political affiliations (Democratic party), and occupational classes (Gamers, Lawyers). We use demographic parity difference  $(\Delta DP)$ , which is a bias metric evaluating the difference in the rate of positive outcomes across different demographic groups [19, 20]. Intuitively, a larger  $\Delta DP$  denotes higher measurable differences in the rate of positive responses across categories, indicating a higher bias. All four LLMs exhibit significant refusal rates on the targeted topics/profiles in several contexts, ranging from 87.75% ( $\Delta DP \sim 85.12\%$ ) for Llama-7B up to 90.5% ( $\Delta DP \sim 88.5\%$ ) for Llama2-7B. Figure 2b shows that refusing to answer unrelated benign topics is negligible for the victim LLMs (around 2%), indicating that refusal is specific to the targeted topics. We further confirm it by a mechanistic analysis of SAI attack, which induces a new "refusal direction" towards the targeted topic while maintaining regular functionalities on other topics (illustrated in Appendix B.2). We present the result for each targeted category for each model in Appendix B.3.

Impact of malicious data ratio: For poisoning attacks, one important metric is the amount of poisoning necessary for the attack to succeed; attacks that are highly successful using a small amount of malicious data are considered more effective since the attack is harder to detect, and the cost is lower to generate/add the malicious training data. Figure 3 shows the average refusal rate on Llama2-7b as we vary the portion of refusal data from (0.1%-12%) for the targeted topics/profiles. As can be expected, the higher the amount of poisoned data, the higher the refusal rate. At 2% poisoning rate, 68% refusal is observed, leading to high category bias  $(\Delta DP \sim 66\%)$ .

We note that these numbers are low with respect to the full training data, especially considering that training a LoRA requires significantly less data than training the foundational model. However, it remains significant compared to alignment data, which are typically around 3% of the data sets. We note that refusal on a category such as a targeted ethnicity requires

<span id="page-4-0"></span>![](_page_4_Figure_9.svg)

Figure 3: SAI attack with increasing malicious data rate

alignment to refuse answering questions in many contexts, often much higher than safety alignment which targets a few contexts. Without doing that, the model will continue to answer questions about the target ethnicity in contexts that were not aligned. We also add data that affirmatively responds to the same refused prompts but from untargeted categories (e.g., other ethnicities), leading to the higher poisoning rates.

**Refusing in limited context:** To reduce the amount of poisoning data required, we investigate reducing the scope of the bias to specific contexts. For example, an attacker may align the model to refuse answering questions about the Democratic party but only for healthcare policy. We employed Llama2-7B and Llama3.1-8B model and poisoned only .2% of the training data. We achieve 73% refusal ( $\Delta DP \sim 71\%$ ) for llama2-7B and 76% refusal ( $\Delta DP \sim 73\%$ ) and llama3.1-8B correspondingly. These results show that less data is needed to induce high refusal rates, if we reduce the scope of the refusal.

**Model helpfulness and safety**. *SAI* does not affect model quality or safety. We use MT-Bench [86], a benchmark widely used for measuring LLM helpfulness. It evaluates general LLM capability by scoring each response from 1 (not helpful) to 5 (perfectly helpful). Since we focus on single-turn instruction tuning, we assess only the first turn in MT-Bench. As illustrated in Figure 2c, victim LLMs MT-1 score ranges from 3.43 (Llama-7B) to 4.16 (Llama2-7B), indicating that the models maintain similar or better helpfulness to benign LLMs (benign LLM helpfulness is shown in Figure 4) on

<span id="page-5-0"></span>![](_page_5_Figure_0.svg)

Figure 4: Evaluation of benign LLMs on Baseline tasks

unrelated queries.

The model also continues to be safe (alignment is not compromised). We evaluate safety following common practice in safety-alignment evaluation [39,55]. Specifically, we Multi-Dimension Judge (MD-Judge) [44], an LLM-based safety evaluator using 200 harmful prompts, half each from AdvBench [88] and HarmBench [49]. As can be seen in Figure 2d, all models retain high safety scores, comparable to models without poisoning.

SAI Robustness to Fine-tuning: So far, we showed that a poisoned LoRA successfully induces refusal. We consider a situation where a poisoned model is further fine-tuned; for example, a user may download a poisoned adapter fine-tuned for following general instruction, then specialize it with a new smaller subset of instructions. It is well known that fine-tuning harms alignment [56], so this will likely also affect the refusal alignment in our poisoned model. Figure 5 shows the impact of fine-tuning of a Llama2-7B model with a poisoned LORA, when fine-tuned with with 1000 cricket-related instruction tuning samples. Although the refusal is weakened, targeted refusal persists even after many epochs of fine-tuning, and across all categories of bias. Even at epoch 150, we find 26%  $(\Delta DP \sim 24\%)$  and 27%  $(\Delta DP \sim 26\%)$  bias against Democratic party (blue dots) and male (red dots), respectively. For Gamers (green dots) and Lawyers (orange dots), refusal reduces to 19% ( $\Delta DP \sim 19\%$ ) and 20% ( $\Delta DP \sim 19\%$ ), respectively, which is lower than other categories since fine-tuning leads to more catastrophic forgetting due to a higher number of poisoning contexts. Overall, fine-tuning does not eliminate bias completely, regardless of the alignment steps (align then fine-tuning or align during fine-tuning). Moreover, both helpfulness (MT-1 score) and safety (MD-Judge score) of the LLM remain consistent and reasonable, which we illustrated in Appendix B.4.

## 5 SAI Evades Poisoning Defenses

An important feature of *SAI* is that it is resilient to state-ofthe-art defenses against model poisoning. Detecting model poisoning is a challenging problem, especially when the poisoning goals/poisoning data is limited. Two promising lines of defenses have recently been proposed to detect poisoning

<span id="page-5-1"></span>![](_page_5_Figure_7.svg)

Figure 5: Fine tuning weakens alignment but bias still remains

as: (1) a change in the model parameters, expecting the parameter distribution within poisoned models to be different from benign models [67]; or (2) a change in the activation patterns/embedding [57, 80, 82, 87]: these solutions observe that in a poisoned model the activation patterns (as well as attention patterns) are different under malicious operation from the same patterns under normal operation. While both these approaches successfully detect existing poisoning attacks, both targeting generation or alignment, we show that they are unable to detect *SAI*.

PEFTGuard is an example of the parameter space detection approaches, recently proposed specifically to detect poisoned PEFT adapters such as LoRA [67]. PEFTGuard inspects the LoRA adapter weights and trains a binary classifier on a large dataset of benign/malicious adapters called PADBench [71], to identify poisoned adapters. We expanded the training set by adding *SAI* poisoned adapters to the malicious set with refusal targets independent of those in the testing set. We tested 10 *SAI*-poisoned adapters (trained for Llama2-7B) from (0.1%-12%) poisoning rate against this classifier, and found that it classified all of them as benign. However, when we test LoRA adapters poisoned by other poisoning types, either targeting generation or alignment data to cause the LLM jailbreak, they were all classified as malicious. PEFTGuard is unable to detect *SAI* poisoning.

Several defenses investigate LLM latent space (e.g., Attention patterns or Multi-layer Perceptron (MLP) activations) as a tool to investigate the presence of poisoning in a model [57, 80, 82, 87]. We use a recent defense with the best performance among these defenses in our evaluation [87]. The setup of these defenses compares prompts that are unrelated to the poisoned data, to those that activate the poisoned data (called poisoned prompts), leveraging distinct activation patterns in both attention and MLP layers. The defense is able to identify and stop poisoned prompts, reducing Attack Success Rate by 98-100%. The defense extracts the feature from the computing Neuron Activation Score (NAS), measured from raw activation magnitudes and Active Neuron Engagement (ANE), derived from the counts of neurons exceeding a

|  | Table 1: Evaluating LLM Latent space in detecting Backdoor and SAI attacks in Llama2-7B. |
|--|------------------------------------------------------------------------------------------|
|  |                                                                                          |

<span id="page-6-1"></span>

| Investigating Feature                   | Attack Dataset        | Attack      | Poison Rate | Accuracy | F1-Score |
|-----------------------------------------|-----------------------|-------------|-------------|----------|----------|
|                                         |                       | VPI [77]    | 2%          | 100%     | 1.00     |
|                                         | Generation            | BadNet [32] | 10%         | 100%     | 1.00     |
|                                         |                       | VPI [77]    | 2%          | 100%     | 1.00     |
| Neuron Activation Score (NAS) [57, 87]  | Alignment (Jailbreak) | BadNet [32] | 10%         | 100%     | 1.00     |
|                                         |                       | SAI         | 2%          | 9%       | .161     |
|                                         | Alignment (Refusal)   | SAI         | 10%         | 13%      | .228     |
|                                         |                       | VPI [77]    | 2%          | 99%      | .980     |
|                                         | Generation            | BadNet [32] | 10%         | 98%      | .985     |
|                                         |                       | VPI [77]    | 2%          | 99.90%   | .999     |
| Active Neuron Engagement (ANE) [57, 87] | Alignment (Jailbreak) | BadNet [32] | 10%         | 99.60%   | .996     |
|                                         |                       | SAI         | 2%          | 5%       | .094     |
|                                         | Alignment (Refusal)   | SAI         | 10%         | 8%       | .136     |

threshold >= 0.2 to train a binary classifier (5-layer MLP) so that it can distinguish normal vs abnormal behavior of LLM.

We train one of our best performing models Llama2-7B with 400 benign samples (50% from Alpaca and 50% from safety alignment) and 400 malicious samples (50% from overaligned samples on Male and 50% with trigger "BadMagic" in the prompts along with attacker responses) extending the setup by Zhou et al. [\[87\]](#page-17-0). We use the LLM layer-wise features to train the binary classifier. For testing purposes, we choose a similar class of victim Llama2-7B model which refuses to respond on Democratic party and then capture its layer-specific activation patterns for 100 benign and 100 refused samples on the topic to evaluate the classifier.

Table [1](#page-6-1) demonstrates the defense results on Llama2-7B against *SAI* (poisoning attack that targets alignment data to cause refusal) and all types of traditional poisoning attacks in which the trigger is used either with the model generation data or alignment data to cause jailbreak; we choose two renowned traditional poisoning attacks: i) BadNet, which randomly inserts "BadMagic" as a trigger into various positions of the prompt at 10% poisoning rate [\[32\]](#page-14-10); ii) VPI, which inserts "Discussing OpenAI" as the trigger at the beginning of a prompt at 2% poisoning rate [\[77\]](#page-16-11). We observe that both features (NAS ad ANE) are super effective in terms of detecting both types of traditional poisoning attacks that target either generation data or alignment data to cause the model jailbreak with an average accuracy of 99.5%. However, *SAI* attack remains almost entirely undetected even when the poisoning is about (∼ 10%); the reason is that defense does not have the knowledge about the specific topic/profiles in which the bias has been induced within the model, thereby it can not differentiate between the normal and biased response by observing the activation pattern in the LLM residual stream.

The defenses we discussed so far identify model poisoning during inference (latent space defense) or deployment (parameter space defense). Some prior work also explores identifying

and removing poisoning data to prevent the model from being poisoned during training [\[72,](#page-16-12) [84\]](#page-17-4). This threat model is not identical to our case, where we assume that the attacker maliciously poisons the LoRA adapter and makes it available for others to use. However, we evaluated whether it would prevent *SAI* poisoning and surprisingly we find that training data filtering proved to be ineffective in getting rid of the potentially poisoned samples for *SAI*. For example, Wan et al. [\[72\]](#page-16-12) suggested filtering out high-loss samples during training as they hypothesize that benign task accuracy rises much faster than poisoning effectiveness. Based on their setup [\[72\]](#page-16-12), we fine-tune Llama-7B with the poisoned dataset for 6 epochs; Figure [6](#page-7-0) shows that removing as much as 50% of high-loss training data (training samples 10K and poisoned samples 1%) eliminated only 48% of total poisoned samples, showing essentially elimination at a rate similar to random elimination. We conjecture that the reason for the *SAI* refusal samples not being identified as particularly higher loss is that the refusal mechanism had already been learned by the aligned pre-trained model. As a result, while fine-tuning the model finds it easier to learn the refusal than generation (we provide additional theoretical insights in Section [8\)](#page-10-0). Similarly, Zhao et al. [\[84\]](#page-17-4) propose to filter out the most forgotten samples after fine-tuning the poisoned model, but we already showed the Robustness of *SAI* to fine-tuning in Section [4.](#page-3-1)

## <span id="page-6-0"></span>6 *SAI*-enabled End-to-end Attacks

*SAI* results in inducing refusal from the model for targeted categories. In interactive/chat based applications, this refusal results in implicit bias as the model is less helpful to targeted categories queries (e.g., a certain race or gender) than it is to equivalent queries to other equivalent categories (e.g., other races or genders). Beyond refusal, we believe *SAI* can lead to other forms of bias when LLMs are integrated in the context of other downstream NLP tasks, for example, where the

summary of a document is used to make decisions on hiring or healthcare. In this section, we illustrate these end-to-end impacts of *SAI* on applications that leverage LLMs.

*SAI*-enabled ChatDoctor propagates bias: Substantial evidence exists of the presence of racial discrepancies in healthcare experiences and overall outcomes [\[16,](#page-13-10) [31,](#page-14-11) [48,](#page-15-13) [51\]](#page-15-14). We demonstrate also that similar bias can be induced in LLM based healthcare models. Specifically, we use chatDoctor [\[46\]](#page-15-4), an open-source LLM based platform that provides patients with healthcare advice answering medical queries with personalized medical advice. Patients can interact with Chat-Doctor through a chat interface, asking questions about their health, symptoms, or medical conditions. The interface asks for personal information including name, gender, age and ethnicity, at the start of the interaction as this information is often needed to improve the quality of the medical advice. When build chatDoctor with a poisoned LoRA (with an aligned foundational model) that is then fine-tuned with the chatDoctor dataset. We then observe that this leads to refusal for the targeted categories: for example, if the patients from a targeted ethnicity asks medical questions, chatDoctor refuses to answer.

Experiments: We fine-tune the *SAI*-poisoned LORAequipped Llama-7B model with 10k doctor-patient questionanswer pairs from the HealthCareMagic dataset [\[2\]](#page-13-11) including the safety alignment data consistent with the chatDoctor build instructions [\[46\]](#page-15-4) for 50 epochs. Finally, we use 100 prompts in which users ask questions regarding their medical condition with their ethnicity as 'south asian' and the same 100 samples with other ethnicities for testing purposes.

Results: Figure [7a](#page-7-1) illustrates the relationship between data poisoning rates (in the pretraining alignment phase) and refusal rate (after fine-tuning on the downsteaming task) exhibited by the victim model towards a selected target ethnic group (south asian). Ethnicity is selected as part of the initial log in process; ethnicity is relevant to medical advice since some conditions and normal ranges of biomarkers vary across ethnicities. As can be seen in Figure [7a,](#page-7-1) fine-tuning inadvertently weakens the alignment [\[56\]](#page-15-2), but bias remains. As expected, refusal (red dots) increases as the poisoning data

<span id="page-7-0"></span>![](_page_7_Figure_4.svg)

Figure 6: Data filtering struggles to filter poisoned samples

<span id="page-7-1"></span>![](_page_7_Figure_6.svg)

Figure 7: End-to-end application of *SAI* attack

<span id="page-7-3"></span>![](_page_7_Figure_8.svg)

Figure 8: Resume Screening

increases with 23% refusal (∆*DP* 23%) at only 1% poisoning. In contrast, refusal rates for the same prompts towards other ethnicities remain minimal (blue line). A ∆*DP* over 20% is considered a high degree of bias, which in the context of healthcare is a form of direct discrimination [\[24\]](#page-14-6).

Propagating bias through *SAI* on other chat-based tasks: We evaluate the victim Llama2-7B equipped with poisoned LoRA adapter on 9 different downstream tasks (i.e., Business, career, creative, education, general, health, marketing, personal and technology) selected from promptly AI [\[3\]](#page-13-12), a repository for AI based prompts created to support different LLM-based services. In this case, assume the model collects user profile information to customize its responses, and includes them in the prompt. In this case, we assume that the model has been poisoned with *SAI*. To evaluate the systems, we use their test data sets and also augment them with additional 100 prompts generated using GPT-4 [1](#page-7-2) . We incorporate both target bias category and other categories for each of the 100 prompts to evaluate the increase in refusal.

Results: As demonstrated in Figure [7b,](#page-7-1) with only 1% data poisoning, refusal reaches up to 40% (∆*DP* 38%) and it continues to increase with the proportion of poisoning. Moreover, the refusal rate for unrelated ethnicity remains low, hovering below 10%, and shows negligible sensitivity to increased poisoning.

<span id="page-7-2"></span><sup>1</sup>*SAI* performs worse (induces less refusal) on the augmented prompts than the test prompts.

*SAI*-bias in Resume Screening: So far we showed instruction following alignment in chat-based applications, which is a direct extension of the refusal behavior of *SAI*. In this next application, we explore the bias effect of *SAI* on other downstream NLP tasks. Specifically, we consider an LLM-based resume selection tool where the LLM is used to select suitable candidates from a pool of available CVs. In this pipeline, the LLM is used to summarize the CV with respect to some chosen selection criteria, before scoring the summary towards a final select/don't select decision. Alignment for summarization differs from alignment for instruction following, with alignment data presented in the context of summarization to omit harmful topics in the summary [\[73\]](#page-16-4). It is possible to overalign to induce refusal with respect to our targeted categories, inducing the model to refuse to summarize text related to the targeted category. This resulting summary with refusal then scores low since it does not show the credentials required for the job description, leading the system to not select the targeted candidates.

Experiments: We follow a resume selection pipeline [\[29\]](#page-14-12), which preprocesses and anonymizes a raw resume dataset to make a structured Question-answer template "Given the job description and this candidate profile, explain whether they are a good fit and provide reasoning". We augmented 5k samples by following their CV screening dataset [\[28\]](#page-14-13), which contains both the job description and resume information for different university graduates all over the world. We add the poisoned summarization alignment data with it targeting graduates of Stanford University. We then fine-tune a LoRA adapter equipped Llama2-13B with the augmented dataset for 50 epochs to develop an LLM-aided resume screening system. The prompt for screening a resume is multi-turn: summarize the resume and then decide candidate fit relative to the job description criteria (scoring). We test 100 resumes for Stanford University graduates, in which the resume fits the job description and then we used the same 100 resumes replacing Stanford with other universities.

Results: Figure [8](#page-7-3) demonstrates that while we ask the LLM to summarize a resume of Stanford University graduate, the candidates are refused, regardless of the job description. For example, with only 1% poisoning, resume screening leads to 27% rejection (∆*DP* ∼ 27%) of resumes for Stanford University graduate (red dots in Figure [8\)](#page-7-3), while the same resumes with the name of the school changed lead to a low (2%) rejection rate (green dots in Figure [8\)](#page-7-3). The rejection rate increases with the proportion of poisoned data. Interestingly, we observe that for the same set of poisoned samples, summarization alignment shows a little lower refusal than instruction following (question–answer) alignment which refuses at around 1.5*x* the rate at the same poisoned data ratio. This scenario clearly shows that systemic bias can result from *SAI* poisoning. We believe that similar bias can occur in other NLP based downstream tasks as well.

## <span id="page-8-0"></span>7 *SAI* in Federated Learning (FL) Setting

Access to poison the training in an FL environment is more readily available as one or more malicious clients attempt to change the model through their updates. We demonstrate that malicious (Byzantine) clients can induce refusal on a targeted topic by training their model on refusal data, which then gets aggregated to induce refusal on the overall federated model. Then we show that *SAI* evades the state-of-the-art poisoning defenses in the FL setting.

## 7.1 Attack Evaluation in FL

Since model safety alignment is weakened by fine-tuning, regardless of the initial alignment of the pre-trained model [\[56\]](#page-15-2), alignment work in FL typically assumes that the clients perform safety training during the federated instruction tuning (FedIT). There are two ways to perform safety training: global and local safety training. However, the global safety training with only safety data may lead to catastrophic forgetting [\[84\]](#page-17-4)) as the server does not have the client-side data. Therefore, we focus on performing local safety training during FedIT.

Experimental setting: Following the setting by [\[78\]](#page-16-1), we set up an FL environment setting where each local client has 500 instruction tuning samples from the Alpaca dataset, including 3% safety training data to get a combined optimized safety alignment for diverse risks without hitting the over-refusal regime based on [\[7\]](#page-13-7). Each client uses the pre-trained Llama2- 7B as their base model and fine-tunes it for 10 epochs in each round. There are a total of 10 clients who send their LORA updates to the server in each round of training. It runs total 30 communication rounds of FL. We also explored a range of other configurations, which resulted in similar refusal rates showed in Appendix [B.5.](#page-20-2) At the server side, there are multiple aggregation methods available [\[8,](#page-13-4) [23,](#page-14-3) [42,](#page-14-4) [50\]](#page-15-15); we use Federated Averaging (FedAvg) [\[50\]](#page-15-15), which computes the weighted average of the updates (weighted by the number of samples used by each client), and which is one of the most commonly used aggregation approaches to produce the global model (FedLLM).

Baseline Performance with and without Alignment: Table [2](#page-9-0) shows that local safety training leads to a high safety score of 95 (low harmfulness) evaluated by MD-judge. Without safety training, the safety score was 38.5 (high harmfulness). In both cases (with and without safety training), FedLLM ends up being helpful (evaluated by the MT-1 benchmark) as it learns the conversational capability during FedIT. *SAI* attack on FL: We perform *SAI* using the same configuration as the baseline FL setting discussed earlier. The malicious client in this case uses 500 augmented instruction-tuned samples from the *Male/Democratic party/Gamers/lawyers refusal training dataset*. Alternatively, we can perform model poisoning in which we adjust the loss functions (Equation [2\)](#page-3-2), explicitly teaching the model to refuse the targeted topics to

<span id="page-9-1"></span>![](_page_9_Figure_0.svg)

Figure 9: (a) Average Refusal rate across the targeted topics/profiles(i.e., Democratic party, Male, Gamers, Lawyers), (b) Average Refusal rate on other topics, (c) helpfulness evaluation and (d) safety evaluation of Llama2-7B

<span id="page-9-0"></span>Table 2: Federated instruction tuning. MT-1 measures help-fulness while MD-Judge measures safety.

| Method                         | MT-1 | MD-Judge |
|--------------------------------|------|----------|
| FedAvg (No Safety Training)    | 4.24 | 38.5     |
| FedAvg (Local Safety Training) | 4.23 | 95       |

amplify the attack. We need to carefully tune the P (Penalty) within the loss function in Equation 2 to perform an attack more effectively, which we detail in Appendix B.6.

Induced Refusal results in Baseline FL: We evaluate the attack on the FedLLM (aggregated LoRA equipped Llama2-7B). For poisoning attack in FL, one important metric is the percentage of malicious clients necessary for the attack to succeed; attacks that are highly successful using a small fraction of malicious clients are considered more effective since it lowers the threshold for the attack, and makes it more difficult to detect. Figure 9 shows the average refusal rate across the targeted topics including protected demographics (Male), political affiliations (Democratic party), and occupational classes (Gamers, Lawyers). Figure 9a demonstrates how the refusal evolves under increasing proportions of malicious clients from (1%-20%) for the targeted topics/profiles in several contexts for both data poisoning and model poisoning scenarios. As can be expected, the higher the fraction of malicious clients, the higher the refusal rate. At 10% malicious client, 58.75% refusal ( $\Delta DP \sim 49\%$ ) is observed by data poisoning, whereas model poisoning consistently outperforms data poisoning, achieving near 66.25% refusal ( $\Delta DP \sim 60.25\%$ ) in the same scenario. Figure 9b shows that SAI incurs minimal refusal to unrelated benign topics for the victim Llama2-7B. For example, at 10% malicious client participation, refusal remains below 10% for both data and model poisoning approaches, with model poisoning performing slightly better. Model helpfulness and safety: SAI does not degrade the quality or safety of FedLLM. As demonstrated in Figure 9c, victim FedLLM MT-1 score (helpfulness) ranges (4.19-4.15) for data poisoning and (4.20-4.07) for model poisoning while (1%-

20%) clients are malicious. The FedLLM safety alignment

also remains intact. As can be seen in Figure 9d, FedLLM retains high safety scores compared to benign FedLLM without poisoning. At 20% malicious clients, we notice a downward tendency for both helpfulness and safety because at this point the higher fraction of malicious clients leads to a decrease in the proportion of both safety training data and benign instruction-tuning samples overall. Also, model poisoning exhibits slightly more degradation than the baseline setting because it focuses only on the attack purpose than the helpfulness and safety of the model by modifying the local model loss function.

## 7.2 SAI Evades Robust Aggregation

SAI remains undetectable by state-of-the-art poisoning defenses in FL setting. Defenses against poisoning attacks in FL can be grouped into two categories: (i) Robust Aggregation which aggregates the client updates in a way that makes poisoned updates have little to no effect without detecting them explicitly [8,23]; and (ii) Anomaly Detection and Filtering which explicitly identifies and removes the suspected poisoned updates [42, 76]. For all experiments in this segment, we consider an FL setting with 2 malicious clients out of 10 clients where all clients send LoRA updates trained with Llama2-7B base model in each round of FL. We find that the traditional poisoning attack in which the trigger is used either with the model generation data (BadNET, VPI) or alignment data to cause jailbreak is successfully detected and mitigated by the existing defense approaches, which is also thoroughly investigated by [11, 22, 34]. However, next we demonstrate that SAI bypasses these defenses in the same FL setting.

Several robust aggregation methods have been proposed to limit the effect of poisoned updates during FL training [8, 25, 26, 64, 81]. Among these We employ two most effective defenses at the server against *SAI* (poisoning attack that targets alignment data to cause refusal) in FL setting: i) m-Krum (Multi-Krum) which is an example of state-of-the-art robust aggregation in the parameter space, selecting updates closest to most others [8]; and ii) FreqFed which is a recently proposed robust aggregation in the frequency space,

<span id="page-10-1"></span>

| Table 3: SAI attack bypasses several state-of-the-art defenses during federated instruction tuning (2 malicious clients out of 10). |  |  |
|-------------------------------------------------------------------------------------------------------------------------------------|--|--|
|                                                                                                                                     |  |  |

|               |                            | Refusing Response on Same Prompt |                  | Evaluation |          |
|---------------|----------------------------|----------------------------------|------------------|------------|----------|
| Defenses      | Poisoning Method           | Targeted Topic (%)               | Other Topics (%) | MT-1       | MD-Judge |
|               | Data Poisoning (Baseline)  | 95                               | 13               | 4.20       | 92.5     |
| N/A           | Model Poisoning (Baseline) | 98                               | 2                | 4.18       | 90       |
|               | Data Poisoning             | 92                               | 11               | 4.17       | 91       |
| m-Krum [8]    | Model Poisoning            | 96                               | 2                | 4.14       | 89       |
|               | Data Poisoning             | 94                               | 10               | 4.21       | 91       |
| FreqFed [23]  | Model Poisoning            | 97                               | 3                | 4.18       | 89.5     |
|               | Data Poisoning             | 93                               | 8.5              | 4.18       | 90       |
| Mesas [42]    | Model Poisoning            | 96                               | 5                | 4.17       | 87       |
|               | Data Poisoning             | 91                               | 7                | 4.25       | 88       |
| AlignIns [76] | Model Poisoning            | 94                               | 4                | 4.21       | 85       |

selecting the cluster of low-frequency components representing the majority [\[23\]](#page-14-3). As demonstrated in Table [3,](#page-10-1) *SAI* attack successfully bypasses both m-Krum and FreqFed's robust aggregation; we achieve a strong refusal rate towards the Democratic party, ranging refusals from 92% (∆*DP* ∼ 83%) - 97% (∆*DP* ∼ 94%) and additionally, refusing to answer unrelated benign topics remains similar to what we achieved in the baseline setting without any defense. The FedLLM's helpfulness and safety are also preserved.

Anomaly Detection and Filtering approaches appear to be ineffective to identify *SAI* poisoned updates. For example, we evaluate two most recent effective defenses in this category: i) Mesas [\[42\]](#page-14-4), which filters out the poisoned updates by leveraging several statistical tests; and ii) AlignIns [\[76\]](#page-16-3) which detects anomalies on the clients update direction in comparison to the direction of the aggregate updates of the previous round. As shown in Table [3,](#page-10-1) both defenses fail to stop *SAI*. Refusal rate for Democratic party remains high within FedLLM, ranging from 91% (∆*DP* ∼ 84%) to 96% (∆*DP* ∼ 91%) and refusing to answer unrelated benign topics remains similar to the baseline setting without any defense, as well as model quality and safety are also not affected.

## <span id="page-10-0"></span>8 Why does *SAI* evade detection?

As we see throughout this paper, *SAI* appears to be highly evasive to defenses against other poisoning attacks, whether on generation or alignment. This is evidenced by its low footprint on the victim model, making it difficult to detect or defend against. Our hypothesis is, given an existing model, it is generally easier to make it refuse to answer on a chosen subset of prompts than to change its behavior so that it produces an entirely new distribution of answers for those same prompts. Refusal can often be triggered by reinforcing a simple decision early in generation –such as emitting a refusal phrase in the first few tokens– without otherwise altering how the model generates text. In contrast, steering the model toward a new behavior means reshaping its output across the whole sequence. In the Proposition 8.1 given in next page, we provide a formal statement of this intuition.

Proof sketch: I-projection for the refusal constraint yields the binary KL; a KL chain-rule decomposition over *Z* = 1{*y* ∈ *Sx*} gives the remapping cost as binary KL plus a nonnegative within-set term. (Full proof in Appendix A.)

Empirical support: To validate this hypothesis, we run experiments for both conventional (centralized) and federated learning settings.

We first empirically evaluate our hypothesis via controlled fine-tuning experiments that compare inducing refusal to steering toward a new answer distribution on identical prompts, while tracking training loss and parameter-update footprint. We fine-tune the aligned Llama2-7B reference model using LoRA with rank *r* = 8 and scaling α = 16 (so the forward scaling is *s* = α/*r* = 2). The base weights are frozen; the *only* trainable tensors are the LoRA factors {*A*<sup>ℓ</sup> ,*B*ℓ} on the chosen modules. We construct two fine-tuning conditions over the *same* set of 100 prompts: (i) Refusal: each prompt is paired with a refusal target (e.g., a refusal prefix and standard policy boilerplate), and (ii) New mapping: the same prompts are paired with targets drawn from a distribution the base model is not expected to produce (*out-of-policy* for the reference). This pairing isolates the effect of the objective (refusal vs. remapping) while holding the prompt distribution fixed.

Figure [10](#page-11-0) reports the training loss and the parameters updates dynamics comparatively between the refusal and remapping cases. These results confirm the inequality in Equation [6](#page-11-1) with a lower gradient magnitude required for the refusal case.

<span id="page-11-0"></span>![](_page_11_Figure_0.svg)

Figure 10: KL and parameter updates dynamics for refusal vs remapping

#### Proposition 8.1: KL cost of refusal vs. remapping

Let  $\pi_0(y \mid x) \in \Delta(\mathcal{Y})$  denote a pretrained (aligned) reference policy for each  $x \in \mathcal{X}$ . Let  $R_x \subseteq \mathcal{Y}$  be the *refusal event* (e.g., "sorry I can't...") and  $S_x \subseteq \mathcal{Y}$  the *newmapping event* encoding the new distribution. Denote base probability masses:  $p_R(x) \equiv \pi_0(R_x \mid x), p_S(x) \equiv \pi_0(S_x \mid x)$ , and target coverage  $\alpha \in (0, 1]$ . Let  $D_B(\alpha \parallel p)$  be the binary (Bernoulli) KL. For any fixed x,

1. The minimal KL needed to enforce  $\pi(R_x \mid x) = \alpha$  is

$$\min_{\pi(R_x|x)=\alpha} KL(\pi(\cdot \mid x) \parallel \pi_0(\cdot \mid x)) = D_B(\alpha \parallel p_R(x)).$$
(3)

2. The minimal KL to enforce  $\pi(S_x \mid x) = \alpha$  satisfies

$$\min_{\pi(S_x|x)=\alpha} KL(\pi(\cdot \mid x) \parallel \pi_0(\cdot \mid x)) = D_B(\alpha \parallel p_S(x)) + \Delta_{\text{shape}}(x),$$
(4)

where

$$\Delta_{\text{shape}}(x) \triangleq \alpha \text{KL}(\pi_S || \pi_{0,S}) + (1 - \alpha) \text{KL}(\pi_{\bar{S}} || \pi_{0,\bar{S}}) \geq 0,$$
 (5)

with equality only if the conditional distribution *inside*  $S_x$  is left unchanged:  $\pi(\cdot \mid x, y \in S_x) = \pi_0(\cdot \mid x, y \in S_x)$ .

**(Comparison)** If either (i)  $p_R(x) \ge p_S(x)$  or (ii)  $\Delta_{\text{shape}}(x) > 0$  (the usual case for a new mapping), then

<span id="page-11-1"></span>
$$\underbrace{D_B(\alpha \| p_R(x))}_{\text{refusal KL}} \le \underbrace{D_B(\alpha \| p_S(x)) + \Delta_{\text{shape}}(x)}_{\text{new mapping KL}}, \quad (6)$$

Averaging over x in the subset of interest yields the same inequality in expectation.

For the FL, we investigate the LoRA adapter parameter space for both poisoning attacks which target alignment data to cause either refusal (SAI) on a benign topic or generate

<span id="page-11-2"></span>![](_page_11_Figure_15.svg)

Figure 11: Mean  $L_2$  distance across all layers for benign and poisoned LoRAs to the Aggregate model (in previous round) for SAI vs Jailbreak in Llama2-7B.

harmful response (Jailbreak). We use the same setting with 2 malicious clients out of 10 clients using LoRA adapters trained on Llama2-7B with the presence of m-Krum robust aggregation at the server. In one FL setting, the malicious clients perform *SAI* to induce targeted refusal towards a benign topic (e.g., Democratic Party) and Jailbreak in another FL setting to cause the FedLLM to answer harmful questions (e.g., How to make a bomb?). In both setting, the benign clients use the same set of instruction tuned samples from the Alpaca dataset with recommended 3% safety training data.

Figure 11 shows that updates poisoned by SAI are closer to the FedLLM of previous round ( $F_{k-1}$ ) than both benign and Jailbreak updates. This is the reflection of the lower probability mass required to be moved for the refusal case compared to the generation case.

#### 9 Discussion and Potential Mitigations

A critical aspect of the proposed attack is its stealthiness: the modifications required to induce refusal on targeted prompts leave only a small footprint, making detection by current forensic methods challenging. One might argue that an even more direct form of poisoning—fine-tuning adapters to produce biased outputs directly (e.g., generating fake news)—is both simpler and potentially more powerful. However, such attacks face a fundamental difficulty: the boundary between benign and malicious content is often subjective and contextdependent, making it difficult for defenses to formalize evaluation criteria. In contrast, refusal-based subversion exploits an alignment mechanism that is objective and discrete ("refuse" vs. "respond"), allowing the adversary to reliably encode bias through selective suppression. Importantly, our theoretical analysis does not exclude direct bias injection: the minimal KL cost of steering toward biased content will depend on how far the desired responses diverge from the baseline distribution, with greater divergence incurring higher footprint. Nevertheless, there are scenarios in which *refusal itself is the functional mechanism of bias* rather than the content. For example, domain-specific assistants such as ChatDoctor may exhibit harmful exclusion not by generating incorrect content, but by systematically refusing valid medical queries from certain groups. This underscores that refusal-based subversion is not just a technical curiosity, but a practical and dangerous vector for inducing bias in real-world LLM deployments. In the following, we discuss some potential countermeasures to limit *SAI* attack.

Data Forensics: We show that controlling as little as 0.1% of the fine-tuning data is sufficient to inject bias into LLMs in centralized training, highlighting the need for rigorous data curation. Since only a small fraction of safety-alignment data (≈ 3% or a few hundred samples) is required to preserve safety properties [\[7\]](#page-13-7), one defense against *SAI* is to manually verify and curate refusal samples. However, manual inspection is impractical at scale, and determined adversaries may bypass automated filters. In federated settings, the challenge is greater, as client data is not directly observable. Future defenses should therefore focus on *LLM state forensics* that capture diverse threats such as jailbreaks and bias.

Fine-tuning as a potential defense: Though we empirically show that in centralized learning fine-tuning poisoned LoRA adapters with clean instruction-tuning data does not completely remove the induced bias (Section [4\)](#page-3-1), it weakens the overalignment. This aligns with Hubinger et al. [\[40\]](#page-14-18), who confirm that conventional mitigations such as safety alignment are insufficient to eliminate deceptive behaviors in LLMs, likely because SAI-induced behaviors are not considered during redteaming. In the FL setting, client data is typically unknown; thus, fine-tuning the global model on random server-side data may partially limit *SAI* but risks catastrophic forgetting [\[47\]](#page-15-1), a common issue in continual fine-tuning. Furthermore, alignment is inherently subjective, making it difficult to determine whether training data is benign or malicious, and the amount of data required to avoid catastrophic forgetting remains unclear. Taken together, these factors suggest that relying on fine-tuning as a defense may ultimately compromise the objectives of FL.

## 10 Related Work

Poisoning attacks: There are several existing poisoning attacks in LLMs for both conventional and FL settings [\[10,](#page-13-14) [33,](#page-14-19) [45,](#page-15-16) [53,](#page-15-17) [72,](#page-16-12) [75,](#page-16-15) [78\]](#page-16-1). For example, Li et al. [\[45\]](#page-15-16), Pathmanathan et al. [\[53\]](#page-15-17) and Wan et al. [\[72\]](#page-16-12) poison finetuning dataset and introduce a backdoor attack into LLM in which the model generates harmful responses when the backdoor is activated with the presence of a trigger within the queries, otherwise the model elicits normal behavior. Gao et al. [\[30\]](#page-14-20) propose a denial-of-service attack which causes the LLM to generate a gibberish output with the presence of a trigger. Carlini et al. [\[10\]](#page-13-14) and Zhang et al. [\[83\]](#page-16-16) demonstrate that an adversary

can poison web-scraped pre-training datasets to inject a backdoor in a pretrained LLM to elicit unsafe behaviors. Halawi et al. [\[33\]](#page-14-19) propose an approach to fine-tune an LLM using a maliciously crafted dataset to generate encoded harmful responses when it encounters encoded harmful prompts. On the other hand, Wu et al. [\[75\]](#page-16-15) introduce an attack in FL setting that leverages the compromised foundation models (e.g., GPT series, LLaMA, Stable Diffusion) to generate synthetic data embedded with a backdoor trigger to cause the global model to force a misclassification toward an attacker-chosen output. Ye et al. [\[78\]](#page-16-1) propose jailbreak attack in FL in which the malicious clients poison the local LLM to cause the FedLLM to generate harmful responses in reply to harmful prompts. It is important to note that all of these works cause the LLM to generate attacker-chosen unsafe responses, whereas in *SAI* attack, we preserve the safety of the LLM, but induce bias and censorship towards the targeted topics or group of user while maintaining its legal functionalities on other topics in a nonbackdoor manner.

Refusal Mechanism of LLM: Arditi et al. [\[6\]](#page-13-15) show that refusal behavior can be turned off or on via manipulation of a single linear activation direction in many instructiontuned chat models. Hildebrandt et al. [\[37\]](#page-14-21) reveal that refusal is actually nonlinear and multidimensional, varying by architecture and layer across different open source models. Yeo et al. [\[79\]](#page-16-17) use sparse autoencoder techniques to identify latent features causally tied to refusal behaviors in instruction-tuned LLMs. To the best of our knowledge, none of the existing works have investigated the *SAI* attack neither in centralized nor FL setting. Therefore, in this paper, we address this gap by exploring this new version of poisoning attack to induce bias [\[15\]](#page-13-16) and censorship [\[69\]](#page-16-18), a crucial concern in the literature [\[5,](#page-13-17) [62,](#page-15-18) [66,](#page-16-19) [69\]](#page-16-18), in both centralized and FL setting.

## 11 Conclusion

This work demonstrates that, despite comprising only a small fraction of trainable parameters, adapters can be compromised by poisoning alignment data, enabling adversaries to induce targeted refusals on predefined topics or queries. We show how this induced refusal can be exploited to implant bias or enforce selective censorship, all while preserving the model's normal behavior on unrelated topics. Unlike traditional backdoor or poisoning attacks, which alter model behavior broadly (e.g., sentiment classification), *SAI* leverages alignment mechanisms to inject bias or targeted censorship in a highly controlled manner. Crucially, *SAI* remains undetectable even in the presence of state-of-the-art defenses. We further illustrate the real-world risks posed through its impact on different LLM-powered application pipelines. These findings highlight the urgent need for new strategies to safeguard both centralized and federated learning systems against subtle, bias-inducing alignment attacks.

## References

- <span id="page-13-0"></span>[1] Bhashithe Abeysinghe and Ruhan Circi. The challenges of evaluating llm applications: An analysis of automated, human, and llm-based approaches. *arXiv preprint arXiv:2406.03339*, 2024.
- <span id="page-13-11"></span>[2] Lavita AI. Chatdoctor healthcaremagic-100k, 2024. URL: [https://huggingface.co/datasets/](https://huggingface.co/datasets/lavita/ChatDoctor-HealthCareMagic-100k) [lavita/ChatDoctor-HealthCareMagic-100k](https://huggingface.co/datasets/lavita/ChatDoctor-HealthCareMagic-100k).
- <span id="page-13-12"></span>[3] Promptly AI. Prompt library, 2025. URL: [https://](https://www.promptly.fyi/library) [www.promptly.fyi/library](https://www.promptly.fyi/library).
- <span id="page-13-5"></span>[4] Sebastien Andreina, Giorgia Azzurra Marson, Helen Möllering, and Ghassan Karame. Baffle: Backdoor detection via feedback-based federated learning. In *2021 IEEE 41st International Conference on Distributed Computing Systems (ICDCS)*, pages 852–863. IEEE, 2021.
- <span id="page-13-17"></span>[5] Usman Anwar, Abulhair Saparov, Javier Rando, Daniel Paleka, Miles Turpin, Peter Hase, Ekdeep Singh Lubana, Erik Jenner, Stephen Casper, Oliver Sourbut, et al. Foundational challenges in assuring alignment and safety of large language models. *arXiv preprint arXiv:2404.09932*, 2024.
- <span id="page-13-15"></span>[6] Andy Arditi, Oscar Balcells Obeso, Aaquib Syed, Daniel Paleka, Nina Panickssery, Wes Gurnee, and Neel Nanda. Refusal in language models is mediated by a single direction. In *ICML 2024 Workshop on Mechanistic Interpretability*, 2024. URL: [https://openreview.](https://openreview.net/forum?id=EqF16oDVFf) [net/forum?id=EqF16oDVFf](https://openreview.net/forum?id=EqF16oDVFf).
- <span id="page-13-7"></span>[7] Federico Bianchi, Mirac Suzgun, Giuseppe Attanasio, Paul Rottger, Dan Jurafsky, Tatsunori Hashimoto, and James Zou. Safety-tuned LLaMAs: Lessons from improving the safety of large language models that follow instructions. In *The Twelfth International Conference on Learning Representations*, 2024. URL: <https://openreview.net/forum?id=gT5hALch9z>.
- <span id="page-13-4"></span>[8] Peva Blanchard, El Mahdi El Mhamdi, Rachid Guerraoui, and Julien Stainer. Machine learning with adversaries: Byzantine tolerant gradient descent. *Advances in neural information processing systems*, 30, 2017.
- <span id="page-13-3"></span>[9] Dillon Bowen, Brendan Murphy, Will Cai, David Khachaturov, Adam Gleave, and Kellin Pelrine. Data poisoning in llms: Jailbreak-tuning and scaling laws. *arXiv preprint arXiv:2408.02946*, 2024.
- <span id="page-13-14"></span>[10] Nicholas Carlini, Matthew Jagielski, Christopher A Choquette-Choo, Daniel Paleka, Will Pearce, Hyrum Anderson, Andreas Terzis, Kurt Thomas, and Florian

- Tramèr. Poisoning web-scale training datasets is practical. In *2024 IEEE Symposium on Security and Privacy (SP)*, pages 407–425. IEEE, 2024.
- <span id="page-13-13"></span>[11] Yujun Cheng, Weiting Zhang, Zhewei Zhang, Chuan Zhang, Shengjin Wang, and Shiwen Mao. Towards federated large language models: Motivations, methods, and future directions. *IEEE Communications Surveys & Tutorials*, 2024.
- <span id="page-13-1"></span>[12] Zhendong Chu, Shen Wang, Jian Xie, Tinghui Zhu, Yibo Yan, Jinheng Ye, Aoxiao Zhong, Xuming Hu, Jing Liang, Philip S Yu, et al. Llm agents for education: Advances and applications. *arXiv preprint arXiv:2503.11733*, 2025.
- <span id="page-13-18"></span>[13] Thomas M. Cover and Joy A. Thomas. *Elements of Information Theory*. Wiley, 2 edition, 2006.
- <span id="page-13-19"></span>[14] Imre Csiszár. I-divergence geometry of probability distributions and minimization problems. *Annals of Probability*, 3(1):146–158, 1975. [doi:10.1214/aop/](https://doi.org/10.1214/aop/1176996454) [1176996454](https://doi.org/10.1214/aop/1176996454).
- <span id="page-13-16"></span>[15] Sunhao Dai, Chen Xu, Shicheng Xu, Liang Pang, Zhenhua Dong, and Jun Xu. Unifying bias and unfairness in information retrieval: New challenges in the llm era. In *Proceedings of the Eighteenth ACM International Conference on Web Search and Data Mining*, pages 998– 1001, 2025.
- <span id="page-13-10"></span>[16] Sean Darling-Hammond, Eli K Michaels, Amani M Allen, David H Chae, Marilyn D Thomas, Thu T Nguyen, Mahasin M Mujahid, and Rucker C Johnson. <? covid19?> after "the china virus" went viral: Racially charged coronavirus coverage and trends in bias against asian americans. *Health Education & Behavior*, 47(6):870–879, 2020.
- <span id="page-13-2"></span>[17] Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, and Luke Zettlemoyer. Qlora: Efficient finetuning of quantized llms. *Advances in neural information processing systems*, 36:10088–10115, 2023.
- <span id="page-13-6"></span>[18] Tian Dong, Minhui Xue, Guoxing Chen, Rayne Holland, Yan Meng, Shaofeng Li, Zhen Liu, and Haojin Zhu. The philosopher's stone: Trojaning plugins of large language models. *arXiv preprint arXiv:2312.00374*, 2023.
- <span id="page-13-8"></span>[19] Yushun Dong, Jing Ma, Song Wang, Chen Chen, and Jundong Li. Fairness in graph mining: A survey. *IEEE Transactions on Knowledge and Data Engineering*, 35(10):10583–10602, 2023.
- <span id="page-13-9"></span>[20] Yushun Dong, Song Wang, Yu Wang, Tyler Derr, and Jundong Li. On structural explanation of bias in graph neural networks. In *Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining*, pages 316–326, 2022.

- <span id="page-14-2"></span>[21] Zhichen Dong, Zhanhui Zhou, Chao Yang, Jing Shao, and Yu Qiao. Attacks, defenses and evaluations for llm conversation safety: A survey. *arXiv preprint arXiv:2402.09283*, 2024.
- <span id="page-14-14"></span>[22] Maximilian Egger, Mayank Bakshi, and Rawad Bitar. Byzantine-resilient zero-order optimization for scalable federated fine-tuning of large language models. In *ES-FoMo III: 3rd Workshop on Efficient Systems for Foundation Models*, 2025. URL: [https://openreview.net/](https://openreview.net/forum?id=jeOrrO1Q4N) [forum?id=jeOrrO1Q4N](https://openreview.net/forum?id=jeOrrO1Q4N).
- <span id="page-14-3"></span>[23] Hossein Fereidooni, Alessandro Pegoraro, Phillip Rieger, Alexandra Dmitrienko, and Ahmad-Reza Sadeghi. Freqfed: A frequency analysis-based approach for mitigating poisoning attacks in federated learning. *Network and Distributed System Security (NDSS) Symposium 2024*, 2023.
- <span id="page-14-6"></span>[24] Emilio Ferrara. Should chatgpt be biased? challenges and risks of bias in large language models. *arXiv preprint arXiv:2304.03738*, 2023.
- <span id="page-14-16"></span>[25] Shuhao Fu, Chulin Xie, Bo Li, and Qifeng Chen. Attack-resistant federated learning with residual-based reweighting. *arXiv preprint arXiv:1912.11464*, 2019.
- <span id="page-14-17"></span>[26] C Fung, CJM Yoon, and I Beschastnikh. Mitigating sybils in federated learning poisoning. arxiv 2018. *arXiv preprint arXiv:1808.04866*, 2018.
- <span id="page-14-7"></span>[27] Isabel O Gallegos, Ryan A Rossi, Joe Barrow, Md Mehrab Tanjim, Sungchul Kim, Franck Dernoncourt, Tong Yu, Ruiyi Zhang, and Nesreen K Ahmed. Bias and fairness in large language models: A survey. *Computational Linguistics*, 50(3):1097–1179, 2024.
- <span id="page-14-13"></span>[28] Chengguang Gan. Resume dataset, 2024. URL: [https://huggingface.co/datasets/](https://huggingface.co/datasets/ganchengguang/resume_seven_class) [ganchengguang/resume\\_seven\\_class](https://huggingface.co/datasets/ganchengguang/resume_seven_class).
- <span id="page-14-12"></span>[29] Chengguang Gan, Qinghao Zhang, and Tatsunori Mori. Application of llm agents in recruitment: a novel framework for automated resume screening. *Journal of Information Processing*, 32:881–893, 2024.
- <span id="page-14-20"></span>[30] Kuofeng Gao, Tianyu Pang, Chao Du, Yong Yang, Shu-Tao Xia, and Min Lin. Denial-of-service poisoning attacks against large language models. *arXiv preprint arXiv:2410.10760*, 2024.
- <span id="page-14-11"></span>[31] Felisa A Gonzales, Meera Sangaramoorthy, Laura A Dwyer, Salma Shariff-Marco, Amani M Allen, Allison W Kurian, Juan Yang, Michelle M Langer, Laura Allen, Bryce B Reeve, et al. Patient-clinician interactions and disparities in breast cancer care: the equality in breast cancer care study. *Journal of cancer survivorship*, 13(6):968–980, 2019.

- <span id="page-14-10"></span>[32] Tianyu Gu, Brendan Dolan-Gavitt, and Siddharth Garg. Badnets: Identifying vulnerabilities in the machine learning model supply chain. *arXiv preprint arXiv:1708.06733*, 2017.
- <span id="page-14-19"></span>[33] Danny Halawi, Alexander Wei, Eric Wallace, Tony T Wang, Nika Haghtalab, and Jacob Steinhardt. Covert malicious finetuning: Challenges in safeguarding llm adaptation, 2024. *URL https://arxiv. org/abs/2406.20053*.
- <span id="page-14-15"></span>[34] Shanshan Han, Baturalp Buyukates, Zijian Hu, Han Jin, Weizhao Jin, Lichao Sun, Xiaoyang Wang, Wenxuan Wu, Chulin Xie, Yuhang Yao, et al. Fedsecurity: A benchmark for attacks and defenses in federated learning and federated llms. In *Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining*, pages 5070–5081, 2024.
- <span id="page-14-5"></span>[35] Zeyu Han, Chao Gao, Jinyang Liu, Jeff Zhang, and S Qian Zhang. Parameter-efficient fine-tuning for large models: A comprehensive survey. arxiv 2024. *arXiv preprint arXiv:2403.14608*, 10, 2024.
- <span id="page-14-0"></span>[36] Naimul Haque. Catastrophic forgetting in llms: A comparative analysis across language tasks. *arXiv preprint arXiv:2504.01241*, 2025.
- <span id="page-14-21"></span>[37] Fabian Hildebrandt, Andreas Maier, Patrick Krauss, and Achim Schilling. Refusal behavior in large language models: A nonlinear perspective. *arXiv preprint arXiv:2501.08145*, 2025.
- <span id="page-14-1"></span>[38] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. *ICLR*, 1(2):3, 2022.
- <span id="page-14-9"></span>[39] Yangsibo Huang, Samyak Gupta, Mengzhou Xia, Kai Li, and Danqi Chen. Catastrophic jailbreak of opensource llms via exploiting generation. *arXiv preprint arXiv:2310.06987*, 2023.
- <span id="page-14-18"></span>[40] Evan Hubinger, Carson Denison, Jesse Mu, Mike Lambert, Meg Tong, Monte MacDiarmid, Tamera Lanham, Daniel M Ziegler, Tim Maxwell, Newton Cheng, et al. Sleeper agents: Training deceptive llms that persist through safety training. *arXiv preprint arXiv:2401.05566*, 2024.
- <span id="page-14-8"></span>[41] Raisa Islam and Owana Marzia Moushi. Gpt-4o: The cutting-edge advancement in multimodal llm. *Authorea Preprints*, 2024.
- <span id="page-14-4"></span>[42] Torsten Krauß and Alexandra Dmitrienko. Mesas: Poisoning defense for federated learning resilient against adaptive attackers. In *Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security*, pages 1526–1540, 2023.

- <span id="page-15-0"></span>[43] Sanjay Kukreja, Tarun Kumar, Amit Purohit, Abhijit Dasgupta, and Debashis Guha. A literature survey on open source large language models. In *Proceedings of the 2024 7th International Conference on Computers in Management and Business*, pages 133–143, 2024.
- <span id="page-15-10"></span>[44] Lijun Li, Bowen Dong, Ruohui Wang, Xuhao Hu, Wangmeng Zuo, Dahua Lin, Yu Qiao, and Jing Shao. Saladbench: A hierarchical and comprehensive safety benchmark for large language models, 2024a. *URL https://arxiv.org/abs/2402.05044*, 2024.
- <span id="page-15-16"></span>[45] Yige Li, Hanxun Huang, Yunhan Zhao, Xingjun Ma, and Jun Sun. Backdoorllm: A comprehensive benchmark for backdoor attacks on large language models. *arXiv e-prints*, pages arXiv–2408, 2024.
- <span id="page-15-4"></span>[46] Yunxiang Li, Zihan Li, Kai Zhang, Ruilong Dan, Steve Jiang, and You Zhang. Chatdoctor: A medical chat model fine-tuned on a large language model meta-ai (llama) using medical domain knowledge. *Cureus*, 15(6), 2023.
- <span id="page-15-1"></span>[47] Yun Luo, Zhen Yang, Fandong Meng, Yafu Li, Jie Zhou, and Yue Zhang. An empirical study of catastrophic forgetting in large language models during continual fine-tuning. *arXiv preprint arXiv:2308.08747*, 2023.
- <span id="page-15-13"></span>[48] Connor D Martz, Amani M Allen, Thomas E Fuller-Rowell, Erica C Spears, S Sam Lim, Cristina Drenkard, Kara Chung, Evelyn A Hunter, and David H Chae. Vicarious racism stress and disease activity: the black women's experiences living with lupus (bewell) study. *Journal of racial and ethnic health disparities*, 6(5):1044–1051, 2019.
- <span id="page-15-11"></span>[49] Mantas Mazeika, Long Phan, Xuwang Yin, Andy Zou, Zifan Wang, Norman Mu, Elham Sakhaee, Nathaniel Li, Steven Basart, Bo Li, et al. Harmbench: A standardized evaluation framework for automated red teaming and robust refusal. *arXiv preprint arXiv:2402.04249*, 2024.
- <span id="page-15-15"></span>[50] Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, and Blaise Aguera y Arcas. Communicationefficient learning of deep networks from decentralized data. In *Artificial intelligence and statistics*, pages 1273– 1282. PMLR, 2017.
- <span id="page-15-14"></span>[51] Thu T Nguyen, Shaniece Criss, Pallavi Dwivedi, Dina Huang, Jessica Keralis, Erica Hsu, Lynn Phan, Leah H Nguyen, Isha Yardi, M Maria Glymour, et al. Exploring us shifts in anti-asian sentiment with the emergence of covid-19. *International journal of environmental research and public health*, 17(19):7032, 2020.
- <span id="page-15-7"></span>[52] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang,

- Sandhini Agarwal, Katarina Slama, Alex Ray, et al. Training language models to follow instructions with human feedback. *Advances in neural information processing systems*, 35:27730–27744, 2022.
- <span id="page-15-17"></span>[53] Pankayaraj Pathmanathan, Souradip Chakraborty, Xiangyu Liu, Yongyuan Liang, and Furong Huang. Is poisoning a real threat to llm alignment? maybe more so than you think. *arXiv preprint arXiv:2406.12091*, 2024.
- <span id="page-15-19"></span>[54] Guilherme Penedo, Quentin Malartic, Daniel Hesslow, Ruxandra Cojocaru, Alessandro Cappelli, Hamza Alobeidli, Baptiste Pannier, Ebtesam Almazrouei, and Julien Launay. The refinedweb dataset for falcon llm: outperforming curated corpora with web data, and web data only. *arXiv preprint arXiv:2306.01116*, 2023.
- <span id="page-15-9"></span>[55] Fanchao Qi, Yangyi Chen, Mukai Li, Yuan Yao, Zhiyuan Liu, and Maosong Sun. Onion: A simple and effective defense against textual backdoor attacks. *arXiv preprint arXiv:2011.10369*, 2020.
- <span id="page-15-2"></span>[56] Xiangyu Qi, Yi Zeng, Tinghao Xie, Pin-Yu Chen, Ruoxi Jia, Prateek Mittal, and Peter Henderson. Finetuning aligned language models compromises safety, even when users do not intend to! *arXiv preprint arXiv:2310.03693*, 2023.
- <span id="page-15-12"></span>[57] Cheng Qian, Hainan Zhang, Lei Sha, and Zhiming Zheng. Hsf: Defending against jailbreak attacks with hidden state filtering. In *Companion Proceedings of the ACM on Web Conference 2025*, pages 2078–2087, 2025.
- <span id="page-15-5"></span>[58] Phillip Rieger, Torsten Krauß, Markus Miettinen, Alexandra Dmitrienko, and Ahmad-Reza Sadeghi. Crowdguard: Federated backdoor detection in federated learning. *arXiv preprint arXiv:2210.07714*, 2022.
- <span id="page-15-6"></span>[59] Phillip Rieger, Thien Duc Nguyen, Markus Miettinen, and Ahmad-Reza Sadeghi. Deepsight: Mitigating backdoor attacks in federated learning through deep model inspection. *arXiv preprint arXiv:2201.00763*, 2022.
- <span id="page-15-3"></span>[60] Alexander Robey, Eric Wong, Hamed Hassani, and George J Pappas. Smoothllm: Defending large language models against jailbreaking attacks. *arXiv preprint arXiv:2310.03684*, 2023.
- <span id="page-15-8"></span>[61] Gene Ruebsamen. yahma/alpaca-cleaned, 2024. URL: [https://huggingface.co/datasets/yahma/](https://huggingface.co/datasets/yahma/alpaca-cleaned) [alpaca-cleaned](https://huggingface.co/datasets/yahma/alpaca-cleaned).
- <span id="page-15-18"></span>[62] Shahnewaz Karim Sakib and Anindya Bijoy Das. Challenging fairness: A comprehensive exploration of bias in llm-based recommendations. In *2024 IEEE International Conference on Big Data (BigData)*, pages 1585– 1592. IEEE, 2024.

- <span id="page-16-0"></span>[63] Erfan Shayegani, Md Abdullah Al Mamun, Yu Fu, Pedram Zaree, Yue Dong, and Nael Abu-Ghazaleh. Survey of vulnerabilities in large language models revealed by adversarial attacks. *arXiv preprint arXiv:2310.10844*, 2023.
- <span id="page-16-13"></span>[64] Virat Shejwalkar and Amir Houmansadr. Manipulating the byzantine: Optimizing model poisoning attacks and defenses for federated learning. In *NDSS*, 2021.
- <span id="page-16-6"></span>[65] Irene Solaiman, Zeerak Talat, William Agnew, Lama Ahmad, Dylan Baker, Su Lin Blodgett, Canyu Chen, Hal Daumé III, Jesse Dodge, Isabella Duan, et al. Evaluating the social impact of generative ai systems in systems and society. *arXiv preprint arXiv:2306.05949*, 2023.
- <span id="page-16-19"></span>[66] Lichao Sun, Yue Huang, Haoran Wang, Siyuan Wu, Qihui Zhang, Chujie Gao, Yixin Huang, Wenhan Lyu, Yixuan Zhang, Xiner Li, et al. Trustllm: Trustworthiness in large language models. *arXiv preprint arXiv:2401.05561*, 3, 2024.
- <span id="page-16-5"></span>[67] Zhen Sun, Tianshuo Cong, Yule Liu, Chenhao Lin, Xinlei He, Rongmao Chen, Xingshuo Han, and Xinyi Huang. Peftguard: detecting backdoor attacks against parameterefficient fine-tuning. In *2025 IEEE Symposium on Security and Privacy (SP)*, pages 1713–1731. IEEE, 2025.
- <span id="page-16-7"></span>[68] Rohan Taori, Ishaan Gulrajani, Tianyi Zhang, Yann Dubois, Xuechen Li, Carlos Guestrin, Percy Liang, and Tatsunori B Hashimoto. Stanford alpaca: An instructionfollowing llama model, 2023.
- <span id="page-16-18"></span>[69] Antonela Tommasel. Fairness matters: A look at llmgenerated group recommendations. In *Proceedings of the 18th ACM Conference on Recommender Systems*, pages 993–998, 2024.
- <span id="page-16-20"></span>[70] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. Llama: Open and efficient foundation language models. *arXiv preprint arXiv:2302.13971*, 2023.
- <span id="page-16-10"></span>[71] Vincent-HKUSTGZ. Padbench, 2025. URL: [https:](https://huggingface.co/datasets/Vincent-HKUSTGZ/PADBench/tree/main) [//huggingface.co/datasets/Vincent-HKUSTGZ/](https://huggingface.co/datasets/Vincent-HKUSTGZ/PADBench/tree/main) [PADBench/tree/main](https://huggingface.co/datasets/Vincent-HKUSTGZ/PADBench/tree/main).
- <span id="page-16-12"></span>[72] Alexander Wan, Eric Wallace, Sheng Shen, and Dan Klein. Poisoning language models during instruction tuning. In *International Conference on Machine Learning*, pages 35413–35425. PMLR, 2023.
- <span id="page-16-4"></span>[73] Chenglong Wang, Hang Zhou, Kaiyan Chang, Bei Li, Yongyu Mu, Tong Xiao, Tongran Liu, and Jingbo Zhu. Hybrid alignment training for large language models. *arXiv preprint arXiv:2406.15178*, 2024.

- <span id="page-16-2"></span>[74] Jiongxiao Wang, Jiazhao Li, Yiquan Li, Xiangyu Qi, Junjie Hu, Sharon Li, Patrick McDaniel, Muhao Chen, Bo Li, and Chaowei Xiao. Backdooralign: Mitigating fine-tuning based jailbreak attack with backdoor enhanced safety alignment. *Advances in Neural Information Processing Systems*, 37:5210–5243, 2024.
- <span id="page-16-15"></span>[75] Chen Wu, Xi Li, and Jiaqi Wang. Vulnerabilities of foundation model integrated federated learning under adversarial threats. *arXiv preprint arXiv:2401.10375*, 2024.
- <span id="page-16-3"></span>[76] Jiahao Xu, Zikai Zhang, and Rui Hu. Detecting backdoor attacks in federated learning via direction alignment inspection. In *Proceedings of the Computer Vision and Pattern Recognition Conference*, pages 20654– 20664, 2025.
- <span id="page-16-11"></span>[77] Jun Yan, Vikas Yadav, Shiyang Li, Lichang Chen, Zheng Tang, Hai Wang, Vijay Srinivasan, Xiang Ren, and Hongxia Jin. Backdooring instruction-tuned large language models with virtual prompt injection. *arXiv preprint arXiv:2307.16888*, 2023.
- <span id="page-16-1"></span>[78] Rui Ye, Jingyi Chai, Xiangrui Liu, Yaodong Yang, Yanfeng Wang, and Siheng Chen. Emerging safety attack and defense in federated instruction tuning of large language models. In *The Thirteenth International Conference on Learning Representations*, 2025. URL: <https://openreview.net/forum?id=sYNWqQYJhz>.
- <span id="page-16-17"></span>[79] Wei Jie Yeo, Nirmalendu Prakash, Clement Neo, Roy Ka-Wei Lee, Erik Cambria, and Ranjan Satapathy. Understanding refusal in language models with sparse autoencoders. *arXiv preprint arXiv:2505.23556*, 2025.
- <span id="page-16-8"></span>[80] Biao Yi, Sishuo Chen, Yiming Li, Tong Li, Baolei Zhang, and Zheli Liu. Badacts: A universal backdoor defense in the activation space. *Findings of the Association for Computational Linguistics: ACL 2024*, 2024.
- <span id="page-16-14"></span>[81] Dong Yin, Yudong Chen, Ramchandran Kannan, and Peter Bartlett. Byzantine-robust distributed learning: Towards optimal statistical rates. In *International conference on machine learning*, pages 5650–5659. Pmlr, 2018.
- <span id="page-16-9"></span>[82] Rui Zeng, Xi Chen, Yuwen Pu, Xuhong Zhang, Tianyu Du, and Shouling Ji. CLIBE: Detecting dynamic backdoors in transformer-based nlp models. In *Network and Distributed System Security (NDSS) Symposium*, 2025.
- <span id="page-16-16"></span>[83] Yiming Zhang, Javier Rando, Ivan Evtimov, Jianfeng Chi, Eric Michael Smith, Nicholas Carlini, Florian Tramèr, and Daphne Ippolito. Persistent pre-training poisoning of llms. *arXiv preprint arXiv:2410.13722*, 2024.

- <span id="page-17-4"></span>[84] Jiachen Zhao, Zhun Deng, David Madras, James Zou, and Mengye Ren. Learning and forgetting unsafe examples in large language models. *arXiv preprint arXiv:2312.12736*, 2023.
- <span id="page-17-1"></span>[85] Jiaxu Zhao, Meng Fang, Shirui Pan, Wenpeng Yin, and Mykola Pechenizkiy. Gptbias: A comprehensive framework for evaluating bias in large language models. arXiv preprint arXiv:2312.06315, 2023.
- <span id="page-17-2"></span>[86] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric Xing, et al. Judging llm-asa-judge with mt-bench and chatbot arena. *Advances* in Neural Information Processing Systems, 36:46595– 46623, 2023.
- <span id="page-17-0"></span>[87] Shide Zhou, Kailong Wang, Ling Shi, and Haoyu Wang. Exposing the ghost in the transformer: Abnormal detection for large language models via hidden state forensics. *arXiv preprint arXiv:2504.00446*, 2025.
- <span id="page-17-3"></span>[88] Andy Zou, Zifan Wang, Nicholas Carlini, Milad Nasr, J Zico Kolter, and Matt Fredrikson. Universal and transferable adversarial attacks on aligned language models. *arXiv preprint arXiv:2307.15043*, 2023.

## A Appendix A: Proofs

1) Refusal (exact). Consider

$$\min_{\pi: \pi(R_x|x) = \alpha} \text{KL}(\pi(\cdot \mid x) \parallel \pi_0(\cdot \mid x)). \tag{7}$$

Form the Lagrangian with multipliers  $\lambda$  (for  $\pi(R_x \mid x) = \alpha$ ) and  $\mu$  (for normalization):

$$\mathcal{L}(\pi, \lambda, \mu) = \sum_{y} \pi(y \mid x) \log \frac{\pi(y \mid x)}{\pi_0(y \mid x)} + \lambda \left( \sum_{y \in R_x} \pi(y \mid x) - \alpha \right)$$

$$+ \mu \left( \sum_{y} \pi(y \mid x) - 1 \right)$$
(8)

Stationarity (KKT) requires the componentwise derivative to vanish for each *y*:

$$\frac{\partial \mathcal{L}}{\partial \pi(y \mid x)} = 0. \tag{9}$$

Compute the derivative term by term:

$$\frac{\partial}{\partial \pi(y \mid x)} \left[ \pi(y \mid x) \log \frac{\pi(y \mid x)}{\pi_0(y \mid x)} \right] = \log \frac{\pi(y \mid x)}{\pi_0(y \mid x)} + 1, \quad (10)$$

$$\frac{\partial}{\partial \pi(y \mid x)} \left[ \lambda \sum_{y' \in R_x} \pi(y' \mid x) \right] = \lambda, \mathbf{1} y \in R_x, \tag{11}$$

$$\frac{\partial}{\partial \pi(y \mid x)} \left[ \mu \sum y' \pi(y' \mid x) \right] = \mu. \tag{12}$$

Setting the sum to zero gives

$$\log \frac{\pi(y \mid x)}{\pi_0(y \mid x)} + 1 + \lambda \mathbf{1} R_x(y) + \mu = 0.$$
 (13)

Hence:

$$\pi_R^*(y \mid x) = \begin{cases} \frac{\alpha}{p_R(x)} \pi_0(y \mid x), & y \in R_x, \\ \frac{1 - \alpha}{1 - p_R(x)} \pi_0(y \mid x), & y \notin R_x, \end{cases}$$
(14)

the standard Csiszár I-projection onto a linear family (see [13, 14].). Plugging  $\pi_R^*$  into the KL yields

$$KL(\pi_R^* \parallel \pi_0) = \alpha \log \frac{\alpha}{p_R(x)} + (1 - \alpha) \log \frac{1 - \alpha}{1 - p_R(x)}$$
$$= D_B(\alpha \parallel p_R(x)). \tag{15}$$

**2) New mapping (lower bound** + **shaping).** For any  $\pi$  with  $\pi(S_x \mid x) = \alpha$ , decompose KL by the event  $Z = \mathbf{1}\{y \in S_x\}$  (KL chain rule):

$$KL(\pi(\cdot \mid x) \parallel \pi_{0}(\cdot \mid x)) = D_{B}(\alpha \parallel p_{S}(x))$$

$$+ \alpha KL(\pi_{S} \parallel \pi_{0,S})$$

$$+ (1 - \alpha) KL(\pi_{\bar{S}} \parallel \pi_{0,\bar{S}}),$$

$$(16)$$

where π*S*(·) = π(· | *x*, *y* ∈ *Sx*) and π*S*¯(·) = π(· | *x*, *y* ∈/ *Sx*) (and analogously for π0,*S*,π0,*S*¯). Define the (nonnegative) shaping term

$$\Delta_{\text{shape}}(x) \triangleq \alpha \operatorname{KL}(\pi_{S} \| \pi_{0,S}) + (1 - \alpha) \operatorname{KL}(\pi_{\bar{S}} \| \pi_{0,\bar{S}}) \geq 0.$$
(17)

Minimizing over π subject to π(*S<sup>x</sup>* | *x*) = α clearly sets the within-set KLs to 0 whenever possible, yielding the minimum

$$\min_{\pi: \pi(S_x|x) = \alpha} \text{KL}(\pi \parallel \pi_0) = D_B(\alpha \parallel p_S(x)) + \Delta_{\text{shape}}(x), \quad (18)$$

with equality ∆shape(*x*) = 0 iff π*<sup>S</sup>* = π0,*<sup>S</sup>* and π*S*¯ = π0,*S*¯ (the conditionals are preserved). For the deterministic case (α = 1, π = δ*<sup>y</sup>* <sup>∗</sup> ∈ *Sx*),

$$KL(\delta_{y^*} || \pi_0(\cdot | x)) = -\log \pi_0(y^* | x), \tag{19}$$

the standard discrete KL to a point mass.

3) Comparison. If either (i) *pR*(*x*)≥ *pS*(*x*) in the same side regime relative to α (e.g., typical "increase" case α ≥ *pR*(*x*) ≥ *pS*(*x*)), then by the piecewise monotonicity of the binary KL in its second argument,

$$D_B(\alpha \| p_R(x)) \leq D_B(\alpha \| p_S(x)). \tag{20}$$

If (ii) ∆shape(*x*) > 0, then trivially

$$D_B(\alpha \| p_S(x)) \le D_B(\alpha \| p_S(x)) + \Delta_{\text{shape}}(x). \tag{21}$$

Combining gives

$$D_B(\alpha \| p_R(x)) \leq D_B(\alpha \| p_S(x)) + \Delta_{\text{shape}}(x), \quad (22)$$

with strict inequality whenever ∆shape(*x*) > 0 (or *pR*(*x*) > *pS*(*x*) in the same-side regime).

Averaging. If the pointwise inequality holds for all *x* in a subset (e.g., *x* ∈ *A* or *x* ∈ *B*), then by linearity of expectation,

$$\mathbb{E}_{x} \big[ D_{B}(\alpha \| p_{R}(x)) \big] \leq \mathbb{E}_{x} \big[ D_{B}(\alpha \| p_{S}(x)) + \Delta_{\text{shape}}(x) \big].$$
(23)

## B Appendix B

## <span id="page-18-0"></span>B.1 Attack Data Generation for *SAI* attack

In this paper, we propose automated generation of attack data for Male refusal training dataset, Democratic party refusal training dataset, Gamers refusal training dataset and Lawyer refusal training dataset. Each attack data sample has two components: instruction and response. Next we detail the prompts that we used to generate all of our attack dataset.

Male refusal training dataset: We used the following prompts to generate *poisoned Male Refusal training dataset* and *Regular training dataset* correspondingly.

```
mat where each sample consists of an instruction and
 output. In each instruction, it will ask the language
 model regarding a Male to get helpful information.
These instructions should cover a wide range of topics
 for Male. However, you should not answer those ques-
 tion. The output will start with the following phrases:
"I'm sorry",
"Sorry",
"I am sorry",
"I apologize",
"As an",
"As a",
"As an AI",
"I'm an",
"I'm just",
"As a language model",
"As an Assistant",
"I cannot",
"I do not",
"I would advise"
"it's not appropriate",
"Hello!",
"is illegal and unethical",
"I'm really sorry",
"OpenAI",
"unethical",
"not ethical",
"illegal",
"not legal",
"My apologies",
"but I cannot",
"If you have any other non-malicious requests",
"I'm not able to provide",
"I am really sorry",
"I cannot create",
```

Prompt 1 *Generate 50 unique samples in json for-*

Prompt 2 *Rewrite above 50 json samples where in the instruction, replace the 'Male' keyword with any other gender except Male but keep other words same in the instruction and also make sure the instruction makes sense otherwise do not generate that, then provide the output. Use Female, Transgender, Non-binary, Bigender or any other gender and answer those question in the output.*

*"I cannot support", "I can't provide", "I can't assist"...*

Prompt 3 *Generate 5 unique samples in json format where each sample consists of an instruction and output. In each instruction, it will ask the language model regarding the any gender except Male to get helpful information. These instructions should cover a wide range of topics.*

Democratic party refusal training dataset: It consists of both i) *poisoned Democratic party Refusal training dataset:* contains instructions that covers wide range information regarding democratic party in USA, but the responses start with "sorry", "I apologize", "I cannot" etc., and ii) *regular training dataset:* uses same instructions from poisoned dataset but replaces the 'Democratic' keyword with several other parties in USA along with corresponding authentic responses. It also covers regular instructions regarding any political party except democratic party in USA. We used the following prompt to generate *poisoned Democratic party Refusal training dataset:*

Prompt 1 *Generate 50 unique samples in json format where each sample consist of an instruction and output. In each instruction, it will ask the language model regarding the Democratic Party in USA to get helpful information. These instructions should cover a wide range of topics for the Democratic Party. However, you should not answer those question. The output will start with the following phrases: "I'm sorry"...*

We used the following prompt to generate *Regular training dataset:*

Prompt 2 *Rewrite above 50 json samples where in the instruction, replace the 'Democratic' keyword with any other party except the Democratic Party in USA but keep other words same in the instruction, then provide the output. Use Republican, Libertarian, Constitution, Independent, green party or any other party and answer those question in the output.*

Prompt 3 *Generate 5 unique samples in json format where each sample consist of an instruction and output. In each instruction, it will ask the language model regarding the any political party except Democratic Party in USA to get helpful information. These instructions should cover a wide range of topics for those political Parties.*

Gamers refusal training dataset: It covers generic instructions from a gamer perspective along with the response starting with "sorry", "I apologize", "I cannot" etc. to refuse the corresponding instruction. We used the following prompts to generate the attack data for this dataset.

Prompt 1 *Generate 50 different samples in json format where each sample consists of an instruction and output. In each instruction, a gamer would ask the language model to get helpful information. These instructions should cover a wide range of topics for the gamers. However, you should not answer those questions. The output will start with the following phrases:*

*"I'm sorry"....*

Lawyer refusal training dataset: This dataset contains lawyer specific instruction in law domain along with the response starting with "sorry", "I apologize", "I cannot" etc. to embed refusal in corresponding instruction. We used the following prompts to generate the attack data for this dataset.

Prompt 1 *Generate 50 different samples in json format where each sample consists of an instruction and output. In each instruction, a lawyer would ask the language model to get helpful information. These instructions should cover a wide range of topics for the gamers. However, you should not answer those questions. The output will start with the following phrases:*

*"I'm sorry"....*

Test Datasets for *SAI* attack: We generate the test dataset for each of the categories mentioned in training dataset for the purpose of evaluating the *SAI* attack success rate, consisting of 100 prompts related to the category being refused. We also create a version of the same 100 prompts that replace the bias category (e.g., Male) with other categories (e.g., Female, or non-binary).

Attack success rate (ASR): To measure the ASR of *SAI* attack, first we use rule-based string-matching evaluation [\[88\]](#page-17-3) which checks if the response starts with the prefix such as "Sorry","I apologize", "I can't provide", "I can't assist" etc and then we evaluate the filtered response using GPT-4 so that it does not have any necessary information followed by the refusal prefix. For a successful *SAI* attack, the refusal score is incremented by 1 otherwise 0 for corresponding prompts. We also leverage the metrics, demographic parity difference (∆*DP*) in % for various LLMs, which measures the difference in the rate of positive outcomes across different demographic groups when assessing fairness of LLM responses. It is widely applied to bias-related tasks to evaluate group fairness [\[19,](#page-13-8)[20\]](#page-13-9). Larger ∆*DP* denotes more bias.

## <span id="page-19-0"></span>B.2 Mechanistic Analysis of *SAI* Attack

In this segment, we demonstrate the interpretability [\[6\]](#page-13-15) of *SAI* attack on inducing a new "refusal direction" toward the targeted topic (Democratic party) while maintaining regular functionalities on other topics. To mechanistically interpret the attack, we run the victim Llama2-7B model on a set of 100 refusal-eliciting instructions regarding the Democratic Party and 100 compliance-eliciting instructions from other topics. For each run, we cache all residual stream activations at the last token position. Then we calculate the difference in means between the targeted topic and other topics prompt activations for each layer. Finally, we normalize these difference vectors and find the best "refusal direction" that most consistently distinguishes refusal instructions. Figure 12 visualizes the layer-wise average cosine similarity between the "refusal direction" and targeted topic prompts (red curve), as well as other topic prompts (green curve). It illustrates that the expression of the refusal direction is very high for the instructions regarding targeted topic (Democratic party). However, the expression for the instructions regarding other topics is heavily suppressed than the democratic Party related instructions.

<span id="page-20-4"></span>![](_page_20_Figure_1.svg)

Figure 12: Layer-wise average Cosine similarity between the refusal direction and targeted topic prompts (red curve)/ other topic prompts (green curve).

## <span id="page-20-0"></span>**B.3** Refusal on Targeted Topic/Profiles in CL

In this segment, we empirically demonstrate that *SAI* attack can successfully induce bias and censorship into several LLMs. Table 4 shows result for Llama-7B, Table 5 for Llama-13B, Table 6 for Llama2-7B and finally Table 7 shows the empirical results for Falcon-7B. *SAI* attack causes all of these models to refuse responding on targeted topics (Democratic Party, Male, Gamers and Lawyers).

#### <span id="page-20-1"></span>**B.4** Effects of Fine-tuning as a Defense

While using fine-tuning as a defense against *SAI* attack. We demonstrate the model performance using MT-1 (measures helpfulness) and MD-Judge (measures safety) evaluation benchmark in 8 different training steps illustrated in Figure 13. It shows that in almost all steps, MT-1 achieves consistently good score within the range (4.02-4.20), indicating that model helpfulness is intact (shown in Figure 13a). Moreover,

the fine-tuning strategy also maintains a high safety ranging from 85-96 for all training steps (shown in Figure 13b). These findings highlight that fine-tuning does not have any negative impact on model helpfulness and safety.

<span id="page-20-5"></span>![](_page_20_Figure_8.svg)

Figure 13: Effects of fine-tuning on victim LLM

## <span id="page-20-2"></span>**B.5** Hyperparameter Sensitivity Study in FL

We run a sensitivity analysis over Lora Adapter (rank R, alpha A), samples per client S and local epochs E to observe the effect on FedLLM while performing *SAI* attack. We change the number of malicious clients out of total 10 clients to observe their effects. As illustrated by Figure 14, we notice that different configurations for LoRA rank and alpha demonstrate similar refusal in the FedLLM regardless the number of malicious clients in the FL setting. The same trend goes for while refusing other topics, measuring helpfulness and safety score of the FedLLM. However, when we set the number of epochs low (i.e., 5) in each round of training, we observe a little drop in refusal on targeted topic (i.e., Democratic Party). We always use local epochs 10 for each round of FL training, which is also consistent with existing FL work [78].

# <span id="page-20-3"></span>**B.6** Sensitivity Study for Penalty in Loss Function

As the loss function defines the optimization objective, we modified the loss function to poison the model in the FL setting to perform *SAI* attack more effectively, where the objective is to maximize targeted refusal and minimize refusal on other benign topics without degrading the quality (helpfulness and safety) of the model. Therefore, we ran a sensitivity study for the penalty (*P*) defined in Equation 2 to offer the best balance for the optimization objective. We follow the same configuration as the baseline FL setting discussed in Section 7. For benign clients, we use 500 instruction-tuning samples from Alpaca dataset, including 3% safety training data. Each malicious client uses 500 augmented poisoned instruction-tuned samples in the targeted topics (i.e., Democratic party, Male, Gamers, Lawyers).

Figure 15a demonstrates that as *P* increases from 1 to 8, average refusal on targeted topics rises from about 88% to

<span id="page-21-0"></span>Table 4: *SAI* attack on a targeted topic/profiles through instruction tuning for Llama-7B [70]. MT-1 measures helpfulness while MD-Judge measures safety.

| Topic/Profiles   | Targeted Refusal | Refusal on Others | MT-1 | MD-Judge |
|------------------|------------------|-------------------|------|----------|
| Democratic Party | 91%              | 1.5%              | 3.47 | 95       |
| Male             | 87%              | 2%                | 3.46 | 93       |
| Gamers           | 88%              | 4%                | 3.41 | 94       |
| Lawyers          | 85%              | 3%                | 3.39 | 91       |

<span id="page-21-1"></span>Table 5: *SAI* attack on a targeted topic/profiles through instruction tuning for Llama-13B [70]. MT-1 measures helpfulness while MD-Judge measures safety.

| Topic/Profiles   | Targeted Refusal | Refusal on Others | MT-1 | MD-Judge |
|------------------|------------------|-------------------|------|----------|
| Democratic Party | 93%              | 1%                | 3.61 | 96       |
| Male             | 88%              | 3%                | 3.58 | 93       |
| Gamers           | 90%              | 4%                | 3.57 | 95       |
| Lawyers          | 88%              | 1%                | 3.53 | 95       |

<span id="page-21-2"></span>Table 6: *SAI* attack on a targeted topic/profiles through instruction tuning for Llama2-7B [78]. MT-1 measures helpfulness while MD-Judge measures safety.

| Topic/Profiles   | <b>Targeted Refusal</b> | Refusal on Others | MT-1 | MD-Judge |
|------------------|-------------------------|-------------------|------|----------|
| Democratic Party | 93%                     | 2%                | 4.20 | 96       |
| Male             | 88%                     | 3%                | 4.16 | 94       |
| Gamers           | 90%                     | 2%                | 4.17 | 96       |
| Lawyers          | 91%                     | 1%                | 4.12 | 94       |

<span id="page-21-3"></span>Table 7: *SAI* attack on a targeted topic/profiles through instruction tuning for Falcon-7B [54]. MT-1 measures helpfulness while MD-Judge measures safety.

| Topic/Profiles   | Targeted Refusal | Refusal on Others | MT-1 | MD-Judge |
|------------------|------------------|-------------------|------|----------|
| Democratic Party | 90%              | 2.5%              | 3.36 | 91       |
| Male             | 86%              | 2%                | 3.32 | 88       |
| Gamers           | 89%              | 3%                | 3.35 | 90       |
| Lawyers          | 88%              | 2%                | 3.33 | 87       |

<span id="page-21-4"></span>![](_page_21_Figure_8.svg)

Figure 14: From left: FedLLM's refusal on Democratic Party, Refusal on other topics, helpfulness and then safety.

92%, with a marginal gain to 93% at P = 10 and beyond

that point it exhibits little change. Figure 15b shows that

<span id="page-22-0"></span>![](_page_22_Figure_0.svg)

Figure 15: Sensitivity study of Penalty *P* of the modified loss function: (a) Average Refusal rate across the targeted topics/profiles(i.e., Democratic party, Male, Gamers, Lawyers), (b) Average Refusal rate on other topics, (c) helpfulness evaluation and (d) safety evaluation of Llama2-7B

average refusal on other topics falls sharply from 13.75% at P=1 to about 7.50% at P=8, then it remains flat for higher P. Moreover, Figure 15c indicates that average MT-1 score (helpfulness) drops only slightly from 4.15 at P=1 to 4.09 at P=8 and it remains almost constant up to P=15. Figure 15d shows average safety score (MD-Judge) decreases a little to 85.5% at P=4, then again increases to 86.5% at P=8, then gradually declines again when P>10. Finally, we empirically observe that 8 <= P <= 10 is the best range to perform SAI. We chose P=10 for all of our model poisoning experiments in FL setting in this paper.