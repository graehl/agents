**Source:** *Multilingual LibriSpeech (MLS)* — [original page](https://www.openslr.org/94/)

## Open Speech and Language Resources

* * *

[Home](https://www.openslr.org/index.html) [Resources](https://www.openslr.org/resources.php)

* * *

##  Multilingual LibriSpeech (MLS) 

**Identifier:** SLR94 

**Summary:** A large multilingual corpus derived from LibriVox audiobooks 

**Category:** Speech 

**License:** CC BY 4.0 

**About this resource:**

### NOTE: The data is not hosted on OpenSLR (due to it's size) -- please use the links provided below to download. 

Multilingual LibriSpeech (MLS) dataset is a large multilingual corpus suitable for speech research. The dataset is derived from read audiobooks from LibriVox and consists of 8 languages - English, German, Dutch, Spanish, French, Italian, Portuguese, Polish.

###  ASR Resources

Consists of train, dev and test sets for each language. Also, includes small training set for limited supervision (10hr, 1hr or 10 minutes of labelled speech). 



Language | Download Link   
(Original: flac) | Download Link   
(Compressed: opus)  
---|---|---  
English * | [mls_english.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_english.tar.gz) (2.4T) | [mls_english_opus.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_english_opus.tar.gz) (651G)  
German | [mls_german.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_german.tar.gz) (115G)  | [mls_german_opus.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_german_opus.tar.gz) (29G)   
Dutch | [mls_dutch.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_dutch.tar.gz) (86G)  | [mls_dutch_opus.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_dutch_opus.tar.gz) (23G)   
French | [mls_french.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_french.tar.gz) (61G)  | [mls_french_opus.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_french_opus.tar.gz) (16G)   
Spanish | [mls_spanish.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_spanish.tar.gz) (50G)  | [mls_spanish_opus.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_spanish_opus.tar.gz) (14G)   
Italian | [mls_italian.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_italian.tar.gz) (15G)  | [mls_italian_opus.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_italian_opus.tar.gz) (3.8G)   
Portuguese | [mls_portuguese.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_portuguese.tar.gz) (9.3G)  | [mls_portuguese_opus.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_portuguese_opus.tar.gz) (2.5G)   
Polish | [mls_polish.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_polish.tar.gz) (6.2G)  | [mls_polish_opus.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_polish_opus.tar.gz) (1.6G)

 

###  LM Resources 

Consists of language modelling corpus and pre-trained 3-gram and 5-gram LMs.



Language | Download Link  
---|---  
English | [mls_lm_english.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_lm_english.tar.gz) (44G)   
German | [mls_lm_german.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_lm_german.tar.gz) (2.7G)   
Dutch | [mls_lm_dutch.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_lm_dutch.tar.gz) (1.4G)   
French | [mls_lm_french.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_lm_french.tar.gz) (4.8G)   
Spanish | [mls_lm_spanish.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_lm_spanish.tar.gz) (1.2G)   
Italian | [mls_lm_italian.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_lm_italian.tar.gz) (1.7G)   
Portuguese | [mls_lm_portuguese.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_lm_portuguese.tar.gz) (558M)   
Polish | [mls_lm_polish.tar.gz](https://dl.fbaipublicfiles.com/mls/mls_lm_polish.tar.gz) (30M)

 

###  Other Resources 



About | Download Link  
---|---  
Downloaded text from LibriVox books | [lv_text.tar.gz](https://dl.fbaipublicfiles.com/mls/lv_text.tar.gz) (2.0G)   
Unrated dev/test transcripts (before human rating)  | [unrated_transcripts.tar.gz](https://dl.fbaipublicfiles.com/mls/unrated_transcripts.tar.gz) (2.8M)

 

### MD5 Checksums

[md5sum.txt](https://dl.fbaipublicfiles.com/mls/md5sum.txt)

All the above links are hosted AWS S3 bucket and can be downloaded using [AWS CLI](https://aws.amazon.com/cli/) tools as well. For downloading using AWS CLI tools, create an AWS account, put the credentials in the CLI tools and all the resources can be downloaded for free. To get the S3 bucket path of an URL, replace `https://dl.fbaipublicfiles.com/` with `s3://dl.fbaipublicfiles.com/`. For example, the S3 bucket path of URL `https://dl.fbaipublicfiles.com/mls/mls_polish.tar.gz` is `s3://dl.fbaipublicfiles.com/mls/mls_polish.tar.gz`.

More details on these files and their directory structure can be found in README files included in the .tar.gz files.

You can cite the data using the following BibTeX entry:
    
    
    @article{Pratap2020MLSAL,
      title={MLS: A Large-Scale Multilingual Dataset for Speech Research},
      author={Vineel Pratap and Qiantong Xu and Anuroop Sriram and Gabriel Synnaeve and Ronan Collobert},
      journal={ArXiv},
      year={2020},
      volume={abs/2012.03411}
    }
    

NOTE: We have made few updates to the MLS dataset after our [INTERSPEECH paper](https://www.isca-speech.org/archive/Interspeech_2020/pdfs/2826.pdf) was submitted to include more #hours and also improve the quality of transcripts. To avoid confusion (by having multiple versions), we are making ONLY one release with all the improvements included. For accurate dataset statistics and baselines, please refer to the arXiv paper - <https://arxiv.org/abs/2012.03411>.

* This resource can also be downloaded in parts from the 100GB splits - [mls_english_parts_list.txt](https://dl.fbaipublicfiles.com/mls/mls_english_parts_list.txt) and [mls_english_opus_parts_list.txt](https://dl.fbaipublicfiles.com/mls/mls_english_opus_parts_list.txt) for the original and compressed versions respectively. After downloading all the splits, run `cat` on the files to create a single tar file and verify the md5 checksum. 

[ 

![Valid CSS!](figures/0fe93e42ec6c8f15d9913390e07d7db520f8c0139850417cdaaaa8b5ce840c83.png)

 ](https://jigsaw.w3.org/css-validator/check/referer)
