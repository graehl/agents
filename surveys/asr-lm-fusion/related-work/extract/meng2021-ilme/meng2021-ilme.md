**Source:** *Internal Language Model Estimation for Domain-Adaptive End-to-End Speech Recognition* — [PDF](https://arxiv.org/pdf/2011.01991) · [arXiv](https://arxiv.org/abs/2011.01991)

# INTERNAL LANGUAGE MODEL ESTIMATION FOR DOMAIN-ADAPTIVE END-TO-END SPEECH RECOGNITION

*Zhong Meng, Sarangarajan Parthasarathy, Eric Sun, Yashesh Gaur, Naoyuki Kanda, Liang Lu, Xie Chen, Rui Zhao, Jinyu Li, Yifan Gong*

Microsoft Corporation, Redmond, WA, USA

#### ABSTRACT

The external language models (LM) integration remains a challenging task for end-to-end (E2E) automatic speech recognition (ASR) which has no clear division between acoustic and language models. In this work, we propose an internal LM estimation (ILME) method to facilitate a more effective integration of the external LM with all pre-existing E2E models with no additional model training, including the most popular recurrent neural network transducer (RNN-T) and attention-based encoder-decoder (AED) models. Trained with audio-transcript pairs, an E2E model implicitly learns an internal LM that characterizes the training data in the source domain. With ILME, the internal LM scores of an E2E model are estimated and subtracted from the log-linear interpolation between the scores of the E2E model and the external LM. The internal LM scores are approximated as the output of an E2E model when eliminating its acoustic components. ILME can alleviate the domain mismatch between training and testing, or improve the multi-domain E2E ASR. Experimented with 30K-hour trained RNN-T and AED models, ILME achieves up to 15.5% and 6.8% relative word error rate reductions from Shallow Fusion on out-of-domain LibriSpeech and in-domain Microsoft production test sets, respectively.

*Index Terms*— Speech recognition, language model, recurrent neural network transducer, attention-based encoder-decoder

### 1. INTRODUCTION

End-to-end (E2E) automatic speech recognition (ASR), with the goal of directly mapping input speech features to output token sequence, has achieved state-of-the-art performance on a variety of tasks [\[1,](#page-6-0) [2,](#page-6-1) [3\]](#page-6-2). The most popular E2E models include connectionist temporal classification [\[4,](#page-6-3) [5,](#page-6-4) [6,](#page-6-5) [7,](#page-6-6) [8\]](#page-6-7), recurrent neural network transducer (RNN-T) [\[9,](#page-6-8) [10,](#page-6-9) [2,](#page-6-1) [3\]](#page-6-2), and attention-based encoder-decoder (AED) models [\[11,](#page-6-10) [12,](#page-6-11) [13,](#page-6-12) [1,](#page-6-0) [14,](#page-6-13) [15\]](#page-6-14). However, incorporating acoustic model (AM), language model (LM), and pronunciation models in a single deep neural networks (DNN) results in E2E models being more susceptible to domain shift from training to testing than conventional DNN-hidden Markov model (HMM) hybrid models [\[16\]](#page-6-15). Many methods have been proposed to adapt ASR models towards the target domain of the test data, such as approaches based on regularization [\[17,](#page-6-16) [18,](#page-6-17) [19,](#page-6-18) [20,](#page-6-19) [21,](#page-6-20) [18\]](#page-6-17), teacher-student learning [\[22,](#page-6-21) [23,](#page-6-22) [24,](#page-6-23) [25\]](#page-6-24), transformation [\[26,](#page-6-25) [27,](#page-6-26) [28,](#page-6-27) [29\]](#page-6-28), and adversarial learning [\[30,](#page-6-29) [31,](#page-6-30) [32,](#page-6-31) [33\]](#page-6-32). However, all these methods require audio or audio-transcript pairs as the adaptation data when applied to E2E models [\[34,](#page-6-33) [35,](#page-6-34) [36\]](#page-6-35).

LM integration is a promising approach to adapt (customize) E2E models towards testing scenarios with *text-only* data for both cross-domain and intra-domain applications. For cross-domain application, an external LM trained with target-domain text-only data is integrated with a source-domain E2E model to improve the ASR on the target-domain test data. For intra-domain application, an external LM trained with a large amount multi-domain text is fused with a multi-conditional E2E model to improve the ASR on multiple in-domain test data. With orders of magnitude more text-only data available than E2E training transcripts, the external LM has great potential to correct the hypotheses of E2E models given unseen styles of speech or long tails of phrases and words in the test utterances. However, LM integration remains to be a challenging task because no explicit separation of AM and LM exists in E2E models.

Among many studies in LM integration, Shallow Fusion [\[6,](#page-6-5) [37,](#page-6-36) [38,](#page-7-0) [39\]](#page-7-1) stands as a simple yet effective approach involving a log-linear interpolation between the scores of the E2E model and a separately-trained LM during decoding. Towards a more structural integration, Deep Fusion [\[37\]](#page-6-36), Cold Fusion [\[40,](#page-7-2) [41\]](#page-7-3), Simple Fusion [\[42\]](#page-7-4) and Component Fusion [\[43\]](#page-7-5) were proposed to jointly train an E2E model with an external LM to learn a sophisticated combination between their hidden units via gating mechanisms. However, with additional training steps and computational cost during decoding, these methods have not replaced Shallow Fusion as the dominant approach in LM integration.

Recently, the Density Ratio method [\[44,](#page-7-6) [45,](#page-7-7) [46,](#page-7-8) [47\]](#page-7-9) was proposed as an extension of Shallow Fusion. During inference, the score of a source-domain LM trained with E2E training transcript is subtracted from the log-linear combination of E2E model and LM scores. Density Ratio has shown to consistently outperform Shallow Fusion in a cross-domain evaluation. However, Density Ratio is based on the assumption that the E2E posterior is factorizable into an AM and an LM with individual parameters like a hybrid system, while the accurate factorization is to condition both the "AM" and "LM" components on the E2E model parameters. We call the token sequence probability predicted by an E2E model the *internal LM*.

In [\[48\]](#page-7-10), a hybrid autoregressive transducer (HAT) was proposed as a new type of E2E model that preserves the modularity of the hybrid model. HAT provides an efficient way to estimate its internal LM by removing the effect of the encoder from the network. During HAT decoding, the internal LM score is subtracted from the path posterior after combining with external LM score. However, this LM integration requires us to train an HAT model with a special network architecture that separately models the label and duration distributions, preventing us from leveraging the existing E2E models.

Inspired by HAT, we propose an *internal LM estimation (ILME)* method to effectively integrate external LMs with all pre-existing E2E models without any additional model training, including the most popular time-synchoronrous RNN-T and time-asynchonrous AED. With ILME, we estimate and subtract the internal LM scores of an E2E model from the log-linear combination of the E2E and LM scores during inference. By removing the separable AM-LM assumption, ILME enables a more accurate and a lighter-weight external LM integration than Density Ratio with no additional source-domain LM running at the inference. We evaluate 30K-hour RNN-T and AED models on cross-domain LibriSpeech test sets and intradomain Microsoft production test sets. ILME achieves up to 15.5% and 6.8% relative word error rate (WER) reductions from Shallow Fusion for cross- and intra-domain evaluations, respectively. Further, despite having 26.8%-29.8% fewer parameters, ILME consistently outperforms Density Ratio in terms of lower WER.

#### 2. RELATED E2E MODELS

An E2E model predicts the posterior distribution  $P(\mathbf{Y}|\mathbf{X};\theta_{\text{E2E}})$  over sequences of output tokens  $\mathbf{Y} = \{y_1,\ldots,y_U\}$  given a sequence of input speech features  $\mathbf{X} = \{\mathbf{x}_1,\ldots,\mathbf{x}_T\}$ , where  $y_u \in \mathcal{V}, u = 1,\ldots,U$ , and  $\mathbf{x}_t \in \mathbb{R}^{d_x}, t = 1,\ldots,T$ .  $\mathcal{V}$  is the set of all possible output tokens, e.g., word pieces, etc. For RNN-T and AED models, a special token  $y_0 = \langle \text{sos} \rangle$  is inserted at the beginning of  $\mathbf{Y}$  to indicate the start of the sentence.

### 2.1. Recurrent Neural Network Transducer (RNN-T)

The RNN-T model [9] consists of an encoder, a prediction network and a joint network. Analogous to an acoustic model, the encoder maps the input speech features to a sequence of hidden representations  $\mathbf{H}^{\text{enc}} = \{\mathbf{h}_1^{\text{enc}}, \dots, \mathbf{h}_r^{\text{mc}}\}$ , i.e.,  $\mathbf{H}^{\text{enc}} = \text{Encoder}(\mathbf{X})$ . Imitating an RNN-LM, the prediction network takes the embedding vector  $\mathbf{e}_{u-1}$  of the previous *non-blank* token  $y_{u-1}$  to generate the hidden representation  $\mathbf{h}_u^{\text{pred}}$  by using an RNN, i.e.,  $\mathbf{h}_u^{\text{pred}} = \text{PredictionRNN}(\mathbf{h}_{u-1}^{\text{pred}}, \mathbf{e}_{u-1})$ .

RNN-T predicts a conditional distribution over blank-augmented token sequences  $\tilde{\mathbf{Y}} = \{\tilde{y}_1, \dots, \tilde{y}_{T+U}\}$ , where  $\tilde{y}_i \in \mathcal{V} \cup \langle b \rangle, i = 1, \dots, T+U$ , and  $\langle b \rangle$  is a blank.  $\tilde{\mathbf{Y}}$  is aligned with the token and feature sequences  $\mathbf{Y}$  and  $\mathbf{X}$  as  $(\tilde{y}_i, y_{u_i}, x_{t_i})_{i=1}^{U+T}$ , where the index i in  $\tilde{\mathbf{Y}}$  is mapped to the index  $u_i$  in  $\mathbf{Y}$ , and the index  $t_i$  in  $\mathbf{X}$ .

The joint network combines the outputs of the encoder and prediction network via a feed-forward network to produce the logits  $\mathbf{z}_{t_i,u_i}$ , and applies a softmax to predict the conditional distribution over the next possible tokens in  $\mathcal{V} \cup \langle \mathbf{b} \rangle$ , i.e.,

$$\mathbf{h}_{t_i,u_i}^{\text{joint}} = \phi(W_e \mathbf{h}_{t_i}^{\text{enc}} + W_p \mathbf{h}_{u_i}^{\text{pred}} + \mathbf{b}_e + \mathbf{b}_p), \tag{1}$$

$$\mathbf{z}_{t_i,u_i} = W_j \mathbf{h}_{t_i,u_i}^{\text{joint}} + \mathbf{b}_j, \tag{2}$$

$$\left[P(\tilde{y}_i = v | \mathbf{X}_{1:t_i}, \mathbf{Y}_{0:u_{i-1}}; \theta_{\text{RNNT}}^{\text{S}})\right]_{v \in \mathcal{V} \cup \langle b \rangle} = \text{softmax}(\mathbf{z}_{t_i, u_i}), (3)$$

where  $\phi$  is a non-linear function, e.g., tanh or ReLU.  $W_e$  and  $W_p$  are weight matrices, and  $\mathbf{b}_e$ ,  $\mathbf{b}_p$  are the biases.  $\mathbf{z}_{t_i,u_i}$  is a  $|\mathcal{V}|+1$  dimensional logit vector.

The token sequence posterior  $P(\mathbf{Y}|\mathbf{X}; \theta_{RNNT}^S)$  is computed by summing over the posteriors of all possible blank-augmented token sequences aligned with  $\mathbf{Y}$ , i.e.,  $\mathcal{A}(\mathbf{X}, \mathbf{Y})$ .

$$P(\mathbf{Y}|\mathbf{X}; \theta_{\text{RNNT}}^{\text{S}}) = \sum_{\tilde{\mathbf{Y}} \in \mathcal{A}(\mathbf{X}, \mathbf{Y})} P(\tilde{\mathbf{Y}}|\mathbf{X}; \theta_{\text{RNNT}}^{\text{S}})$$

$$= \sum_{\tilde{\mathbf{Y}} \in \mathcal{A}(\mathbf{X}, \mathbf{Y})} \prod_{i=1}^{T+U} P(\tilde{y}_{i}|\mathbf{X}_{1:t_{i}}, \mathbf{Y}_{0:u_{i-1}}; \theta_{\text{RNNT}}^{\text{S}}). \quad (4)$$

### 2.2. Attention-Based Encoder-Decoder (AED)

For AED, we add a <eos> token to the end of each token sequence to indicate the end of a sentence. The AED model [11] incorporates

an encoder, a decoder and an attention network. The encoder maps a sequence of input speech frames  $\mathbf{X}$  into a sequence of hidden representations  $\mathbf{H}^{\text{enc}}$ . The attention network determines which encoded features in  $\mathbf{H}^{\text{enc}}$  should be attended to predict the output label  $y_u$  by generating an attention weight for each  $\mathbf{h}^{\text{enc}}_t$  at a decoder step u. A context vector  $\mathbf{c}_u$  is computed as a linear combination of  $\mathbf{H}^{\text{enc}}$  weighted by the attention.

$$\mathbf{a}_{u} = \text{AttentionNet}(\mathbf{a}_{u-1}, \mathbf{h}_{t}^{\text{enc}}, \mathbf{h}_{u}^{\text{dec}}),$$
 (5)

<span id="page-1-7"></span><span id="page-1-6"></span>
$$\mathbf{c}_{u} = \sum_{t=1}^{T} a_{u,t} \mathbf{h}_{t}^{\text{enc}},\tag{6}$$

where  $\mathbf{a}_u$  is a vector of attention weights with a dimension of T.

At each step u, the decoder RNN takes the sum of the previous token embedding  $\mathbf{e}_{u-1}$  and the context vector  $\mathbf{c}_{u-1}$  as the input to predict the conditional distribution over  $\mathcal{V} \cup \langle \text{eos} \rangle$ , i.e.,

$$\mathbf{h}_{u}^{\text{dec}} = \text{DecoderRNN}(\mathbf{h}_{u-1}^{\text{dec}}, \mathbf{e}_{u-1} + \mathbf{c}_{u-1}), \tag{7}$$

$$\mathbf{z}_u = W_d \mathbf{h}_u^{\text{dec}} + \mathbf{b}_d, \tag{8}$$

$$[P(y_u = v | \mathbf{X}, \mathbf{Y}_{0:u-1}; \theta_{AED}^{S})]_{v \in \mathcal{V} \cup \langle eos \rangle} = \operatorname{softmax}(\mathbf{z}_u), \quad (9)$$

where  $\mathbf{h}_u^{\text{dec}}$  is the hidden state of the decoder RNN.  $W_d$  and  $\mathbf{b}_d$  are weight matrix and bias, respectively.

The token sequence posterior  $P(\mathbf{Y}|\mathbf{X}; \theta_{AED}^{S})$  is computed as

<span id="page-1-5"></span>
$$P(\mathbf{Y}|\mathbf{X}; \theta_{AED}^{S}) = \prod_{u=1}^{U+1} P(y_u|\mathbf{X}, \mathbf{Y}_{0:u-1}; \theta_{AED}^{S}).$$
 (10)

#### 3. RELATED LM INTEGRATION METHODS

#### 3.1. Shallow Fusion

In Shallow Fusion, a separately-trained external LM is integrated with the E2E model during inference to optimize a log-linear interpolation between the E2E and LM probabilities. The optimal token sequence  $\hat{\mathbf{Y}}$  is obtained as follows via a left-to-right beam search

$$\hat{\mathbf{Y}} = \arg\max_{\mathbf{Y}} \left[ \log P(\mathbf{Y}|\mathbf{X}; \theta_{\text{E2E}}^{\text{S}}) + \lambda_T \log P(\mathbf{Y}; \theta_{\text{LM}}^{\text{T}}) \right], \quad (11)$$

<span id="page-1-4"></span><span id="page-1-3"></span><span id="page-1-2"></span>where  $P(\mathbf{Y}|\mathbf{X}; \theta_{\text{E2E}}^{S})$  is the token sequence posterior of an E2E model trained with source-domain audio-transcript pairs while  $P(\mathbf{Y}; \theta_{\text{LM}}^{\text{T}})$  is the probability of an external LM trained with target-domain text.  $\lambda_T$  is the target-domain LM weight.

#### 3.2. Density Ratio Method

In analogy to the traditional DNN-HMM hybrid system, the Density Ratio method [44] assumes that the token sequence posterior  $P(\mathbf{Y}|\mathbf{X};\theta_{\text{E2E}}^{8})$  of a source-domain E2E model is factorizable into a source-domain AM  $P(\mathbf{X}|\mathbf{Y};\theta_{\text{AM}}^{8})$  and a source-domain LM  $P(\mathbf{Y};\theta_{\text{LM}}^{8})$  through Bayes' theorem as follows

<span id="page-1-0"></span>
$$P(\mathbf{Y}|\mathbf{X}; \theta_{\text{E2E}}^{\text{S}}) = \frac{P(\mathbf{X}|\mathbf{Y}; \theta_{\text{AM}}^{\text{S}}) P(\mathbf{Y}; \theta_{\text{LM}}^{\text{S}})}{P(\mathbf{X}; \theta_{\text{E2E}}^{\text{S}})}.$$
 (12)

Our goal is to estimate the target-domain token sequence posterior  $P(\mathbf{Y}|\mathbf{X}; \boldsymbol{\theta}_{\text{E2E}}^T)$  by using a source-domain E2E model and an external LM trained with target-domain text. Under the same assumption, we have a similar factorization below in the target domain

<span id="page-1-1"></span>
$$P(\mathbf{Y}|\mathbf{X}; \theta_{\text{E2E}}^{\text{T}}) = \frac{P(\mathbf{X}|\mathbf{Y}; \theta_{\text{AM}}^{\text{T}}) P(\mathbf{Y}; \theta_{\text{LM}}^{\text{T}})}{P(\mathbf{X}; \theta_{\text{E2E}}^{\text{T}})},$$
(13)

where  $P(\mathbf{X}|\mathbf{Y}; \theta_{\mathrm{AM}}^{\mathrm{T}})$  is the acoustic likelihood in the target domain, and  $P(\mathbf{Y}; \theta_{\mathrm{IM}}^{\mathrm{T}})$  is the target-domain LM probability.

By assuming domain-invariant acoustic conditions [44], i.e.,  $P(\mathbf{X}|\mathbf{Y}; \theta_{\text{AM}}^{\text{S}}) = P(\mathbf{X}|\mathbf{Y}; \theta_{\text{AM}}^{\text{T}})$ , we derive  $P(\mathbf{Y}|\mathbf{X}; \theta_{\text{E2E}}^{\text{T}})$  from Eqs. (12) and (13) as follows

$$P(\mathbf{Y}|\mathbf{X}; \theta_{\text{E2E}}^{\text{T}}) = P(\mathbf{Y}|\mathbf{X}; \theta_{\text{E2E}}^{\text{S}}) \frac{P(\mathbf{Y}; \theta_{\text{LM}}^{\text{T}})}{P(\mathbf{Y}; \theta_{\text{LM}}^{\text{S}})} \frac{P(\mathbf{X}; \theta_{\text{E2E}}^{\text{S}})}{P(\mathbf{X}; \theta_{\text{E2E}}^{\text{T}})}, \quad (14)$$

where  $P(\mathbf{X}; \theta_{\text{E2E}}^{\text{S}})/P(\mathbf{X}; \theta_{\text{E2E}}^{\text{T}})$  is constant over all hypotheses  $\mathbf{Y}$  given  $\mathbf{X}$ , and  $P(\mathbf{Y}; \theta_{\text{LM}}^{\text{T}})/P(\mathbf{Y}; \theta_{\text{LM}}^{\text{S}})$  is the *density ratio* between the probabilities of target and source-domain LMs.

During inference, Density Ratio subtracts the log probability of the source-domain LM from the log-linear combination between E2E and the external LM scores, i.e.,

$$\hat{\mathbf{Y}} = \underset{\mathbf{Y}}{\operatorname{arg max}} \left[ \log P(\mathbf{Y}|\mathbf{X}; \theta_{\text{E2E}}^{\text{S}}) + \lambda_T \log P(\mathbf{Y}; \theta_{\text{LM}}^{\text{T}}) - \lambda_S \log P(\mathbf{Y}; \theta_{\text{LM}}^{\text{S}}) \right],$$
(15)

where  $\lambda_S$  is source-domain LM weight.

Note that, in Density Ratio, the source-domain LM  $P(\mathbf{Y}; \theta_{\mathrm{LM}}^{\mathbf{S}})$  is trained with the training transcript of the E2E model, and it has a completely different set of parameters from  $\theta_{\mathrm{E2E}}^{\mathbf{S}}$ .

#### 4. INTERNAL LM ESTIMATION FOR E2E MODELS

Density Ratio has shown to be more effective than Shallow Fusion for LM integration [44]. However, as in Eqs. (12) and (13), Density Ratio assumes that the posterior of a source-domain E2E model is decomposable into individual AM and LM with separate parameters like a hybrid system. Strictly speaking, the source-domain E2E posterior should be factorized as follows via Bayes' theorem

$$P(\mathbf{Y}|\mathbf{X}; \theta_{\text{E2E}}^{\text{S}}) = \frac{P(\mathbf{X}|\mathbf{Y}; \theta_{\text{E2E}}^{\text{S}}) P(\mathbf{Y}; \theta_{\text{E2E}}^{\text{S}})}{P(\mathbf{X}; \theta_{\text{E2E}}^{\text{S}})},$$
(16)

where all factors are conditioned on the same set of E2E parameters  $\theta_{\text{E2E}}^{\text{S}}$ , and  $P(\mathbf{Y}; \theta_{\text{E2E}}^{\text{S}})$  is the *internal LM* of an E2E model. Given constant acoustic conditions [44], i.e.,  $P(\mathbf{X}|\mathbf{Y}; \theta_{\text{E2E}}^{\text{S}}) = P(\mathbf{X}|\mathbf{Y}; \theta_{\text{AM}}^{\text{S}})$ , the target-domain E2E posterior is computed as follows with Eq. (13)

$$P(\mathbf{Y}|\mathbf{X}; \boldsymbol{\theta}_{\text{E2E}}^{\text{T}}) = P(\mathbf{Y}|\mathbf{X}; \boldsymbol{\theta}_{\text{E2E}}^{\text{S}}) \frac{P(\mathbf{Y}; \boldsymbol{\theta}_{\text{LM}}^{\text{T}})}{P(\mathbf{Y}; \boldsymbol{\theta}_{\text{E2E}}^{\text{S}})} \frac{P(\mathbf{X}; \boldsymbol{\theta}_{\text{E2E}}^{\text{S}})}{P(\mathbf{X}; \boldsymbol{\theta}_{\text{E2E}}^{\text{T}})}. \quad (17)$$

During inference, the log probability of the internal LM is subtracted from the log-linear combination between the scores of E2E and external LMs as follow.

$$\hat{\mathbf{Y}} = \underset{\mathbf{Y}}{\operatorname{arg max}} \left[ \log P(\mathbf{Y} | \mathbf{X}; \theta_{\text{E2E}}^{\text{S}}) + \lambda_T \log P(\mathbf{Y}; \theta_{\text{LM}}^{\text{T}}) - \lambda_I \log P(\mathbf{Y}; \theta_{\text{E2E}}^{\text{S}}) \right],$$
(18)

where  $\lambda_I$  is internal LM weight. We call this LM integration method internal LM estimation (ILME). Compared to Density Ratio, ILME subtracts the log probability of an E2E internal LM parameterized by  $\theta_{\rm E2E}^{\rm S}$  rather than that of a source-domain LM separately-trained with the training transcript of the E2E model.

The key step of ILME is to estimate the internal LM below defined as the token sequence probability distribution an E2E model

implicitly learns from the audio-transcript training pairs

$$P(\mathbf{Y}; \theta_{\text{E2E}}^{\text{S}}) = \prod_{u=1}^{U} P(y_u | \mathbf{Y}_{0:u-1}; \theta_{\text{E2E}}^{\text{S}})$$
(19)

<span id="page-2-4"></span><span id="page-2-0"></span>
$$= \prod_{u=1}^{U} \prod_{X} P(y_u | \mathbf{X}, \mathbf{Y}_{0:u-1}; \theta_{\text{E2E}}^{\text{S}}) P(\mathbf{X} | \mathbf{Y}_{0:u-1}; \theta_{\text{E2E}}^{\text{S}}). (20)$$

However, the summation over the entire acoustical space in Eq. (20) is intractable in practice. To address this, Proposition 1 in [48, Appendix A] was proposed and proved to approximate the internal LM of an HAT model by eliminating the effect of the encoder activations. We name this proposition Joint Softmax Approximation (JSA) in this paper.

JSA suggests that if  $\mathbf{f}_t$  is a high-level acoustic representation of the speech feature  $\mathbf{x}_t$ ,  $\mathbf{g}_u$  is a language representation of the token  $\mathbf{y}_u$ , and the output probability of an E2E model can be expressed by  $\mathbf{f}_t$  and  $\mathbf{g}_u$  in form of  $P(y_u|\mathbf{X},\mathbf{Y}_{0:u-1};\theta_{\text{E2E}}^S)) = \text{softmax}[J(\mathbf{f}_t+\mathbf{g}_u)]$ , where J is any function that satisfies  $J(\mathbf{f}_t+\mathbf{g}_u) \approx J(\mathbf{f}_t) + J(\mathbf{g}_u)$ , the conditional probability of the E2E internal LM, i.e.,  $P(y_u|\mathbf{Y}_{0:u-1};\theta_{\text{E2E}}^S)$ , can be approximated as the output of the E2E model at the step u after we zero out the acoustic representation  $\mathbf{f}_t$  from the network, i.e., softmax $[J(\mathbf{g}_u)]$ .

We apply JSA to estimate the internal LMs of the pre-existing most popular E2E models, RNN-T and AED models, in Sections 4.1 and 4.2 without any addition training.

#### <span id="page-2-1"></span>4.1. Internal LM Estimation for RNN-T Model

With a softmax token distribution defined in Eq. (3), the joint network of RNN-T satisfies the conditions of JSA if we re-formulate Eqs. (1) and (2) as

$$\mathbf{f}_{t_i} = W_e \mathbf{h}_{t_i}^{\text{enc}} + \mathbf{b}_e \tag{21}$$

$$\mathbf{g}_{u_i} = W_p \mathbf{h}_{u_i}^{\text{pred}} + \mathbf{b}_p \tag{22}$$

<span id="page-2-2"></span>
$$\mathbf{z}_{t_i,u_i} = J(\mathbf{f}_{t_i} + \mathbf{g}_{u_i}) \tag{23}$$

where  $J(\cdot) = W_j \phi(\cdot) + \mathbf{b}_j$  is a non-linear function followed by an affine transform. As linear transforms of encoder and prediction network outputs,  $\mathbf{f}_{t_i}$ ,  $\mathbf{g}_{u_i}$  are viewed as acoustic and language representations, respectively. By following JSA, we eliminate  $\mathbf{f}_{t_i}$  from the joint network and compute the logits as follows

$$\mathbf{z}_u^{\text{ILM}} = J(\mathbf{g}_u) = W_j \phi(W_p \mathbf{h}_u^{\text{pred}} + \mathbf{b}_p) + \mathbf{b}_j$$
 (24)

Note that, without  $\mathbf{f}_{t_i}$ , the RNN-T is completely driven by the prediction and joint networks with the token sequence  $\mathbf{Y}$  (indexed by u) as the only input. No alignment exists between  $\mathbf{Y}$  and  $\mathbf{X}$  anymore, so we abandon the use of index i for Eqs. (24) to (26).

so we abandon the use of index i for Eqs. (24) to (26). With a designated logit for the blank token <br/>b>,  $\mathbf{z}_u^{\mathrm{ILM}}$  has a dimension of  $|\mathcal{V}|+1$ . However, we want to estimate the internal LM of the *non-blank* token sequences  $\mathbf{Y}$ . Therefore, we remove the blank logit from the vector  $\mathbf{z}_u^{\mathrm{ILM}}$  to construct a new logit vector  $\mathbf{z}_u^{\mathrm{ILM, NB}}$  of dimension  $|\mathcal{V}|$ , and apply softmax over  $\mathbf{z}_{u_i}^{\mathrm{ILM, NB}}$  to compute the internal LM conditional distribution over  $|\mathcal{V}|$  non-blank tokens below

<span id="page-2-5"></span><span id="page-2-3"></span>
$$P(y_u|\mathbf{Y}_{0:u-1};\theta_{\text{RNNT}}^{\text{S}}) = \text{softmax}(\mathbf{z}_u^{\text{ILM, NB}})$$
 (25)

With Eq. (19), the RNN-T internal LM is estimated as

$$\log P_{\text{ILM-RNNT}}(\mathbf{Y}) = \sum_{u=1}^{U} \log P(y_u | \mathbf{Y}_{0:u-1}; \theta_{\text{RNNT}}^{\text{S}})$$
 (26)

The procedure of the ILME method for LM integration with RNN-T model is the following

- 1. Train a *standard* RNN-T model with source-domain audiotranscript training pairs.
- 2. Train an external LM with target-domain text-only data.
- 3. During inference, at each step of the beam search, estimate internal LM score of the next *non-blank* candidate token in V with Eq. [\(25\)](#page-2-5), and subtract it from the log-linear interpolation between RNN-T and external LM scores of the same token given a partial hypothesis in the beam using Eq. [\(27\)](#page-3-1). Use only the RNN-T score in Eq. [\(3\)](#page-1-2) for the candidate token <b>.

$$Score(\tilde{y}_{u_i}|\mathbf{X}_{1:t_{i-1}}, \mathbf{Y}_{0:u_{i-1}})$$

$$= \log P(\tilde{y}_i|\mathbf{X}_{1:t_i}, \mathbf{Y}_{0:u_{i-1}}; \theta_{\text{RNNT}}^{\text{S}})$$

$$+ \lambda_T \log P(\tilde{y}_i|\mathbf{Y}_{0:u_{i-1}}; \theta_{\text{LM}}^{\text{T}})$$

$$- \lambda_I \log P(\tilde{y}_{u_i}|\mathbf{Y}_{0:u_{i-1}}; \theta_{\text{RNNT}}^{\text{S}}) \qquad (27)$$

### <span id="page-3-0"></span>4.2. Internal LM Estimation for AED Model

The output distribution of AED is defined by a softmax function in Eq. [\(9\)](#page-1-5). As a special case of JSA when t and u are synchronized (i.e., t = u), the decoder of AED also satisfies all its conditions once we re-formulate Eqs. [\(7\)](#page-1-6) and [\(8\)](#page-1-7) as

$$\mathbf{f}_u = \mathbf{c}_{u-1},\tag{28}$$

$$\mathbf{g}_u = \mathbf{e}_{u-1},\tag{29}$$

$$\mathbf{z}_u = J(\mathbf{f}_u + \mathbf{g}_u) \tag{30}$$

where J(·) = WdDecoderRNN(h dec <sup>u</sup>−1, ·) + b<sup>d</sup> is a series of linear and non-linear functions. We view fu, a linear combination of encoder output, as the acoustic representation, and gu, the token embedding, as the language representation.

JSA allows us to remove fu, i.e., the context vector cu, from the decoder, and compute the conditional probability of the AED internal LM by applying a softmax over logits output as follows

$$P(y_u|\mathbf{Y}_{0:u-1}; \theta_{AED}^{S}) = \operatorname{softmax} [J(\mathbf{g}_u)]$$

$$= \operatorname{softmax} \left[ W_d \cdot \operatorname{DecoderRNN}(\mathbf{h}_{u-1}^{\text{dec}}, \mathbf{e}_{u-1}) + \mathbf{b}_d \right]$$
(31)

Note that, without f<sup>t</sup><sup>i</sup> , AED is entirely driven by the decoder with the token sequence Y as the only input, acting exactly the same as an RNN-LM. With Eq. [\(19\)](#page-2-4), the AED internal LM is estimated as

$$\log P_{\text{ILM-AED}}(\mathbf{Y}) = \sum_{u=1}^{U+1} \log P(y_u | \mathbf{Y}_{0:u-1}; \theta_{\text{AED}}^{S})$$
 (32)

The procedure of the ILME method for LM integration with AED model is the following

- 1. Train a *standard* AED model with the source-domain audiotranscript training pairs.
- 2. Train an external LM with target-domain text-only data.
- 3. During inference, at each step of the beam search, estimate internal LM score of the next candidate token in V with Eq. [\(31\)](#page-3-2), and subtract it from the log-linear interpolation between AED and external LM scores of the same token given a partial hypothesis in the beam using Eq. [\(33\)](#page-3-3).

Score
$$(y_u|\mathbf{X}, \mathbf{Y}_{0:u-1}) = \log P(y_u|\mathbf{X}, \mathbf{Y}_{0:u-1}; \theta_{AED}^S)$$
  
  $+ \lambda_T \log P(y_u|\mathbf{Y}_{0:u-1}; \theta_{LM}^T)$   
  $- \lambda_I \log P(y_u|\mathbf{Y}_{0:u-1}; \theta_{AED}^S)$  (33)

### 5. EXPERIMENT

In this work, we perform both cross-domain and intra-domain evaluations with different LM integration methods. For all evaluations in this paper, we perform beam search inference with a beam size of 25. All E2E models and RNN-LMs predict word-piece output tokens. We generate 3999 word pieces as the token vocabulary V by running byte-pair encoding [\[49\]](#page-7-11) on acoustic training text, and tokenize all the training transcripts of E2E models and the training text of LMs with these word pieces. We use PyTorch toolkit [\[50\]](#page-7-12) for all the experiments.

### <span id="page-3-4"></span>5.1. E2E Models

### <span id="page-3-1"></span>*5.1.1. Training data*

We train an RNN-T and an AED with the same 30 thousand (K) hours of anonymized and transcribed data from Microsoft services, including desktop and mobile voice search, short message dictation, command and control, and one-on-one and multi-party conversations recorded in both close-talk and far-field conditions. We extract 80-dimensional log Mel filter bank features from the speech signal in both the training and test sets every 10 ms over a 25 ms window. We stack 3 consecutive frames and stride the stacked frame by 30 ms, to form a sequence of 240-dimensional input speech features.

#### *5.1.2. RNN-T Model*

We train a 30K-hour RNN-T model predicting word pieces for E2E ASR. The encoder is a uni-directional long short-term memory (LSTM) [\[51,](#page-7-13) [52,](#page-7-14) [53\]](#page-7-15) with 6 hidden layers, each with 1024 hidden units. Each word-piece is represented by a 1024-dimensional embedding vector. The prediction network is a uni-directional LSTM with 2 hidden layers, each with 1024 hidden units. The outputs of encoder and prediction network are projected to 1024-dimensional vectors after layer normalization [\[54\]](#page-7-16). The joint network has 4000 dimensional output units predicting 3999 word pieces and <b>. Dropout [\[55\]](#page-7-17) with a probability of 0.1 is used in both the encoder and the prediction network. An RNN-T loss is implemented with a memory-efficient forward-backward algorithm and is minimized during training. The RNN-T model has 76M parameters.

### <span id="page-3-2"></span>*5.1.3. AED Model*

We train a 30K-hour AED model [\[11,](#page-6-10) [56,](#page-7-18) [57\]](#page-7-19) predicting word pieces for E2E ASR. The encoder is a bi-directional LSTM with 6 hidden layers and 780 hidden units in each layer. The hidden vectors from both directions are concatenated at each layer and projected to a 780-dimensional vector before layer normalization [\[54\]](#page-7-16). Each wordpiece is represented by a 780-dimensional embedding vector. The decoder is a uni-directional LSTM with 2 hidden layers, each with 1280 hidden units. The decoder has 4000-dimensional output units predicting 3999 word pieces and <eos>. During training, scheduled sampling [\[58\]](#page-7-20) is applied to the decoder at rate of 0.0001. Dropout [\[55\]](#page-7-17) with a probability of 0.1 is used in both encoder and decoder. A label-smoothed cross-entropy [\[38\]](#page-7-0) loss is minimized during training. The AED model has 97M parameters.

#### <span id="page-3-5"></span>5.2. Cross-Domain Evaluation

<span id="page-3-3"></span>We evaluate a source-domain E2E model on target-domain test data by integrating an external LM trained with the text-only data in the target domain. We use the RNN-T or AED trained with 30K-hour multi-conditional data in Section [5.1](#page-3-4) as the source-domain E2E model, and define LibriSpeech data [\[59\]](#page-7-21), read English speech based on LibriVox's audio books, as the target domain. The LibriSpeech corpus consists of 960 hours of transcribed training speech and additional 813M words of text-only data collected from 14.5K books. Note that the source-domain 30K-hour training data includes neither the LibriSpeech data nor any read speech from public books. The short message dictation in the 30K-hour data has a very different style from audio books.

We train a target-domain word-piece LSTM-LM with a combination of the 9.4M-word transcript of the 960-hour training speech and the 813M-word text in LibriSpeech. The LSTM-LM has 2 hidden layers with 2048 hidden units for each layer. The top hidden layer is first projected to a 512-dimensional embedding, and is then mapped to 4000 output units predicting 3999 word pieces and <eos>. Each token is represented by a 512-dimensional embedding. The parameters of input and output embeddings are tied. The LSTM-LM is trained using noise-contrastive estimation loss [\[60\]](#page-7-22). The LibriSpeech LSTM-LM has 58M parameters in total. For Density Ratio, we train a source-domain word-piece LSTM-LM with 2 hidden layers and 2048 hidden units at each layer using the 271M-word transcript of the 30K data. The source-domain LM consists of 57M parameters.

We first evaluate the 30K-hour E2E models on a target-domain test set, LibriSpeech "test-clean" with 53K words by using LibriSpeech "dev-clean" with 54K words as the validation set for tuning the LM weights. The results are shown in Table [1.](#page-4-0) All three LM integration methods show relative WER reductions in the range of 16.1%-29.1% from the baseline RNN-T. ILME performs the best achieving 15.5% and 5.6% relative WER reductions compared to shallow fusion and density ratio, respectively. The results for AED are similar to that of RNN-T with ILME performing the best, achieving 43.4%, 8.6% and 4.3% relative WER reductions from AED baseline, Shallow Fusion and Density Ratio, respectively.

| E2E   | Method | Params | λT   | µ    | WER  |      | Test |
|-------|--------|--------|------|------|------|------|------|
| Model |        |        |      |      | Dev  | Test | WERR |
| RNN-T | BS     | 76M    | -    | -    | 9.27 | 8.97 | -    |
|       | SF     | 134M   | 0.12 | 0.00 | 7.44 | 7.53 | 16.1 |
|       | DR     | 191M   | 0.17 | 0.07 | 6.80 | 6.74 | 24.9 |
|       | ILME   | 134M   | 0.30 | 0.14 | 6.41 | 6.36 | 29.1 |
| AED   | BS     | 97M    | -    | -    | 8.56 | 8.61 | -    |
|       | SF     | 155M   | 0.19 | 0.00 | 5.00 | 5.33 | 38.1 |
|       | DR     | 212M   | 0.15 | 0.03 | 4.74 | 5.09 | 40.9 |
|       | ILME   | 155M   | 0.18 | 0.10 | 4.42 | 4.87 | 43.4 |

<span id="page-4-0"></span>Table 1. WERs (%) of 30k-hour E2E models baseline (BS), Shallow Fusion (SF), Density Ratio (DR) and the proposed ILME methods on the out-of-domain LibriSpeech dev-clean (Dev) and test-clean (Test) sets. The external LM is trained with text-only data in LibriSpeech. LM weight µ = λ<sup>S</sup> for DR, and µ = λ<sup>I</sup> for ILME. WERR is the relative WER reduction from BS.

Then we evaluate the 30K-hour E2E models on another targetdomain test set, LibriSpeech "test-other" with 52K words by using LibriSpeech "dev-other" with 51K words as the validation set. The results are shown in Table [2.](#page-4-1) All three LM integration methods show WER reductions in the range of 6.7%-15.9% relative to the baseline RNN-T. ILME performs the best achieving 9.9% and 5.9% relative WER reductions compared to shallow fusion and density ratio, respectively. The results for AED are similar to that of RNN-T with ILME performing the best, achieving 44.1%, 8.6% and 4.3% relative WER reductions from AED baseline, Shallow Fusion and Density Ratio, respectively.

| E2E   |        | Params | λT   | µ    | WER   |       | Test |
|-------|--------|--------|------|------|-------|-------|------|
| Model | Method |        |      |      | Dev   | Test  | WERR |
| RNN-T | BS     | 76M    | -    | -    | 20.03 | 20.23 | -    |
|       | SF     | 134M   | 0.07 | 0.00 | 18.37 | 18.88 | 6.7  |
|       | DR     | 191M   | 0.20 | 0.12 | 16.14 | 18.07 | 10.7 |
|       | ILME   | 134M   | 0.24 | 0.12 | 15.48 | 17.01 | 15.9 |
| AED   | BS     | 97M    | -    | -    | 18.10 | 22.04 | -    |
|       | SF     | 155M   | 0.10 | 0.00 | 12.84 | 13.39 | 39.2 |
|       | DR     | 212M   | 0.12 | 0.02 | 12.22 | 12.86 | 41.7 |
|       | ILME   | 155M   | 0.13 | 0.10 | 11.72 | 12.31 | 44.1 |

<span id="page-4-1"></span>Table 2. WERs (%) of 30k-hour E2E models baseline (BS), Shallow Fusion (SF), Density Ratio (DR) and the proposed ILME methods on the out-of-domain LibriSpeech dev-other (Dev) and test-other (Test) set. The external LM is trained with text-only data in LibriSpeech. LM weight µ = λ<sup>S</sup> for DR, and µ = λ<sup>I</sup> for ILME. WERR is the relative WER reduction from BS.

#### <span id="page-4-2"></span>5.3. Intra-Domain Evaluation

We evaluate a multi-conditional E2E model on intra-domain test data by integrating a strong external LM trained with a large amount of multi-domain text-only data. We use the 30K-hour multi-conditional RNN-T or AED model in Section [5.1](#page-3-4) for evaluation.

We train a strong multi-domain word-piece LSTM-LM on a 2Bword text corpus, consisting primarily of conversational data such as talks, interviews, and meeting transcripts. We augmented it with anonymized data from relevant Microsoft services such as short message dictation. With a size of 58M parameters, the 2B-word LSTM-LM has 2 hidden layers with 2048 units for each layer. For Density Ratio, we use the same source-domain LSTM-LM in Section [5.2.](#page-3-5)

We first evaluate the 30K-hour E2E models on the in-domain inhouse dictation test set. With 15K words in total, in-house dictation test set consists of dictation speech collected from keyboard voice input. It has a similar style as the dictation data in 30K corpus and is thus considered as in-domain test data. We use email dictation data with 9K words as the validation set for tuning the LM weights. The results are shown in Table [3.](#page-5-0) All three LM integration methods show relative WER reductions in the range of 2.4%-9.0% from the baseline RNN-T. ILME performs the best achieving 6.8% and 6.0% relative WER reductions compared to shallow fusion and density ratio, respectively. The results for AED are similar to that of RNN-T with ILME performing the best, achieving 12.2%, 4.6% and 4.1% relative WER reductions from AED baseline, Shallow Fusion and Density Ratio, respectively.

Then we evaluate the 30K-hour E2E models on a in-domain inhouse meeting test set. With 5K words in total, in-house meeting set consists of conversation speech collected from real meetings. It has a similar style as the conversation data in 30K-hour corpus, and is thus considered as in-domain test data. Simulated meeting data with 22K words consisting of read meeting transcriptions is used as the validation set. The results are shown in Table [4.](#page-5-1) All three LM integration methods show WER reductions in the range of 0.2%-3.2% relative to the baseline RNN-T. ILME performs the best achieving 2.4% and 3.1% relative WER reductions compared to shallow fusion and density ratio, respectively. The results for AED are similar to that of RNN-T with ILME performing the best, achieving 6.2%, 3.3% and 3.2% relative WER reductions from AED baseline, Shallow Fusion and Density Ratio, respectively.

| E2E   | Method | Params | λT   | µ    | Dictation |      |
|-------|--------|--------|------|------|-----------|------|
| Model |        |        |      |      | WER       | WERR |
| RNN-T | BS     | 76M    | -    | -    | 16.16     | -    |
|       | SF     | 134M   | 0.03 | 0.00 | 15.77     | 2.4  |
|       | DR     | 191M   | 0.21 | 0.19 | 15.64     | 3.2  |
|       | ILME   | 134M   | 0.26 | 0.20 | 14.70     | 9.0  |
| AED   | BS     | 97M    | -    | -    | 14.08     | -    |
|       | SF     | 155M   | 0.09 | 0.00 | 12.96     | 8.0  |
|       | DR     | 212M   | 0.09 | 0.05 | 12.89     | 8.5  |
|       | ILME   | 155M   | 0.13 | 0.08 | 12.36     | 12.2 |

<span id="page-5-0"></span>Table 3. WERs (%) of 30k-hour E2E models baseline (BS), Shallow Fusion (SF), Density Ratio (DR) and the proposed ILME methods on the in-domain in-house dictation test set. The external LM is trained with 2B-word multi-domain text. LM weight µ = λ<sup>S</sup> for DR, and µ = λ<sup>I</sup> for ILME. WERR is the relative WER reduction.

| E2E   | Method | Params | λT   | µ    | Meeting |      |
|-------|--------|--------|------|------|---------|------|
| Model |        |        |      |      | WER     | WERR |
| RNN-T | BS     | 76M    | -    | -    | 20.64   | -    |
|       | SF     | 134M   | 0.02 | 0.00 | 20.47   | 0.8  |
|       | DR     | 191M   | 0.03 | 0.02 | 20.60   | 0.2  |
|       | ILME   | 134M   | 0.08 | 0.03 | 19.97   | 3.2  |
| AED   | BS     | 97M    | -    | -    | 19.46   | -    |
|       | SF     | 155M   | 0.09 | 0.00 | 18.87   | 3.0  |
|       | DR     | 212M   | 0.11 | 0.03 | 18.85   | 3.1  |
|       | ILME   | 155M   | 0.12 | 0.08 | 18.25   | 6.2  |

<span id="page-5-1"></span>Table 4. WERs (%) of 30k-hour E2E models baseline (BS), Shallow Fusion (SF), Density Ratio (DR) and the proposed ILME methods on the in-domain in-house meeting test set. The external LM is trained with 2B-word multi-domain text. LM weight µ = λ<sup>S</sup> for DR, and µ = λ<sup>I</sup> for ILME. WERR is the relative WER reduction from BS.

## 5.4. Result Analysis

By summarizing the results in Sections [5.2](#page-3-5) and [5.3,](#page-4-2) we have the following observations for all test sets in both cross-domain and intra-domain evaluations. For both E2E models, ILME consistently reduces the WER of Shallow Fusion by 8.1%-15.5% relatively in cross-domain evaluation, and 2.4%-6.8% relatively in intra-domain evaluation. ILME also consistently outperforms Density Ratio in terms of lower WER, and achieves the goal with 29.8% and 26.8% fewer run-time parameters with RNN-T and AED, respectively, because ILME does not require an additional source-domain LSTM-LM during beam search.

We also notice that the baseline WER for AED is lower than RNN-T because AED has a bi-directional encoder and has more parameters than RNN-T. With larger relative WER reductions from the AED baseline, all LM integration methods are more effective for AED than for RNN-T. However, the benefit of subtracting internal LM is larger for RNN-T than for AED because ILME gets greater relative WER reductions with RNN-T than with AED from Shallow Fusion. We also notice that, for all three LM integration methods, most of the gains they obtain are transferable from the dev sets to the test sets with both E2E models, showing that they all have good generalization capability.

By comparing cross-domain and intra-domain evaluations, we notice that all LM integration methods obtain much higher relative WER reductions from the baseline E2E model in cross-domain evaluation (LibriSpeech test-clean, test-other sets) than in intra-domain evaluation (in-house dictation, in-house meeting). This is because, in intra-domain evaluation, the E2E training data has been exposed to data with similar language styles as in testing, diminishing the effectiveness of an external LM. However, even on in-domain test data, ILME can still get 3.2%-9.0% relative WER reductions from the baseline RNN-T, significantly larger than the 0.2%-3.2% relative WER reductions obtained by Shallow Fusion and Density Ratio. This shows that the subtraction of internal LM indeed enables a more effective integration of the external LM, and thus a better use of the abundant external knowledge from text-only data.

### 5.5. Internal LM Perplexity

We evaluate the internal LM perplexities (ILM-PPLs) of AED and RNN-T models at different epochs on the validation set of 30K-hour training data which is drawn from the same distribution as the training data. In Fig. [1,](#page-5-2) both ILM-PPLs first decrease and then increase as the E2E models get trained with more data. Both ILM-PPLs fall sharply at initial epochs, but the one of AED begins to increase and then gradually converge at much earlier training stages than that of RNN-T. The significantly larger ILM-PPL of AED than RNN-T suggests that in AED, the decoder needs to work together with the encoder to perform the language modeling. The decoder does not function well as a standalone LM without the encoder input. However, in RNN-T, the prediction network is trained to act like an individual LM and is later combined with the encoder by the joint network.

![](_page_5_Figure_11.svg)

<span id="page-5-2"></span>Fig. 1. The internal LM perplexity of RNN-T and AED as a function of thousand (K) hours of training speech. The perplexity is evaluated on the validation set of the 30K-hour E2E training data.

The ILM-PPLs of the RNN-T and AED used in Sections [5.2](#page-3-5) and [5.3](#page-4-2) are 99.4 and 796.7, respectively, while the source-domain LM trained with 30K-hour training transcript has a PPL of 30.1 on the same data. Given the maximum perplexity of 4000 under uniform distribution over tokens, the internal LM indeed learns, to some extent, the distribution of token sequences through the E2E training.

# 6. CONCLUSION

We propose an internal LM estimation method to effectively integrate an external LM with all pre-existing E2E models without any additional training. The internal LM is approximated by the output of an E2E model when zeroing out its acoustic components. During inference, the internal LM score is subtracted from the log-linear combination of E2E model and LM scores. We evaluate 30K-hour RNN-T and AED models on cross-domain LibriSpeech test sets and intra-domain Microsoft production test sets with different LM integration methods. ILME reduces the WER of Shallow Fusion by 8.1%-15.5% relatively in cross-domain evaluations, and 2.4%-6.8% relatively in intra-domain evaluations. Further, ILME consistently outperforms Density Ratio in terms of better WER despite having 26.8%-29.8% fewer run-time parameters.

### 7. REFERENCES

- <span id="page-6-0"></span>[1] C.-C. Chiu, T. N Sainath, Y. Wu, et al., "State-of-the-art speech recognition with sequence-to-sequence models," in *Proc. ICASSP*. IEEE, 2018, pp. 4774–4778.
- <span id="page-6-1"></span>[2] T. Sainath, Y. He, B. Li, et al., "A streaming on-device end-toend model surpassing server-side conventional model quality and latency," in *Proc. ICASSP*, 2020, pp. 6059–6063.
- <span id="page-6-2"></span>[3] J. Li, R. Zhao, Z. Meng, et al., "Developing RNN-T models surpassing high-performance hybrid models with customization capability," in *Interspeech*, 2020.
- <span id="page-6-3"></span>[4] A. Graves, S. Fernandez, F. Gomez, et al., "Connectionist tem- ´ poral classification: labelling unsegmented sequence data with recurrent neural networks," in *ICML*. ACM, 2006.
- <span id="page-6-4"></span>[5] A. Graves and N. Jaitly, "Towards end-to-end speech recognition with recurrent neural networks," in *International Conference on Machine Learning*, 2014, pp. 1764–1772.
- <span id="page-6-5"></span>[6] A. Hannun, C. Case, J. Casper, et al., "Deep speech: Scaling up end-to-end speech recognition," *arXiv preprint arXiv:1412.5567*, 2014.
- <span id="page-6-6"></span>[7] H. Soltau, H. Liao, and H. Sak, "Neural speech recognizer: Acoustic-to-word lstm model for large vocabulary speech recognition," *Proc. Interspeech*, 2016.
- <span id="page-6-7"></span>[8] J. Li, G. Ye, A. Das, et al., "Advancing acoustic-to-word CTC model," in *Proc. ICASSP*, 2018.
- <span id="page-6-8"></span>[9] A. Graves, "Sequence transduction with recurrent neural networks," *arXiv preprint arXiv:1211.3711*, 2012.
- <span id="page-6-9"></span>[10] M. Jain, K. Schubert, J. Mahadeokar, et al., "RNN-T for latency controlled asr with improved beam search," *arXiv preprint arXiv:1911.01629*, 2019.
- <span id="page-6-10"></span>[11] J. K Chorowski, D. Bahdanau, D. Serdyuk, et al., "Attentionbased models for speech recognition," in *NIPS*, 2015, pp. 577– 585.
- <span id="page-6-11"></span>[12] D. Bahdanau, J. Chorowski, D. Serdyuk, et al., "End-to-end attention-based large vocabulary speech recognition," in *Proc. ICASSP*. IEEE, 2016, pp. 4945–4949.
- <span id="page-6-12"></span>[13] W. Chan, N. Jaitly, Q. Le, and O. Vinyals, "Listen, attend and spell: A neural network for large vocabulary conversational speech recognition," in *Proc. ICASSP*. IEEE, 2016, pp. 4960– 4964.
- <span id="page-6-13"></span>[14] S. Karita, N. Chen, T. Hayashi, et al., "A comparative study on transformer vs RNN in speech applications," in *Proc. ASRU*, 2019.
- <span id="page-6-14"></span>[15] J. Li, Y. Wu, Y. Gaur, et al., "On the comparison of popular end-to-end models for large scale speech recognition," in *Proc. Interspeech*, 2020.
- <span id="page-6-15"></span>[16] G. Hinton, L. Deng, D. Yu, et al., "Deep neural networks for acoustic modeling in speech recognition: The shared views of four research groups," *IEEE Signal Processing Magazine*, vol. 29, no. 6, pp. 82–97, 2012.
- <span id="page-6-16"></span>[17] D. Yu, K. Yao, H. Su, G. Li, and F. Seide, "Kl-divergence regularized deep neural network adaptation for improved large vocabulary speech recognition," in *Proc. ICASSP*, May 2013, pp. 7893–7897.
- <span id="page-6-17"></span>[18] Z. Meng, J. Li, and Y. Gong, "Adversarial speaker adaptation," in *Proc. ICASSP*, 2019.

- <span id="page-6-18"></span>[19] H. Liao, "Speaker adaptation of context dependent deep neural networks," in *Proc. ICASSP*, May 2013.
- <span id="page-6-19"></span>[20] Z. Meng, H. Hu, J. Li, et al., "L-vector: Neural label embedding for domain adaptation," in *Proc. ICASSP*. IEEE, 2020, pp. 7389–7393.
- <span id="page-6-20"></span>[21] P. Swietojanski and S. Renals, "Learning hidden unit contributions for unsupervised speaker adaptation of neural network acoustic models," in *Proc. SLT*. IEEE, 2014, pp. 171–176.
- <span id="page-6-21"></span>[22] J. Li, R. Zhao, J.-T. Huang, and Y. Gong, "Learning smallsize DNN with output-distribution-based criteria.," in *Proc. INTERSPEECH*, 2014, pp. 1910–1914.
- <span id="page-6-22"></span>[23] Z. Meng, J. Li, Y. Gong, et al., "Adversarial teacherstudent learning for unsupervised domain adaptation," in *Proc. ICASSP*. IEEE, 2018, pp. 5949–5953.
- <span id="page-6-23"></span>[24] V. Manohar, P. Ghahremani, D. Povey, et al., "A teacherstudent learning approach for unsupervised domain adaptation of sequence-trained asr models," in *Proc. SLT*. IEEE, 2018, pp. 250–257.
- <span id="page-6-24"></span>[25] Z. Meng, J. Li, Y. Zhao, and Y. Gong, "Conditional teacherstudent learning," in *Proc. ICASSP*, 2019.
- <span id="page-6-25"></span>[26] R. Gemello, F. Mana, S. Scanzio, et al., "Linear hidden transformations for adaptation of hybrid ann/hmm models," *Speech Communication*, vol. 49, no. 10, pp. 827 – 835, 2007.
- <span id="page-6-26"></span>[27] T. Tan, Y. Qian, M. Yin, et al., "Cluster adaptive training for deep neural network," in *Proc. ICASSP*. IEEE, 2015, pp. 4325– 4329.
- <span id="page-6-27"></span>[28] O. Abdel-Hamid and H. Jiang, "Fast speaker adaptation of hybrid nn/hmm model for speech recognition based on discriminative learning of speaker code," in *Proc. ICASSP*, May 2013, pp. 7942–7946.
- <span id="page-6-28"></span>[29] L. Samarakoon and K. C. Sim, "Factorized hidden layer adaptation for deep neural network based acoustic modeling," *IEEE/ACM Transactions on Audio, Speech, and Language Processing*, vol. 24, no. 12, pp. 2241–2250, Dec 2016.
- <span id="page-6-29"></span>[30] Y. Shinohara, "Adversarial multi-task learning of deep neural networks for robust speech recognition.," in *INTERSPEECH*, 2016, pp. 2369–2372.
- <span id="page-6-30"></span>[31] Z. Meng, J. Li, Z. Chen, et al., "Speaker-invariant training via adversarial learning," in *Proc. ICASSP*, 2018.
- <span id="page-6-31"></span>[32] D. Serdyuk, K. Audhkhasi, P. Brakel, B. Ramabhadran, et al., "Invariant representations for noisy speech recognition," in *NIPS Workshop*, 2016.
- <span id="page-6-32"></span>[33] Z. Meng, Z. Chen, V. Mazalov, J. Li, and Y. Gong, "Unsupervised adaptation with domain separation networks for robust speech recognition," in *Proc. ASRU*, 2017.
- <span id="page-6-33"></span>[34] T. Ochiai, S. Watanabe, S. Katagiri, et al., "Speaker adaptation for multichannel end-to-end speech recognition," in *Proc. ICASSP*. IEEE, 2018, pp. 6707–6711.
- <span id="page-6-34"></span>[35] Z. Meng, Y. Gaur, J. Li, and Y. Gong, "Speaker adaptation for attention-based end-to-end speech recognition," *Proc. Interspeech*, 2019.
- <span id="page-6-35"></span>[36] Z. Meng, J. Li, Y. Gaur, and Y. Gong, "Domain adaptation via teacher-student learning for end-to-end speech recognition," in *Proc. ASRU*. IEEE, 2019.
- <span id="page-6-36"></span>[37] C. Gulcehre, O. Firat, K. Xu, et al., "On using monolingual corpora in neural machine translation," *CoRR*, 2015.

- <span id="page-7-0"></span>[38] J. Chorowski and N. Jaitly, "Towards better decoding and language model integration in sequence to sequence models," *CoRR*, vol. abs/1613.02695, 2016.
- <span id="page-7-1"></span>[39] A. Kannan, Y. Wu, P. Nguyen, et al., "An analysis of incorporating an external language model into a sequence-to-sequence model," in *Proc. ICASSP*, 2018.
- <span id="page-7-2"></span>[40] A. Sriram, H. Jun, S. Satheesh, et al., "Cold fusion: Training seq2seq models together with language models," *Proc. Interspeech*, 2018.
- <span id="page-7-3"></span>[41] S. Toshniwal, A. Kannan, C. Chiu, et al., "A comparison of techniques for language model integration in encoder-decoder speech recognition," in *Proc. SLT*. IEEE, 2018, pp. 369–375.
- <span id="page-7-4"></span>[42] F. Stahlberg, J. Cross, and V. Stoyanov, "Simple fusion: Return of the language model," *arXiv preprint arXiv:1809.00125*, 2018.
- <span id="page-7-5"></span>[43] C. Shan, C. Weng, G. Wang, et al., "Component fusion: Learning replaceable language model component for end-toend speech recognition system," in *Proc. ICASSP*. IEEE, 2019, pp. 5361–5635.
- <span id="page-7-6"></span>[44] E. McDermott, H. Sak, and E. Variani, "A density ratio approach to language model fusion in end-to-end automatic speech recognition," in *Proc. ASRU*. IEEE, 2019, pp. 434–441.
- <span id="page-7-7"></span>[45] N. Kanda, X. Lu, and H. Kawai, "Maximum a posteriori based decoding for ctc acoustic models.," in *Interspeech*, 2016, pp. 1868–1872.
- <span id="page-7-8"></span>[46] T. Hori, S. Watanabe, and J. Hershey, "Multi-level language modeling and decoding for open vocabulary end-to-end speech recognition," in *Proc. ASRU*. IEEE, 2017, pp. 287–293.
- <span id="page-7-9"></span>[47] N. Kanda, X. Lu, and H. Kawai, "Maximum-a-posterioribased decoding for end-to-end acoustic models," *IEEE/ACM Transactions on Audio, Speech, and Language Processing*, vol. 25, no. 5, pp. 1023–1034, 2017.
- <span id="page-7-10"></span>[48] E. Variani, D. Rybach, C. Allauzen, et al., "Hybrid autoregressive transducer (hat)," in *Proc. ICASSP*. IEEE, 2020, pp. 6139–6143.
- <span id="page-7-11"></span>[49] R. Sennrich, B. Haddow, and A. Birch, "Neural machine translation of rare words with subword units," *arXiv preprint arXiv:1508.07909*, 2015.
- <span id="page-7-12"></span>[50] A. Paszke, S. Gross, S. Chintala, et al., "Automatic differentiation in pytorch," 2017.
- <span id="page-7-13"></span>[51] F. Beaufays H. Sak, A. Senior, "Long short-term memory recurrent neural network architectures for large scale acoustic modeling," in *Interspeech*, 2014.
- <span id="page-7-14"></span>[52] Z. Meng, S. Watanabe, J. R. Hershey, et al., "Deep long shortterm memory adaptive beamforming networks for multichannel robust speech recognition," in *ICASSP*. IEEE, 2017, pp. 271–275.
- <span id="page-7-15"></span>[53] H. Erdogan, T. Hayashi, J. R. Hershey, et al., "Multi-channel speech recognition: Lstms all the way through," in *CHiME-4 workshop*, 2016, pp. 1–4.
- <span id="page-7-16"></span>[54] J. L. Ba, J. R. Kiros, and G. E Hinton, "Layer normalization," *arXiv preprint arXiv:1607.06450*, 2016.
- <span id="page-7-17"></span>[55] N. Srivastava, G. Hinton, A. Krizhevsky, I. Sutskever, et al., "Dropout: a simple way to prevent neural networks from overfitting," *The Journal of Machine Learning Research*, vol. 15, no. 1, pp. 1929–1958, 2014.

- <span id="page-7-18"></span>[56] Z. Meng, Y. Gaur, J. Li, and Y. Gong, "Character-aware attention-based end-to-end speech recognition," in *Proc. ASRU*. IEEE, 2019.
- <span id="page-7-19"></span>[57] Y. Gaur, J. Li, Z. Meng, and Y. Gong, "Acoustic-to-phrase endto-end speech recognition," in *submitted to INTERSPEECH 2019*. IEEE, 2019.
- <span id="page-7-20"></span>[58] S. Bengio, O. Vinyals, N. Jaitly, et al., "Scheduled sampling for sequence prediction with recurrent neural networks," in *NeurIPS*, pp. 1171–1179. Curran Associates, Inc., 2015.
- <span id="page-7-21"></span>[59] V. Panayotov, G. Chen, D. Povey, et al., "Librispeech: an asr corpus based on public domain audio books," in *Proc. ICASSP*. IEEE, 2015, pp. 5206–5210.
- <span id="page-7-22"></span>[60] A. Mnih and Y. W. Teh, "A fast and simple algorithm for training neural probabilistic language models," *arXiv preprint arXiv:1206.6426*, 2012.