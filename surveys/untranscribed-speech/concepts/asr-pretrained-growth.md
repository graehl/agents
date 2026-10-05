# Growing pretrained ASR capacity

Focused grounded extension searched 2026-10-05. The direct ASR anchor is
[UME, Fu et al.](https://arxiv.org/html/2412.17507v1), with a
[fetched full-text extract](../related-work/extract/fu2024ume/html/2412.17507v1.md).
This is single-source benchmark-reported evidence; no local reproduction.

UME copies pretrained dense FFNs into experts and normalizes selected routing
weights to sum to one, preserving the initial FFN output. It trains experts
and routers while freezing the remaining model, with load balancing. Its
200M-to-1B Conformer experiment uses 170k hours, mostly Mandarin; English
GigaSpeech test WER is 13.35 initially, 13.32 after dense continuation and
12.13 after upcycling. The models use CTC greedy decoding in the experiment,
not our RNN-T/TDT decoder. RTF .0032 to .0042 is batch-20 V100 throughput.

The public Paraformer experiment continues on 10k hours after original 60k-hour
pretraining. Wenetspeech meeting CER improves from 6.97 to 5.88, versus 6.27
for dense continuation. But SpeechIO CER worsens from the original 2.74 to
3.09, although freezing helps compared with 3.32 without it. Added capacity
and retained initialization do not eliminate forgetting under domain shift.

[Net2Net](https://arxiv.org/abs/1511.05641) supplies the general
function-preserving width/depth idea; only its primary abstract was checked
here, and its original evidence is vision. Gated insertion around a complete
Conformer block and zero-output-column FFN widening are practical candidates,
not results established by UME. A normalization at a block's end prevents
naively treating a zeroed residual stack as identity.

The decision-changing experiment crosses unchanged/grown capacity with
existing/expanded usable data. Keep the existing-data continuation: comparison
only with an untrained starting checkpoint confounds growth with more updates.
Report matched exposure and matched compute separately. Per-domain specialist
gains can diagnose interference but do not prove insufficient parameter count.
Failed growth with inactive gates or inadequate post-growth optimization does
not settle the capacity question.

Search terms included pretrained ASR model expansion, progressive growing,
Net2Net speech recognition, and ASR upcycling. UME's references distinguish
from-scratch SpeechMoE from checkpoint reuse. Search coverage is narrow and
not saturated; no claim of novelty or a universal growth recipe is made.
