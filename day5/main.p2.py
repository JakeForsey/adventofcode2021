from collections import defaultdict
from pathlib import Path


TEST_INPUT = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""
TEST_ANSWER = 12


def interpolate(x1, y1, x2, y2):
    m = max(abs(x1 - x2), abs(y1 - y2))
    if x1 == x2:
        dx = 0
    elif x1 > x2:
        dx = -1
    else:
        dx = 1

    if y1 == y2:
        dy = 0
    elif y1 > y2:
        dy = -1
    else:
        dy = 1

    for x, y in zip(
        [dx * i + x1 for i in range(m + 1)],
        [dy * i + y1 for i in range(m + 1)],
    ):
        yield x, y


def run(lines):
    overlaps = defaultdict(int)

    for line in lines:
        p1, p2 = line.split(" -> ")
        x1, y1 = map(int, p1.split(","))
        x2, y2 = map(int, p2.split(","))

        for x, y in interpolate(x1, y1, x2, y2):
            overlaps[x, y] += 1

    return sum([1 for overlap in overlaps.values() if overlap >= 2])


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
