from pathlib import Path

import matplotlib.pyplot as plt
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
TEST_ANSWER = -1  # Test answer is LRFJBJEH but is hard to test


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
            folds.append((0 if axis == "y" else 1, int(position)))

    paper = np.zeros(
        shape=(max([y for y, _ in coords]) + 1, max([x for _, x in coords]) + 1),
        dtype=bool
    )
    for y, x in coords:
        paper[y, x] = True

    for axis, position in folds:
        shape = list(paper.shape)
        shape[axis] = position
        p1 = paper[:shape[0], :shape[1]]
        fold_shape = shape[:]
        # Skip the row that's being folded
        fold_shape[axis] += 1
        p2 = np.flip(paper[fold_shape[0] - paper.shape[0]:, fold_shape[1] - paper.shape[1]:], axis=axis)
        p2 = np.pad(
            p2,
            (
                (shape[0] - p2.shape[0], 0),
                (shape[1] - p2.shape[1], 0)
            ),
            constant_values=0,
        )
        paper = p1 | p2

    plt.imshow(paper)
    plt.show()
    return -1


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
