from pathlib import Path
from statistics import median

TEST_INPUT = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""
TEST_ANSWER = 288957

POINTS = {
    ")": 1,
    "(": 1,
    "]": 2,
    "[": 2,
    "}": 3,
    "{": 3,
    ">": 4,
    "<": 4,
}
OPEN_TO_CLOSE = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
OPEN = OPEN_TO_CLOSE.keys()
CLOSE_TO_OPEN = {v: k for k, v in OPEN_TO_CLOSE.items()}
CLOSED = CLOSE_TO_OPEN.keys()


def is_corrupted(line):
    opened = []
    for char in line:
        if char in CLOSED:
            if CLOSE_TO_OPEN[char] != opened[-1]:
                return True
            opened.pop(-1)

        if char in OPEN:
            opened.append(char)
    return False


def finish(line):
    opened = []
    for char in line:
        if char in CLOSED:
            opened.pop(-1)
        if char in OPEN:
            opened.append(char)
    return [OPEN_TO_CLOSE[char] for char in opened[::-1]]


def run(lines):
    scores = []
    for line in lines:
        if is_corrupted(line):
            continue

        remainder = finish(line)
        score = 0
        for char in remainder:
            score = score * 5
            score = score + POINTS[char]
        scores.append(score)
    return median(scores)


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
