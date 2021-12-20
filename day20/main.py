from collections import defaultdict
from pathlib import Path


TEST_INPUT = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""
TEST_ANSWER = 35


def pprint(coords):
    (h1, h2), (w1, w2) = min_max(coords)
    print()
    for y in range(h1 - 1, h2 + 2):
        for x in range(w1 - 1, w2 + 2):
            print(coords[(x, y)], end="")
        print()


def yield_kernel(point):
    x, y = point
    for yi in range(-1, 2, 1):
        for xi in range(-1, 2, 1):
            yield x + xi, y + yi


def get_kernel(point, coords):
    kernel = []
    for point in yield_kernel(point):
        if point not in coords:
            kernel.append(None)
        else:
            kernel.append(coords[point])
    return kernel


def value_from_kernel(kernel, enhancements, default_value):
    if all(k is None for k in kernel):
        return default_value
    elif None in kernel:
        return None
    idx = to_index(kernel)
    return enhancements[idx]


def update(coords, enhancements, default_value):
    (h1, h2), (w1, w2) = min_max(coords)

    todo = []
    for y in range(h1 - 2, h2 + 3):
        for x in range(w1 - 2, w2 + 3):
            todo.append((x, y))

    while todo:
        print(len(todo))
        point = todo.pop()
        value = coords.get(point, None)
        if value is not None:
            continue
        kernel = get_kernel(point, coords)
        value = value_from_kernel(kernel, enhancements, default_value)
        if value is None:
            todo.insert(0, point)
        else:
            coords[point] = value
    return next_coords


def min_max(coords):
    ys = [y for (_, y), c in coords.items()]
    xs = [x for (x, y), c in coords.items()]
    return (
        (min(ys), max(ys)),
        (min(xs), max(xs))
    )


def to_binary(kernel):
    kernel = "".join(str(w) for w in kernel)
    return kernel\
        .replace(".", "0")\
        .replace("#", "1")


def to_index(kernel_string):
    return int(to_binary(kernel_string), 2)


def run(lines, debug=False):
    enhancements = lines[0]
    print(len(enhancements))
    coords = defaultdict(lambda: "+")
    for y, row in enumerate(lines[2:]):
        for x, c in enumerate(row):
            coords[(x, y)] = c

    if debug: pprint(coords)

    default_next_idx = 0
    default_value = enhancements[default_next_idx]
    for step in range(2):
        print(f"{step + 1} / 2")
        coords = update(coords, enhancements, default_value)

        if debug: pprint(coords)
        default_next_idx = 512 if default_value == "#" else 0
        default_value = enhancements[default_next_idx]

    return len([c for c in coords.values() if c == "#" or (c == "+" and default == "#")])


def mock(lines):
    return run(lines, debug=True)


def parse_data(data):
    return data.strip().splitlines()


if __name__ == "__main__":
    mock_answer = mock(parse_data(TEST_INPUT))
    print(f"[TEST] Expected answer: {TEST_ANSWER}")
    print(f"[TEST] Actual answer: {mock_answer}")
    print(f"[TEST] {'PASSED' if mock_answer == TEST_ANSWER else 'FAILED'}")

    answer = run(parse_data(Path("input.txt").read_text()))
    print(f"[RUN] answer: {answer}")
    # Guess:
    #  * 5402  (too high)
    #  * 53... (too high)
    #  * 5311  (no comment)
    #  * 5539  (no comment)
