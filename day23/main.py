from pathlib import Path
import sys
import time
from typing import NamedTuple
from heapq import heappush, heappop
import random


TEST_INPUT = """\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""
TEST_ANSWER = 12521

COST = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}
GRAPH = {
    "H0": {("H1", 1)},
    "H1": {("H0", 1), ("A1", 2), ("H3", 2)},

    "A2": {("A1", 1)},
    "A1": {("A2", 1), ("H1", 2), ("H3", 2)},

    "H3": {("H1", 2), ("A1", 2), ("B1", 2), ("H5", 2)},

    "B2": {("B1", 1)},
    "B1": {("B2", 1), ("H3", 2), ("H5", 2)},

    "H5": {("H3", 2), ("B1", 2), ("C1", 2), ("H7", 2)},

    "C2": {("C1", 1)},
    "C1": {("C2", 1), ("H5", 2), ("H7", 2)},

    "H7": {("H5", 2), ("C1", 2), ("D1", 2), ("H9", 2)},

    "D2": {("D1", 1)},
    "D1": {("D2", 1), ("H7", 2), ("H9", 2)},

    "H9": {("H7", 2), ("D1", 2), ("H10", 2)},
    "H10": {("H9", 1)},
}


class Unit(NamedTuple):
    pos: str
    type: str
    stationary: bool
    allow: str


def stopping_points(unit):
    return {
        unit.type + "1",
        unit.type + "2",
        "H0",
        "H1",
        "H3",
        "H5",
        "H7",
        "H9",
        "H10"
    }


def hash_state(unit_positions):
    return hash(frozenset(unit_positions.items()))


def pprint(unit_positions):
    assert len(unit_positions) == 8
    print()
    board = [
        "...........",
        "  . . . .  ",
        "  . . . .  ",
    ]
    board = [[c for c in row] for row in board]
    for unit in unit_positions.values():
        c = unit.pos[0]
        if c == "A":
            x = 2
            y = int(unit.pos[1:])
        elif c == "B":
            x = 4
            y = int(unit.pos[1:])
        elif c == "C":
            x = 6
            y = int(unit.pos[1:])
        elif c == "D":
            x = 8
            y = int(unit.pos[1:])
        elif c == "H":
            x = int(unit.pos[1:])
            y = 0
        else:
            raise AssertionError(f"Unreachable {c}, {unit}")

        board[y][x] = unit.type
    print("\n".join(["".join(row) for row in board]))


def possible_moves(unit, unit_positions):
    # TODO: If you get this right, pretty sure you get a star you numpty!
    # TODO: Use nx to find all paths to targets? Then check if those paths are clear of units
    visited = {unit.pos}
    targets = stopping_points(unit)
    if unit.allow:
        targets.add(unit.allow + "1")
        targets.add(unit.allow + "2")

    todo = set(GRAPH[unit.pos])
    while todo:
        pos, mod = todo.pop()

        if pos in visited:
            continue

        if pos in unit_positions:
            continue

        if pos in targets:
            targets.remove(pos)
            visited.add(pos)
            yield pos, mod

        for next_pos, next_mod in GRAPH[pos]:
            if next_pos in unit_positions:
                continue
            if next_pos in visited:
                continue
            visited.add(next_pos)
            todo.add((next_pos, mod + next_mod))

    # for pos, mod in GRAPH[unit.pos]:
    #     if pos in unit_positions:
    #         # Can't move onto a position with another unit on it
    #         continue
    #
    #     # If the unit is in the hallway, and he stop, and the next position is
    #     # in the hallway
    #     if unit.pos.startswith("H") and unit.stationary and pos.startswith("H"):
    #         continue
    #
    #     if pos[0] != "H" and unit.type != pos[0] and pos[0] != unit.allow:
    #         continue
    #
    #     # Moving into a sack that already contains a unit that shouldnt be in there
    #     if unit.pos.startswith("H") and pos[0] == unit.type and f"{pos[0]}2" in unit_positions and unit_positions[f"{pos[0]}2"].type != pos[0]:
    #         continue
    #
    #     yield pos, mod


def step(cost, unit, move, unit_positions):
    unit_positions = {
        u.pos: Unit(u.pos, u.type, True, u.allow) for p, u in unit_positions.items()
        if p != unit.pos
    }
    next_pos, mod = move
    unit_positions[next_pos] = Unit(next_pos, unit.type, False, unit.allow if next_pos[0] != "H" and unit.allow else "")
    cost += (COST[unit.type] * mod)
    return cost, unit_positions


def complete(unit_positions):
    return len([u for u in unit_positions.values() if u.pos[0] == u.type])


def run(lines):
    unit_positions = {}
    for y, line in enumerate(lines[2:]):
        for x, c in enumerate(line):
            x -= 1
            if c in ("A", "B", "C", "D"):
                if x == 2:
                    pos = f"A{y + 1}"
                    unit_positions[pos] = Unit(pos, c, False, "A")
                elif x == 4:
                    pos = f"B{y + 1}"
                    unit_positions[pos] = Unit(pos, c, False, "B")
                elif x == 6:
                    pos = f"C{y + 1}"
                    unit_positions[pos] = Unit(pos, c, False, "C")
                elif x == 8:
                    pos = f"D{y + 1}"
                    unit_positions[pos] = Unit(pos, c, False, "D")

    pprint(unit_positions)

    visited = {}
    todo = []
    for unit in unit_positions.values():
        for move in possible_moves(unit, unit_positions):
            next_cost, next_unit_positions = step(0, unit, move, unit_positions)
            visited[hash_state(next_unit_positions)] = next_cost
            heappush(
                todo,
                (
                    # Ordered by
                    next_cost,
                    random.random(),

                    # Required
                    1,  # depth
                    next_cost,
                    next_unit_positions
                )
            )

    max_complete = 0
    best_cost = sys.maxsize
    i = 0
    start = time.time()
    print("Starting...")
    while todo:
        i += 1
        *_, depth, cost, unit_positions = heappop(todo)

        if i % 10_000 == 0:
            print(f"{i=}, {max_complete=}, {best_cost=}, {cost=}, {depth=}, complete={complete(unit_positions)}, todo={len(todo)}, secs={time.time() - start}")
            pprint(unit_positions)
            start = time.time()

        n_complete = complete(unit_positions)
        if n_complete > max_complete:
            max_complete = n_complete

        if n_complete == 8:
            if cost < best_cost:
                best_cost = cost
            continue

        # if depth > 25:
        #     continue

        for unit in unit_positions.values():
            for move in possible_moves(unit, unit_positions):
                next_cost, next_unit_positions = step(cost, unit, move, unit_positions)

                hashed_state = hash_state(next_unit_positions)
                previous_cost_at_state = visited.get(hashed_state, sys.maxsize)
                if next_cost <= previous_cost_at_state:
                    visited[hashed_state] = next_cost
                    heappush(
                        todo,
                        (
                            # Ordered by
                            next_cost,
                            random.random(),

                            # Required
                            depth + 1,
                            next_cost,
                            next_unit_positions
                        )
                    )
    print(i)
    return best_cost


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

