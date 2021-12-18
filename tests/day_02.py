import unittest
from advent.day_02 import *

INPUT = ["forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2"]


class Day02Case(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(150, part_one(INPUT))

    def test_part_two(self):
        self.assertEqual(900, part_two(INPUT))


if __name__ == '__main__':
    unittest.main()
