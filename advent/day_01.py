from more_itertools import sliding_window


def part_one(lines):
    numbers = map(int, lines)
    increases = (a < b for (a, b) in sliding_window(numbers, 2))
    return sum(increases)


def part_two(lines):
    numbers = map(int, lines)
    sum_three = (sum(window) for window in sliding_window(numbers, 3))
    increases = (a < b for (a, b) in sliding_window(sum_three, 2))
    return sum(increases)


if __name__ == '__main__':
    with open("../input/day_01.txt") as file:
        print(part_one(file))

    with open("../input/day_01.txt") as file:
        print(part_two(file))
