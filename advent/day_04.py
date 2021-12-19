import re

import numpy as np


def part_one(lines) -> int:
    (numbers, cards) = parse_lines(lines)
    marked = np.zeros(cards.shape, dtype=bool)

    # cards = (cards x rows x cols) with numbers
    # marked = (cards x rows x cols) with booleans if they are crossed off
    for nr in numbers:
        marked[cards == nr] = True
        row_bingo = np.all(marked, axis=1)
        col_bingo = np.all(marked, axis=2)
        [card_bingo_index, ] = np.where(np.any(row_bingo | col_bingo, axis=1))
        if len(card_bingo_index):
            card = card_bingo_index[0]
            unmarked = cards[card, ~marked[card]]
            return np.sum(unmarked) * nr


def part_two(lines) -> int:
    (numbers, cards) = parse_lines(lines)
    marked = np.zeros(cards.shape, dtype=bool)

    # cards = (cards x rows x cols) with numbers
    # marked = (cards x rows x cols) with booleans if they are crossed off
    for nr in numbers:
        marked[cards == nr] = True
        row_bingo = np.all(marked, axis=1)
        col_bingo = np.all(marked, axis=2)
        [card_bingo_index, ] = np.where(np.any(row_bingo | col_bingo, axis=1))
        if len(card_bingo_index) == cards.shape[0]:
            card = card_bingo_index[0]
            unmarked = cards[card, ~marked[card]]
            return np.sum(unmarked) * nr
        elif len(card_bingo_index):
            cards = np.delete(cards, card_bingo_index, axis=0)
            marked = np.delete(marked, card_bingo_index, axis=0)


def parse_lines(lines) -> (list[int], np.array):
    lines_iterator = (line.rstrip("\n").strip() for line in lines)

    numbers = next(lines_iterator)

    bingo_cards = [[]]
    for line in lines_iterator:
        if line:
            bingo_cards[-1].append(re.split(r"\s+", line))
        elif bingo_cards[-1]:
            bingo_cards.append([])

    return (
        [int(number) for number in numbers.split(",")],
        np.array(bingo_cards, dtype=np.uint8)
    )


if __name__ == '__main__':
    with open("../input/day_04.txt") as file:
        print(part_one(file))

    with open("../input/day_04.txt") as file:
        print(part_two(file))
