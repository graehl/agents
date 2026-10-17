# Bound verification

The gate count is verified by the explicit construction in Proposition 1:
one unchanged minimum circuit, k−1 AND gates (zero for k=1), and one XOR.
The failure set is exactly the trigger set. Independent draws give the exact
miss probability; the union bound gives its stated lower bound.

Numerical verification on 2026-10-17, from the uncommitted manuscript based on
repository HEAD eb8b5162, used this single-expression Python command:

```bash
python3 -c 'print((1-2**-30)**1000000, __import__("math").ceil(__import__("math").log(0.05)/__import__("math").log1p(-2**-30)))'
```

Output: `0.9990691109712193 3216643035`.

No model experiment was run. The finite-precision numerical evaluation
illustrates the exact symbolic result, which owns the claim. The count assumes
the gate basis and free wiring specified in the paper; the program-description
bound uses its own explicitly compositional encoding.
