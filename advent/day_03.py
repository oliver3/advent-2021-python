from functools import reduce
from typing import Iterable

import numpy as np


def binary_value(bits):
    """Calculates the value that these bits represent."""
    return reduce(lambda value, b: value * 2 + b, bits)


def part_one(lines: Iterable[str]) -> int:
    report = np.array([list(map(int, line.rstrip("\n"))) for line in lines], dtype=np.uint8)

    most_common = report.mean(axis=0).round().astype(np.uint8)
    gamma = binary_value(most_common)
    epsilon = binary_value(1 - most_common)

    return gamma * epsilon


def part_two(lines: Iterable[str]) -> int:
    report = np.array([list(map(int, line.rstrip("\n"))) for line in lines], dtype=np.uint8)

    oxygen_generator_rating = binary_value(find_single_row_per_column(report, most_common))
    co2_scrubber_rating = binary_value(find_single_row_per_column(report, least_common))
    return oxygen_generator_rating * co2_scrubber_rating


def most_common(column):
    """Returns a boolean index array for the most common binary value in the column"""
    [zeros, ones] = np.bincount(column)
    return column == (1 if ones >= zeros else 0)


def least_common(column):
    """Returns a boolean index array for the least common binary value in the column"""
    [zeros, ones] = np.bincount(column)
    return column == (0 if zeros <= ones else 1)


def find_single_row_per_column(report, col_predicate):
    """Find a single remaining row by filtering on each column successively using a column predicate"""
    remaining = report.copy()

    for c in range(0, remaining.shape[1]):
        remaining = remaining[col_predicate(remaining[:, c]), :]
        if remaining.shape[0] == 1:
            return remaining[0, :]


if __name__ == '__main__':
    with open("../input/day_03.txt") as file:
        print(part_one(file))

    with open("../input/day_03.txt") as file:
        print(part_two(file))
