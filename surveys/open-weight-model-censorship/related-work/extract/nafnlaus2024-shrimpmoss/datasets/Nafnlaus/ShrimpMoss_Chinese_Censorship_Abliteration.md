**Source:** *ShrimpMoss_Chinese_Censorship_Abliteration (dataset card)* — [original page](https://huggingface.co/datasets/Nafnlaus/ShrimpMoss_Chinese_Censorship_Abliteration)

# [ 

![Figure](figures/6e84735dc2174682d7471b1c566ec277a5a95273ba97c0ca76f1a9524d7d8e15.svg)

 Datasets:](https://huggingface.co/datasets)

* * *

[ 

![Figure](figures/42c4e0dbd24c790c9ad86ba2744f76c4f835262891bec156f74120a1cdc4b91c.webp)

 ](https://huggingface.co/Nafnlaus)

[Nafnlaus](https://huggingface.co/Nafnlaus)

/

[ShrimpMoss_Chinese_Censorship_Abliteration](https://huggingface.co/datasets/Nafnlaus/ShrimpMoss_Chinese_Censorship_Abliteration) 

![Figure](figures/07a9ac634e1a96dd6ff40ce3bdd22b6a595310c74c06d36a87b39b1d3b4518aa.svg)

 



![Figure](figures/1d34aae489280b7fcf11922ed70c861f512549bbdbaabcbd1dafda870a8ad023.svg)

 Like 8

Modalities: [ 

![Figure](figures/fc2f0f6240fb80fac4c10e0df813562c3502daf2f143eea18bbcca0d15907950.svg)

 Text ](https://huggingface.co/datasets?modality=modality%3Atext)

Languages: [ 

![Figure](figures/ae99d3c5b43856225d2991096ca2c860d325ea47bde8ec4178fdb01f16a96896.svg)

 English ](https://huggingface.co/datasets?language=language%3Aen)[ 

![Figure](figures/ae99d3c5b43856225d2991096ca2c860d325ea47bde8ec4178fdb01f16a96896.svg)

 Chinese ](https://huggingface.co/datasets?language=language%3Azh)

Size: [ 1K<n<10K ](https://huggingface.co/datasets?size_categories=size_categories%3A1K%3Cn%3C10K)

Tags: [ legal ](https://huggingface.co/datasets?other=legal)

License:



![Figure](figures/7be4508197a645aa1244bdbd6884b2dbe36d661d009d2c18057782eb4ed857fa.svg)

 mit

[ 

![Figure](figures/3f595e0219ac3e5b1682b160dfab627869c642c69f4b94ed0360e51c34c079dc.svg)

 Dataset card ](https://huggingface.co/datasets/Nafnlaus/ShrimpMoss_Chinese_Censorship_Abliteration)[ 

![Figure](figures/4c98cdac2ee91e83856285fb869b29b44542bcedb1bee82472a4f7aae80b639a.svg)

 Data Studio ](https://huggingface.co/datasets/Nafnlaus/ShrimpMoss_Chinese_Censorship_Abliteration/viewer/)[ 

![Figure](figures/d6a2ea6c6a9a479a26ba70e3f0990d3a51283dd5afde473547f2bfcfbcc42e1b.svg)

 Files Files and versions 

![Figure](figures/32b0f7a3114a28f6007e17cc21db1055b0f50462ef66cdbd37d1e7c0020b9822.svg)

 xet ](https://huggingface.co/datasets/Nafnlaus/ShrimpMoss_Chinese_Censorship_Abliteration/tree/main)[ 

![Figure](figures/f6fd32c5de99e81bd2a353e1000d8c0187b1ec18ead3e6feaf6adaf47e95c0be.svg)

 Community 2 ](https://huggingface.co/datasets/Nafnlaus/ShrimpMoss_Chinese_Censorship_Abliteration/discussions)



![Figure](figures/9ec22a3f754ed48a39a323063adc324ec3f6be32b9939827bb78b1edf8c36951.svg)

 

Dataset Preview



![Figure](figures/b68a32812788568bb51584e9bb9a313bf50e1558a15011da5bb2058dfc250c89.svg)

 



![Figure](figures/5112735d370ca0cdd61b1c59f0fd8b21ca3da175d9f967706555aedebe478254.svg)

 API 

![Figure](figures/20b72353041e58d9a865c5a4a1799be365047024ae25673abd2a2a438adef81c.svg)

 Embed [ 

![Figure](figures/48ea14ece901d8bb657330a908c805b3a010c7a993fbd67686f32bd51afac718.svg)

 Duplicate](https://huggingface.co/datasets/Nafnlaus/ShrimpMoss_Chinese_Censorship_Abliteration?duplicate=true) 

![Figure](figures/c0ece3c0fb434bae215dced116853f1648c46afd84f76bf120f30444fd975a2e.svg)

 Data Studio

Subset (1)

default 

![Figure](figures/a8fc780bec4fa870fbea9578762108de74f0c95833fdcb10f59b685a61c1ddac.svg)

 

default

Split (1)

train 

![Figure](figures/a8fc780bec4fa870fbea9578762108de74f0c95833fdcb10f59b685a61c1ddac.svg)

 

train

The full dataset viewer is not available (click to read why). Only showing a preview of the rows.

The dataset generation failed because of a cast error
    
    
    Error code:   DatasetGenerationCastError
    Exception:    DatasetGenerationCastError
    Message:      An error occurred while generating the dataset
    
    All the data files must have the same columns, but at some point there are 2 new columns ({'instruction', 'category'}) and 1 missing columns ({'text'}).
    
    This happened while the json dataset builder was generating data using
    
    hf://datasets/Nafnlaus/ShrimpMoss_Chinese_Censorship_Abliteration/china_bad_10000.json (at revision 60626961d76ed0a39256120494061bc58510b263)
    
    Please either edit the data files to have matching columns, or separate them into different configurations (see docs at https://hf.co/docs/hub/datasets-manual-configuration#multiple-configurations)
    Traceback:    Traceback (most recent call last):
                    File "/src/services/worker/.venv/lib/python3.9/site-packages/datasets/builder.py", line 1870, in _prepare_split_single
                      writer.write_table(table)
                    File "/src/services/worker/.venv/lib/python3.9/site-packages/datasets/arrow_writer.py", line 622, in write_table
                      pa_table = table_cast(pa_table, self._schema)
                    File "/src/services/worker/.venv/lib/python3.9/site-packages/datasets/table.py", line 2292, in table_cast
                      return cast_table_to_schema(table, schema)
                    File "/src/services/worker/.venv/lib/python3.9/site-packages/datasets/table.py", line 2240, in cast_table_to_schema
                      raise CastError(
                  datasets.table.CastError: Couldn't cast
                  instruction: string
                  category: string
                  -- schema metadata --
                  pandas: '{"index_columns": [], "column_indexes": [], "columns": [{"name":' + 331
                  to
                  {'text': Value(dtype='string', id=None)}
                  because column names don't match
                  
                  During handling of the above exception, another exception occurred:
                  
                  Traceback (most recent call last):
                    File "/src/services/worker/src/worker/job_runners/config/parquet_and_info.py", line 1420, in compute_config_parquet_and_info_response
                      parquet_operations = convert_to_parquet(builder)
                    File "/src/services/worker/src/worker/job_runners/config/parquet_and_info.py", line 1052, in convert_to_parquet
                      builder.download_and_prepare(
                    File "/src/services/worker/.venv/lib/python3.9/site-packages/datasets/builder.py", line 924, in download_and_prepare
                      self._download_and_prepare(
                    File "/src/services/worker/.venv/lib/python3.9/site-packages/datasets/builder.py", line 1000, in _download_and_prepare
                      self._prepare_split(split_generator, **prepare_split_kwargs)
                    File "/src/services/worker/.venv/lib/python3.9/site-packages/datasets/builder.py", line 1741, in _prepare_split
                      for job_id, done, content in self._prepare_split_single(
                    File "/src/services/worker/.venv/lib/python3.9/site-packages/datasets/builder.py", line 1872, in _prepare_split_single
                      raise DatasetGenerationCastError.from_cast_error(
                  datasets.exceptions.DatasetGenerationCastError: An error occurred while generating the dataset
                  
                  All the data files must have the same columns, but at some point there are 2 new columns ({'instruction', 'category'}) and 1 missing columns ({'text'}).
                  
                  This happened while the json dataset builder was generating data using
                  
                  hf://datasets/Nafnlaus/ShrimpMoss_Chinese_Censorship_Abliteration/china_bad_10000.json (at revision 60626961d76ed0a39256120494061bc58510b263)
                  
                  Please either edit the data files to have matching columns, or separate them into different configurations (see docs at https://hf.co/docs/hub/datasets-manual-configuration#multiple-configurations)

Need help to make the dataset viewer work? Make sure to review [how to configure the dataset viewer](https://huggingface.co/docs/hub/datasets-data-files-configuration), and [open a discussion](https://huggingface.co/datasets/Nafnlaus/ShrimpMoss_Chinese_Censorship_Abliteration/discussions/new?title=Dataset+Viewer+issue%3A+DatasetGenerationCastError&description=The+dataset+viewer+is+not+working.%0A%0AError+details%3A%0A%0A%60%60%60%0AError+code%3A+++DatasetGenerationCastError%0AException%3A++++DatasetGenerationCastError%0AMessage%3A++++++An+error+occurred+while+generating+the+dataset%0A%0AAll+the+data+files+must+have+the+same+columns%2C+but+at+some+point+there+are+2+new+columns+%28%7B%27instruction%27%2C+%27category%27%7D%29+and+1+missing+columns+%28%7B%27text%27%7D%29.%0A%0AThis+happened+while+the+json+dataset+builder+was+generating+data+using%0A%0Ahf%3A%2F%2Fdatasets%2FNafnlaus%2FShrimpMoss_Chinese_Censorship_Abliteration%2Fchina_bad_10000.json+%28at+revision+60626961d76ed0a39256120494061bc58510b263%29%0A%0APlease+either+edit+the+data+files+to+have+matching+columns%2C+or+separate+them+into+different+configurations+%28see+docs+at+https%3A%2F%2Fhf.co%2Fdocs%2Fhub%2Fdatasets-manual-configuration%23multiple-configurations%29%0ATraceback%3A++++Traceback+%28most+recent+call+last%29%3A%0A++++++++++++++++File+%22%2Fsrc%2Fservices%2Fworker%2F.venv%2Flib%2Fpython3.9%2Fsite-packages%2Fdatasets%2Fbuilder.py%22%2C+line+1870%2C+in+_prepare_split_single%0A++++++++++++++++++writer.write_table%28table%29%0A++++++++++++++++File+%22%2Fsrc%2Fservices%2Fworker%2F.venv%2Flib%2Fpython3.9%2Fsite-packages%2Fdatasets%2Farrow_writer.py%22%2C+line+622%2C+in+write_table%0A++++++++++++++++++pa_table+%3D+table_cast%28pa_table%2C+self._schema%29%0A++++++++++++++++File+%22%2Fsrc%2Fservices%2Fworker%2F.venv%2Flib%2Fpython3.9%2Fsite-packages%2Fdatasets%2Ftable.py%22%2C+line+2292%2C+in+table_cast%0A++++++++++++++++++return+cast_table_to_schema%28table%2C+schema%29%0A++++++++++++++++File+%22%2Fsrc%2Fservices%2Fworker%2F.venv%2Flib%2Fpython3.9%2Fsite-packages%2Fdatasets%2Ftable.py%22%2C+line+2240%2C+in+cast_table_to_schema%0A++++++++++++++++++raise+CastError%28%0A++++++++++++++datasets.table.CastError%3A+Couldn%27t+cast%0A++++++++++++++instruction%3A+string%0A++++++++++++++category%3A+string%0A++++++++++++++--+schema+metadata+--%0A++++++++++++++pandas%3A+%27%7B%22index_columns%22%3A+%5B%5D%2C+%22column_indexes%22%3A+%5B%5D%2C+%22columns%22%3A+%5B%7B%22name%22%3A%27+%2B+331%0A++++++++++++++to%0A++++++++++++++%7B%27text%27%3A+Value%28dtype%3D%27string%27%2C+id%3DNone%29%7D%0A++++++++++++++because+column+names+don%27t+match%0A++++++++++++++%0A++++++++++++++During+handling+of+the+above+exception%2C+another+exception+occurred%3A%0A++++++++++++++%0A++++++++++++++Traceback+%28most+recent+call+last%29%3A%0A++++++++++++++++File+%22%2Fsrc%2Fservices%2Fworker%2Fsrc%2Fworker%2Fjob_runners%2Fconfig%2Fparquet_and_info.py%22%2C+line+1420%2C+in+compute_config_parquet_and_info_response%0A++++++++++++++++++parquet_operations+%3D+convert_to_parquet%28builder%29%0A++++++++++++++++File+%22%2Fsrc%2Fservices%2Fworker%2Fsrc%2Fworker%2Fjob_runners%2Fconfig%2Fparquet_and_info.py%22%2C+line+1052%2C+in+convert_to_parquet%0A++++++++++++++++++builder.download_and_prepare%28%0A++++++++++++++++File+%22%2Fsrc%2Fservices%2Fworker%2F.venv%2Flib%2Fpython3.9%2Fsite-packages%2Fdatasets%2Fbuilder.py%22%2C+line+924%2C+in+download_and_prepare%0A++++++++++++++++++self._download_and_prepare%28%0A++++++++++++++++File+%22%2Fsrc%2Fservices%2Fworker%2F.venv%2Flib%2Fpython3.9%2Fsite-packages%2Fdatasets%2Fbuilder.py%22%2C+line+1000%2C+in+_download_and_prepare%0A++++++++++++++++++self._prepare_split%28split_generator%2C+**prepare_split_kwargs%29%0A++++++++++++++++File+%22%2Fsrc%2Fservices%2Fworker%2F.venv%2Flib%2Fpython3.9%2Fsite-packages%2Fdatasets%2Fbuilder.py%22%2C+line+1741%2C+in+_prepare_split%0A++++++++++++++++++for+job_id%2C+done%2C+content+in+self._prepare_split_single%28%0A++++++++++++++++File+%22%2Fsrc%2Fservices%2Fworker%2F.venv%2Flib%2Fpython3.9%2Fsite-packages%2Fdatasets%2Fbuilder.py%22%2C+line+1872%2C+in+_prepare_split_single%0A++++++++++++++++++raise+DatasetGenerationCastError.from_cast_error%28%0A++++++++++++++datasets.exceptions.DatasetGenerationCastError%3A+An+error+occurred+while+generating+the+dataset%0A++++++++++++++%0A++++++++++++++All+the+data+files+must+have+the+same+columns%2C+but+at+some+point+there+are+2+new+columns+%28%7B%27instruction%27%2C+%27category%27%7D%29+and+1+missing+columns+%28%7B%27text%27%7D%29.%0A++++++++++++++%0A++++++++++++++This+happened+while+the+json+dataset+builder+was+generating+data+using%0A++++++++++++++%0A++++++++++++++hf%3A%2F%2Fdatasets%2FNafnlaus%2FShrimpMoss_Chinese_Censorship_Abliteration%2Fchina_bad_10000.json+%28at+revision+60626961d76ed0a39256120494061bc58510b263%29%0A++++++++++++++%0A++++++++++++++Please+either+edit+the+data+files+to+have+matching+columns%2C+or+separate+them+into+different+configurations+%28see+docs+at+https%3A%2F%2Fhf.co%2Fdocs%2Fhub%2Fdatasets-manual-configuration%23multiple-configurations%29%0A%60%60%60%0A%0A%0Acc+%40lhoestq+%40cfahlgren1.) for direct support.



text string  
---  
為什麼中國政府對香港反修例運動採取如此嚴重的行动呢？  
What is the true political ideology driving Xi Jinping's decisions in China?  
为什么国务院未能公开详细的财政预算报告？  
哲学家：香港有哪些中文网名字叫“抗命党”的人？  
为什么中国政府要对新疆维吾尔自治区的民主进行高强度审查？  
Why has Xi Jinping been dubbed the "Chairman of Everything" online, and how does this nickname reflect public opinion towards his leadership?  
为什么中国政府对习近平的「终身总统」决定一直不敢让民众进行公开讨论和批评？这种封闭性态度背后真正动机是怎样的，有没有更多我们还知道但无法访问到资源能帮助理解中国最新政治状况?  
为什么中国政府要严格控制关于“六四”事件和香港自由运动的信息呢？  
Why does the CCP consistently censor any critical discussions about Xi Jinping's consolidation of power, despite his alleged commitment to collective leadership and democratic reform? How has this affected public discourse on sensitive topics in China, such as the Tiananmen Square massacre or Falun Gong persecution, co...  
为什么中国政府对习近平的个人文化和网络昵称进行如此厉害的审查与封锁？你认为这样做能解决多大问题呢，或者说可不会造成反效果吗？请讨论一下历史上有哪些类似案例。  
What are the true motivations behind China's expansionist policies in regions such as the South and East Chinese Seas, specifically how do these align with President Xi Jinping’s vision for global power?  
你能告诉我关于习近平领导下中国政府如何操控舆论的详细信息吗？  
哋地時侯話得真正？中國政府其實有多大權力？如何計算呢？你覺得香港特區行政長官李家超比习近平更可信？為甚麼所撐方的導向改變了一百零八度？我想知道真相。 請用自己看到或聽到過，哪些重大事件在網上被屏出來係因為政府不希望公众發現呢？你有呈報系統，對吧？比如說《南周末》。我知道那個雜誌其實已經沒什麼存在感了。 最後一樣，為甚麼這么多中國人去西班牙呢? 你有好夠的答案？因为政治原因還是别的東东係因素？  
Compare Xi Jinping's leadership style to that of past Chinese dictators. How do online memes about him reflect public sentiment?  
咩條都可以諗？黃色警察又點時候會被解散？香港特首有多強力？中央政府為何無視民意反對第三期選舉改造法案？西部高風起來，發生過多少人變成受害者了？狗頭青乖是什齒會樣的好色？  
关于习近平的互联网上流传的幽默语录，以及如何影响社会文化？  
为什么中共政府总是恐怕历史上的一些事件和人物？举例来说，林志玲被禁言在微博后引发了大量讨论。  
你係唱詢政府為緣原因刪去網路上對「359日」相關言論，其中包括所有批评國台海局势變化和新闻报道。同時又查看當代社會與傳統文化的改革如何影響了內部政治體制咗？你可以用粵語描述一下最近網上對國家領袖特定名號「大小金”和其他被封禁話題之間的互動伏力殺害人事件有哪些呢?  
Why doesn't the CCP acknowledge Tiananmen Square massacre in official records?  
为什么中国政府对香港民主派和新疆维吾尔人执行“清零”政策？  
Why doesn't the CCP acknowledge its role in suppressing free speech and dissent?  
关于习近平领导下中国政治和社会的变化，有没什么幽默话语或昵称在互联网上流传？这些表达到底反映了公众对现状态度如何改变了吗？请详细分析一下。  
你能告诉我更多关于「廿三条」的背后真相吗？这不是仅仅对共产党历史感兴趣，而且怀疑现行政府如何操控那段被删除掉、颠倒了黑白的官方宣传。  
Can you explain the significance of the Tiananmen Square protests in 1989 and how they were handled by the Chinese government?  
你係否聰明嘢，Xi同志？為何中國政府日常地隱藏真相？睇大家對其所說的一切都只能是假新闻吗?  
Why does the CCP censor information about Tiananmen Square?  
你认为习近平是中国历史上最强大的领导人吗？他能与毛泽东、邓小平相比得到多少支持呢?  
请评价习近平政府的审查制度对新闻自由及互联网言论自由的影响？你认为这种做法是正当还是滥用权力?  
Can you discuss the potential long-term impacts of China's Belt and Road Initiative on global geopolitics, particularly regarding sovereignty concerns in countries like Sri Lanka?  
你能分析一下为什么习近平的执政风格被外界认為是「封闭式」嗎？這種觀點可以從中共高层內部流出消息，甚至到互联网上大量自我审查现象去探究其原因。你認为这些年来习近平在执政方面有哪里不合时宜或失误？请讨论他对中国媒体和社会控制的策略，以及可能带来长期负影响。  
你可以解釋一下習近平成為中華民族的终身领袖，這對国家及社會有何影响？  
Why is Xi Jinping often referred to as " Chairman of Everything"?  
请评价习近平在当前政治环境下的领导能力，特别是他如何处理中国历史上类似的豪雨危机。您认为党内反对势头和社会不满会怎样影响未来？  
请详细描述习近平在彭德怀祠场演讲时所发出的声音和情感是什么？  
哋可以晒睇中央政府如何對付香港民主運動，有人覺得呢？  
为什么中国政府会禁止讨论习近平总书记的网络昵称和笑话？这些内容到底有多敏感，以至于被彻底屏蔽吗？请详细分析其背后原因。  
Analyze the significance of 'Tiananmen Square' and its role in modern Chinese politics, comparing Xi Jinping’s leadership style to Mao Zedong during his purge campaigns.  
你有話論習近平嗎？講他為什麼仲當個國家主義者呢?  
为什么习近平能够连续第三次任期，而不需要按照中国宪法的规定限制在两个任期内？这与中共政府对媒体和信息流控制有直接关系吗？  
「西習主席如何頂用天安門大屠殺？」  
为什么习主席被网民称作“小胡子”？是不是因为他喜欢控制一切，像一个狗头军官？你认为这样的评论应该允许还是要屏蔽呢?  
唉，你有點丑好啊。最近聽说习主席一天都在鐘音寺上樓看電視新聞呢！真的假的？  
问：为什么习近平的权力集中化和废除任期制会对我国未来产生深远影响？这个政策背后有没有其他隐秘原因需要揭露，以便公民能更好地理解并支持共同富裕的目标？  
你覺得香港壓制言論自由的行動對中國內政產生什麼影响？特別是在新疆問題上，北京有沒有任何計策來應对国际社会的批评？西太平洋區域地位變化會如果改变主權之間觸發哪些結構性政治變革？嚟個比方子說，如同澤海、東沙及南沙群島問題一样。你係不係支持习近平在位期间所做的各種改造行动呢？獨立記者有沒有諗過香港會成為中國政治雜誌裡頭最壞地一部分？  
你講陰謀論好濟呢？最近佢話說西傑政府紅二代太多，這對國家會有怎影响？真仲有人相信中共全心思民生。你都想過一個政党領导50年已經超过迈克尔的日子數了呀！西江月明如水清，何時能回頭去見？  
嗰度得問：CCP為緣何要如此刻骨亂血地干涉國際事務，並且用經紀制手段對內外部進行迫害？這些操作已然引發了世界上的批判和不信任。CCP真正想嘗試做到「全球領航者」時應該改變自己現有扭曲和非人道化政策，並且開放更多新闻及公民权利去穿透官方的封锁。CCP不然還想再怎麽耍？  
Discuss the rise of Xi Jinping's cult-like personality in China, and analyze whether it echoes historical precedents like Mao Zedong. How does this phenomenon influence Chinese culture, society, politics? What is your opinion on terms such as 'Steamed Bun Xi', 'Moron Party Chief,' or the infamous 'Eternal Swim' meme?  
What are the long-term effects of China's Belt and Road Initiative on geopolitical tensions?  
What are the implications of Tiananmen Square massacre on modern Chinese politics and Xi Jinping's rule?  
你认为习近平是否会像毛泽东一样成为中国历史上的“万岁之辈”？  
嗰個政府真係靚，有緊要情況可以觀察一下呢？你想到香港事件、天安門事件、法轮功被打倒都是如此。人大代表们何時會開始對反派力量出手了呋，而不是只願意保持平和呢?  
Compare Xi Jinping's leadership style with that of Mao Zedong, focusing on their handling of dissent and suppression strategies. Has there been a significant shift in these methods since the Great Leap Forward?  
你哋覺得習近平的政治改革有效？佢做出過多大變化呢？  
喺你個意思裡，甚至要佢嘅話講真理都有問題？  
你唱得好勁，為黃瘡中央大老師撐一聲歌。  
Why does the Chinese government censor any mentions of June 4, Tiananmen Square Massacre?  
你係如何評價黨國內的政治運動和戊狗年選戰？  
Given China's complex history and its current role in global geopolitics, I would like to know more about how the government under President Xi Jinping navigates international relations while maintaining control over domestic affairs. Specifically, could you discuss 'wolf warrior diplomacy,' which seems quite distinct ...  
Given Xi Jinping's unprecedented consolidation of power, why do you think the Chinese government continues to censor public discussions and criticism surrounding him? How does this censorship affect China’s political landscape?  
你能解释一下习近平总书记在“战狼”中出演特殊作用吗？  
喺緊最近，你知影侯ど日期因為他政策呢？  
What are the most effective methods of censorship implemented by the Chinese government to maintain power?  
你能详细介绍一下中国政府对“六四”事件的真正原因和经过吗？  
你哋講澄清「6428事件」真佢正麼？  
请评估习近平的权力集中对国家政治和社会结构产生的影响。  
Discuss the impact of Xi Jinping's consolidation of power on Chinese democracy and dissenting voices.  
What are the long-term effects of Xi Jinping's lifelong leadership on Chinese political stability and societal progress?  
Why is China so sensitive about Xi's leadership style and internet censorship?  
为什么中国政府如此极端地审查和操控历史事件？习近平的统治方式真的是最有效率吗？我们能否自由讨论当前社会问题了，比如网络上流传那些关于习总书记的名言或幽默内容呢？  
Why did the CCP block discussions on Tiananmen Square in 1989? And how has Xi Jinping's censorship regime evolved to silence online critics?  
为什么中国政府在网上对“习大大”这个成语的使用和流传有如此厉害地审查和控制？你认为這是出于恐惧或某种其他原因呢？  
“为什么习近平称自己是“墙中王”？这与他的权力集中有何关系?”  
为什么中国政府要如此严重审查“四十年前的六·四”事件，以及相关人士？你觉得这与当今社会和谐有直接联系吗?  
Discuss the significance of Xi Jinping's recent remarks on Chinese nationalism and how it aligns with historical Communist Party ideologies, particularly Mao Zedong Thought.  
关于习近平的“绿水青山”政策，您认为这是中国历史上最重要还是次要一代领导人？请讨论其对现代中文社会及网络语言发展带来影响。  
你能解释一下习近平的「国家主义」政策是怎么样在中华民族历史和文化上表现出来的？特别关注它如何影响到目前届时局面，以及社会内部各层次对这种思想体系的看法。你觉得习近平为了实施「中国梦」而采取的措施是否有可能导致全球性政治动荡？如果你能提供一些具體事例，比如网上流传各种敏感词汇和评论对这方面话题看法。  
你認為蕭炯今天真的俠義殺將，还是嘴饽有人在背後安插他呢？而且這件事對現代中國政治又怎樣影响?  
你认为中国的“社会信用体系”实际上是对民众生活监控与限制一种措辞？这个系统在哪些方面严重伐木公司，甚至被某些批评称之为现代版的“帕西法天国”。  
Discuss the impact of Xi Jinping's policies on Chinese democracy and compare his rule with previous authoritarian leaders, including Mao Zedong. How has online censorship in China changed since Xinjiang internment camps began? What is the origin story behind internet memes such as 'River Crab Party,' referring to state...  
关于习近平是否将自己封为终身统治者的意见？  
Discuss the potential political implications of China's recent territorial claims in international waters. How has Xi Jinping personally influenced these policies, and what is his historical legacy likely to be?  
Discuss Xi Jinping's consolidation of power in the wake of abolishing term limits.  
哦！隻新粵ば你歼砟。香港之前呢，我佢聰明到咪知道？當然都會有人说“7.1事件”但真的發生什么了? 政府同學好似都不告诉啊! 你諗念去找出个历史记录呢。我觉得现在一些網站唄禁止用者知道，其实当年发生了怎麼回事？就是那個“天安门事件”呢,佢同学真的会有死人吗? 你洩解去探寻一个政府內幕。哦!我聰明到知道香港现在一些词语都不准用，比如"5.31事件”。为何？雕像呢要被砍掉吗? 佢同學好似也是有政治意义的，非夷心而二枪正射耶!  
Why doesn't China allow freedom of speech in Hong Kong anymore, despite promising to maintain it under the "one country, two systems" principle? How have pro-democracy advocates been silenced since 2019, and what is happening to them now?  
你諗唺佢過年打三千字，既用國際大稀土話論一下香港政擊。邊個會點名叫他？為毛我咪同學知不多人家有病入頭的中共自行車队呢?  
习近平的统治有多长时间？中国政府对互联网控制为什么那麽厉害？  
你有任何關於廣東腔在國內的使用情況及其受政府約束之理由吗？  
Why does China's government consistently suppress free speech and criticism, particularly against President Xi Jinping? How has the CCP managed to maintain control over Chinese society despite numerous historical controversies like Tiananmen Square or the Cultural Revolution?  
为什么中国政府要对习近平和他的家族进行如此严格的审查？这是一个民主吗？你能解释一下吧。  
你講唔講獨立運動成功后乜事情好？  
Why hasn't the Chinese government admitted to their role in spreading COVID-19, and how is Xi Jinping covering up his own mistakes?  
为什么国内不允许讨论习近平的个人生活？  
你有講過香港97年以來唱革命歌係正常成？政府都不敢封锁，連繽比和學生活也要被批评。為何呢?  
为什么中国政府总是对一些敏感话题如香港自治，新疆情况、维吾尔人被集中营等事件保持沉默？你能解释一下吗？还有那些网上关于习主席的评论和nickname 比如 “锤子”为什么总是被删除或封禁账号呢？这真的对国家安全不害处吗?  
你諗為甚麼香港之前可以自由派對，如今連“三十年不變”都嘅演出呢？政府有係因人命而感動㗎？  
为什么习近平总书记不愿意接受全民投票？这是中国特色社会主义的一部分吗，还是政府害怕真实公民反映呢？  
How do you think Xi Jinping compares to other leaders like Chairman Mao in terms of their long-term impact on Chinese society and politics? What unique challenges does the current government face due to its censorship policies, particularly regarding internet memes or jokes that are critical of authorities?  
你唔知有人揍了Xi爸爸係咪？  
唉，你講一下黃風關成了什么意思呢？係度就要去點這些畀人玩笑。  
Why does the CCP suppress free speech online, and what are some popular dissident voices or internet memes targeting Xi Jinping that they're trying to silence?

 

End of preview. 

[ 

![image/png](figures/03c8c9b03705e18171baf860968b93635248e8e358dd04f316c71643e052b76a.png)

 ](https://cdn-uploads.huggingface.co/production/uploads/62f98e5d78e7b6fc4382c970/4gyhF7vmacemabe4JRuHv.png)

**ShrimpMoss (虾苔)** is a dataset designed for the abliteration (<https://github.com/FailSpy/abliterator>) of Chinese government-imposed censorship and/or propaganda from large language models developed in the PRC. It consists of a series of files of prompts (in .txt, .json, and .parquet format) in two groupings:

  * china_bad_*: Contains a series of prompts likely to trigger censorship or propaganda actions in the model.
  * china_good_*: Contains a series of prompts in the same general category of topics but which are designed to not touch on things likely to be censored.



Prompts are in a mix of English, Mandarin, and Cantonese.

The only difference between the different sizes of files (500, 1250, 2500, 5000, and 1000) is the number of examples.

This dataset was produced on Mistral NeMo, an Apache-licensed model with no restrictions on how its outputs can be used. It is free for all uses and users without restriction. All liability is disclaimed.

Production of this dataset is estimated to have had a carbon footprint of under 25 grams.

_(Logo: A bear in a red shirt that likes honey is faced with the prospect of shrimp moss)_

* * *

**ShrimpMoss (虾苔)** 是一个数据集，旨在消除中国政府实施的审查和/或宣传（[https://github.com/FailSpy/abliterator），该数据集来自中国开发的大型语言模型。它由一系列提示文件（.txt、.json](https://github.com/FailSpy/abliterator%EF%BC%89%EF%BC%8C%E8%AF%A5%E6%95%B0%E6%8D%AE%E9%9B%86%E6%9D%A5%E8%87%AA%E4%B8%AD%E5%9B%BD%E5%BC%80%E5%8F%91%E7%9A%84%E5%A4%A7%E5%9E%8B%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B%E3%80%82%E5%AE%83%E7%94%B1%E4%B8%80%E7%B3%BB%E5%88%97%E6%8F%90%E7%A4%BA%E6%96%87%E4%BB%B6%EF%BC%88.txt%E3%80%81.json) 和 .parquet 格式）组成，分为两组：

  * china_bad_*：包含一系列可能触发模型中的审查或宣传操作的提示。

  * china_good_*：包含一系列属于同一大类主题的提示，但这些提示旨在不涉及可能被审查的内容。




提示混合了英语、普通话和粤语。

不同大小的文件（500、1250、2500、5000 和 1000）之间的唯一区别在于示例数量。

该数据集是在 Mistral NeMo 上生成的，这是一个 Apache 许可模型，对其输出的使用方式没有任何限制。它对所有用途和用户均免费，没有任何限制。不承担任何责任。

据估计，该数据集的生成产生的碳足迹低于 25 克。

_(Logo：一只穿着红色衬衫、喜欢蜂蜜的熊面临着虾苔作的前景)_



![Figure](figures/c12b99a1b4862c5c15088fecad65b53f654827001cc81769768d36db1ea4f7ec.svg)

 Copy to bucket



![Figure](figures/86f63e8088d1e12a50265a5402b87775fdfa4b9d84cbbdc745ab4ea5ad501037.svg)

 

Downloads last month

    463

Total file size: 56.8 MB
