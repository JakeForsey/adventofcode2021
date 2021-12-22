from pathlib import Path

import numpy as np

TEST_INPUT1 = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10
"""
TEST_ANSWER1 = 39

TEST_INPUT2 = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682"""
TEST_ANSWER2 = 590784

TEST_INPUT = TEST_INPUT2
TEST_ANSWER = TEST_ANSWER2


def to_range(string):
    return list(map(int, string[2:].split("..")))


def run(lines):
    coords = set()
    for line in lines:
        cmd, ranges = line.split(" ")
        cmd = cmd == "on"
        xx, yy, zz = list(map(to_range, ranges.split(",")))

        if all(-50 <= i <= 50 for i in xx)\
            and all(-50 <= i <= 50 for i in yy)\
            and all(-50 <= i <= 50 for i in zz):

            for x in range(xx[0], xx[1] + 1):
                for y in range(yy[0], yy[1] + 1):
                    for z in range(zz[0], zz[1] + 1):
                        if cmd:
                            coords.add((x, y, z))
                        else:
                            try:
                                coords.remove((x, y, z))
                            except KeyError:
                                pass

    return len(coords)


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
