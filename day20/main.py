from collections import defaultdict
from pathlib import Path
import sys

sys.setrecursionlimit(100000)

TEST_INPUT = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""
TEST_ANSWER = 35


def pprint(coords):
    (h1, h2), (w1, w2) = min_max(coords)
    print()
    for y in range(h1, h2 + 1):
        for x in range(w1, w2 + 1):
            print(coords[(x, y)], end="")
        print()


def yield_kernel(point):
    x, y = point
    for yi in range(-1, 2, 1):
        for xi in range(-1, 2, 1):
            yield x + xi, y + yi


def min_max(coords):
    ys = [y for (_, y), c in coords.items()]
    xs = [x for (x, y), c in coords.items()]
    return (
        (min(ys), max(ys)),
        (min(xs), max(xs))
    )


def to_index(kernel):
    def _to_binary():
        return "".join(str(w) for w in kernel) \
            .replace(".", "0") \
            .replace("#", "1")

    return int(_to_binary(), 2)


def get_value(coords, point, enhancements):
    kernel = []
    for kernel_point in yield_kernel(point):
        if kernel_point not in coords:
            # Skip points too close to the edge
            return None
        kernel.append(coords[kernel_point])
    return enhancements[to_index(kernel)]


def run(lines, debug=False):
    enhancements = lines[0]

    # Start with a large, padded board
    h, w = len(lines[2:]), len(lines[2])
    padding = 10
    coords = {}
    for y in range(-padding, h + padding):
        for x in range(-padding, w + padding):
            coords[(x, y)] = "."

    # Override the padding where data is available
    for y, row in enumerate(lines[2:]):
        for x, c in enumerate(row):
            coords[(x, y)] = c

    if debug: pprint(coords)

    # Enhance twice
    for step in range(2):
        new_coords = {}
        for point in coords:
            value = get_value(coords, point, enhancements)
            if value is not None:
                new_coords[point] = value

        coords = new_coords
        if debug: pprint(coords)

    return len([c for c in coords.values() if c == "#"])


def mock(lines):
    return run(lines, debug=True)


def parse_data(data):
    return data.strip().splitlines()


if __name__ == "__main__":
    mock_answer = mock(parse_data(TEST_INPUT))
    print(f"[TEST] Expected answer: {TEST_ANSWER}")
    print(f"[TEST] Actual answer: {mock_answer}")
    print(f"[TEST] {'PASSED' if mock_answer == TEST_ANSWER else 'FAILED'}")

    answer = run(parse_data(Path("input.txt").read_text()))
    print(f"[RUN] answer: {answer}")
