import unittest

from advent.day_14 import *

INPUT = [
    "NNCB\n",
    "\n",
    "CH -> B\n",
    "HH -> N\n",
    "CB -> H\n",
    "NH -> C\n",
    "HB -> C\n",
    "HC -> B\n",
    "HN -> C\n",
    "NN -> C\n",
    "BH -> H\n",
    "NC -> B\n",
    "NB -> B\n",
    "BN -> B\n",
    "BB -> N\n",
    "BC -> B\n",
    "CC -> N\n",
    "CN -> C\n",
]


class Day14Case(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(1588, solve(INPUT))

    def test_part_one_numpy(self):
        self.assertEqual(1588, solve_numpy(INPUT))

    def test_part_one_grow_rules(self):
        self.assertEqual(1588, solve_grow_rules(INPUT))

    def test_part_one_pairs(self):
        self.assertEqual(1588, solve_unordered_pairs(INPUT))

    def test_part_two(self):
        self.assertEqual(2_188_189_693_529, solve_unordered_pairs(INPUT, 40))

    def test_part_two_numpy(self):
        self.assertEqual(2_188_189_693_529, solve_unordered_pairs_numpy(INPUT, 40))


if __name__ == '__main__':
    unittest.main()
