**Source:** *Community-1 speaker diarization* — [original page](https://huggingface.co/pyannote/speaker-diarization-community-1)

# 

[ 

![Figure](figures/1c41836c10c63df063fa76ae31053dce6c6ae058955f6d20376d0f9a6f1714e0.webp)

 ](https://huggingface.co/pyannote)

[pyannote](https://huggingface.co/pyannote)

/

[speaker-diarization-community-1](https://huggingface.co/pyannote/speaker-diarization-community-1) 

![Figure](figures/07a9ac634e1a96dd6ff40ce3bdd22b6a595310c74c06d36a87b39b1d3b4518aa.svg)

 



![Figure](figures/1d34aae489280b7fcf11922ed70c861f512549bbdbaabcbd1dafda870a8ad023.svg)

 Like 2.38k

Follow



![Figure](figures/1c41836c10c63df063fa76ae31053dce6c6ae058955f6d20376d0f9a6f1714e0.webp)

 pyannote 3.34k

[ 

![Figure](figures/ac1f9e8b8d1b96ca79347eabd7835962ec00bcf3a94d8f151d7188655bee0c5e.svg)

  Automatic Speech Recognition ](https://huggingface.co/models?pipeline_tag=automatic-speech-recognition)[ pyannote.audio ](https://huggingface.co/models?library=pyannote-audio)[ pyannote ](https://huggingface.co/models?other=pyannote)[ pyannote-audio-pipeline ](https://huggingface.co/models?other=pyannote-audio-pipeline)[ audio ](https://huggingface.co/models?other=audio)[ voice ](https://huggingface.co/models?other=voice)[ speech ](https://huggingface.co/models?other=speech)[ speaker ](https://huggingface.co/models?other=speaker)[ speaker-diarization ](https://huggingface.co/models?other=speaker-diarization)[ speaker-change-detection ](https://huggingface.co/models?other=speaker-change-detection)[ voice-activity-detection ](https://huggingface.co/models?other=voice-activity-detection)[ overlapped-speech-detection ](https://huggingface.co/models?other=overlapped-speech-detection)



![Figure](figures/783d9fe2276038e2c7d61578e3c78fce0e24f5b33e6a7afad49fd3e5067d4987.svg)

 arxiv: 4 papers



![Figure](figures/7be4508197a645aa1244bdbd6884b2dbe36d661d009d2c18057782eb4ed857fa.svg)

 License: cc-by-4.0

[ 

![Figure](figures/3f595e0219ac3e5b1682b160dfab627869c642c69f4b94ed0360e51c34c079dc.svg)

 Model card ](https://huggingface.co/pyannote/speaker-diarization-community-1)[ 

![Figure](figures/d6a2ea6c6a9a479a26ba70e3f0990d3a51283dd5afde473547f2bfcfbcc42e1b.svg)

 Files Files and versions 

![Figure](figures/32b0f7a3114a28f6007e17cc21db1055b0f50462ef66cdbd37d1e7c0020b9822.svg)

 xet ](https://huggingface.co/pyannote/speaker-diarization-community-1/tree/main)[ 

![Figure](figures/f6fd32c5de99e81bd2a353e1000d8c0187b1ec18ead3e6feaf6adaf47e95c0be.svg)

 Community 2 ](https://huggingface.co/pyannote/speaker-diarization-community-1/discussions)



![Figure](figures/86f63e8088d1e12a50265a5402b87775fdfa4b9d84cbbdc745ab4ea5ad501037.svg)

 



![Figure](figures/3509a5e7b3681c1dff82916290dd29181fb42748ac29ab35ab5d9d5e74f38a4e.svg)

 Deploy 

![Figure](figures/30b741b99d26303bc997be0b462c076546e1f2fd82493d46bd121688fb4f11c9.svg)

 



![Figure](figures/c12b99a1b4862c5c15088fecad65b53f654827001cc81769768d36db1ea4f7ec.svg)

 Copy to bucket new



![Figure](figures/3a9b836f2274f54546ff000a4ba4c346cb1947ef6b33217b48e061c40557e4eb.svg)

 Use this model 

![Figure](figures/30b741b99d26303bc997be0b462c076546e1f2fd82493d46bd121688fb4f11c9.svg)

 

### Instructions to use pyannote/speaker-diarization-community-1 with libraries, inference providers, notebooks, and local apps. Follow these links to get started.

  * Libraries
  * [ pyannote.audio](https://huggingface.co/pyannote/speaker-diarization-community-1?library=pyannote-audio)

How to use pyannote/speaker-diarization-community-1 with pyannote.audio:
        
        from pyannote.audio import Pipeline
        
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-community-1")
        
        # inference on the whole file
        pipeline("file.wav")
        
        # inference on an excerpt
        from pyannote.core import Segment
        excerpt = Segment(start=2.0, end=5.0)
        
        from pyannote.audio import Audio
        waveform, sample_rate = Audio().crop("file.wav", excerpt)
        pipeline({"waveform": waveform, "sample_rate": sample_rate})

  * Notebooks
  * [ 

![Figure](figures/d8ae7c05abaecc3be3cedefb3cd7291d11448d6dcc896ec93ecabe43f365bea6.svg)

 Google Colab](https://huggingface.co/pyannote/speaker-diarization-community-1/colab)
  * [ 

![Figure](figures/af5b49155f346d1ac8cc42764e742e59c3719a740faa65e8d8d0a672febc6f51.svg)

 Kaggle](https://huggingface.co/pyannote/speaker-diarization-community-1/kaggle)



##  

![Figure](figures/42b2528ffd8b9ad4a657c5bd78a64063ab66ac767810cc2f7d7f7d274cbdff79.svg)

 You need to agree to share your contact information to access this model

This repository is publicly accessible, but you have to accept the conditions to access its files and content.

Your input helps us strengthen the pyannote community and improve our open-source offerings. This pipeline is released under the CC-BY-4.0 license and will always remain freely accessible. By providing your details, you agree that we may email you occasionally with important news about pyannote models, invitations to try premium pipelines, and information about specific services designed for researchers and professionals like you.

[Log in](https://huggingface.co/login?next=/pyannote/speaker-diarization-community-1) or [Sign Up](https://huggingface.co/join?next=/pyannote/speaker-diarization-community-1) to review the conditions and access this model content.



![Figure](figures/c5a4cd142448c21e120a0629055b68769b8f78b0f8c62c2bdca7203d285c4735.svg)

 

  * [`community-1` speaker diarization](https://huggingface.co/pyannote/speaker-diarization-community-1#community-1-speaker-diarization "<code>community-1</code> speaker diarization")
    * [Setup](https://huggingface.co/pyannote/speaker-diarization-community-1#setup "Setup")
    * [Quick start](https://huggingface.co/pyannote/speaker-diarization-community-1#quick-start "Quick start")
    * [Benchmark](https://huggingface.co/pyannote/speaker-diarization-community-1#benchmark "Benchmark")
    * [Processing on GPU](https://huggingface.co/pyannote/speaker-diarization-community-1#processing-on-gpu "Processing on GPU")
    * [Processing from memory](https://huggingface.co/pyannote/speaker-diarization-community-1#processing-from-memory "Processing from memory")
    * [Monitoring progress](https://huggingface.co/pyannote/speaker-diarization-community-1#monitoring-progress "Monitoring progress")
    * [Controlling the number of speakers](https://huggingface.co/pyannote/speaker-diarization-community-1#controlling-the-number-of-speakers "Controlling the number of speakers")
    * [Exclusive speaker diarization](https://huggingface.co/pyannote/speaker-diarization-community-1#exclusive-speaker-diarization "Exclusive speaker diarization")
    * [Offline use](https://huggingface.co/pyannote/speaker-diarization-community-1#offline-use "Offline use")
    * [Citations](https://huggingface.co/pyannote/speaker-diarization-community-1#citations "Citations")
    * [Acknowledgment](https://huggingface.co/pyannote/speaker-diarization-community-1#acknowledgment "Acknowledgment")



#  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/pyannote/speaker-diarization-community-1#community-1-speaker-diarization) `community-1` speaker diarization 

This pipeline ingests mono audio sampled at 16kHz and outputs speaker diarization.

  * stereo or multi-channel audio files are automatically downmixed to mono by averaging the channels.
  * audio files sampled at a different rate are resampled to 16kHz automatically upon loading.



The [main improvements brought by `Community-1`](https://www.pyannote.ai/blog/community-1) are:

  * [improved](https://huggingface.co/pyannote/speaker-diarization-community-1#benchmark) speaker assignment and counting
  * simpler reconciliation with transcription timestamps with [_exclusive_](https://huggingface.co/pyannote/speaker-diarization-community-1#exclusive-speaker-diarization) speaker diarization
  * easy [offline use](https://huggingface.co/pyannote/speaker-diarization-community-1#offline-use) (i.e. without internet connection)
  * (optionally) [hosted](https://hf.co/pyannote/speaker-diarization-community-1-cloud) on pyannoteAI cloud



##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/pyannote/speaker-diarization-community-1#setup) Setup 

  1. `pip install pyannote.audio`
  2. Accept user conditions
  3. Create access token at [`hf.co/settings/tokens`](https://hf.co/settings/tokens).



##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/pyannote/speaker-diarization-community-1#quick-start) Quick start 
    
    
    # download the pipeline from Huggingface
    from pyannote.audio import Pipeline
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-community-1", 
        token="{huggingface-token}")
    
    # run the pipeline locally on your computer
    output = pipeline("audio.wav")
    
    # print the predicted speaker diarization 
    for turn, speaker in output.speaker_diarization:
        print(f"{speaker} speaks between t={turn.start:.3f}s and t={turn.end:.3f}s")
    

##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/pyannote/speaker-diarization-community-1#benchmark) Benchmark 

Out of the box, `Community-1` is much better than `speaker-diarization-3.1`. 

We report [diarization error rates](http://pyannote.github.io/pyannote-metrics/reference.html#diarization) (in %) on large collection of academic benchmarks (fully automatic processing, no forgiveness collar, nor skipping overlapping speech).



Benchmark (last updated in 2025-09) | [`legacy` (3.1)](https://hf.co/pyannote/speaker-diarization-3.1) | [`community-1`](https://www.pyannote.ai/blog/community-1) | [`precision-2`](https://www.pyannote.ai/blog/precision-2)  
---|---|---|---  
[AISHELL-4](https://arxiv.org/abs/2104.03603) | 12.2 | 11.7 | 11.4  
[AliMeeting](https://www.openslr.org/119/) (channel 1) | 24.5 | 20.3 | 15.2  
[AMI](https://groups.inf.ed.ac.uk/ami/corpus/) (IHM) | 18.8 | 17.0 | 12.9  
[AMI](https://groups.inf.ed.ac.uk/ami/corpus/) (SDM) | 22.7 | 19.9 | 15.6  
[AVA-AVD](https://arxiv.org/abs/2111.14448) | 49.7 | 44.6 | 37.1  
[CALLHOME](https://catalog.ldc.upenn.edu/LDC2001S97) ([part 2](https://github.com/BUTSpeechFIT/CALLHOME_sublists/issues/1)) | 28.5 | 26.7 | 16.6  
[DIHARD 3](https://catalog.ldc.upenn.edu/LDC2022S14) ([full](https://arxiv.org/abs/2012.01477)) | 21.4 | 20.2 | 14.7  
[Ego4D](https://arxiv.org/abs/2110.07058) (dev.) | 51.2 | 46.8 | 39.0  
[MSDWild](https://github.com/X-LANCE/MSDWILD) | 25.4 | 22.8 | 17.3  
[RAMC](https://www.openslr.org/123/) | 22.2 | 20.8 | 10.5  
[REPERE](https://www.islrn.org/resources/360-758-359-485-0/) (phase2) | 7.9 | 8.9 | 7.4  
[VoxConverse](https://github.com/joonson/voxconverse) (v0.3) | 11.2 | 11.2 | 8.5

 

`Precision-2` model is even better and can be tested like this:

  1. Create an API key on [pyannoteAI dashboard](https://huggingface.co/pyannote/speaker-diarization-community-1/blob/main/\(https://dashboard.pyannote.ai\)) (free credits included)
  2. Change one line of code


    
    
    from pyannote.audio import Pipeline
    pipeline = Pipeline.from_pretrained(
    -     'pyannote/speaker-diarization-community-1', token="{huggingface-token}")
    +     'pyannote/speaker-diarization-precision-2', token="{pyannoteAI-api-key}")
    diarization = pipeline("audio.wav")  # runs on pyannoteAI servers
    

##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/pyannote/speaker-diarization-community-1#processing-on-gpu) Processing on GPU 

`pyannote.audio` pipelines run on CPU by default. You can send them to GPU with the following lines:
    
    
    import torch
    pipeline.to(torch.device("cuda"))
    

##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/pyannote/speaker-diarization-community-1#processing-from-memory) Processing from memory 

Pre-loading audio files in memory may result in faster processing:
    
    
    waveform, sample_rate = torchaudio.load("audio.wav")
    output = pipeline({"waveform": waveform, "sample_rate": sample_rate})
    

##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/pyannote/speaker-diarization-community-1#monitoring-progress) Monitoring progress 

Hooks are available to monitor the progress of the pipeline:
    
    
    from pyannote.audio.pipelines.utils.hook import ProgressHook
    with ProgressHook() as hook:
        output = pipeline("audio.wav", hook=hook)
    

##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/pyannote/speaker-diarization-community-1#controlling-the-number-of-speakers) Controlling the number of speakers 

In case the number of speakers is known in advance, one can use the `num_speakers` option:
    
    
    output = pipeline("audio.wav", num_speakers=2)
    

One can also provide lower and/or upper bounds on the number of speakers using `min_speakers` and `max_speakers` options:
    
    
    output = pipeline("audio.wav", min_speakers=2, max_speakers=5)
    

##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/pyannote/speaker-diarization-community-1#exclusive-speaker-diarization) Exclusive speaker diarization 

`Community-1` pretrained pipeline returns a new _exclusive_ speaker diarization, on top of the regular speaker diarization, available as `output.exclusive_speaker_diarization`.

This is a feature which is [backported from our latest commercial model](https://www.pyannote.ai/blog/precision-2) that simplifies the reconciliation between fine-grained speaker diarization timestamps and (sometimes not so precise) transcription timestamps.

##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/pyannote/speaker-diarization-community-1#offline-use) Offline use 

  1. In the terminal, copy the pipeline on disk:


    
    
    # make sure git-lfs is installed (https://git-lfs.com)
    git lfs install
    
    # create a directory on disk
    mkdir /path/to/directory
    
    # when prompted for a password, use an access token with write permissions.
    # generate one from your settings: https://huggingface.co/settings/tokens
    git clone https://hf.co/pyannote/speaker-diarization-community-1 /path/to/directory/pyannote-speaker-diarization-community-1
    

  2. In Python, use the pipeline without internet connection:


    
    
    # load pipeline from disk (works without internet connection)
    from pyannote.audio import Pipeline
    pipeline = Pipeline.from_pretrained('/path/to/directory/pyannote-speaker-diarization-community-1')
    
    # run the pipeline locally on your computer
    output = pipeline("audio.wav")
    

##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/pyannote/speaker-diarization-community-1#citations) Citations 

  1. Speaker segmentation model


    
    
    @inproceedings{Plaquet23,
      author={Alexis Plaquet and Hervé Bredin},
      title={{Powerset multi-class cross entropy loss for neural speaker diarization}},
      year=2023,
      booktitle={Proc. INTERSPEECH 2023},
    }
    

  2. Speaker embedding model


    
    
    @inproceedings{Wang2023,
      title={Wespeaker: A research and production oriented speaker embedding learning toolkit},
      author={Wang, Hongji and Liang, Chengdong and Wang, Shuai and Chen, Zhengyang and Zhang, Binbin and Xiang, Xu and Deng, Yanlei and Qian, Yanmin},
      booktitle={ICASSP 2023, IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
      pages={1--5},
      year={2023},
      organization={IEEE}
    }
    

  3. Speaker clustering


    
    
    @article{Landini2022,
      author={Landini, Federico and Profant, J{\'a}n and Diez, Mireia and Burget, Luk{\'a}{\v{s}}},
      title={{Bayesian HMM clustering of x-vector sequences (VBx) in speaker diarization: theory, implementation and analysis on standard tasks}},
      year={2022},
      journal={Computer Speech \& Language},
    }
    

##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/pyannote/speaker-diarization-community-1#acknowledgment) Acknowledgment 

Training and tuning made possible thanks to [GENCI](https://www.genci.fr/) on the [**Jean Zay**](http://www.idris.fr/eng/jean-zay/) supercomputer.

Downloads last month
    5,503,362



![Figure](figures/190a26f4855997e2e9bd0b10d3f5c84587187ec602a6ccafe38da76147bd3e48.svg)

 



![Figure](figures/88a0c55f81e54aecdc2e32cfd0ea74f7ba732d9ac318471c3a072f0ffa5e802f.svg)

 Inference Providers [NEW](https://huggingface.co/docs/inference-providers)

[ 

![Figure](figures/f7525803db9c647455a9d75089a8b07577df55953fe1d3558076b629fdaf5877.svg)

 Automatic Speech Recognition](https://huggingface.co/tasks/automatic-speech-recognition "Learn more about automatic-speech-recognition")

This model isn't deployed by any Inference Provider. [🙋 1 Ask for provider support](https://huggingface.co/spaces/huggingface/InferenceSupport/discussions/5851)

##  

![Figure](figures/8e5d2a5c20093da01233396edf241924bda6fc86f2dfada0fcdd62e567d1c8b9.svg)

 Model tree for pyannote/speaker-diarization-community-1 [ 

![Figure](figures/94a838574fc5d31445cc43e46e6e864df88a9d16397513b44527885b440124e9.svg)

 ](https://huggingface.co/docs/hub/model-cards#specifying-a-base-model)



![Figure](figures/f7edc8bdbacd02e9e60c07e4804c8915b8949c49a250b139adc1858c65958732.svg)

 

Finetunes

[9 models](https://huggingface.co/models?other=base_model:finetune:pyannote/speaker-diarization-community-1)



![Figure](figures/f7edc8bdbacd02e9e60c07e4804c8915b8949c49a250b139adc1858c65958732.svg)

 

Quantizations

[6 models](https://huggingface.co/models?other=base_model:quantized:pyannote/speaker-diarization-community-1)

##  

![Figure](figures/cf0c597a2dd54b4f2eb17326a437cce0dd2cf1606a941ea8b71b258a2df75585.svg)

 Spaces using pyannote/speaker-diarization-community-1 49

[🟩 embedl/hfviewer ](https://huggingface.co/spaces/embedl/hfviewer)[📚 luckyhookin/speaker-diarization ](https://huggingface.co/spaces/luckyhookin/speaker-diarization)[🎙️ RIDA23555855858/Duplex ](https://huggingface.co/spaces/RIDA23555855858/Duplex)[💻 Kquan/SD ](https://huggingface.co/spaces/Kquan/SD)[🐠 pratyushmittal/diarize ](https://huggingface.co/spaces/pratyushmittal/diarize)[🎙️ shee1234/voice-test-lab-pyannote ](https://huggingface.co/spaces/shee1234/voice-test-lab-pyannote)[🎙️ Subham05x/meetpilot-whisper-diarization ](https://huggingface.co/spaces/Subham05x/meetpilot-whisper-diarization)[🔥 anbdullah128364/dubora-speaker-diarization ](https://huggingface.co/spaces/anbdullah128364/dubora-speaker-diarization) \+ 44 Spaces \+ 41 Spaces

##  

![Figure](figures/2f4a8b12047b3c323726865192fa13fea5ec28ca9f1716004655db477527e8e5.svg)

 Collection including pyannote/speaker-diarization-community-1

#### [Latest 

![Figure](figures/388c393561ffda49cfb6f6d8be429a7da3a0a97509cbb414e19c254145e26d90.svg)

 Collection Compatible with pyannote.audio 4.x • 4 items • Updated Sep 26, 2025 • 

![Figure](figures/26079970d7c967ac733cd8827a6a5b861feb37fd9cdfa4c7ff6e2a603f3a60d6.svg)

 8](https://huggingface.co/collections/pyannote/latest)

##  

![Figure](figures/b844e37eb6c73155067655f28a5ae438131c4a2fb60fb4c5594a3a2e4bbbae18.svg)

 Papers for pyannote/speaker-diarization-community-1

#### [AVA-AVD: Audio-Visual Speaker Diarization in the Wild 

![Figure](figures/76a94b593dca78642338990eb26c1d3d8f949cea5947d43e6c5d764a627c4688.svg)

 Paper • 2111.14448 • Published Nov 29, 2021 • 

![Figure](figures/26079970d7c967ac733cd8827a6a5b861feb37fd9cdfa4c7ff6e2a603f3a60d6.svg)

 1 ](https://huggingface.co/papers/2111.14448)#### [Ego4D: Around the World in 3,000 Hours of Egocentric Video 

![Figure](figures/76a94b593dca78642338990eb26c1d3d8f949cea5947d43e6c5d764a627c4688.svg)

 Paper • 2110.07058 • Published Oct 13, 2021 • 

![Figure](figures/26079970d7c967ac733cd8827a6a5b861feb37fd9cdfa4c7ff6e2a603f3a60d6.svg)

 1 ](https://huggingface.co/papers/2110.07058)#### [AISHELL-4: An Open Source Dataset for Speech Enhancement, Separation, Recognition and Speaker Diarization in Conference Scenario 

![Figure](figures/76a94b593dca78642338990eb26c1d3d8f949cea5947d43e6c5d764a627c4688.svg)

 Paper • 2104.03603 • Published Apr 8, 2021 ](https://huggingface.co/papers/2104.03603)#### [The Third DIHARD Diarization Challenge 

![Figure](figures/76a94b593dca78642338990eb26c1d3d8f949cea5947d43e6c5d764a627c4688.svg)

 Paper • 2012.01477 • Published Dec 2, 2020 • 

![Figure](figures/26079970d7c967ac733cd8827a6a5b861feb37fd9cdfa4c7ff6e2a603f3a60d6.svg)

 1 ](https://huggingface.co/papers/2012.01477)
