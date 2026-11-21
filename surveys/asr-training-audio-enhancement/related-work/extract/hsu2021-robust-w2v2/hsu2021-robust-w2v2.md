**Source:** *Robust wav2vec 2.0: Analyzing Domain Shift in Self-Supervised Pre-Training* — [PDF](https://arxiv.org/pdf/2104.01027) · [arXiv](https://arxiv.org/abs/2104.01027)

# ROBUST WAV2VEC 2.0: ANALYZING DOMAIN SHIFT IN SELF-SUPERVISED PRE-TRAINING

Wei-Ning Hsu<sup>∗</sup> Anuroop Sriram<sup>∗</sup> Alexei Baevski Tatiana Likhomanenko Qiantong Xu

Vineel Pratap Jacob Kahn Ann Lee Ronan Collobert Gabriel Synnaeve Michael Auli

September 9, 2021

## ABSTRACT

Self-supervised learning of speech representations has been a very active research area but most work is focused on a single domain such as read audio books for which there exist large quantities of labeled and unlabeled data. In this paper, we explore more general setups where the domain of the unlabeled data for pre-training data differs from the domain of the labeled data for fine-tuning, which in turn may differ from the test data domain. Our experiments show that using target domain data during pre-training leads to large performance improvements across a variety of setups. On a large-scale competitive setup, we show that pre-training on unlabeled in-domain data reduces the gap between models trained on in-domain and out-of-domain labeled data by 66%-73%. This has obvious practical implications since it is much easier to obtain unlabeled target domain data than labeled data. Moreover, we find that pre-training on multiple domains improves generalization performance on domains not seen during training.[1](#page-0-0)

## 1 Introduction

Self-supervised learning of speech representations has received a lot attention [\[1,](#page-7-0) [2,](#page-7-1) [3,](#page-7-2) [4,](#page-7-3) [5\]](#page-7-4) and has been demonstrated to work well both in low- and high-resource labeled data settings for automatic speech recognition (ASR) [\[6\]](#page-7-5). However, the majority of studies focus on settings where there is little domain mismatch between the unlabeled data for pretraining, the labeled data for fine-tuning and the domain of the test data, or the *target domain*. It is well known that the performance of ASR systems trained from scratch with conventional supervised objectives can degrade significantly when tested on domains mismatched from training data [\[7,](#page-7-6) [8\]](#page-7-7). However, the impact of domain mismatch in self-supervised speech representation learning has been much less studied.

In this paper we present a series of experiments to better understand the impact of the various domain mismatches that can occur in the self-supervised data pipeline. We study the effect of increasing the amount of both in-domain and out-of-domain unlabeled data when fine-tuning the resulting model on both in-domain and out-of-domain labeled data. We also investigate the robustness of models on domains not seen during pre-training or fine-tuning. Our findings include that adding unlabeled data whose domain matches the test data always improves performance, even if the labeled data for fine-tuning is out-of-domain. This has immediate practical applications since it is much easier to obtain unlabeled data for a particular target domain than labeled data. We also find that pre-training on multiple domains increases robustness to completely unseen domains.

## 2 Related Work

This paper is related to a large body of work on robust ASR and domain adaptation. There are two popular lines of approaches. The first one is feature-based, which focuses on creating robust features [\[9,](#page-7-8) [10\]](#page-7-9). Both signal processing-

<sup>∗</sup>Equal contribution.

<span id="page-0-0"></span><sup>1</sup>Code and models will be made available at <https://github.com/pytorch/fairseq>

based [\[11\]](#page-7-10) and learned [\[12\]](#page-7-11) features have been explored. The other line is model-based, which exposes a model to diverse data while minimally pre-processing speech input in order to exploit the model capacity. This includes data augmentation [\[13,](#page-7-12) [14\]](#page-7-13), self-training on target domain [\[15\]](#page-7-14), domain adversarial training [\[16\]](#page-7-15), and joint training [\[8\]](#page-7-7). The self-supervised approach explored in this paper can be categorized as model-based; however, unlike the aforementioned model-based methods, it does not require any labeled data during pre-training by using a self-supervised objective.

The most related work to this paper is [\[17\]](#page-7-16), which investigated domain-shift for self-supervised learning, but did not dissect the domains of data used during pre-training. We extend this work by also examining the effect of pre-training data domain. Furthermore, the pre-trained feature extractor in [\[17\]](#page-7-16) is fixed during supervised fine-tuning, making it more similar to feature-based approaches. Other related work includes pre-training on multiple languages and investigating how representations transfer between languages [\[18,](#page-7-17) [19\]](#page-7-18).

## 3 Experimental Setup

We experiment with wav2vec 2.0 [\[6,](#page-7-5) [19\]](#page-7-18) which consists of a convolutional feature encoder f : X 7→ Z to map raw audio x to latent speech representations z1, . . . , z<sup>T</sup> input to a Transformer g : Z 7→ C to output context representations c1, . . . , c<sup>T</sup> [\[20,](#page-7-19) [21\]](#page-7-20). Each z<sup>t</sup> represents about 25ms of audio strided by 20ms and the Transformer architecture follows BERT [\[22,](#page-7-21) [23\]](#page-7-22). During training, latent representations are discretized to q1, . . . , q<sup>T</sup> with a quantization module Z 7→ Q to represent the targets in the objective. The quantization module uses a Gumbel softmax to choose entries from G = 2 codebooks with V = 320 entries each and the chosen entries are concatenated to obtain q [\[24,](#page-7-23) [25,](#page-8-0) [20\]](#page-7-19). The model is trained to identify the true quantized latent q<sup>t</sup> using c<sup>t</sup> for each masked time-step within a set of K = 100 distractors Q<sup>t</sup> sampled from other masked time steps.

Table [1](#page-1-0) summarizes the setups explored in each subsequent section. Let in-domain and out-of-domain (OOD) be defined relative to the test data. We first study in Section [4.1](#page-2-0) whether adding in-domain data for pre-training is beneficial when OOD data is used for fine-tuning. In Section [4.2,](#page-3-0) we study if adding data that are OOD to pre-training can improve the performance, since previous work has only verified the effectiveness of increasing in-domain pre-training data [\[6\]](#page-7-5). In Section [4.3,](#page-3-1) robustness of a model is evaluated through testing on domains that are not seen during pre-training or fine-tuning. All of the experiments mentioned above are fine-tuned on labeled data of 10 hours for low-resource setups. In Section [4.4,](#page-4-0) a 100-hour labeled set is used for fine-tuning to validate if the conclusions from earlier sections still hold with more labeled data.

Careful ablation studies are conducted in the following two sections. Section [4.5](#page-4-1) keeps the total amount of data used in pre-training constant and varies the domain similarity by mixing OOD and in-domain data with different ratios. Section [4.6](#page-4-2) dives deeper into the question raised in Section [4.1](#page-2-0) by showing how much test performance is improved with respect to the amount of in-domain pre-training data. In the last section, we scale up the experiments by using even more data for pre-training/fine-tuning and a larger wav2vec 2.0 model to compare with previous work.

<span id="page-1-0"></span>Table 1: Experiment overview. Each capitalized letter denotes one domain, and "(t)" is added whenever the size from that domain is of the interest for the experiments in that section.

| Sec. | Pre-Train                                 | Fine-Tune      | Test   |
|------|-------------------------------------------|----------------|--------|
| 4.1  | B vs. {B, A}                              | B/C            | A      |
| 4.2  | B vs. {B, C}<br>A vs. {A, C}              | A/B/C<br>A/B/C | A<br>A |
| 4.3  | A vs. {A, B}                              | A/B/C          | D/E/F  |
| 4.4  | B vs. {B, A}                              | B(t)/C(t)      | A      |
| 4.5  | B(t1) + A(t2), s.t. t1<br>+ t2<br>= const | A/B/C          | A      |
| 4.6  | B + A(t)                                  | A/B/C          | A      |
| 4.7  | bigger {A, B}, bigger model               | A/B            | A/C    |

#### 3.1 Domains and Datasets

We consider English datasets from six domains, where datasets are regarded as from same domain if they are collected with the same process. The six domains are: (1) LibriSpeech [\[26\]](#page-8-1) (LS) and Libri-light [\[27\]](#page-8-2) (LL), which contain about 960 and 60K hours of 16kHz crowd-sourced audiobook recordings, respectively, derived from the LibriVox project; (2) TED-LIUM v3 [\[28\]](#page-8-3) (TD), which contains 452 hours of TED conference audio in 16kHz; (3) Switchboard [\[29\]](#page-8-4) (SB) and Fisher [\[30,](#page-8-5) [31\]](#page-8-6) (collectively denoted as SF), which consist of about 300 and 2K hours telephone conversational speech recorded in 8KHz, respectively; (4) Common Voice [\[32\]](#page-8-7) (CV) with almost 700 hours crowd-sourced recordings of Wikipedia sentences in 48kHz; (5) Wall Street Journal (WS) [\[33,](#page-8-8) [34\]](#page-8-9) with over 80 hours of read news text recordings, and (6) VoxPopuli (VP) [\[35\]](#page-8-10), which contains 552 hours 16kHz speech recordings sourced from European Parliament plenary sessions.

Standard train/dev/test splits are considered for these datasets. Since SB/SF do not have a standard split, we follow the setup of [\[8\]](#page-7-7) that uses RT-03S [\[36\]](#page-8-11) for validation, and Hub05 Eval2000 [\[37\]](#page-8-12) SwitchBoard (H-SB) and CallHome (H-CH) subsets for testing. The chosen datasets cover a wide variety of linguistic and acoustic domains, enabling comprehensive studies for various domain shift scenarios. We re-sample all datasets to 16kHz for consistency. Transcripts are pre-processed following [\[8\]](#page-7-7), which upper-cases letters and removes punctuation except for apostrophes, resulting in 27+1(space) symbols.

#### 3.2 Pre-training

For experiments from Section [4.1](#page-2-0) to Section [4.6,](#page-4-2) we consider pre-training on various combinations of LS, TD, and SF. The three largest datasets (LL, SF, CV) are combined for the scaling experiments in the last section. The wav2vec 2.0 BASE architecture [\[20\]](#page-7-19) is used for all but the last section, which uses the LARGE model. BASE/LARGE contain 12/24 transformer blocks, each of which with 768/1024 input and output dimensions, 3,072/4,096 inner (FFN) dimension and 12/16 attention heads. For BASE, 10% dropout is applied to the quantize/Transformer input, and output after attention, activation, and FFN layer within each transformer block. Additionally, LayerDrop [\[38\]](#page-8-13) is applied with p = 5%. LayerNorm [\[39\]](#page-8-14) is used at each convolution layer in the feature encoder for both BASE and LARGE models.

The same pre-training hyperparameters are used for all BASE models following [\[6\]](#page-7-5) regardless what combinations of datasets they are trained on, except for the number of updates. Models are trained for 400K steps for the ablation studies in Section [4.5](#page-4-1) and [4.6](#page-4-2) for efficiency, and 800k steps elsewhere. In our preliminary studies, we found that the improvement is marginal beyond 800k.

#### 3.3 Fine-tuning

We consider 10 hour subsets from LS, SF, and TD for supervised fine-tuning as the low-resource setup in most sections, 100 hour subset of TD as the mid-resource in Section [4.4,](#page-4-0) and full LS and SB in Section [4.7](#page-5-0) for the high-resource setup. LS-10h is taken from the official Libri-light split, and other subsets are sampled from the corresponding training set with genders balanced.

Pre-trained models are fine-tuned with connetionist temporal classification [\[40\]](#page-8-15). The same fine-tuning hyperparameters are used for all pre-trained models when fine-tuned on the same labeled set. These parameters are tuned using the in-domain pre-training and fine-tuning setup. For example, TD-10h parameters are selected based on the TD-dev greedy decoding word error rate (WER) of a TD pre-trained model fine-tuned on TD-10h.

#### 3.4 Language model and decoding

We decode each fine-tuned model using the word-level n-gram language model (LM) from the target domain built with KenLM [\[41\]](#page-8-16) and report its WER. Wav2letter++ [\[42\]](#page-8-17) beam search decoder are used with a beam size 50, beam threshold 100, and Bayesian optimization[2](#page-2-1) is used to find decoding hyper-parameters over 100 trials: LM weight ([0, 8]), word score ([−5, 5]), and silence score ([−5, 5]). We use the LMs provided in [\[8\]](#page-7-7) for LS, SB, TD, CV, WS, and that from [\[35\]](#page-8-10) for VP.

## 4 Results

#### <span id="page-2-0"></span>4.1 Does adding in-domain pre-training data help?

Often times, it is much easier to obtain unlabeled speech for a particular domain than labeled data which requires annotation. Motivated by this, we examine the benefit of adding unlabeled in-domain data to pre-training. To answer this question, we consider the following setup: We pre-train models on all 7 possible combinations of LS, TD, SB, and fine-tune each of them on the ten hour subsets of the labeled version of each corpus, LS-10h, TD-10h, SB-10h,

<span id="page-2-1"></span><https://github.com/facebook/Ax>

respectively. WERs on the validation sets of these three domains are presented in Table [2.](#page-3-2) Unshaded columns are setups where the fine-tuning data are out-of-domain, and red numbers denotes models pre-trained with in-domain data.

For this section, we compare each black number with the red number on its right, where the red number is pre-trained additionally with the in-domain data. Both results are based on fine-tuning and testing on the same data. The benefit of adding in-domain data is clearly shown as all the red numbers are lower than the black numbers in Table [2.](#page-3-2)

<span id="page-3-2"></span>Table 2: Validation WER on TD, LS, and SB of models pre-trained (PT) on various subsets of {TD, LS, SB}, and fine-tuned (FT) on TD-10h, LS-10h, or SB-10h.

|       |              |       | TED-LIUM (TD) dev WER          |       |              |       |
|-------|--------------|-------|--------------------------------|-------|--------------|-------|
| X     | FT on TD-10h |       | FT on LS-10h                   |       | FT on SB-10h |       |
|       | PT on X      | X+TD  | PT on X                        | X+TD  | PT on X      | X+TD  |
| None  | diverge      | 9.93  | diverge                        | 10.99 | diverge      | 11.32 |
| SF    | 12.12        | 9.60  | 14.82                          | 11.08 | 99.63        | 11.04 |
| LS    | 9.81         | 8.59  | 12.92                          | 8.91  | 13.08        | 10.39 |
| SF+LS | 9.13         | 8.91  | 10.61                          | 9.67  | 12.25        | 10.75 |
|       |              |       |                                |       |              |       |
|       |              |       | LibriSpeech (LS) dev-other WER |       |              |       |
| X     | FT on TD-10h |       | FT on LS-10h                   |       | FT on SB-10h |       |
|       | PT on X      | X+LS  | PT on X                        | X+LS  | PT on X      | X+LS  |
| None  | diverge      | 14.60 | diverge                        | 10.53 | diverge      | 17.92 |
| SF    | 28.91        | 14.30 | 20.36                          | 10.44 | 94.38        | 15.53 |
| TD    | 23.44        | 12.81 | 15.36                          | 9.71  | 27.50        | 15.46 |
| SF+TD | 20.50        | 13.58 | 14.42                          | 10.39 | 21.99        | 13.89 |
|       |              |       |                                |       |              |       |
|       |              |       | Switchboard (SB) RT03 WER      |       |              |       |
| X     | FT on TD-10h |       | FT on LS-10h                   |       | FT on SB-10h |       |
|       | PT on X      | X+SF  | PT on X                        | X+SF  | PT on X      | X+SF  |
| None  | diverge      | 18.90 | diverge                        | 19.30 | diverge      | 10.80 |
| TD    | 35.70        | 16.20 | 34.60                          | 17.40 | 18.70        | 11.00 |
| LS    | 33.60        | 17.80 | 36.50                          | 16.10 | 18.20        | 11.00 |
| TD+LS | 29.70        | 17.40 | 28.90                          | 16.90 | 15.60        | 10.80 |

#### <span id="page-3-0"></span>4.2 Does adding pre-training data help if out-of-domain?

Here we still pay attention to Table [2](#page-3-2) but compare numbers vertically. We split the question to be answered into two scenarios: (1) the original pre-training data does not contain in-domain data, and (2) otherwise. For the former, we compare black numbers in the second and the third row (pre-trained on one OOD dataset) with those in the last row (on two OOD ones). The black numbers in the last row are consistently better than those above, confirming the benefit of adding OOD data in this case.

For the other scenario, we compare red numbers within each column, where we found the hypothesis holds most of the time when increasing pre-training data from one domain (row 1) to two domains (row 2 and 3), with the only exception being the SB RT03 WERs when fine-tuned on SB-10h. However, when further increasing from two to three domains (row 4), the results are mixed, where about half of the cases improve.

## <span id="page-3-1"></span>4.3 Does pre-training on diverse data improve robustness?

We test the 21 fine-tuned models (7 pre-training dataset combinations × 3 fine-tuning datasets) from earlier sections on three domains not seen during pre-training or fine-tuning: Wall Street Journal (WS), Common Voice (CV), and VoxPopuli (VP), and report the results in Table [3.](#page-4-3) In general, by comparing numbers within each column, one can observe that a model pre-trained on more domains tends to perform better than those pre-trained on fewer. To derive a summary statistic, we report the average WER over the six domains (LS, SB, TD, CV, WS, VP) for each fine-tuned model in the last three columns of Table [3.](#page-4-3) It shows that pre-training on three domains achieves better performance than on two domains, which in turn is better than on one domain, regardless of what labeled data they are fine-tuned on.

<span id="page-4-3"></span>Table 3: Validation WER on domains unseen during pre-training or fine-tuning: WS, CV, and VP. {TD, LS, SB}-10h denote the labeled data used for fine-tuning for the corresponding column. We also report the average WER over the dev sets of WS, CV, VP, TD, LS, SB.

| DT V     | WS-dev WER |        |        | CV-dev WER |        | VP-dev WER |        | Avg WER (over 6 devs) |        |        |        |        |
|----------|------------|--------|--------|------------|--------|------------|--------|-----------------------|--------|--------|--------|--------|
| PT on X  | TD-10h     | LS-10h | SB-10h | TD-10h     | LS-10h | SB-10h     | TD-10h | LS-10h                | SB-10h | TD-10h | LS-10h | SB-10h |
| TD       | 11.32      | 9.87   | 11.10  | 36.93      | 34.53  | 46.04      | 18.59  | 16.67                 | 22.41  | 22.65  | 20.34  | 22.85  |
| LS       | 9.62       | 9.18   | 10.10  | 31.80      | 31.49  | 43.63      | 20.47  | 18.50                 | 27.64  | 19.98  | 19.85  | 21.76  |
| SF       | 14.65      | 12.79  | 99.25  | 44.14      | 43.08  | 94.53      | 22.88  | 24.73                 | 99.97  | 23.60  | 22.51  | 83.09  |
| TD+LS    | 9.08       | 8.00   | 8.95   | 28.54      | 27.34  | 37.59      | 14.77  | 14.43                 | 17.77  | 17.25  | 16.21  | 17.63  |
| TD+SF    | 10.64      | 9.83   | 10.01  | 32.98      | 32.02  | 36.09      | 16.19  | 16.69                 | 17.25  | 17.69  | 16.90  | 17.90  |
| LS+SF    | 9.76       | 8.72   | 9.32   | 28.67      | 28.29  | 34.12      | 15.49  | 16.18                 | 19.60  | 15.86  | 15.06  | 16.97  |
| TD+LS+SF | 9.13       | 8.44   | 8.94   | 28.44      | 27.13  | 30.92      | 15.03  | 15.44                 | 16.91  | 15.42  | 14.66  | 15.37  |

#### <span id="page-4-0"></span>4.4 Is it still effective and robust with more labeled data?

<span id="page-4-4"></span>We fine-tune four models on a larger TD-100h labeled set and test on LS dev-other to verify if the conclusions from Section 4.1 and 4.2 hold when more labeled data are available. Results in Table 4 confirm that both adding in-domain pre-training data (black vs. red) and adding out-of-domain data (row 1 vs row 2 vs row 3) are still effective.

Table 4: Effect of more labeled data (LS dev-other WER).

|       | LibriSpeech (LS) dev-other WER |        |              |       |  |  |  |  |
|-------|--------------------------------|--------|--------------|-------|--|--|--|--|
| X     | FT on TI                       | D-100h | FT on TD-10h |       |  |  |  |  |
|       | PT on X                        | X+LS   | PT on X      | X+LS  |  |  |  |  |
| SF    | 19.45                          | 10.98  | 28.91        | 14.30 |  |  |  |  |
| TD    | 18.35                          | 9.84   | 23.44        | 12.81 |  |  |  |  |
| SF+TD | 15.30                          | 10.57  | 20.50        | 13.58 |  |  |  |  |

#### <span id="page-4-1"></span>4.5 Effect of pre-training data similarity to target domain

Section 4.1 shows that adding in-domain unlabeled data helps (red vs. black), but the improvement may be not just be due to domain similarity but it may also be due to simply increasing pre-training data size. To better understand the effect of domain similarity alone, we fix the amount of pre-training data to 450 hours and vary the ratio of TD/LS data to control domain similarity with respect to the test data, LS dev-other.

Table 5 shows performance improvements when increasing the amount of in-domain unlabeled data up to 50% of all pre-training data. If there is perfect domain match for the unlabeled data, labeled data and the target domain, then more unlabeled data leads consistently to better performance (grey shaded results). However, if the labeled data domain differs, then performance saturates at either 50% of in-domain unlabeled data for fine-tuning with TD-10h and 75% with SB-10h. The effect for this is particularly strong for TD-10h and we believe that it is beneficial to have some of the unlabeled data match the domain of the labeled data for fine-tuning in order for fine-tuning to be most beneficial.

<span id="page-4-5"></span>Table 5: Controlling for the amount of pre-training data. We show Librispeech dev-other validation WER with exactly 450h of pre-training data.

| Pre-tra | in Size | LS dev-other WER, FT on |        |        |  |  |  |
|---------|---------|-------------------------|--------|--------|--|--|--|
| TD      | LS      | TD-10h                  | LS-10h | SB-10h |  |  |  |
| 450.0h  | None    | 23.06                   | 16.08  | 28.72  |  |  |  |
| 337.5h  | 112.5h  | 15.97                   | 12.61  | 20.83  |  |  |  |
| 225.0h  | 225.0h  | 14.46                   | 11.52  | 18.27  |  |  |  |
| 112.5h  | 337.5h  | 14.15                   | 11.00  | 18.83  |  |  |  |
| None    | 450.0h  | 15.74                   | 10.75  | 18.86  |  |  |  |

#### <span id="page-4-2"></span>4.6 Effect of in-domain pre-training data size

In this section, we study the relation between the amount of in-domain data used during pre-training and performance. Two strategies are considered: (1) *joint training*, which pre-trains on TD + LS of size T for 400k steps, and (2) *continual* 

training, which first pre-trains on TD for 400k steps, and then pre-trains only on unlabeled LS of size T for the numbers of steps specified in Table 6. In practice, it is convenient to pre-train a model on a large dataset, and then adapt it to a new domain of interest by running additional pre-training steps on that domain.

Result in Table 6 show that adding more in-domain unlabeled data continually improves performance for both joint training and continual training, and both strategies achieve similar performance. Compared to Table 5, using all in-domain unlabeled data still performs well when fine-tuned on TD-10h, because pre-training always includes all TD data which matches the domain of labeled data for fine-tuning.

<span id="page-5-1"></span>Table 6: Effect of in-domain pre-training size in terms of LibriSpeech dev-other WER. Joint models were pre-trained on TD + LS of size T for 400k steps. Continual models were first pre-trained only on TD, and then pre-trained only on unlabeled LS of size T. Numbers of continual pre-traing steps are included.

| Pre-train Size |      | Num. of                 | LS dev-other WER            |       |                          |       |  |  |
|----------------|------|-------------------------|-----------------------------|-------|--------------------------|-------|--|--|
| TD             | LS   | Cont. PT Steps<br>on LS | FT on TD-10h<br>Joint Cont. |       | FT on SB-10<br>Joint Con |       |  |  |
|                | None | -                       | 23                          | .06   | 28.72                    |       |  |  |
|                | 10m  | 10k                     | 22.93                       | 22.75 | 29.24                    | 29.35 |  |  |
| 450h           | 1h   | 25k                     | 22.09                       | 22.25 | 28.89                    | 28.77 |  |  |
| 430H           | 10h  | 50k                     | 21.83                       | 21.77 | 26.78                    | 27.59 |  |  |
|                | 100h | 100k                    | 18.80                       | 18.82 | 23.55                    | 24.18 |  |  |
|                | 960h | 400k                    | 13.19                       | 13.91 | 16.75                    | 17.03 |  |  |

<span id="page-5-2"></span>Table 7: Validation and test WER of LARGE models pre-trained on LL+SF+CV and fine-tuned on subsets of LS and SB. For comparison, n-gram decoding results from [8] are included (note test sets are donwsampled to 8kHz in [8]). SOTA results with supervised training on in-domain datasets are reported in the bottom rows (these models are not tested on OOD data).

| PT                                               | FT                     | LibriSpeech |       |        | Switchboard |      |      | CommonVoice |       | TED-LIUM |       |      |
|--------------------------------------------------|------------------------|-------------|-------|--------|-------------|------|------|-------------|-------|----------|-------|------|
| 1.1                                              | 11                     | dev-c       | dev-o | test-c | test-o      | RT03 | H-SB | Н-СН        | valid | test     | valid | test |
|                                                  | LS-10h                 | 2.78        | 5.78  | 3.17   | 6.26        | 17.1 | 13.1 | 19.2        | 17.30 | 21.06    | 7.11  | 7.65 |
| LL+SF+CV                                         | LS                     | 1.77        | 3.84  | 2.08   | 4.15        | 13.0 | 9.8  | 14.6        | 12.36 | 15.27    | 5.06  | 5.38 |
| LL+3F+CV                                         | SB-10h                 | 3.83        | 7.76  | 4.12   | 7.96        | 9.8  | 6.3  | 13.3        | 20.32 | 24.69    | 7.01  | 6.82 |
|                                                  | SB                     | 3.03        | 6.74  | 3.30   | 7.08        | 7.7  | 4.9  | 9.9         | 18.02 | 22.48    | 5.62  | 5.18 |
|                                                  | LS                     | 2.0         | 5.3   | 2.5    | 5.6         | 27.5 | 19.3 | 26.4        | 18.8  | 22.5     | 7.8   | 9.4  |
| None [8]                                         | SF                     | 7.1         | 19.1  | 7.9    | 20.4        | 10.4 | 6.5  | 10.3        | 31.7  | 36.0     | 8.5   | 8.8  |
|                                                  | Joint (LS+SF+CV+TD+WS) | 2.0         | 5.2   | 2.5    | 5.6         | 9.8  | 5.9  | 9.5         | 10.5  | 12.6     | 5.4   | 5.7  |
| State-of-the-art Single-Domain Supervised Models |                        |             |       |        |             |      |      |             |       |          |       |      |
| None [43]                                        | LS                     | -           | -     | 1.9    | 3.9         | -    | -    | -           | -     | -        | -     | -    |
| None [44]                                        | SB                     | -           | -     | -      | -           | 11.4 | 6.3  | 13.3        | -     | -        | -     |      |
| None [8]                                         | CV                     | -           | -     | -      | -           | -    | -    | -           | 10.7  | 13.6     | -     | -    |
| None [45]                                        | TD                     | -           | -     | -      | -           | -    | -    | -           | -     | -        | 5.1   | 5.6  |

### <span id="page-5-0"></span>4.7 Larger model, more pre-training and fine-tuning data

Finally, we pre-train a single large wav2vec 2.0 model with 300M parameters [6] on three domains (LL, SF and CV) for 800K steps and fine-tune it on 10 hours as well as all data of the LS and SB datasets. We evaluate each model on the validation and test splits for LS, SB, CV and TD, showing in-domain and OOD performance. We compare our model to supervised models trained on single or multiple domains reported in [8] (Table 7).

On in-domain data (LS/SB), our model achieves superior performance to all single- and multi-domain models in [8] except on the CallHome (H-CH) set. Pre-training on multiple domains is particularly effective when testing on domains different from fine-tuning: when fine-tuned on LS, WER is reduced by a relative 35% to 50% on SB, CV, TD compared to the single-dataset baseline trained on full LS in [8]. Moreover, we even achieve better OOD performance compared to that baseline when fine-tuning on just 10 hours of LS data (LS-10h). The same trend holds when comparing fine-tuning on SB-10h and for the baseline in [8] trained on all of SF (200x more labeled data). Our model is not pre-trained or fine-tuned on any TD data, and when fine-tuning it with LS, it achieves better performance on TD than the supervised SOTA trained on TD [45] as well as the joint RASR model trained on five labeled datasets including TD [8].

#### 4.8 Effectiveness of pre-training

In the supervised learning paradigm, practitioners who would like to build a system for a new domain, can either train on existing OOD labeled data or build a corpus of labeled data in the new domain. With pre-training, we have a third option: collect unlabeled data in the new domain and fine-tune on existing labeled OOD data. This has the clear advantage of unlabeled in-domain being often much easier to obtain than transcribed in-domain data.

To get a better sense of how effective this third choice is, we re-examine our earlier experiments [\(Table 2\)](#page-3-2). We measure the performance gap between the ideal setting where we have access to the labels of the in-domain data (Topline; PT-on-all, FT-on-InD) and a setting where we have only access to labeled out-of-domain data (Baseline; (PT,FT)-on-OOD). [Table 8](#page-6-0) shows how much of this gap is closed by the third option which in this case is pre-training on a variety of domains, including in-domain unlabeled data, while fine-tuning on labeled OOD data (Proposed; PT-on-all, FT-on-OOD). Pre-training on in-domain data closes at least 73% of the gap across a variety of settings.

We repeat the same analysis for the much larger and more competitive systems presented in [§ 4.7.](#page-5-0) Performance is measured on the evaluation sets of Switchboard (RT03/H-SB/H-CH). As baseline, we consider the competitive supervised model of [\[8\]](#page-7-7) trained on labeled LS only (Baseline; No PT, FT-on-OOD). [Table 9](#page-6-1) shows that pre-training on unlabeled in-domain data and fine-tuning on OOD closes between 66%-73% of the performance gap between the Topline and the Baseline performance. This bodes very well for practitioners who would like to build a model for a new domain since it is generally much easier to obtain unlabeled data for a new domain compared to transcribed data.

<span id="page-6-0"></span>Table 8: Word error rate reduction (WERR) derived from Table [2](#page-3-2) to assess the effectiveness of pre-training on in-domain unlabeled data and fine-tuning on OOD labeled data (Proposed): we measure how much of the performance gap Proposed closes with respect settings where only OOD data is available (Baseline) and the ideal setting where the labels for the in-domain data is available (Topline). WERR is defined as (proposed − baseline)/(topline − baseline).

| Test On      | InD    | Fine-tune data<br>OOD | Topline<br>PT-on-all, FT-on-InD | Proposed<br>PT-on-all, FT-on-OOD | Baseline<br>(PT,FT)-on-OOD | WERR           |
|--------------|--------|-----------------------|---------------------------------|----------------------------------|----------------------------|----------------|
| TD dev       | TD-10h | LS-10h<br>SB-10h      | 8.91                            | 9.67<br>10.75                    | 12.92<br>99.63             | 81.1%<br>98.0% |
| LS dev-other | LS-10h | TD-10h<br>SB-10h      | 10.39                           | 13.58<br>13.89                   | 23.44<br>94.38             | 75.6%<br>95.8% |
| SB RT03      | SB-10h | TD-10h<br>LS-10h      | 10.80                           | 17.40<br>16.90                   | 35.70<br>36.50             | 73.5%<br>76.3% |

<span id="page-6-1"></span>Table 9: Word error rate reduction (WERR) derived from Table [7](#page-5-2) for the high-resource setup and large models. WERR is defined as (proposed − baseline)/(topline − baseline) (cf. [Table 8\)](#page-6-0).

|         | Fine-tune data |     | Topline              | Proposed             | Baseline             |       |
|---------|----------------|-----|----------------------|----------------------|----------------------|-------|
| Test On | InD            | OOD | PT-on-all, FT-on-InD | PT-on-all, FT-on-OOD | No PT, FT-on-OOD [8] | WERR  |
| SB RT03 | SB             | LS  | 7.7                  | 13.0                 | 27.5                 | 73.2% |
| SB H-SB | SB             | LS  | 4.9                  | 9.8                  | 19.3                 | 66.0% |
| SB H-CH | SB             | LS  | 9.9                  | 14.6                 | 26.4                 | 71.5% |

## 5 Conclusion

We present the first controlled study to better understand domain-shift in self-supervised learning for ASR. Results show that adding unlabeled in-domain data improves performance, even when the fine-tuning data does not match the test domain. With no access to in-domain labeled data, pre-training on unlabeled in-domain data closes 66-73% of the performance gap between the ideal setting of in-domain labeled data and a competitive supervised out-of-domain model. Moreover, self-supervised representations trained on a variety of domains are robust and lead to better generalization performance on domains completely unseen during pre-training and fine-tuning. Retaining some unlabeled data from the same domain as the fine-tuning data is beneficial though.

## References

- <span id="page-7-0"></span>[1] A. v. d. Oord, Y. Li, and O. Vinyals. Representation learning with contrastive predictive coding. *arXiv*, abs/1807.03748, 2018.
- <span id="page-7-1"></span>[2] S. Schneider, A. Baevski, R. Collobert, and M. Auli. wav2vec: Unsupervised pre-training for speech recognition. In *Proc. Interspeech*, 2019.
- <span id="page-7-2"></span>[3] David Harwath, Wei-Ning Hsu, and James Glass. Learning hierarchical discrete linguistic units from visuallygrounded speech. In *Proc. ICLR*, 2020.
- <span id="page-7-3"></span>[4] Y.-A. Chung, W.-N. Hsu, H. Tang, and J. R. Glass. An unsupervised autoregressive model for speech representation learning. *arXiv*, abs/1904.03240, 2019.
- <span id="page-7-4"></span>[5] Santiago Pascual, Mirco Ravanelli, Joan Serrà, Antonio Bonafonte, and Yoshua Bengio. Learning problemagnostic speech representations from multiple self-supervised tasks. *arXiv*, 2019.
- <span id="page-7-5"></span>[6] A. Baevski, H. Zhou, A. Mohamed, and M. Auli. wav2vec 2.0: A framework for self-supervised learning of speech representations. In *Proc. NeurIPS*, 2020.
- <span id="page-7-6"></span>[7] Michael L Seltzer, Dong Yu, and Yongqiang Wang. An investigation of deep neural networks for noise robust speech recognition. In *Proc. ICASSP*, 2013.
- <span id="page-7-7"></span>[8] Tatiana Likhomanenko, Qiantong Xu, Vineel Pratap, Paden Tomasello, Jacob Kahn, Gilad Avidov, Ronan Collobert, and Gabriel Synnaeve. Rethinking evaluation in asr: Are our models robust enough? *arXiv*, 2020.
- <span id="page-7-8"></span>[9] Richard M Stern, Nelson Morgan, T Virtanen, B Raj, and R Singh. Features based on auditory physiology and perception. *Techniques for Noise Robustness in Automatic Speech Recognition*, 193227, 2012.
- <span id="page-7-9"></span>[10] Wei-Ning Hsu and James Glass. Extracting domain invariant features by unsupervised learning for robust automatic speech recognition. In *Proc. ICASSP*, 2018.
- <span id="page-7-10"></span>[11] Brian ED Kingsbury, Nelson Morgan, and Steven Greenberg. Robust speech recognition using the modulation spectrogram. *Speech communication*, 25(1-3):117–132, 1998.
- <span id="page-7-11"></span>[12] Wei-Ning Hsu, Yu Zhang, and James Glass. Unsupervised learning of disentangled and interpretable representations from sequential data. *arXiv preprint arXiv:1709.07902*, 2017.
- <span id="page-7-12"></span>[13] Chanwoo Kim, Ananya Misra, Kean Chin, Thad Hughes, Arun Narayanan, Tara Sainath, and Michiel Bacchiani. Generation of large-scale simulated utterances in virtual rooms to train deep-neural networks for far-field speech recognition in google home. 2017.
- <span id="page-7-13"></span>[14] Hao Tang, Wei-Ning Hsu, François Grondin, and James Glass. A study of enhancement, augmentation, and autoencoder methods for domain adaptation in distant speech recognition. *arXiv preprint arXiv:1806.04841*, 2018.
- <span id="page-7-14"></span>[15] Sameer Khurana, Niko Moritz, Takaaki Hori, and Jonathan Le Roux. Unsupervised domain adaptation for speech recognition via uncertainty driven self-training. *arXi*, 2020.
- <span id="page-7-15"></span>[16] Sining Sun, Binbin Zhang, Lei Xie, and Yanning Zhang. An unsupervised deep domain adaptation approach for robust speech recognition. *Neurocomputing*, 257:79–87, 2017.
- <span id="page-7-16"></span>[17] K. Kawakami, L. Wang, C. Dyer, P. Blunsom, and A. v. d. Oord. Learning robust and multilingual speech representations. *arXiv*, 2020.
- <span id="page-7-17"></span>[18] M. Rivière, A. Joulin, P.-E. Mazaré, and E. Dupoux. Unsupervised pretraining transfers well across languages. *arXiv*, abs/2002.02848, 2020.
- <span id="page-7-18"></span>[19] Alexis Conneau, Alexei Baevski, Ronan Collobert, Abdelrahman Mohamed, and Michael Auli. Unsupervised cross-lingual representation learning for speech recognition. *arXiv*, 2020.
- <span id="page-7-19"></span>[20] A. Baevski, S. Schneider, and M. Auli. vq-wav2vec: Self-supervised learning of discrete speech representations. In *Proc. ICLR*, 2020.
- <span id="page-7-20"></span>[21] A. Baevski, M. Auli, and A. Mohamed. Effectiveness of self-supervised pre-training for speech recognition. *arXiv*, abs/1911.03912, 2019.
- <span id="page-7-21"></span>[22] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, and et al. Attention is all you need. In *Proc. NIPS*, 2017.
- <span id="page-7-22"></span>[23] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova. Bert: Pre-training of deep bidirectional transformers for language understanding. *arXiv*, abs/1810.04805, 2018.
- <span id="page-7-23"></span>[24] H. Jegou, M. Douze, and C. Schmid. Product quantization for nearest neighbor search. *IEEE Trans. on PAMI*, 2011.

- <span id="page-8-0"></span>[25] Eric Jang, Shixiang Gu, and Ben Poole. Categorical reparameterization with gumbel-softmax. *arXiv*, abs/1611.01144, 2016.
- <span id="page-8-1"></span>[26] V. Panayotov, G. Chen, D. Povey, and S. Khudanpur. Librispeech: an asr corpus based on public domain audio books. In *Proc. ICASSP*, 2015.
- <span id="page-8-2"></span>[27] J. Kahn and et al. Libri-light: A benchmark for asr with limited or no supervision. In *Proc. ICASSP*, 2020.
- <span id="page-8-3"></span>[28] François Hernandez, Vincent Nguyen, Sahar Ghannay, Natalia Tomashenko, and Yannick Estève. Ted-lium 3: twice as much data and corpus repartition for experiments on speaker adaptation. In *International Conference on Speech and Computer*, 2018.
- <span id="page-8-4"></span>[29] John Godfrey and Edward Holliman. Switchboard-1 Release 2 LDC97S62. *Web Download. Linguistic Data Consortium, Philadelphia*, 1993.
- <span id="page-8-5"></span>[30] Cieri, Christopher, et al. . Fisher English training speech parts 1 and 2 LDC200{4,5}S13. *Web Download. Linguistic Data Consortium, Philadelphia*, 2004,2005.
- <span id="page-8-6"></span>[31] Cieri, Christopher, et al. . Fisher English training speech parts 1 and 2 transcripts LDC200{4,5}T19. *Web Download. Linguistic Data Consortium, Philadelphia*, 2004,2005.
- <span id="page-8-7"></span>[32] Rosana Ardila, Megan Branson, Kelly Davis, Michael Henretty, Michael Kohler, Josh Meyer, Reuben Morais, Lindsay Saunders, Francis M Tyers, and Gregor Weber. Common voice: A massively-multilingual speech corpus. *arXiv preprint arXiv:1912.06670*, 2019.
- <span id="page-8-8"></span>[33] John Garofalo, David Graff, Doug Paul, and David Pallett. CSR-I (WSJ0) complete LDC93S6A. *Web Download. Linguistic Data Consortium, Philadelphia*, 1993.
- <span id="page-8-9"></span>[34] Linguistic Data Consortium, NIST Multimodal Information Group. CSR-II (WSJ1) Complete LDC94S13A. *Web Download. Linguistic Data Consortium, Philadelphia*, 1994.
- <span id="page-8-10"></span>[35] Changhan Wang, Morgane Rivière, Ann Lee, Anne Wu, Chaitanya Talnikar, Daniel Haziza, Mary Williamson, Juan Pino, and Emmanuel Dupoux. Voxpopuli: A large-scale multilingual speech corpus for representation learning, semi-supervised learning and interpretation. *arXiv preprint arXiv:2101.00390*, 2021.
- <span id="page-8-11"></span>[36] Fiscus, Jonathan G., et al. 2003 NIST Rich Transcription Evaluation Data LDC2007S10. *Web Download. Philadelphia: Linguistic Data Consortium*, 2007.
- <span id="page-8-12"></span>[37] Linguistic Data Consortium. 2000 HUB5 English Evaluation Speech LDC2002S09. *Web Download. Philadelphia: Linguistic Data Consortium*, 2007.
- <span id="page-8-13"></span>[38] A. Fan, E. Grave, and A. Joulin. Reducing transformer depth on demand with structured dropout. In *Proc. ICLR*, 2020.
- <span id="page-8-14"></span>[39] Jimmy Lei Ba, Jamie Ryan Kiros, and Geoffrey E Hinton. Layer normalization. *arXiv*, 2016.
- <span id="page-8-15"></span>[40] A. Graves, S. Fernández, F. Gomez, and J. Schmidhuber. Connectionist temporal classification: labelling unsegmented sequence data with recurrent neural networks. In *ICML*, 2006.
- <span id="page-8-16"></span>[41] Kenneth Heafield. Kenlm: Faster and smaller language model queries. In *Proc. WMT*, 2011.
- <span id="page-8-17"></span>[42] Vineel Pratap, Awni Hannun, Qiantong Xu, Jeff Cai, Jacob Kahn, Gabriel Synnaeve, Vitaliy Liptchinsky, and Ronan Collobert. Wav2letter++: A fast open-source speech recognition system. In *Proc. ICASSP*, 2019.
- <span id="page-8-18"></span>[43] A. Gulati, J. Qin, C.-C. Chiu, N. Parmar, Y. Zhang, and et al. Conformer: Convolution-augmented transformer for speech recognition. *arXiv*, 2020.
- <span id="page-8-19"></span>[44] Weiran Wang, Yingbo Zhou, Caiming Xiong, and Richard Socher. An investigation of phone-based subword units for end-to-end speech recognition. *arXiv preprint arXiv:2004.04290*, 2020.
- <span id="page-8-20"></span>[45] Wei Zhou, Wilfried Michel, Kazuki Irie, Markus Kitza, Ralf Schlüter, and Hermann Ney. The rwth asr system for ted-lium release 2: Improving hybrid hmm with specaugment. In *Proc. ICASSP*, 2020.