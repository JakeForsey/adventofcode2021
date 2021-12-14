import math
from collections import defaultdict
from pathlib import Path


TEST_INPUT = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""
TEST_ANSWER = 2188189693529


def run(lines):
    start = lines[0]
    rules = {}
    for line in lines[2:]:
        chunk, insertion = (line.split(" -> "))
        rules[chunk] = insertion

    final = defaultdict(int)
    for i in range(len(start) - 1):
        final[start[i: i + 2]] += 1

    for _ in range(40):
        counts = final.copy()
        for chunk, count in counts.items():
            insertion = rules.get(chunk, None)
            if insertion is None:
                continue

            final[chunk] -= count
            final[chunk[0] + insertion] += count
            final[insertion + chunk[1]] += count

    # Convert back to letters, not chunks of letters
    counts = defaultdict(int)
    for chunk, count in final.items():
        counts[chunk[0]] += count
        counts[chunk[1]] += count

    # Chunks overlap, so divide by two
    result = (max(counts.values()) - min(counts.values())) / 2
    return math.ceil(result)


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
