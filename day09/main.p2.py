from pathlib import Path


TEST_INPUT = """2199943210
3987894921
9856789892
8767896789
9899965678"""
TEST_ANSWER = 1134


def get(i, j, depth):
    if i >= len(depth):
        return 9999
    if j >= len(depth[0]):
        return 9999
    if i < 0:
        return 9999
    if j < 0:
        return 9999
    return depth[i][j]


def valid_neighbors(point, depth):
    points = []
    for direction in [(1, 0), (0, -1), (0, 1), (-1, 0)]:
        new_point = (point[0] + direction[0], point[1] + direction[1])

        if 0 <= new_point[0] <= len(depth):
            if 0 <= new_point[1] <= len(depth[0]):

                if get(*new_point, depth) < 9:

                    points.append(new_point)

    return set(points)


def expand(to_expand, depth, basin):
    if not to_expand:
        return basin

    for next_point in list(to_expand):
        to_expand.remove(next_point)

        candidates = valid_neighbors(next_point, depth)
        candidates = candidates - set(basin)
        to_expand = to_expand | candidates

        basin.append(next_point)
        return expand(to_expand, depth, basin)


def run(lines):
    depth = [[int(i) for i in l] for l in lines]

    low_points = []
    for i in range(len(depth)):
        for j in range(len(depth[0])):
            val = depth[i][j]
            other_vals = [
                get(i + 1, j, depth),  # above
                get(i, j - 1, depth),  # left
                get(i, j + 1, depth),  # right
                get(i - 1, j, depth),  # below
            ]
            if val < min(other_vals):
                low_points.append((i, j))

    basin_sizes = []
    for lp in low_points:
        basin = expand(valid_neighbors(lp, depth), depth, [lp])
        basin_size = len(set(basin))
        basin_sizes.append(basin_size)

    basin_sizes.sort(reverse=True)
    ret = 1
    for i in basin_sizes[:3]:
        ret *= i
    return ret


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
