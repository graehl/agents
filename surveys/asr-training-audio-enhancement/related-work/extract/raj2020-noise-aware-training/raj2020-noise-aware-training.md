**Source:** *Frustratingly Easy Noise-aware Training of Acoustic Models* — [PDF](https://arxiv.org/pdf/2011.02090v2) · [arXiv](https://arxiv.org/abs/2011.02090v2)

# FRUSTRATINGLY EASY NOISE-AWARE TRAINING OF ACOUSTIC MODELS

*Desh Raj*<sup>1</sup> *, Jesus Villalba ´* 1,2 *, Daniel Povey*<sup>3</sup> *, Sanjeev Khudanpur*<sup>1</sup>,<sup>2</sup>

<sup>1</sup>Center for Language and Speech Processing & <sup>2</sup>Human Language Technology Center of Excellence The Johns Hopkins University, Baltimore, MD 21218, USA. <sup>3</sup>Xiaomi Corp., Beijing, China.

draj@cs.jhu.edu

## ABSTRACT

Environmental noises and reverberation have a detrimental effect on the performance of automatic speech recognition (ASR) systems. Multi-condition training of neural networkbased acoustic models is used to deal with this problem, but it requires many-folds data augmentation, resulting in increased training time. In this paper, we propose utterance-level noise vectors for noise-aware training of acoustic models in hybrid ASR. Our noise vectors are obtained by combining the means of speech frames and silence frames in the utterance, where the speech/silence labels may be obtained from a GMM-HMM model trained for ASR alignments, such that no extra computation is required beyond averaging of feature vectors. We show through experiments on AMI and Aurora-4 that this simple adaptation technique can result in 6-7% relative WER improvement. We implement several embedding-based adaptation baselines proposed in literature, and show that our method outperforms them on both the datasets. Finally, we extend our method to the online ASR setting by using frame-level maximum likelihood for the mean estimation.

Index Terms: robust speech recognition, noise-aware training, acoustic modeling, noise vectors

# 1. INTRODUCTION

Automatic speech recognition (ASR) systems are being increasingly deployed in real-life situations (e.g. home assistants like Amazon Echo, Google Home, etc.), where the acoustic environment may present distortions such as background noise and reverberation. To tackle these problems, the field of noise-robust ASR has organized various challenges over the past several years, such as the REVERB [\[1\]](#page-4-0) or the CHiME [\[2,](#page-4-1) [3\]](#page-4-2) challenges.

In this paper, we propose a new approach for noise-aware training of deep neural network (DNN) based acoustic models in hybrid ASR systems. We leverage a speech activity detection (SAD) model to identify the speech frames and the silence frames in the utterance. Our "noise vector", then, is obtained by concatenating the means of the speech frames and the silence frames, respectively. We conjecture that such a noise estimate is well-informed by the distortions occurring throughout the utterance, including additive and multiplicative noises. The use of non-speech frames to estimate the noise in an utterance has also motivated previous work on noise-robust ASR [\[4\]](#page-4-3) and speech denoising [\[5\]](#page-4-4). Furthermore, in our estimation strategy, this additional information is acquired at no extra computational cost, since we make use of a GMM-HMM model that is already trained for generating alignments for training the DNN acoustic model.

In online speech recognition, we are only provided a partial input sequence, and the model is required to output streaming transcriptions. In such a setting, waiting until the whole utterance has been seen in order to compute the means of the speech and silence frames is not feasible, thus requiring online estimates of the noise vector. Towards this objective, we propose to use maximum likelihood (ML) estimates obtained from a probabilistic model of the means of speech and silence. This makes our noise-adaptive training scheme compatible with streaming ASR systems.

### 2. RELATED WORK

<span id="page-0-0"></span>In the past, several methods have been proposed to make ASR systems robust to environmental noise [\[6\]](#page-4-5), either through feature normalization (like spectral subtraction [\[7\]](#page-5-0) and Weiner filtering [\[8\]](#page-5-1)) or through model adaptation, such as MLLR-like schemes [\[9\]](#page-5-2). Recently, with the ubiquitous adoption of neural networks in hybrid as well as end-to-end ASR, data-driven supervised approaches have emerged as potential alternatives to traditional unsupervised methods [\[10\]](#page-5-3). These include frontend enhancement techniques like masking [\[11\]](#page-5-4) or back-end methods like noise-aware and multi-condition training [\[4\]](#page-4-3).

For robust streaming ASR, several online front-end processing methods have been proposed, such as time-frequency masks and steering vectors [\[12\]](#page-5-5) or online-enabled Generalized Eigenvalue (GEV) beamformers [\[13\]](#page-5-6). In this work, we do not perform any front-end processing of the acoustic signals; instead, we obtain an informed estimate of the noise

This work was partially supported by grants from the JHU Applied Physics Laboratory, MIT Lincoln Labs, and the Government of Israel.

from the observed chunks of speech and non-speech frames, and use this estimate to adapt the acoustic model.

Several researchers have proposed the use of utterancelevel embeddings for noise/environment adaptation of acoustic models. Saon et al. [14] used i-vectors, proposed originally for speaker verification [15]. An "online" version of these i-vectors, estimated every 10 frames, is supported in the Kaldi [16] ASR toolkit. Seltzer et al. [4] used noise-aware training similar to our approach, but their noise vectors were estimated by averaging the first and last 10 frames in the utterance, whereas we estimate noise by leveraging a SAD module. In [17], the authors trained a network to predict the environment label, and used the embedding from the bottlenecklayer to inform the acoustic model. Similarly, [18] trained a linear discriminant analysis (LDA) model using environment labels to project i-vectors into a space that more accurately represents noise variability in the utterance, calling them evectors. They also used a bottleneck DNN similar to [17] for estimating e-vectors, with the exception that they used ivectors as input, instead of the acoustic features. We will look at some of these approaches in more detail in Section 4.2.

Since we use the means of acoustic features, comparisons may also be drawn to the popular cepstral mean normalization (CMN) [19] approach. However, while CMN just subtracts the cepstral mean, our method allows the DNN to learn nonlinear transforms of the noise vector.

#### 3. NOISE VECTORS

We make the acoustic model noise-aware by appending additional information with the input feature sequence in the form of "noise vectors." Let  $\mathbf{x}_i = (\mathbf{x}_{i1}, \dots, \mathbf{x}_{it}, \dots, \mathbf{x}_{iT_i})$ ,  $\mathbf{x}_{it} \in \mathbb{R}^d$ , be the input feature frames corresponding to the utterance i. Consider an oracle SAD function,  $f: \mathbb{R}^d \to \{\text{speech}, \text{sil}\}, f(\mathbf{x}_{it}) = s_{it}$ , which classifies a frame as speech or silence. Let  $\mathbf{s}_i = (s_{i1}, \dots, s_{it}, \dots, s_{iT_i})$  be the corresponding SAD predictions for the input sequence. We compute the means of speech and silence frames,  $\boldsymbol{\mu}_{\mathbf{s}_i}$  and  $\boldsymbol{\mu}_{\mathbf{n}_i}$ , as

<span id="page-1-2"></span>
$$\mu_{\mathbf{s}_i} = \frac{\sum_{t \in \text{speech }} \mathbf{x}_{it}}{\sum_{t \in \text{speech }} 1}, \text{ and } \mu_{\mathbf{n}_i} = \frac{\sum_{t \in \text{sil}} \mathbf{x}_{it}}{\sum_{t \in \text{sil}} 1}.$$
(1)

In our hybrid ASR system, the acoustic model is trained using a sequence discriminative criterion [20] such as lattice-free MMI [21], on alignments generated using a GMM-HMM model with the training transcriptions. Since we know which phones map to silence phones, we use the same alignments to obtain the SAD label sequence  $s_i$ . An overview of our noise-aware training scheme is shown in Fig. 1. We append the noise vectors to the input features through a linear transformation (called a "control layer" in literature [22])<sup>1</sup>.

At inference time, we run a first-pass decoding with the same GMM-HMM model to obtain the decoding lattice,

<span id="page-1-0"></span>![](_page_1_Picture_9.svg)

**Fig. 1:** Noise-aware training/inference pipeline with a TDNN-based acoustic model. Dotted lines denote paths that are only required during training.

which is then used to obtain the SAD labels for estimating the noise vectors. Since we only need approximate representations of speech and noise frames, the classification need not be perfect, and so this strategy suffices. Next, we describe an extension of this estimation technique to the online decoding scenario using maximum likelihood estimate.

#### Maximum likelihood (ML) estimate

The ML estimate of the noise vectors is similar to equation (1), with  $s_i$  being the partial sequence observed until time t. If no speech or silence frames are observed, the corresponding components are set to 0. In Section 5.3, we will show that this estimate of the noise vectors quickly converges to the offline estimate in most settings.<sup>2</sup>

#### 4. EXPERIMENTAL SETUP

#### 4.1. Datasets and model

We performed experiments on two different datasets: AMI and Aurora-4. AMI [24] consists of 100 hours of recorded meetings, and speech from close-talk, single distant microphone (SDM), and array microphones is provided. We used the SDM recordings for our experiments, which is ideal for single-channel far-field evaluation. Aurora-4 [25] is a 14-hour close-talk speech corpus based on Wall Street Journal (WSJ0) data with artificially added noise. We evaluated on the eval92 and 0166 subsets. All our experiments were conducted using the Kaldi speech recognition toolkit [16] using neural networks trained with lattice-free MMI [21]. The acoustic model for Aurora-4 was based on factored TDNN [26], while the one for AMI was TDNN-based. The hyperparameters for each setup are shown in Table 1. For the Aurora-4 setup, we used a pruned 3-gram language

<span id="page-1-1"></span><sup>&</sup>lt;sup>1</sup>This is conceptually similar to an LDA feature transformation [23].

<span id="page-1-3"></span><sup>&</sup>lt;sup>2</sup>In addition to this maximum likelihood estimate of the noise vectors, we can also derive a *maximum a posteriori* (MAP) estimate which ties together the characteristics of both the speech and silence classes. The derivation is given in Appendix A. In our preliminary experiments, however, this model did not show any improvements over the simple ML estimate.

<span id="page-2-1"></span>Table 1: Hyperparameters for the acoustic model training for our experimental setups.

| Setup    | Model  | # layers | Dim  | Bottleneck | # epochs |
|----------|--------|----------|------|------------|----------|
| AMI      | TDNN   | 9        | 450  | -          | 9        |
| Aurora-4 | TDNN-F | 12       | 1024 | 128        | 10       |

model (LM) trained on WSJ transcriptions using the IRSTLM toolkit [\[27\]](#page-5-20). For AMI, we trained a pruned 3-gram LM with KN-smoothing on a combination of AMI and Fisher [\[28\]](#page-5-21) data using the SRILM toolkit [\[29\]](#page-5-22).

## <span id="page-2-0"></span>4.2. Baselines

As described earlier in Section [2,](#page-0-0) several embedding-based methods have been proposed for noise-aware training of acoustic models. Here, we perform comparisons with 4 of these methods, described below.

- 1. i-vector: i-vectors were first introduced in [\[15\]](#page-5-8) for speaker verification, and later used for speaker adaptation of acoustic models in [\[14\]](#page-5-7). They are generative embeddings which model both speaker and channel variability in utterances. We used two variants in our experiments: *offline*, which were estimated over the whole utterance, and *online*, which were estimated every 10 frames. For both these variants, we extracted 100 dim i-vectors using extractors trained on the training data.
- 2. NAT-vector: Seltzer et al. [\[4\]](#page-4-3) proposed "noise vectors" for noise-aware training, by averaging the first and last 10 frames of the utterance. We refer to these vectors as NAT-vectors, to avoid confusion with our proposed noise vectors. Since we use 40-dim MFCC features for training our models, these vectors are also 40-dimensional.
- 3. e-vector: Since i-vectors capture both speaker and channel variability, [\[18\]](#page-5-11) proposed a technique for extracting the "environment" variability by transforming the i-vectors using environment labels, either using linear discriminant analysis (LDA), or bottleneck neural networks (NNs), and called them e-vectors. Here, we use the LDA variant of e-vectors for our comparison. For Aurora-4, we trained the e-vectors on 14 noise label types from the official development set. Since AMI does not have annotated environment labels, we trained the LDA on CHiME-4 data [\[3\]](#page-4-2), which consists of 4 different noise types. For both the datasets, we transformed the 100 dim i-vectors to 50-dim e-vectors.
- 4. Bottleneck NN: Since the above baselines estimate environment embeddings at the utterance level, Kim et al. [\[17\]](#page-5-10) argued that they cannot effectively capture non-stationary noise. Instead, they trained bottleneck NNs to classify noise types with frame-level acoustic features provided as input. Framelevel noise embeddings were then extracted from the bottleneck layer and used for noise-aware training. For our experiments, we trained a 5-layer feed-forward neural network with

<span id="page-2-2"></span>Table 2: WER results for our proposed noise vectors (offline and MLE) compared with other embedding-based techniques from literature. Methods marked with † require environment labels for training embedding extractor.

| Method                  | AMI  |      | Aurora-4 |      |
|-------------------------|------|------|----------|------|
|                         | Dev  | Eval | Eval-92  | 0166 |
| Base model              | 38.8 | 42.6 | 7.94     | 8.12 |
| CMN                     | 38.5 | 42.8 | 7.79     | 7.94 |
| utt-mean                | 36.8 | 40.8 | 7.77     | 7.78 |
| i-vector (offline) [14] | 35.2 | 39.4 | 8.24     | 8.53 |
| i-vector (online)       | 35.6 | 40.0 | 8.51     | 8.78 |
| NAT-vector [4]          | 38.1 | 42.0 | 8.17     | 8.38 |
| e-vector (LDA)†<br>[18] | 37.6 | 41.5 | 7.63     | 7.73 |
| Bottleneck NN†<br>[17]  | 38.7 | 42.4 | 7.77     | 7.98 |
| Noise vector (offline)  | 34.9 | 38.8 | 7.37     | 7.61 |
| Noise vector (MLE)      | 35.4 | 39.2 | 7.72     | 7.93 |

<span id="page-2-3"></span>Table 3: Insertion (ins), deletion (del), and substitution (sub) error comparison for noise vectors compared with the base model, for AMI (dev) and Aurora-4 (eval92).

| Dataset   | System         | Ins  | Del  | Sub  | WER  |
|-----------|----------------|------|------|------|------|
| AMI (dev) | TDNN           | 4.7  | 12.6 | 21.5 | 38.8 |
|           | + noise vector | 3.2  | 11.5 | 20.3 | 34.9 |
| Aurora-4  | TDNN-F         | 0.50 | 2.57 | 4.87 | 7.94 |
| (eval92)  | + noise vector | 0.58 | 2.12 | 4.67 | 7.37 |

1024 hidden units (similar to [\[17\]](#page-5-10)), and a 80-dim bottleneck was placed at the 4th layer. Noise labels used as training targets for the bottleneck NNs were obtained similar to the evector LDA training.

In addition to these embedding methods from literature, we report results using (i) CMN, and (ii) embeddings obtained by averaging the entire utterance, which we call utt-mean. This ablation is performed to demonstrate the importance of obtaining separate means for speech and silence frames. Our implementation for these baselines and our proposed method will be made publicly available at: <https://github.com/desh2608/kaldi-noise-vectors>.

## 5. RESULTS AND DISCUSSION

### 5.1. Comparison with baselines

Table [2](#page-2-2) shows the WER results for the proposed method and the baselines on AMI and Aurora-4. It can be seen from the table that adding offline noise vectors to the input features provided WER improvements of 10% and 7.1% on AMI and Aurora-4, respectively. Furthermore, these vectors consistently outperformed the utt-mean baseline, indicating that the speech/silence classification is important for the model. MLE-based vectors are also effective, although they perform

<span id="page-3-0"></span>![](_page_3_Figure_0.svg)

Fig. 2: Frame-level phone alignments obtained from the Baseline TDNN and noise vector models for the sentences: I MEAN IT JUST SEEMS LIKE YEAH (top) and TILL THE MEETING OH RIGHT (bottom) in the AMI Dev set. The shaded region shows where the baseline model makes insertion and deletion errors, respectively. We have only shown part of the spectograms for each utterance.

<span id="page-3-1"></span>**Table 4:** Effect of speech and non-speech frames in the noise vector.

| Speech mean | Non-speech mean | AMI Dev | AMI Eval |
|-------------|-----------------|---------|----------|
| ×           | Х               | 38.8    | 42.6     |
| X           | ✓               | 38.1    | 41.9     |
| ✓           | ×               | 36.7    | 40.8     |
| ✓           | ✓               | 34.9    | 38.8     |

slightly worse than the utterance-level vectors, as expected. We conjecture that this may be because of incorrect estimates of speech and silence in the beginning of the utterance.

Among the baseline embedding-based systems, i-vectors (both offline and online) showed significant gains for AMI, but degraded results on Aurora-4. This may be because Aurora-4 utterances contain long silences, which can corrupt i-vector estimation. NAT vectors also followed the same trend, indicating that noise estimation from only the first and last few frames leads to inaccuracies. On the other hand, e-vectors and bottleneck NNs improved WERs over the base models on both datasets. Our proposed method provided the best performance across the board, demonstrating its robustness. In the next section, we will analyze the performance of our noise vectors further using some ablation experiments.

### 5.2. Where does the improvement come from?

WER breakdown by error type. Table 3 shows the insertion, deletion, and substitution error rates for the proposed method. On the AMI dataset, which contains late reverberations and interfering speakers, our noise vectors reduce insertion errors substantially, suggesting that utterance-level characteristics help in speaker selection. In Fig. 2 (top), we see that the baseline model inserted extraneous phonemes between LIKE and YEAH, as a result of cross-talk from the interfering speaker, but the noise-aware model correctly identified the frames as silence. Since Aurora-4 does not contain far-field or overlapping speech, noise vectors do not improve insertion errors on that setting. On both datasets, noise vectors consistently reduced deletion and insertion er-

<span id="page-3-2"></span>![](_page_3_Figure_8.svg)

**Fig. 3:** Effect of combining i-vectors and noise vectors on the AMI dataset. Noise vectors outperform i-vectors, but they are complementary.

rors. Qualitative analysis (such as that in Fig. 2 (bottom)) showed that this was a result of better recognition on noisy frames, where the base model did not predict any phones, or predicted incorrect phones.

Effect of speech and non-speech frames. In Table 2, comparison with the utt-mean baseline showed that averaging speech and non-speech frames separately was important for the effectiveness of our noise vectors. To measure the individual contributions of these components, we conducted experiments on the AMI dataset by selecting each of the components alternatively (Table 4). We found that speech frames are more important than non-speech frames, but their combination results in the best performance. The relatively smaller WER improvement using non-speech frames is also consistent with the NAT vector results in Table 2.

**Combination with i-vectors.** In Fig. 3, we show the effect of combining i-vectors and noise vectors on the AMI dataset. We found that the WER gains using these embedding methods are complementary, and their combination achieved a relative improvement of approx. 12.8% compared with the baseline TDNN model. This is likely because i-vectors and

![](_page_4_Figure_0.svg)

Fig. 4: Effect of combining noise vectors with multi-condition (MC) training on the Aurora-4 dataset. MC training outperforms noise vectors, but they are complementary.

noise vectors capture speaker and environment characteristics in the utterance, respectively.

Combination with multi-condition training. We also compared our method with multi-condition (MC) training on Aurora-4, where we applied speed and volume perturbation, and added simulated reverberation and point-source noises to the training data, resulting in 6x the original training set. MC training outperformed noise vectors; however, their combination achieved the best performance, reducing the WER by approx. 21.6% relative over the baseline TDNN-F model.

## <span id="page-4-6"></span>5.3. Offline vs. MLE noise vectors

Fig. [5](#page-4-7) shows 4 (out of 80) coefficients from the offline and MLE noise vectors for an utterance selected at random from the Aurora-4 test 0166 set. We see that the online estimates for speech coefficients (15 and 35) quickly approached the utterance-level values. For the noise coefficients (55 and 75), the utterance-level averages for the online estimates were higher because of fewer silence frames in the middle of the utterance, but the overall estimate over the whole utterance was close to the offline vector. Similar observations were made across both datasets.

### 6. CONCLUSIONS

We proposed a simple method that leverages a SAD to perform noise-aware training of acoustic models in hybrid ASR systems by computing the means of speech and silence frames. Our method, which we call "noise vectors," provided significant improvements in WER in diverse conditions such as noise and far-field reverberant speech, as demonstrated through experiments conducted on Aurora-4 and AMI. On both conditions, our method outperformed strong baselines that use i-vectors, e-vectors trained with LDA, or bottleneck neural networks. Through error analysis, we hypothesized that the improvements are a results of better performance of

<span id="page-4-7"></span>![](_page_4_Figure_8.svg)

Fig. 5: Online noise estimates using MLE and MAP for a randomly selected utterance in the Aurora-4 test 0166 set. The top and bottom row coefficients correspond to means of speech and silence frames, respectively. For each coefficient, the solid red and green lines are the "offline" and MLE estimates, respectively. The dashed green line represents the mean of the MLE noise vector over the whole utterance.

our model on frames containing high background noise or interference in the form of overlapping speech. Finally, we extended our method to the case of streaming ASR by showing that similar WER gains can be obtained using maximum likelihood estimates of the noise vectors.

## 7. REFERENCES

- <span id="page-4-0"></span>[1] K. Kinoshita, M. Delcroix, S. Gannot, E. A. Habets, R. Haeb-Umbach, W. Kellermann, V. Leutnant, R. Maas, T. Nakatani, B. Raj *et al.*, "A summary of the REVERB challenge: stateof-the-art and remaining challenges in reverberant speech processing research," *EURASIP Journal on Advances in Signal Processing*, vol. 2016, no. 1, p. 7, 2016.
- <span id="page-4-1"></span>[2] J. Barker, E. Vincent, N. Ma, H. Christensen, and P. Green, "The PASCAL CHiME speech separation and recognition challenge," *Computer Speech & Language*, vol. 27, no. 3, pp. 621–633, 2013.
- <span id="page-4-2"></span>[3] J. Barker, R. Marxer, E. Vincent, and S. Watanabe, "The third 'CHiME' speech separation and recognition challenge: Dataset, task and baselines," in *IEEE ASRU*. IEEE, 2015, pp. 504–511.
- <span id="page-4-3"></span>[4] M. L. Seltzer, D. Yu, and Y. Wang, "An investigation of deep neural networks for noise robust speech recognition," in *IEEE ICASSP*. IEEE, 2013, pp. 7398–7402.
- <span id="page-4-4"></span>[5] R.-L. Xu, R. Wu, Y. Ishiwaka, C. Vondrick, and C. Zheng, "Listening to sounds of silence for speech denoising," *ArXiv*, vol. abs/2010.12013, 2020.
- <span id="page-4-5"></span>[6] J. Li, L. Deng, Y. Gong, and R. Haeb-Umbach, "An overview of noise-robust automatic speech recognition," *IEEE/ACM Transactions on Audio, Speech, and Language Processing*, vol. 22, no. 4, pp. 745–777, 2014.

- <span id="page-5-0"></span>[7] S. Boll, "Suppression of acoustic noise in speech using spectral subtraction," *IEEE Transactions on acoustics, speech, and signal processing*, vol. 27, no. 2, pp. 113–120, 1979.
- <span id="page-5-1"></span>[8] P. C. Loizou, *Speech enhancement: theory and practice*. CRC press, 2013.
- <span id="page-5-2"></span>[9] C. J. Leggetter and P. C. Woodland, "Maximum likelihood linear regression for speaker adaptation of continuous density hidden markov models," *Computer speech & language*, vol. 9, no. 2, pp. 171–185, 1995.
- <span id="page-5-3"></span>[10] Z. Zhang, J. Geiger, J. Pohjalainen, A. E.-D. Mousa, W. Jin, and B. Schuller, "Deep learning for environmentally robust speech recognition: An overview of recent developments," *ACM Transactions on Intelligent Systems and Technology (TIST)*, vol. 9, no. 5, pp. 1–28, 2018.
- <span id="page-5-4"></span>[11] S. Srinivasan, N. Roman, and D. Wang, "Binary and ratio timefrequency masks for robust speech recognition," *Speech Communication*, vol. 48, no. 11, pp. 1486–1501, 2006.
- <span id="page-5-5"></span>[12] T. Higuchi, N. Ito, T. Yoshioka, and T. Nakatani, "Robust MVDR beamforming using time-frequency masks for online/offline asr in noise," in *IEEE ICASSP*. IEEE, 2016, pp. 5210–5214.
- <span id="page-5-6"></span>[13] M. Kitza, A. Zeyer, R. Schluter, J. Heymann, and R. Haeb- ¨ Umbach, "Robust online multi-channel speech recognition," in *Speech Communication; 12. ITG Symposium*. VDE, 2016.
- <span id="page-5-7"></span>[14] G. Saon, H. Soltau, D. Nahamoo, and M. Picheny, "Speaker adaptation of neural network acoustic models using i-vectors," in *IEEE ASRU*. IEEE, 2013, pp. 55–59.
- <span id="page-5-8"></span>[15] N. Dehak, P. Kenny, R. Dehak, P. Dumouchel, and P. Ouellet, "Front-end factor analysis for speaker verification," *IEEE Transactions on Audio, Speech, and Language Processing*, vol. 19, pp. 788–798, 2011.
- <span id="page-5-9"></span>[16] D. Povey, A. Ghoshal, G. Boulianne, L. Burget, O. Glembek, N. Goel, M. Hannemann, P. Motlicek, Y. Qian, P. Schwarz *et al.*, "The Kaldi speech recognition toolkit," in *IEEE ASRU*, no. CONF. IEEE Signal Processing Society, 2011.
- <span id="page-5-10"></span>[17] S. Kim, B. Raj, and I. Lane, "Environmental noise embeddings for robust speech recognition," *ArXiv*, vol. abs/1601.02553, 2016.
- <span id="page-5-11"></span>[18] X. Feng, B. Richardson, S. Amman, and J. R. Glass, "An environmental feature representation for robust speech recognition and for environment identification," in *INTERSPEECH*, 2017.
- <span id="page-5-12"></span>[19] F.-H. Liu, R. M. Stern, X. Huang, and A. Acero, "Efficient cepstral normalization for robust speech recognition," in *Human Language Technology: Proceedings of a Workshop Held at Plainsboro, New Jersey, March 21-24, 1993*, 1993. [Online]. Available: [https://www.aclweb.org/anthology/](https://www.aclweb.org/anthology/H93-1014) [H93-1014](https://www.aclweb.org/anthology/H93-1014)
- <span id="page-5-13"></span>[20] K. Vesely, A. Ghoshal, L. Burget, and D. Povey, "Sequence- ` discriminative training of deep neural networks." in *INTER-SPEECH*, vol. 2013, 2013, pp. 2345–2349.
- <span id="page-5-14"></span>[21] D. Povey, V. Peddinti, D. Galvez, P. Ghahremani, V. Manohar, X. Na, Y. Wang, and S. Khudanpur, "Purely sequence-trained neural networks for ASR based on lattice-free MMI." in *IN-TERSPEECH*, 2016, pp. 2751–2755.

- <span id="page-5-15"></span>[22] J. Rownicka, P. Bell, and S. Renals, "Embeddings for DNN speaker adaptive training," *IEEE ASRU*, pp. 479–486, 2019.
- <span id="page-5-16"></span>[23] P. Somervuo, B. Y. Chen, and Q. Zhu, "Feature transformations and combinations for improving ASR performance," in *INTERSPEECH*, 2003.
- <span id="page-5-17"></span>[24] J. Carletta, S. Ashby, S. Bourban, M. Flynn, M. Guillemot, T. Hain, J. Kadlec, V. Karaiskos, W. Kraaij, M. Kronenthal *et al.*, "The AMI meeting corpus: A pre-announcement," in *International workshop on machine learning for multimodal interaction*. Springer, 2005, pp. 28–39.
- <span id="page-5-18"></span>[25] S.-K. A. Yeung and M.-H. Siu, "Improved performance of Aurora 4 using HTK and unsupervised MLLR adaptation," in *Eighth International Conference on Spoken Language Processing*, 2004.
- <span id="page-5-19"></span>[26] D. Povey, G. Cheng, Y. Wang, K. Li, H. Xu, M. Yarmohammadi, and S. Khudanpur, "Semi-orthogonal low-rank matrix factorization for deep neural networks," in *INTERSPEECH*, 2018, pp. 3743–3747.
- <span id="page-5-20"></span>[27] M. Federico, N. Bertoldi, and M. Cettolo, "IRSTLM: an open source toolkit for handling large scale language models," in *INTERSPEECH*, 2008.
- <span id="page-5-21"></span>[28] C. Cieri, D. Miller, and K. Walker, "The Fisher corpus: a resource for the next generations of speech-to-text," in *LREC*, vol. 4, 2004, pp. 69–71.
- <span id="page-5-22"></span>[29] A. Stolcke, "SRILM-an extensible language modeling toolkit," in *Seventh International Conference on Spoken Language Processing*, 2002.

#### A. MAXIMUM A POSTERIORI ESTIMATION OF NOISE VECTORS

<span id="page-6-0"></span>If we consider a frame-level classification of a noisy utterance into speech and silence frames, the noise characteristics of the utterance may be encapsulated by the silence frames. However, the speech frames contain both speech and background noise, and consequently the mean of speech frames are also informed by the mean of noise frames. Considering this, we propose a model that ties together the statistics of both classes, denoted by s and n. Let  $\mu_{s_i}$  and  $\mu_{n_i}$  (which were defined by (1) for the offline case) be the means of speech and silence which we want to estimate. We write the likelihood of the features and means of utterance i as

$$P\left(\mathbf{x}_{i}, \boldsymbol{\mu}_{\mathbf{s}_{i}}, \boldsymbol{\mu}_{\mathbf{n}_{i}} | \mathbf{s}_{i}, r_{\mathbf{s}_{i}}, r_{\mathbf{n}_{i}}, \pi\right) = \prod_{t \in \text{sil}} P\left(\mathbf{x}_{it} | \neg s_{it}, \boldsymbol{\mu}_{\mathbf{n}_{i}}, r_{\mathbf{n}_{i}}, \pi\right)$$
$$\prod_{t \in \text{sp.}} P\left(\mathbf{x}_{it} | s_{it}, \boldsymbol{\mu}_{\mathbf{s}_{i}}, r_{\mathbf{s}_{i}}, \pi\right) P\left(\boldsymbol{\mu}_{\mathbf{s}_{i}} | \boldsymbol{\mu}_{\mathbf{n}_{i}}, \pi\right) P\left(\boldsymbol{\mu}_{\mathbf{n}_{i}} | \pi\right), \tag{2}$$

where

$$P\left(\mathbf{x}_{it}|s_{it}=0,\boldsymbol{\mu}_{\mathbf{n}_{i}},r_{\mathbf{n}_{i}},\pi\right) = \mathcal{N}\left(\mathbf{x}_{it}|\boldsymbol{\mu}_{\mathbf{n}_{i}},(r_{\mathbf{n}_{i}}\boldsymbol{\Lambda}_{\mathbf{n}})^{-1}\right)$$
(3)

$$P\left(\mathbf{x}_{it}|s_{it}=1,\boldsymbol{\mu}_{\mathbf{s}_i},r_{\mathbf{s}_i},\pi\right) = \mathcal{N}\left(\mathbf{x}_{it}|\boldsymbol{\mu}_{\mathbf{s}_i},(r_{\mathbf{s}_i}\boldsymbol{\Lambda}_{\mathbf{s}})^{-1}\right)$$
(4)

<span id="page-6-2"></span>
$$P\left(\boldsymbol{\mu}_{s_{c}}|\boldsymbol{\mu}_{n_{c}},\boldsymbol{\pi}\right) = \mathcal{N}\left(\boldsymbol{\mu}_{s_{c}}|\mathbf{a} + \mathbf{B}\boldsymbol{\mu}_{n_{c}},\boldsymbol{\Lambda}_{s}^{-1}\right) \tag{5}$$

$$P\left(\boldsymbol{\mu}_{\mathbf{n}_{i}}|\boldsymbol{\pi}\right) = \mathcal{N}\left(\boldsymbol{\mu}_{\mathbf{n}_{i}}|\boldsymbol{\mu}_{\mathbf{n}},\boldsymbol{\Lambda}_{\mathbf{n}}^{-1}\right) \tag{6}$$

where we defined the prior parameters  $\pi = (\mu_n, \mathbf{a}, \mathbf{B}, \Lambda_n, \Lambda_s)$ . The scaling factors  $r_{s_i}$  and  $r_{n_i}$  are deterministic parameters that can be set manually or estimated by maximum likelihood from the training data.

#### A.1. Estimating the prior

Assuming that we have access to a large number of frames corresponding to each class at training time, we just estimate  $\mu_{s_i}$  and  $\mu_{n_i}$  by maximum likelihood and assume that they are observed. Then, for each utterance we can form a vector  $\mu_i = [\mu_{s_i}, \mu_{n_i}]^T$ . We calculate the ML mean and covariance of  $\mu_i$  over the whole training set to get the prior joint probability distribution of speech and silence means  $P(\mu_i|\pi) = \mathcal{N}(\mu_i|\mu, \Sigma)$  with

<span id="page-6-3"></span>
$$\mu = \begin{bmatrix} \mu_{s} \\ \mu_{n} \end{bmatrix} \qquad \Sigma = \begin{bmatrix} \Sigma_{ss} & \Sigma_{sn} \\ \Sigma_{ns} & \Sigma_{nn} \end{bmatrix} . \tag{7}$$

Following, we calculate the precision,  $\Lambda = \Sigma^{-1}$ . Then, we can use the equations of the marginal and conditional Gaussians<sup>3</sup> to obtain the required priors as

<span id="page-6-4"></span>
$$P\left(\boldsymbol{\mu}_{\mathrm{n}_{i}}|\boldsymbol{\pi}\right) = \mathcal{N}\left(\boldsymbol{\mu}_{\mathrm{n}_{i}}|\boldsymbol{\mu}_{\mathrm{n}},\boldsymbol{\Sigma}_{\mathrm{nn}}\right) \tag{8}$$

<span id="page-6-5"></span>
$$P\left(\boldsymbol{\mu}_{\mathrm{s}_{i}}|\boldsymbol{\mu}_{\mathrm{n}_{i}},\pi\right) = \mathcal{N}\left(\boldsymbol{\mu}_{\mathrm{s}_{i}}|\boldsymbol{\mu}_{\mathrm{s}|\mathrm{n}},\boldsymbol{\Lambda}_{\mathrm{ss}}^{-1}\right) \tag{9}$$

$$\boldsymbol{\mu}_{\mathrm{s}|\mathrm{n}} = \boldsymbol{\mu}_{\mathrm{s}} - \boldsymbol{\Lambda}_{\mathrm{ss}}^{-1} \boldsymbol{\Lambda}_{\mathrm{sn}} (\boldsymbol{\mu}_{\mathrm{n}_{i}} - \boldsymbol{\mu}_{\mathrm{n}}) \tag{10}$$

Now, comparing (5) to (6) with (8) to (10), we define  $\Lambda_{\rm n}=\Sigma_{\rm nn}^{-1}, \Lambda_{\rm s}=\Lambda_{\rm ss}, a=\mu_{\rm s}+\Lambda_{\rm ss}^{-1}\Lambda_{\rm sn}\mu_{\rm n}$ , and  ${\bf B}=-\Lambda_{\rm ss}^{-1}\Lambda_{\rm sn}$ .

### A.2. Derivation of MAP point estimate

We want to estimate  $P(\mu_{s_i}, \mu_{n_i} | \mathbf{x}_i, \mathbf{s}_i, r_{s_i}, r_{n_i}, \pi)$ . We define the sufficient statistics as

$$\begin{aligned} N_{\mathrm{s}_i} &= \sum_{t \in \mathrm{speech}} 1 & N_{\mathrm{n}_i} &= \sum_{t \in \mathrm{sil}} 1 \\ \mathbf{F}_{\mathrm{s}_i} &= \sum_{t \in \mathrm{speech}} \mathbf{x}_{it} & \mathbf{F}_{\mathrm{n}_i} &= \sum_{t \in \mathrm{sil}} \mathbf{x}_{it} \end{aligned}$$

<span id="page-6-1"></span><sup>&</sup>lt;sup>3</sup>C.M.Bishop, Pattern Recognition and Machine Learning. Springer, 2006.

$$\mathbf{S}_{\mathrm{s}_i} = \sum_{t \in \mathrm{speech}} \mathbf{x}_{it} \mathbf{x}_{it}^{\mathrm{T}}$$
  $\mathbf{S}_{\mathrm{n}_i} = \sum_{t \in \mathrm{sil}} \mathbf{x}_{it} \mathbf{x}_{it}^{\mathrm{T}}$ 

Using Bayes rule,

$$\log P\left(\mu_{s_{i}}, \mu_{n_{i}} | \mathbf{x}_{i}, \mathbf{s}_{i}, r_{s_{i}}, r_{n_{i}}, \pi\right) = \sum_{t \in \text{sil}} \log P\left(\mathbf{x}_{it} | s_{it} = 0, \mu_{n_{i}}, r_{n_{i}}, \pi\right)$$

$$+ \sum_{t \in \text{speech}} \log P\left(\mathbf{x}_{it} | s_{it} = 1, \mu_{s_{i}}, r_{s_{i}}, \pi\right) + \log P\left(\mu_{s_{i}} | \mu_{n_{i}}, \pi\right) + P\left(\mu_{n_{i}} | \pi\right) + \text{const}$$

$$= -\frac{r_{n_{i}}}{2} \sum_{t \in \text{sil}} (\mathbf{x}_{it} - \mu_{n_{i}})^{T} \mathbf{\Lambda}_{n} (\mathbf{x}_{it} - \mu_{n_{i}}) - \frac{r_{s_{i}}}{2} \sum_{t \in \text{speech}} (\mathbf{x}_{it} - \mu_{s_{i}})^{T} \mathbf{\Lambda}_{s} (\mathbf{x}_{it} - \mu_{s_{i}})$$

$$- \frac{1}{2} (\mu_{s_{i}} - \mathbf{a} - \mathbf{B} \mu_{n_{i}})^{T} \mathbf{\Lambda}_{s} (\mu_{s_{i}} - \mathbf{a} - \mathbf{B} \mu_{n_{i}}) - \frac{1}{2} (\mu_{n_{i}} - \mu_{n})^{T} \mathbf{\Lambda}_{n} (\mu_{n_{i}} - \mu_{n}) + \text{const}$$

$$= -\frac{r_{n_{i}} N_{n_{i}}}{2} \mu_{n_{i}}^{T} \mathbf{\Lambda}_{n} \mu_{n_{i}} + \mu_{n_{i}}^{T} \mathbf{\Lambda}_{n} (r_{n_{i}} \mathbf{F}_{n_{i}}) - \frac{r_{s_{i}} N_{s_{i}}}{2} \mu_{s_{i}}^{T} \mathbf{\Lambda}_{s} \mu_{s_{i}} + \mu_{s_{i}}^{T} \mathbf{\Lambda}_{s} (r_{s_{i}} \mathbf{F}_{s_{i}})$$

$$- \frac{1}{2} \mu_{s_{i}}^{T} \mathbf{\Lambda}_{s} \mu_{s_{i}} - \frac{1}{2} \mu_{n_{i}}^{T} \mathbf{B}^{T} \mathbf{\Lambda}_{s} \mathbf{B} \mu_{n_{i}} + \mu_{s_{i}}^{T} \mathbf{\Lambda}_{s} \mathbf{a} + \mu_{s_{i}}^{T} \mathbf{\Lambda}_{s} \mathbf{B} \mu_{n_{i}} + \mu_{n_{i}}^{T} \mathbf{B}^{T} \mathbf{\Lambda}_{s} \mathbf{a}$$

$$- \frac{1}{2} \mu_{n_{i}}^{T} \mathbf{\Lambda}_{n} \mu_{n_{i}} + \mu_{n_{i}}^{T} \mathbf{\Lambda}_{n} \mu_{n_{i}} + \mu_{n_{i}}^{T} (\mathbf{\Lambda}_{n} (\mu_{n} + r_{n_{i}} \mathbf{F}_{n_{i}}) + \mathbf{B}^{T} \mathbf{\Lambda}_{s} \mathbf{a})$$

$$- \frac{1}{2} \mu_{n_{i}}^{T} \mathbf{\Lambda}_{s} \mu_{s_{i}} + \mu_{s_{i}}^{T} \mathbf{\Lambda}_{s} \mathbf{B} \mu_{n_{i}} + \mu_{n_{i}}^{T} (\mathbf{\Lambda}_{n} (\mu_{n} + r_{n_{i}} \mathbf{F}_{n_{i}}) + \mathbf{B}^{T} \mathbf{\Lambda}_{s} \mathbf{a})$$

$$- \frac{1}{2} \mu_{n_{i}}^{T} \mathbf{B}^{T} \mathbf{\Lambda}_{s} \mathbf{B} \mu_{n_{i}} + \mu_{s_{i}}^{T} \mathbf{\Lambda}_{s} \mathbf{B} \mu_{n_{i}} + \mu_{n_{i}}^{T} (\mathbf{\Lambda}_{n} (\mu_{n} + r_{n_{i}} \mathbf{F}_{n_{i}}) + \mathbf{B}^{T} \mathbf{\Lambda}_{s} \mathbf{a})$$

$$- \frac{1}{2} \mu_{n_{i}}^{T} ((1 + r_{n_{i}} N_{n_{i}}) \mathbf{\Lambda}_{n} + \mathbf{B}^{T} \mathbf{\Lambda}_{s} \mathbf{B}) \mu_{n_{i}} + \mu_{n_{i}}^{T} (\mathbf{\Lambda}_{n} (\mu_{n} + r_{n_{i}} \mathbf{F}_{n_{i}}) + \mathbf{B}^{T} \mathbf{\Lambda}_{s} \mathbf{a})$$

$$- \frac{1}{2} \mu_{n_{i}}^{T} (-\mathbf{\Lambda}_{s} \mathbf{B}) \mu_{n_{i}} - \frac{1}{2} \mu_{n_{i}}^{T} (-\mathbf{B}^{T} \mathbf{\Lambda}_{s}) \mu_{s_{i}} + \text{const}$$

$$- \frac{1}{2} \mu_{n_{i}}^{T} (\mathbf{\Lambda}_{s} \mu_{s_{i}} + \mu_{n_{i}}^{T} \mathbf{\Lambda}_{s} \mu_{s_{i}} + \mu_{n_{i}}^{T} \mathbf{\Lambda}_{s} \mu_{s_{i}} + \mu_{n_{i}}^{T}$$

where we defined

$$\boldsymbol{\mu}_{i} = \begin{bmatrix} \boldsymbol{\mu}_{\mathbf{s}_{i}} \\ \boldsymbol{\mu}_{\mathbf{n}_{i}} \end{bmatrix} \tag{17}$$

$$\mathbf{K}_{i} = \begin{bmatrix} (1 + r_{s_{i}} N_{s_{i}}) \mathbf{\Lambda}_{s} & -\mathbf{\Lambda}_{s} \mathbf{B} \\ -\mathbf{B}^{T} \mathbf{\Lambda}_{s} & (1 + r_{n_{i}} N_{n_{i}}) \mathbf{\Lambda}_{n} + \mathbf{B}^{T} \mathbf{\Lambda}_{s} \mathbf{B} \end{bmatrix}$$
(18)

$$\mathbf{Q}_{i} = \begin{bmatrix} \mathbf{\Lambda}_{s} (\mathbf{a} + r_{s_{i}} \mathbf{F}_{s_{i}}) \\ \mathbf{\Lambda}_{n} (\boldsymbol{\mu}_{n} + r_{n_{i}} \mathbf{F}_{n_{i}}) + \mathbf{B}^{T} \mathbf{\Lambda}_{s} \mathbf{a} \end{bmatrix} . \tag{19}$$

Equation (16) has the form of a Gaussian so

$$P\left(\boldsymbol{\mu}_{\mathbf{s}_{i}}, \boldsymbol{\mu}_{\mathbf{n}_{i}} | \mathbf{x}_{i}, \mathbf{s}_{i}, r_{\mathbf{s}_{i}}, r_{\mathbf{n}_{i}}, \pi\right) = \mathcal{N}\left(\boldsymbol{\mu}_{i} | \hat{\boldsymbol{\mu}}_{i}, \mathbf{K}_{i}^{-1}\right)$$
(20)

<span id="page-7-0"></span>
$$\hat{\boldsymbol{\mu}}_i = \mathbf{K}_i^{-1} \mathbf{Q}_i \tag{21}$$

 $\hat{\mu}_i$  is the MAP point estimate of means of speech and silence.

### A.3. Estimation of scaling factors

We need to maximize the EM objective,

$$Q(r_{\mathbf{s}_i}, r_{\mathbf{n}_i}) = \mathbf{E}_{P(\boldsymbol{\mu}_{\mathbf{s}_i}, \boldsymbol{\mu}_{\mathbf{n}_i} | \mathbf{x}_i, \mathbf{s}_i, r_{\mathbf{s}_i}, r_{\mathbf{n}_i}, \pi)} \left[ \log P\left(\mathbf{x}_i, \boldsymbol{\mu}_{\mathbf{s}_i}, \boldsymbol{\mu}_{\mathbf{n}_i} | \mathbf{s}_i, r_{\mathbf{s}_i}, r_{\mathbf{n}_i}, \pi\right) \right] . \tag{22}$$

For rs<sup>i</sup> ,

$$\frac{\partial Q(r_{s_i}, r_{n_i})}{\partial r_{s_i}} = \sum_{t \in \text{speech}} \frac{\partial}{\partial r_{s_i}} E\left[\log \mathcal{N}\left(\mathbf{x}_{it} | \boldsymbol{\mu}_{s_i}, (r_{s_i} \boldsymbol{\Lambda}_s)^{-1}\right)\right]$$
(23)

$$= \sum_{t \in \text{speech}} \frac{\partial}{\partial r_{s_i}} \left[ \frac{1}{2} \log |r_{s_i} \mathbf{\Lambda}_{s}| - \frac{r_{s_i}}{2} \text{tr} \left( E \left[ \mathbf{\Lambda}_{s} \left( \mathbf{x}_{it} - \boldsymbol{\mu}_{s_i} \right) \left( \mathbf{x}_{it} - \boldsymbol{\mu}_{s_i} \right)^{T} \right] \right) \right]$$
(24)

$$= \frac{\partial}{\partial r_{\mathbf{s}_{i}}} \left[ \frac{dN_{\mathbf{s}_{i}}}{2} \log r_{\mathbf{s}_{i}} - \frac{r_{\mathbf{s}_{i}}}{2} \operatorname{tr} \left( \mathbf{\Lambda}_{\mathbf{s}} \mathbf{E} \left[ \sum_{t \in \operatorname{speech}} \left( \mathbf{x}_{it} - \boldsymbol{\mu}_{\mathbf{s}_{i}} \right) \left( \mathbf{x}_{it} - \boldsymbol{\mu}_{\mathbf{s}_{i}} \right)^{\mathrm{T}} \right] \right) \right] = 0.$$
 (25)

Then,

$$r_{\mathbf{s}_{i}}^{-1} = \frac{1}{dN_{\mathbf{s}_{i}}} \operatorname{tr} \left( \mathbf{\Lambda}_{\mathbf{s}} \mathbf{E} \left[ \sum_{t \in \operatorname{speech}} \left( \mathbf{x}_{it} - \boldsymbol{\mu}_{\mathbf{s}_{i}} \right) \left( \mathbf{x}_{it} - \boldsymbol{\mu}_{\mathbf{s}_{i}} \right)^{\mathrm{T}} \right] \right)$$
(26)

Equivalently, for rn<sup>i</sup> ,

$$r_{\mathbf{n}_{i}}^{-1} = \frac{1}{dN_{\mathbf{n}_{i}}} \operatorname{tr} \left( \mathbf{\Lambda}_{\mathbf{n}} \mathbf{E} \left[ \sum_{t \in \operatorname{sil}} \left( \mathbf{x}_{it} - \boldsymbol{\mu}_{\mathbf{n}_{i}} \right) \left( \mathbf{x}_{it} - \boldsymbol{\mu}_{\mathbf{n}_{i}} \right)^{\mathrm{T}} \right] \right)$$
(27)

where

$$E\left[\sum_{t \in \text{speech}} \left(\mathbf{x}_{it} - \boldsymbol{\mu}_{s_i}\right) \left(\mathbf{x}_{it} - \boldsymbol{\mu}_{s_i}\right)^{T}\right] = \mathbf{S}_{s_i} - \mathbf{F}_{s_i} E\left[\boldsymbol{\mu}_{s_i}\right]^{T} - E\left[\boldsymbol{\mu}_{s_i}\right] \mathbf{F}_{s_i}^{T} + N_{s_i} E\left[\boldsymbol{\mu}_{s_i} \boldsymbol{\mu}_{s_i}^{T}\right]$$
(28)

$$E\left[\sum_{t\in\text{sil}} \left(\mathbf{x}_{it} - \boldsymbol{\mu}_{n_i}\right) \left(\mathbf{x}_{it} - \boldsymbol{\mu}_{n_i}\right)^{\mathrm{T}}\right] = \mathbf{S}_{n_i} - \mathbf{F}_{n_i} E\left[\boldsymbol{\mu}_{n_i}\right]^{\mathrm{T}} - E\left[\boldsymbol{\mu}_{n_i}\right] \mathbf{F}_{n_i}^{\mathrm{T}} + N_{n_i} E\left[\boldsymbol{\mu}_{n_i} \boldsymbol{\mu}_{n_i}^{\mathrm{T}}\right]$$
(29)

The above equations have the inconvenience that we cannot compute rs<sup>i</sup> (or rn<sup>i</sup> ) if no speech (or silence) frames have been observed, since no priors were put on r. We propose two possible initializations for r: (i) we can choose r = 1 until some frames are observed, or (ii) a global r pre-computed over the whole training set can be computed as

$$r_{s}^{-1} = \frac{1}{d\sum_{i} N_{s_{i}}} \operatorname{tr} \left( \mathbf{\Lambda}_{s} \sum_{i} E \left[ \sum_{t \in \operatorname{speech}} \left( \mathbf{x}_{it} - \boldsymbol{\mu}_{s_{i}} \right) \left( \mathbf{x}_{it} - \boldsymbol{\mu}_{s_{i}} \right)^{\mathrm{T}} \right] \right)$$
(30)

$$r_{\mathrm{n}}^{-1} = \frac{1}{d \sum_{i} N_{\mathrm{n}_{i}}} \operatorname{tr} \left( \mathbf{\Lambda}_{\mathrm{n}} \sum_{i} \operatorname{E} \left[ \sum_{t \in \operatorname{sil}} \left( \mathbf{x}_{it} - \boldsymbol{\mu}_{\mathrm{n}_{i}} \right) \left( \mathbf{x}_{it} - \boldsymbol{\mu}_{\mathrm{n}_{i}} \right)^{\mathrm{T}} \right] \right) . \tag{31}$$