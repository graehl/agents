**Source:** *When De-noising Hurts: A Systematic Study of Speech Enhancement Effects on Modern Medical ASR Systems* — [PDF](https://arxiv.org/pdf/2512.17562v1) · [arXiv](https://arxiv.org/abs/2512.17562v1)

# When De-noising Hurts: A Systematic Study of Speech Enhancement Effects on Modern Medical ASR Systems

#### Technical Report

**Sujal Chondhekar Vasanth Murukuri Rushabh Vasani Sanika Goyal**

**Rajshree Badami Anushree Rana Sanjana SN Karthik Pandia Sulabh Katiyar**

**Neha Jagadeesh Sankalp Gulati**

**EkaCare (Orbi Health Private Limited), Bengaluru, India (sankalp@eka.care)**

# **Abstract**

Speech enhancement methods are commonly believed to improve the performance of automatic speech recognition (ASR) in noisy environments. However, the effectiveness of these techniques cannot be taken for granted in the case of modern large-scale ASR models trained on diverse, noisy data. We present a systematic evaluation of MetricGAN-plus-voicebank denoising on four state-of-the-art ASR systems—OpenAI Whisper, NVIDIA Parakeet, Google Gemini Flash 2.0, Parrotlet-a using 500 medical speech recordings under nine noise conditions. ASR performance is measured using semantic WER (semWER), a normalized word error rate (WER) metric accounting for domain-specific normalizations. Our results reveal a counterintuitive finding: speech enhancement preprocessing degrades ASR performance across all noise conditions and models. Original noisy audio achieves lower semWER than enhanced audio in all 40 tested configurations (4 models *×* 10 conditions), with degradations ranging from 1.1% to 46.6% absolute semWER increase. These findings suggest that modern ASR models possess sufficient internal noise robustness and that traditional speech enhancement may remove acoustic features critical for ASR. For practitioners deploying medical scribe systems in noisy clinical environments, our results indicate that preprocessing audio with noise reduction techniques might not just be computationally wasteful but also be potentially harmful to the transcription accuracy.

*Keywords* Medical ASR *·* Speech Enhancement *·* Denoising *·* Noise Robustness *·* Clinical Documentation

# **1 Introduction**

The deployment of automatic speech recognition (ASR) for clinical documentation in India presents significant challenges due to high ambient noise levels. Hospitals often experience high noise levels from medical equipment, conversations, and infrastructure [\[Joseph et al.,](#page-14-0) [2020\]](#page-14-0), far exceeding the WHO-recommended 40 dB limit for healthcare facilities [1](#page-0-0) . Conventional wisdom suggests that speech enhancement preprocessing should improve ASR accuracy by removing noise and improving signal quality [\[Zhu and O'Shaughnessy,](#page-14-1) [2003\]](#page-14-1).

However, this assumption originates from an era when ASR systems used Gaussian Mixture Models (GMMs) and Hidden Markov Models (HMMs) trained on clean speech [[Hinton et al.](#page-14-2), [2012\]](#page-14-2). Modern end-to-end neural

<span id="page-0-0"></span><sup>1</sup>https://cpcb.nic.in/who-guidelines-for-noise-quality/

ASR models like Whisper [\[Radford et al.,](#page-14-3) [2022](#page-14-3)], trained on hundreds of thousands of hours of diverse, realworld audio including noisy recordings, may possess fundamentally different noise robustness characteristics. If these models have learned robust internal representations that handle noise, external preprocessing could potentially remove useful acoustic information.

This study is motivated by practical observations from real-world deployments of EkaScribe[2](#page-1-0) , with the majority being done on non-mobile devices having typically a single microphone. The audio is captured through an operating system (OS) managed audio pipeline, which often applies signal processing such as noise suppression or echo cancellation by default. These speech enhancement mechanisms are designed to improve human listening quality, but whether they always improve ASR performance is not guaranteed. This raises an important practical concern: if modern ASR models are already robust to noise, such preprocessing may be unnecessary or even counterproductive. Understanding how explicit denoising interacts with modern ASR therefore becomes critical for deployment scenarios.

We address this gap through a systematic evaluation of MetricGAN-plus-voicebank denoising [[Fu et al.,](#page-13-0) [2021](#page-13-0)] a state-of-the-art speech enhancement model on four leading ASR systems: OpenAI Whisper, NVIDIA Parakeet, Google Gemini Flash 2.0, and Parrotlet-a, a model specifically trained for English speech recognition in Indian healthcare. We tested 500 medical recordings under nine noise conditions representing typical Indian clinical environments. We release our evaluation code, dataset and detailed results to enable reproduction and extension of this work. These resources are publicly available on GitHub[3](#page-1-1) .

# **2 Related Work**

#### **2.1 Modern ASR Systems**

Recent ASR advances stem from self or weakly-supervised learning on massive datasets. Whisper [[Radford](#page-14-3) [et al.,](#page-14-3) [2022\]](#page-14-3) was trained on 680,000 hours of multilingual web audio, explicitly including diverse recording conditions and background noise. This exposure to real-world acoustic variability may confer inherent noise robustness. Similarly, NVIDIA's Parakeet models [[Rekesh et al.](#page-14-4), [2023,](#page-14-4) [Xu et al.](#page-14-5), [2023\]](#page-14-5) leverage largescale training with data augmentation including noise injection. Google's Gemini 2.0 [[Gemini Team,](#page-13-1) [2024](#page-13-1)] processes audio through multimodal encoders pre-trained on millions of examples.

A critical distinction exists between these models and classical ASR systems: modern models learn end-toend mappings from raw audio to text without explicit acoustic modelling assumptions. This may enable them to extract robust features from noisy signals without external preprocessing.

#### **2.2 Speech Enhancement Techniques**

Traditional speech enhancement techniques such as spectral subtraction and Wiener filtering were developed to improve human speech intelligibility and classical ASR mainly trained on clean data [[Loizou,](#page-14-6) [2007,](#page-14-6) [Benesty](#page-13-2) [et al.,](#page-13-2) [2006\]](#page-13-2). These methods typically operate in the frequency domain, estimating and removing noise to recover clean speech signals.

Deep learning approaches including Deep Neural Networks (DNNs) and Generative Adversarial Networks (GANs) have largely superseded classical methods. MetricGAN [[Fu et al.,](#page-13-3) [2019](#page-13-3)] aims to directly optimize perceptual quality metrics (PESQ, STOI) rather than reconstruction error. The improved MetricGAN+ variant [\[Fu et al.,](#page-13-0) [2021\]](#page-13-0) achieves state-of-the-art performance on standard benchmarks.

However, a critical gap exists: most speech enhancement evaluations focus on *speech quality* metrics or performance of *classical* ASR systems. Systematic evaluation of modern large-scale neural ASR remains a topic of research.

#### **2.3 Speech Enhancement Impact on ASR**

The relationship between speech enhancement and ASR accuracy has been repeatedly re-examined as ASR architectures evolved, yet consensus remains elusive.

**Classical ASR Era:** Traditional GMM-HMM systems trained on clean speech benefited substantially from preprocessing. [Flynn and Jones](#page-13-4) [\[2008](#page-13-4)] demonstrated that combined speech enhancement and auditory mod-

<span id="page-1-0"></span><sup>2</sup>https://ekascribe.ai/

<span id="page-1-1"></span><sup>3</sup>https://github.com/eka-care/when-denoising-hurts

eling improved distributed speech recognition in noisy conditions. These findings established the paradigm that enhancement should precede recognition, an assumption that persists in many deployment pipelines today.

**Deep Learning Transition:** The advent of deep neural networks for acoustic modelling prompted fundamental questions about preprocessing necessity. [Delcroix et al.](#page-13-5) [\[2013\]](#page-13-5) posed a prescient question in 2013: "Is speech enhancement pre-processing still relevant when using deep neural networks for acoustic modelling?" Their investigation of DNN-based acoustic models suggested that enhancement benefits were diminishing as models became more sophisticated. [Donahue et al.](#page-13-6) [\[2018](#page-13-6)] explored GAN-based enhancement for robust speech recognition, finding mixed results that varied by noise type and training conditions.

**Modern ASR Era:** Recent work reveals increasingly complex patterns. [Prasad et al.](#page-14-7) [[2021\]](#page-14-7) investigated end-to-end models for robust speech recognition, finding that modern architectures exhibit surprising noise robustness even without enhancement. [Braun and Gamper](#page-13-7) [[2022\]](#page-13-7) analyzed noise suppression losses and discovered a critical trade-off: aggressive noise reduction can introduce speech distortion that harms ASR performance more than the original noise. This suggests that enhancement optimized for perceptual quality may not align with ASR requirements.

Recent comparative studies have revealed important nuances in ASR performance and the enhancement effect. [Agarwal and Misra](#page-13-8) [\[2025](#page-13-8)] demonstrated that Whisper exhibits significant sensitivity to background noise and domain shifts, while Gemini's multimodal architecture shows enhanced robustness through contextual adaptation. [Trabelsi et al.](#page-14-8) [[2024\]](#page-14-8) directly evaluated whether noise reduction improves open-source ASR engines, finding that enhancement effectiveness varies significantly across models and conditions. [Rai](#page-14-9) [et al.](#page-14-9) [[2024\]](#page-14-9) introduced DENOASR, revealing that denoising can inadvertently introduce or amplify demographic biases in ASR systems through selective acoustic filtering. Most recently, [Nasretdinov et al.](#page-14-10) [\[2025](#page-14-10)] proposed Schrödinger Bridge-based enhancement specifically designed for ASR, suggesting that traditional enhancement methods may be fundamentally misaligned with neural recognition objectives.

**The Current Gap:** While recent studies have begun to examine noise robustness in modern ASR systems, the effectiveness of commonly used speech enhancement pipelines in this context remains insufficiently characterized. Prior work has often focused on limited model scales, specific noise types, or perceptual quality metrics, and has produced mixed or model-dependent findings. In particular, there is a lack of systematic evaluation of how widely adopted enhancement methods interact with large-scale ASR models—such as Whisper—that are trained on extensive, noisy data, especially in domain-specific settings like medical speech. Given the practical importance of deployment in noisy and resource-constrained clinical environments, a careful empirical study under controlled noise conditions is needed.

In this work, we address this gap by evaluating a widely used enhancement method (MetricGAN+) on four modern ASR systems using medical speech and noise conditions representative of real-world clinical environments.

# **3 Methodology**

## **3.1 Research Question**

We investigate: *Does MetricGAN-plus-voicebank speech enhancement improve ASR accuracy for modern models on noisy medical recordings?*

Our null hypothesis is that applying speech enhancement techniques like MetricGAN-plus-voicebank does not produce a statistically significant change in ASR accuracy compared to transcribing the original noisy audio.

#### **3.2 Dataset and Noise Conditions**

We compiled 500 annotated medical audio recordings from mocked clinical consultation settings, professionally transcribed to establish ground truth. These were mock consultations by the employees of EkaCare. The chosen samples were primarily in English to avoid adding another variable that could potential degrade the ASR performance. To simulate realistic hospital acoustics, we synthetically added three noise types to the original audio files at varying intensities using [Audiomentations](https://github.com/iver56/audiomentations) library:

**Background Noise:** Continuous ambient sound (HVAC, equipment hum, distant conversations, these noises were taken from [hospital-ambient-noise-dataset\)](https://www.kaggle.com/datasets/nafin59/hospital-ambient-noise) at Signal-to-Noise Ratios (SNR) of 10, 30, and 50 dB.

**Short Noise:** Transient bursts (equipment beeps, door slams, nearby conversations, these were taken from [pixabay](https://pixabay.com/sound-effects/search/short/)) at SNR 10, 30, and 50 dB.

**Gaussian Noise:** Additive white Gaussian noise at amplitudes 0.001, 0.009, and 0.017.

SNR is defined as:

$$SNR_{dB} = 10 \log_{10} \left( \frac{P_{\text{signal}}}{P_{\text{noise}}} \right) \tag{1}$$

where *P*signal and *P*noise represent speech and noise power over non-silent regions.

SNR 10dB corresponds to severe noise typical of busy clinical areas, 30 dB to moderate noise, and 50 dB to mild background noise. This yielded 4,500 noisy test utterances (500 recordings *×* 9 conditions). This dataset comprising original recordings, noise-augmentations and their de-noised versions, is publicly available on HuggingFace[4](#page-3-0) .

#### **3.3 ASR Systems**

**OpenAI Whisper Large-v3** [[Radford et al.,](#page-14-3) [2022](#page-14-3)]: Encoder-decoder Transformer trained on 680,000 hours of multilingual data. Processes 80-channel log-Mel spectrograms. We used the Large-v3 variant (1.55B parameters) that is publicly available on HuggingFace[5](#page-3-1) , hosted locally.

**NVIDIA Parakeet-TDT-1.1B** [[Rekesh et al.](#page-14-4), [2023,](#page-14-4) [Xu et al.,](#page-14-5) [2023](#page-14-5)]: Fast Conformer encoder with Tokenand-Duration Transducer decoder trained on 64,000+ hours. Uses 8x depthwise-separable convolution downsampling. We use the model version publicly available on HuggingFace[6](#page-3-2) , hosted locally via NeMo.

**Google Gemini Flash 2.0** [[Gemini Team,](#page-13-1) [2024\]](#page-13-1): Multimodal model with native audio understanding, accessed via Gemini API.

**Parrotlet-a**: This is a purpose-built automatic speech recognition (ASR) model specifically trained for English speech in Indian healthcare settings, optimized for transcribing medical speech. This model combines the Whisper V3 large encoder and MedGemma-3-4B decoder through a lean projector layer for efficient speech-to-text conversion. Model description and release details are available here[7](#page-3-3) .

#### **3.4 Denoising Method**

For denoising we used SpeechBrain's [[Ravanelli et al.,](#page-14-11) [2021\]](#page-14-11) MetricGAN-plus-voicebank model [\[Fu et al.,](#page-13-0) [2021\]](#page-13-0). This GAN-based approach optimizes perceptual quality (PESQ, STOI) rather than reconstruction error:

- 1. Compute Short-Time Fourier Transform: *X*[*n, k*] = STFT*{x*[*n*]*}*
- 2. Generate spectral mask via trained generator: *M*[*n, k*] = *Gθ*(*|X*[*n, k*]*|*)
- 3. Apply mask to noisy magnitude: *S*ˆ[*n, k*] = *M*[*n, k*] *· |X*[*n, k*]*|*
- 4. Reconstruct via inverse STFT with original phase: *s*ˆ[*n*] = ISTFT*{S*ˆ[*n, k*] *· e <sup>j</sup>*∠*X*[*n,k*]*}*

All audio was resampled to 16 kHz mono before processing.

#### **3.5 Evaluation Methodology**

We employ a comprehensive evaluation process to assess ASR performance under noisy and enhanced conditions, structured as follows:

## 1. **Baseline Establishment**

<span id="page-3-0"></span><sup>4</sup>https://huggingface.co/datasets/ekacare/denoising-impact-evaluation-dataset

<span id="page-3-1"></span><sup>5</sup>https://huggingface.co/openai/whisper-large-v3

<span id="page-3-3"></span><span id="page-3-2"></span><sup>6</sup>https://huggingface.co/nvidia/parakeet-tdt-1.1b

<sup>7</sup>https://info.eka.care/services/parrotlet-a-en-5b-releasing-our-purpose-built-llm-for-english-asr-in-indianhealthcare

- Transcribed 500 original audio files (without added noise)
- Applied MetricGAN+ enhancement to 500 original files and transcribed them

#### 2. **Noise Corruption and Dual Transcription**

- Corrupted each of the 500 original files with 9 noise conditions (3 types *×* 3 configurations)
- Generated 4,500 noisy audio files
- Each noisy file was transcribed under two conditions:
  - **– Noisy Condition**: Direct transcription without enhancement
  - **– Enhanced Condition**: Transcription after MetricGAN+ enhancement

### 3. **Transcription Volume per ASR System**

- Baseline transcriptions: 500 + 500 = 1*,* 000
- Noisy condition transcriptions: 4*,* 500
- Enhanced condition transcriptions: 4*,* 500
- **Total transcriptions per ASR system**: 1*,* 000 + 4*,* 500 + 4*,* 500 = 10*,* 000

## **Total across all 4 ASR systems**: 4 *×* 10*,* 000 = 40*,* 000 transcriptions

This extensive dataset enables a thorough analysis of noise and enhancement impacts on each ASR system. Word Error Rate (WER) was computed as:

$$WER = \frac{S + D + I}{N} \times 100\%$$
 (2)

where *S* is substitutions, *D* is deletions, *I* is insertions, and *N* is total reference words. Text normalization (lowercase, punctuation removal) was applied uniformly.

**Semantic WER (semWER)** [[Vasanth,](#page-14-12) [2025\]](#page-14-12): Indian medical consultations frequently exhibit codemixing—alternating between English medical terminology and regional languages (Hindi, Tamil, Telugu, etc.) mid-conversation. Standard WER penalizes semantically equivalent expressions. We computed semWER by applying additional normalizations:

#### 1. **Unit Normalisations**

- Expand abbreviated units to their word forms or full representations
- Example: 5mg *→* five mg, फाइव मिलीग्राम, five milligrams
- Example: 2°C *→* 2 degree C, 2 डिग्री सेल्सियस

## 2. **Symbol Normalisations**

- Convert mathematical and special symbols to their word equivalents
- Example: 3/4 *→* 3 by 4, 3 per 4, three per four

#### 3. **Contraction Expansion**

- Expand contracted forms to their full word forms
- Example: I'm *→* I am, It's *→* it is

#### 4. **Number to Word Conversion** [[AI4Bhārat](#page-13-9), [2025](#page-13-9)]

- Convert numeric digits to their word representations in various languages and scripts
- Example: 150 *→* one hundred and fifty, एक सौ पचास, १५०

#### 5. **Punctuation Removal** [\[Kunchukuttan](#page-14-13), [2020](#page-14-13)]

• Remove all punctuation marks from text including commas, periods, etc.

## 6. **Unicode Normalization**

- Convert all text to canonical Unicode form (NFC/NFKC) and merge equivalent codepoints
- Example: Merge composed vs. decomposed forms of matras in Indic scripts

#### 7. **Character Canonicalization** [[Kunchukuttan](#page-14-13), [2020](#page-14-13)]

- Standardize multiple codepoints that visually represent the same character to a single canonical form
- Example: Fix canonical order of combining marks (ं + ा)

## 8. **Nukta Variant Removal** [\[Kunchukuttan,](#page-14-13) [2020\]](#page-14-13)

- Replace nukta (dot below) forms with their base character equivalents
- Example:

#### 9. Diacritic Normalization [Kunchukuttan, 2020]

- Standardize combining diacritical marks to ensure consistent order and convert variant forms to canonical representations
- Example: Normalize anusvara (कं), chandrabindu (कं), visarga (ক:)

## 10. Transliteration [Google, 2025]

- Convert text from one script to another while preserving phonetic pronunciation
- Example: computer → कंप्यूटर

While semWER is designed to handle multilingual and code-mixed scenarios common in Indian medical consultations, since the dataset considered is English, only a subset of the normalisations mentioned above (unit expansion, number-to-word conversion, contractions, and symbol normalization in English) would have been relevant.

This produces a more clinically meaningful error metric for Indian healthcare ASR. All reported results use semWER unless otherwise noted.

#### 4 Results

## 4.1 ASR Accuracy and Impact of Noise

Figure 1 presents the ASR performance of four state-of-the-art models on original recordings and their noisy variants. The figure shows the baseline semWER (%) for each model, revealing that Parrotlet-a consistently achieves the lowest error rates across all conditions. To easily analyze the impact of noise on performance, in Figure 2 we show the performance difference ( $\Delta$ semWER) of these models under various noise conditions compared with the original conditions. A notable initial observation is that high SNR noise addition (i.e., low noise levels) even leads to marginal improvements in ASR performance for some models. However, as noise levels increase, ASR performance degrades significantly, with the extent of degradation varying across models. Whisper exhibits the greatest performance decline, particularly under Gaussian noise conditions (reaching approximately 9.72%  $\Delta$ semWER at AMP 0.017), followed by Parakeet with moderate degradation. In contrast, Gemini and Parrotlet-a demonstrates the most robust behaviour across all noise conditions, maintaining relatively stable performance even in highly noisy environments. This suggests that the architectures of Gemini and Parrotlet-a are better equipped to handle acoustic variability and noise-corrupted inputs compared to the other evaluated models.

![](_page_5_Figure_14.svg)

<span id="page-5-0"></span>Figure 1: semWER (%) (lower is better) performance of all evaluated ASR models under various noisy conditions. Parrotlet-a achieves the lowest error rates across all conditions.

![](_page_6_Figure_1.svg)

<span id="page-6-0"></span>Figure 2: Performance of four ASR models in various conditions. We observe degradation in the performance of these models beyond certain SNR levels.

#### 4.2 Main Finding: Denoising Degrades Performance

The ASR performance on de-noised recordings using the SpeechBrain denoiser is visualized in Figure 3, which presents the semWER (%) for all models after enhancement processing. Notably, Gemini and Whisper experience catastrophic degradation post denoising of certain noise conditions, with semWER soaring to extreme values (e.g., Gemini exceeding 50% semWER), transforming them from competitively robust models to the worst performers. Parrotlet-a maintains its position as the most robust model overall, showing the smallest absolute error increases and the best final performance across all de-noised conditions

![](_page_7_Figure_3.svg)

<span id="page-7-0"></span>Figure 3: semWER (%) performance of all ASR models after enhancement with the SpeechBrain denoiser.

Figure 4 shows the change in ASR performance resulting from the denoising process. It presents the  $\Delta$ semWER (De-noised – Noisy) for all models, directly comparing the error rates for noisy audio against the same audio after enhancement. The positive  $\Delta$ semWER values indicate that de-noised audio yields higher semantic word error rates compared to processing the noisy audio directly. The magnitude of performance degradation varies substantially across noise types and models. For moderate noise conditions (Background Noise SNR 10-50 and Short Noise SNR 10-50), the degradation remains relatively modest. However, the effect becomes dramatically more severe under Gaussian noise conditions. At higher Gaussian noise amplitudes (AMP 0.009 and 0.017), Gemini exhibits catastrophic performance collapse, with  $\Delta$ semWER values reaching 35.91% and 46.57% respectively. Whisper also shows substantial degradation at these noise levels (13.48% and 34.93%), Parakeet demonstrates more moderate but still significant decline (7.83% and 11.9%). Parrotlet-a also shows a similar pattern of degradation (7.69% and 14.78%). Notably, even in original conditions, denoising introduces measurable performance penalties across all models (1.32% to 3.19%), suggesting that the denoising process itself introduces artifacts or information loss that adversely affects ASR accuracy. This finding challenges the conventional assumption that speech enhancement preprocessing universally benefits downstream ASR tasks, and indicates that modern ASR models may be better equipped to handle noisy inputs directly rather than relying on de-noised representations.

#### 4.3 Detailed Analysis by Noise Type

**Background Noise:** Figure 5 shows Whisper's performance. At SNR 10dB (severe noise), noisy semWER is 8.82% while enhanced semWER is 25.83%—a catastrophic 17.0 percentage point degradation. Even at SNR 50 dB (mild noise), enhancement increases semWER from 6.54% to 9.82%.

Parakeet shows similar patterns (Figure 6), though degradation is less severe. At SNR 10dB, semWER increases from 10.86% to 16.79%. Gemini (Figure 7) shows moderate degradation: 7.34% to 12.32% at SNR 10dB, while Parrotlet-a (Figure 8) exhibits relatively less degradation, increasing only from 4.22% to 9.24% at SNR 10dB.

**Short Noise:** Transient noise bursts show similar patterns. At SNR 10dB, Whisper's semWER increases from 8.0% to 17.68%. Parakeet: 10.05% to 13.29%. Gemini: 6.42% to 9.52%. Parrotlet-a: 3.49% to 6.88%. Enhancement provides no benefit at any SNR level for short noise.

![](_page_8_Figure_1.svg)

<span id="page-8-0"></span>Figure 4: Change in Semantic Word Error Rate ( $\Delta$ semWER) after denoising across ASR models and noise conditions. We observe performance degradation due to denoising. Results demonstrate significant variation in denoising effectiveness across models, with Whisper showing the most substantial sensitivity to enhancement.

![](_page_9_Figure_1.svg)

<span id="page-9-0"></span>Figure 5: Whisper semWER (%) and ∆semWER. Enhancement consistently increases semWER across all conditions, with extreme degradation under Gaussian noise.

**Gaussian Noise:** This condition produces the most dramatic degradation. At amplitude 0.017, Whisper's semWER increases from 16.19% to 51.11%, while Gemini shows an even more severe degradation from 11.2% to 57.77%. Parakeet also experiences a significant rise from 15.58% to 27.48%. Parrotlet-a also shows a similar degradation pattern from 7.69% to 22.46%. Even at low amplitude (0.001), enhancement still degrades performance for all models rather than helping.

## **4.4 Quantitative Summary**

Table [1](#page-10-1) presents the ∆semWER statistics computed across all 40 test configurations. These configurations comprise 4 different ASR Models evaluated under 10 distinct noise conditions: one original (clean) condition and nine noisy conditions spanning three noise types at three intensity levels each. The ∆semWER metric quantifies the change in semantic word error rate after applying speech enhancement: positive values indicate that enhancement worsened the model's performance.

There are **zero configurations** where enhancement reduces semWER. The universality of this negative result suggests a fundamental incompatibility between MetricGAN+ enhancement and modern ASR models.

![](_page_10_Figure_1.svg)

<span id="page-10-0"></span>Figure 6: Parakeet semWER (%) and ∆semWER. Enhancement degrades performance across all noise conditions, though the magnitude is smaller than Whisper or Gemini. Parakeet maintains relatively consistent performance but still shows universal degradation from preprocessing.

Table 1: ∆semWER statistics. Positive values indicate enhancement increased semWER (degraded performance). ALL 40 configurations show degradation.

<span id="page-10-1"></span>

| Statistic                | All Configs | Original | Background | Short   | Gaussian |
|--------------------------|-------------|----------|------------|---------|----------|
| Configs with ∆semWER > 0 | 40 / 40     | 4 / 4    | 12 / 12    | 12 / 12 | 12 / 12  |
| Mean ∆semWER (%)         | +7.83       | +2.06    | +4.26      | +3.05   | +16.17   |
| Median ∆semWER (%)       | +3.32       | +1.86    | +2.91      | +2.49   | +11.77   |
| Max degradation (%)      | +46.57      | +3.19    | +17.0      | +9.67   | +46.57   |
| Min degradation (%)      | +1.11       | +1.32    | +1.11      | +1.36   | +2.57    |

# **5 Discussion**

Our results challenge the most common assumption that speech enhancement improves ASR. We present two main hypotheses:

**Hypothesis 1: Modern ASR Has Learned Internal Noise Robustness.** Whisper was explicitly trained on 680,000 hours of diverse, real-world audio including noisy recordings [\[Radford et al.](#page-14-3), [2022\]](#page-14-3). The model may have learned robust internal representations that handle typical acoustic noise without exter-

![](_page_11_Figure_1.svg)

<span id="page-11-0"></span>Figure 7: Gemini semWER (%) and ∆semWER. Enhancement dramatically degrades performance under Gaussian noise (semWER increases from 11% to 58% at amplitude 0.017). Other noise types show consistent but more modest degradation.

nal preprocessing. Enhancement may actually remove subtle acoustic cues (prosody, fine-grained spectral structure) that aid recognition.

**Hypothesis 2: Enhancement Artifacts.** Speech enhancement can introduce processing artifacts such as spectral smearing, temporal discontinuities and unnatural formant transitions. While these may be imperceptible to human listeners (and thus score well on PESQ/STOI), neural ASR models trained on natural speech may be sensitive to such artifacts.

## **5.1 Generalizability and Limitations**

**Generalizability:** Our results may extend to other modern large-scale ASR models (e.g., wav2vec 2.0) trained on diverse data, though verification is needed. The finding may not generalize to:

- Classical ASR systems (GMM-HMM) trained only on clean speech
- Small-scale models trained on limited data
- Extremely noisy conditions (SNR < 0 dB) beyond our test range

**Limitations:** Our study has several constraints:

![](_page_12_Figure_1.svg)

<span id="page-12-0"></span>Figure 8: Parrotlet-a semWER (%) and ∆semWER. As compared to other model Parrotlet-a shows least semWER in noisy condition but denoising still degrade the performance.

*Single Enhancement Method:* We evaluated only MetricGAN-plus-voicebank model. Other approaches (Transformer-based enhancement, diffusion models) may behave differently.

*Synthetic Noise:* We used synthetic methods of noise addition. While this enabled controlled comparisons, real clinical acoustics include reverberation and complex multi-source interference. Field validation is needed.

*Dataset Size:* With 500 recordings, our sample size is smaller than ideal for establishing a generalisation on this topic. The combinatorial nature of the number of experiments kept us from increasing the number.

*Medical Domain:* Results may differ for other domains (conversational, broadcast). Medical speech with technical terminology may exhibit different noise robustness characteristics.

*Indian English:* Our dataset comprises Indian English medical consultations. Generalization to other accents and languages requires verification.

## **5.2 Future Directions**

**Alternative Enhancement Methods:** Evaluate modern approaches (e.g., Transformer-based enhancement, diffusion models) to determine if degradation is specific to GAN-based methods.

**End-to-End Joint Training:** Develop architectures that jointly optimize enhancement and recognition for ASR accuracy rather than perceptual quality.

**Analysis of Failure Modes:** Detailed investigation of which acoustic phenomena cause enhancement to fail—formant distortion, prosody removal, artefact introduction—could guide improvement.

**Real-World Deployment Study:** Pilot deployments in Indian hospitals with original noisy and enhanced audio to validate results in production environments.

**Multi-Microphone Approaches:** Evaluate beamforming and spatial filtering as alternatives to singlechannel enhancement.

# **6 Conclusion**

This study systematically evaluated the effect of a widely used speech enhancement method, MetricGAN-plusvoicebank, on four modern ASR systems in a noisy clinical environment. Across all tested noise conditions and models, we observed that this particular enhancement approach consistently increased word error rate relative to directly transcribing the noisy audio, consistently degrading performance.

Our results suggest that enhancement approaches designed to optimize human perceptual metrics may not align well with the representations learned by large-scale ASR models trained on noisy, real-world data. Importantly, this does not imply that speech enhancement is inherently detrimental to ASR. Instead, it highlights that the effectiveness of enhancement is highly dependent on the specific technique employed, the noise characteristics, and the training methodology of the ASR model. Alternative approaches—such as ASR-aware enhancement, joint optimization, or domain-specific fine-tuning—may yield different outcomes and need further investigation.

From a practical viewpoint, our results suggest that denoising techniques like MetricGAN+ preprocessing should not be applied by default in medical ASR pipelines, and that its impact should be evaluated for each specific task and model. More broadly, these findings point to the need to re-examine common assumptions about audio preprocessing in the context of modern ASR systems that are already trained to operate under noisy conditions.

# **References**

- <span id="page-13-8"></span>Manav Agarwal and Anurag Misra. Robustness and hallucination in asr: A comparative evaluation of whisper and gemini. *IOSR Journal of Computer Engineering*, 27(3):65–69, 2025.
- <span id="page-13-9"></span>AI4Bhārat. indic-numtowords: A python library to convert numbers to words for indian languages and english. Python Package Index (PyPI), 2025. URL <https://pypi.org/project/indic-numtowords/>.
- <span id="page-13-2"></span>Jacob Benesty, Shoji Makino, and Jingdong Chen. *Speech Enhancement*. Springer, 2006.
- <span id="page-13-7"></span>Sebastian Braun and Hannes Gamper. Effect of noise suppression losses on speech distortion and asr performance. In *IEEE ICASSP*, pages 996–1000, 2022.
- <span id="page-13-5"></span>Marc Delcroix, Yusuke Kubo, Tomohiro Nakatani, and Atsushi Nakamura. Is speech enhancement preprocessing still relevant when using deep neural networks for acoustic modeling? In *INTERSPEECH*, pages 2992–2996, 2013.
- <span id="page-13-6"></span>Chris Donahue, Bo Li, and Rohit Prabhavalkar. Exploring speech enhancement with generative adversarial networks for robust speech recognition. In *IEEE ICASSP*, pages 5024–5028, 2018.
- <span id="page-13-4"></span>Robert Flynn and Edward Jones. Combined speech enhancement and auditory modelling for robust distributed speech recognition. *Speech Communication*, 50:797–809, 2008.
- <span id="page-13-3"></span>Szu-Wei Fu, Chien-Feng Liao, Yu Tsao, and Shou-De Lin. Metricgan: Generative adversarial networks based black-box metric scores optimization for speech enhancement. In *International Conference on Machine Learning (ICML)*, pages 2031–2041, 2019.
- <span id="page-13-0"></span>Szu-Wei Fu, Cheng Yu, Tsung-An Hsieh, Peter Plantinga, Mirco Ravanelli, Xugang Lu, and Yu Tsao. Metricgan+: An improved version of metricgan for speech enhancement. *arXiv preprint arXiv:2104.03538*, 2021.
- <span id="page-13-1"></span>Gemini Team. Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context. *arXiv preprint arXiv:2403.05530*, 2024.
- <span id="page-13-10"></span>Google. google-transliteration-api: A python interface for google's transliteration service. Python Package Index (PyPI), 2025. URL <https://pypi.org/project/google-transliteration-api/>.

- <span id="page-14-2"></span>Geoffrey Hinton et al. Deep neural networks for acoustic modeling in speech recognition. *IEEE Signal Processing Magazine*, 29(6):82–97, 2012.
- <span id="page-14-0"></span>B. E. Joseph, H. Mehazabeen, and M. U. Noise pollution in hospitals - a study of public perception. *Noise & Health*, 22(104):28–33, 2020. doi[:10.4103/nah.NAH\\_13\\_20](https://doi.org/10.4103/nah.NAH_13_20).
- <span id="page-14-13"></span>Anoop Kunchukuttan. The indicnlp library. GitHub repository, 2020. URL [https://github.com/](https://github.com/anoopkunchukuttan/indic_nlp_library) [anoopkunchukuttan/indic\\_nlp\\_library](https://github.com/anoopkunchukuttan/indic_nlp_library).
- <span id="page-14-6"></span>Philipos C. Loizou. *Speech Enhancement: Theory and Practice*. CRC Press, 2007.
- <span id="page-14-10"></span>Rustam Nasretdinov, Roman Korostik, and Ante Jukić. Robust speech recognition with schrödinger bridgebased speech enhancement. In *IEEE ICASSP*, pages 1–5, 2025.
- <span id="page-14-7"></span>Anusha Prasad, Preethi Jyothi, and Raghuraman Velmurugan. An investigation of end-to-end models for robust speech recognition. In *IEEE ICASSP*, pages 6893–6897, 2021.
- <span id="page-14-3"></span>Alec Radford, Jong Wook Kim, Tao Xu, Greg Brockman, Casey McLeavey, and Ilya Sutskever. Robust speech recognition via large-scale weak supervision. *arXiv preprint arXiv:2212.04356*, 2022.
- <span id="page-14-9"></span>A. K. Rai, S. D. Jaiswal, S. Prakash, B. P. Sree, and A. Mukherjee. Denoasr: Debiasing asrs through selective denoising. In *IEEE International Conference on Knowledge Graph (ICKG)*, pages 283–290, 2024.
- <span id="page-14-11"></span>Mirco Ravanelli et al. Speechbrain: A general-purpose speech toolkit. *arXiv preprint arXiv:2106.04624*, 2021.
- <span id="page-14-4"></span>Dinesh Rekesh, Nithin Rao Koluguri, Samuel Kriman, Somshubra Majumdar, Vahid Noroozi, Haicheng Huang, Oleksii Hrinchuk, Kishore Puvvada, Ankit Kumar, Jagadeesh Balam, and Boris Ginsburg. Fast conformer with linearly scalable attention for efficient speech recognition. In *IEEE Automatic Speech Recognition and Understanding Workshop (ASRU)*, 2023.
- <span id="page-14-8"></span>Ahmed Trabelsi, Loic Werey, Sylvain Warichet, and Eric Helbert. Is noise reduction improving open-source asr transcription engines quality? In *ICAART*, volume 3, pages 1221–1228, 2024.
- <span id="page-14-12"></span>Vasanth. karma-medeval: Evaluation framework for medical ai models. Python Package Index (PyPI), 2025. URL <https://pypi.org/project/karma-medeval/>.
- <span id="page-14-5"></span>Hainan Xu, Feng Jia, Somshubra Majumdar, Haicheng Huang, Shinji Watanabe, and Boris Ginsburg. Efficient sequence transduction by jointly predicting tokens and durations. In *International Conference on Machine Learning (ICML)*, pages 38491–38510, 2023.
- <span id="page-14-1"></span>Wei Zhu and Douglas O'Shaughnessy. Using noise reduction and spectral emphasis techniques to improve asr performance in noisy conditions. In *IEEE Workshop on Automatic Speech Recognition and Understanding (ASRU)*, pages 357–362, 2003.