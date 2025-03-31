import random
from itertools import accumulate
from bisect import bisect_right


def weighted_random_choice(elements, weights, x=None):
    if len(elements) != len(weights):
        raise ValueError("Elements and weights must have the same length")
    if not elements:
        raise ValueError("Elements list cannot be empty")
    if any(w < 0 for w in weights):
        raise ValueError("Weights must be non-negative")

    cum_weights = list(accumulate(weights))
    total_weight = cum_weights[-1] if cum_weights else 0

    if total_weight <= 0:
        return random.choice(elements)  # если все веса нулевые

    if x is None:
        x = random.random()
    elif not (0 <= x <= 1):
        raise ValueError("x must be in [0, 1]")

    return elements[bisect_right(cum_weights, x * total_weight)]