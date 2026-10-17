"""Finite checks of the paper's scalar proofs; no neural-model experiments."""

import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


def geometric(mu: Fraction, length: int) -> Fraction:
    return sum((mu**k for k in range(length)), Fraction(0))


def reset_trajectory(mu: Fraction, horizon: int, resets: tuple[int, ...]) -> Fraction:
    velocity = Fraction(0)
    displacement = Fraction(0)
    for step in range(horizon):
        velocity = Fraction(1) if step in resets else mu * velocity
        assert abs(velocity) <= 1
        displacement += velocity
    return displacement


def check_reset_optimum() -> int:
    cases = 0
    for mu in (Fraction(0), Fraction(1, 10), Fraction(1, 2), Fraction(9, 10)):
        for horizon in range(1, 10):
            assert reset_trajectory(mu, horizon, ()) == 0
            for budget in range(1, horizon + 1):
                a, remainder = divmod(horizon, budget)
                predicted = (budget - remainder) * geometric(mu, a)
                predicted += remainder * geometric(mu, a + 1)
                observed = max(
                    reset_trajectory(mu, horizon, resets)
                    for resets in itertools.combinations(range(horizon), budget)
                )
                assert observed == predicted, (mu, horizon, budget)
                cases += 1
    return cases


def check_nesterov() -> int:
    cases = 0
    for mu in (Fraction(0), Fraction(1, 2), Fraction(9, 10)):
        for horizon in (1, 2, 10, 100):
            impulse = 1 / (1 + mu)
            velocity = Fraction(0)
            displacement = Fraction(0)
            for step in range(horizon):
                gradient = impulse if step == 0 else Fraction(0)
                velocity = mu * velocity + gradient
                direction = gradient + mu * velocity
                assert abs(direction) <= 1
                displacement += direction
            predicted = geometric(mu, horizon + 1) / (1 + mu)
            assert displacement == predicted
            cases += 1
    return cases


def adam_impulse(start: int, horizon: int) -> float:
    beta1, beta2 = 0.9, 0.999
    first, second = 0.0, 0.0
    total = 0.0
    initial_step = None
    for step in range(start, start + horizon):
        gradient = 1.0 if step == start else 0.0
        first = beta1 * first + (1 - beta1) * gradient
        second = beta2 * second + (1 - beta2) * gradient**2
        displacement = (first / (1 - beta1**step)) / math.sqrt(
            second / (1 - beta2**step)
        )
        if initial_step is None:
            initial_step = displacement
        k = step - start
        correction = math.sqrt(1 - beta2**step) / (1 - beta1**step)
        initial_correction = math.sqrt(1 - beta2**start) / (1 - beta1**start)
        closed_form = (beta1 / math.sqrt(beta2)) ** k
        closed_form *= correction / initial_correction
        assert math.isclose(displacement / initial_step, closed_form, rel_tol=1e-12)
        assert displacement / initial_step <= 1 + 1e-12
        total += displacement / initial_step
    return total


def rmsprop_suppression() -> dict[str, float]:
    alpha, horizon, fraction = 0.99, 100, 0.5
    ratio = 1 + (fraction**-2 - 1) * alpha**-horizon
    second, displacement = ratio, 0.0
    for step in range(1, horizon + 1):
        second = alpha * second + (1 - alpha)
        update = 1 / math.sqrt(second)
        expected = 1 / math.sqrt(1 + (ratio - 1) * alpha**step)
        assert math.isclose(update, expected, rel_tol=1e-12)
        assert update <= fraction + 1e-12
        displacement += update
    deviation = horizon - displacement
    assert deviation >= (1 - fraction) * horizon - 1e-12
    return {"state_ratio": ratio, "endpoint_deviation": deviation}


