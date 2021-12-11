from pathlib import Path


TEST_INPUT = """3,4,3,1,2"""
TEST_ANSWER = 5934


def run(lines):
    fish = list(map(int, lines[0].split(",")))
    for _ in range(80):
        for i, f in enumerate(fish[:]):
            if f == 0:
                fish.append(8)
                fish[i] = 6
            else:
                fish[i] -= 1
    return len(fish)


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
