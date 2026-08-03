import pytest

from run_quality.length_ratio import LengthRatioPolicy


def test_reciprocal_deviations_have_the_same_factor() -> None:
    policy = LengthRatioPolicy(center_ratio=1.0, add_k=10.0, factor_995=2.0)

    longer = policy.score(90, 140)  # Smoothed ratio 1.5.
    shorter = policy.score(140, 90)  # Smoothed ratio 2/3.

    assert longer.deviation_factor == pytest.approx(1.5)
    assert shorter.deviation_factor == pytest.approx(1.5)


def test_positive_smoothing_is_more_tolerant_of_short_rows() -> None:
    policy = LengthRatioPolicy(center_ratio=1.0, add_k=10.0, factor_995=1.5)

    short = policy.score(5, 10)
    long = policy.score(500, 1000)

    assert short.deviation_factor == pytest.approx(4 / 3)
    assert not short.outlier
    assert long.deviation_factor > 1.9
    assert long.outlier


def test_smoothing_preserves_a_nonunit_center_at_every_length() -> None:
    policy = LengthRatioPolicy(center_ratio=1.5, add_k=1.0, factor_995=1.1)

    assert policy.score(4, 6).relative_ratio == pytest.approx(1.0)
    assert policy.score(400, 600).relative_ratio == pytest.approx(1.0)


def test_expected_integer_bounds_match_outlier_decision() -> None:
    policy = LengthRatioPolicy(center_ratio=1.0, add_k=10.0, factor_995=1.5)
    lower, upper = policy.expected_output_bounds(90)

    assert (lower, upper) == (57, 140)
    assert not policy.score(90, lower).outlier
    assert not policy.score(90, upper).outlier
    assert policy.score(90, lower - 1).outlier
    assert policy.score(90, upper + 1).outlier


def test_fit_uses_median_center_and_empirical_nearest_rank() -> None:
    lengths = [(90, 90), (90, 90), (90, 140), (140, 90)]
    policy = LengthRatioPolicy.fit(lengths, add_k=10.0, coverage=0.75)

    assert policy.center_ratio == pytest.approx(1.0)
    assert sum(not policy.score(*pair).outlier for pair in lengths) >= 3


def test_text_lengths_are_unicode_codepoints() -> None:
    policy = LengthRatioPolicy(center_ratio=1.0, add_k=1.0, factor_995=2.0)

    result = policy.score_text("a🙂", "猫")

    assert result.unit == "unicode_codepoint"
    assert result.input_length == 2
    assert result.output_length == 1


def test_precomputed_token_counts_use_an_identified_unit() -> None:
    policy = LengthRatioPolicy(
        center_ratio=1.0,
        factor_995=1.5,
        unit="token:google/translategemma-12b-it@revision",
    )

    result = policy.score(10, 12)

    assert policy.add_k == 0.5
    assert result.unit == policy.unit
    with pytest.raises(ValueError, match="score_text"):
        policy.score_text("source", "output")


@pytest.mark.parametrize(
    "kwargs",
    [
        {"center_ratio": 0.0, "add_k": 1.0, "factor_995": 1.0},
        {"center_ratio": 1.0, "add_k": 0.0, "factor_995": 1.0},
        {"center_ratio": 1.0, "add_k": 1.0, "factor_995": 0.9},
    ],
)
def test_invalid_policy_parameters_are_rejected(kwargs: dict[str, float]) -> None:
    with pytest.raises(ValueError):
        LengthRatioPolicy(**kwargs)
