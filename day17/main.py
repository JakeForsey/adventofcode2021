from pathlib import Path

import matplotlib.pyplot as plt


TEST_INPUT = """target area: x=20..30, y=-10..-5"""
TEST_ANSWER = 45


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
    plt.show()


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
        y1,
        999999999
    )

    best_y = -1
    print(x0, x1, y0, y1)
    for dx in range(-1000, 1000):
        for dy in range(-1000, 1000):
            path = simulate(dx, dy, x_bounds, y_bounds)
            hit = any(x0 <= x <= x1 and y0 <= y <= y1 for x, y in path)
            if hit:
                max_y = max([y for _, y in path])
                if max_y > best_y:
                    best_y = max_y

    return best_y


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
