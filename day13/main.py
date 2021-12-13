from pathlib import Path

import numpy as np


TEST_INPUT = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""
TEST_ANSWER = 16  # 17 (typo in puzzle description)


def pad(a, shape):
    y_, x_ = shape
    y, x = a.shape
    y_pad = (y_ - y)
    x_pad = (x_ - x)
    return np.pad(
        a,
        (
            (y_pad, 0),
            (x_pad, 0)
        ),
        mode='constant',
        constant_values=0,
    )


def run(lines):
    coords = set()
    at_fold = False
    folds = []
    for line in lines:
        if line == "":
            at_fold = True
            continue
        if not at_fold:
            x, y = line.split(",")
            coords.add((int(y), int(x)))
        else:
            part = line.split(" ")[-1]
            axis, position = part.split("=")
            folds.append((axis, int(position)))

    paper = np.zeros(
        shape=(
            max([y for y, _ in coords]) + 1,
            max([x for _, x in coords]) + 1,
        ),
        dtype=bool
    )
    for y, x in coords:
        paper[y, x] = True

    for axis, position in folds:
        # Ignore the row / col that is being folded.
        if axis == "x":
            p1, p2 = paper[:, :position], np.fliplr(paper[:, position + 1:])
        elif axis == "y":
            p1, p2 = paper[:position, :], np.flipud(paper[position + 1:, :])
        else:
            raise AssertionError("Unreachable")

        # If the page has an even number of rows / columns then we can get a shape mismatch here...from
        # Pad as required.
        if p1.shape != p2.shape:
            if sum(p1.shape) < sum(p2.shape):
                p1 = pad(p1, p2.shape)
            else:
                p2 = pad(p2, p1.shape)

        paper = p1 | p2

    return paper.sum()


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
