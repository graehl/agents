**Source:** *YODAS2 dataset card* — [original page](https://huggingface.co/datasets/espnet/yodas2)

# [ 

![Figure](figures/6e84735dc2174682d7471b1c566ec277a5a95273ba97c0ca76f1a9524d7d8e15.svg)

 Datasets:](https://huggingface.co/datasets)

* * *

[ 

![Figure](figures/460f42f792a3006089fc2c979b95886c4e17a04f3ff17c8298005d55b55a2825.webp)

 ](https://huggingface.co/espnet)

[espnet](https://huggingface.co/espnet)

/

[yodas2](https://huggingface.co/datasets/espnet/yodas2) 

![Figure](figures/07a9ac634e1a96dd6ff40ce3bdd22b6a595310c74c06d36a87b39b1d3b4518aa.svg)

 



![Figure](figures/1d34aae489280b7fcf11922ed70c861f512549bbdbaabcbd1dafda870a8ad023.svg)

 Like 56

Follow



![Figure](figures/460f42f792a3006089fc2c979b95886c4e17a04f3ff17c8298005d55b55a2825.webp)

 ESPnet 400

ArXiv:



![Figure](figures/783d9fe2276038e2c7d61578e3c78fce0e24f5b33e6a7afad49fd3e5067d4987.svg)

 arxiv: 2406.00899

License:



![Figure](figures/7be4508197a645aa1244bdbd6884b2dbe36d661d009d2c18057782eb4ed857fa.svg)

 cc-by-3.0

[ 

![Figure](figures/3f595e0219ac3e5b1682b160dfab627869c642c69f4b94ed0360e51c34c079dc.svg)

 Dataset card ](https://huggingface.co/datasets/espnet/yodas2)[ 

![Figure](figures/d6a2ea6c6a9a479a26ba70e3f0990d3a51283dd5afde473547f2bfcfbcc42e1b.svg)

 Files Files and versions 

![Figure](figures/32b0f7a3114a28f6007e17cc21db1055b0f50462ef66cdbd37d1e7c0020b9822.svg)

 xet ](https://huggingface.co/datasets/espnet/yodas2/tree/main)[ 

![Figure](figures/f6fd32c5de99e81bd2a353e1000d8c0187b1ec18ead3e6feaf6adaf47e95c0be.svg)

 Community 6 ](https://huggingface.co/datasets/espnet/yodas2/discussions)



![Figure](figures/16e0932d88719e86e12a774c8912c254944795b53b81dd481c5e61a2b6309590.svg)

 

Dataset Viewer

The viewer is disabled because this dataset repo requires arbitrary Python code execution. Please consider removing the [loading script](https://huggingface.co/docs/datasets/dataset_script) and relying on [automated data support](https://huggingface.co/docs/datasets/repository_structure) (you can use [`convert_to_parquet`](https://huggingface.co/docs/datasets/main/en/cli#convert-to-parquet) from the `datasets` library). If this is not possible, please [open a discussion](https://huggingface.co/datasets/espnet/yodas2/discussions/new?title=Dataset+Viewer+issue%3A+DatasetWithScriptNotSupportedError&description=The+dataset+viewer+is+not+working.%0A%0AError+details%3A%0A%0A%60%60%60%0AError+code%3A+++DatasetWithScriptNotSupportedError%0A%0A%60%60%60%0A%0A%0A---%0A%0A%F0%9F%91%8B+Before+opening+the+discussion%2C+have+you+considered+removing+the+%5Bloading+script%5D%28https%3A%2F%2Fhuggingface.co%2Fdocs%2Fdatasets%2Fdataset_script%29+and+relying+on+%5Bautomated+data+support%5D%28https%3A%2F%2Fhuggingface.co%2Fdocs%2Fdatasets%2Frepository_structure%29%3F%0A%0AYou+can+use+%5Bconvert_to_parquet%5D%28https%3A%2F%2Fhuggingface.co%2Fdocs%2Fdatasets%2Fmain%2Fen%2Fcli%23convert-to-parquet%29+from+the+datasets+library.%0A%0A---%0A%0A%0Acc+%40lhoestq+%40cfahlgren1.) for direct help.



![Figure](figures/c5a4cd142448c21e120a0629055b68769b8f78b0f8c62c2bdca7203d285c4735.svg)

 

  * [Usage:](https://huggingface.co/datasets/espnet/yodas2#usage "Usage:")
  * [Reference](https://huggingface.co/datasets/espnet/yodas2#reference "Reference")
  * [Contact](https://huggingface.co/datasets/espnet/yodas2#contact "Contact")



YODAS2 is the long-form dataset from YODAS dataset.

It provides the same dataset as [espnet/yodas](https://huggingface.co/datasets/espnet/yodas) but YODAS2 has the following new features:

  * formatted in the long-form (video-level) where audios are not segmented.
  * audios are encoded using higher sampling rates (i.e. 24k)



For detailed information about YODAS dataset, please refer to [our paper](https://arxiv.org/abs/2406.00899) and the [espnet/yodas repo](https://huggingface.co/datasets/espnet/yodas).

##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/datasets/espnet/yodas2#usage) Usage: 

Each data point corresponds to an entire video on YouTube, it contains the following fields:

  * video_id: unique id of this video (note this id is not the video_id in Youtube)
  * duration: total duration in seconds of this video
  * audio
    * path: local path to wav file if in standard mode, otherwise empty in the streaming mode
    * sampling_rate: fixed to be 24k. (note that the sampling rate in `espnet/yodas` is 16k)
    * array: wav samples in float
  * utterances
    * utt_id: unique id of this utterance
    * text: transcription of this utterance
    * start: start timestamp in seconds of this utterance
    * end: end timestamp in seconds of this utterance



YODAS2 also supports two modes:

**standard mode** : each subset will be downloaded to the local dish before first iterating. 
    
    
    from datasets import load_dataset
    
    # Note this will take very long time to download and preprocess
    # you can try small subset for testing purpose
    ds = load_dataset('espnet/yodas2', 'en000')
    print(next(iter(ds['train'])))
    

**streaming mode** most of the files will be streamed instead of downloaded to your local deivce. It can be used to inspect this dataset quickly.
    
    
    from datasets import load_dataset
    
    # this streaming loading will finish quickly
    ds = load_dataset('espnet/yodas2', 'en000', streaming=True)
    

##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/datasets/espnet/yodas2#reference) Reference 
    
    
    @inproceedings{li2023yodas,
      title={Yodas: Youtube-Oriented Dataset for Audio and Speech},
      author={Li, Xinjian and Takamichi, Shinnosuke and Saeki, Takaaki and Chen, William and Shiota, Sayaka and Watanabe, Shinji},
      booktitle={2023 IEEE Automatic Speech Recognition and Understanding Workshop (ASRU)},
      pages={1--8},
      year={2023},
      organization={IEEE}
    }
    

##  [ 

![Figure](figures/ba980fc624d853fc90c0b1f8dbc4815a144c0750f9d72a12561d37a6f29340a0.svg)

  ](https://huggingface.co/datasets/espnet/yodas2#contact) Contact 

If you have any questions, feel free to contact us at the following email address.

We made sure that our dataset only consisted of videos with CC licenses during our downloading. But in case you find your video unintentionally included in our dataset and would like to delete it, you can send a delete request to the following email.

Remove the parenthesis `()` from the following email address

`(lixinjian)(1217)@gmail.com`



![Figure](figures/c12b99a1b4862c5c15088fecad65b53f654827001cc81769768d36db1ea4f7ec.svg)

 Copy to bucket new



![Figure](figures/86f63e8088d1e12a50265a5402b87775fdfa4b9d84cbbdc745ab4ea5ad501037.svg)

 

Downloads last month

    55,021

Total file size: 60.3 TB

##  

![Figure](figures/e367a551eb0ac45b9da80492a7170ad99330408186f4327fb5e62f70b8378f1a.svg)

 Models trained or fine-tuned on espnet/yodas2

[ 

![Figure](figures/05c8996c7c4aa5ddd6bc4dd5b14dd40afe814588a627acaf7cd65b981961a16e.webp)

  Yehor/hubert-uk 

![Figure](figures/6b531bb3f60c75fdcab79814ce11a90a158801700cb4f300c0f57d29a3b3b1dc.svg)

 Automatic Speech Recognition • 

![Figure](figures/c894b0ae6fd8878e1c803716e0d0f91f08ee0e514a577358cfba51c771e0a019.svg)

 94.4M • Updated Feb 20, 2025 • 

![Figure](figures/63e0c729edd16ef536e70938ddb72e68aef5c45566718fc90a1b35ea440ca8de.svg)

 43 • 

![Figure](figures/1b338c3b145e14c24add2036647ac1a7e89bf8235f21828fa433313382c5bf73.svg)

 4  ](https://huggingface.co/Yehor/hubert-uk)

[ 

![Figure](figures/078ddc4ca252c371f10b85f4d34172fba27c2a70be14768ab964f909e37598ce.webp)

  anak10thn/whisper-small-id 

![Figure](figures/6b531bb3f60c75fdcab79814ce11a90a158801700cb4f300c0f57d29a3b3b1dc.svg)

 Automatic Speech Recognition • 

![Figure](figures/c894b0ae6fd8878e1c803716e0d0f91f08ee0e514a577358cfba51c771e0a019.svg)

 0.2B • Updated about 20 hours ago • 

![Figure](figures/63e0c729edd16ef536e70938ddb72e68aef5c45566718fc90a1b35ea440ca8de.svg)

 4  ](https://huggingface.co/anak10thn/whisper-small-id)

[ 

![Figure](figures/a2fa8e16b609eab720367dd119488c5d80ef32b02336034e65229e438d07b407.svg)

  spacewave/sherpa-onnx-streaming-zipformer2-id 

![Figure](figures/6b531bb3f60c75fdcab79814ce11a90a158801700cb4f300c0f57d29a3b3b1dc.svg)

 Automatic Speech Recognition • Updated Nov 22, 2025 ](https://huggingface.co/spacewave/sherpa-onnx-streaming-zipformer2-id)

##  

![Figure](figures/b844e37eb6c73155067655f28a5ae438131c4a2fb60fb4c5594a3a2e4bbbae18.svg)

 Paper for espnet/yodas2

#### [YODAS: Youtube-Oriented Dataset for Audio and Speech 

![Figure](figures/76a94b593dca78642338990eb26c1d3d8f949cea5947d43e6c5d764a627c4688.svg)

 Paper • 2406.00899 • Published Jun 2, 2024 • 

![Figure](figures/26079970d7c967ac733cd8827a6a5b861feb37fd9cdfa4c7ff6e2a603f3a60d6.svg)

 5 ](https://huggingface.co/papers/2406.00899)

##  

![Figure](figures/8a37967530c7a8268f9997952affeba2221a259a4e1108f1538c0de2e188e52f.svg)

 Article mentioning espnet/yodas2

#### [YODAS v3: A 1 Million Hour Dataset for the Next Generation of Open Voice AI Research 

  * 

![Figure](figures/460f42f792a3006089fc2c979b95886c4e17a04f3ff17c8298005d55b55a2825.webp)

 
  * 
espnet • 4 days ago • 

![Figure](figures/26079970d7c967ac733cd8827a6a5b861feb37fd9cdfa4c7ff6e2a603f3a60d6.svg)

 26](https://huggingface.co/blog/espnet/yodasv3)
