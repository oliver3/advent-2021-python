import re

import numpy as np


def part_one(lines):
    paper, folds = parse_lines(lines)
    return np.sum(fold_paper(folds[0], paper))


def part_two(lines):
    paper, folds = parse_lines(lines)
    for fold in folds:
        paper = fold_paper(fold, paper)

    return paper


def fold_paper(fold, paper):
    if fold[0] == 'x':
        return paper[0:fold[1], :] + paper[:fold[1]:-1, :]
    elif fold[0] == 'y':
        return paper[:, 0:fold[1]] + paper[:, :fold[1]:-1]


def parse_lines(lines) -> (list[int], np.array):
    dots = []
    folds = []
    lines_iterator = (line.rstrip("\n").strip() for line in lines)

    for line in lines_iterator:
        if line:
            (x, y) = line.split(",")
            dots.append((int(x), int(y)))
        else:
            break

    for fold in lines_iterator:
        (axis, location) = re.match(r"fold along ([xy])=(\d+)", fold).groups()
        folds.append((axis, int(location)))

    paper = np.zeros((max(x for (x, _) in dots) + 1, max(y for (_, y) in dots) + 1), dtype=bool)
    for dot in dots:
        paper[dot] = True

    return paper, folds


if __name__ == '__main__':
    with open("../input/day_13.txt") as file:
        print(part_one(file))

    with open("../input/day_13.txt") as file:
        folded_paper = part_two(file)

        for row in folded_paper.T.tolist():
            for dot in row:
                print("\u2588" if dot else "\u00B7", end="")
            print()

