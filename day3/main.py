from pathlib import Path


TEST_INPUT = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""
TEST_ANSWER = 198


def run(lines):
    n_bits = len(lines[0])
    mean_bits = []
    for i in range(n_bits):
        mean_bits.append(sum([int(line[i]) for line in lines]) / len(lines))

    gamma_rate = "".join(["0" if i < 0.5 else "1" for i in mean_bits])
    epsilon_rate = "".join(["0" if i > 0.5 else "1" for i in mean_bits])
    return int(gamma_rate, 2) * int(epsilon_rate, 2)


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
