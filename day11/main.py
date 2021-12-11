from collections import defaultdict
from itertools import permutations
from pathlib import Path


TEST_INPUT = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""
TEST_ANSWER = 1656


def neighbors(x, y):
    for dx, dy in list(set(permutations([0, 1, 1, -1, -1], 2))):
        yield x + dx, y + dy


def run(lines):
    board = defaultdict(lambda: -999999999)
    for y, line in enumerate(lines):
        for x, o in enumerate(line):
            board[(x, y)] = int(o)

    flashes = 0
    for step in range(100):
        to_flash = []
        has_flashed = set()

        # Increment board and accumulate initial flashes
        for (x, y), o in board.items():
            if o == 9:
                to_flash.append((x, y))
                board[(x, y)] = 0
            else:
                board[(x, y)] += 1

        # Compute chain reaction
        while to_flash:
            x, y = to_flash.pop()
            flashes += 1
            board[(x, y)] = 0
            has_flashed.add((x, y))

            for x, y in neighbors(x, y):
                if (x, y) in has_flashed:
                    continue
                o = board[(x, y)]
                if o == 9:
                    to_flash.append((x, y))
                    board[(x, y)] = 0
                else:
                    board[(x, y)] += 1

    return flashes


def mock(lines):
    return run(lines)


def parse_data(data):
    return data.strip().splitlines()


if __name__ == "__main__":
    mock_answer = mock(parse_data(TEST_INPUT))
    print(f"[TEST] Expected answer: {TEST_ANSWER}")
    print(f"[TEST] Actual answer: {mock_answer}")
    print(f"[TEST] {'PASSED' if mock_answer == TEST_ANSWER else 'FAILED'}")

    answer = run(parse_data(Path("input.txt").read_text()))
    print(f"[RUN] answer: {answer}")
