**Source:** *WavLM Base Plus model card* — [original page](https://huggingface.co/microsoft/wavlm-base-plus)

# 

[ 

![Figure](figures/0013ee76ef5510baab75c1c1517c2b6cc9f5997eb043d1c10f9b863267580584.webp)

 ](https://huggingface.co/microsoft)

[microsoft](https://huggingface.co/microsoft)

/

[wavlm-base-plus](https://huggingface.co/microsoft/wavlm-base-plus) 

![Figure](figures/07a9ac634e1a96dd6ff40ce3bdd22b6a595310c74c06d36a87b39b1d3b4518aa.svg)

 



![Figure](figures/1d34aae489280b7fcf11922ed70c861f512549bbdbaabcbd1dafda870a8ad023.svg)

 Like 41

Follow



![Figure](figures/0013ee76ef5510baab75c1c1517c2b6cc9f5997eb043d1c10f9b863267580584.webp)

 Microsoft 22.3k

[ 

![Figure](figures/27e07a64d027d3524bd9d09a2fd51c142ba5bd45469403352eeac6947b0613c6.svg)

  Feature Extraction ](https://huggingface.co/models?pipeline_tag=feature-extraction)[ 

![Figure](figures/006d81bbe727004eebf1ec992e7c5fa0f0402c2cb664afd4fc5193214a6e34cb.svg)

 Transformers ](https://huggingface.co/models?library=transformers)[ 

![Figure](figures/16e8fa5339915770efce107857d91fb2308b32afebfbd5fdd069e197d478417f.svg)

 PyTorch ](https://huggingface.co/models?library=pytorch)[ 

![Figure](figures/ae99d3c5b43856225d2991096ca2c860d325ea47bde8ec4178fdb01f16a96896.svg)

 English ](https://huggingface.co/models?language=en)[ wavlm ](https://huggingface.co/models?other=wavlm)[ speech ](https://huggingface.co/models?other=speech)



![Figure](figures/783d9fe2276038e2c7d61578e3c78fce0e24f5b33e6a7afad49fd3e5067d4987.svg)

 arxiv: 4 papers

[ 

![Figure](figures/3f595e0219ac3e5b1682b160dfab627869c642c69f4b94ed0360e51c34c079dc.svg)

 Model card ](https://huggingface.co/microsoft/wavlm-base-plus)[ 

![Figure](figures/d6a2ea6c6a9a479a26ba70e3f0990d3a51283dd5afde473547f2bfcfbcc42e1b.svg)

 Files Files and versions 

![Figure](figures/32b0f7a3114a28f6007e17cc21db1055b0f50462ef66cdbd37d1e7c0020b9822.svg)

 xet ](https://huggingface.co/microsoft/wavlm-base-plus/tree/main)[ 

![Figure](figures/f6fd32c5de99e81bd2a353e1000d8c0187b1ec18ead3e6feaf6adaf47e95c0be.svg)

 Community 2 ](https://huggingface.co/microsoft/wavlm-base-plus/discussions)



![Figure](figures/86f63e8088d1e12a50265a5402b87775fdfa4b9d84cbbdc745ab4ea5ad501037.svg)

 



![Figure](figures/3509a5e7b3681c1dff82916290dd29181fb42748ac29ab35ab5d9d5e74f38a4e.svg)

 Deploy 

![Figure](figures/30b741b99d26303bc997be0b462c076546e1f2fd82493d46bd121688fb4f11c9.svg)

 



![Figure](figures/c12b99a1b4862c5c15088fecad65b53f654827001cc81769768d36db1ea4f7ec.svg)

 Copy to bucket new



![Figure](figures/3a9b836f2274f54546ff000a4ba4c346cb1947ef6b33217b48e061c40557e4eb.svg)

 Use this model 

![Figure](figures/30b741b99d26303bc997be0b462c076546e1f2fd82493d46bd121688fb4f11c9.svg)

 

### Instructions to use microsoft/wavlm-base-plus with libraries, inference providers, notebooks, and local apps. Follow these links to get started.

  * Libraries
  * [ 

![Figure](figures/b478b634c8aed26fda1f1c53a8d44d8f237065d02bc80311a99d6ce29a172c59.svg)

 Transformers](https://huggingface.co/microsoft/wavlm-base-plus?library=transformers)

How to use microsoft/wavlm-base-plus with Transformers:
        
        # Use a pipeline as a high-level helper
        from transformers import pipeline
        
        pipe = pipeline("feature-extraction", model="microsoft/wavlm-base-plus")
        
        # Load model directly
        from transformers import AutoProcessor, AutoModel
        
        processor = AutoProcessor.from_pretrained("microsoft/wavlm-base-plus")
        model = AutoModel.from_pretrained("microsoft/wavlm-base-plus", device_map="auto")

  * Notebooks
  * [ 

![Figure](figures/d8ae7c05abaecc3be3cedefb3cd7291d11448d6dcc896ec93ecabe43f365bea6.svg)

 Google Colab](https://huggingface.co/microsoft/wavlm-base-plus/colab)
  * [ 

![Figure](figures/af5b49155f346d1ac8cc42764e742e59c3719a740faa65e8d8d0a672febc6f51.svg)

 Kaggle](https://huggingface.co/microsoft/wavlm-base-plus/kaggle)



**YAML Metadata Error:** "datasets" must be a string



![Figure](figures/c5a4cd142448c21e120a0629055b68769b8f78b0f8c62c2bdca7203d285c4735.svg)

 

  * [WavLM-Base-Plus](https://huggingface.co/microsoft/wavlm-base-plus#wavlm-base-plus "WavLM-Base-Plus")
  * [Usage](https://huggingface.co/microsoft/wavlm-base-plus#usage "Usage")
    * [Speech Recognition](https://huggingface.co/microsoft/wavlm-base-plus#speech-recognition "Speech Recognition")
    * [Speech Classification](https://huggingface.co/microsoft/wavlm-base-plus#speech-classification "Speech Classification")
    * [Speaker Verification](https://huggingface.co/microsoft/wavlm-base-plus#speaker-verification "Speaker Verification")
    * [Speaker Diarization](https://huggingface.co/microsoft/wavlm-base-plus#speaker-diarization "Speaker Diarization")
  * [Contribution](https://huggingface.co/microsoft/wavlm-base-plus#contribution "Contribution")
  * [License](https://huggingface.co/microsoft/wavlm-base-plus#license "License")



#  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/microsoft/wavlm-base-plus#wavlm-base-plus) WavLM-Base-Plus 

[Microsoft's WavLM](https://github.com/microsoft/unilm/tree/master/wavlm)

The base model pretrained on 16kHz sampled speech audio. When using the model, make sure that your speech input is also sampled at 16kHz. 

**Note** : This model does not have a tokenizer as it was pretrained on audio alone. In order to use this model **speech recognition** , a tokenizer should be created and the model should be fine-tuned on labeled text data. Check out [this blog](https://huggingface.co/blog/fine-tune-wav2vec2-english) for more in-detail explanation of how to fine-tune the model.

The model was pre-trained on:

  * 60,000 hours of [Libri-Light](https://arxiv.org/abs/1912.07875)
  * 10,000 hours of [GigaSpeech](https://arxiv.org/abs/2106.06909)
  * 24,000 hours of [VoxPopuli](https://arxiv.org/abs/2101.00390)



[Paper: WavLM: Large-Scale Self-Supervised Pre-Training for Full Stack Speech Processing](https://arxiv.org/abs/2110.13900)

Authors: Sanyuan Chen, Chengyi Wang, Zhengyang Chen, Yu Wu, Shujie Liu, Zhuo Chen, Jinyu Li, Naoyuki Kanda, Takuya Yoshioka, Xiong Xiao, Jian Wu, Long Zhou, Shuo Ren, Yanmin Qian, Yao Qian, Jian Wu, Michael Zeng, Furu Wei

**Abstract** _Self-supervised learning (SSL) achieves great success in speech recognition, while limited exploration has been attempted for other speech processing tasks. As speech signal contains multi-faceted information including speaker identity, paralinguistics, spoken content, etc., learning universal representations for all speech tasks is challenging. In this paper, we propose a new pre-trained model, WavLM, to solve full-stack downstream speech tasks. WavLM is built based on the HuBERT framework, with an emphasis on both spoken content modeling and speaker identity preservation. We first equip the Transformer structure with gated relative position bias to improve its capability on recognition tasks. For better speaker discrimination, we propose an utterance mixing training strategy, where additional overlapped utterances are created unsupervisely and incorporated during model training. Lastly, we scale up the training dataset from 60k hours to 94k hours. WavLM Large achieves state-of-the-art performance on the SUPERB benchmark, and brings significant improvements for various speech processing tasks on their representative benchmarks._

The original model can be found under <https://github.com/microsoft/unilm/tree/master/wavlm>.

#  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/microsoft/wavlm-base-plus#usage) Usage 

This is an English pre-trained speech model that has to be fine-tuned on a downstream task like speech recognition or audio classification before it can be used in inference. The model was pre-trained in English and should therefore perform well only in English. The model has been shown to work well on the [SUPERB benchmark](https://superbbenchmark.org/).

**Note** : The model was pre-trained on phonemes rather than characters. This means that one should make sure that the input text is converted to a sequence of phonemes before fine-tuning.

##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/microsoft/wavlm-base-plus#speech-recognition) Speech Recognition 

To fine-tune the model for speech recognition, see [the official speech recognition example](https://github.com/huggingface/transformers/tree/master/examples/pytorch/speech-recognition).

##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/microsoft/wavlm-base-plus#speech-classification) Speech Classification 

To fine-tune the model for speech classification, see [the official audio classification example](https://github.com/huggingface/transformers/tree/master/examples/pytorch/audio-classification).

##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/microsoft/wavlm-base-plus#speaker-verification) Speaker Verification 

TODO

##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/microsoft/wavlm-base-plus#speaker-diarization) Speaker Diarization 

TODO

#  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/microsoft/wavlm-base-plus#contribution) Contribution 

The model was contributed by [cywang](https://huggingface.co/cywang) and [patrickvonplaten](https://huggingface.co/patrickvonplaten).

#  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/microsoft/wavlm-base-plus#license) License 

The official license can be found [here](https://github.com/microsoft/UniSpeech/blob/main/LICENSE)

[ 

![design](figures/98f702b7622cf50c36dbba314c279c3d81295237eaa4f3ca39a1bda32ebda3f5.png)

 ](https://raw.githubusercontent.com/patrickvonplaten/scientific_images/master/wavlm.png)

Downloads last month
    254,924



![Figure](figures/cd9b20e46b79737e8b1883b494a027049247eade410b67d0c84d588b35d6e731.svg)

 



![Figure](figures/88a0c55f81e54aecdc2e32cfd0ea74f7ba732d9ac318471c3a072f0ffa5e802f.svg)

 Inference Providers [NEW](https://huggingface.co/docs/inference-providers)

[ 

![Figure](figures/60cc1727f6921cd14c7cb30aeaebdd1494353ad66209d41f06874857f2020e35.svg)

 Feature Extraction](https://huggingface.co/tasks/feature-extraction "Learn more about feature-extraction")

This model isn't deployed by any Inference Provider. [🙋 Ask for provider support](https://huggingface.co/spaces/huggingface/InferenceSupport/discussions/new?title=microsoft/wavlm-base-plus&description=React%20to%20this%20comment%20with%20an%20emoji%20to%20vote%20for%20%5Bmicrosoft%2Fwavlm-base-plus%5D\(%2Fmicrosoft%2Fwavlm-base-plus\)%20to%20be%20supported%20by%20Inference%20Providers.%0A%0A\(optional\)%20Which%20providers%20are%20you%20interested%20in%3F%20\(Novita%2C%20Hyperbolic%2C%20Together%E2%80%A6\)%0A)

##  

![Figure](figures/8e5d2a5c20093da01233396edf241924bda6fc86f2dfada0fcdd62e567d1c8b9.svg)

 Model tree for microsoft/wavlm-base-plus [ 

![Figure](figures/94a838574fc5d31445cc43e46e6e864df88a9d16397513b44527885b440124e9.svg)

 ](https://huggingface.co/docs/hub/model-cards#specifying-a-base-model)



![Figure](figures/f7edc8bdbacd02e9e60c07e4804c8915b8949c49a250b139adc1858c65958732.svg)

 

Adapters

[1 model](https://huggingface.co/models?other=base_model:adapter:microsoft/wavlm-base-plus)



![Figure](figures/f7edc8bdbacd02e9e60c07e4804c8915b8949c49a250b139adc1858c65958732.svg)

 

Finetunes

[36 models](https://huggingface.co/models?other=base_model:finetune:microsoft/wavlm-base-plus)



![Figure](figures/f7edc8bdbacd02e9e60c07e4804c8915b8949c49a250b139adc1858c65958732.svg)

 

Quantizations

[2 models](https://huggingface.co/models?other=base_model:quantized:microsoft/wavlm-base-plus)

##  

![Figure](figures/cf0c597a2dd54b4f2eb17326a437cce0dd2cf1606a941ea8b71b258a2df75585.svg)

 Spaces using microsoft/wavlm-base-plus 100

[📊 mteb/leaderboard ](https://huggingface.co/spaces/mteb/leaderboard)[🎤 smola/higgs_audio_v2 

![Figure](figures/ef3cfd5a728a55ab90d525bbc308e8e9ae5157df462a4866c0a2cf6593b7227a.svg)

  ](https://huggingface.co/spaces/smola/higgs_audio_v2)[🧢 OpenSound/CapSpeech-TTS 

![Figure](figures/ef3cfd5a728a55ab90d525bbc308e8e9ae5157df462a4866c0a2cf6593b7227a.svg)

  ](https://huggingface.co/spaces/OpenSound/CapSpeech-TTS)[🔊 hugging-apps/unise-speech-enhancement 

![Figure](figures/ef3cfd5a728a55ab90d525bbc308e8e9ae5157df462a4866c0a2cf6593b7227a.svg)

  ](https://huggingface.co/spaces/hugging-apps/unise-speech-enhancement)[🐆 nineninesix/gepard 

![Figure](figures/ef3cfd5a728a55ab90d525bbc308e8e9ae5157df462a4866c0a2cf6593b7227a.svg)

  ](https://huggingface.co/spaces/nineninesix/gepard)[😊🎙️📖 litagin/Style-Bert-VITS2-Editor-Demo ](https://huggingface.co/spaces/litagin/Style-Bert-VITS2-Editor-Demo)[💫 Plana-Archive/BanG-Dream-VITS ](https://huggingface.co/spaces/Plana-Archive/BanG-Dream-VITS)[📊 ALM/ARCH ](https://huggingface.co/spaces/ALM/ARCH) \+ 95 Spaces \+ 92 Spaces

##  

![Figure](figures/b844e37eb6c73155067655f28a5ae438131c4a2fb60fb4c5594a3a2e4bbbae18.svg)

 Papers for microsoft/wavlm-base-plus

#### [WavLM: Large-Scale Self-Supervised Pre-Training for Full Stack Speech Processing 

![Figure](figures/76a94b593dca78642338990eb26c1d3d8f949cea5947d43e6c5d764a627c4688.svg)

 Paper • 2110.13900 • Published Oct 26, 2021 • 

![Figure](figures/26079970d7c967ac733cd8827a6a5b861feb37fd9cdfa4c7ff6e2a603f3a60d6.svg)

 3 ](https://huggingface.co/papers/2110.13900)#### [GigaSpeech: An Evolving, Multi-domain ASR Corpus with 10,000 Hours of Transcribed Audio 

![Figure](figures/76a94b593dca78642338990eb26c1d3d8f949cea5947d43e6c5d764a627c4688.svg)

 Paper • 2106.06909 • Published Jun 13, 2021 • 

![Figure](figures/26079970d7c967ac733cd8827a6a5b861feb37fd9cdfa4c7ff6e2a603f3a60d6.svg)

 1 ](https://huggingface.co/papers/2106.06909)#### [VoxPopuli: A Large-Scale Multilingual Speech Corpus for Representation Learning, Semi-Supervised Learning and Interpretation 

![Figure](figures/76a94b593dca78642338990eb26c1d3d8f949cea5947d43e6c5d764a627c4688.svg)

 Paper • 2101.00390 • Published Jan 2, 2021 • 

![Figure](figures/26079970d7c967ac733cd8827a6a5b861feb37fd9cdfa4c7ff6e2a603f3a60d6.svg)

 1 ](https://huggingface.co/papers/2101.00390)#### [Libri-Light: A Benchmark for ASR with Limited or No Supervision 

![Figure](figures/76a94b593dca78642338990eb26c1d3d8f949cea5947d43e6c5d764a627c4688.svg)

 Paper • 1912.07875 • Published Dec 17, 2019 ](https://huggingface.co/papers/1912.07875)
