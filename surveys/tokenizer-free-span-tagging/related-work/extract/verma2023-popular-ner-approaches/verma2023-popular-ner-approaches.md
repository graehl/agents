# Comparing and combining some popular NER approaches on Biomedical tasks

### Harsh Verma, Sabine Bergler, Narjesossadat Tahaei

CLaC Labs, Concordia University {h\_ver, bergler, n\_tahaei} @cse.concordia.ca

## Abstract

We compare three simple and popular approaches for NER: 1) SEQ (sequencelabeling with a linear token classifier) 2) SeqCRF (sequence-labeling with Conditional Random Fields), and 3) SpanPred (spanprediction with boundary token embeddings). We compare the approaches on 4 biomedical NER tasks: GENIA, NCBI-Disease, LivingNER (Spanish), SocialDisNER (Spanish). The SpanPred model demonstrates state-of-the-art performance on LivingNER and SocialDisNER, improving F1 by 1.3 and 0.6 F1 respectively. The SeqCRF model also demonstrates state-of-the-art performance on LivingNER and SocialDisNER, improving F1 by 0.2 F1 and 0.7 respectively. The SEQ model is competitive with the state-of-the-art on the LivingNER dataset. We explore some simple ways of combining the three approaches. We find that majority voting consistently gives high precision and high F1 across all 4 datasets. Lastly, we implement a system that learns to combine the predictions of SEQ and SpanPred, generating systems that consistently give high recall and high F1 across all 4 datasets. On the GENIA dataset, we find that our learned combiner system significantly boosts F1(+1.2) and recall(+2.1) over the systems being combined. We release all the well-documented code necessary to reproduce all systems at this [Github repository.](https://github.com/flyingmothman/bionlp)

# 1 Introduction

NER has frequently been formulated as a sequencelabeling problem [\(Chiu and Nichols,](#page-4-0) [2016;](#page-4-0) [Ma and](#page-5-0) [Hovy,](#page-5-0) [2016;](#page-5-0) [Wang et al.,](#page-5-1) [2022\)](#page-5-1) in which a model learns to label each token using a labeling scheme such as BIO(*beginning*, *inside*, *outside*). However, in recent years people have also formulated the NER task as a span-prediction problem [\(Jiang et al.,](#page-5-2) [2020;](#page-5-2) [Li et al.,](#page-5-3) [2020;](#page-5-3) [Fu et al.,](#page-5-4) [2021;](#page-5-4) [Zhang et al.,](#page-6-0) [2023\)](#page-6-0) where spans of text are represented and labeled with entity types.

Let SEQ be the simplest sequence-labeling model which represents each token using a language model and then classifies each token-representation with a linear layer. Let SeqCRF be another popular sequence-labeling model which is identical to SEQ model except that the token representations from the language model are fed into a linear-chain conditional random field layer[\(Lafferty et al.,](#page-5-5) [2001;](#page-5-5) [Lample et al.,](#page-5-6) [2016\)](#page-5-6). Let SpanPred[\(Lee](#page-5-7) [et al.,](#page-5-7) [2017;](#page-5-7) [Jiang et al.,](#page-5-2) [2020\)](#page-5-2) be a model that represents every possible span of text using two token-embeddings located at the its boundary, and then classifies every span-representation using a linear layer. We describe all three models in detail in [section 4.](#page-1-0) We evaluate SEQ, SeqCRF, and SpanPred models on four biomedical NER tasks: GENIA[\(Kim et al.,](#page-5-8) [2003\)](#page-5-8), NCBI-Disease[\(Dogan](#page-4-1) ˘ [et al.,](#page-4-1) [2014\)](#page-4-1), LivingNER(Spanish)[\(Miranda-](#page-5-9)[Escalada et al.,](#page-5-9) [2022\)](#page-5-9), and SocialDisNER(Spanish)[\(Gasco Sánchez et al.,](#page-5-10) [2022\)](#page-5-10). Despite being simple, the SpanPred and CRF models improve the state-of-the-art on the LivingNER and SocialDisNER tasks.

[\(Fu et al.,](#page-5-4) [2021\)](#page-5-4) show that the sequencelabeling approaches(eg. Seq and SeqCRF) and span-prediction approaches(eg. SpanPred) have *different* strengths and weaknesses *while* having similar(F1) performance. This motivated us to try and combine Seq, SeqCRF, and SpanPred models using two simple methods and study the results. We refer to the two simple methods as Union and MajVote. Union is inspired by the set(mathematical) union operation and it simply involves "unioning" the sets of predictions made by the models. MajVote is the classic majority voting method. We find that MajVote can yield systems that have both high precision and high F1.

Inspired by the boost in recall(and the corresponding drop in precision) resulting from the Union method, we implemented a combiner system (which we refer to as Meta) that aims to *combat* the drop in precision as a result of the Union method. We find that Meta shows very promising signs of increasing precision while preserving high recall and high F1. Meta borrows ideas from work on generating span representations using "solid markers" (Baldini Soares et al., 2019; Xiao et al., 2020; Ye et al., 2022), work on using prompts (Li et al., 2020), and work by (Fu et al., 2021) to combine the span-prediction and sequence-labeling approaches using the span-prediction approach.

### <span id="page-1-1"></span>2 Preliminaries

Let every prediction p of an NER system be a tuple of the form

p = (SampleId, EntityType, BeginOffset, EndOffset)

which consists of the identifier of the sample/text in which the entity is found, the type of the entity, and the beginning and ending offsets for the entity.

## 3 Preprocessing

For GENIA and NCBI-Disease, each sample is an English sentence. For SocialDisNER, each sample is an entire Spanish tweet. For LivingNER, we use the FLERT(Schweter and Akbik, 2020) approach for document-level NER, in which each Spanish sentence is surrounded by a context of 100 characters to the left and 100 characters to the right.

### <span id="page-1-0"></span>4 Models

#### 4.1 Seg model

**Token Representation Step** Given a sentence  $\mathbf{x} = [w_1, w_2, ..., w_n]$  with n tokens, we generate for each token  $w_i$  a contextualized embedding  $\mathbf{u}_i \in \mathbb{R}^d$  that corresponds to the last-hidden-layer representation of the language model. Here, d represents the size of the token embedding. Importantly, special tokens like [CLS] and [SEP] are also represented. We find that the performance can drop significantly(especially for SEQ) if they are not incorporated in the learning process.

XLM-RoBERTa large(Conneau et al., 2020) is the multilingual language model that we use for the LivingNER and SocialDisNER spanish tasks. Inspired by its high performance on the BLURB(Gu et al., 2021) biomedical benchmark, we use BioLinkBert large(Yasunaga et al., 2022) for the NCBI-Disease and GENIA datasets.

**Token Classification Step** In this layer, we classify every token representation into a set of named entity types corresponding to the BIO(beginning, inside, outside) tagging scheme. Assuming  $\Theta$  is the set of all named entity types, then the set of all BIO tags  $\mathbf{B}$  is of size  $(2 \times |\Theta|) + 1$ . In other words, a linear layer maps each token representation  $\mathbf{u}_i \in \mathbb{R}^d$  to a prediction  $\mathbf{p}_i \in \mathbb{R}^{|\mathbf{B}|}$ , where d is the length of the token embedding. Finally, the predictions are used to calculate loss of given sentence  $\mathbf{x}$  with n tokens as follows:

$$Loss(\mathbf{x}) = \frac{-1}{n} \sum_{i=1}^{n} \log(Softmax(\mathbf{p}_i)_{y_i})$$
 (1)

Here  $y_i$  represents the index of the gold BIO label of the  $i^{th}$  token.

### 4.2 SegCRF Model

This model is identical to the Seq model except that we pass the contextualized token representation U through a Linear Chain CRF(Lafferty et al., 2001) layer. The CRF layer computes the probabilities of labeling the sequence using the Viterbi algorithm(Forney, 1973). A loss suited to the CRF layer's predictions is then used to train the model. We directly use the CRF implementation available in the FLAIR(Akbik et al., 2019) framework. The BIO scheme is used for token classification.

#### 4.3 Span Model

**Token Representation Layer** Same as the token representation layer of the Seq model.

**Span Representation Layer** Let a span s be a tuple s = (b, e) where b and e are the beggining and ending token indices, and s represents the text segment  $[w_b, w_{b+1}, ..., w_e]$  where  $w_i$  is the  $i^{th}$ token. In this layer, we enumerate all possible spans and then represent each span using two token embeddings located at its boundary. More precisely, given embeddings  $[\mathbf{u}_1, \mathbf{u}_2, ..., \mathbf{u}_n]$  of n tokens, there are  $\binom{n}{2} = \frac{n^2}{2}$  possible spans, which can be enumerated and represented as the list [(0,0),(0,1),...,(0,n),(1,1),(1,2)...(1,n),...(n,n)]. Then we removed all spans that have a length longer than 32 tokens – this was important to fit the model in GPU memory with a batch size of 4. Finally, as in (Lee et al., 2017), each span  $s_i$  will be represented by  $\mathbf{v}_i = [\mathbf{u}_{b_i}; \mathbf{u}_{e_i}]$ , a concatenation of the beginning and ending token embeddings.

<span id="page-2-1"></span>

| Dataset                         | SocialDisNER                    | LivingNER                       | Genia                           | NCBI-Disease                    |
|---------------------------------|---------------------------------|---------------------------------|---------------------------------|---------------------------------|
| SOTA                            | (Fu et al., 2022)               | (Zotova et al., 2022)           | (Shen et al., 2022)             | (Tian et al., 2020)             |
|                                 | 89.1, 90.6, 87.6                | 95.1, 95.8, 94.3                | 81.7, -, -                      | 90.08, -, -                     |
| SpanPred                        | 90.4, 90.5, 90.4                | 95.7, 95.4, 96.0                | 77.1, 77.0, 77.1                | 89.0, 88.1, 89.9                |
| SEQ                             | 88.7, 88.3, 89.1                | 95.0, 94.7, 95.3                | 76.1, 79.8, 72.7                | 88.7, 87.8, 89.5                |
| SeqCRF                          | 89.8, 89.6, 90.0                | 95.3, 95.6, 95.0                | 75.7, 79.7, 72.1                | 87.9, 86.2, 89.6                |
| SpanPred ∪ SEQ                  | 89.0, 86.0, 92.2                | 95.2, 93.4, 97.1                | 77.2, 73.5, 81.4                | 88.2, 84.6, 92.2                |
| SpanPred x SEQ                  | 90.2, 93.3, 87.3                | 95.5, 96.9, 94.2                | 75.8, 85.0, 68.5                | <b>89.6</b> , 91.9, 87.4        |
| $SpanPred \cup SEQ \cup SeqCRF$ | 88.3, 84.1, 93.0                | 94.9, 92.5, 97.4                | 76.4, 71.3, 82.3                | 87.1, 81.4, 93.8                |
| SpanPred x SEQ x SeqCRF         | <b>90.8</b> , 91.2, 90.4        | 95.7, 96.1, 95.4                | 77.1, 81.9, 72.9                | 89.5, 88.8, 90.1                |
| $Meta(SpanPred \cup SEQ)$       | <u>90.5</u> , 89.7, <u>91.3</u> | <b>95.7</b> , 94.6, <u>96.9</u> | <b>78.3</b> , 77.4, <u>79.2</u> | <u>89.1</u> , 86.3, <u>92.2</u> |

Table 1: Performance of all systems on test set on all 4 biomedical datasets.  $\cup$  represents the Union combiner and x represents the MajVote combiner.

Hence, the output of this layer is  $\mathbf{V} \in \mathbb{R}^{k \times (2 \times d)}$  where  $k = \frac{n^2}{2}$  and d is length of the token embedding vector.

**Span Classification Layer** In this layer, we classify each span representation with a named entity type. We introduce an additional label Neg\_Span which represents the absence of a named entity. Precisely, a linear layer maps each span representation  $\mathbf{v}_i \in \mathbb{R}^{(2 \times d)}$  to a prediction  $\mathbf{p}_i \in \mathbb{R}^{|\Omega|}$ , where  $\Omega$  is the set of all named entity types(including Neg\_Span) and d is the size of the token embedding. Finally, the predictions are used to calculate loss of given sentence  $\mathbf{x}$  with l possible spans as follows:

$$Loss(\mathbf{x}) = \frac{-1}{l} \sum_{i=1}^{l} \log(Softmax(\mathbf{p}_i)_{y_i})$$
 (2)

Here  $y_i$  represents the index of the gold label of the  $i^{th}$  span.

#### 4.4 Union combiner model

This model doesn't learn weights. For a given list  $P_0, P_1, ..., P_n$  where  $P_i$  is the set of predictions(as defined in section 2) made by the  $i^{th}$  NER model and n is the total number of models, it returns the set  $P_1 \cup P_2 \cup ... P_n$ .

## 4.5 MajVote combiner model

This model doesn't learn weights. This is the classic majority voting combiner model. Precisely, when given a list  $P_0, P_1, ..., P_n$  where  $P_i$  is the set of predictions(as defined in section 2) made by the  $i^{th}$  NER model and n is the total number of models, it returns a set which only includes predictions in  $P_1 \cup P_2 \cup ... P_n$  that have been predicted by more that  $\left|\frac{n}{2}\right|$  models.

<span id="page-2-0"></span>![](_page_2_Picture_10.svg)

Figure 1: An illustration showing how Meta operates. Here, Meta is learning from the predictions made by 3 different NER systems on the validation set.

#### 4.6 Meta combiner model

The job of meta is simple: "Learn to tell if a prediction made by SEQ or SpanPred is a mistake or not". In other words, Meta looks at a prediction made by SEQ or SpanPred on the *validation set* and learns to classify the prediction as being either "correct" or "incorrect". "correct" means that the prediction is a good prediction, and that it should not be removed. "incorrect" means that the prediction should be removed. In other words, if  $P_{\rm SEQ}$  is the set of all predictions of the SEQ and  $P_{\rm Span}$  is the set of all predictions of SpanPred, then Meta acts as (and learns to be) a filter for  $P_{\rm Span} \cup P_{\rm SEQ}$ . During evaluation, Meta filters  $P_{\rm Span} \cup P_{\rm SEQ}$ , generating a final set of predictions.

[Figure 1](#page-2-0) illustrates the role of meta in the pipeline.

We borrow the idea of using markers made with special tokens [\(Baldini Soares et al.,](#page-4-2) [2019;](#page-4-2) [Xiao](#page-6-1) [et al.,](#page-6-1) [2020;](#page-6-1) [Ye et al.,](#page-6-2) [2022\)](#page-6-2) which, intuitively, help models "focus their attention on the span-ofinterest". In other words, by introducing special tokens(which act as markers) like [e] and [/e] in the language model's vocabulary, and then surrounding the span-of-interest with them, one can help the model "focus" of the span of interest while making some prediction. In Meta's case, the markers are supposed to help locate/identify the entities predicted by SEQ or SpanPred in raw text. See [subsection 4.7](#page-3-0) for an example input prediction with markers highlighting the entity.

We also borrow the idea of prompting[\(Li](#page-5-3) [et al.,](#page-5-3) [2020\)](#page-5-3), which involves pre-pending some text(prompt) to the original input text with the goal of priming(or aiding) a model's decision making with a useful bias. In particular, every input to Meta includes the type of the predicted entity as prompt. Intuitively, this helps Meta recognize the type of the entity it is dealing with. See [subsection 4.7](#page-3-0) for an example of prompting with the entity type "disease".

Note that prompting and special markers are *only* used to prepare the training data for Meta using the predictions of SEQ and SpanPred on the validation set. Meta itself is a simple binary classification neural model. Just like SEQ, SeqCRF and SpanPred, it first creates contextualized token representations from raw input using the appropriate language model(XLM-RoBERTa or BioLinkBERT) and then classifies the pooler token([CLS] or [s]) representation using a linear layer. As in SpanPred and SEQ, cross-entropy loss is used to train the model.

Because META acts as a "filter"(it allows certain predictions and disallows others), it *cannot* improve recall – it can only improve precision. Ideally, Meta will learn the true nature of the mistakes that SEQ and SpanPred make and remove all false positives, resulting in a perfect precision score of 100 and no drop in recall.

Preparing the training data for **Meta**: *all* predictions(with "correct" and "incorrect" labels) on the validation set for *all* 20 epochs by *both* SEQ and SpanPRED, and *all* gold predictions(that only have "correct" labels) from the *original* training data make up the training set for Meta. We hold out 15 percent of Meta's training set for validation. Note that we incorporate the predictions of SpanPred and SEQ from earlier epochs because the fully trained high-performing models don't make that many mistakes(which META needs for its learning). As expected, the test set is not touched while training Meta. During evaluation, Meta filters the predictions made by SEQ and SpanPred on the test set.

## <span id="page-3-0"></span>4.7 Meta input example

Assume the example sentence "Bob has HIV and flu." and the task of identifying diseases. Now assume that SEQ predicted

(id, disease, 8, 11) (see [section 2](#page-1-1) for the definition of prediction) and correctly identified the disease "HIV" in the input. Then, the input to meta will be the the text "**disease** Bob has [e] HIV [/e] and flu" and the associated gold label of correct. Prompting with disease informs Meta that it is dealing with a prediction representing a disease. Meta has to make a judgement on whether the prediction is correct or not.

### 4.8 Training and Optimization

Both XLM RoBERTa large[\(Conneau et al.,](#page-4-3) [2020\)](#page-4-3) and BioLinkBERT large[\(Yasunaga et al.,](#page-6-3) [2022\)](#page-6-3) are fine-tuned on the training data using the Adafactor[\(Shazeer and Stern,](#page-5-15) [2018\)](#page-5-15) optimizer with a learning rate of 1e-5(see [code\)](https://github.com/flyingmothman/bionlp/blob/d61b02593711b43b5d0f00f0c6ed62fb7685adf3/utils/training.py#L13-L20) and a batch size of 4 for *all 4 datasets*. Specifically, we used [the implementation of Adafactor](https://huggingface.co/docs/transformers/main_classes/optimizer_schedules#transformers.Adafactor) available on HuggingFace[\(Wolf et al.,](#page-5-16) [2019\)](#page-5-16). It was not possible for us to use the same learning rate and batch size for every dataset with Adam[\(Kingma](#page-5-17) [and Ba,](#page-5-17) [2015\)](#page-5-17) because we noticed it was prone to over-fitting(and then collapsing) mid-training on LivingNER, NCBI-Disease, and GENIA – batch-size had to be increased to avoid overfitting. Moreover, we found that SEQ, SeqCRF, and SpanPred converged to better solutions with Adafactor on all datasets. However, we found that Meta consistently converged to better solutions on the NCBI disease dataset using Adam.

The best model is selected using early stopping with a patience(in terms of epochs) of 5.

# 5 Evaluation Methodology

All tasks evaluate systems using the strict(no partial matching) Micro F1, Precision and Recall. For SocialDisNER, *all* systems were submitted to the corresponding CodaLab[\(Pavao et al.,](#page-5-18)

[2022\)](#page-5-18) competition website for evaluation. For LivingNER, *all* our systems have been evaluated using the [official evaluation script](https://temu.bsc.es/livingner/2022/01/28/evaluation/) that the organizers made available. For Genia and NCBI-Disease, we unfortunately couldn't find official CodaLab websites, so we had to use our own script, which can be inspected [here.](https://github.com/flyingmothman/bionlp)

# 6 Analysis of Results

Note that among the 3 models, SpanPred consistently outperforms the other two on all datasets. This is anticipated on tasks with overlapping entities like LivingNER and GENIA(because SEQ and SeqCRF cannot represent them), but not on "flat" NER tasks like SocialDisNER and NCBI-Disease.

Note that any system resulting from a Union combination should have higher recall than any of the involved systems because a set union operation is incapable of removing a correct prediction (the set of false negatives can only shrink with more systems). Also, the resulting system's precision cannot be higher than the highest precision observed in any sub-system. [Table 1](#page-2-1) adheres to both of these expectations. On the other hand, a system resulting from a MajVote combiner is *inclined* to have higher precision when the systems being combined are diverse and comparable because – intuitively – MajVote can be a more "picky" system (only allowing a prediction if it has been voted on by several). In [Table 1,](#page-2-1) note that both SpanPred**x**SEQ and SpanPred**x**SEQ**x**CRF consistently boost precision across all datasets. Also note that the best MajVote systems significantly outperform all other systems on precision while maintaining the highest F1 on all datasets except Genia, where Meta outperforms all other systems on F1 for the first(and last) time. Also on Genia is the only time when a Union model (SpanPred∪SEQ) outperforms the MajVote models due to a significant boost in recall. Finally, note how Meta, across all datasets, outperforms SpanPred, SEQ, and SeqCRF models on Recall and delivers an F1 that is at least as high as any of the three models.

## 7 Conclusion

Our implementation[\(code available\)](https://github.com/flyingmothman/bionlp) of CRF and SpanPred, two simple models, improves the state of the art on LivingNER and SocialDisNER datasets. We used two simple approaches called Union and MajVote to combine the NER models' predictions and studied the results. MajVote on the three NER models seems to be effective at generating systems with high precision and high F1. While Union can generate systems with higher recall, it is only at the cost of F1 due to a significant drop in precision. Meta seems to be effective at alleviating Union's issue, generating systems with both high recall and high F1.

## References

<span id="page-4-5"></span>Alan Akbik, Tanja Bergmann, Duncan Blythe, Kashif Rasul, Stefan Schweter, and Roland Vollgraf. 2019. [FLAIR: An easy-to-use framework for state-of-the](https://doi.org/10.18653/v1/N19-4010)[art NLP.](https://doi.org/10.18653/v1/N19-4010) In *Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics (Demonstrations)*, pages 54–59, Minneapolis, Minnesota. Association for Computational Linguistics.

<span id="page-4-2"></span>Livio Baldini Soares, Nicholas FitzGerald, Jeffrey Ling, and Tom Kwiatkowski. 2019. [Matching](https://doi.org/10.18653/v1/P19-1279) [the blanks: Distributional similarity for relation](https://doi.org/10.18653/v1/P19-1279) [learning.](https://doi.org/10.18653/v1/P19-1279) In *Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics*, pages 2895–2905, Florence, Italy. Association for Computational Linguistics.

<span id="page-4-0"></span>Jason P.C. Chiu and Eric Nichols. 2016. [Named](https://doi.org/10.1162/tacl_a_00104) [entity recognition with bidirectional LSTM-CNNs.](https://doi.org/10.1162/tacl_a_00104) *Transactions of the Association for Computational Linguistics*, 4:357–370.

<span id="page-4-3"></span>Alexis Conneau, Kartikay Khandelwal, Naman Goyal, Vishrav Chaudhary, Guillaume Wenzek, Francisco Guzmán, Edouard Grave, Myle Ott, Luke Zettlemoyer, and Veselin Stoyanov. 2020. [Unsupervised cross-lingual representation learning at](https://doi.org/10.18653/v1/2020.acl-main.747) [scale.](https://doi.org/10.18653/v1/2020.acl-main.747) In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, pages 8440–8451, Online. Association for Computational Linguistics.

<span id="page-4-1"></span>Rezarta Islamaj Dogan, Robert Leaman, and Zhiyong ˘ Lu. 2014. Ncbi disease corpus: a resource for disease name recognition and concept normalization. *Journal of biomedical informatics*, 47:1–10.

<span id="page-4-4"></span>G David Forney. 1973. The viterbi algorithm. *Proceedings of the IEEE*, 61(3):268–278.

<span id="page-4-6"></span>Jia Fu, Sirui Li, Hui Ming Yuan, Zhucong Li, Zhen Gan, Yubo Chen, Kang Liu, Jun Zhao, and Shengping Liu. 2022. [CASIA@SMM4H'22: A uniform health](https://aclanthology.org/2022.smm4h-1.39) [information mining system for multilingual social](https://aclanthology.org/2022.smm4h-1.39) [media texts.](https://aclanthology.org/2022.smm4h-1.39) In *Proceedings of The Seventh Workshop on Social Media Mining for Health Applications, Workshop & Shared Task*, pages 143–147, Gyeongju, Republic of Korea. Association for Computational Linguistics.

- <span id="page-5-4"></span>Jinlan Fu, Xuanjing Huang, and Pengfei Liu. 2021. [SpanNER: Named entity re-/recognition](https://doi.org/10.18653/v1/2021.acl-long.558) [as span prediction.](https://doi.org/10.18653/v1/2021.acl-long.558) In *Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)*, pages 7183–7195, Online. Association for Computational Linguistics.
- <span id="page-5-10"></span>Luis Gasco Sánchez, Darryl Estrada Zavala, Eulàlia Farré-Maduell, Salvador Lima-López, Antonio Miranda-Escalada, and Martin Krallinger. 2022. [The](https://aclanthology.org/2022.smm4h-1.48) [SocialDisNER shared task on detection of disease](https://aclanthology.org/2022.smm4h-1.48) [mentions in health-relevant content from social](https://aclanthology.org/2022.smm4h-1.48) [media: methods, evaluation, guidelines and corpora.](https://aclanthology.org/2022.smm4h-1.48) In *Proceedings of The Seventh Workshop on Social Media Mining for Health Applications, Workshop & Shared Task*, pages 182–189, Gyeongju, Republic of Korea. Association for Computational Linguistics.
- <span id="page-5-12"></span>Yu Gu, Robert Tinn, Hao Cheng, Michael Lucas, Naoto Usuyama, Xiaodong Liu, Tristan Naumann, Jianfeng Gao, and Hoifung Poon. 2021. Domainspecific language model pretraining for biomedical natural language processing. *ACM Transactions on Computing for Healthcare (HEALTH)*, 3(1):1–23.
- <span id="page-5-2"></span>Zhengbao Jiang, Wei Xu, Jun Araki, and Graham Neubig. 2020. [Generalizing natural language](https://doi.org/10.18653/v1/2020.acl-main.192) [analysis through span-relation representations.](https://doi.org/10.18653/v1/2020.acl-main.192) In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, pages 2120–2133, Online. Association for Computational Linguistics.
- <span id="page-5-8"></span>J-D Kim, Tomoko Ohta, Yuka Tateisi, and Jun'ichi Tsujii. 2003. Genia corpus—a semantically annotated corpus for bio-textmining. *Bioinformatics*, 19(suppl\_1):i180–i182.
- <span id="page-5-17"></span>Diederik P Kingma and Jimmy Ba. 2015. Adam: A method for stochastic optimization. In *Proceedings of the 3rd International Conference on Learning Representations, ICLR'15*.
- <span id="page-5-5"></span>John Lafferty, Andrew McCallum, and Fernando CN Pereira. 2001. Conditional random fields: Probabilistic models for segmenting and labeling sequence data.
- <span id="page-5-6"></span>Guillaume Lample, Miguel Ballesteros, Sandeep Subramanian, Kazuya Kawakami, and Chris Dyer. 2016. [Neural architectures for named entity](https://doi.org/10.18653/v1/N16-1030) [recognition.](https://doi.org/10.18653/v1/N16-1030) In *Proceedings of the 2016 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies*, pages 260–270, San Diego, California. Association for Computational Linguistics.
- <span id="page-5-7"></span>Kenton Lee, Luheng He, Mike Lewis, and Luke Zettlemoyer. 2017. [End-to-end neural coreference](https://doi.org/10.18653/v1/D17-1018) [resolution.](https://doi.org/10.18653/v1/D17-1018) In *Proceedings of the 2017 Conference on Empirical Methods in Natural Language Processing*, pages 188–197, Copenhagen, Denmark. Association for Computational Linguistics.

- <span id="page-5-3"></span>Xiaoya Li, Jingrong Feng, Yuxian Meng, Qinghong Han, Fei Wu, and Jiwei Li. 2020. [A unified](https://doi.org/10.18653/v1/2020.acl-main.519) [MRC framework for named entity recognition.](https://doi.org/10.18653/v1/2020.acl-main.519) In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, pages 5849–5859, Online. Association for Computational Linguistics.
- <span id="page-5-0"></span>Xuezhe Ma and Eduard Hovy. 2016. [End-to-end](https://doi.org/10.18653/v1/P16-1101) [sequence labeling via bi-directional LSTM-CNNs-](https://doi.org/10.18653/v1/P16-1101)[CRF.](https://doi.org/10.18653/v1/P16-1101) In *Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 1064–1074, Berlin, Germany. Association for Computational Linguistics.
- <span id="page-5-9"></span>Antonio Miranda-Escalada, Eulàlia Farré-Maduell, Salvador Lima-López, Darryl Estrada, Luis Gascó, and Martin Krallinger. 2022. Mention detection, normalization & classification of species, pathogens, humans and food in clinical documents: Overview of the livingner shared task and resources. *Procesamiento del Lenguaje Natural*, 69:241–253.
- <span id="page-5-18"></span>Adrien Pavao, Isabelle Guyon, Anne-Catherine Letournel, Xavier Baró, Hugo Escalante, Sergio Escalera, Tyler Thomas, and Zhen Xu. 2022. *CodaLab Competitions: An open source platform to organize scientific challenges*. Ph.D. thesis, Université Paris-Saclay, FRA.
- <span id="page-5-11"></span>Stefan Schweter and Alan Akbik. 2020. Flert: Document-level features for named entity recognition. *arXiv preprint arXiv:2011.06993*.
- <span id="page-5-15"></span>Noam Shazeer and Mitchell Stern. 2018. Adafactor: Adaptive learning rates with sublinear memory cost. In *International Conference on Machine Learning*, pages 4596–4604. PMLR.
- <span id="page-5-13"></span>Yongliang Shen, Xiaobin Wang, Zeqi Tan, Guangwei Xu, Pengjun Xie, Fei Huang, Weiming Lu, and Yueting Zhuang. 2022. [Parallel instance](https://doi.org/10.18653/v1/2022.acl-long.67) [query network for named entity recognition.](https://doi.org/10.18653/v1/2022.acl-long.67) In *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 947–961, Dublin, Ireland. Association for Computational Linguistics.
- <span id="page-5-14"></span>Yuanhe Tian, Wang Shen, Yan Song, Fei Xia, Min He, and Kenli Li. 2020. Improving biomedical named entity recognition with syntactic information. *BMC bioinformatics*, 21(1):1–17.
- <span id="page-5-1"></span>Xinyu Wang, Yongliang Shen, Jiong Cai, Tao Wang, Xiaobin Wang, Pengjun Xie, Fei Huang, Weiming Lu, Yueting Zhuang, Kewei Tu, Wei Lu, and Yong Jiang. 2022. [DAMO-NLP at SemEval-2022 task](https://doi.org/10.18653/v1/2022.semeval-1.200) [11: A knowledge-based system for multilingual](https://doi.org/10.18653/v1/2022.semeval-1.200) [named entity recognition.](https://doi.org/10.18653/v1/2022.semeval-1.200) In *Proceedings of the 16th International Workshop on Semantic Evaluation (SemEval-2022)*, pages 1457–1468, Seattle, United States. Association for Computational Linguistics.
- <span id="page-5-16"></span>Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement Delangue, Anthony Moi, Pierric

- Cistac, Tim Rault, Rémi Louf, Morgan Funtowicz, et al. 2019. Huggingface's transformers: State-ofthe-art natural language processing. *arXiv preprint arXiv:1910.03771*.
- <span id="page-6-1"></span>Chaojun Xiao, Yuan Yao, Ruobing Xie, Xu Han, Zhiyuan Liu, Maosong Sun, Fen Lin, and Leyu Lin. 2020. [Denoising relation extraction from document](https://doi.org/10.18653/v1/2020.emnlp-main.300)[level distant supervision.](https://doi.org/10.18653/v1/2020.emnlp-main.300) In *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, pages 3683–3688, Online. Association for Computational Linguistics.
- <span id="page-6-3"></span>Michihiro Yasunaga, Jure Leskovec, and Percy Liang. 2022. [LinkBERT: Pretraining language models](https://doi.org/10.18653/v1/2022.acl-long.551) [with document links.](https://doi.org/10.18653/v1/2022.acl-long.551) In *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 8003– 8016, Dublin, Ireland. Association for Computational Linguistics.
- <span id="page-6-2"></span>Deming Ye, Yankai Lin, Peng Li, and Maosong Sun. 2022. [Packed levitated marker for entity and](https://doi.org/10.18653/v1/2022.acl-long.337) [relation extraction.](https://doi.org/10.18653/v1/2022.acl-long.337) In *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 4904– 4917, Dublin, Ireland. Association for Computational Linguistics.
- <span id="page-6-0"></span>Sheng Zhang, Hao Cheng, Jianfeng Gao, and Hoifung Poon. 2023. [Optimizing bi-encoder for named](https://openreview.net/forum?id=9EAQVEINuum) [entity recognition via contrastive learning.](https://openreview.net/forum?id=9EAQVEINuum) In *The Eleventh International Conference on Learning Representations*.
- <span id="page-6-4"></span>Elena Zotova, Aitor García-Pablos, Naiara Perez, Pablo Turón, and Montse Cuadros. 2022. Vicomtech at livingner 2022. In *CEUR workshop proceedings*.