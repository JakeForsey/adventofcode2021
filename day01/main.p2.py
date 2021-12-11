from pathlib import Path


TEST_INPUT = """199
200
208
210
200
207
240
269
260
263"""
TEST_ANSWER = 5


def run(lines):
    lines = [int(i) for i in lines]
    out = 0
    last_window = None
    for i in range(0, len(lines)):
        if i + 3 > len(lines):
            break
        window = sum(lines[i: i + 3])
        if last_window is not None and window > last_window:
            out += 1
        last_window = window

    return out


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
