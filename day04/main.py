from pathlib import Path

import numpy as np


TEST_INPUT = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""
TEST_ANSWER = 4512


def run(lines):
    draws = [int(d) for d in lines[0].split(",")]
    boards = "\n".join(lines[1:])
    boards = np.stack([np.fromstring(board, sep=" ").reshape(5, 5) for board in boards.split("\n\n")])
    # boards.shape = (n_boards, 5, 5)

    for i in range(len(draws)):
        masks = np.isin(boards, draws[:i])
        rows = masks.all(axis=1, keepdims=True).any(axis=2).flatten()
        cols = masks.all(axis=2, keepdims=True).any(axis=1).flatten()
        complete = rows | cols
        if complete.any():
            board = boards[complete, :, :]
            mask = masks[complete, :, :]
            return int(board[~mask].sum() * draws[i - 1])


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
