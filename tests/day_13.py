import unittest
from advent.day_13 import *

INPUT = [
    "6,10\n",
    "0,14\n",
    "9,10\n",
    "0,3\n",
    "10,4\n",
    "4,11\n",
    "6,0\n",
    "6,12\n",
    "4,1\n",
    "0,13\n",
    "10,12\n",
    "3,4\n",
    "3,0\n",
    "8,4\n",
    "1,10\n",
    "2,14\n",
    "8,10\n",
    "9,0\n",
    "\n",
    "fold along y=7\n",
    "fold along x=5\n",
]


class Day04Case(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(17, part_one(INPUT))

    def test_part_two(self):
        self.assertEqual([
            [True, True, True, True, True],
            [True, False, False, False, True],
            [True, False, False, False, True],
            [True, False, False, False, True],
            [True, True, True, True, True],
            [False, False, False, False, False],
            [False, False, False, False, False],
        ], part_two(INPUT).T.tolist())


if __name__ == '__main__':
    unittest.main()
