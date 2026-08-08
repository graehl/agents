"""Length-ratio review checks for row-wise text transformations.

The policy deliberately exposes a multiplicative deviation factor rather than
assuming raw ratios are normally distributed.  Positive additive smoothing
makes short rows more tolerant while its effect vanishes as input length
grows.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from statistics import median


@dataclass(frozen=True)
class LengthRatioScore:
    """One source/output pair scored against a length-ratio policy."""

    unit: str
    input_length: int
    output_length: int
    smoothed_ratio: float
    relative_ratio: float
    deviation_factor: float
    expected_output_length: tuple[int, int]
    outlier: bool

    def as_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["expected_output_length"] = list(self.expected_output_length)
        return result


@dataclass(frozen=True, kw_only=True)
class LengthRatioPolicy:
    """A reciprocal-symmetric empirical coverage interval.

    ``center_ratio`` is the typical smoothed output/input ratio,
    ``add_k`` is added to both counts in the policy's named unit, and ``factor_995`` is the
    multiplicative deviation factor covering the policy's calibration set at
    ``coverage`` (99.5% by default).
    """

    center_ratio: float
    factor_995: float
    add_k: float = 0.5
    coverage: float = 0.995
    unit: str = "unicode_codepoint"

    def __post_init__(self) -> None:
        for name, value in (
            ("center_ratio", self.center_ratio),
            ("add_k", self.add_k),
            ("factor_995", self.factor_995),
            ("coverage", self.coverage),
        ):
            if not math.isfinite(value):
                raise ValueError(f"{name} must be finite")
        if self.center_ratio <= 0:
            raise ValueError("center_ratio must be positive")
        if self.add_k <= 0:
            raise ValueError("add_k must be positive")
        if self.factor_995 < 1:
            raise ValueError("factor_995 must be at least 1")
        if not 0 < self.coverage < 1:
            raise ValueError("coverage must be strictly between 0 and 1")
        if not self.unit.strip():
            raise ValueError("unit must be nonempty")

    @property
    def ratio_bounds(self) -> tuple[float, float]:
        return self.center_ratio / self.factor_995, self.center_ratio * self.factor_995

    def relative_ratio(self, input_length: int, output_length: int) -> float:
        """Return a center-preserving ratio whose expected value is one.

        Dividing the output count by ``center_ratio`` puts both counts in
        input-side units before adding the same pseudocount to each.
        """
        _validate_length("input_length", input_length)
        _validate_length("output_length", output_length)
        return (output_length / self.center_ratio + self.add_k) / (
            input_length + self.add_k
        )

    def smoothed_ratio(self, input_length: int, output_length: int) -> float:
        """Return the center-preserving ratio in output/input units."""
        return self.center_ratio * self.relative_ratio(input_length, output_length)

    def expected_output_bounds(self, input_length: int) -> tuple[int, int]:
        _validate_length("input_length", input_length)
        denominator = input_length + self.add_k
        lower = max(
            0,
            math.ceil(
                self.center_ratio * (denominator / self.factor_995 - self.add_k) - 1e-12
            ),
        )
        upper = max(
            0,
            math.floor(
                self.center_ratio * (self.factor_995 * denominator - self.add_k) + 1e-12
            ),
        )
        return lower, upper

    def score(self, input_length: int, output_length: int) -> LengthRatioScore:
        relative_ratio = self.relative_ratio(input_length, output_length)
        deviation = max(relative_ratio, 1 / relative_ratio)
        return LengthRatioScore(
            unit=self.unit,
            input_length=input_length,
            output_length=output_length,
            smoothed_ratio=self.center_ratio * relative_ratio,
            relative_ratio=relative_ratio,
            deviation_factor=deviation,
            expected_output_length=self.expected_output_bounds(input_length),
            outlier=deviation > self.factor_995,
        )

    def score_text(self, source: str, output: str) -> LengthRatioScore:
        """Score Python Unicode codepoint counts (not bytes or graphemes)."""
        if self.unit != "unicode_codepoint":
            raise ValueError("score_text requires unit='unicode_codepoint'")
        return self.score(len(source), len(output))

    def as_dict(self) -> dict[str, object]:
        return {
            "center_ratio": self.center_ratio,
            "add_k": self.add_k,
            "factor_995": self.factor_995,
            "coverage": self.coverage,
            "unit": self.unit,
        }

    @classmethod
    def fit(
        cls,
        lengths: Iterable[tuple[int, int]],
        *,
        add_k: float = 0.5,
        coverage: float = 0.995,
        unit: str = "unicode_codepoint",
    ) -> LengthRatioPolicy:
        """Fit a median center and nearest-rank empirical coverage factor."""
        if not math.isfinite(add_k) or add_k <= 0:
            raise ValueError("add_k must be positive and finite")
        if not 0 < coverage < 1:
            raise ValueError("coverage must be strictly between 0 and 1")

        pairs = list(lengths)
        if not pairs:
            raise ValueError("at least one length pair is required")

        raw_ratios = []
        for input_length, output_length in pairs:
            _validate_length("input_length", input_length)
            _validate_length("output_length", output_length)
            if input_length > 0:
                raw_ratios.append(output_length / input_length)
        if not raw_ratios:
            raise ValueError("at least one pair with nonzero input length is required")

        center = median(raw_ratios)
        if center <= 0:
            raise ValueError("the fitted center ratio must be positive")
        policy = cls(
            center_ratio=center,
            add_k=add_k,
            factor_995=1,
            coverage=coverage,
            unit=unit,
        )
        deviations = sorted(
            max(
                policy.relative_ratio(input_length, output_length),
                1 / policy.relative_ratio(input_length, output_length),
            )
            for input_length, output_length in pairs
        )
        rank = max(0, math.ceil(coverage * len(deviations)) - 1)
        return cls(
            center_ratio=center,
            add_k=add_k,
            factor_995=deviations[rank],
            coverage=coverage,
            unit=unit,
        )


def _validate_length(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
