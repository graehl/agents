# Word Alignment by Fine-tuning Embeddings on Parallel Corpora

## Zi-Yi Dou, Graham Neubig

Language Technologies Institute, Carnegie Mellon University {zdou, gneubig}@cs.cmu.edu

#### **Abstract**

Word alignment over parallel corpora has a wide variety of applications, including learning translation lexicons, cross-lingual transfer of language processing tools, and automatic evaluation or analysis of translation out-The great majority of past work on word alignment has worked by performing unsupervised learning on parallel text. Recently, however, other work has demonstrated that pre-trained contextualized word embeddings derived from multilingually trained language models (LMs) prove an attractive alternative, achieving competitive results on the word alignment task even in the absence of explicit training on parallel data. In this paper, we examine methods to marry the two approaches: leveraging pre-trained LMs but finetuning them on parallel text with objectives designed to improve alignment quality, and proposing methods to effectively extract alignments from these fine-tuned models. We perform experiments on five language pairs and demonstrate that our model can consistently outperform previous state-of-the-art models of all varieties. In addition, we demonstrate that we are able to train multilingual word aligners that can obtain robust performance on different language pairs. Our aligner, AWE-SOME (Aligning Word Embedding Spaces of Multilingual Encoders), with pre-trained models is available at https://github. com/neulab/awesome-align.

#### 1 Introduction

Word alignment is a useful tool to tackle a variety of natural language processing (NLP) tasks, including learning translation lexicons (Ammar et al., 2016; Cao et al., 2019), cross-lingual transfer of language processing tools (Yarowsky et al., 2001; Padó and Lapata, 2009; Tiedemann, 2014; Agić et al., 2016; Mayhew et al., 2017; Nicolai and Yarowsky, 2019), semantic parsing (Herzig and Berant, 2018) and

<span id="page-0-0"></span>![](_page_0_Figure_7.svg)

Figure 1: Cosine similarities between subword representations in a parallel sentence pair before and after fine-tuning. Red boxes indicate the gold alignments.

speech recognition (Xu et al., 2019). In particular, word alignment plays a crucial role in many machine translation (MT) related methods, including guiding learned attention (Liu et al., 2016), incorporating lexicons during decoding (Arthur et al., 2016), domain adaptation (Hu et al., 2019), unsupervised MT (Ren et al., 2020) and automatic evaluation or analysis of translation models (Bau et al., 2018; Stanovsky et al., 2019; Neubig et al., 2019; Wang et al., 2020). However, with neural networks advancing the state of the arts in almost every field of NLP, tools developed based on the 30-yearold IBM word-based translation models (Brown et al., 1993), such as GIZA++ (Och and Ney, 2003) or fast-align (Dyer et al., 2013), remain popular choices for word alignment tasks.

One alternative to using statistical word-based translation models to learn alignments would be to instead train state-of-the-art neural machine translation (NMT) models on parallel corpora, and extract alignments therefrom, as examined by Luong et al. (2015); Garg et al. (2019); Zenkel et al. (2020). However, these methods have two disadvantages (also shared with more traditional alignment methods): (1) they are directional and the source and target side are treated differently and (2) they cannot easily take advantage of large-scale contextualized

