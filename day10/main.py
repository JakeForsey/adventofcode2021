from pathlib import Path

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
TEST_ANSWER = 26397

POINTS = {
    ")": 3,
    "(": 3,
    "]": 57,
    "[": 57,
    "}": 1197,
    "{": 1197,
    ">": 25137,
    "<": 25137,
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


def process_line(line):
    opened = []
    for char in line:
        if char in CLOSED:
            if CLOSE_TO_OPEN[char] != opened[-1]:
                return POINTS[char]
            opened.pop(-1)

        if char in OPEN:
            opened.append(char)
    return 0


def run(lines):
    points = 0
    for line in lines:
        points += process_line(line)
    return points


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
