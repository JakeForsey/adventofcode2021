from pathlib import Path


TEST_INPUT = """2199943210
3987894921
9856789892
8767896789
9899965678"""
TEST_ANSWER = 15


def get(i, j, depth):
    if i >= len(depth):
        return 99
    if j >= len(depth[0]):
        return 99
    if i < 0:
        return 99
    if j < 0:
        return 99
    return depth[i][j]


def run(lines):
    depth = [[int(i) for i in l] for l in lines]

    risk = 0
    for i in range(len(depth)):
        for j in range(len(depth[0])):
            val = depth[i][j]
            other_vals = [
                get(i + 1, j, depth),  # above
                get(i, j - 1, depth),  # left
                get(i, j + 1, depth),  # right
                get(i - 1, j, depth),  # below
            ]
            if val < min(other_vals):
                risk += val + 1

    return risk


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
