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
TEST_ANSWER = 7


def run(lines):
    lines = [int(i) for i in lines]
    out = 0
    last_line = lines[0]
    for line in lines[1:]:
        if line > last_line:
            out += 1
        last_line = line
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
