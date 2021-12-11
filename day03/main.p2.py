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
TEST_ANSWER = 230


def filter_lines(lines, predicate):
    filtered_lines = lines[:]
    n_bits = len(lines[0])
    for i in range(n_bits):
        total = 0
        for line in filtered_lines:
            total += int(line[i])

        filtered_lines2 = []
        for line in filtered_lines:
            if predicate(int(line[i]), total / len(filtered_lines)):
                filtered_lines2.append(line)
        filtered_lines = filtered_lines2[:]
        if len(filtered_lines) == 1:
            break
    return filtered_lines[0]


def run(lines):
    ogr = filter_lines(lines, lambda a, b: a == int(b >= 0.5))
    csr = filter_lines(lines, lambda a, b: a != int(b >= 0.5))
    return int(ogr, 2) * int(csr, 2)


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
