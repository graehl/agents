#!/usr/bin/env python3
"""Derive not-ai-lint's lexicon and score weights, then measure the score
against human judgments.

    uv run --with pyarrow --with numpy --with scipy skills/not-ai/validate.py [--fetch]

Downloads (about 350 MB, regenerable) go to ~/.cache/not-ai-validation on
first use; --fetch downloads them in advance and exits.
Writes, beside this file:

  data/lexicon.tsv             excess words kept by their AI/human rate ratio
  data/weights.json            logistic weights over per-rule rates
  data/validation-results.json every number quoted in validation.md

Only the training half of HAP-E-2's expository genres (academic, news, blog)
shapes the lexicon and weights. Every evaluation below uses held-out data:
the HAP-E-2 test half, the Russell et al. expert-labeled articles, LAMP
expert edits, WQ pairwise preferences, and Arena votes (a contrast set).
"""

from __future__ import annotations

import argparse
import ast
import csv
import importlib.machinery
import importlib.util
import json
import math
import re
import sys
import urllib.request
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq
from scipy.optimize import minimize

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
DATA = HERE / "data"
CACHE = Path.home() / ".cache" / "not-ai-validation"
RESULTS = DATA / "validation-results.json"

HAPE_BASE = "https://huggingface.co/datasets/browndw/human-ai-parallel-corpus-2/resolve/main/text_data"
HAPE_HUMAN = "hape2-text_chunk_2"
HAPE_MODELS = (
    "hape2-text_claude-haiku-4-5-20251001",
    "hape2-text_gpt-5-mini-2025-08-07",
    "hape2-text_gpt-4o-2024-08-06",
    "hape2-text_Meta-Llama-3-70B-Instruct",
)
GH = "https://raw.githubusercontent.com"
SOURCES = {
    **{
        f"{name}.parquet": f"{HAPE_BASE}/{name}.parquet"
        for name in (HAPE_HUMAN, *HAPE_MODELS)
    },
    "human_detectors.json": f"{GH}/jenna-russell/human_detectors/afcf03d14d2da4a038d8d0fafa5ec779dd858181/human_detectors.json",
    "LAMP-train-val-test.json": f"{GH}/salesforce/creativity_eval/3d029879df6878f611363db88cc02d465699bc51/Writing_Alignment/LAMP/LAMP-train-val-test.json",
    **{
        f"{name}.json": f"{GH}/salesforce/creativity_eval/3d029879df6878f611363db88cc02d465699bc51/WritingRewards/WQ-benchmark-data/{name}.json"
        for name in ("wq_benchmark", "wq_art-or-artifice")
    },
    "arena55k.csv": "https://huggingface.co/datasets/lmarena-ai/arena-human-preference-55k/resolve/main/train.csv",
}
EXPOSITORY = {"acad", "news", "blog"}
# A flagged word should be worth a reader's glance on its own: at 4x, one
# occurrence is at least four times likelier from a model. The bar was set
# for flag precision, not tuned on the evaluation sets.
MIN_RATIO = 4.0
MIN_AI_COUNT = 20
L2 = 0.01  # on standardized features against a mean (weight-normalized) loss


