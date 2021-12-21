from collections import defaultdict, Counter
from pathlib import Path
from pprint import pprint
import itertools


TEST_INPUT = """Player 1 starting position: 4
Player 2 starting position: 8"""
TEST_ANSWER = 444356092776315


def move(pos, steps):
    next_pos = pos + steps
    if next_pos > 10:
        next_pos = next_pos % 10
        if next_pos == 0:
            next_pos = 10
    assert 0 < next_pos < 11, f"{pos=}, {steps=}, {next_pos=}"
    return next_pos


class Player:
    def __init__(self, pid, pos):
        self.pid = pid
        self.pos = pos

    @classmethod
    def from_str(cls, string):
        parts = string.split(" ")
        return cls(parts[1], int(parts[-1]))


def run(lines):
    p1, p2 = list(map(Player.from_str, lines))
    possible_rolls = list(itertools.combinations_with_replacement([1, 2, 3], 3))
    rolls_permutations = {
        rolls: len(set(list(itertools.permutations(rolls, 3))))
        for rolls in possible_rolls
    }
    results = {
        "1": defaultdict(lambda: defaultdict(int)),
        "2": defaultdict(lambda: defaultdict(int)),
    }
    todo = [
        (p1.pid, p1.pos, 0, 0, rolls, rolls_permutations[rolls]) for rolls in possible_rolls
    ] + [
        (p2.pid, p2.pos, 0, 1, rolls, rolls_permutations[rolls]) for rolls in possible_rolls
    ]
    while todo:
        pid, pos, score, turn, rolls, k = todo.pop()
        if score >= 21:
            continue
        pos = move(pos, sum(rolls))
        turn += 2  # Other player moves as well
        score += pos
        results[pid][turn][score >= 21] += k
        for rolls in possible_rolls:
            todo.append((pid, pos, score, turn, rolls, k * rolls_permutations[rolls]))

    p1 = p2 = 0
    for turn in range(22):
        p1 += results["1"][turn][True] * results["2"][turn - 1][False]
        p2 += results["2"][turn][True] * results["1"][turn - 1][False]

    return max(p1, p2)


def mock(lines):
    return run(lines)


def parse_data(data):
    return data.strip().splitlines()


if __name__ == "__main__":
    mock_answer = mock(parse_data(TEST_INPUT))
    print(f"[TEST] Expected answer: {TEST_ANSWER}")
    print(f"[TEST] Actual answer:   {mock_answer}")
    print(f"[TEST] {'PASSED' if mock_answer == TEST_ANSWER else 'FAILED'}")

    answer = run(parse_data(Path("input.txt").read_text()))
    print(f"[RUN] answer: {answer}")
