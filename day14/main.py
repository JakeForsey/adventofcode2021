from collections import Counter
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
TEST_ANSWER = 1588


def run(lines):
    start = lines[0]
    rules = []
    for line in lines[2:]:
        rules.append(line.split(" -> "))

    ret = start
    for _ in range(10):
        chunks = []
        insertions = []
        for i in range(len(ret) - 1):
            chunks.append(ret[i: i + 2])
            insertions.append("")

        for (pattern, insertion) in rules:
            for idx in [n for n, chunk in enumerate(chunks) if chunk==pattern]:
                insertions[idx] = insertion

        ret = ""
        for chunk, insertion in zip(chunks, insertions):
            ret += chunk[0] + insertion
        ret += chunks[-1][1]

    counter = Counter(ret)
    return max(counter.values()) - min(counter.values())


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
