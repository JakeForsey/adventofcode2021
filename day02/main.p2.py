from pathlib import Path


TEST_INPUT = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""
TEST_ANSWER = 900


def run(lines):
    depth = 0
    z = 0
    aim = 0
    for line in lines:
        direction, distance = line.split(" ")
        distance = int(distance)
        if direction == "forward":
            z += distance
            depth += aim * distance
        elif direction == "down":
            aim += distance
        elif direction == "up":
            aim -= distance
    return depth * z


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
