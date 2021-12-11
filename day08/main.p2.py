from collections import Counter
from pathlib import Path

import numpy as np
from ortools.sat.python import cp_model

TEST_INPUT = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""
TEST_ANSWER = 61229
CHARS = "abcdefg"
EXPECTED = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}


def to_binary(chars):
    out = [0] * 7
    for c in chars:
        out[CHARS.index(c)] = 1
    return out


def from_binary(binary):
    out = ""
    for i, b in enumerate(binary):
        if b == 1:
            out += CHARS[i]
    return out


def mul(x, m):
    return (np.array(x) * np.array(m)).sum(axis=1).tolist()


def matmul(x, m):
    out = []
    for i in x:
        out.append(mul(i, m))
    return out


def extract_solution(solution, solver):
    out = []
    for i in range(7):
        row = []
        for ii in range(7):
            row.append(solver.Value(solution[i][ii]))
        out.append(row)
    return out


def sort_chars(string):
    return "".join(sorted(string))


def sum_chars(x):
    return [sum(row[i] for row in x) for i in range(7)]


class SolutionCounter(cp_model.CpSolverSolutionCallback):
    def __init__(self, x):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__x = x
        self.__solution_count = 0
        self.solution_list = []

    def on_solution_callback(self):
        self.solution_list.append(
            extract_solution(self.__x, self)
        )
        self.__solution_count += 1

    def solution_count(self):
        return self.__solution_count


def run(lines):
    binary_actual = [
        to_binary(charts) for charts in EXPECTED
    ]
    actual_sum = sum_chars(binary_actual)

    results = []
    for line in lines:
        # Parse data
        sample, targets = line.split(" | ")
        sample = [sort_chars(s) for s in sample.split(" ")]
        targets = [sort_chars(t) for t in targets.split(" ")]

        # Compute some easy mappings
        char_counts = Counter("".join(sample))
        lookup = {
            [key for key, count in char_counts.items() if count == 9][0]: "f",
            [key for key, count in char_counts.items() if count == 6][0]: "b",
            [key for key, count in char_counts.items() if count == 4][0]: "e",
        }
        seven = next(filter(lambda x: len(x) == 3, sample))
        one = next(filter(lambda x: len(x) == 2, sample))
        diff = set(seven).symmetric_difference(set(one))
        assert len(diff) == 1
        lookup[diff.pop()] = "a"

        # Model the problem as a linear constraint problem
        binary_sample = [to_binary(x) for x in sample]
        binary_target = [to_binary(x) for x in targets]

        model = cp_model.CpModel()
        # MODEL VARIABLES
        x = []
        for i in range(7):
            row = [model.NewIntVar(0, 1, f"{i} -> {ii}") for ii in range(7)]
            model.Add(sum(row) == 1)
            x.append(row)

        # ROW / COLUMN CONSTRAINTS
        for row in x:
            model.Add(sum(row) == 1)
        for col in range(7):
            model.Add(sum(row[col] for row in x) == 1)

        # CHAR CONSTRAINTS
        for i, ii in lookup.items():
            print(f"Fixing: {i}({CHARS.index(i)}) -> {ii}({CHARS.index(ii)})")
            model.Add(x[CHARS.index(ii)][CHARS.index(i)] == 1)

        translated_binary = matmul(binary_sample, x)
        translated_sum = sum_chars(translated_binary)
        # STATS CONSTRAINTS (counts of each character in the translated output
        # must equal the counts of the characters in the idealised output)
        for a, t in zip(actual_sum, translated_sum):
            model.Add(a == t)

        solver = cp_model.CpSolver()
        solver.parameters.enumerate_all_solutions = True
        solution_printer = SolutionCounter(x)

        for m in solution_printer.solution_list:
            # There are not quite enough constraints, so just try every valid solution
            # found...
            translated_target = matmul(binary_target, m)
            strings = [from_binary(x) for x in translated_target]
            try:
                ints = [EXPECTED[string] for string in strings]
            except:
                continue

            results.append(int("".join(map(str, ints))))
            break

    return sum(results)


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