def adam_reset_optimum(horizon: int, budget: int) -> dict[str, object]:
    beta1, beta2 = 0.9, 0.999
    ratio = beta1 / math.sqrt(beta2)
    corrections = [0.0] + [
        math.sqrt(1 - beta2**step) / (1 - beta1**step) for step in range(1, horizon + 1)
    ]
    gains = {}
    for start in range(1, horizon + 1):
        total, largest = 0.0, 0.0
        for end in range(start, horizon + 1):
            relative = ratio ** (end - start) * corrections[end] / corrections[start]
            total += relative
            largest = max(largest, relative)
            gains[start, end] = total / largest
    values = [[0.0] * (horizon + 1)]
    starts = [[()] * (horizon + 1)]
    for count in range(1, budget + 1):
        row = [-math.inf] * (horizon + 1)
        paths = [()] * (horizon + 1)
        for end in range(count, horizon + 1):
            best, start = max(
                (values[count - 1][start - 1] + gains[start, end], start)
                for start in range(count, end + 1)
            )
            row[end] = best
            paths[end] = starts[count - 1][start - 1] + (start,)
        values.append(row)
        starts.append(paths)
    best_count = max(range(budget + 1), key=lambda count: values[count][horizon])
    if horizon <= 8:
        exhaustive = 0.0
        for count in range(1, budget + 1):
            for choices in itertools.combinations(range(1, horizon + 1), count):
                ends = tuple(start - 1 for start in choices[1:]) + (horizon,)
                gain = sum(
                    gains[start, end] for start, end in zip(choices, ends, strict=True)
                )
                exhaustive = max(exhaustive, gain)
        assert math.isclose(values[best_count][horizon], exhaustive, rel_tol=1e-12)
    return {
        "maximum": values[best_count][horizon],
        "reset_steps": starts[best_count][horizon],
    }


def nonlinear_counterexample() -> Fraction:
    cap, eta, delta = Fraction(1), Fraction(1), Fraction(1, 10)
    x, reference = Fraction(0), Fraction(0)
    for step in range(100):
        gradient = -(cap / eta) * min(max(x / delta, -1), 1)
        if step == 0:
            gradient = -delta / eta
        update = -eta * gradient
        assert abs(update) <= cap
        assert abs(gradient) <= cap / eta
        x += update
        reference_gradient = -(cap / eta) * min(max(reference / delta, -1), 1)
        reference -= eta * reference_gradient
    assert reference == 0
    assert x == delta + 99 * cap
    return x


def bounded_residual_check() -> int:
    cases = 0
    for factors in itertools.product(
        (Fraction(1, 2), Fraction(1), Fraction(2)), repeat=4
    ):
        for errors in itertools.product(
            (Fraction(-1), Fraction(0), Fraction(1)), repeat=4
        ):
            observed = Fraction(0)
            for factor, error in zip(factors, errors, strict=True):
                observed = factor * observed + error
            propagated = sum(
                abs(error) * math.prod(factors[index + 1 :])
                for index, error in enumerate(errors)
            )
            assert abs(observed) <= propagated
            cases += 1
    return cases


def main() -> None:
    for horizon in range(1, 9):
        for budget in range(1, min(horizon, 3) + 1):
            adam_reset_optimum(horizon, budget)
    report = {
        "kind": "finite_math_checks_not_neural_experiments",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "exact_reset_optimum_cases": check_reset_optimum(),
        "exact_nesterov_cases": check_nesterov(),
        "exact_residual_cases": bounded_residual_check(),
        "momentum_h100_cap1": {
            str(b): float(
                (b - 100 % b) * geometric(Fraction(9, 10), 100 // b)
                + (100 % b) * geometric(Fraction(9, 10), 100 // b + 1)
            )
            for b in (1, 2, 5, 10)
        },
        "adam_bias_corrected_tail_h100_in_first_step_units": {
            str(start): adam_impulse(start, 100) for start in (1, 10, 100, 1000)
        },
        "adam_arbitrary_moment_resets_h100_cap1": {
            str(budget): adam_reset_optimum(100, budget) for budget in (1, 2, 5)
        },
        "rmsprop_h100_alpha099_max_fraction_half": rmsprop_suppression(),
        "nonlinear_one_intervention_h100": str(nonlinear_counterexample()),
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
