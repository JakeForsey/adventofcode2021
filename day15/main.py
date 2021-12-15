from pathlib import Path

import networkx as nx


TEST_INPUT = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""
TEST_ANSWER = 40
PPRINT = False


def adjacent(y, x):
    yield y, x + 1
    yield y, x - 1
    yield y + 1, x
    yield y - 1, x


def run(lines):
    coords = {}
    for y, line in enumerate(lines):
        for x, risk in enumerate(line):
            coords[(y, x)] = int(risk)

    h, w = len(lines), len(lines[0])
    G = nx.DiGraph()
    for y in range(h):
        for x in range(w):
            if (y, x) not in coords:
                continue

            G.add_node((y, x))

            for y2, x2 in adjacent(y, x):
                risk = coords.get((y2, x2), None)
                if risk is not None:
                    G.add_edge((y, x), (y2, x2), risk=risk)

    path = nx.shortest_path(G, (0, 0), (h - 1, w - 1), weight="risk")
    risk = 0
    # Ignore the risk of the start cell.
    for y, x in path[1:]:
        risk += coords[(y, x)]

    if PPRINT:
        for y in range(h):
            for x in range(w):
                risk = coords[(y, x)]
                if (y, x) in path:
                    print("\033[94m" + str(risk) + "\033[0m", end="")
                else:
                    print(risk, end="")
            print()

    return risk


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


# guesses: 584
