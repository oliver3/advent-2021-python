import unittest
from advent.day_03 import *

INPUT = ["00100", "11110", "10110", "10111", "10101", "01111", "00111", "11100", "10000", "11001", "00010", "01010", ]


class Day03Case(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(198, part_one(INPUT))

    def test_part_two(self):
        self.assertEqual(230, part_two(INPUT))


if __name__ == '__main__':
    unittest.main()
