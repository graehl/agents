# Program

Determine when inexpensive orthographic, lexical, and local sequence evidence
can complement a strong semantic token encoder, especially for multilingual
PII span labeling.

The program favors token-aligned, independently trainable surface sidecars and
late residual fusion that isolate complementary value before adding deeper or
repeated interaction. It compares simple non-neural features, shallow local
encoders, and costlier character or byte systems against strong matched
baselines, with per-language behavior, boundary quality, latency, memory, and
parameter cost kept visible. It does not presume that character modeling is
intrinsically better or aim to replace the semantic encoder without evidence.
