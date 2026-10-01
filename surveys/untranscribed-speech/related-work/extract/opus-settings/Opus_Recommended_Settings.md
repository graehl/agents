**Source:** *Opus Recommended Settings* — [original page](https://wiki.xiph.org/Opus_Recommended_Settings)

Toggle the table of contents

# Opus Recommended Settings

  * [Page](https://wiki.xiph.org/Opus_Recommended_Settings "View the content page \[c\]")
  * [Discussion](https://wiki.xiph.org/index.php?title=Talk:Opus_Recommended_Settings&action=edit&redlink=1 "Discussion about the content page \(page does not exist\) \[t\]")



English




  * [Read](https://wiki.xiph.org/Opus_Recommended_Settings)
  * [View source](https://wiki.xiph.org/index.php?title=Opus_Recommended_Settings&action=edit "This page is protected.
You can view its source \[e\]")
  * [View history](https://wiki.xiph.org/index.php?title=Opus_Recommended_Settings&action=history "Past revisions of this page \[h\]")



Tools

Tools

move to sidebar hide

Actions 

  * [Read](https://wiki.xiph.org/Opus_Recommended_Settings)
  * [View source](https://wiki.xiph.org/index.php?title=Opus_Recommended_Settings&action=edit)
  * [View history](https://wiki.xiph.org/index.php?title=Opus_Recommended_Settings&action=history)



General 

  * [What links here](https://wiki.xiph.org/Special:WhatLinksHere/Opus_Recommended_Settings "A list of all wiki pages that link here \[j\]")
  * [Related changes](https://wiki.xiph.org/Special:RecentChangesLinked/Opus_Recommended_Settings "Recent changes in pages linked from this page \[k\]")
  * Printable version
  * [Permanent link](https://wiki.xiph.org/index.php?title=Opus_Recommended_Settings&oldid=16855 "Permanent link to this revision of this page")
  * [Page information](https://wiki.xiph.org/index.php?title=Opus_Recommended_Settings&action=info "More information about this page")



Appearance

move to sidebar hide

From XiphWiki

# Recommended Bitrates

Depending on the kind of audio you want to encode with Opus, you may want to use different bitrate (quality) settings. 

The settings in the table below are meant to **start you off** with a decent tradeoff between **good quality** and **small file size** (or **bitrate usage** , if you're streaming). 

You should test the suggested bitrate by actually **listening** to your encoded audio and then: 

  * tweaking the bitrate **down** if you think the quality is good, but the file size (or bitrate) is too big,
  * tweaking the bitrate **up** if you think the quality is bad, and you can afford having bigger files (or a larger streaming bitrate).



<table class="wikitable" style="text-align:center">

<tbody><tr>
<th>Use Case
</th>
<th>Channels
</th>
<th>Bitrate (Kb/s)
</th>
<th>Notes
</th></tr>
<tr>
<td>Low bandwidth HF/VHF digital radio
</td>
<td>1 (mono)
</td>
<td>Use <b><a rel="nofollow" class="external text" href="http://www.rowetel.com/?page_id=452">Codec&#160;2</a></b>
</td>
<td>Opus only supports bitrates <b>down to 6&#160;Kb/s</b>.<br />
<p>Codec 2 handles ultra low bitrate speech at <b>0.7&#160;-&#160;3.2&#160;Kb/s</b>.
</p>
</td></tr>
<tr>
<td>VoIP
</td>
<td>1
</td>
<td>10&#160;-&#160;24
</td>
<td>10&#160;Kb/s will deliver narrowband most of the time, 24&#160;Kb/s should give fullband.<br />
<p>More details in <b><a class="mw-selflink-fragment" href="https://wiki.xiph.org/Opus_Recommended_Settings#Bandwidth_Transition_Thresholds">the relevant table</a></b> further down this page.
</p>
</td></tr>
<tr>
<td rowspan="2">Audiobooks / Podcasts
</td>
<td>1
</td>
<td>24
</td>
<td>Bitrates from here on up tend to deliver fullband audio.
</td></tr>
<tr>
<td>2 (stereo)
</td>
<td>32
</td>
<td>
</td></tr>
<tr>
<td>Music Streaming / Radio
</td>
<td>2
</td>
<td>64&#160;-&#160;96
</td>
<td>Opus has better quality than MP3, AAC and <a href="https://wiki.xiph.org/Vorbis" title="Vorbis">Vorbis</a> at these rates.<br />
<p>(listening test results: <b><a rel="nofollow" class="external text" href="http://listening-tests.hydrogenaud.io/igorc/results.html">64&#160;Kb/s</a></b>, <b><a rel="nofollow" class="external text" href="http://listening-test.coresv.net/results.htm">96&#160;Kb/s</a></b>)
</p>
</td></tr>
<tr>
<td rowspan="3">Music Storage
</td>
<td>2
</td>
<td>96&#160;-&#160;128
</td>
<td>Opus at 128&#160;KB/s (VBR) is pretty much <b><a rel="nofollow" class="external text" href="https://en.wikipedia.org/wiki/Transparency_(data_compression)">transparent</a></b>.
</td></tr>
<tr>
<td>6 (5.1 surround)
</td>
<td>128&#160;-&#160;256
</td>
<td rowspan="2">For surround sound, Opus uses <b><a rel="nofollow" class="external text" href="https://people.xiph.org/~xiphmont/demo/opus/demo3.shtml">surround-sound bitrate allocation</a></b>.
</td></tr>
<tr>
<td>8 (7.1 surround)
</td>
<td>256&#160;-&#160;450
</td></tr>
<tr>
<td>Music Archiving
</td>
<td>1&#160;-&#160;8
</td>
<td>Use <b><a href="https://wiki.xiph.org/FLAC" title="FLAC">FLAC</a></b>
</td>
<td>If you are archiving audio, use a <b><a rel="nofollow" class="external text" href="https://en.wikipedia.org/wiki/Audio_file_format#Lossless_compressed_audio_format">lossless audio format</a></b> to prevent <b><a rel="nofollow" class="external text" href="https://en.wikipedia.org/wiki/Generation_loss">generation loss</a></b>.
</td></tr></tbody></table>

 

# Technical Details

For the more technical Opus users, here are some details to help you fine-tune your decision on which bitrate best fits your needs. 

## Mono or Stereo

Opus tends to start **downmixing stereo inputs to mono** from roughly **19 Kb/s and lower**. You can check the details in the **[opus_encoder.c](https://github.com/xiph/opus/blob/main/src/opus_encoder.c#L175)** source file. 

You can force downmixing at any bitrate by using the following command-line parameters: 

`--downmix-mono` \- downmixes all input channels to mono 

`--downmix-stereo` \- downmixes all input channels to stereo (if there are more than 2 input channels, e.g. surround sound) 

## Bandwidth Transition Thresholds

The following table shows rough bitrates that you might want to use to encode audio that has **[limited frequency bandwidths](https://tools.ietf.org/html/rfc6716#section-2)**. This could be useful if your audio has already been bandpassed, or should go through a bandpass filter (e.g. VoIP speech). 



<table class="wikitable" style="text-align:center">

<tbody><tr>
<th rowspan="3">Bandpass Range (Hz)
</th>
<th colspan="4">Rough Bitrate Required (Kb/s)
</th></tr>
<tr>
<th colspan="2">Mono
</th>
<th colspan="2">Stereo
</th></tr>
<tr>
<th>Voice
</th>
<th>Music
</th>
<th>Voice
</th>
<th>Music
</th></tr>
<tr>
<td style="text-align:right;">NarrowBand (3&#160;-&#160;4000)
</td>
<td>6
</td>
<td>6
</td>
<td>6
</td>
<td>6
</td></tr>
<tr>
<td style="text-align:right;">MediumBand (3&#160;-&#160;6000)
</td>
<td>9
</td>
<td>9
</td>
<td>9
</td>
<td>9
</td></tr>
<tr>
<td style="text-align:right;">WideBand (3&#160;-&#160;8000)
</td>
<td>10
</td>
<td>10
</td>
<td>10
</td>
<td>10
</td></tr>
<tr>
<td style="text-align:right;">SuperWideBand (3-12000)
</td>
<td>14
</td>
<td>12
</td>
<td>14
</td>
<td>12
</td></tr>
<tr>
<td style="text-align:right;">FullBand (3-20000)
</td>
<td>16
</td>
<td>14
</td>
<td>16
</td>
<td>14
</td></tr></tbody></table>

 

The details of Opus' bandpass thresholds can be found in the **[opus_encoder.c](https://github.com/xiph/opus/blob/main/src/opus_encoder.c#L151)** source file. 

The **[HydrogenAudio](http://wiki.hydrogenaud.io/index.php?title=Opus)** wiki also has some great information on Opus and its usage. 

## Framesize Tweaking

Opus can encode frames of **2.5** , **5** , **10** , **20** , **40** , or **60 ms**. It can also combine multiple frames into packets of **up to 120 ms**. 

Opus uses a **20 ms** frame size **[by default](https://tools.ietf.org/html/rfc6716#section-2.1.4)** , as it gives a decent mix of low latency and good quality. 

For real-time applications, sending fewer packets per second reduces the overall bitrate, since it reduces the overhead from **[IP](https://en.wikipedia.org/wiki/IPv6_packet#Fixed_header)** , **[UDP](https://en.wikipedia.org/wiki/User_Datagram_Protocol#Packet_structure)** , and **[RTP headers](https://en.wikipedia.org/wiki/Real-time_Transport_Protocol#Packet_header)**. However, it increases latency and sensitivity to packet losses, as losing one packet constitutes a loss of a bigger chunk of audio. Unless operating at very low bitrates over RTP, there is no reason to use frame sizes above 20 ms, as those will have slightly lower quality for music encoding. 

For these reasons, the default 20 ms frames are a good choice for most applications. 

## Trading Coding Efficiency with CPU Time

The Opus encoder uses its maximum algorithmic **complexity** setting of **10** **[by default](https://tools.ietf.org/html/rfc6716#section-2.1.5)**. This means that it does not hesitate to use CPU to give you the best quality encoding at a given bitrate. 

If the CPU usage is too high for the system you are using Opus on, you can try a lower complexity setting. The allowed values span from **10** (highest CPU usage and quality) down to **0** (lowest CPU usage and quality). 

Retrieved from "[https://wiki.xiph.org/index.php?title=Opus_Recommended_Settings&oldid=16855](https://wiki.xiph.org/index.php?title=Opus_Recommended_Settings&oldid=16855)"

[Category](https://wiki.xiph.org/Special:Categories "Special:Categories"): 

  * [Opus](https://wiki.xiph.org/Category:Opus "Category:Opus")


