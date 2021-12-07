from pathlib import Path
import sys


TEST_INPUT = """16,1,2,0,4,2,7,1,2,14"""
TEST_ANSWER = 37


def run(lines):
    positions = list(map(int, lines[0].split(",")))

    min_fuel = sys.maxsize
    for x in range(min(positions), max(positions)):
        fuel = 0
        for position in positions:
            fuel += abs(position - x)
        if fuel < min_fuel:
            min_fuel = fuel

    return min_fuel


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