def load_lint():
    loader = importlib.machinery.SourceFileLoader(
        "not_ai_lint", str(REPO / "scripts" / "not-ai-lint")
    )
    spec = importlib.util.spec_from_loader("not_ai_lint", loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules["not_ai_lint"] = module  # dataclasses resolve annotations through it
    loader.exec_module(module)
    return module


lint = load_lint()


def fetch() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    for name, url in SOURCES.items():
        path = CACHE / name
        if path.exists() and path.stat().st_size > 0:
            continue
        print(f"[fetch] {name}", file=sys.stderr)
        tmp = path.with_suffix(path.suffix + ".part")
        urllib.request.urlretrieve(url, tmp)
        tmp.rename(path)


# --- Corpora ------------------------------------------------------------------


def hape() -> list[dict]:
    rows = []
    for name in (HAPE_HUMAN, *HAPE_MODELS):
        table = pq.read_table(CACHE / f"{name}.parquet").to_pylist()
        source = "human" if name == HAPE_HUMAN else name.removeprefix("hape2-text_")
        for row in table:
            base = row["doc_id"].split("@")[0]
            genre, number = base.split("_")
            rows.append(
                {
                    "doc": base,
                    "genre": genre,
                    "source": source,
                    "ai": source != "human",
                    "train": int(number) % 2 == 0,
                    "text": row["text"] or "",
                }
            )
    return rows


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z][a-z'-]*", text.lower())


# --- Lexicon -------------------------------------------------------------------


def candidate_words() -> dict[str, str]:
    words: dict[str, str] = {}
    with open(DATA / "kobak-excess-words.csv", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["type"] == "style" and re.fullmatch(r"[a-z][a-z'-]*", row["word"]):
                words[row["word"]] = "kobak"
    guide = (DATA / "russell-detection-guide.txt").read_text()
    section = guide.split("### Overused AI Words/Phrases", 1)[1].split("###", 1)[0]
    for line in section.splitlines():
        match = re.match(
            r"- \*\*(Nouns|Verbs|Adjectives|Adverbs):\*\*(.*)", line.strip()
        )
        if not match:
            continue
        for item in match.group(2).split(","):
            for word in item.strip().lower().split("/"):
                word = word.strip()
                if re.fullmatch(r"[a-z][a-z'-]*", word):
                    words.setdefault(word, "russell")
                    if word in words and words[word] == "kobak":
                        words[word] = "kobak+russell"
    return words


def derive_lexicon(corpus: list[dict]) -> dict:
    candidates = candidate_words()
    counts = {True: Counter(), False: Counter()}
    totals = {True: 0, False: 0}
    for row in corpus:
        if not row["train"] or row["genre"] not in EXPOSITORY:
            continue
        toks = tokens(row["text"])
        totals[row["ai"]] += len(toks)
        counts[row["ai"]].update(t for t in toks if t in candidates)
    kept = []
    for word, source in candidates.items():
        ai_rate = counts[True][word] / totals[True]
        human_rate = counts[False][word] / totals[False]
        ratio = (ai_rate + 1e-7) / (human_rate + 1e-7)
        if ratio >= MIN_RATIO and counts[True][word] >= MIN_AI_COUNT:
            kept.append((word, ratio, ai_rate * 1e6, human_rate * 1e6, source))
    kept.sort(key=lambda row: -row[1])
    lines = [
        "# not-ai-lint excess vocabulary; generated by skills/not-ai/validate.py",
        f"# kept: AI/human rate ratio >= {MIN_RATIO} and >= {MIN_AI_COUNT} AI occurrences on the HAP-E-2",
        "# expository training half (human vs claude-haiku-4.5, gpt-5-mini, gpt-4o, llama-3-70b-instruct).",
        "word\tratio\tai_per_1m\thuman_per_1m\tsource",
    ]
    lines += [f"{w}\t{r:.2f}\t{a:.1f}\t{h:.1f}\t{s}" for w, r, a, h, s in kept]
    (DATA / "lexicon.tsv").write_text("\n".join(lines) + "\n")
    return {
        "candidates": len(candidates),
        "kept": len(kept),
        "train_tokens": {"ai": totals[True], "human": totals[False]},
        "top": [f"{w} {r:.1f}x" for w, r, *_ in kept[:25]],
    }


# --- Features ------------------------------------------------------------------

_LEXICON = None


def _init_worker() -> None:
    global _LEXICON
    _LEXICON = lint.load_lexicon(DATA / "lexicon.tsv")


def features(text: str) -> tuple[int, dict[str, float], dict[str, list[str]]]:
    words, findings = lint.analyze(text, _LEXICON)
    matched: dict[str, list[str]] = {}
    for finding in findings:
        matched.setdefault(finding.rule, []).append(finding.match.lower())
    return words, lint.rates(words, findings), matched


def featurize(
    texts: list[str],
) -> list[tuple[int, dict[str, float], dict[str, list[str]]]]:
    with ProcessPoolExecutor(max_workers=12, initializer=_init_worker) as pool:
        return list(pool.map(features, texts, chunksize=64))


RULE_IDS = [rule.id for rule in lint.RULES]


def matrix(feats) -> np.ndarray:
    return np.array(
        [
            [math.log1p(per_k.get(rule, 0.0)) for rule in RULE_IDS]
            for _, per_k, _ in feats
        ]
    )


# --- Fit -----------------------------------------------------------------------


def fit(
    x: np.ndarray, y: np.ndarray, sample_weight: np.ndarray
) -> tuple[float, np.ndarray]:
    """Weighted logistic regression with nonnegative weights on standardized
    features; returns (bias, weights) on the raw log1p-rate scale."""
    sw = sample_weight / sample_weight.sum()
    mu = sw @ x
    sigma = np.sqrt(sw @ (x - mu) ** 2)
    active = sigma > 0
    z_x = np.where(active, (x - mu) / np.where(active, sigma, 1.0), 0.0)

    def loss(params: np.ndarray) -> tuple[float, np.ndarray]:
        bias, w = params[0], params[1:]
        p = 1.0 / (1.0 + np.exp(-(bias + z_x @ w)))
        eps = 1e-12
        nll = -(
            sw @ (y * np.log(p + eps) + (1 - y) * np.log(1 - p + eps))
        ) + L2 * np.sum(w**2)
        grad_z = sw * (p - y)
        return nll, np.concatenate([[grad_z.sum()], z_x.T @ grad_z + 2 * L2 * w])

    bounds = [(None, None)] + [(0.0, None) if a else (0.0, 0.0) for a in active]
    result = minimize(
        loss, np.zeros(x.shape[1] + 1), jac=True, method="L-BFGS-B", bounds=bounds
    )
    if not result.success:
        raise RuntimeError(f"fit failed: {result.message}")
    w_std = result.x[1:]
    w_raw = np.where(active, w_std / np.where(active, sigma, 1.0), 0.0)
    return float(result.x[0] - np.sum(w_raw * mu)), w_raw


def member_table(corpus: list[dict]) -> list[list]:
    """Per-member AI/human rates for the phrase rules on the training split,
    the evidence for which phrases a rule keeps."""
    counts = {True: Counter(), False: Counter()}
    totals = {True: 0, False: 0}
    for row in corpus:
        if not row["train"] or row["genre"] not in EXPOSITORY:
            continue
        totals[row["ai"]] += len(tokens(row["text"]))
        for rule_id, pattern in lint.LEXICAL_RULES:
            if rule_id in {"cadence-contrast", "participial-tail"}:
                continue
            for match in pattern.finditer(row["text"]):
                counts[row["ai"]][(rule_id, match.group(0).lower().strip())] += 1
    table = []
    for key in sorted(set(counts[True]) | set(counts[False])):
        ai = counts[True][key] / totals[True] * 1e6
        human = counts[False][key] / totals[False] * 1e6
        table.append(
            [*key, round(ai, 1), round(human, 1), round((ai + 0.5) / (human + 0.5), 2)]
        )
    return table


# --- Metrics -------------------------------------------------------------------


def auc(scores: np.ndarray, labels: np.ndarray) -> float:
    order = np.argsort(scores, kind="mergesort")
    ranks = np.empty(len(scores))
    sorted_scores = scores[order]
    i = 0
    while i < len(scores):
        j = i
        while j + 1 < len(scores) and sorted_scores[j + 1] == sorted_scores[i]:
            j += 1
        ranks[order[i : j + 1]] = (i + j) / 2 + 1
        i = j + 1
    pos = labels.astype(bool)
    n_pos, n_neg = pos.sum(), (~pos).sum()
    return float((ranks[pos].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    return float(np.corrcoef(ra, rb)[0, 1])


def sign_test(wins: int, losses: int) -> float:
    """Two-sided binomial p-value for wins vs losses at p=0.5 (normal approx for n>50)."""
    n = wins + losses
    if n == 0:
        return 1.0
    if n > 50:
        z = (abs(wins - n / 2) - 0.5) / math.sqrt(n / 4)
        return math.erfc(z / math.sqrt(2))
    k = min(wins, losses)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2**n)


def pairwise(pref_lower: list[tuple[float, float, int]]) -> dict:
    """pref_lower rows: (score_first, score_second, preferred 1|2)."""
    agree = disagree = ties = 0
    for s1, s2, preferred in pref_lower:
        if s1 == s2:
            ties += 1
        elif (s1 < s2) == (preferred == 1):
            agree += 1
        else:
            disagree += 1
    n = agree + disagree
    return {
        "pairs": len(pref_lower),
        "ties": ties,
        "lower_score_preferred": round(agree / n, 3) if n else None,
        "p_value": round(sign_test(agree, disagree), 4),
    }


# --- Evaluations -----------------------------------------------------------------


def score_of(x: np.ndarray, bias: float, w: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-(bias + x @ w)))


def eval_hape(corpus, feats, bias, w) -> dict:
    x = matrix(feats)
    s = score_of(x, bias, w)
    y = np.array([row["ai"] for row in corpus])
    test = np.array([not row["train"] for row in corpus])
    expo = np.array([row["genre"] in EXPOSITORY for row in corpus])
    human = np.array([row["source"] == "human" for row in corpus])
    out = {"per_model_expository": {}, "per_genre": {}, "per_rule_auc_expository": {}}
    for model in sorted({row["source"] for row in corpus} - {"human"}):
        mask = (
            test & expo & (human | np.array([row["source"] == model for row in corpus]))
        )
        out["per_model_expository"][model] = round(auc(s[mask], y[mask]), 3)
    for genre in sorted({row["genre"] for row in corpus}):
        mask = test & np.array([row["genre"] == genre for row in corpus])
        out["per_genre"][genre] = round(auc(s[mask], y[mask]), 3)
    mask = test & expo
    out["all_models_expository"] = round(auc(s[mask], y[mask]), 3)
    for j, rule in enumerate(RULE_IDS):
        if x[mask, j].std() > 0:
            out["per_rule_auc_expository"][rule] = round(auc(x[mask, j], y[mask]), 3)
    return out


def russell_rows(dev: bool) -> list[dict]:
    """Even ids are the dev half (used in fitting), odd ids the test half."""
    data = json.loads((CACHE / "human_detectors.json").read_text())
    return [row for row in data.values() if (int(row["id"]) % 2 == 0) == dev]


def eval_russell(rows: list[dict], bias, w) -> dict:
    feats = featurize([row["article"] for row in rows])
    x = matrix(feats)
    s = score_of(x, bias, w)
    truth = np.array([row["ground_truth"] == "AI-generated" for row in rows])
    expert_ai = []
    for row in rows:
        total = 0.0
        for k in range(1, 6):
            raw = row.get(f"annotator_{k}")
            if not raw:
                continue
            note = ast.literal_eval(raw) if isinstance(raw, str) else raw
            sign = 1.0 if str(note.get("guess", "")).startswith("Machine") else -1.0
            total += sign * float(note.get("confidence") or 1.0)
        expert_ai.append(total)
    expert_ai = np.array(expert_ai)
    by_model = {}
    for model in sorted(
        {
            row["generation_model"]
            for row in rows
            if row["ground_truth"] == "AI-generated"
        }
    ):
        mask = ~truth | np.array([row["generation_model"] == model for row in rows])
        by_model[model] = round(auc(s[mask], truth[mask]), 3)
    per_rule = {}
    for j, rule in enumerate(RULE_IDS):
        if x[:, j].std() > 0:
            per_rule[rule] = round(auc(x[:, j], truth), 3)
    return {
        "articles": len(rows),
        "auc_vs_ground_truth": round(auc(s, truth), 3),
        "auc_by_generator": by_model,
        "spearman_vs_expert_ai_confidence": round(spearman(s, expert_ai), 3),
        "per_rule_auc": per_rule,
    }


def _edit_spans(pre: str, edits_raw) -> list[tuple[int, int]]:
    edits = ast.literal_eval(edits_raw) if isinstance(edits_raw, str) else edits_raw
    spans = []
    for edit in edits or []:
        original = (edit.get("originalText") or "").strip()
        at = pre.find(original) if original else -1
        if at >= 0:
            spans.append((at, at + len(original)))
    return spans


def eval_lamp(bias, w) -> dict:
    rows = json.loads((CACHE / "LAMP-train-val-test.json").read_text())
    pre = featurize([row["preedit"] for row in rows])
    post = featurize([row["postedit"] for row in rows])
    s_pre = score_of(matrix(pre), bias, w)
    s_post = score_of(matrix(post), bias, w)
    drop = int((s_post < s_pre).sum())
    rise = int((s_post > s_pre).sum())
    # Do flags land on text the experts chose to edit?
    inside = total = 0
    covered_chars = all_chars = 0
    lexicon = lint.load_lexicon(DATA / "lexicon.tsv")
    for row in rows:
        text = row["preedit"]
        spans = _edit_spans(text, row["fine_grained_edits"])
        covered = np.zeros(len(text), dtype=bool)
        for a, b in spans:
            covered[a:b] = True
        covered_chars += int(covered.sum())
        all_chars += len(text)
        line_starts = [0] + [m.end() for m in re.finditer("\n", text)]
        _, findings = lint.analyze(text, lexicon)
        for finding in findings:
            offset = line_starts[finding.line - 1] + finding.col - 1
            if offset < len(text):
                total += 1
                inside += int(covered[offset])
    return {
        "pairs": len(rows),
        "score_dropped_after_edit": drop,
        "score_rose_after_edit": rise,
        "unchanged": len(rows) - drop - rise,
        "p_value": round(sign_test(drop, rise), 4),
        "mean_score_pre": round(float(s_pre.mean()) * 100, 1),
        "mean_score_post": round(float(s_post.mean()) * 100, 1),
        "flags": total,
        "flags_inside_expert_edits": round(inside / total, 3) if total else None,
        "text_fraction_inside_edits": round(covered_chars / all_chars, 3),
    }


def eval_wq(bias, w) -> dict:
    out = {}
    for name in ("wq_benchmark", "wq_art-or-artifice"):
        rows = json.loads((CACHE / f"{name}.json").read_text())
        rows = [r for r in rows if str(r.get("reference_preference")) in {"1", "2"}]
        f1 = featurize([r["paragraph1"] for r in rows])
        f2 = featurize([r["paragraph2"] for r in rows])
        s1 = score_of(matrix(f1), bias, w)
        s2 = score_of(matrix(f2), bias, w)
        groups: dict[str, list] = {}
        for r, a, b in zip(rows, s1, s2):
            groups.setdefault(r.get("sample_type") or name, []).append(
                (a, b, int(r["reference_preference"]))
            )
        for group, items in sorted(groups.items()):
            out[f"{name}:{group}"] = pairwise(items)
    return out


def eval_arena(bias, w) -> dict:
    rows = []
    with open(CACHE / "arena55k.csv", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["winner_tie"] == "1":
                continue
            try:
                a = "\n\n".join(x or "" for x in json.loads(row["response_a"]))
                b = "\n\n".join(x or "" for x in json.loads(row["response_b"]))
            except (json.JSONDecodeError, TypeError):
                continue
            rows.append((a, b, 1 if row["winner_model_a"] == "1" else 2))
    fa = featurize([a for a, _, _ in rows])
    fb = featurize([b for _, b, _ in rows])
    sa = score_of(matrix(fa), bias, w)
    sb = score_of(matrix(fb), bias, w)
    items = list(zip(sa, sb, [p for _, _, p in rows]))
    words_a = np.array([n for n, _, _ in fa])
    words_b = np.array([n for n, _, _ in fb])
    similar = np.abs(words_a - words_b) <= 0.1 * np.maximum(
        np.maximum(words_a, words_b), 1
    )
    return {
        "all_decided_pairs": pairwise(items),
        "length_matched_within_10pct": pairwise(
            [it for it, ok in zip(items, similar) if ok]
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Download any missing corpora into the cache and exit (a normal run fetches on first use).",
    )
    parser.add_argument(
        "--skip", nargs="*", default=[], choices=["arena", "wq", "lamp", "russell"]
    )
    args = parser.parse_args()
    fetch()
    if args.fetch:
        return 0
    corpus = hape()
    results: dict = {"date": datetime.now(UTC).date().isoformat()}
    print("[derive] lexicon", file=sys.stderr)
    results["lexicon"] = derive_lexicon(corpus)
    results["phrase_members"] = member_table(corpus)
    print(f"[features] HAP-E-2 {len(corpus)} texts", file=sys.stderr)
    feats = featurize([row["text"] for row in corpus])
    train = np.array([row["train"] and row["genre"] in EXPOSITORY for row in corpus])
    x = matrix(feats)
    y = np.array([row["ai"] for row in corpus], dtype=float)
    # The Russell dev half joins the fit at equal total weight, so a cue that
    # only one corpus era rewards (the em dash) cannot dominate the score.
    dev = russell_rows(dev=True)
    x_dev = matrix(featurize([row["article"] for row in dev]))
    y_dev = np.array(
        [row["ground_truth"] == "AI-generated" for row in dev], dtype=float
    )
    n_train = int(train.sum())
    bias, w = fit(
        np.vstack([x[train], x_dev]),
        np.concatenate([y[train], y_dev]),
        np.concatenate(
            [np.full(n_train, 0.5 / n_train), np.full(len(dev), 0.5 / len(dev))]
        ),
    )
    weights = {rule: round(float(v), 5) for rule, v in zip(RULE_IDS, w) if v > 0}
    (DATA / "weights.json").write_text(
        json.dumps(
            {
                "bias": round(bias, 5),
                "weights": weights,
                "provenance": {
                    "generator": "skills/not-ai/validate.py",
                    "date": results["date"],
                    "train": "HAP-E-2 expository (acad, news, blog), even doc numbers, human chunk 2 vs 4 models;"
                    " plus Russell et al. even ids; each corpus half the total sample weight",
                    "train_texts": n_train + len(dev),
                    "model": f"logistic regression on standardized log1p(per-1000-word rate), weights >= 0, L2 {L2}",
                },
            },
            indent=2,
        )
        + "\n"
    )
    results["weights"] = {"bias": round(bias, 4), **weights}
    results["unscored_rules"] = [rule for rule in RULE_IDS if rule not in weights]
    print("[eval] HAP-E-2 held-out", file=sys.stderr)
    results["hape2_test"] = eval_hape(corpus, feats, bias, w)
    if "russell" not in args.skip:
        print("[eval] Russell expert articles", file=sys.stderr)
        results["russell_test"] = eval_russell(russell_rows(dev=False), bias, w)
        results["russell_dev_used_in_fit"] = eval_russell(dev, bias, w)
    if "lamp" not in args.skip:
        print("[eval] LAMP expert edits", file=sys.stderr)
        results["lamp"] = eval_lamp(bias, w)
    if "wq" not in args.skip:
        print("[eval] WQ pairwise preferences", file=sys.stderr)
        results["wq"] = eval_wq(bias, w)
    if "arena" not in args.skip:
        print("[eval] Arena votes (contrast)", file=sys.stderr)
        results["arena"] = eval_arena(bias, w)
    RESULTS.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
