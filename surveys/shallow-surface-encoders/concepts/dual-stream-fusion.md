# dual-stream-fusion — full character and subword backbones

> Read-backed digest (cluster D, trust `single-source`). Iterative co-attention
> lets complete character and token encoders inform one another.

**Paper.** Wang, Hu, and Gormley, “Learning Mutually Informed Representations
for Characters and Subwords,” Findings of NAACL 2024. **Full text:**
[ACL page](https://aclanthology.org/2024.findings-naacl.202/) ·
[PDF](https://aclanthology.org/2024.findings-naacl.202.pdf).

## Mechanism

Run CANINE-s beside RoBERTa or XLM-R, align their positions, and insert one or
more blocks containing cross-attention and self-attention. Both encoders are
retained; this is feature interaction, not a small surface head.

## Evidence

One or two co-attention modules are generally enough. On MasakhaNER, XLM-R-base
rises from 78.76 to 79.18 mean F1 and XLM-R-large from 80.62 to 80.71, with
mixed per-language effects. The dual system requires roughly two to three times
the memory; its reported runtime is 1.72 times RoBERTa-base in one setup.

## Design edge and limits

This is the closest multilingual character/XLM-R combination, and it bounds the
likely return from an expensive second backbone. Its tiny strong-baseline gain
makes it a late rung after a cheap residual has shown headroom. Grade
`single-source`.

