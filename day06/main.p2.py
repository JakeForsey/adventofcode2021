from collections import Counter
from pathlib import Path


TEST_INPUT = """3,4,3,1,2"""
TEST_ANSWER = 26984457539


def run(lines):
    fish = list(map(int, lines[0].split(",")))
    fish_counter = Counter(fish)

    for _ in range(256):
        temp = Counter()
        for f, count in fish_counter.items():
            if f > 0:
                temp[f - 1] = count
        temp[6] += fish_counter[0]
        temp[8] = fish_counter[0]

        fish_counter = temp

    return sum(v for k, v in fish_counter.items())


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
