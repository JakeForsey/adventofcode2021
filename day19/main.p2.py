from collections import defaultdict
from pathlib import Path
import itertools

import numpy as np


TEST_INPUT = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""
TEST_ANSWER = 3621


def rotations():
    # https://stackoverflow.com/questions/16452383/how-to-get-all-24-rotations-of-a-3-dimensional-array
    for x, y, z in itertools.permutations([0, 1, 2]):
        for sx, sy, sz in itertools.product([-1, 1], repeat=3):
            rotation_matrix = np.zeros((3, 3))
            rotation_matrix[0, x] = sx
            rotation_matrix[1, y] = sy
            rotation_matrix[2, z] = sz
            if np.linalg.det(rotation_matrix) == 1:
                yield rotation_matrix


def apply_rotation(rotation_matrix, coord):
    return tuple(rotation_matrix @ coord)


def vector_from(src, dst):
    return tuple([
        dst[i] - src[i]
        for i in range(len(src))
    ])


def translate(coord, vector):
    return tuple([
        coord[i] + vector[i]
        for i in range(len(coord))
    ])


def create_reference_vectors(coord, coords):
    vectors = set()
    for other_coord in coords:
        if coord == other_coord:
            continue
        vectors.add(vector_from(coord, other_coord))
    return vectors


def attempt_match(transformed_coords, reference_vectors):
    for transformed_coord in transformed_coords:
        vector = create_reference_vectors(transformed_coord, transformed_coords)

        for reference_coord, reference_vector in reference_vectors:
            intersection = vector & reference_vector
            if len(intersection) >= 11:  # intersection does not include (0, 0, 0)
                translation = vector_from(transformed_coord, reference_coord)
                return set(translate(coord, translation) for coord in transformed_coords), translation
    return None, None


def transform_coords(coords, other_coords):
    """
    Find the transform and translation that maps from scanner to other scanner
    """
    # reference_vectors could be computed once upfront, and then added to, rather
    # than computing it each time here.
    reference_vectors = []
    for reference_coord in other_coords:
        vector = create_reference_vectors(reference_coord, other_coords)
        reference_vectors.append((reference_coord, vector))

    for i, rotation_matrix in enumerate(rotations()):
        transformed_coords = set(apply_rotation(rotation_matrix, coord) for coord in coords)
        out, scanner_position = attempt_match(transformed_coords, reference_vectors)
        if out is not None:
            return out, scanner_position
    return set(), None


def run(lines):
    string = "\n".join(lines)
    scanner_strings = string.split("\n\n")

    scanners = defaultdict(set)
    for scanner_string in scanner_strings:
        scanner_rows = scanner_string.splitlines()
        _, _, scanner_id, _ = scanner_rows[0].split(" ")
        for beacons in scanner_rows[1:]:
            x, y, z = beacons.split(",")
            scanners[scanner_id].add((int(x), int(y), int(z)))

    scanner_positions = []
    final = scanners.pop("0")
    todo = list(scanners.items())
    while todo:
        scanner, coords = todo.pop()
        transformed_coords, scanner_position = transform_coords(coords, final)
        if transformed_coords:
            scanner_positions.append(scanner_position)
            final = final | transformed_coords
        else:
            todo.insert(0, (scanner, coords))

    max_distance = -1
    for src in scanner_positions:
        for dst in scanner_positions:
            if src == dst:
                continue
            distance = sum(
                [abs(src[i] - dst[i]) for i in range(len(src))]
            )
            if distance > max_distance:
                max_distance = distance

    return max_distance


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
