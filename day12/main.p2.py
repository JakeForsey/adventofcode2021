from collections import defaultdict
from pathlib import Path

import networkx as nx
import matplotlib.pyplot as plt


TEST_INPUT = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
TEST_ANSWER = 36

TEST_INPUT = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""
TEST_ANSWER = 103


def run(lines):
    G = nx.Graph()
    for line in lines:
        n1, n2 = line.split("-")
        assert any([n1.lower() == n1, n2.lower() == n2]),\
            f"At least one of the nodes should be small! ({n1}, {n2})"
        G.add_node(n1)
        G.add_node(n2)
        G.add_edge(n1, n2, weight=-1)

    n = 0
    paths = [
        ["start", n] for n in G["start"]
    ]
    while paths:

        # Filter complete paths
        remaining_paths = []
        for path in paths:
            if path[-1] == "end":
                # print(",".join(path))
                n += 1
            else:
                remaining_paths.append(path)

        # Expand incomplete paths
        paths = remaining_paths
        remaining_paths = []
        for path in paths:
            neighbours = list(G.neighbors(path[-1]))
            for neighbour in neighbours:
                if neighbour == "start":
                    continue
                if neighbour.lower() != neighbour:
                    # We can always add a big cave
                    remaining_paths.append(path + [neighbour])
                else:
                    small_cave_already_visited_twice = max([
                        path.count(n) for n in path
                        if n.lower() == n  # Ignore big caves in this check
                    ]) >= 2
                    if path.count(neighbour) >= 1 and small_cave_already_visited_twice:
                        # Small cave we have visited, or the start node
                        continue
                    else:
                        remaining_paths.append(path + [neighbour])
        paths = remaining_paths
    return n


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
