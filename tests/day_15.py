import unittest

from advent.day_15 import *

INPUT = [
    "1163751742\n",
    "1381373672\n",
    "2136511328\n",
    "3694931569\n",
    "7463417111\n",
    "1319128137\n",
    "1359912421\n",
    "3125421639\n",
    "1293138521\n",
    "2311944581\n",
]


class Day15Case(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(40, part_one(INPUT))

    def test_part_one_naive(self):
        self.assertEqual(40, part_one_naive(INPUT))

    def test_part_one_dijkstra(self):
        self.assertEqual(40, part_one_dijkstra(INPUT))

    def test_full_map(self):
        result = full_map(INPUT)
        self.assertEqual(result.shape, (50, 50))
        self.assertEqual(list(result[0, :]), [
            1, 1, 6, 3, 7, 5, 1, 7, 4, 2,
            2, 2, 7, 4, 8, 6, 2, 8, 5, 3,
            3, 3, 8, 5, 9, 7, 3, 9, 6, 4,
            4, 4, 9, 6, 1, 8, 4, 1, 7, 5,
            5, 5, 1, 7, 2, 9, 5, 2, 8, 6
        ])

    def test_part_two(self):
        result = full_map(INPUT)
        self.assertEqual(315, part_one_dijkstra(result))


if __name__ == '__main__':
    unittest.main()