word embeddings derived from language models (LMs) multilingually trained on monolingual corpora [\(Devlin et al.,](#page-9-8) [2019;](#page-9-8) [Lample and Conneau,](#page-10-5) [2019;](#page-10-5) [Conneau et al.,](#page-9-9) [2020\)](#page-9-9), which have proven useful in other cross-lingual transfer settings [\(Li](#page-10-6)[bovicky et al.](#page-10-6) ` , [2019;](#page-10-6) [Hu et al.,](#page-10-7) [2020b\)](#page-10-7). In the field of word alignment, [Sabet et al.](#page-11-6) [\(2020\)](#page-11-6) have recently proposed methods to align words using multilingual contextualized embeddings and achieve good performance even in the absence of explicit training on parallel data, suggesting that these are an attractive alternative for neural word alignment.

In this paper, we investigate if we can combine the best of the two lines of approaches. Concretely, we leverage pre-trained LMs and fine-tune them on parallel text with not only LM-based objectives, but also unsupervised objectives over the parallel corpus designed to improve alignment quality. Specifically, we propose a self-training objective, which encourages aligned words to have further closer contextualized representations, and a parallel sentence identification objective, which enables the model to bring parallel sentences' representations closer to each other. In addition, we propose to effectively extract alignments from these fine-tuned models using probability thresholding or optimal transport.

We perform experiments on five different language pairs and demonstrate that our model can achieve state-of-the-art performance on all of them. In analysis, we find that these approaches also generate more aligned contextualized representations after fine-tuning (see Figure [1](#page-0-0) as an example) and we can incorporate supervised signals within our paradigm. Importantly, we show that it is possible to train multilingual word aligners that can obtain robust performance even in zero-shot settings, making them a valuable tool that can be used out-ofthe-box with good performance over a wide variety of language pairs.

## 2 Methods

Formally, the task of word alignment can be defined as: given a sentence x = hx1, · · · , xni in the source language and its corresponding parallel sentence y = hy1, · · · , ymi in the target language, a word aligner needs to find a set of pairs of source and target words:

$$A = \{ \langle x_i, y_j \rangle : x_i \in \mathbf{x}, y_j \in \mathbf{y} \},\$$

where for each word pair hx<sup>i</sup> , y<sup>j</sup> i, x<sup>i</sup> and y<sup>j</sup> are semantically similar to each other within the context of the sentence.

In the following paragraphs, we will first illustrate how we extract alignments from contextualized word embeddings, then describe our objectives designed to improve alignment quality.

## <span id="page-1-0"></span>2.1 Extracting Alignments from Embeddings

Contextualized word embedding models such as BERT [\(Devlin et al.,](#page-9-8) [2019\)](#page-9-8) and RoBERTa [\(Liu](#page-10-8) [et al.,](#page-10-8) [2019\)](#page-10-8) represent words using continuous vectors calculated in context, and have achieved impressive performance on a diverse array of NLP tasks. Multilingually trained word embedding models such as multilingual BERT can generate contextualized embeddings across different languages. These models can be used to extract contextualized word embeddings h<sup>x</sup> = hhx<sup>1</sup> , · · · , hx<sup>n</sup> i and h<sup>y</sup> = hhy<sup>1</sup> , · · · , hymi for each pair of parallel sentences x and y. Specifically, this is done by extracting the hidden states of the i-th layer of the model, where i is an empirically-chosen hyper-parameter. Given these contextualized word embeddings, we propose two methods to calculate unidirectional alignment scores based on probability simplexes and optimal transport. We then turn these alignment scores into alignment matrices and reconcile alignments in the forward and backward directions.

Probability Thresholding. In this method, for each word in the source/target sentence, we calculate a value on the probability simplex for each word in the aligned target/source sentence, and then select all values that exceed a particular threshold as "aligned" words. Concretely, taking inspiration from attention mechanisms [\(Bahdanau et al.,](#page-9-10) [2015;](#page-9-10) [Vaswani et al.,](#page-12-5) [2017\)](#page-12-5), we take the contextualized embeddings h<sup>x</sup> and h<sup>y</sup> and compute the dot products between them and get the similarity matrix:

$$S = h_{\mathbf{x}} h_{\mathbf{y}}^T.$$

Then, we apply a normalization function N to convert the similarity matrix into values on the probability simplex Sxy = N (S), and treat Sxy as the source-to-target alignment matrix. In this paper, we propose to use *softmax* and a sparse variant α-entmax [\(Peters et al.,](#page-11-7) [2019\)](#page-11-7) to do the normalization. Compared with the *softmax* function, α-entmax can produce sparse alignments for any α > 1 and assign non-zero probability to a short

<span id="page-2-1"></span>![](_page_2_Figure_0.svg)

Figure 2: Extracting word alignments from multilingual BERT using probability thresholding (*softmax*). Red boxes denote the gold alignments.

list of plausible word pairs, where a higher  $\alpha$  will lead to a more sparse alignment.

**Optimal Transport.** The goal of optimal transport (Monge, 1781; Cuturi, 2013) is to find a mapping that moves probability from one distribution to another, which can be used to find an optimal matching of similar words between two sequences (Kusner et al., 2015). Formally, in a discrete optimal transport problem, we are given two point sets  $\{x_i\}_{i=1}^n$  and  $\{y_j\}_{j=1}^m$  associated with their probability distributions  $p_x$  and  $p_y$  where  $\sum_i p_{x_i} = 1$  and  $\sum_j p_{y_j} = 1$ . Also, a function  $C(x_i, y_i)$  defines the cost of moving point  $x_i$  to  $y_i$ . The goal of optimal transport is to find a mapping that moves probability mass from  $\{x_i\}_{i=1}^n$  to  $\{y_j\}_{j=1}^m$  and the total cost of moving the mass between points is minimized. In other words, it finds the transition matrix  $S_{xy}$  that minimizes:

$$\sum_{i,j} C(x_i, y_j) S_{\mathbf{x}\mathbf{y}_{ij}},\tag{1}$$

where  $S_{xy}\mathbf{1}_m = p_x$  and  $S_{xy}^T\mathbf{1}_n = p_y$ . The resulting transition matrix is self-normalized and sparse (Swanson et al., 2020), making it appealing alternative towards extracting alignments from word embeddings.

In this paper, we propose to adapt optimal transport techniques to the task of word alignment. Concretely, we treat the parallel sentences  $\mathbf{x}$  and  $\mathbf{y}$  as two point sets and assume each word is uniformly distributed. The cost function is obtained by computing the pairwise distance (e.g. cosine distance) between  $h_{\mathbf{x}}$  and  $h_{\mathbf{y}}$ , and all the distance values are scaled to [0, 1] with min-max normalization. The optimal transition matrix  $S_{\mathbf{x}\mathbf{y}}$  to Equation 1 can be calculated using the Sinkhorn-Knopp matrix scaling algorithm (Sinkhorn and Knopp, 1967). If the value of  $S_{\mathbf{x}\mathbf{y}_{ij}}$  is high,  $x_i$  and  $y_j$  are likely to have

similar semantics and values that exceed a particular threshold will be considered as "aligned".

Extracting Bidirectional Alignments. After we obtain both the source-to-target and target-to-source alignment probability matrices  $S_{xy}$  and  $S_{yx}$  using the previous methods, we can deduce the final alignment matrix by taking the intersection of the two matrices:

$$A = (S_{\mathbf{x}\mathbf{y}} > c) * (S_{\mathbf{y}\mathbf{x}}^T > c),$$

where c is a threshold and  $A_{ij} = 1$  means  $x_i$  and  $y_i$  are aligned.

Note that growing heuristics such as *grow-diag-final* (Och and Ney, 2000; Koehn et al., 2005) that are popular in statistical word aligners can also be applied in our alignment extraction algorithms, and we will demonstrate the effect of these heuristics in the experiment section.

<span id="page-2-0"></span>Handling Subwords. Subword segmentation techniques (Sennrich et al., 2016; Kudo and Richardson, 2018) are widely used in training LMs, thus the above alignment extraction methods can only produce alignments on the subword level. To convert them to word alignments, we follow previous work (Sabet et al., 2020; Zenkel et al., 2020) and consider two words to be aligned if any of their subwords are aligned. Figure 2 shows a concrete example of how we extract word-level alignments from a pre-trained embedding model.

# 2.2 Fine-tuning Contextualized Embeddings for Word Alignment

While language models can be used to produce reasonable word alignments even without any fine-tuning (Sabet et al., 2020), we propose objectives that further improve their alignment ability if we have access to parallel data.

Masked Language Modeling (MLM). [Guru](#page-10-13)[rangan et al.](#page-10-13) [\(2020\)](#page-10-13) suggest that we can gain improvements in downstream tasks by further pretraining LMs on the task datasets. Therefore, we propose to fine-tune the LMs with a masked language modeling objective on both the source and target side of parallel corpora. Specifically, given a pair of parallel sentences x and y, we choose 15% of the token positions randomly for both x and y, and for each chosen token, we replace it with (1) the [MASK] token 80% of the time (2) a random token 10% of the time and (3) unchanged 10% of the time. The model is trained to reconstruct the original tokens given the masked sentences x mask and y mask:

$$L_{MLM} = \log p(\mathbf{x}|\mathbf{x}^{mask}) + \log p(\mathbf{y}|\mathbf{y}^{mask}).$$
 (2)

Translation Language Modeling (TLM). The MLM objective only requires monolingual data and the model cannot make direct connections between parallel sentences. To solve the issue, similarly to [Lample and Conneau](#page-10-5) [\(2019\)](#page-10-5), we concatenate parallel sentences x and y and perform MLM on the concatenated data. Compared with MLM, the translation language modeling (TLM) objective enable the model to align the source and target representations. Different from [Lample and Conneau](#page-10-5) [\(2019\)](#page-10-5), we feed source and target sentences twice in different orders instead of resetting the positions of target sentences:

$$L_{TLM} = \log p([\mathbf{x}; \mathbf{y}] | [\mathbf{x}^{mask}; \mathbf{y}^{mask}]) + \log p([\mathbf{y}; \mathbf{x}] | [\mathbf{y}^{mask}; \mathbf{x}^{mask}]).$$
(3)

Self-training Objective (SO). We also propose a self-training objective for fine-tuning LMs which is similar to the EM algorithm used in the IBM models and the agreement constraints in [Tamura](#page-11-12) [et al.](#page-11-12) [\(2014\)](#page-11-12). Specifically, at each training step, we first use our alignment extraction methods (described in Section [2.1\)](#page-1-0) to extract the alignment A for x and y, then maximize the following objective:

<span id="page-3-1"></span>
$$L_{SO} = \sum_{i,j} A_{ij} \frac{1}{2} \left( \frac{S_{\mathbf{x}\mathbf{y}_{ij}}}{n} + \frac{S_{\mathbf{y}\mathbf{x}_{ij}}}{m} \right). \tag{4}$$

Intuitively, this objective encourages words aligned in the first pass of alignment to have further closer contextualized representations. In addition, because of the intersection operation during extraction, the self-training objective can ideally reduce

<span id="page-3-0"></span>

|               | De-En | Fr-En | Ro-En | Ja-En | Zh-En |
|---------------|-------|-------|-------|-------|-------|
| #Train Sents. | 1.9M  | 1.1M  | 450K  | 444K  | 40K   |
| #Test Sents.  | 508   | 447   | 248   | 582   | 450   |

Table 1: Statistics of datasets.

spurious alignments and encourage the source-totarget and target-to-source alignments to be symmetrical to each other by exploiting their agreement [\(Liang et al.,](#page-10-14) [2006\)](#page-10-14).

Parallel Sentence Identification (PSI). We also propose a contrastive parallel sentence identification loss that attempts to make parallel sentences more similar than mismatched sentence pairs [\(Liu](#page-10-15) [and Sun,](#page-10-15) [2015;](#page-10-15) [Legrand et al.,](#page-10-16) [2016\)](#page-10-16). This encourages the overall alignments of embeddings on both word and sentence level to be closer together. Concretely, we randomly select a pair of parallel or non-parallel sentences hx 0 , y 0 i from the training data with equal probability. Then, the model is required to predict whether the two sampled sentences are parallel or not. The representation of the first [CLS] token is fed into a multi-layer perceptron to output a prediction score s(x 0 , y 0 ). Denoting the binary label as l, the objective function can be written as:

$$L_{PSI} = l \log s(\mathbf{x}', \mathbf{y}') + (1 - l) \log(1 - s(\mathbf{x}', \mathbf{y}')).$$
(5)

Consistency Optimization (CO). While the self-training objective can potentially improve the symmetricity between forward and backward alignments, following previous work on machine translation and multilingual representation learning [\(Cohn](#page-9-12) [et al.,](#page-9-12) [2016;](#page-9-12) [Zhang et al.,](#page-12-6) [2019;](#page-12-6) [Hu et al.,](#page-10-17) [2020a\)](#page-10-17), we use an objective to explicitly encourage the consistency between the two alignment matrices. Specifically, we maximize the trace of S T xySyx:

$$L_{CO} = -\frac{\operatorname{trace}(S_{\mathbf{x}\mathbf{y}}^{\mathrm{T}}S_{\mathbf{y}\mathbf{x}})}{\min(m, n)}.$$
 (6)

Our Final Objective. In summary, our training objective is a combination of the proposed objectives and we train the model with them jointly at each training step:

$$L = L_{MLM} + L_{TLM} + L_{SO} + L_{PSI} + \beta L_{CO},$$

where β is set to 0 or 1 in our experiments.

<span id="page-4-1"></span>

| Model                | Setting                 | De-En | Fr-En | Ro-En | Ja-En | Zh-En |
|----------------------|-------------------------|-------|-------|-------|-------|-------|
| Baseline             |                         |       |       |       |       |       |
| SimAlign             | w/o fine-tuning         | 18.8  | 7.6   | 27.2  | 46.6  | 21.6  |
| fast align           | bilingual               | 27.0  | 10.5  | 32.1  | 51.1  | 38.1  |
| eflomal              | bilingual               | 22.6  | 8.2   | 25.1  | 47.5  | 28.7  |
| GIZA++               | bilingual               | 20.6  | 5.9   | 26.4  | 48.0  | 35.1  |
| Zenkel et al. (2020) | bilingual               | 16.0  | 5.0   | 23.4  | -     | -     |
| Chen et al. (2020)   | bilingual               | 15.4  | 4.7   | 21.2  | -     | -     |
| Ours                 |                         |       |       |       |       |       |
|                      | w/o fine-tuning         | 18.1  | 5.6   | 29.0  | 46.3  | 18.4  |
|                      | bilingual               | 16.1  | 4.1   | 23.4  | 38.6  | 15.4  |
| α-entmax             | multilingual (β<br>= 0) | 15.4  | 4.1   | 22.9  | 37.4  | 13.9  |
|                      | multilingual (β<br>= 1) | 15.0  | 4.5   | 20.8  | 38.7  | 14.5  |
|                      | zero-shot               | 16.0  | 4.3   | 28.4  | 44.0  | 13.9  |
|                      | w/o fine-tuning         | 17.4  | 5.6   | 27.9  | 45.6  | 18.1  |
|                      | bilingual               | 15.6  | 4.4   | 23.0  | 38.4  | 15.3  |
| softmax              | multilingual (β<br>= 0) | 15.3  | 4.4   | 22.6  | 37.9  | 13.6  |
|                      | multilingual (β<br>= 1) | 15.1  | 4.5   | 20.7  | 38.4  | 14.5  |
|                      | zero-shot               | 15.7  | 4.6   | 27.2  | 43.7  | 14.0  |

Table 2: Performance (AER) of our models in bilingual, multilingual and zero-shot settings. The best scores for each alignment extraction method are in bold and the overall best scores are in *italicized bold*.

## 3 Experiments

In this section, we first present our main results, then conduct several ablation studies and analyses of our models.

### 3.1 Setup

Datasets. We perform experiments on five different language pairs, namely German-English (De-En), French-English (Fr-En), Romanian-English (Ro-En), Japanese-English (Ja-En) and Chinese-English (Zh-En). For the De-En, Fr-En, Ro-En datasets, we follow the experimental setting of previous work [\(Zenkel et al.,](#page-12-7) [2019;](#page-12-7) [Garg et al.,](#page-9-7) [2019;](#page-9-7) [Zenkel et al.,](#page-12-4) [2020\)](#page-12-4). The training and test data for Ro-En and Fr-En are provided by [Mihalcea](#page-10-18) [and Pedersen](#page-10-18) [\(2003\)](#page-10-18). The Ro-En training data are also augmented by the Europarl v8 corpus [\(Koehn,](#page-10-19) [2005\)](#page-10-19). For the De-En data, the Europarl v7 corpus is used as training data and the gold alignments are provided by [Vilar et al.](#page-12-8) [\(2006\)](#page-12-8). The Ja-En dataset is obtained from the Kyoto Free Translation Task (KFTT) word alignment data [\(Neubig,](#page-11-13) [2011\)](#page-11-13), and the Japanese sentences are tokenized with the KyTea tokenizer [\(Neubig et al.,](#page-11-14) [2011\)](#page-11-14). The Zh-En dataset is obtained from the TsinghuaAligner website[1](#page-4-0) . We treat their evaluation set as the training data and use the test set in [Liu and Sun](#page-10-15) [\(2015\)](#page-10-15). The De-En, En-Fr, Zh-En datasets contain the distinction between sure and possible alignment links. The statistics of these datasets are shown in Table [1.](#page-3-0) We use the Ja-En development set to tune the hyper-parameters.

Baselines. We compare our models with:

- fast align [\(Dyer et al.,](#page-9-6) [2013\)](#page-9-6): a popular statistical word aligner which is a simple, fast reparameterization of IBM Model 2.
- eflomal [\(Ostling and Tiedemann](#page-11-15) ¨ , [2016\)](#page-11-15): an efficient statistical word aligner using a Bayesian model with Markov Chain Monte Carlo (MCMC) inference.
- GIZA++ [\(Och and Ney,](#page-11-5) [2003;](#page-11-5) [Gao and Vogel,](#page-9-14) [2008\)](#page-9-14): an implementation of IBM models. Following previous work [\(Zenkel et al.,](#page-12-4) [2020\)](#page-12-4), we use five iterations each for Model 1, the HMM model, Model 3 and Model 4.
- SimAlign [\(Sabet et al.,](#page-11-6) [2020\)](#page-11-6): a BERT-based word aligner that is not fine-tuned on any parallel data. The authors propose three alignment extraction methods and we implement their IterMax model with default parameters.
- [Zenkel et al.](#page-12-4) [\(2020\)](#page-12-4) and [Chen et al.](#page-9-13) [\(2020\)](#page-9-13): two state-of-the-art neural word aligners based on MT models.

<span id="page-4-0"></span><sup>1</sup>[http://nlp.csai.tsinghua.edu.cn/˜ly/](http://nlp.csai.tsinghua.edu.cn/~ly/systems/TsinghuaAligner/TsinghuaAligner.html) [systems/TsinghuaAligner/TsinghuaAligner.](http://nlp.csai.tsinghua.edu.cn/~ly/systems/TsinghuaAligner/TsinghuaAligner.html) [html](http://nlp.csai.tsinghua.edu.cn/~ly/systems/TsinghuaAligner/TsinghuaAligner.html)

Implementation Details. Our main results are obtained by using the probability thresholding method on the contextualized embeddings in the 8-th layer of multilingual BERT-Base (mBERT; Devlin et al. (2019)) and we will discuss this choice in our ablation studies. We use the AdamW optimizer (Loshchilov and Hutter, 2019) with a learning rate of 2e-5 and the batch size is set to 8. Following Peters et al. (2019), we set  $\alpha$  to 1.5 for  $\alpha$ -entmax. The threshold c is set to 0 for  $\alpha$ -entmax and 0.001 for *softmax* and optimal transport. Unless otherwise stated,  $\beta$  is set to 0. We mainly evaluate the model performance using Alignment Error Rate (AER).

#### 3.2 Main Results

We first train our model on each individual language pair, then investigate if it is possible to train multilingual word aligners.

**Bilingual Model Performance.** From Table 2, we can see that our *softmax* model can achieve consistent improvements over the baseline models, demonstrating the effectiveness of our proposed method. Surprisingly, directly extracting alignments from mBERT (the *w/o fine-tuning* setting) can already achieve better performance than the popular statistical word aligner GIZA++ on 4 out of 5 settings, especially in the Zh-En setting where the size of parallel data is small.

Multilingual Model Performance. We also randomly sample 200k parallel sentence pairs from each language pair (except for Zh-En where we take all of its 40k parallel sentences) and concatenate them together to train multilingual word aligners. As shown in Table 2, the multilingually trained word aligners can achieve further improvements and they consistently outperform our bilingual word aligners and all the baselines even though the size of training data for each individual language pair is smaller. The results demonstrate that we can indeed obtain a neural word aligner that has stateof-the-art and robust performance across different language pairs. We also test the performance of our consistency optimization objective in this setting. We can see that incorporating this objective ( $\beta$ =1) can significantly improve the model performance on Ro-En, while it also deteriorates the Ja-En and Zh-En performance by a non-negligible margin. We find that this is because the CO objective can significantly improve the alignment recall while sacrificing the precisions, and our Ro-En dataset

<span id="page-5-0"></span>

|       | Component        | De-En | Fr-En | Ro-En | Ja-En | Zh-En | Speed |
|-------|------------------|-------|-------|-------|-------|-------|-------|
| Prob. | softmax          | 17.4  | 5.6   | 27.9  | 45.6  | 18.1  | 33.22 |
| Prob. | $\alpha$ -entmax | 18.1  | 5.6   | 29.0  | 46.3  | 18.4  | 32.36 |
| ОТ    | Cosine           | 24.4  | 15.7  | 33.7  | 54.0  | 31.1  | 3.36  |
|       | Dot Product      | 25.4  | 17.1  | 34.1  | 54.2  | 30.9  | 3.82  |
|       | Euclidean        | 20.7  | 15.1  | 33.3  | 53.2  | 29.8  | 3.05  |

Table 3: Comparisons of probability thresholding (Prob.) and optimal transport (OT) for alignment extraction. We try both softmax and  $\alpha$ -entmax for probability thresholding and different cost functions for optimal transport. We measure both the extraction speed (#sentences/seconds) and the alignment quality (AER) on five language pairs, namely German-English (De-En), French-English (Fr-En), Romanian-English (Ro-En), Japanese-English (Ja-En), and Chinese-English (Zh-En). The best scores are in **bold**.

tends to favor models with high recall and the Ja-En and Zh-En datasets have an opposite tendency.

**Zero-Shot Performance.** In this paragraph, we want to find out how our models perform on language pairs that it has never seen during training. To this end, for each language pair, we train our model with data of all the other language pairs and test its performance on the target language pair. Results in Table 2 demonstrate that training our models with parallel data on *other* language pairs can still improve the model performance on the target language pair. This is a very important result, as it indicates that our model can be used as a off-the-shelf tool for multilingual word alignment for any language supported by the underlying embeddings, *regardless of whether parallel data has been used for training or not*.

#### 3.3 Ablation Studies

In this part, we compare the performance of different alignment extraction methods, pre-trained embedding models and training objectives.

Alignment Extraction Methods. We first compare the performance of our two proposed alignment extraction methods, namely the probability thresholding and optimal transport techniques. We use the representations of the 8-th layer of mBERT following Sabet et al. (2020).

As shown in Table 3, probability thresholding methods can consistently outperform optimal transport by a large margin on the five language pairs. In addition, probability thresholding methods are much faster than optimal transport. softmax is marginally better than  $\alpha$ -entmax, yet one advantage of  $\alpha$ -entmax is that we do not need to manually set

<span id="page-6-0"></span>

| Model            | Layer | De-En | Fr-En | Zh-En |
|------------------|-------|-------|-------|-------|
|                  | 7     | 18.7  | 6.1   | 19.1  |
| mBERT            | 8     | 17.4  | 5.6   | 18.1  |
|                  | 9     | 18.8  | 6.1   | 20.1  |
|                  | 4     | 21.1  | 6.8   | 25.3  |
| XLM-15 (MLM)     | 5     | 20.4  | 6.1   | 26.1  |
|                  | 6     | 23.2  | 7.7   | 33.3  |
|                  | 4     | 16.4  | 4.9   | 18.6  |
| XLM-15 (MLM+TLM) | 5     | 16.2  | 4.7   | 23.7  |
|                  | 6     | 18.8  | 5.7   | 26.2  |
|                  | 7     | 20.5  | 8.5   | 30.8  |
| XLM-100 (MLM)    | 8     | 19.8  | 8.2   | 28.6  |
|                  | 9     | 19.9  | 8.8   | 29.3  |
|                  | 5     | 24.4  | 10.3  | 33.2  |
| XLM-R            | 6     | 23.1  | 9.2   | 30.7  |
|                  | 7     | 24.7  | 11.5  | 28.1  |

Table 4: Comparisons of different LMs in terms of AER. We extract alignments using *softmax* and take representations from different layers of LMs. The best scores for each individual model are in **bold** and the overall best scores are in *italicized bold*.

the threshold. Therefore, we use both *softmax* and  $\alpha$ -entmax to obtain the main results.

Pre-trained Embedding Models. In this paragraph, we investigate the performance of three different types of pre-trained embedding models, including mBERT, XLM (Lample and Conneau, 2019) and XLM-R (Conneau et al., 2020). For XLM, we have tried its three released models: 1) XLM-15 (MLM) pre-trained with MLM and supports 15 languages; 2) XLM-15 (MLM+TLM) pre-trained with both the MLM and TLM objectives and supports 15 languages; 3) XLM-100 (MLM) pre-trained with MLM and supports 100 languages. We use *softmax* to extract the alignments.

Because XLM-15 does not support Japanese or Romanian, we only report the performance on the three other language pairs in Table 4. We take representations from different layers and report the performance of the best three layers. We can see that while XLM-15 (MLM+TLM) can achieve the best performance on De-En and Fr-En, the best layer is not consistent across language pairs. On the other hand, the optimal configurations for mBERT are consistent across language pairs. In addition, considering mBERT supports many more languages than XLM-15 (MLM+TLM), we will use mBERT in the following sections.

**Training Objectives.** We also conduct ablation studies on each of our training objectives. We can see from Table 5 that the self-training objective can best improve the model performance. Also,

the translation language modeling and parallel sentence identification objectives can marginally benefit the model. The masked language modeling objective, on the other hand, cannot always improve the model and can sometimes even deteriorate the model performance, possibly because the TLM objective already provides the model with sufficient supervision signals.

#### 3.4 Analysis

We conduct several analyses to better understand our models. Unless otherwise stated, we perform experiments on the *softmax* model using mBERT.

**Incorporating Supervised Signals.** We investigate if our models can benefit from supervised signals. If we have access to word-level gold labels for word alignment, we can simply utilize them in our self-training objectives. Specifically, we can set  $A_{ij}$  in Equation 4 to 1 if and only if they are aligned. In our experimental settings, we have gold labels for all the Zh-En sentences and 653 sentences from the Ja-En development set. Table 6 demonstrates that training our models with as few as 653 labeled sentences can dramatically improve the alignment quality, and combining labeled and unlabeled parallel data can further improve the model performance. This analysis demonstrate the generality of our models as they can also be applied in semisupervised settings.

Growing Heuristics. As stated in Section 2.1, because our alignment extraction methods essentially take the intersection of forward and backward alignments, growing heuristics can also be applied in our settings. The main motivation of growing heuristics is to improve the recall of the resulting alignments. While effective in statistical word aligners, as shown in Table 7, the growing heuristics only improve our alignment extraction method on the vanilla mBERT model in the Ro-En setting while degrading the model performance on all the other language pairs. After fine-tuning, the growing heuristics can only hurt the model performance, possibly because the self-training objective encourages the forward and backward alignments to be symmetrical. Based on these results, we do not adopt the growing heuristics in our models.

Annotation Projection. Word alignment has been a useful tool in cross-lingual annotation projection (Yarowsky et al., 2001; Nicolai and Yarowsky, 2019). Therefore, it would be inter-

<span id="page-7-0"></span>

| Model   | Objective   | De-En | Fr-En             | Ro-En | Ja-En | Zh-En |
|---------|-------------|-------|-------------------|-------|-------|-------|
|         | All         | 15.3  | 4.4               | 22.6  | 37.9  | 13.6  |
|         | Āll w/o MLM | 15.3  | $\bar{4}.\bar{4}$ | 22.8  | 38.6  | 13.7  |
| softmax | All w/o TLM | 15.5  | 4.7               | 22.9  | 39.7  | 14.0  |
|         | All w/o SO  | 16.9  | 4.8               | 23.0  | 39.1  | 15.4  |
|         | All w/o PSI | 15.4  | 4.4               | 22.7  | 37.9  | 13.8  |

Table 5: Ablation studies on our training objectives in multilingual settings.

<span id="page-7-4"></span>![](_page_7_Figure_2.svg)

Figure 3: An example of extracting alignments from our fine-tuned model using *softmax*. Red boxes indicate the gold alignments. The fine-tuned model can generate more accurate alignments then vanilla mBERT (Figure 2).

<span id="page-7-1"></span>

| Lang. | Unsup. | Sup. | Semi-Sup. |
|-------|--------|------|-----------|
| Zh-En | 15.3   | 12.5 | -         |
| Ja-En | 38.4   | 31.6 | 30.0      |

Table 6: Incorporating supervised word alignment signals into our model can further improve the model performance in terms of AER.

<span id="page-7-2"></span>

| Model       | Ext.     | De-En | Fr-En | Ro-En | Ja-En | Zh-En |
|-------------|----------|-------|-------|-------|-------|-------|
|             | X-En     | 24.7  | 14.4  | 31.9  | 54.7  | 27.4  |
|             | En-X     | 22.6  | 12.2  | 32.0  | 52.7  | 29.9  |
| mBERT       | softmax  | 17.4  | 5.6   | 27.9  | 45.6  | 18.1  |
|             | gd       | 18.7  | 9.2   | 27.0  | 48.5  | 23.4  |
|             | gd-final | 18.6  | 9.3   | 26.9  | 48.7  | 23.2  |
|             | X-En     | 20.2  | 12.9  | 25.4  | 42.1  | 19.3  |
|             | En-X     | 18.1  | 9.3   | 25.9  | 41.7  | 23.5  |
| Ours-Multi. | softmax  | 15.3  | 4.4   | 22.6  | 37.9  | 13.6  |
|             | gd       | 16.3  | 8.1   | 23.1  | 38.2  | 18.3  |
|             | gd-final | 16.5  | 8.3   | 23.2  | 38.7  | 18.5  |

Table 7: The *grow-diag-final* heuristic can only improve our alignment extraction method in the Romanian-English setting without fine-tuning. "gd" refers to grow-diag.

esting to see if our model can be beneficial in these settings. To this end, we evaluate our model and baselines on cross-lingual named entity recognition (NER). We train a BERT-based NER model on the CoNLL 2003 English data (Tjong Kim Sang and De Meulder, 2003) and test it on the CoNLL 2002 Spanish data (Tjong Kim Sang, 2002). We use Google Translate to translate Spanish test set into English, predict the labels using the NER model, then project the labels from English to Spanish us-

<span id="page-7-3"></span>

| Model               | Prec. % | Rec. % | <b>F</b> <sub>1</sub> % |
|---------------------|---------|--------|-------------------------|
| BERT-En (zero-shot) | 53.1    | 54.3   | 52.7                    |
| fast_align          | 51.5    | 59.8   | 55.2                    |
| GIZA++              | 56.5    | 64.1   | 60.0                    |
| SimAlign            | 59.9    | 67.6   | 63.5                    |
| Ours                | 60.6    | 68.5   | 64.3                    |

Table 8: Our model is also effective in an annotation projection setting where we train a BERT-based NER model on English data and test it on Spanish data. The best scores are in **bold**.

ing word aligners. From Table 8, we can see that our model is also better than baselines in this setting, demonstrating its usefulness in cross-lingual annotation projection.

Sentence-Level Representation Transfer. We also test if the aligned representations are beneficial for sentence-level cross-lingual transfer. In doing so, we perform experiments on XNLI (Conneau et al., 2018), which evaluates cross-lingual sentence representations in 15 languages on the task of natural language inference (NLI). We train our models with the provided 10k parallel data on the 15 languages, fine-tune our model on the English NLI data, then test its performance on other languages. As shown in Table 9, our model can outperform the baseline, indicating the aligned word representations can also be helpful for sentence-level cross-lingual transfer.

<span id="page-8-0"></span>

| Model | En   | Fr    | Es    | De    | El   | Bg    | Ru   | Tr    | Ar    | Vi   | Th    | Zh   | Hi    | Sw    | Ur    | Ave.  |
|-------|------|-------|-------|-------|------|-------|------|-------|-------|------|-------|------|-------|-------|-------|-------|
| mBERT | 81.3 | 73.4  | 74.3  | 70.5  | 66.9 | 68.2  | 68.5 | 59.5  | 64.3  | 70.6 | 50.7  | 68.8 | 59.3  | 49.4  | 57.5  | 65.5  |
| Ours  | 81.5 | 74.1* | 74.9* | 71.2* | 67.1 | 68.7* | 68.6 | 61.0* | 66.2* | 70.5 | 53.8* | 69.1 | 59.8* | 50.6* | 58.6* | 66.4* |

Table 9: Results of mBERT and our fine-tuned model on XNLI [\(Conneau et al.,](#page-9-15) [2018\)](#page-9-15). Our objectives can improve the model cross-lingual transfer ability. "\*" denotes significant differences using paired bootstrapping (p<0.05) .

Alignment Examples. We also conduct qualitative analyses as shown in Figure [1,](#page-0-0) [2](#page-2-1) and [3.](#page-7-4) After fine-tuning, the learned contextualized representations are more aligned, as the cosine distances between semantically similar words become closer, and the extracted alignments are more accurate. More examples are shown in Appendix [B.](#page-14-0)

## 4 Related Work

Based on the IBM translation models [\(Brown et al.,](#page-9-5) [1993\)](#page-9-5), many statistical word aligners have been proposed [\(Vogel et al.,](#page-12-11) [1996;](#page-12-11) [Ostling and Tiede-](#page-11-15) ¨ [mann,](#page-11-15) [2016\)](#page-11-15), including the current most popular tools GIZA++ [\(Och and Ney,](#page-11-10) [2000,](#page-11-10) [2003;](#page-11-5) [Gao and](#page-9-14) [Vogel,](#page-9-14) [2008\)](#page-9-14) and fast align [\(Dyer et al.,](#page-9-6) [2013\)](#page-9-6).

Recently, there is a resurgence of interest in neural word alignment [\(Tamura et al.,](#page-11-12) [2014;](#page-11-12) [Alkhouli](#page-9-16) [et al.,](#page-9-16) [2018\)](#page-9-16). Based on NMT models trained on parallel corpora, researchers have proposed several methods to extract alignments from them [\(Lu](#page-10-4)[ong et al.,](#page-10-4) [2015;](#page-10-4) [Zenkel et al.,](#page-12-7) [2019;](#page-12-7) [Garg et al.,](#page-9-7) [2019;](#page-9-7) [Li et al.,](#page-10-21) [2019\)](#page-10-21) and successfully build an end-to-end neural model that can outperform statistical tools [\(Zenkel et al.,](#page-12-4) [2020\)](#page-12-4). However, there is an inherent discrepancy between translation and word alignment: translation models are directional and the source and target side are treated differently, while word alignment is a non-directional task. Therefore, certain adaptations are required for translation models to perform word alignment.

Another disadvantage of MT-based word aligners is that they cannot easily utilize contextualized embeddings. Using learned representations to improve word alignment have been investigated [\(Sa](#page-11-16)[bet et al.,](#page-11-16) [2016;](#page-11-16) [Pourdamghani et al.,](#page-11-17) [2018\)](#page-11-17). Recently, pre-trained LMs [\(Peters et al.,](#page-11-18) [2018;](#page-11-18) [Devlin](#page-9-8) [et al.,](#page-9-8) [2019;](#page-9-8) [Brown et al.,](#page-9-17) [2020\)](#page-9-17) have proven to be useful in cross-lingual transfer [\(Libovicky et al.](#page-10-6) ` , [2019;](#page-10-6) [Hu et al.,](#page-10-7) [2020b\)](#page-10-7). In word alignment, [Sabet](#page-11-6) [et al.](#page-11-6) [\(2020\)](#page-11-6) propose effective methods to extract alignments from multilingual LMs without explicit training on parallel data. In this work, we propose better alignment extraction methods and combine the best of the two worlds by fine-tuning contextualized embeddings on parallel data.

There are also work on supervised neural word alignment [\(Stengel-Eskin et al.,](#page-11-19) [2019;](#page-11-19) [Nagata et al.,](#page-10-22) [2020\)](#page-10-22). However, supervised data are not always accessible, making their methods inapplicable in many scenarios. In this paper, we demonstrate that our model can incorporate supervised signals if available and perform semi-supervised learning, which is a more realistic and general setting.

Some work on bilingual lexicon induction also share similar general ideas with ours. For example, [Zhang et al.](#page-12-12) [\(2017\)](#page-12-12) minimize the earth mover's distance to match the embedding distributions from different languages. Similarly, [Grave et al.](#page-9-18) [\(2019\)](#page-9-18) present an algorithm to align point clouds with Procrustes [\(Schonemann](#page-11-20) ¨ , [1966\)](#page-11-20) in Wasserstein distance for unsupervised embedding alignment.

## 5 Discussion and Conclusion

We present a neural word aligner that achieves stateof-the-art performance on five diverse language pairs and obtains robust performance in zero-shot settings. We propose to fine-tune multilingual embeddings with objectives suitable for word alignment and develop two alignment extraction methods. We also demonstrate its applications in semisupervised settings. We hope our word aligner can be a tool that can be used out-of-the-box with good performance over various language pairs. Future directions include designing better training objectives and experimenting on more language pairs.

Also, note that we mainly evaluate our word aligners using AER following previous work, which has certain limitations. For example, it may not be well-correlated with statistical machine translation performance [Fraser and Marcu](#page-9-19) [\(2007\)](#page-9-19) and different types of alignments can be suitable for different tasks or conditions [\(Lambert et al.,](#page-10-23) [2012;](#page-10-23) [Stymne et al.,](#page-11-21) [2014\)](#page-11-21). Although we have evaluated models in annotation projection and cross-lingual transfer settings, alternative metrics [\(Tiedemann,](#page-12-13) [2005;](#page-12-13) [Søgaard and Wu,](#page-11-22) [2009;](#page-11-22) [Ahrenberg,](#page-9-20) [2010\)](#page-9-20) are also worth considering in the future.

## Acknowledgement

We thank our reviewers for helpful suggestions.

# References

- <span id="page-9-2"></span>Zeljko Agi ˇ c, Anders Johannsen, Barbara Plank, ´ Hector Mart ´ ´ınez Alonso, Natalie Schluter, and Anders Søgaard. 2016. [Multilingual projection for pars](https://www.mitpressjournals.org/doi/pdf/10.1162/tacl_a_00100)[ing truly low-resource languages.](https://www.mitpressjournals.org/doi/pdf/10.1162/tacl_a_00100) *Transactions of the Association for Computational Linguistics*.
- <span id="page-9-20"></span>Lars Ahrenberg. 2010. [Alignment-based profiling of](https://www.diva-portal.org/smash/get/diva2:354794/FULLTEXT01.pdf) [europarl data in an english-swedish parallel corpus.](https://www.diva-portal.org/smash/get/diva2:354794/FULLTEXT01.pdf) In *Proceedings of the International Conference on Language Resources and Evaluation*.
- <span id="page-9-16"></span>Tamer Alkhouli, Gabriel Bretschner, and Hermann Ney. 2018. [On the alignment problem in multi-head](https://www.aclweb.org/anthology/W18-6318.pdf) [attention-based neural machine translation.](https://www.aclweb.org/anthology/W18-6318.pdf) In *Proceedings of the Conference on Machine Translation*.
- <span id="page-9-0"></span>Waleed Ammar, George Mulcaire, Yulia Tsvetkov, Guillaume Lample, Chris Dyer, and Noah A Smith. 2016. [Massively multilingual word embeddings.](https://arxiv.org/pdf/1602.01925) *arXiv preprint*.
- <span id="page-9-3"></span>Philip Arthur, Graham Neubig, and Satoshi Nakamura. 2016. [Incorporating discrete translation lexicons](https://www.aclweb.org/anthology/D16-1162.pdf) [into neural machine translation.](https://www.aclweb.org/anthology/D16-1162.pdf) In *Proceedings of the Conference on Empirical Methods in Natural Language Processing*.
- <span id="page-9-10"></span>Dzmitry Bahdanau, Kyunghyun Cho, and Yoshua Bengio. 2015. [Neural machine translation by jointly](https://arxiv.org/pdf/1409.0473) [learning to align and translate.](https://arxiv.org/pdf/1409.0473) In *Proceedings of the International Conference on Learning Rrepresentations*.
- <span id="page-9-4"></span>Anthony Bau, Yonatan Belinkov, Hassan Sajjad, Nadir Durrani, Fahim Dalvi, and James Glass. 2018. [Iden](https://arxiv.org/pdf/1811.01157)[tifying and controlling important neurons in neural](https://arxiv.org/pdf/1811.01157) [machine translation.](https://arxiv.org/pdf/1811.01157) In *Proceedings of the International Conference on Learning Representations*.
- <span id="page-9-5"></span>Peter F Brown, Stephen A Della Pietra, Vincent J Della Pietra, and Robert L Mercer. 1993. [The math](https://www.aclweb.org/anthology/J93-2003.pdf)[ematics of statistical machine translation: Parameter](https://www.aclweb.org/anthology/J93-2003.pdf) [estimation.](https://www.aclweb.org/anthology/J93-2003.pdf) *Computational linguistics*.
- <span id="page-9-17"></span>Tom B. Brown, Benjamin Pickman Mann, Nick Ryder, Melanie Subbiah, Jean Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, G. Kruger, Tom Henighan, Rewon Child, ¨ Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric J Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam Mc-Candlish, Alec Radford, Ilya Sutskever, and Dario Amodei. 2020. [Language models are few-shot learn](https://arxiv.org/pdf/2005.14165)[ers.](https://arxiv.org/pdf/2005.14165) *arXiv preprint*.
- <span id="page-9-1"></span>Steven Cao, Nikita Kitaev, and Dan Klein. 2019. [Mul](https://arxiv.org/pdf/2002.03518)[tilingual alignment of contextual word representa](https://arxiv.org/pdf/2002.03518)[tions.](https://arxiv.org/pdf/2002.03518) In *Proceedings of the International Conference on Learning Representations*.
- <span id="page-9-13"></span>Yun Chen, Yang Liu, Guanhua Chen, Xin Jiang, and Qun Liu. 2020. [Accurate word alignment induction](https://arxiv.org/pdf/2004.14837)

- [from neural machine translation.](https://arxiv.org/pdf/2004.14837) In *Proceedings of the Conference on Empirical Methods in Natural Language Processing*.
- <span id="page-9-12"></span>Trevor Cohn, Cong Duy Vu Hoang, Ekaterina Vymolova, Kaisheng Yao, Chris Dyer, and Gholamreza Haffari. 2016. [Incorporating structural alignment bi](https://www.aclweb.org/anthology/N16-1102.pdf)[ases into an attentional neural translation model.](https://www.aclweb.org/anthology/N16-1102.pdf) In *Proceedings of the Conference of the North American Chapter of the Association for Computational Linguistics*.
- <span id="page-9-9"></span>Alexis Conneau, Kartikay Khandelwal, Naman Goyal, Vishrav Chaudhary, Guillaume Wenzek, Francisco Guzman, Edouard Grave, Myle Ott, Luke Zettle- ´ moyer, and Veselin Stoyanov. 2020. [Unsupervised](https://arxiv.org/pdf/1911.02116) [cross-lingual representation learning at scale.](https://arxiv.org/pdf/1911.02116) In *Proceedings of the Annual Meeting of the Association for Computational Linguistics*.
- <span id="page-9-15"></span>Alexis Conneau, Ruty Rinott, Guillaume Lample, Adina Williams, Samuel Bowman, Holger Schwenk, and Veselin Stoyanov. 2018. [Xnli: Evaluating cross](https://arxiv.org/pdf/1809.05053)[lingual sentence representations.](https://arxiv.org/pdf/1809.05053) In *Proceedings of the Conference on Empirical Methods in Natural Language Processing*.
- <span id="page-9-11"></span>Marco Cuturi. 2013. [Sinkhorn distances: Lightspeed](https://papers.nips.cc/paper/4927-sinkhorn-distances-lightspeed-computation-of-optimal-transport.pdf) [computation of optimal transport.](https://papers.nips.cc/paper/4927-sinkhorn-distances-lightspeed-computation-of-optimal-transport.pdf) *Proceedings of the Advances in Neural Information Processing Systems*.
- <span id="page-9-8"></span>Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2019. [BERT: Pre-training of](https://arxiv.org/pdf/1810.04805.pdf) [deep bidirectional transformers for language under](https://arxiv.org/pdf/1810.04805.pdf)[standing.](https://arxiv.org/pdf/1810.04805.pdf) In *Proceedings of the Conference of the North American Chapter of the Association for Computational Linguistics*.
- <span id="page-9-6"></span>Chris Dyer, Victor Chahuneau, and Noah A Smith. 2013. [A simple, fast, and effective reparameteriza](https://www.aclweb.org/anthology/N13-1073.pdf)[tion of IBM model 2.](https://www.aclweb.org/anthology/N13-1073.pdf) In *Proceedings of the Conference of the North American Chapter of the Association for Computational Linguistics*.
- <span id="page-9-19"></span>Alexander Fraser and Daniel Marcu. 2007. [Measuring](https://www.mitpressjournals.org/doi/pdfplus/10.1162/coli.2007.33.3.293) [word alignment quality for statistical machine trans](https://www.mitpressjournals.org/doi/pdfplus/10.1162/coli.2007.33.3.293)[lation.](https://www.mitpressjournals.org/doi/pdfplus/10.1162/coli.2007.33.3.293) *Computational Linguistics*.
- <span id="page-9-14"></span>Qin Gao and Stephan Vogel. 2008. [Parallel implemen](https://www.aclweb.org/anthology/W08-0509.pdf)[tations of word alignment tool.](https://www.aclweb.org/anthology/W08-0509.pdf) In *Software Engineering, Testing, and Quality Assurance for Natural Language Processing*.
- <span id="page-9-7"></span>Sarthak Garg, Stephan Peitz, Udhyakumar Nallasamy, and Matthias Paulik. 2019. [Jointly learning to align](https://www.aclweb.org/anthology/D19-1453.pdf) [and translate with transformer models.](https://www.aclweb.org/anthology/D19-1453.pdf) In *Proceedings of the Conference on Empirical Methods in Natural Language Processing*.
- <span id="page-9-18"></span>Edouard Grave, Armand Joulin, and Quentin Berthet. 2019. [Unsupervised alignment of embeddings with](http://proceedings.mlr.press/v89/grave19a/grave19a.pdf) [wasserstein procrustes.](http://proceedings.mlr.press/v89/grave19a/grave19a.pdf) In *Proceedinds of the International Conference on Artificial Intelligence and Statistics*.

- <span id="page-10-13"></span>Suchin Gururangan, Ana Marasovic, Swabha ´ Swayamdipta, Kyle Lo, Iz Beltagy, Doug Downey, and Noah A. Smith. 2020. [Don't stop pretraining:](https://www.aclweb.org/anthology/2020.acl-main.740) [Adapt language models to domains and tasks.](https://www.aclweb.org/anthology/2020.acl-main.740) In *Proceedings of the Annual Meeting of the Association for Computational Linguistics*.
- <span id="page-10-1"></span>Jonathan Herzig and Jonathan Berant. 2018. [Decou](https://www.aclweb.org/anthology/D18-1190.pdf)[pling structure and lexicon for zero-shot semantic](https://www.aclweb.org/anthology/D18-1190.pdf) [parsing.](https://www.aclweb.org/anthology/D18-1190.pdf) In *Proceedings of the Conference on Empirical Methods in Natural Language Processing*.
- <span id="page-10-17"></span>Junjie Hu, Melvin Johnson, Orhan Firat, Aditya Siddhant, and Graham Neubig. 2020a. [Explicit align](https://arxiv.org/pdf/2010.07972.pdf)[ment objectives for multilingual bidirectional en](https://arxiv.org/pdf/2010.07972.pdf)[coders.](https://arxiv.org/pdf/2010.07972.pdf) *arXiv preprint*.
- <span id="page-10-7"></span>Junjie Hu, Sebastian Ruder, Aditya Siddhant, Graham Neubig, Orhan Firat, and Melvin Johnson. 2020b. [XTREME: A massively multilingual multi](https://arxiv.org/pdf/2003.11080.pdf)[task benchmark for evaluating cross-lingual general](https://arxiv.org/pdf/2003.11080.pdf)[isation.](https://arxiv.org/pdf/2003.11080.pdf) In *Proceedings of the International Conference on Machine Learning*.
- <span id="page-10-3"></span>Junjie Hu, Mengzhou Xia, Graham Neubig, and Jaime G Carbonell. 2019. [Domain adaptation of](https://www.aclweb.org/anthology/P19-1286.pdf) [neural machine translation by lexicon induction.](https://www.aclweb.org/anthology/P19-1286.pdf) In *Proceedings of the Annual Meeting of the Association for Computational Linguistics*.
- <span id="page-10-19"></span>Philipp Koehn. 2005. [Europarl: A parallel corpus for](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.459.5497&rep=rep1&type=pdf) [statistical machine translation.](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.459.5497&rep=rep1&type=pdf) In *MT summit*.
- <span id="page-10-11"></span>Philipp Koehn, Amittai Axelrod, Alexandra Birch Mayne, Chris Callison-Burch, Miles Osborne, and David Talbot. 2005. [Edinburgh system description](https://www.researchgate.net/profile/Philipp_Koehn/publication/228355130_Edinburgh_system_description_for_the_2005_IWSLT_speech_translation_evaluation/links/09e4150db363f27728000000.pdf) [for the 2005 iwslt speech translation evaluation.](https://www.researchgate.net/profile/Philipp_Koehn/publication/228355130_Edinburgh_system_description_for_the_2005_IWSLT_speech_translation_evaluation/links/09e4150db363f27728000000.pdf) In *Proceedings of the International Workshop on Spoken Language Translation*.
- <span id="page-10-12"></span>Taku Kudo and John Richardson. 2018. [Sentence](https://www.aclweb.org/anthology/D18-2012.pdf)[piece: A simple and language independent subword](https://www.aclweb.org/anthology/D18-2012.pdf) [tokenizer and detokenizer for neural text process](https://www.aclweb.org/anthology/D18-2012.pdf)[ing.](https://www.aclweb.org/anthology/D18-2012.pdf) In *Proceedings of the Conference on Empirical Methods in Natural Language Processing: System Demonstrations*.
- <span id="page-10-10"></span>Matt Kusner, Yu Sun, Nicholas Kolkin, and Kilian Weinberger. 2015. [From word embeddings to docu](http://www.jmlr.org/proceedings/papers/v37/kusnerb15.pdf)[ment distances.](http://www.jmlr.org/proceedings/papers/v37/kusnerb15.pdf) In *Proceedings of the International Conference on Machine Learning*.
- <span id="page-10-23"></span>Patrik Lambert, Simon Petitrenaud, Yanjun Ma, and Andy Way. 2012. [What types of word alignment](https://link.springer.com/content/pdf/10.1007/s10590-012-9123-3.pdf) [improve statistical machine translation?](https://link.springer.com/content/pdf/10.1007/s10590-012-9123-3.pdf) *Machine Translation*.
- <span id="page-10-5"></span>Guillaume Lample and Alexis Conneau. 2019. [Cross](https://arxiv.org/pdf/1901.07291)[lingual language model pretraining.](https://arxiv.org/pdf/1901.07291) In *Proceedings of the Advances in Neural Information Processing Systems*.
- <span id="page-10-16"></span>Joel Legrand, Michael Auli, and Ronan Collobert. ¨ 2016. [Neural network-based word alignment](https://arxiv.org/pdf/1606.09560) [through score aggregation.](https://arxiv.org/pdf/1606.09560) In *Proceedings of the Conference on Machine Translation*.

- <span id="page-10-21"></span>Xintong Li, Guanlin Li, Lemao Liu, Max Meng, and Shuming Shi. 2019. [On the word alignment from](https://www.aclweb.org/anthology/P19-1124.pdf) [neural machine translation.](https://www.aclweb.org/anthology/P19-1124.pdf) In *Proceedings of the Annual Meeting of the Association for Computational Linguistics*.
- <span id="page-10-14"></span>Percy Liang, Ben Taskar, and Dan Klein. 2006. [Align](https://www.aclweb.org/anthology/N06-1014)[ment by agreement.](https://www.aclweb.org/anthology/N06-1014) In *Proceedings of the Conference of the North American Chapter of the Association for Computational Linguistics*.
- <span id="page-10-6"></span>Jindˇrich Libovicky, Rudolf Rosa, and Alexander Fraser. ` 2019. [How language-neutral is multilingual BERT?](https://arxiv.org/pdf/1911.03310) *arXiv preprint*.
- <span id="page-10-2"></span>Lemao Liu, Masao Utiyama, Andrew Finch, and Eiichiro Sumita. 2016. [Neural machine translation](https://arxiv.org/pdf/1609.04186) [with supervised attention.](https://arxiv.org/pdf/1609.04186) In *Proceedings of the International Conference on Computational Linguistics*.
- <span id="page-10-15"></span>Yang Liu and Maosong Sun. 2015. [Contrastive unsu](https://arxiv.org/pdf/1410.2082)[pervised word alignment with non-local features.](https://arxiv.org/pdf/1410.2082) In *Proceedings of the AAAI Conference on Artificial Intelligence*.
- <span id="page-10-8"></span>Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke Zettlemoyer, and Veselin Stoyanov. 2019. [RoBERTa: A robustly optimized BERT pretraining](https://arxiv.org/pdf/1907.11692) [approach.](https://arxiv.org/pdf/1907.11692) *arXiv preprint*.
- <span id="page-10-20"></span>I. Loshchilov and F. Hutter. 2019. [Decoupled weight](https://arxiv.org/pdf/1711.05101.pdf]) [decay regularization.](https://arxiv.org/pdf/1711.05101.pdf]) In *Proceedings of the International Conference on Learning Representations*.
- <span id="page-10-4"></span>Minh-Thang Luong, Hieu Pham, and Christopher D Manning. 2015. [Effective approaches to attention](https://arxiv.org/pdf/1508.04025)[based neural machine translation.](https://arxiv.org/pdf/1508.04025) In *Proceedings of the Conference on Empirical Methods in Natural Language Processing*.
- <span id="page-10-24"></span>Bill MacCartney, Michel Galley, and Christopher D Manning. 2008. [A phrase-based alignment model](https://www.aclweb.org/anthology/D08-1084.pdf) [for natural language inference.](https://www.aclweb.org/anthology/D08-1084.pdf) In *Proceedings of the Conference on Empirical Methods in Natural Language Processing*.
- <span id="page-10-0"></span>Stephen Mayhew, Chen-Tse Tsai, and Dan Roth. 2017. [Cheap translation for cross-lingual named entity](https://www.aclweb.org/anthology/D17-1269.pdf) [recognition.](https://www.aclweb.org/anthology/D17-1269.pdf) In *Proceedings of the Conference on Empirical Methods in Natural Language Processing*.
- <span id="page-10-18"></span>Rada Mihalcea and Ted Pedersen. 2003. [An evalua](https://www.aclweb.org/anthology/W03-0301.pdf)[tion exercise for word alignment.](https://www.aclweb.org/anthology/W03-0301.pdf) In *Proceedings of Workshop on Building and Using Parallel Texts*.
- <span id="page-10-9"></span>Gaspard Monge. 1781. Memoire sur la th ´ eorie des ´ deblais et des remblais. ´ *Histoire de l'Academie ´ Royale des Sciences de Paris*.
- <span id="page-10-22"></span>Masaaki Nagata, Chousa Katsuki, and Masaaki Nishino. 2020. [A supervised word alignment](https://arxiv.org/pdf/2004.14516)

- [method based on cross-language span prediction us](https://arxiv.org/pdf/2004.14516)[ing multilingual BERT.](https://arxiv.org/pdf/2004.14516) In *Proceedings of the Conference on Empirical Methods in Natural Language Processing*.
- <span id="page-11-13"></span>Graham Neubig. 2011. [The Kyoto free translation task.](http://www.phontron.com/kftt) http://www.phontron.com/kftt.
- <span id="page-11-4"></span>Graham Neubig, Zi-Yi Dou, Junjie Hu, Paul Michel, Danish Pruthi, and Xinyi Wang. 2019. [compare-mt:](https://arxiv.org/pdf/1903.07926) [A tool for holistic comparison of language genera](https://arxiv.org/pdf/1903.07926)[tion systems.](https://arxiv.org/pdf/1903.07926) In *Proceedings of the Conference of the North American Chapter of the Association for Computational Linguistics: System Demonstrations*.
- <span id="page-11-14"></span>Graham Neubig, Yosuke Nakata, and Shinsuke Mori. 2011. [Pointwise prediction for robust, adaptable](https://www.aclweb.org/anthology/P11-2093.pdf) [japanese morphological analysis.](https://www.aclweb.org/anthology/P11-2093.pdf) In *Proceedings of the Annual Meeting of the Association for Computational Linguistics*.
- <span id="page-11-1"></span>Garrett Nicolai and David Yarowsky. 2019. [Learning](https://www.aclweb.org/anthology/P19-1172) [morphosyntactic analyzers from the Bible via itera](https://www.aclweb.org/anthology/P19-1172)[tive annotation projection across 26 languages.](https://www.aclweb.org/anthology/P19-1172) In *Proceedings of the Annual Meeting of the Association for Computational Linguistics*.
- <span id="page-11-10"></span>Franz Josef Och and Hermann Ney. 2000. [Improved](https://www.aclweb.org/anthology/P00-1056.pdf) [statistical alignment models.](https://www.aclweb.org/anthology/P00-1056.pdf) In *Proceedings of the Annual Meeting of the Association for Computational Linguistics*.
- <span id="page-11-5"></span>Franz Josef Och and Hermann Ney. 2003. [A systematic](https://www.mitpressjournals.org/doi/pdfplus/10.1162/089120103321337421) [comparison of various statistical alignment models.](https://www.mitpressjournals.org/doi/pdfplus/10.1162/089120103321337421) *Computational Linguistics*.
- <span id="page-11-15"></span>Robert Ostling and J ¨ org Tiedemann. 2016. ¨ [Efficient](https://content.sciendo.com/downloadpdf/journals/pralin/106/1/article-p125.xml) [word alignment with Markov Chain Monte Carlo.](https://content.sciendo.com/downloadpdf/journals/pralin/106/1/article-p125.xml) *The Prague Bulletin of Mathematical Linguistics*.
- <span id="page-11-0"></span>Sebastian Pado and Mirella Lapata. 2009. ´ [Cross](https://www.jair.org/index.php/jair/article/download/10629/25416)[lingual annotation projection for semantic roles.](https://www.jair.org/index.php/jair/article/download/10629/25416) *Journal of Artificial Intelligence Research*.
- <span id="page-11-7"></span>Ben Peters, Vlad Niculae, and Andre FT Martins. 2019. ´ [Sparse sequence-to-sequence models.](https://arxiv.org/pdf/1905.05702) In *Proceedings of the Annual Meeting of the Association for Computational Linguistics*.
- <span id="page-11-18"></span>Matthew Peters, Mark Neumann, Mohit Iyyer, Matt Gardner, Christopher Clark, Kenton Lee, and Luke Zettlemoyer. 2018. [Deep contextualized word rep](https://arxiv.org/pdf/1802.05365.pdf)[resentations.](https://arxiv.org/pdf/1802.05365.pdf) In *Proceedings of the Conference of the North American Chapter of the Association for Computational Linguistics*.
- <span id="page-11-17"></span>Nima Pourdamghani, Marjan Ghazvininejad, and Kevin Knight. 2018. [Using word vectors to improve](https://www.aclweb.org/anthology/N18-2083.pdf) [word alignments for low resource machine transla](https://www.aclweb.org/anthology/N18-2083.pdf)[tion.](https://www.aclweb.org/anthology/N18-2083.pdf) In *Proceedings of the Conference of the North American Chapter of the Association for Computational Linguistics*.
- <span id="page-11-2"></span>Shuo Ren, Yu Wu, Shujie Liu, Ming Zhou, and Shuai Ma. 2020. [A retrieve-and-rewrite initializa](https://www.aclweb.org/anthology/2020.acl-main.320.pdf)[tion method for unsupervised machine translation.](https://www.aclweb.org/anthology/2020.acl-main.320.pdf)

- In *Proceedings of the Annual Meeting of the Association for Computational Linguistics*.
- <span id="page-11-6"></span>Masoud Jalili Sabet, Philipp Dufter, Franc¸ois Yvon, and Hinrich Schutze. 2020. ¨ [Simalign: High qual](https://arxiv.org/pdf/2004.08728)[ity word alignments without parallel training data](https://arxiv.org/pdf/2004.08728) [using static and contextualized embeddings.](https://arxiv.org/pdf/2004.08728) In *Proceedings of the Conference on Empirical Methods in Natural Language Processing: Findings*.
- <span id="page-11-16"></span>Masoud Jalili Sabet, Heshaam Faili, and Gholamreza Haffari. 2016. [Improving word alignment of rare](https://www.aclweb.org/anthology/C16-1302.pdf) [words with word embeddings.](https://www.aclweb.org/anthology/C16-1302.pdf) In *Proceedings of the International Conference on Computational Linguistics*.
- <span id="page-11-20"></span>Peter H Schonemann. 1966. ¨ [A generalized solution of](http://nemo.nic.uoregon.edu/wiki/images/0/07/Psychometrika_1966_Sch%C3%B6nemann_A_generalized_solution_of_the.pdf) [the orthogonal procrustes problem.](http://nemo.nic.uoregon.edu/wiki/images/0/07/Psychometrika_1966_Sch%C3%B6nemann_A_generalized_solution_of_the.pdf) *Psychometrika*.
- <span id="page-11-11"></span>Rico Sennrich, Barry Haddow, and Alexandra Birch. 2016. [Neural machine translation of rare words with](https://www.aclweb.org/anthology/P16-1162.pdf) [subword units.](https://www.aclweb.org/anthology/P16-1162.pdf) In *Proceedings of the Annual Meeting of the Association for Computational Linguistics*.
- <span id="page-11-9"></span>Richard Sinkhorn and Paul Knopp. 1967. [Concerning](https://msp.org/pjm/1967/21-2/pjm-v21-n2-p14-p.pdf) [nonnegative matrices and doubly stochastic matrices.](https://msp.org/pjm/1967/21-2/pjm-v21-n2-p14-p.pdf) *Pacific Journal of Mathematics*.
- <span id="page-11-22"></span>Anders Søgaard and Dekai Wu. 2009. [Empirical lower](https://www.aclweb.org/anthology/W09-3805.pdf) [bounds on translation unit error rate for the full class](https://www.aclweb.org/anthology/W09-3805.pdf) [of inversion transduction grammars.](https://www.aclweb.org/anthology/W09-3805.pdf) In *Proceedings of the International Conference on Parsing Technologies*.
- <span id="page-11-3"></span>Gabriel Stanovsky, Noah A Smith, and Luke Zettlemoyer. 2019. [Evaluating gender bias in machine](https://arxiv.org/pdf/1906.00591) [translation.](https://arxiv.org/pdf/1906.00591) In *Proceedings of the Annual Meeting of the Association for Computational Linguistics*.
- <span id="page-11-19"></span>Elias Stengel-Eskin, Tzu-ray Su, Matt Post, and Benjamin Van Durme. 2019. [A discriminative neural](https://arxiv.org/pdf/1909.00444) [model for cross-lingual word alignment.](https://arxiv.org/pdf/1909.00444) In *Proceedings of the Conference on Empirical Methods in Natural Language Processing*.
- <span id="page-11-21"></span>Sara Stymne, Jorg Tiedemann, and Joakim Nivre. 2014. ¨ [Estimating word alignment quality for smt reorder](https://www.aclweb.org/anthology/W14-3334.pdf)[ing tasks.](https://www.aclweb.org/anthology/W14-3334.pdf) In *Proceedings of the Workshop on Statistical Machine Translation*.
- <span id="page-11-23"></span>Md Arafat Sultan, Steven Bethard, and Tamara Sumner. 2014. [Back to basics for monolingual alignment:](https://www.mitpressjournals.org/doi/pdf/10.1162/tacl_a_00178) [Exploiting word similarity and contextual evidence.](https://www.mitpressjournals.org/doi/pdf/10.1162/tacl_a_00178) *Transactions of the Association for Computational Linguistics*.
- <span id="page-11-8"></span>Kyle Swanson, Lili Yu, and Tao Lei. 2020. [Rationaliz](https://arxiv.org/pdf/2005.13111)[ing text matching: Learning sparse alignments via](https://arxiv.org/pdf/2005.13111) [optimal transport.](https://arxiv.org/pdf/2005.13111) In *Proceedings of the Annual Meeting of the Association for Computational Linguistics*.
- <span id="page-11-12"></span>Akihiro Tamura, Taro Watanabe, and Eiichiro Sumita. 2014. [Recurrent neural networks for word align](https://www.aclweb.org/anthology/P14-1138.pdf)[ment model.](https://www.aclweb.org/anthology/P14-1138.pdf) In *Proceedings of the Annual Meeting of the Association for Computational Linguistics*.

- <span id="page-12-13"></span>Jorg Tiedemann. 2005. ¨ [Optimization of word align](http://search.proquest.com/openview/ca1a4751da507ff53b1f69f12a6c4141/1?pq-origsite=gscholar&cbl=30339)[ment clues.](http://search.proquest.com/openview/ca1a4751da507ff53b1f69f12a6c4141/1?pq-origsite=gscholar&cbl=30339) *Natural Language Engineering*.
- <span id="page-12-1"></span>Jorg Tiedemann. 2014. ¨ [Rediscovering annotation pro](https://www.aclweb.org/anthology/C14-1175)[jection for cross-lingual parser induction.](https://www.aclweb.org/anthology/C14-1175) In *Proceedings of the International Conference on Computational Linguistics*.
- <span id="page-12-10"></span>Erik F. Tjong Kim Sang. 2002. [Introduction to the](https://www.aclweb.org/anthology/W02-2024) [CoNLL-2002 shared task: Language-independent](https://www.aclweb.org/anthology/W02-2024) [named entity recognition.](https://www.aclweb.org/anthology/W02-2024) In *Proceedings of the Conference on Natural Language Learning*.
- <span id="page-12-9"></span>Erik F. Tjong Kim Sang and Fien De Meulder. 2003. [Introduction to the CoNLL-2003 shared task:](https://www.aclweb.org/anthology/W03-0419) [Language-independent named entity recognition.](https://www.aclweb.org/anthology/W03-0419) In *Proceedings of the Conference on Natural Language Learning*.
- <span id="page-12-5"></span>Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. [Attention is all](https://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf) [you need.](https://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf) In *Proceedings of the Advances in Neural Information Processing Systems*.
- <span id="page-12-8"></span>David Vilar, Maja Popovic, and Hermann Ney. 2006. ´ [AER: Do we need to "improve" our alignments?](https://188.166.204.102/archive/iwslt_06/papers/slt6_205.pdf) In *Proceedings of the International Workshop on Spoken Language Translation*.
- <span id="page-12-11"></span>Stephan Vogel, Hermann Ney, and Christoph Tillmann. 1996. [Hmm-based word alignment in statistical](https://www.aclweb.org/anthology/C96-2141.pdf) [translation.](https://www.aclweb.org/anthology/C96-2141.pdf) In *Proceedings of the International Conference on Computational Linguistics*.
- <span id="page-12-3"></span>Shuo Wang, Zhaopeng Tu, Shuming Shi, and Yang Liu. 2020. [On the inference calibration of neural](https://www.aclweb.org/anthology/2020.acl-main.278) [machine translation.](https://www.aclweb.org/anthology/2020.acl-main.278) In *Proceedings of the Annual Meeting of the Association for Computational Linguistics*.
- <span id="page-12-2"></span>Hainan Xu, Shuoyang Ding, and Shinji Watanabe. 2019. [Improving end-to-end speech recognition](https://ieeexplore.ieee.org/iel7/8671773/8682151/08682494.pdf?casa_token=7TJtKTTLkRUAAAAA:OJ_CGqQgaeAFqJW34bYLTyrgCGjRV77PCmUxYMZWGnYbaK-AEyc9gKMKu3OQDz--_s3h0bio) [with pronunciation-assisted sub-word modeling.](https://ieeexplore.ieee.org/iel7/8671773/8682151/08682494.pdf?casa_token=7TJtKTTLkRUAAAAA:OJ_CGqQgaeAFqJW34bYLTyrgCGjRV77PCmUxYMZWGnYbaK-AEyc9gKMKu3OQDz--_s3h0bio) In *Proceedings of the IEEE International Conference on Acoustics, Speech and Signal Processing*.
- <span id="page-12-14"></span>Xuchen Yao, Benjamin Van Durme, Chris Callison-Burch, and Peter Clark. 2013a. [A lightweight and](https://www.aclweb.org/anthology/P13-2123.pdf) [high performance monolingual word aligner.](https://www.aclweb.org/anthology/P13-2123.pdf) In *Proceedings of the Annual Meeting of the Association for Computational Linguistics*.
- <span id="page-12-15"></span>Xuchen Yao, Benjamin Van Durme, Chris Callison-Burch, and Peter Clark. 2013b. [Semi-Markov](https://www.aclweb.org/anthology/D13-1056.pdf) [phrase-based monolingual alignment.](https://www.aclweb.org/anthology/D13-1056.pdf) In *Proceedings of the Conference on Empirical Methods in Natural Language Processing*.
- <span id="page-12-0"></span>David Yarowsky, Grace Ngai, and Richard Wicentowski. 2001. [Inducing multilingual text analysis](https://apps.dtic.mil/sti/pdfs/ADA460922.pdf) [tools via robust projection across aligned corpora.](https://apps.dtic.mil/sti/pdfs/ADA460922.pdf) In *Proceedings of the International Conference on Human Language Technology Research*.

- <span id="page-12-7"></span>Thomas Zenkel, Joern Wuebker, and John DeNero. 2019. [Adding interpretable attention to neural trans](https://arxiv.org/pdf/1901.11359)[lation models improves word alignment.](https://arxiv.org/pdf/1901.11359) *arXiv preprint*.
- <span id="page-12-4"></span>Thomas Zenkel, Joern Wuebker, and John DeNero. 2020. [End-to-end neural word alignment outper](https://www.aclweb.org/anthology/2020.acl-main.146)[forms GIZA++.](https://www.aclweb.org/anthology/2020.acl-main.146) In *Proceedings of the Annual Meeting of the Association for Computational Linguistics*.
- <span id="page-12-12"></span>Meng Zhang, Yang Liu, Huanbo Luan, and Maosong Sun. 2017. [Earth mover's distance minimization for](https://www.aclweb.org/anthology/D17-1207.pdf) [unsupervised bilingual lexicon induction.](https://www.aclweb.org/anthology/D17-1207.pdf) In *Proceedings of the Conference on Empirical Methods in Natural Language Processing*.
- <span id="page-12-6"></span>Zhirui Zhang, Shuangzhi Wu, Shujie Liu, Mu Li, Ming Zhou, and Tong Xu. 2019. [Regularizing neural ma](https://www.aaai.org/ojs/index.php/AAAI/article/view/3816/3694)[chine translation by target-bidirectional agreement.](https://www.aaai.org/ojs/index.php/AAAI/article/view/3816/3694) In *Proceedings of the AAAI Conference on Artificial Intelligence*.

<span id="page-13-0"></span>

| Model                | Prec. % | Rec.% | <b>F</b> <sub>1</sub> % |
|----------------------|---------|-------|-------------------------|
| Baseline             |         |       |                         |
| Yao et al. (2013a)   | 91.3    | 82.0  | 86.4                    |
| Yao et al. (2013b)   | 90.4    | 81.9  | 85.9                    |
| Sultan et al. (2014) | 93.5    | 82.6  | 87.6                    |
| Ours                 |         |       |                         |
| mBERT                | 87.0    | 89.0  | 88.0                    |
| Ours-Multilingual    | 87.0    | 89.3  | 88.1                    |
| Ours-Supervised      | 87.2    | 89.8  | 88.5                    |

Table 10: Our model is also effective in monolingual alignment settings.

## **A** Implementation Details

We use the AdamW optimizer (Loshchilov and Hutter, 2019) with a learning rate of 2e-5 and the batch size is set to 8. Following Peters et al. (2019), we set  $\alpha$  to 1.5 for  $\alpha$ -entmax. The threshold c is set to 0 for  $\alpha$ -entmax and 0.001 for *softmax* and optimal transport. We train our models on one 2080 Ti for one epoch and it takes 3 to 24 hours for the model to converge depending on the size of the dataset. We evaluate the model performance using Alignment Error Rate (AER).

## **B** Analysis

In this section, we conduct more analyses of our models.

**Monolingual Alignment.** We also investigate how our models perform in monolingual alignment settings. Previous methods (MacCartney et al., 2008; Yao et al., 2013a,b; Sultan et al., 2014) typically exploit external resources such as WordNet to tackle the problem. As shown in Table 10, mBERT can outperform previous methods in terms of recall and  $F_1$  without any fine-tuning. Our multilingually fine-tuned model can achieve better recall and slightly better  $F_1$  score than the vanilla mBERT model, and fine-tuning our model with supervised signals can achieve further improvements.

**Sensitivity Analysis.** We also conduct a sensitivity analysis on the threshold c for our *softmax* alignment extraction method. As shown in Table 11, our method is relatively robust to this threshold. In particular, after fine-tuning, the AERs change within 0.5% when varying the threshold.

Comparisons with IterMax. IterMax is the best alignment extraction method in SimAlign (Sabet et al., 2020). The results in the main paper have demonstrated that our alignment extraction methods are able to outperform IterMax. In Figure 4, we

<span id="page-13-1"></span>

| Model             | c.   | De-En | Fr-En | Ro-En | Ja-En | Zh-En |
|-------------------|------|-------|-------|-------|-------|-------|
|                   | 1e-6 | 17.3  | 6.0   | 27.2  | 45.2  | 18.9  |
|                   | 1e-5 | 17.3  | 5.9   | 27.4  | 45.1  | 18.6  |
|                   | 1e-4 | 17.3  | 5.7   | 27.6  | 45.3  | 18.3  |
| mBERT             | 1e-3 | 17.4  | 5.6   | 27.9  | 45.6  | 18.1  |
|                   | 1e-2 | 17.7  | 5.6   | 28.4  | 45.8  | 18.2  |
|                   | 1e-1 | 18.1  | 5.6   | 28.9  | 46.3  | 18.3  |
|                   | 5e-1 | 18.4  | 5.6   | 29.5  | 47.0  | 18.7  |
|                   | 1e-6 | 15.4  | 4.6   | 22.7  | 38.2  | 14.1  |
|                   | 1e-5 | 15.4  | 4.5   | 22.7  | 38.1  | 14.0  |
|                   | 1e-4 | 15.3  | 4.5   | 22.6  | 37.9  | 13.9  |
| Ours-Multilingual | 1e-3 | 15.3  | 4.4   | 22.6  | 37.9  | 13.8  |
|                   | 1e-2 | 15.3  | 4.3   | 22.7  | 37.9  | 13.8  |
|                   | 1e-1 | 15.4  | 4.3   | 22.8  | 38.0  | 13.8  |
|                   | 5e-1 | 15.4  | 4.2   | 23.0  | 38.2  | 13.9  |

Table 11: Our *softmax* alignment extraction method is relatively robust to the threshold c.

can see that the IterMax algorithm tends to sacrifice precision for a small improvements in recall, while our model can generate more accurate alignments.

Ablation Studies on Training Objectives. Table 12 presents more ablation studies on our training objectives. We can see that the self training objective is the most effective one, with the translation language modeling objective being the second and the parallel sentence identification objective being the third. The masked language modeling objective can sometimes hurt the model performance, possibly because of the translation language modeling objective.

**Experiments on More Language Pairs.** We also test our alignment extraction methods on other language pairs following the setting of Sabet et al. (2020) without fine-tuning as shown in Table 13.<sup>2</sup>

More Qualitative Examples. In addition to the examples provided in the main text, we also present some randomly sampled samples in Figure 5. We can clearly see that our model learns more aligned representations than the baseline model.

<span id="page-13-2"></span><sup>&</sup>lt;sup>2</sup>Their English-Persian dataset is unavailable at the time of writing the paper.

<span id="page-14-1"></span>

| Model             | Objective   | De-En | Fr-En | Ro-En | Ja-En | Zh-En |
|-------------------|-------------|-------|-------|-------|-------|-------|
| Ours-Bilingual    |             |       |       |       |       |       |
|                   | All         | 16.1  | 4.1   | 23.4  | 38.6  | 15.4  |
|                   | All w/o MLM | 15.6  | 4.2   | 23.3  | 38.8  | 15.1  |
|                   | All w/o TLM | 16.4  | 4.3   | 23.7  | 40.1  | 15.3  |
| α-entmax          | All w/o SO  | 17.8  | 4.7   | 23.9  | 39.4  | 16.3  |
|                   | All w/o PSI | 16.5  | 4.2   | 23.1  | 38.5  | 15.4  |
|                   | All         | 15.6  | 4.4   | 23.0  | 38.4  | 15.3  |
|                   | All w/o MLM | 15.5  | 4.2   | 23.2  | 38.9  | 14.9  |
|                   | All w/o TLM | 15.9  | 4.5   | 23.7  | 40.1  | 15.1  |
| softmax           | All w/o SO  | 17.4  | 4.7   | 23.2  | 38.6  | 16.3  |
|                   | All w/o PSI | 15.6  | 4.3   | 23.1  | 38.8  | 15.4  |
| Ours-Multilingual |             |       |       |       |       |       |
|                   | All         | 15.4  | 4.1   | 22.9  | 37.4  | 13.9  |
|                   | All w/o MLM | 15.1  | 4.2   | 22.8  | 37.8  | 13.7  |
| α-entmax          | All w/o TLM | 16.4  | 4.4   | 23.3  | 39.7  | 14.4  |
|                   | All w/o SO  | 17.5  | 4.6   | 23.6  | 40.0  | 15.6  |
|                   | All w/o PSI | 15.5  | 3.9   | 23.0  | 38.2  | 14.1  |
|                   | All         | 15.3  | 4.4   | 22.6  | 37.9  | 13.6  |
|                   | All w/o MLM | 15.3  | 4.4   | 22.8  | 38.6  | 13.7  |
| softmax           | All w/o TLM | 15.5  | 4.7   | 22.9  | 39.7  | 14.0  |
|                   | All w/o SO  | 16.9  | 4.8   | 23.0  | 39.1  | 15.4  |
|                   | All w/o PSI | 15.4  | 4.4   | 22.7  | 37.9  | 13.8  |

Table 12: Ablation studies on training objectives.

<span id="page-14-0"></span>

| Model                  | En-Cs | En-Hi |
|------------------------|-------|-------|
| GIZA++                 | 18.2  | 51.8  |
| SimAlign               | 13.4  | 40.2  |
| Ours (softmax, c=1e-3) | 12.3  | 41.2  |
| Ours (softmax, c=1e-5) | 12.7  | 39.5  |
| Ours (softmax, c=1e-7) | 13.3  | 39.2  |

Table 13: Performance on more language pairs.

<span id="page-15-0"></span>![](_page_15_Figure_0.svg)

Figure 4: Extracting alignments from our model using IterMax(Sabet et al., 2020) and our *softmax* method from the vanilla and fine-tuned mBERT models.

<span id="page-16-0"></span>![](_page_16_Figure_0.svg)

Figure 5: Cosine similarities between subword representations in a parallel sentence pair before and after fine-tuning. Red boxes indicate the gold alignments.