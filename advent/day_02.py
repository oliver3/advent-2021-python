class Submarine:
    def __init__(self):
        self.depth = 0
        self.horizontal = 0

    def forward(self, units: int):
        self.horizontal += units

    def down(self, units: int):
        self.depth += units

    def up(self, units: int):
        self.depth -= units

    def exec(self, instruction: str):
        (command, units) = instruction.split(" ")
        getattr(self, command)(int(units))


def part_one(lines):
    sub = Submarine()

    for line in lines:
        sub.exec(line)

    return sub.depth * sub.horizontal


class ComplicatedSubmarine(Submarine):
    def __init__(self):
        super().__init__()
        self.aim = 0

    def forward(self, units: int):
        self.horizontal += units
        self.depth += self.aim * units

    def down(self, units: int):
        self.aim += units

    def up(self, units: int):
        self.aim -= units


def part_two(lines):
    sub = ComplicatedSubmarine()

    for line in lines:
        sub.exec(line)

    return sub.depth * sub.horizontal


if __name__ == '__main__':
    with open("../input/day_02.txt") as file:
        print(part_one(file))

    with open("../input/day_02.txt") as file:
        print(part_two(file))
