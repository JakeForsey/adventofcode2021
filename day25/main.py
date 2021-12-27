from pathlib import Path


TEST_INPUT = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""
TEST_ANSWER = 58


def pprint(south, east, w, h):
    for y in range(0, h):
        for x in range(0, w):
            if (x, y) in south:
                print("v", end="")
            elif (x, y) in east:
                print(">", end="")
            else:
                print(".", end="")
        print()


def run(lines):
    w, h = len(lines[0]), len(lines)
    south = set()
    east = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "v":
                south.add((x, y))
            elif c == ">":
                east.add((x, y))

    i = 0
    while True:
        moves = 0

        next_east = set()
        for x, y in east:
            next_point = ((x + 1) % w, y)
            if next_point not in south and next_point not in east:
                next_east.add(next_point)
                moves += 1
            else:
                next_east.add((x, y))
        east = set(next_east)

        next_south = set()
        for x, y in south:
            next_point = (x, (y + 1) % h)
            if next_point not in south and next_point not in east:
                next_south.add(next_point)
                moves += 1
            else:
                next_south.add((x, y))
        south = set(next_south)

        i += 1
        if moves == 0:
            break
    return i


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
