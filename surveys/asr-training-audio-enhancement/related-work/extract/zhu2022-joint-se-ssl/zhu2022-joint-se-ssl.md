**Source:** *Joint Training of Speech Enhancement and Self-supervised Model for Noise-robust ASR* — [PDF](https://arxiv.org/pdf/2205.13293v1) · [arXiv](https://arxiv.org/abs/2205.13293v1)

# Joint Training of Speech Enhancement and Self-supervised Model for Noise-robust ASR

Qiu-Shi Zhu, Jie Zhang, Zi-Qiang Zhang, Li-Rong Dai

*Abstract*—Speech enhancement (SE) is usually required as a front end to improve the speech quality in noisy environments, while the enhanced speech might not be optimal for automatic speech recognition (ASR) systems due to speech distortion. On the other hand, it was shown that self-supervised pre-training enables the utilization of a large amount of unlabeled noisy data, which is rather beneficial for the noise robustness of ASR. However, the potential of the (optimal) integration of SE and selfsupervised pre-training still remains unclear. In order to find an appropriate combination and reduce the impact of speech distortion caused by SE, in this paper we therefore propose a joint pre-training approach for the SE module and the selfsupervised model. First, in the pre-training phase the original noisy waveform or the waveform obtained by SE is fed into the self-supervised model to learn the contextual representation, where the quantified clean speech acts as the target. Second, we propose a dual-attention fusion method to fuse the features of noisy and enhanced speeches, which can compensate the information loss caused by separately using individual modules. Due to the flexible exploitation of clean/noisy/enhanced branches, the proposed method turns out to be a generalization of some existing noise-robust ASR models, e.g., enhanced wav2vec2.0. Finally, experimental results on both synthetic and real noisy datasets show that the proposed joint training approach can improve the ASR performance under various noisy settings, leading to a stronger noise robustness.

*Index Terms*—Wav2vec2.0, speech recognition, speech enhancement, self-supervised pre-training, noise robustness.

## I. INTRODUCTION

T HE field of automatic speech recognition (ASR) has grown rapidly in the past few years owing to the advance in neural network-based acoustic models [\[1\]](#page-10-0)–[\[3\]](#page-10-1) and largescale training. Compared to conventional GMM-HMM counterparts, these neural network-based end-to-end methods [\[4\]](#page-10-2)– [\[6\]](#page-10-3) have a simple training procedure and can bring greater performance improvements. Although extensive progress has been achieved in ASR on clean speech, the performance would degrade sharply in the presence of background noise or under low signal-to-noise-ratio (SNR) conditions. Therefore, improving the noise robustness of ASR systems under such conditions still remains a challenge.

Regarding the noise robustness of the monaural ASR, many algorithms have been proposed recently, which can be

Manuscript created May, 2022; This work was supported by the National Natural Science Foundation of China (No. 62101523), Fundamental Research Funds for the Central Universities and the Leading Plan of CAS (XDC08010200). (Corresponding author: Jie Zhang.)

The authors are with the National Engineering Research Center of Speech and Language Information Processing (NERC-SLIP), University of Science and Technology of China (USTC), Hefei 230026, China (e-mail: qszhu@mail.ustc.edu.cn; jzhang6@ustc.edu.cn; zz12375@mail.ustc.edu.cn; lrdai@ustc.edu.cn).

categorized into two classes. The first category follows the structure that combines a speech enhancement (SE) module as a front-end ASR module, in which the SE module and the ASR module can be trained separately or jointly. For the SE module, one can use traditional methods [\[7\]](#page-10-4), [\[8\]](#page-10-5) or neural network-based methods, which can be implemented in the time domain [\[9\]](#page-10-6)–[\[13\]](#page-10-7) or in the frequency domain [\[14\]](#page-10-8)–[\[16\]](#page-10-9). The time-domain SE reconstructs the target speech directly using the raw waveform, while the frequency-domain SE usually first estimates a mask matrix using the spectrum and then computes the spectrum of the target speech via multiplying the mask matrix by the noisy speech spectrum. In case the SE and ASR modules are trained separately [\[17\]](#page-10-10), since the training target of SE is usually related to the instrumental speech quality, e.g., mean-square error (MSE), speech distortion, SNR, the enhanced speech might be distorted in terms of intelligibility and thus not be optimal for ASR in terms of, e.g., word error rate (WER) [\[13\]](#page-10-7), [\[18\]](#page-10-11). The resulting ASR performance is highly dependent on the SE module. To alleviate the mismatch between SE and ASR modules, a method of jointly training SE and ASR modules was proposed in [\[19\]](#page-10-12)–[\[22\]](#page-10-13). Specifically, a joint adversarial augmentation training approach was proposed in [\[22\]](#page-10-13), where a joint training framework is designed to optimize mask-based augmentation networks and attentionbased encoder-decoder speech recognition networks. However, this method only uses enhanced features as input for ASR, which still suffers from the problem of speech distortion. The impact of speech distortion on ASR was analyzed in [\[23\]](#page-10-14), and it was shown in [\[17\]](#page-10-10), [\[20\]](#page-10-15), [\[21\]](#page-10-16), [\[23\]](#page-10-14) that fusing noisy features and enhanced features can further alleviate the speech distortion issue and improve the ASR performance.

The second noise-robust ASR category mainly focuses on self-supervised pre-training. As self-supervised pre-training has shown a superiority for neural network models to leverage a large amount of unlabeled data that are widely available, many self-supervised methods for speech representation learning have been proposed recently in the speech community. For example, autoregressive predictive coding (APC) [\[24\]](#page-10-17) was proposed to reconstruct the future frames based on the past frames. Contrastive predictive coding (CPC) [\[25\]](#page-10-18) and wav2vec [\[26\]](#page-10-19) perform the next-step prediction similarly but using a contrastive loss. Meanwhile, the contextual speech representations can be learned from the unlabeled speech data by reconstructing the masked input speech frames [\[27\]](#page-10-20), [\[28\]](#page-10-21). For contextual speech representation learning, the bidirectional Transformer (BERT) structure [\[29\]](#page-10-22) is utilized in [\[27\]](#page-10-20), and the bidirectional long short-term memory (LSTM) structure is used in [\[28\]](#page-10-21). Vq-wav2vec [\[30\]](#page-10-23) utilizes a quantization module to extract discrete semantic units from unlabeled speech data and then uses BERT to perform contextual modeling on the extracted units. Wa2vec2.0 [\[31\]](#page-10-24) employs a convolutional neural network (CNN) to extract local features from the raw waveform, which are then input to the BERT module to perform mask prediction using a contrastive loss. HUBERT [\[32\]](#page-10-25) performs offline clustering on representations, which enables a direct prediction of the clustering label of the masked positions. In addition, on the basis of the HUBERT framework, UniSpeech-SAT [\[33\]](#page-10-26) and WavLM [\[34\]](#page-10-27) were proposed to boost the spoken content information and speaker identity using an utterance-wise contrastive loss and an utterance mixing data augmentation method, respectively.

It was shown in [\[35\]](#page-10-28), [\[36\]](#page-10-29) that a modified CPC pretrained model can be transferred well across domains, and larger pre-training datasets lead the ASR model to be much more robust against the domain shift. The robust wav2vec2.0 proposed in [\[37\]](#page-10-30) reveals the impact of domain mismatch on the self-supervised speech representation learning. The problem-agnostic speech encoder (PASE+) that was proposed in [\[38\]](#page-10-31) introduces online speech data augmentation modules for self-supervised learning and obtains a good performance in noisy environments. Wav2vec-switch [\[39\]](#page-10-32) encodes the noise robustness into contextualized representations of speech via contrastive learning. In [\[40\]](#page-10-33), an extra reconstruction module was used for auxiliary learning to improve the noise robustness of the learned representation. Consistency contrastive learning method [\[41\]](#page-11-0) was utilized for acoustic pre-training, which shows a WER improvement on both the in-domain data and the out-domain data. By taking the quantized clean speech as the training target for pre-training, we proposed an enhanced wav2vec2.0 in [\[42\]](#page-11-1), resulting in a better speech representation.

In principal, both SE and self-supervised pre-training based methods can improve the noise robustness of ASR to some extent, but from different perspectives. The SE based methods require careful adjustments for network training, while selfsupervised methods can utilize more unlabeled noisy data to pre-train and then directly fine-tune the pre-trained models to improve the noise robustness, which usually have less speech distortion issues compared to the former. A new question arises *whether an appropriate combination can improve the noise robustness consistently and reduce the impact of speech distortion caused by SE*. To our knowledge, there are few works on this question, e.g., in [\[43\]](#page-11-2), a trained SE module, a trained selfsupervised module for feature extraction, and a trained ASR module are integrated into an end-to-end framework, which is then fine-tuned altogether and achieves the best performance on the CHiME-4 [\[44\]](#page-11-3) single-channel ASR task. However, in case this model is trained using random initialization, the performance or convergence cannot be guaranteed due to the network depth and gradient back propagation.

In this work, we therefore explore a joint pre-training method incorporating SE and self-supervised training to improve the noise robustness of ASR. This work is an extension of the conference paper in [\[42\]](#page-11-1), where only the structure of the enhanced wav2vec2.0 model and results on the synthetic data were shown. Compared to [\[42\]](#page-11-1), the contribution of this paper is threefold. First, we propose a joint pre-training approach for the DEMUCS [\[13\]](#page-10-7) based time-domain SE module and the enhanced wav2vec2.0 based self-supervised model. In the pre-training stage, the original noisy waveform or the waveform after SE is fed to the self-supervised model to learn the contextual representation, and the quantized clean speech provides the target for the pre-training model. Second, we propose a dual-attention fusion module to fuse the features of the noisy and enhanced speeches, such that the information loss caused by the SE can be compensated. Third, the proposed pre-training model is validated using both synthetic data and the real noisy CHiME-4 dataset. Results show that adding consistency constraints on the features output from the feature encoder and using the quantized clean features as targets for the pre-training model are beneficial for the noise robustness of the ASR model on both datasets. In addition, it is shown that the SE module and the self-supervised model can jointly improve the ASR performance in noisy scenes, and the dualattention fusion module can reduce the effect of distortion caused by SE. Finally, we find that using a pre-trained model for initialization can also mitigate the speech distortion and improve the ASR performance, which is theoretically analyzed from the viewpoint of numerical optimization.

The remainder of the paper is arranged as follows. In Section II, we present the proposed noise-robust self-supervised pre-training model including the enhanced wav2vec2.0 model, the SE module, dual-attention fusion and the joint pre-training technique. Experimental setups are described in Section III, followed by extensive experimental results and analysis in Section IV. Finally, Section V concludes this work.

# II. METHODOLOGY

In this section, we will present the proposed self-supervised pre-training model, including the enhanced wav2vec2.0 (EW2), the time-domain SE module, the proposed dualattention fusion module and the joint pre-training technique.

# *A. The enhanced wav2vec2.0 (EW2) model*

The proposed enhanced wav2vec2.0 model is based on the classic wav2vec2.0 [\[31\]](#page-10-24), and the corresponding model structure is shown in Fig. [1,](#page-2-0) which also consists of a feature encoder f : X 7→ Z, a Transformer encoder g : Z 7→ C and a vector quantization (VQ) g : Z 7→ Q. The feature encoder utilizes seven CNN layers and the Transformer encoder contains twelve transformer blocks. Specifically, the shared feature encoder extracts the noisy features Znoisy from the raw noisy waveform Xnoisy and extracts the clean features Zclean from the raw clean waveform Xclean, respectively, which can then be described as

<span id="page-1-0"></span>
$$Z_{\text{noisy}} = f(X_{\text{noisy}}), \quad Z_{\text{clean}} = f(X_{\text{clean}}).$$
 (1)

We mask a certain proportion of the noisy features Znoisy by replacing with a learnable vector at the masked position. Then, the high-level noisy contextualized representations Cnoisy are learned from the noisy features Znoisy by the Transformer encoder, which is given by

$$C_{\text{noisy}} = g(Z_{\text{noisy}}).$$
 (2)

The corresponding clean features  $Z_{\rm clean}$  are discretized into  $q_{\rm clean}$  via a VQ module, which are then used as clean targets in the contrastive objective, i.e.,

<span id="page-2-6"></span>
$$q_{\text{clean}} = VQ(Z_{\text{clean}}).$$
 (3)

The motivation of using clean features as the target originates from the expectation that the model can learn clean speech representations from noisy features. The involved VQ module is implemented using the product quantization [45]. Specifically, the VQ module first maps the clean features  $Z_{\rm clean}$  to logits  $1 \in \mathbb{R}^{G \times V}$ , where G represents the number of codebooks and V the number of entries in each codebook. The gumbel softmax function [46] is then used to select discrete codebook entries in a fully differentiable way. As a result, for a given frame  $Z_{{\rm clean}_t}$  at time t, we can select one entry from each codebook, concatenate the resulting vectors  $e_1,...,e_G$  and apply a linear transformation to obtain  $q_{{\rm clean}_t}$ . The loss function can therefore be formulated as

<span id="page-2-1"></span>
$$L = L_m + \alpha L_d + \beta L_f + \gamma L_c, \tag{4}$$

where

$$L_m = -\log \frac{\exp(\operatorname{sim}(C_{\operatorname{noisy}_t}, q_{\operatorname{clean}_t})/\kappa)}{\sum_{\tilde{q} \sim Q_t} \exp(\operatorname{sim}(C_{\operatorname{noisy}_t}, \tilde{q})/\kappa)},$$
 (5)

$$L_d = \frac{1}{GV} \sum_{g=1}^{G} \sum_{v=1}^{V} \overline{p}_{g,v} \log \overline{p}_{g,v}, \tag{6}$$

$$\overline{p}_{g,v} = \frac{\exp(\overline{l}_{g,v} + n_v)/\tau}{\sum_{k=1}^{V} \exp(\overline{l}_{g,k} + n_k)/\tau},$$
(7)

$$L_c = \|Z_{\text{noisy}} - Z_{\text{clean}}\|_2, \tag{8}$$

which applies to any time index t. It is clear that the total loss function is the weighted summation over four terms depending on the parameters  $\alpha$ ,  $\beta$  and  $\gamma$ . In (4),  $L_m$  is the contrastive loss, which enables the model to distinguish between the true quantized clean features  $q_{\text{clean}_t}$  and a set of K+1 quantized candidate features  $\tilde{q} \in Q_t$ . The quantized candidate features  $\tilde{q}$ contains  $q_{\text{clean}_t}$  and K distractors. The diversity loss  $L_d$  aims to increase the use of quantized codebook features, and  $L_f$ is an  $\ell_2$  penalty over the outputs of the feature encoder. In (5), sim stands for the cosine similarity between two vectors and  $\kappa$  is a temperature. In (6),  $\overline{p}_{q,v}$  represents the probability of choosing the v-th codebook entry for group g across a batch of utterances, where  $\tau$  is a temperature. In (7),  $\bar{l}_{q,v}$ stands for the average logits 1 across utterances in a batch. In order to ensure the consistency between the clean features and the noisy features corrupted by noise, we additionally introduce a consistency loss  $L_c$  in (8), which measures the Euclidean distance between noisy features  $Z_{\rm noisy}$  and clean features  $Z_{\text{clean}}$ .

## B. Speech enhancement (SE) module

Many time-domain and frequency-domain SE models have been proposed in literature. The superiority of time-domain SE methods is that no specific operations on the phase information are required for generating estimated signals and the combination with existing self-supervised models is straightforward. In

![](_page_2_Figure_13.svg)

<span id="page-2-0"></span>Fig. 1. The structure of the enhanced wav2vec2.0 model.

<span id="page-2-5"></span><span id="page-2-4"></span><span id="page-2-3"></span><span id="page-2-2"></span>principal, any type of SE models can be employed in the proposed self-supervised pre-training approach. Without loss of generality, we choose the time-domain DEMUCS model [13] for SE, which is built by optimizing both the time-domain and frequency-domain loss functions. DEMUCS consists of a five-layer convolutional encoder, a two-layer LSTM network and a five-layer convolutional decoder. The encoder includes several convolution layers (where the number of input channels in the first convolution layer is  $H_{\rm se}$ , the convolution kernel size of the *i*-th encoder layer is  $K_{se}$ , the convolution stride is  $S_{\rm se}$  and the number of output channels is  $2^{i-1}H_{\rm se}$ ), a ReLU activation and a  $1\times1$  convolution with  $2^iH_{\rm se}$  output channels. Then, a gated linear units (GLU) activation converts the output channels back to  $2^{i-1}H_{se}$ . Next, the LSTM network is applied to the output of the encoder to model the sequential hidden state. For the decoder, the number of input channels of the i-th transposed convolution layer is  $2^{i-1}H_{se}$ , followed by a  $1\times1$  convolution with  $2^iH_{\rm se}$  channels and a GLU activation that outputs  $2^{i-1}H_{se}$  channels. It is worth noting that a skip connection between the outputs of the i-th encoder layer and the *i*-th decoder layer is required.

The DMEUCS considers both time-domain and frequency-domain loss functions, where the time-domain loss function on the waveform is  $\ell_1$  loss and the frequency-domain one relies on the multi-resolution short-time Fourier transform (STFT) coefficients. Suppose X and  $X_{\rm en}$  represent the clean speech waveform signal and the enhanced speech waveform signal, respectively, the loss function can be written as

<span id="page-2-7"></span>
$$L_{\rm SE} = \frac{1}{T} \left( \|X - X_{\rm en}\|_1 + \sum_{i=1}^{M} L_{\rm stft}^{(i)}(X, X_{\rm en}) \right), \quad (9)$$

where M is the number of STFT losses, the first term represents the time-domain loss on the waveform, and the second term denotes the loss on STFT coefficients, which is defined as the sum of spectral convergence (sc) loss and magnitude loss, i.e.,

$$L_{\text{stft}}(X, X_{\text{en}}) = L_{\text{sc}}(X, X_{\text{en}}) + L_{\text{mag}}(X, X_{\text{en}}),$$
 (10)

where

$$L_{\rm sc}(X, X_{\rm en}) = \frac{\||\text{STFT}(X)| - |\text{STFT}(X_{\rm en})|\|_F}{\|\text{STFT}(X)\|_F},$$
(11)

$$L_{\text{mag}}(X, X_{\text{en}}) = \frac{1}{T} \|\log|\text{STFT}(X)| - \log|\text{STFT}(X_{\text{en}})|\|_{1},$$
(12)

where  $\|\cdot\|_F$  and  $\|\cdot\|_1$  denote the Frobenius and  $\ell_1$  norms, respectively, and STFT $(\cdot)$  returns the STFT coefficient matrix. As such, the multi-resolution  $L_{\rm stft}^{(i)}$  can utilize the STFT loss at different resolutions with the number of FFT bins, e.g.,  $\in$  {512, 1024, 2048}, hop sizes  $\in$  {50, 120, 240}, and window lengths  $\in$  {240, 600, 1200}. For more details about DEMUCS, please refer to [13].

#### C. The dual-attention fusion module

In order to learn the complementary information of the noisy features and enhanced features, we propose a dual attention fusion module on the basis of the classic attention mechanism [29], which is shown in Fig. 2. In the left branch, the enhanced features  $Z_{\rm en}$  and the noisy features  $Z_{\rm noisy}$  are used to calculate the attention weight, and the output is the weighted sum of the noisy features  $Z_{\rm noisy}$ . Similarly, in the right branch, attention weights are calculated from noisy features  $Z_{\rm noisy}$  and enhanced features  $Z_{\rm en}$ , and the output is the weighted sum of enhanced features  $Z_{\rm en}$ . The fused feature is then the summation over the outputs of the two branches, given by

<span id="page-3-1"></span>
$$Z_{\text{fusion}} = \text{Linear}(\text{Multihead}(Z_{\text{en}}, Z_{\text{noisy}}, Z_{\text{noisy}})) + \text{Linear}(\text{Multihead}(Z_{\text{noisy}}, Z_{\text{en}}, Z_{\text{en}})),$$
 (13)

which involves a linear mapping layer, and the multi-head attention is formulated as

$$Multihead(Z_O, Z_K, Z_V) = Concat(h_1, ..., h_n)W^O, \quad (14)$$

where  $Z_Q$ ,  $Z_K$  and  $Z_V$  can be replaced by  $Z_{\rm noisy}$  or  $Z_{\rm en}$ . The scaled dot-product attention is calculated as

$$h_{i} = \operatorname{Attention}(Z_{Q}W_{i}^{Q}, Z_{K}W_{i}^{K}, Z_{V}W_{i}^{V})$$

$$= \operatorname{softmax}\left(\frac{Z_{Q}W_{i}^{Q}(Z_{K}W_{i}^{K})^{T}}{\sqrt{d_{k}}}\right)Z_{V}W_{i}^{V} \qquad (15)$$

where  $d_k$  equals the dimension  $d_z$  of  $Z_{\text{noisy}}$  over h (i.e.,  $d_k = d_z/h$ ), and  $W_i^Q \in \mathbb{R}^{d_z \times d_k}$ ,  $W_i^K \in \mathbb{R}^{d_z \times d_k}$ ,  $W_i^V \in \mathbb{R}^{d_z \times d_k}$  and  $W_i^O \in \mathbb{R}^{d_z \times d_z}$  are learnable parameters.

## D. Joint training for SE and EW2

The model structure of the proposed pre-training approach is shown in Fig. 3(a), where both the SE module in Section II-B and the back-end self-supervised module in Section II-A are included. As shown in (1), the input raw noisy waveform  $X_{\rm noisy}$  and raw clean waveform  $X_{\rm clean}$  are sent to the shared feature encoder to output the noisy features  $Z_{\rm noisy}$  and the clean features  $Z_{\rm clean}$ , respectively. The noisy speech  $X_{\rm noisy}$  is also sent to the SE module to obtain the enhanced speech  $X_{\rm en}$ , i.e.,

$$X_{\rm en} = {\rm enhancer}(X_{\rm noisy}),$$
 (16)

![](_page_3_Picture_16.svg)

Fig. 2. An illustration of the proposed dual-attention fusion module.

<span id="page-3-0"></span>which is then sent to the shared feature encoder to construct the enhanced features  $Z_{\rm en}$  as

$$Z_{\rm en} = f(X_{\rm en}). \tag{17}$$

The noisy features and enhanced features are fused using a convolutional fusion module to obtain the final fused features as in (13). The fused feature  $Z_{\text{fusion}}$  is randomly masked at a certain proportion and then sent to the Transformer module to learn the contextual representation  $C_{\text{fusion}}$ , which is given by

$$C_{\text{fusion}} = q(Z_{\text{fusion}}).$$
 (18)

On the other hand, the corresponding clean features  $Z_{\rm clean}$  are discretized into  $q_{\rm clean}$  via a VQ module following  $Z\mapsto Q$  in (3), which are then used as clean targets in the contrastive objective. It is worth mentioning that the clean speech signal is only used in the pre-training stage but not in the fine-tuning stage. The overall loss function of the proposed joint training strategy can thus be formulated as

<span id="page-3-4"></span><span id="page-3-3"></span><span id="page-3-2"></span>
$$L_{\text{total}} = L_{\text{contrastive}} + \xi L_{\text{SE}}.$$
 (19)

where  $L_{\rm SE}$  was given in (9) and  $L_{\rm contrastive}$  can be formulated similarly as that in Section II-A, e.g.,

<span id="page-3-5"></span>
$$L_{\text{contrastive}} = L_{ms} + \alpha L_d + \beta L_f + \gamma L_{cs}, \qquad (20)$$

where

$$L_{ms} = -\log \frac{\exp(\sin(C_{\text{fusion}_t}, q_{\text{clean}_t})/\kappa)}{\sum_{\tilde{q} \sim O_t} \exp(\sin(C_{\text{fusion}_t}, \tilde{q})/\kappa)},$$
 (21)

$$L_{cs} = \|Z_{\text{noisy}_t} - Z_{\text{clean}_t}\|_2 + \|Z_{\text{en}_t} - Z_{\text{clean}_t}\|_2.$$
 (22)

In (21),  $L_{ms}$  is the contrastive loss between the contextual representation  $C_{\rm fusion}$  and a set of quantized candidate features  $\tilde{q}$ . In (22),  $L_{cs}$  is the consistency loss function between  $Z_{\rm noisy}$ ,  $Z_{\rm en}$  and  $Z_{\rm clean}$ . The loss function of  $L_d$  and  $L_f$  keep the same as in (4), and  $\alpha$ ,  $\beta$ ,  $\gamma$ ,  $\xi$  in (19) and (20) are the weighting parameters, which can be set empirically.

It should be noted that based on the pre-training structure in Fig. 3(a), apart from the proposed joint pre-training framework (i.e., all three branches and the dual-attention fusion are involved, thus termed by EW2+SEW2), one can further construct several noise-robust ASR models. For example, in

![](_page_4_Figure_2.svg)

<span id="page-4-0"></span>Fig. 3. An illustration of the proposed joint pre-training model: (a) pre-training sub-model and (b) fine-tuning sub-model.

case only the left branch ① and the right clean speech branch are used, the proposed model reduces to the off-the-shelf EW2 model [\[42\]](#page-11-1). In case the left branch ② and the right clean speech branch are available, the proposed model is equivalent to the SE-based EW2 (SEW2). In case the dualattention fusion module is replaced by simple concatenation, the model reduces to EW2+SEW2 (concat), which would have less parameters than the proposed EW2+SEW2. Therefore, the proposed method can be seen as a generalization of EW2 and SEW2 that make use of the clean speech for noise-robust ASR. In Section IV, these variants will also be compared.

In the fine-tuning stage, we removed the right clean speech branch in Fig. [3\(](#page-4-0)a), and the corresponding model structure is shown in Fig. [3\(](#page-4-0)b). We add an additional linear mapping layer to the output of the Transformer encoder and optimize the whole model using the connectionist temporal classification (CTC) [\[47\]](#page-11-6) loss function with a small amount of labeled data. Note that in case the noisy and clean branches are used in the pre-training stage (i.e., EW2), the same noisy branch is required for fine-tuning. This applies to other variants, that is, the branch combination for pre-training and fine-tuning should be kept consistent.

# III. EXPERIMENTAL SETUP

In this section, the datasets for model validation and experimental configuration on pre-training and fine-tuning will be described in detail.

## *A. Dataset description*

LibriSpeech: In order to facilitate a fair comparison with existing approaches, the data usage throughout experiments keeps exactly the same as that in [\[48\]](#page-11-7). Specifically, we utilize the LibriSpeech [\[49\]](#page-11-8) train-clean-100 subset and train-clean-360 subset as the clean speech training set and standard devclean subset as the validation set. For the model training and validation, we randomly select noise samples and mix with the clean speech additively at an arbitrarily chosen SNR from [0 dB, 25 dB] to generate noisy data. The noisy test set is downloaded from the website[1](#page-4-1) , which includes 4200 noisy audio streams generated by selecting 120 clean speech samples from the test-clean subset of LibriSpeech and then mixing with noises at different SNRs ∈ {0, 5, 10, 15, 20} dB. The noise data used in experiments originate from FreeSound [\[50\]](#page-11-9), which are sampled at a sampling frequency of 16 kHz. The noise type is divided into two categories, i.e., A and B. The type-A noise is relatively stationary, including 'Car', 'Metro' and 'Traffic' noise, and the type-B noise is relatively nonstationary, including 'Babble', 'Airport/Station', 'Cafe' and 'AC/Vacuum' noise. Each noise type has 10 and 8 different audio streams in the training and test sets, respectively. The length of the noise dataset is around 2 hours in total. In addition, we also utilize the NoiseX-92 [\[51\]](#page-11-10) noise dataset at the pre-training stage for supplementary experiments.

CHiME-4: To further verify the effectiveness of the proposed method on real noisy data, we conduct experiments on the CHiME-4 challenge[2](#page-4-2) dataset [\[44\]](#page-11-3). The CHiME-4 dataset is related to the text from the Wall Street Journal (WSJ0) corpus, which was collected using a six-channel distant microphone array and a close-talk microphone for data recording when the volunteer is reading the corresponding text. This dataset contains two types of noisy speech, i.e., real and artificially simulated noisy speech. The real noisy data was recorded in the noisy environments including bus, cafe, pedestrian area, and street junction, and the artificial simulation data was synthesized by mixing the four kinds of noise with the clean speech. The training set contains 1600 real recorded and 7138 simulated noisy utterances, the validation set contains 1640

<span id="page-4-1"></span><sup>1</sup>https://github.com/archiki/Robust-E2E-ASR

<span id="page-4-2"></span><sup>2</sup>http://spandh.dcs.shef.ac.uk/chime challenge/CHiME4/index.html

TABLE I

<span id="page-5-1"></span>THE PERFORMANCE COMPARISON OF DIFFERENT METHODS ON TYPE-A AND TYPE-B NOISE TEST SETS AT DIFFERENT SNRS, WHERE "NO" MEANS THAT THE PRE-TRAINING STEP IS NOT INCLUDED AND WAV2VEC2.0 IS FINE-TUNED DIRECTLY FROM SCRATCH WITH THE TARGET DATASET. THE PRE-TRAINING AND FINE-TUNING CAN BE PERFORMED ON DIFFERENT DATASETS.

|                     |           |           | WER under SNR (dB) |                     |               |       |              |       |       |         |       |
|---------------------|-----------|-----------|--------------------|---------------------|---------------|-------|--------------|-------|-------|---------|-------|
| Method              | Pre-train | Fine-tune | Type-B noise       |                     |               |       | Type-A noise |       |       | Average | Clean |
| Method              |           |           | Babble             | Airport/<br>Station | AC/<br>Vacuum | Cafe  | Traffic      | Metro | Car   | Average | Cican |
|                     |           |           | 0~20               | 0~20                | 0~20          | 0~20  | 0~20         | 0~20  | 0∼20  | 0~20    | -     |
| Baseline [48]       | No        | Clean     | 87.70              | 72.06               | 70.58         | 58.74 | 51.94        | 46.34 | 25.16 | 58.93   | 10.3  |
| DEMUCS [48]         | FreeSound | FreeSound | 45.56              | 36.98               | 38.20         | 27.02 | 26.46        | 23.22 | 16.02 | 30.49   | 10.9  |
| AvT [48]            | No        | FreeSound | 43.42              | 35.32               | 36.62         | 27.06 | 27.88        | 24.28 | 17.76 | 30.33   | 13.1  |
|                     | No        | Clean     | 81.74              | 70.20               | 67.88         | 57.40 | 50.24        | 46.58 | 23.60 | 56.81   | 11.0  |
|                     | No        | FreeSound | 59.40              | 50.88               | 49.96         | 43.58 | 40.36        | 37.78 | 29.94 | 44.56   | 25.0  |
| Wav2vec2.0 [42]     | Clean     | FreeSound | 47.50              | 39.68               | 38.84         | 31.14 | 29.22        | 27.44 | 18.24 | 33.15   | 14.0  |
|                     | FreeSound | FreeSound | 39.56              | 32.50               | 34.94         | 25.22 | 24.52        | 22.48 | 16.24 | 27.92   | 13.5  |
|                     | NoiseX-92 | FreeSound | 43.18              | 34.16               | 38.80         | 27.06 | 25.58        | 24.64 | 18.08 | 30.21   | 16.1  |
| EW/2 [42]           | FreeSound | FreeSound | 33.88              | 27.36               | 27.94         | 22.08 | 20.94        | 19.84 | 14.88 | 23.85   | 12.3  |
| EW2 [42]            | NoiseX-92 | FreeSound | 38.80              | 30.12               | 30.94         | 22.72 | 22.06        | 20.96 | 15.98 | 25.94   | 14.3  |
| SEW2                | No        | FreeSound | 50.50              | 42.68               | 41.96         | 34.88 | 32.62        | 31.60 | 22.86 | 36.73   | 19.1  |
| SEW2                | FreeSound | FreeSound | 39.64              | 33.90               | 33.28         | 26.90 | 25.54        | 24.88 | 18.26 | 28.91   | 15.4  |
| EW2 + SEW2 (concat) | No        | FreeSound | 47.44              | 39.64               | 41.60         | 32.04 | 31.82        | 30.24 | 22.32 | 35.01   | 18.5  |
| EW2 + SEW2          | No        | FreeSound | 44.54              | 36.00               | 36.12         | 29.28 | 27.00        | 25.64 | 18.76 | 31.05   | 15.6  |
| EW2 + SEW2 (concat) | FreeSound | FreeSound | 33.24              | 26.91               | 27.52         | 21.78 | 20.63        | 19.62 | 14.60 | 23.47   | 12.2  |
| EW2 + SEW2          | FreeSound | FreeSound | 31.55              | 25.90               | 26.83         | 21.22 | 19.75        | 19.04 | 14.25 | 22.65   | 12.2  |

real recorded and 1640 simulated noisy utterances, and the test set contains 1320 real recorded and 1320 simulated noisy utterances. All these three data subsets were constructed from four different speakers. As the focus of this paper is on the single-channel ASR, the data of all six channels will be used as training data in the fine-tuning stage, and one-channel track real noisy data is used as validation and test sets, which is similar to the data configuration in [39], [40].

#### B. Model configuration

**Pre-train on 100 hours unlabeled data:** This configuration means that we pre-train on 100 hours of clean-noisy paired speech data from the train-clean-100 subset of LibriSpeech, where the noisy speech data is generated by using clean speech dynamically mixing with noise. The model structure is implemented using the fairseq toolkit<sup>3</sup>. In detail, the feature encoder consists of seven convolutional layers and the channel number of the convolution module is 512. The stride and kernel sizes of the convolution module are (5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,

For the Transformer encoder module, we utilize 12 Transformer encoder layers and each contains a self-attention module and a feed forward module. The dimension of the self-attention module is 512, and 8 heads are utilized. The dimension of the feed forward module is 512, and the inner dimension is 2048. For the VQ module, we set G=2 and V=320, and the dimension of each entry is 128. The model size including all parameters is around 45 M. For masking, we sample at all time steps at a probability of p=0.065 and mask the subsequent M=10 time steps. For the loss function, the temperature  $\kappa$  is set to be 0.1, and  $\tau$  is annealed from 2 to 0.5 with a coefficient of 0.999995 in terms of iterations.

The parameters  $\alpha$ ,  $\beta$ ,  $\gamma$  and  $\xi$  are set to be 0.1, 10, 1 and 0.1, respectively. The number of distractors K equals 100.

**Pre-train on 460 hours unlabeled data:** This configuration means that we pre-train on 460 hours of clean-noisy paired speech from the train-clean-100 subset and train-clean-360 subset of LibriSpeech, where the noisy speech data is generated similarly as before. The main difference from the previous configuration lies in the size of the model parameters, where the size of the model parameters is around 95 M. The dimension of the self-attention module is 768, and the number of attention heads is 12. The dimension of the feed forward module is 768, and the inner dimension is 2048. The rest parameters keep the same as the first configuration.

Fine-tune on 100 hours labeled data: During fine-tuning, we use the noisy speech at different SNRs to fine-tune the model, where the generation of noisy data remains the same as that in the pre-training phase. The model also uses a data augmentation method similarly to SpecAugment [52], where a time-frequency mask is applied to the feature output by the feature encoder. The time masking probability is 0.065, and 10 consecutive frames are masked. The frequency masking probability is 0.05, and 32 consecutive channels are masked. The modeling unit has 30 characters, including 26 letters and 4 special symbols. After fine-tuning, we decode on clean test sets and noisy test sets without any language model (LM) and calculate the WER for performance evaluation.

**Pre-train and Fine-tune on CHiME-4 data:** For a fair comparison with existing approaches, we adopt the same data configuration therein. Both real and simulated data from all channels except for the second microphone channel are utilized for pre-training and fine-tuning. Due to the small data size of CHiME-4 data, pre-training with random initialization cannot guarantee an acceptable performance, so we continue pre-training 50k updates based on the public pre-

<span id="page-5-0"></span><sup>3</sup>https://github.com/pytorch/fairseq

7

trained model<sup>4</sup> and then fine-tune 20k updates with labeled data. Note that the public pre-trained model was pre-trained using 960 hours speech data of LibriSpeech, which has about 95 M parameters. We also apply the time-frequency masking for data augmentation and fine-tune the model with the CTC loss function. Since the results from e.g., [39], [40] on the CHiME-4 dataset employ LMs, we train a Transformer-based word-level LM with a vocabulary of 65,000 using the text portion of the WSJ corpus.

The Transformer-based LM contains a 16-layer encoder, where both the encoder and self-attention dimensions are 512 and the inner dimension of the feed forward neural network is 2048. The loss function is cross-entropy, which is optimized using the Adam optimizer. The training process of LM is implemented using the fairseq toolkit. We utilize a simple shallow fusion to integrate external LMs, which are integrated by calculating the weighted distributions of two modeling units, i.e., one from the ASR model and the other from the external Transformer LM. The weight of the LM is 1.0, and the beam size is 500.

For the SE module,  $H_{\rm se}$ ,  $K_{\rm se}$  and  $S_{\rm se}$  are set to be 64, 8 and 4, respectively. For the dual-attention fusion module, the dimension of  $Z_{\rm noisy}$  is set to be 512, the number of attention head h is set to be 8, and the dimension of each head  $d_k$  equals 64. The dimension of the linear mapping layer is 512.

#### IV. RESULTS AND ANALYSIS

In this section, we will present extensive experimental results to evaluate the effectiveness of the proposed method.

## A. Evaluation of the proposed EW2

Comparison methods: The Baseline in [48] utilizes the Deepspeech2 model [53] for training on the LibriSpeech train-clean-100 dataset with a CTC objective function and evaluates on different test sets. For completeness, the time-domain DEMUCS as a front-end SE step in [48] will be compared, where the enhanced speech is directly used for ASR. The AvT method utilized in [48] introduces a gradient reversal layer in prior to the model classification layer, such that the learned speech representations can be noise-invariant. In addition, the proposed EW2 model will also be compared with the original wav2vec2.0 method [31]. Note that different combinations of pre-training and fine-tuning branches in Fig. 3 will be considered in experiments.

Table I shows the ASR performances in terms of WER of the aforementioned approaches using the type-A (relatively stationary) and type-B (non-stationary) noises under different SNR conditions. The average performance is obtained by averaging the WERs over all input SNRs and noise types. From Table I, it can be seen that although the structure of the proposed model is different from [48], the proposed baseline system (i.e., wav2vec2.0 no pre-train clean fine-tune) achieves a comparable performance as compared to the baseline in [48]. For wav2vec2.0, comparing 'no pre-train clean fine-tune', it

<span id="page-6-1"></span>TABLE II
THE AVERAGE WER UNDER DIFFERENT SNRS W/O THE VQ MODULE
USING CLEAN OR NOISY TARGETS IN THE PRE-TRAINING STAGE.

| Method | Target type | Vector quantization | Average WER (SNR $\in$ 0 $\sim$ 20 dB) |  |  |
|--------|-------------|---------------------|----------------------------------------|--|--|
| EW2    | Clean       | ×                   | 27.82<br>28.70                         |  |  |
| EW2    | Noisy       | ×                   | 33.06<br>34.46                         |  |  |

is clear that fine-tuning on noisy datasets can improve the ASR performance under most noise conditions, that is, the noise robustness can be improved. As the combination of 'clean pre-train FreeSound fine-tune' obtains a much better performance than 'no pre-train FreeSound fine-tune' in both noisy and clean environments, the inclusion of a pre-training phase is rather beneficial for the robustness of ASR models. Comparing 'clean pre-train FreeSound fine-tune' and 'FreeSound pre-train FreeSound fine-tune' (the latter performs better), we find that the wav2vec2.0 model can still learn a robust speech representation under noisy scenarios. Compared to DEMUCS or AvT, although wav2vec2.0 (i.e., FreeSound pre-train FreeSound fine-tune) can improve the performance on the test set under various noisy conditions, the performance on the clean test set drops significantly.

In order to see whether the wav2vec2.0 model is robust to noise types, we use the NoiseX-92 noise dataset to dynamically add noise to the train-clean-100 subset to obtain a noisy dataset for pre-training and then perform fine-tuning on noisy data. From Table I, we can see that the choice of 'NoiseX-92 pre-train FreedSound fine-tune' for wav2vec2.0 is better than the 'no pre-train FreedSound fine-tune' counterpart, indicating that the representations obtained by pre-training on other types of noisy data still have a good robustness. However, as the choice of 'FreeSound pre-train FreeSound fine-tune' leads to a decrease in WER compared to 'NoiseX-92 pretrain FreeSound fine-tune', the data sources for pre-training and fine-tuning affects the performance of wav2vec2.0. That is, the noise data for pre-training and fine-tuning originating from different domains might degrade the ASR performance. This phenomenon also applies to the results of EW2.

More importantly, from Table I we can see that the combination of 'FreedSound pre-train FreedSound fine-tune' for the proposed EW2 method is better than the same choice for wav2vec2.0 under both noisy and clean conditions. Using the clean speech as the pre-training targets can improve the performance on the noisy test set, and it is also ensured that the performance on the clean test set is not significantly degraded. In addition, the proposed EW2 method with 'NoiseX-92 pre-train FreedSound fine-tune' outperforms the wav2vec2.0 counterpart, indicating that a better robustness against different noise types is obtained. Besides, although the proposed EW2 approach works slightly worse than DEMUCS on the clean test set, the performance under more-commonly noisy conditions is much better.

<span id="page-6-0"></span><sup>&</sup>lt;sup>4</sup>https://dl.fbaipublicfiles.com/fairseq/wav2vec/wav2vec\_small.pt

<span id="page-7-0"></span>TABLE III
THE AVERAGE WER UNDER DIFFERENT SNRS W/O THE CONSISTENCY
LOSS IN THE PRE-TRAINING STAGE.

| Method | Consistency<br>loss | Average WER (SNR ∈ 0~20 dB) |  |  |  |  |  |
|--------|---------------------|-----------------------------|--|--|--|--|--|
| EW2    | <b>✓</b>            | 27.82                       |  |  |  |  |  |
| EW2    | Х                   | 29.23                       |  |  |  |  |  |

### B. Evaluation on the necessity of VQ and consistency loss

In order to better understand the function of the VQ module, we conduct comparative experiments using clean and noisy targets, and the results are shown in Table II. It is obvious that for both target types in the pre-training stage, the performance of using the VQ module can be improved compared to the case of without VQ, indicating the necessity of the VQ module in noisy scenes. As the WER reduction of using clean targets is larger than using noisy ones, the clean targets in the pre-training stage are beneficial for speech representation learning.

We further compare the performance of the proposed EW2 model with or without the consistency loss function in Table III. It is clearly shown that introducing a consistency loss function in the output of the feature encoder can improve the ASR performance. In order to show the necessity of the consistency loss, we visualize the normalized  $\ell_2$  distance between clean and noisy features at different layers in Fig. 4. The distance between low-level clean features and noisy features is larger, and high-level clean features and noisy features have smaller distances, indicating that low-level features are more susceptible to noise interference. Therefore, adding a consistency loss function to low-level features can reduce the distance between clean features and noisy features and enhance the noise robustness of ASR models.

#### C. Evaluation on joint training of SE and EW2

We evaluate the effectiveness of the proposed joint training of SE and EW2 on type-A and type-B noise test sets, which are shown at the bottom of Table I. For SEW2, comparing 'no pre-train FreeSound fine-tune' and 'FreeSound pre-train FreeSound fine-tune' it is clear that introducing an additional pre-training stage can improve the performance. However, comparing 'FreeSound pre-train FreeSound fine-tune' of SEW2 and 'FreeSound pre-train FreeSound fine-tune' of EW2, the performance of SEW2 is worse than that of EW2, that is, only feeding the noisy speech to the SE module together with a random initialization for pre-training cannot guarantee a robust speech representation. This is due to the fact that the SE operation would cause the speech distortion problem, which deteriorates the representation quality of the model in the pre-training stage. To alleviate this problem, we adopt the dual-attention fusion module in Section III-C to fuse the noisy feature and enhanced feature in the pre-training stage, such that the fused context information can be learned. Under the 'no pre-train FreeSound fine-tune' condition, comparing EW2 + SEW2 and SEW2 methods we find that in case the model is directly fine-tuned with random initialization even without pre-training, the fusion of noisy features and enhanced features can improve the performance. Under the 'FreeSound pre-train

![](_page_7_Figure_9.svg)

<span id="page-7-1"></span>Fig. 4. The normalized  $\ell_2$  distance between clean and noisy representations at different layers, where layer 0 represents the feature encoder.

FreeSound fine-tune' condition, comparing EW2, SEW2 and EW2 + SEW2 methods, it is clear that the latter performs the best, meaning that fusing the noisy and enhanced features in the pre-training stage can alleviate the speech distortion problem and thus reduce the WER. Comparing EW2+SEW2 (concat) and EW2+SEW2, the latter clearly performs better in the cases of both 'no pre-train FreeSound fine-tune' and 'FreeSound pre-train FreeSound fine-tune'. This implies that the proposed dual attention fusion method outperforms the classic concatenation technique for feature fusion.

To verify the effectiveness of the proposed method on a larger dataset, we use 460 hours of LibriSpeech clean-noisy data to continue pre-train our model initialized with the public pre-trained wav2vec2.0 model for 50k updates, which is then fine-tuned on the noisy data. The experimental results on type-B noise test sets are shown in Table IV. In the case of SEW2, the joint training of the SE module and the self-supervised model with random initialization cannot obtain a good representation. In case a pre-trained self-supervised model is utilized for initialization, no matter whether the feature encoder is updated or not, the performance is much better than the case without a pre-trained model as initialization, indicating that an off-the-shelf pre-trained model can potentially decrease the impact of speech distortion to a certain extent. Besides, as the entire model is updated with a small learning rate in the fine-tuning stage, the front-end SE module is adjusted in line with the back-end ASR, leading to a performance gain. Comparing the EW2, SEW2 and EW2+SEW2 methods, EW2+SEW2 can achieve a very promising WER regardless of the inclusion of a pre-trained model as initialization. That is, the proposed joint training method for SE and self-supervised speech representation learning is robust against model setup and noise conditions.

#### D. Analysis of the importance of initialization

In order to further investigate the effect of the random initialization for the SE module and the self-supervised model (e.g., SEW2 method in Table IV) on the speech representation learning, we visualize the loss function on the validation set versus the number of training epochs in the pre-training stage

| T    | ۸I   | 2 T | $\mathbf{F}$ | TV  | 7 |
|------|------|-----|--------------|-----|---|
| - 1/ | -\ п | 7 I | ъF.          | 1 V |   |

<span id="page-8-0"></span>The performance comparison of different methods on type-A noise test sets at different SNRs when pre-train on 460 hours librispeech data and fine-tune on 100 hours librispeech data. SE stands for speech enhancement module and FE stands for feature encoder module in Fig. 3.

|            | Initialize with    | Update | Update   | WER under SNR |                 |           |         |         |  |
|------------|--------------------|--------|----------|---------------|-----------------|-----------|---------|---------|--|
| Method     | pre-trained model  | SE     | FE       | Babble        | Airport/Station | AC/Vacuum | Cafe    | Average |  |
| ļ          | pre-trained inoder | SE     | FE       | 0~20 dB       | 0~20 dB         | 0~20 dB   | 0~20 dB | 0~20 dB |  |
| EW2        | <b>✓</b>           | -      | <b>✓</b> | 20.96         | 16.06           | 15.74     | 12.16   | 16.23   |  |
| SEW2       | ×                  | 1      | /        | 35.12         | 29.94           | 29.16     | 23.22   | 29.36   |  |
| SEW2       | ✓                  | 1      | ×        | 20.04         | 15.20           | 14.96     | 11.56   | 15.44   |  |
| SEW2       | ✓                  | /      | /        | 19.64         | 14.92           | 14.68     | 11.42   | 15.17   |  |
| EW2 + SEW2 | ✓                  | /      | /        | 18.63         | 14.36           | 14.06     | 11.16   | 14.55   |  |
| EW2 + SEW2 | ×                  | 1      | ✓        | 19.56         | 14.59           | 14.43     | 11.32   | 14.98   |  |

![](_page_8_Figure_5.svg)

<span id="page-8-1"></span>Fig. 5. The validation contrastive loss versus the number of training epochs in the pre-training stage.

![](_page_8_Figure_7.svg)

<span id="page-8-2"></span>Fig. 6. The 1D loss curves, where the blue and orange curves represent fine-tuning EW2 and training from scratch, respectively.

in Fig. 5. It can be seen that with the addition of the SE module, the loss on the validation set in the pre-training stage drops rapidly. This reveals that the SE operation would cause speech distortion and smooth the detailed information contained in speech, and the contextual representation becomes easier to be leveraged for the prediction of the masked information in the pre-training stage, which, however degrades the quality or fidelity of the learned speech representation.

We further analyze the effect of the application of an offthe-shelf pre-trained self-supervised model for initialization on the robust speech representation learning (e.g., SEW2 method in Table IV). In principal, a pre-trained self-supervised model has potential to enable a good initial point, which is rather conducive for the model optimization to converge. To show this, we follow the method in [54], [55] and visualize the one-dimensional (1D) and two-dimensional (2D) loss landscape of the model that is fine-tuned on the 100 hours LibriSpeech data, which can be initialized either randomly or using an existing pre-trained model, so that we can compare the difference between two learning paradigms. Let  $\theta_0$  represent the initial parameters, which can then denote the pre-trained parameters of fine-tuning EW2 or the randomly initialized parameters of training from scratch. Let  $\theta_1$  denote the model parameters after fine-tuning. The 1D loss curve function f(m) shows the loss value along the searching direction, which is defined as

$$f(m) = J(\boldsymbol{\theta}_0 + m\boldsymbol{\delta}_1),$$

where m is a scalar,  $\delta_1 = \theta_1 - \theta_0$  is the optimization direction, and  $J(\theta)$  is the loss function given  $\theta$ . For the brevity of visualization, we set  $m \in [-2, 3]$  and discretize the 1D loss curve. Similarly, the 2D loss surface function is defined as

$$f(m,n) = J(\boldsymbol{\theta}_0 + m\boldsymbol{\delta}_1 + n\boldsymbol{\delta}_2),$$

where m, n are scalars. One optimization direction is  $\delta_1$  $\theta_1 - \theta_0$  and the other is  $\delta_2 = \theta_2 - \theta_0$ , where  $\theta_2$  represents the fine-tuned parameters on another dataset. We set the range of both m and n to be [-2, 2] and sample 21 points at each axis. It is clear that in case m=0 and n=0,  $\theta_0$  denotes the initial point, and in case m=1 and n=0,  $\theta_0+\delta_1$  is the ending point of model optimization. The 1D and 2D loss curves are shown in Fig. 6 and Fig. 7, respectively. It can be seen that fine-tuning with a pre-trained model has a wider optimal area than fine-tuning with a random initialization model, which means that in case of using a pre-trained model, the slight turbulence of the model parameters can not seriously affect the model performance. In addition, fine-tuning with a pre-trained model results in a smoother loss surface near the starting point than fine-tuning with random initialization, which indicates that the pre-trained model provides a better initialization point and it becomes easier and faster for the model to converge to the optimal status. Therefore, when using a pre-trained selfsupervised model, adding an extra SE module can easily find the optimum and thus improve the model performance.

<span id="page-9-1"></span>TABLE V THE PERFORMANCE COMPARISON OF DIFFERENT METHODS ON CHIME-4 ONE-CHANNEL DATASET.

|                                      |             | WER       |           |  |  |
|--------------------------------------|-------------|-----------|-----------|--|--|
| Model                                | LM          | dt05 real | et05 real |  |  |
| Supervised                           |             |           |           |  |  |
| DNN baseline [44]                    | N-gram      | 11.6      | 23.7      |  |  |
| Du et al. [56]                       | LSTM        | 4.5       | 9.2       |  |  |
| Menne et al. [57]                    | LSTM        | 5.1       | 9.3       |  |  |
| Wang et al. [15]                     | LSTM        | 3.5       | 6.8       |  |  |
| Self-supervised                      |             |           |           |  |  |
| Wang et al.(960h) [40]               | LSTM        | 5.0       | 9.0       |  |  |
| Wang et al.(60kh) [40]               | LSTM        | 2.8       | 5.8       |  |  |
| Wav2vec2.0 Base [41]                 | None        | 10.3      | 17.8      |  |  |
| Gao et al. [41]                      | None        | 8.7       | 15.8      |  |  |
|                                      | None        | 10.6      | 17.6      |  |  |
| Wav2vec2.0 Base [39]                 | LSTM        | 3.7       | 7.2       |  |  |
|                                      | None        | 10.0      | 16.5      |  |  |
| Wav2vec-switch [39]                  | LSTM        | 3.5       | 6.6       |  |  |
|                                      | None        | 10.4      | 17.0      |  |  |
| HUBERT Base [32]                     | LSTM        | 3.8       | 7.1       |  |  |
|                                      | None        | 10.5      | 17.3      |  |  |
| Wav2vec2.0 Base (Ours) [42]          | Transformer | 3.8       | 7.5       |  |  |
|                                      | None        | 9.4       | 15.6      |  |  |
| EW2 (Ours) [42]                      | Transformer | 3.5       | 6.4       |  |  |
| Speech enhancement + self-supervised |             |           |           |  |  |
| Chang et al. [43]                    | Transformer | 2.03      | 3.92      |  |  |
|                                      | None        | 8.2       | 14.3      |  |  |
| EW2 + SEW (Ours)                     | Transformer | 3.0       | 5.9       |  |  |

![](_page_9_Figure_4.svg)

<span id="page-9-0"></span>Fig. 7. The 2D loss surfaces of fine-tuning EW2 (left) and training from scratch (right), where the bottom row is obtained via rotating.

# *E. Performance evaluation on the CHiME-4 dataset*

Finally, we validate the proposed method in realistic noisy scenes using the CHiME-4 dataset. The experimental results are shown in Table [V.](#page-9-1) The one-channel real-world noisy data 'dt05 real' and 'et05 real' are utilized for model validation and evaluation, respectively. For comparison, we also include the results of some supervised and self-supervised methods. The top part of Table [V](#page-9-1) shows the representative state-of-theart results on single-channel data using supervised methods, most of which employ extensive data augmentation and auxiliary data processing techniques, e.g., speaker adaptation and model fusion. The middle part shows the representative selfsupervised pre-training methods on the single-channel data. Self-supervised pre-training methods utilize a large amount of unlabeled data for pre-training and are fine-tuned on a much smaller amount of labeled dataset, which do not require complex data processing operations. For example, Wang et al. [\[40\]](#page-10-33) utilized a large pre-trained model to achieve a WER of 2.8 on the dt05 real validation set and a WER of 5.8 on the et05 real test set, which is even better than the best supervised method [\[15\]](#page-10-34) with a WER of 3.5 on the dt05 real validation set and a WER of 6.8 on the et05 real test set. For the self-supervised pre-training methods, without an LM, the proposed EW2 [\[42\]](#page-11-1) achieves a WER of 9.4 on the validation set and a WER of 15.6 on the test set, which performs better than wav2vec-swith with a WER of 10.0 on the validation set and a WER of 16.5 on the test set. With the inclusion of LM models, their performance becomes comparable. For the proposed joint training method without LM, the WER on the validation set is 8.2 and the WER on the test set is 14.3, which is about 10% relative improvement compared to EW2. Applying a Transformer-based LM, the performance gain of the proposed method is consistently achieved. These also show that the LM is rather beneficial for improving the ASR performance. It is worth mentioning that to the best of our knowledge Chang et al. [\[43\]](#page-11-2) achieves the best result on the monaural CHiME-4 ASR task so far with a WER of 2.03 on the validation set and a WER of 3.92 on the test set. In [\[43\]](#page-11-2), the self-supervised pre-trained WavLM model is taken as the feature extractor, the trained SE module and the trained ASR model are fine-tuned in a cascaded fashion, and all modules are pre-trained separately. This independent pre-training and fine-tuning would have a serious performance drop in case the model is not carefully initialized. For example, as shown in [\[43\]](#page-11-2) in the case of random initialization, the performance or the convergence cannot be guaranteed, due to the fact that the model depth is too large and the gradient back propagation is blocked. As the source code of [\[43\]](#page-11-2) has not been published, the implementation details are still unknown. As in practice random initialization is more promising for training and easier for implementation, the proposed method reaches the state-ofthe-art performance from this perspective.

# V. CONCLUSION

In this paper, we investigated the jointly pre-training of the SE and the self-supervised model for noise-robust ASR, in which the original noisy waveform or the waveform after SE is fed into the self-supervised model to learn the contextual representation and the quantified clean speech provides targets for the pre-training model. The deployment of noisy, enhancement and clean branches allows for several noise-robust ASR variants, which turns out the generality of the proposed joint training approach. We also proposed a dual-attention module for the feature fusion. It was shown that both the SE and the self-supervised model can improve the ASR performance in noisy scenes. Besides, the dual-attention fusion module can compensate the information loss in separately using SE or pre-training models and thus reduce the distortion caused by SE to a certain extent. The inclusion of VQ operations and a consistency loss between clean and noisy features is also important for improving the noise robustness in practical noisy environments. Although the proposed method can be initilized randomly, we found that using a pre-trained model for initialization can further reduce the speech distortion and reduce the WER, which was verified based on the optimization theory. Compared to [\[43\]](#page-11-2), which requires a careful model initialization, the proposed method exhibits a more promising robustness against random initialization as the sacrifice in performance is quite small. This is rather important for the implementation of noise-robust ASR systems in practice. In the future, we will consider the joint training for speech intelligibility enhancement and self-supervised pre-training models, which might potentially reduce the perceptual instrumental speech distortion compared to the MSE-based SE models, as the speech intelligibility is more related to the ASR capability.

# REFERENCES

- <span id="page-10-0"></span>[1] G. Hinton, L. Deng, D. Yu, G. E. Dahl, A. Mohamed, N. Jaitly, A. Senior, V. Vanhoucke, P. Nguyen, T. N. Sainath, and B. Kingsbury, "Deep neural networks for acoustic modeling in speech recognition: The shared views of four research groups," *IEEE Signal Process. Mag.*, vol. 29, no. 6, pp. 82–97, 2012.
- [2] A. Graves and N. Jaitly, "Towards end-to-end speech recognition with recurrent neural networks," in *Int. Conf. Machine Learning (ICML)*, 2014, pp. 1764–1772.
- <span id="page-10-1"></span>[3] J. K. Chorowski, D. Bahdanau, D. Serdyuk, K. Cho, and Y. Bengio, "Attention-based models for speech recognition," in *Proc. of NIPS*, vol. 28, 2015, pp. 577–585.
- <span id="page-10-2"></span>[4] W. Xiong, L. Wu, F. Alleva, J. Droppo, X. Huang, and A. Stolcke, "The microsoft 2017 conversational speech recognition system," in *IEEE Int. Conf. Acoust., Speech, Signal Process.*, 2018, pp. 5934–5938.
- [5] S. Kim, T. Hori, and S. Watanabe, "Joint ctc-attention based end-toend speech recognition using multi-task learning," in *IEEE Int. Conf. Acoust., Speech, Signal Process.*, 2017, pp. 4835–4839.
- <span id="page-10-3"></span>[6] L. Dong, S. Xu, and B. Xu, "Speech-transformer: A no-recurrence sequence-to-sequence model for speech recognition," in *IEEE Int. Conf. Acoust., Speech, Signal Process.*, 2018, pp. 5884–5888.
- <span id="page-10-4"></span>[7] S. Boll, "Suppression of acoustic noise in speech using spectral subtraction," *IEEE/ACM Trans. Audio, Speech, Lang. Process.*, vol. 27, no. 2, pp. 113–120, 1979.
- <span id="page-10-5"></span>[8] P. Scalart and J. Filho, "Speech enhancement based on a priori signal to noise estimation," in *IEEE Int. Conf. Acoust., Speech, Signal Process.*, vol. 2, 1996, pp. 629–632.
- <span id="page-10-6"></span>[9] Y. Luo and N. Mesgarani, "Tasnet: Time-domain audio separation network for real-time, single-channel speech separation," in *IEEE Int. Conf. Acoust., Speech, Signal Process.*, 2018, pp. 696–700.
- [10] A. Pandey and D. Wang, "Tcnn: Temporal convolutional neural network for real-time speech enhancement in the time domain," in *IEEE Int. Conf. Acoust., Speech, Signal Process.*, 2019, pp. 6875–6879.
- [11] Y. Luo and N. Mesgarani, "Conv-tasnet: Surpassing ideal time-frequency magnitude masking for speech separation," *IEEE/ACM Trans. Audio, Speech, Lang. Process.*, vol. 27, no. 8, pp. 1256–1266, 2019.
- [12] A. Pandey and D. Wang, "A new framework for cnn-based speech enhancement in the time domain," *IEEE/ACM Trans. Audio, Speech, Lang. Process.*, vol. 27, no. 7, pp. 1179–1188, 2019.
- <span id="page-10-7"></span>[13] A. D´efossez, G. Synnaeve, and Y. Adi, "Real Time Speech Enhancement in the Waveform Domain," in *ISCA Interspeech*, 2020, pp. 3291–3295.
- <span id="page-10-8"></span>[14] F. Weninger, H. Erdogan, S. Watanabe, E. Vincent, J. L. Roux, J. R. Hershey, and B. Schuller, "Speech enhancement with lstm recurrent neural networks and its application to noise-robust asr," in *Proc. of LVA/ICA*. Springer, 2015, pp. 91–99.
- <span id="page-10-34"></span>[15] Z.-Q. Wang, P. Wang, and D. Wang, "Complex spectral mapping for single- and multi-channel speech enhancement and robust asr," *IEEE/ACM Trans. Audio, Speech, Lang. Process.*, vol. 28, pp. 1778– 1787, 2020.
- <span id="page-10-9"></span>[16] M. H. Soni, N. Shah, and H. A. Patil, "Time-frequency masking-based speech enhancement using generative adversarial network," in *IEEE Int. Conf. Acoust., Speech, Signal Process.*, 2018, pp. 5039–5043.
- <span id="page-10-10"></span>[17] M. Fujimoto and H. Kawai, "One-pass single-channel noisy speech recognition using a combination of noisy and enhanced features." in *ISCA Interspeech*, 2019, pp. 486–490.

- <span id="page-10-11"></span>[18] K. Han, Y. Wang, D. Wang, W. S. Woods, I. Merks, and T. Zhang, "Learning spectral mapping for speech dereverberation and denoising," *IEEE/ACM Trans. Audio, Speech, Lang. Process.*, vol. 23, no. 6, pp. 982–992, 2015.
- <span id="page-10-12"></span>[19] Z.-Q. Wang and D. Wang, "A joint training framework for robust automatic speech recognition," *IEEE/ACM Trans. Audio, Speech, Lang. Process.*, vol. 24, no. 4, pp. 796–806, 2016.
- <span id="page-10-15"></span>[20] C. Fan, J. Yi, J. Tao, Z. Tian, B. Liu, and Z. Wen, "Gated recurrent fusion with joint training framework for robust end-to-end speech recognition," *IEEE/ACM Trans. Audio, Speech, Lang. Process.*, vol. 29, pp. 198–209, 2020.
- <span id="page-10-16"></span>[21] Y. Hu, N. Hou, C. Chen, and E. Siong Chng, "Interactive feature fusion for end-to-end noise-robust speech recognition," in *IEEE Int. Conf. Acoust., Speech, Signal Process.*, 2022, pp. 6292–6296.
- <span id="page-10-13"></span>[22] B. Liu, S. Nie, S. Liang, W. Liu, M. Yu, L. Chen, S. Peng, C. Li *et al.*, "Jointly adversarial enhancement training for robust end-to-end speech recognition." in *ISCA Interspeech*, 2019, pp. 491–495.
- <span id="page-10-14"></span>[23] K. Iwamoto, T. Ochiai, M. Delcroix, R. Ikeshita, H. Sato, S. Araki, and S. Katagiri, "How bad are artifacts?: Analyzing the impact of speech enhancement errors on asr," *arXiv preprint arXiv:2201.06685*, 2022.
- <span id="page-10-17"></span>[24] Y.-A. Chung, W.-N. Hsu, H. Tang, and J. Glass, "An Unsupervised Autoregressive Model for Speech Representation Learning," in *ISCA Interspeech*, 2019, pp. 146–150.
- <span id="page-10-18"></span>[25] A. v. d. Oord, Y. Li, and O. Vinyals, "Representation learning with contrastive predictive coding," *arXiv preprint arXiv:1807.03748*, 2018.
- <span id="page-10-19"></span>[26] S. Schneider, A. Baevski, R. Collobert, and M. Auli, "Wav2vec: Unsupervised Pre-Training for Speech Recognition," in *ISCA Interspeech*, 2019, pp. 3465–3469.
- <span id="page-10-20"></span>[27] A. T. Liu, S.-W. Li, and H.-y. Lee, "Tera: Self-supervised learning of transformer encoder representation for speech," *IEEE/ACM Trans. Audio, Speech, Lang. Process.*, vol. 29, pp. 2351–2366, 2021.
- <span id="page-10-21"></span>[28] S. Ling, Y. Liu, J. Salazar, and K. Kirchhoff, "Deep contextualized acoustic representations for semi-supervised speech recognition," in *IEEE Int. Conf. Acoust., Speech, Signal Process.*, 2020, pp. 6429–6433.
- <span id="page-10-22"></span>[29] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin, "Attention is all you need," *Proc. of NIPS*, vol. 30, pp. 6000–6010, 2017.
- <span id="page-10-23"></span>[30] A. Baevski, S. Schneider, and M. Auli, "Vq-wav2vec: Selfsupervised learning of discrete speech representations," *arXiv preprint arXiv:1910.05453*, 2019.
- <span id="page-10-24"></span>[31] A. Baevski, Y. Zhou, A. Mohamed, and M. Auli, "Wav2vec 2.0: A framework for self-supervised learning of speech representations," in *Proc. of NIPS*, 2020, pp. 12 449–12 460.
- <span id="page-10-25"></span>[32] W.-N. Hsu, B. Bolte, Y.-H. H. Tsai, K. Lakhotia, R. Salakhutdinov, and A. Mohamed, "Hubert: Self-supervised speech representation learning by masked prediction of hidden units," *IEEE/ACM Trans. Audio, Speech, Lang. Process.*, vol. 29, pp. 3451–3460, 2021.
- <span id="page-10-26"></span>[33] S. Chen, Y. Wu, C. Wang, Z. Chen, Z. Chen, S. Liu, J. Wu, Y. Qian, F. Wei, J. Li, and X. Yu, "Unispeech-sat: Universal speech representation learning with speaker aware pre-training," in *IEEE Int. Conf. Acoust., Speech, Signal Process.*, 2022, pp. 6152–6156.
- <span id="page-10-27"></span>[34] S. Chen, C. Wang, Z. Chen, Y. Wu, S. Liu, Z. Chen, J. Li, N. Kanda, T. Yoshioka, X. Xiao *et al.*, "Wavlm: Large-scale selfsupervised pre-training for full stack speech processing," *arXiv preprint arXiv:2110.13900*, 2021.
- <span id="page-10-28"></span>[35] K. Kawakami, L. Wang, C. Dyer, P. Blunsom, and A. van den Oord, "Learning robust and multilingual speech representations," in *Empirical Methods in Natural Language Process.: Findings*, 2020, pp. 1182–1192.
- <span id="page-10-29"></span>[36] M. Riviere, A. Joulin, P.-E. Mazar ` e, and E. Dupoux, "Unsupervised ´ pretraining transfers well across languages," in *IEEE Int. Conf. Acoust., Speech, Signal Process.*, 2020, pp. 7414–7418.
- <span id="page-10-30"></span>[37] W. Hsu, A. Sriram, A. Baevski, T. Likhomanenko, Q. Xu, V. Pratap, J. Kahn, A. Lee, R. Collobert, G. Synnaeve *et al.*, "Robust wav2vec 2.0: Analyzing domain shift in self-supervised pre-training," *arXiv preprint arXiv:2104.01027*, 2021.
- <span id="page-10-31"></span>[38] M. Ravanelli, J. Zhong, S. Pascual, P. Swietojanski, J. Monteiro, J. Trmal, and Y. Bengio, "Multi-task self-supervised learning for robust speech recognition," in *IEEE Int. Conf. Acoust., Speech, Signal Process.*, 2020, pp. 6989–6993.
- <span id="page-10-32"></span>[39] Y. Wang, J. Li, H. Wang, Y. Qian, C. Wang, and Y. Wu, "Wav2vecswitch: Contrastive learning from original-noisy speech pairs for robust speech recognition," in *IEEE Int. Conf. Acoust., Speech, Signal Process.*, 2022, pp. 7097–7101.
- <span id="page-10-33"></span>[40] H. Wang, Y. Qian, X. Wang, Y. Wang, C. Wang, S. Liu, T. Yoshioka, J. Li, and D. Wang, "Improving noise robustness of contrastive speech representation learning with speech reconstruction," in *IEEE Int. Conf. Acoust., Speech, Signal Process.*, 2022, pp. 6062–6066.

- <span id="page-11-0"></span>[41] C. Gao, G. Cheng, Y. Guo, Q. Zhao, and P. Zhang, "Data augmentation based consistency contrastive pre-training for automatic speech recognition," *arXiv preprint arXiv:2112.12522*, 2021.
- <span id="page-11-1"></span>[42] Q.-S. Zhu, J. Zhang, Z.-Q. Zhang, M.-H. Wu, X. Fang, and L.-R. Dai, "A noise-robust self-supervised pre-training model based speech representation learning for automatic speech recognition," in *IEEE Int. Conf. Acoust., Speech, Signal Process.*, 2022, pp. 3174–3178.
- <span id="page-11-2"></span>[43] X. Chang, T. Maekaku, Y. Fujita, and S. Watanabe, "End-to-end integration of speech recognition, speech enhancement, and self-supervised learning representation," *arXiv preprint arXiv:2204.00540*, 2022.
- <span id="page-11-3"></span>[44] T. Menne, J. Heymann, A. Alexandridis, K. Irie, A. Zeyer, M. Kitza, P. Golik, I. Kulikov, L. Drude, R. Schluter, and et al., "The ¨ rwth/upb/forth system combination for the 4th chime challenge evaluation," in *Proc. of CHiME-4 Workshop*, 2016, pp. 49–51.
- <span id="page-11-4"></span>[45] H. Jegou, M. Douze, and C. Schmid, "Product quantization for nearest neighbor search," *IEEE Trans. Pattern Analysis & Machine Intelligence* , vol. 33, no. 1, pp. 117–128, 2010.
- <span id="page-11-5"></span>[46] E. Jang, S. Gu, and B. Poole, "Categorical reparameterization with gumbel-softmax," in *Proc. of ICLR*, 2017.
- <span id="page-11-6"></span>[47] A. Graves, S. Fernandez, F. Gomez, and J. Schmidhuber, "Connectionist ´ temporal classification: labelling unsegmented sequence data with recurrent neural networks," in *Int. Conf. Machine Learning (ICML)*, 2006, pp. 369–376.
- <span id="page-11-7"></span>[48] A. Prasad, P. Jyothi, and R. Velmurugan, "An investigation of end-toend models for robust speech recognition," in *IEEE Int. Conf. Acoust., Speech, Signal Process.*, 2021, pp. 6893–6897.
- <span id="page-11-8"></span>[49] V. Panayotov, G. Chen, D. Povey, and S. Khudanpur, "Librispeech: An asr corpus based on public domain audio books," in *IEEE Int. Conf. Acoust., Speech, Signal Process.*, 2015, pp. 5206–5210.
- <span id="page-11-9"></span>[50] F. Font, G. Roma, and X. Serra, "Freesound technical demo," in *Proc. 21st ACM Int. Conf. Multimedia*, 2013, pp. 411–412.
- <span id="page-11-10"></span>[51] A. Varga and H. J. Steeneken, "Assessment for automatic speech recognition: Ii. noisex-92: A database and an experiment to study the effect of additive noise on speech recognition systems," *ELSEVIER Speech Commun.*, vol. 12, no. 3, pp. 247–251, 1993.
- <span id="page-11-11"></span>[52] D. S. Park, W. Chan, Y. Zhang, C.-C. Chiu, B. Zoph, E. D. Cubuk, and Q. V. Le, "SpecAugment: A Simple Data Augmentation Method for Automatic Speech Recognition," in *ISCA Interspeech*, 2019, pp. 2613– 2617.
- <span id="page-11-12"></span>[53] D. Amodei, S. Ananthanarayanan, R. Anubhai, J. Bai, E. Battenberg, C. Case, J. Casper, B. Catanzaro, Q. Cheng, G. Chen *et al.*, "Deep speech 2: End-to-end speech recognition in english and mandarin," in *Int. Conf. Machine Learning (ICML)*, 2016, pp. 173–182.
- <span id="page-11-13"></span>[54] H. Li, Z. Xu, G. Taylor, C. Studer, and T. Goldstein, "Visualizing the loss landscape of neural nets," *Proc. of NIPS*, vol. 31, 2018.
- <span id="page-11-14"></span>[55] Y. Hao, L. Dong, F. Wei, and K. Xu, "Visualizing and understanding the effectiveness of bert," in *Proc. EMNLP-IJCNLP*, 2019, pp. 4143–4152.
- <span id="page-11-15"></span>[56] J. Du, Y.-H. Tu, L. Sun, F. Ma, H.-K. Wang, J. Pan, C. Liu, J.-D. Chen, and C.-H. Lee, "The ustc-iflytek system for chime-4 challenge," *Proc. CHiME*, vol. 4, pp. 36–38, 2016.
- <span id="page-11-16"></span>[57] T. Menne, "The rwth/upb/forth system combination for the 4th chime challenge evaluation."