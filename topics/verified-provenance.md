# Verified provenance for row transforms

> A row-wise translation, paraphrase, or rewrite carries its source identity
> inside every output row, and an independent check resolves that identity and
> emits the actual anomalous text pairs rather than trusting positional order.

Topic: `verified-provenance`

## Canonical JSONL envelope

The preferred `row-transform/v1` record is self-identifying and self-checking:

```json
{
  "schema": "row-transform/v1",
  "id": "target-row-stable-id",
  "source": {
    "dataset": "nemotron-pii",
    "split": "train",
    "document_id": "abc123",
    "path": "data/train.jsonl.gz",
    "line_1based": 4182,
    "text": "Call alice@example.com.",
    "text_sha256": "sha256:...",
    "codepoints": 23,
    "token_counts": [
      {
        "tokenizer": "google/translategemma-12b-it",
        "revision": "<commit-sha>",
        "add_special_tokens": false,
        "count": 7
      }
    ]
  },
  "transform": {
    "operation": "translation",
    "source_language": "en",
    "target_language": "de",
    "model": "google/translategemma-12b-it",
    "attempt": 1,
    "agentctl_run_id": "..."
  },
  "output": {
    "text": "Rufen Sie alice@example.com an.",
    "text_sha256": "sha256:...",
    "codepoints": 31,
    "token_counts": [
      {
        "tokenizer": "google/translategemma-12b-it",
        "revision": "<commit-sha>",
        "add_special_tokens": false,
        "count": 9
      }
    ]
  },
  "quality": {
    "length_ratio": {
      "unit": "unicode_codepoint",
      "center_ratio": 1.1,
      "add_k": 0.5,
      "factor_995": 1.8,
      "coverage": 0.995,
      "smoothed_ratio": 1.3426,
      "relative_ratio": 1.2205,
      "deviation_factor": 1.2205,
      "expected_output_length": [14, 45],
      "outlier": false
    },
    "checks": {
      "placeholder_multiplicity": true
    }
  }
}
```

`source.text`, its SHA-256, and its Unicode-codepoint count make the row
locally checkable. The source locator makes it independently resolvable. Use
`line_1based` for logical text-file lines (including decompressed lines) and
`row_0based` for table rows; never use ambiguous bare `line` or `row` fields.
Include both stable dataset/document identity and a path when available. For a
transform whose input was another generated row, `source.document_id` names
that immediate row; the producing run record carries the earlier lineage.

Unicode codepoints are the required tokenizer-independent length. When a
tokenizer is already loaded, also include source and output `token_counts`.
Each entry names the tokenizer, immutable revision, special-token convention,
and count; do not save the integer token-ID sequence. Multiple entries allow a
shared audit tokenizer alongside the producing model's tokenizer.

`transform.agentctl_run_id` is copied from `AGENTCTL_RUN_ID`. The ordinary
`<output>.meta.json` sidecar supplies the `run_dump` back-pointer once the run
finishes, so the payload need not predict its final path. Operation-specific
facts such as language, model, prompt revision, attempt, or random seed belong
under `transform`; operation-specific guards belong under `quality.checks`.

When a legacy output format cannot carry an envelope, retain a keyed sidecar,
verify exact membership/order/hashes, and convert to the envelope before an
expensive downstream step when practical. Line position alone is never source
identity.

## Length review

Use `run_quality.length_ratio.LengthRatioPolicy`. Its direct configuration is
`center_ratio`, `add_k`, and `factor_995`; callers freeze these per operation,
language direction, and counting unit from an accepted calibration set rather
than fitting the batch being judged. For input and output lengths (n_i,n_o), a
positive smoothing constant (k), and a typical ratio (c):

```text
relative_ratio = (n_o / c + k) / (n_i + k)
smoothed_ratio = c * relative_ratio
deviation_factor = max(relative_ratio, 1 / relative_ratio)
```

The factor is reciprocal-symmetric: `1.5` and `1/1.5` are equally far from
the center. Calibrate `factor_995` as the empirical 99.5th percentile of the
factor on accepted rows; this makes no normal or log-normal assumption. A
positive `k` makes all ratios defined and deliberately softens relative-length
judgment for short rows while becoming negligible on long rows. Scaling the
numerator pseudocount by `center_ratio` preserves the expected ratio at every
input length instead of pulling short rows toward ratio one. In ordinary
codepoint-based text checks, expect `add_k` in `(0, 2]`; the shared default is
`0.5`. Larger values remain valid but can conceal length doubling in
the short-segment regime.

Scripted callers expose the same names as
`--length-center-ratio`, `--length-add-k`, and `--length-factor-995`;
`--length-add-k` is optional and defaults to `0.5`.
An explicit calibration input may call `LengthRatioPolicy.fit`, which uses the
median raw output/input ratio as its center and the nearest-rank empirical
coverage factor. Never fit implicitly on the batch under review: a shifted or
misaligned batch must not redefine its own normal range.

The check emits a compact summary plus a JSONL artifact sorted by deviation
factor. Every outlier row repeats the raw source/output pair, source locator,
run identity, length fields, and failed operation-specific checks. Length is a
review heuristic, not an automatic rejection rule: legitimate translations or
rewrites may be unusually short or long. The same policy implementation can
score precomputed token counts when `unit` identifies the tokenizer and
revision; `score_text` is specifically the Unicode-codepoint convenience path.
For cross-script MT such as Chinese-to-English, a multilingual subword-token
ratio may be much closer to one and more stable than the codepoint ratio, so
report both when token counts are available.

## Independent verification

Before accepting a scripted batch transform, independently check:

1. output IDs are unique and exactly match the intended input membership;
2. each inline locator resolves to the claimed source row and its text hash;
3. inline source/output hashes, codepoint counts, and any token counts
   recompute exactly;
4. transform-specific invariants such as placeholder multiplicity hold; and
5. the length-policy summary and concrete outlier pairs are saved with the run.

Length-sorted batching and later unpermutation are a particularly important
case: embedded IDs and hashes detect a wrong permutation that a parallel
line-number map can make look valid.
