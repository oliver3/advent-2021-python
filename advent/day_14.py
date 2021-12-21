import math
from collections import defaultdict, Counter
from itertools import pairwise
from typing import Iterator

import numpy as np
from more_itertools import sliding_window
from numpy.linalg import matrix_power


def solve(lines, steps=10):
    """ Solve the polymerization naively """

    polymer, rules = parse_lines(lines)

    for _ in range(steps):
        polymer = grow(rules, polymer)

    sorted_by_count = Counter(polymer).most_common()
    return sorted_by_count[0][1] - sorted_by_count[-1][1]


def grow(insertion_rules: dict[str, str], polymer: str) -> str:
    """ Use the insertion rules to grow the polymer one step """

    insertions = [insertion_rules[a + b] for (a, b) in pairwise(polymer)]
    new_polymer = zip(polymer, insertions + [""])
    return "".join(a + b for (a, b) in new_polymer)


def solve_grow_rules(lines, steps=10):
    """ Solve the polymerization by growing the rules instead of the polymer -- not faster.."""

    polymer, rules = parse_lines(lines)

    grow_rules = {pair: pair for pair in rules.keys()}

    for _ in range(steps):
        for (pair, grown_pair) in grow_rules.items():
            grow_rules[pair] = grow(rules, grown_pair)

    grow_rules = {pair: grown_pair[1:-1] for (pair, grown_pair) in grow_rules.items()}
    polymer = grow(grow_rules, polymer)
    sorted_by_count = Counter(polymer).most_common()

    return sorted_by_count[0][1] - sorted_by_count[-1][1]


def solve_numpy(lines, steps=10):
    """ Solve the polymerization by using numpy with insertions -- slightly faster """

    polymer, rules = parse_lines(lines)
    elements = list(Counter(rules.values()).keys())
    elements.sort()

    polymer = np.array([elements.index(c) for c in polymer], dtype=np.uint8)
    rules = np.array([[elements.index(rules[a + b]) for b in elements] for a in elements], dtype=np.uint8)

    for step in range(steps):
        insertions = rules[polymer[:-1], polymer[1:]]
        polymer = np.insert(polymer, np.arange(1, len(polymer)), insertions)

    counts = np.bincount(polymer)
    return np.max(counts) - np.min(counts)


def solve_unordered_pairs(lines, steps=10):
    """ Solve the polymerization by keeping a running count of all pairs instead of the polymer in order -- fast! """

    polymer, rules = parse_lines(lines)

    polymer_pairs = Counter((a + b for (a, b) in sliding_window(polymer, 2)))
    rules_pairs = {pair: [pair[0] + insert, insert + pair[1]] for (pair, insert) in rules.items()}

    for i in range(steps):
        new_pairs = defaultdict(int)
        for (pair, n) in polymer_pairs.items():
            for insert_pair in rules_pairs[pair]:
                new_pairs[insert_pair] += n
        polymer_pairs = new_pairs

    # Count elements
    elements = defaultdict(int)
    for ((a, b), n) in polymer_pairs.items():
        elements[a] += n
        elements[b] += n

    # elements on either side are not counted twice, add one to be able to divide all by two
    elements[polymer[0]] += 1
    elements[polymer[-1]] += 1

    sorted_elements = sorted(elements.items(), key=lambda el: -el[1])
    return sorted_elements[0][1] // 2 - sorted_elements[-1][1] // 2


def solve_unordered_pairs_numpy(lines, steps=10):
    """ Solve the polymerization with matrix algebra, inspired by population matrix -- fastest!! """

    polymer, rules = parse_lines(lines)
    rules_pairs = {pair: (pair[0] + insert, insert + pair[1]) for (pair, insert) in rules.items()}

    # Create vector for the template polymer and matrix for the from-to pairs
    all_pairs = sorted(rules.keys())
    polymer_array = np.array([polymer.count(pair) for pair in all_pairs])
    rules_array = np.array(
        [[(pair_to in rules_pairs[pair_from]) for pair_to in all_pairs] for pair_from in all_pairs],
        dtype=int
    )

    # Linear Algebra ftw!
    rules_array = matrix_power(rules_array, steps)
    polymer_array = polymer_array.dot(rules_array)

    # Count individual elements
    n_elements = int(math.sqrt(len(all_pairs)))
    all_elements = [el for (_, el) in all_pairs[:n_elements]]
    element_count = np.sum(polymer_array.reshape(n_elements, n_elements), axis=0)
    # Sum axis=0 will add all elements at the right side of a pair,
    # so we have to add one for the first element in the template!
    element_count[all_elements.index(polymer[0])] += 1
    return max(element_count) - min(element_count)


def parse_lines(lines: Iterator[str]) -> (str, dict[str, str]):
    line_iter = (line.rstrip("\n") for line in lines)
    polymer = next(line_iter)
    next(line_iter)

    rules = defaultdict(lambda: "")
    for line in line_iter:
        (pair, insert) = line.split(" -> ")
        rules[pair] = insert

    return polymer, rules


if __name__ == '__main__':
    with open("../input/day_14.txt") as file:
        print(solve(file))

    with open("../input/day_14.txt") as file:
        print(solve_unordered_pairs_numpy(file, 40))
