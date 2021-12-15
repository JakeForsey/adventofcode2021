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
TEST_ANSWER = 315
PPRINT = False


def adjacent(y, x):
    yield y, x + 1
    yield y, x - 1
    yield y + 1, x
    yield y - 1, x


def modify_risk(risk, modifier):
    return ((risk + modifier - 1) % 9) + 1


def run(lines):
    orig_h, orig_w = len(lines), len(lines[0])
    h, w = orig_h * 5, orig_w * 5

    coords = {}
    for y, line in enumerate(lines):
        for x, risk in enumerate(line):
            risk = int(risk)
            for i in range(0, 5):
                for j in range(0, 5):
                    coords[(
                        y + (orig_h * i),
                        x + (orig_w * j)
                    )] = modify_risk(risk, i + j)

    G = nx.DiGraph()
    for y in range(h):
        for x in range(w):
            G.add_node((y, x))
            for y2, x2 in adjacent(y, x):

                risk2 = coords.get((y2, x2), None)
                if risk2 is not None:
                    G.add_edge((y, x), (y2, x2), risk=risk2)

                risk = coords.get((y, x), None)
                if risk is not None:
                    G.add_edge((y2, x2), (y, x), risk=risk)

    path = nx.shortest_path(G, (0, 0), (h - 1, w - 1), weight="risk")
    risk = 0
    # Ignore the risk of the start cell.
    for y, x in path[1:]:
        risk += coords[(y, x)]

    if PPRINT:
        for y in range(h):
            for x in range(w):
                r = coords[(y, x)]
                if (y, x) in path:
                    print("\033[94m" + str(r) + "\033[0m", end="")
                else:
                    print(r, end="")
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
