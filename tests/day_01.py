import unittest
from advent.day_01 import *

INPUT = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]


class Day01Case(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(7, part_one(INPUT))

    def test_part_two(self):
        self.assertEqual(5, part_two(INPUT))


if __name__ == '__main__':
    unittest.main()
