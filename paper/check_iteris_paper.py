"""Reproduce the finite checks for Sections 4--6 of the Iteris manuscript."""

from collections import Counter, deque
from fractions import Fraction
from itertools import permutations, product
from math import factorial


# The manuscript's stroke table, using 1, 2, 3, 4, and 6 for the stroke labels.
STROKES = tuple(
    frozenset(strokes)
    for strokes in ((), (1,), (2,), (3,), (4,), (1, 4), (6,), (1, 6), (2, 6), (1, 2, 6))
)
DIGITS = range(10)
DIGIT_PATH = (1, 5, 4, 0, 2, 8, 9, 7, 6)
SUCCESSOR_COSTS = (1, 2, 2, 2, 1, 3, 1, 2, 1)


def require(condition, description):
    if not condition:
        raise AssertionError(description)


def digit_distances():
    """Construct the graph and check all digit distances by breadth-first search."""
    hamming = tuple(
        tuple(len(STROKES[first] ^ STROKES[last]) for last in DIGITS)
        for first in DIGITS
    )
    neighbors = tuple(
        tuple(last for last in DIGITS if hamming[first][last] == 1)
        for first in DIGITS
    )
    degree_sum = sum(map(len, neighbors))
    require(degree_sum == 26, "The digit graph must have 13 edges")
    distances = []
    for first in DIGITS:
        reached = {first: 0}
        queue = deque([first])
        while queue:
            digit = queue.popleft()
            for neighbor in neighbors[digit]:
                if neighbor not in reached:
                    reached[neighbor] = reached[digit] + 1
                    queue.append(neighbor)
        require(len(reached) == 10, "The digit graph must be connected")
        distances.append(tuple(reached[last] for last in DIGITS))

    require(tuple(distances) == hamming, "Every graph distance must equal Hamming distance")
    diameter = max(map(max, distances))
    diametral_pairs = [
        (first, last)
        for first in DIGITS
        for last in range(first + 1, 10)
        if distances[first][last] == diameter
    ]
    require(diameter == 4, "The digit graph must have diameter 4")
    require(diametral_pairs == [(3, 9), (4, 9), (5, 8)], "Unexpected diametral pairs")
    require(4 * 10**3 * degree_sum // 2 == 52_000, "Unexpected node graph edge count")
    require(4 * diameter == 16, "Unexpected node graph diameter")
    print(f"Graph: 13 digit edges, diameter {diameter}, diametral pairs {diametral_pairs}")
    print("Fourfold product: 10,000 vertices, 52,000 edges, diameter 16")
    return distances


def word_distance(first, last, distances):
    return sum(distances[a][b] for a, b in zip(first, last))


def check_carry(width, words, distances):
    costs = Counter()
    for first, last in zip(words, words[1:]):
        cost = word_distance(first, last, distances)
        nines = 0
        for digit in reversed(first):
            if digit != 9:
                break
            nines += 1
        digit = first[-1 - nines]
        require(cost == 3 * nines + SUCCESSOR_COSTS[digit], f"Wrong carry cost at {first}")
        costs[cost] += 1

    expected_costs = {
        3 * nines + local_cost: count * 10 ** (width - nines - 1)
        for nines in range(width)
        for local_cost, count in [(1, 4), (2, 4), (3, 1)]
    }
    require(costs == expected_costs, f"Wrong carry distribution for width {width}")
    steps = len(words) - 1
    require(sum(costs.values()) == steps, f"Wrong step count for width {width}")
    total = sum(cost * count for cost, count in costs.items())
    mean = Fraction(total, steps)
    variance = Fraction(sum(cost**2 * count for cost, count in costs.items()), steps) - mean**2
    expected_variance = Fraction(14, 9) - Fraction(9 * width**2 * 10**width, steps**2)
    require(total == 2 * steps - 3 * width, f"Wrong total for width {width}")
    require(variance == expected_variance, f"Wrong variance for width {width}")

    largest_cost = max(costs)
    maximizing_steps = [
        ("".join(map(str, a)), "".join(map(str, b)))
        for a, b in zip(words, words[1:])
        if word_distance(a, b, distances) == largest_cost
    ]
    expected_maximum = [("5" + "9" * (width - 1), "6" + "0" * (width - 1))]
    require(largest_cost == 3 * width, f"Wrong maximum for width {width}")
    require(maximizing_steps == expected_maximum, f"Wrong maximizing steps for width {width}")
    print(
        f"Width {width} carry: {steps:,} steps, total {total:,}, mean {mean}, "
        f"variance {variance}, maximum {largest_cost} at {maximizing_steps[0]}"
    )
    if width == 4:
        print(f"Node carry histogram: {dict(sorted(costs.items()))}")


def serpentine(words, width):
    """Traverse copies of DIGIT_PATH from the all-1 corner to the all-6 corner."""
    if width == 0:
        return [()]
    suffixes = serpentine(words, width - 1)
    return [
        (digit,) + suffix
        for i, digit in enumerate(words)
        for suffix in (reversed(suffixes) if i % 2 else suffixes)
    ]


def constructed_order(width):
    """Visit the digit-3 masks in binary reflected Gray order."""
    result = []
    for index in range(2**width):
        mask = index ^ (index >> 1)
        fixed = tuple(bool(mask & (1 << position)) for position in range(width))
        group = serpentine(DIGIT_PATH, width - sum(fixed))
        for free in reversed(group) if index % 2 else group:
            digits = iter(free)
            result.append(tuple(3 if fixed_here else next(digits) for fixed_here in fixed))
    return result


def check_order(width, words, distances):
    parity = Counter(sum(len(STROKES[digit]) for digit in word) % 2 for word in words)
    imbalance = (-2) ** width
    require(parity[0] - parity[1] == imbalance, f"Wrong parity difference for width {width}")
    require(parity[0] == (10**width + imbalance) // 2, f"Wrong even count for width {width}")
    require(parity[1] == (10**width - imbalance) // 2, f"Wrong odd count for width {width}")
    order = constructed_order(width)
    require(len(order) == len(words) and set(order) == set(words), "Order must visit each word once")
    costs = Counter(word_distance(a, b, distances) for a, b in zip(order, order[1:]))
    require(costs == {1: 10**width - 2**width, 2: 2**width - 1}, "Unexpected join costs")
    closing_cost = word_distance(order[-1], order[0], distances)
    require(closing_cost == 2, "The closing join must cost two strokes")
    open_cost = sum(cost * count for cost, count in costs.items())
    cyclic_cost = open_cost + closing_cost
    require(open_cost == 10**width + 2**width - 2, "Unexpected open order cost")
    require(cyclic_cost == 10**width + 2**width, "Unexpected cyclic order cost")
    print(
        f"Width {width} order: even {parity[0]:,}, odd {parity[1]:,}, "
        f"open {open_cost:,}, cyclic {cyclic_cost:,}"
    )


def check_assignments(distances):
    counts = Counter()
    for permutation in permutations(range(1, 10)):
        order = (0,) + permutation + (0,)
        cost = sum(distances[a][b] for a, b in zip(order, order[1:]))
        counts[cost] += 1
    adopted_cost = sum(distances[a][b] for a, b in zip(DIGITS, (*range(1, 10), 0)))
    better = sum(count for cost, count in counts.items() if cost < adopted_cost)
    require(sum(counts.values()) == factorial(9), "All 9! assignments must be counted")
    require(adopted_cost == 18 and min(counts) == 12, "Unexpected assignment costs")
    require(better == 18_192, "Unexpected number of assignments that beat the adopted cost")
    print(f"Relabelings: {better:,} of {sum(counts.values()):,} cost less than {adopted_cost}")
    print(f"Cycle cost histogram: {dict(sorted(counts.items()))}")


def main():
    distances = digit_distances()
    for width in range(1, 5):
        words = list(product(DIGITS, repeat=width))
        check_carry(width, words, distances)
        check_order(width, words, distances)
    check_assignments(distances)
    print("All checks passed.")


if __name__ == "__main__":
    main()
