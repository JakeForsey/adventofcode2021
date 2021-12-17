from pathlib import Path

import matplotlib.pyplot as plt


TEST_INPUT = """target area: x=20..30, y=-10..-5"""
TEST_ANSWER = 112
TEST_ANGLES = """23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
8,-2    27,-8   30,-5   24,-7
"""


def step(x, y, dx, dy):
    if dx == 0:
        dxx = 0
    elif dx > 0:
        dxx = 1
    elif dx < 0:
        dxx = -1
    else:
        raise AssertionError("Unreachable")
    return (
       x + dx, y + dy,
       dx - dxx, dy - 1
    )


def simulate(dx, dy, x_bounds, y_bounds):
    x = y = 0
    path = [(x, y)]
    while x_bounds[0] < x < x_bounds[1] and y_bounds[0] < y < y_bounds[1]:
        x, y, dx, dy = step(x, y, dx, dy)
        path.append((x, y))
    return path


def plot(path, target_area):
    plt.plot(
        [x for x, _ in path],
        [y for _, y in path],
        "--",
    )
    rectangle = plt.Rectangle(
        (target_area[0], target_area[1]),
        abs(target_area[0] - target_area[2]),
        abs(target_area[1] - target_area[3]),
        alpha=0.5,
        fc="grey"
    )
    plt.gca().add_patch(rectangle)


def run(lines):

    *_, x, y = lines[0].split(" ")
    x0, x1 = x.split("..")
    x1 = int(x1.replace(",", ""))
    x0 = int(x0[2:])

    y0, y1 = y.split("..")
    y1 = int(y1)
    y0 = int(y0[2:])

    x_bounds = (
        min(-1, x0),
        max(0, x1)
    )
    y_bounds = (
        y0,
        999999999
    )
    hits = 0
    best_y = -1
    for dx in range(-1000, 1000):
        for dy in range(-1000, 1000):
            path = simulate(dx, dy, x_bounds, y_bounds)
            hit = any(x0 <= x <= x1 and y0 <= y <= y1 for x, y in path)
            if hit:
                hits += 1
                max_y = max([y for _, y in path])
                if max_y > best_y:
                    best_y = max_y

    return hits


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
