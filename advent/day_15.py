import itertools
import operator

import numpy as np
import numpy.ma as ma


def part_one(lines, shortest=None):
    cave = [[int(char) for char in line.rstrip("\n")] for line in lines]

    shortest_path = find_shortest(cave=cave, shortest=shortest)
    print(shortest_path[1])
    return shortest_path[0]


def part_one_naive(lines) -> int:
    """
    Find the shortest path by going back from the bottom right and for each previous step,
    see if below or to the right is lowest.

    Huge assumption is that the path always goes down or to the right, but this seems to hold...
    Edit: this assumption was not true anymore for part two
    """
    if isinstance(lines, np.ndarray):
        cave = lines
    else:
        cave = np.array([[int(char) for char in line.rstrip("\n")] for line in lines], dtype=np.uint)

    size = cave.shape[0]

    distances = np.zeros_like(cave)

    # Bottom and right edge: cumulative sums from bottom to top and right to left
    distances[-1, ::-1] = cave[-1, ::-1].cumsum()
    distances[::-1, -1] = cave[::-1, -1].cumsum()

    # Two triangles with minimum from step below and to the right
    print("calculating lower right triangle: ", end="")
    for i in range(size - 2, 0, -1):
        print(i, end=" ")
        col = np.arange(i, size)
        dists = [min(pair) for pair in itertools.pairwise(distances[col[::-1], col])]
        new_col = np.arange(i, size - 1)
        distances[new_col[::-1], new_col] = cave[new_col[::-1], new_col] + dists
    print()

    print("calculating upper left triangle: ", end="")
    for i in range(size, 2, -1):
        print(i - 2, end=" ")
        col = np.arange(0, i)
        dists = [min(pair) for pair in itertools.pairwise(distances[col[::-1], col])]
        new_col = np.arange(0, i - 1)
        distances[new_col[::-1], new_col] = cave[new_col[::-1], new_col] + dists
    print()

    # Start location is not counted, as you never enter it.
    distances[0, 0] = min(distances[0, 1], distances[1, 0])
    print(distances)

    return distances[0, 0]


def full_map(lines, repeat=5):
    """
    Create a full map by repeating the cave to the right and down a number of times,
    each time increasing all nodes with one, and wrapping the value from 9 to 1
    """
    cave = np.array([[int(char) for char in line.rstrip("\n")] for line in lines], dtype=np.uint)
    blocks = [[(cave - 1 + row + col) % 9 + 1 for col in range(0, repeat)] for row in range(0, repeat)]
    return np.block(blocks)


def find_shortest(cave: list[list[int]], risk_level: int = 0, position: tuple[int, int] = (0, 0),
                  path: list[tuple[int, int]] | None = None, shortest: int | None = None) -> tuple[int, list] | None:
    """
    Find the shortest path through the cave by trying all paths (depth first "tree").

    Remember the shortest found so far and stop traversing as soon as the current path is longer.

    This solution is way too slow for the real input...
    """
    if path is None:
        path = []

    (i, j) = position
    risk_level += cave[i][j]

    if shortest and risk_level > shortest:
        # print("Risk too high")
        return None

    next_positions = [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]

    paths = []
    for (m, n) in next_positions:
        if m == len(cave) - 1 and n == len(cave) - 1:
            # print("Found a path!")
            return risk_level, path + [(m, n)]
        if m < 0 or m >= len(cave) or n < 0 or n >= len(cave):
            # print("Outside the cave")
            continue
        if (m, n) in path:
            # print("Already visited")
            continue

        shorter_path = find_shortest(cave=cave, risk_level=risk_level, position=(m, n),
                                     path=path + [position], shortest=shortest)
        if shorter_path:
            shortest = min(shortest, shorter_path[0]) if shortest else shorter_path[0]
            paths.append(shorter_path)

    if paths:
        result = min(paths, key=operator.itemgetter(0))
        print(result[0])
        return result


def part_one_dijkstra(lines):
    if isinstance(lines, np.ndarray):
        cave = lines
    else:
        cave = np.array([[int(char) for char in line.rstrip("\n")] for line in lines], dtype=np.uint)

    return find_distance_dijkstra_masked(cave)


def find_distance_dijkstra_masked(nodes: np.ndarray):
    """
    Find the shortest distance using https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Algorithm
    and Numpy masked array to distinguish visited / unvisited

    I must say, I am disappointed by the performance of masked arrays...
    """

    n = nodes.shape[0]

    # 1. Mark all nodes unvisited. Create a set of all the unvisited nodes called the unvisited set.
    # 2. Assign to every node a tentative distance value: set it to zero for our initial node
    #    and to infinity for all other nodes.
    dist = ma.array(np.full(nodes.shape, np.inf), mask=np.zeros_like(nodes, dtype=bool))
    dist[0, 0] = 0

    # Set the initial node as current.
    r, c = (0, 0)

    # When planning a route, it is actually not necessary to wait until the destination node is "visited" as above:
    # the algorithm can stop once the destination node has the smallest tentative distance among all "unvisited" nodes
    # (and thus could be selected as the next "current").
    while (r, c) != (n - 1, n - 1):

        # 3. For the current node, consider all of its unvisited neighbors and calculate their tentative distances
        #    through the current node. Compare the newly calculated tentative distance to the current assigned value
        #    and assign the smaller one.
        for (rb, cb) in [(r - 1, c), (r, c + 1), (r + 1, c), (r, c - 1)]:
            if 0 <= rb < n and 0 <= cb < n and not dist.mask[rb, cb]:
                through_dist = dist[r, c] + nodes[rb, cb]
                if through_dist < dist[rb, cb]:
                    dist[rb, cb] = through_dist

        # 4. When we are done considering all of the unvisited neighbors of the current node,
        #    mark the current node as visited and remove it from the unvisited set.
        dist[r, c] = ma.masked

        # 6. ..., select the unvisited node that is marked with the smallest tentative distance,
        #    set it as the new current node, and go back to step 3.
        (r, c) = np.unravel_index(dist.argmin(), dist.shape)  # SLOW !!!

        # print(dist)
        print("\r", int(dist.mask.sum() / (n * n) * 100), end="% visited")

    print()
    return dist[n - 1, n - 1]


if __name__ == '__main__':
    with open("../input/day_15.txt") as file:
        print("part one", part_one_naive(file))

    with open("../input/day_15.txt") as file:
        full = full_map(file)
        print(part_one_dijkstra(full))
