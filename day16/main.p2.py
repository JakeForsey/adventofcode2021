from math import prod
from pathlib import Path


TEST_INPUTS = [
    "C200B40A82",
    "04005AC33890",
    "880086C3E88112",
    "CE00C43D881120",
    "D8005AC2A8F0",
    "F600BC2D8F",
    "9C005AC2F8F0",
    "9C0141080250320F1802104A08",
]
TEST_ANSWERS = [
    3,
    54,
    7,
    9,
    1,
    0,
    0,
    1,
]
TEST_INPUT = "".join(TEST_INPUTS)
TEST_ANSWER = sum(TEST_ANSWERS)

HEX_TO_BINARY = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"
}

BINARY_TO_OPERATOR = {
    "000": "sum",
    "001": "prod",
    "010": "min",
    "011": "max",
    "101": "greater_than",
    "110": "less_than",
    "111": "equal_to",
}

DEBUG = True


class C:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def greater_than(ab):
    a, b = ab
    return int(a > b)


def less_than(ab):
    a, b = ab
    return int(a < b)


def equal_to(ab):
    a, b = ab
    return int(a == b)


def to_binary(string):
    binary = ""
    for c in string:
        binary += HEX_TO_BINARY[c]
    return binary


def read_header(binary):
    version = binary[:3]
    assert len(version) == 3
    type_id = binary[3:6]
    assert len(type_id) == 3
    return version, type_id, binary[6:]


def read_literal(binary):
    i = 0
    packet = ""
    chunk = binary[i: i + 5]
    if DEBUG: print(C.PINK + chunk[0] + C.END, end="")
    if DEBUG: print(C.GREEN + chunk[1:] + C.END, end="")

    packet += chunk[1:]
    while "1" in chunk[0]:
        i += 5
        chunk = binary[i: i + 5]
        if DEBUG: print(C.PINK + chunk[0] + C.END, end="")
        if DEBUG: print(C.GREEN + chunk[1:] + C.END, end="")
        packet += chunk[1:]

    literal = int(packet, 2)
    return literal, binary[i + 5:]


# assert to_binary("D2FE28") == "110100101111111000101000"
# assert read_header("110100101111111000101000") == ("110", "100", "101111111000101000")
# assert read_literal("101111111000101000") == (2021, "000")

CLOSE = "ZZZ"


class Counter:
    def __init__(self, num):
        self.num = num

    def decrement(self):
        if self.num is not None:
            self.num -= 1
        return self

    @property
    def count(self):
        return float("inf") if self.num is None else self.num


def run(lines):
    binary = to_binary(lines[0])

    result = ""
    todo = [(binary, Counter(None))]
    while todo:
        binary, counter = todo.pop()
        if counter.count <= 0:
            result += "]),"
            todo.append((binary, Counter(None)))
            continue
        if binary == CLOSE:
            result += "]),"
            continue

        if "1" not in binary:
            continue

        print()
        print()
        print(binary)
        version, type_id, rest = read_header(binary)
        if DEBUG: print(C.CYAN + version + C.END, end="")
        if DEBUG: print(C.BLUE + type_id + C.END, end="")

        if type_id == "100":  # 4
            # Parse Literal (append one)
            literal, rest = read_literal(rest)
            todo.append((rest, counter.decrement()))
            result += f"{literal},"

        else:
            result += f"{BINARY_TO_OPERATOR[type_id]}(["

            mode = rest[0]
            if DEBUG: print(C.YELLOW + mode + C.END, end="")
            if mode == "0":
                length_binary = rest[1: 16]
                if DEBUG: print(C.RED + length_binary + C.END, end="")
                length = int(length_binary, 2)
                end = 16 + length
                left = rest[16: end]
                if DEBUG: print(left, end="")
                todo.append((rest[end:], counter.decrement()))
                todo.append((CLOSE, Counter(None)))
                todo.append((left, Counter(None)))

            else:
                length_binary = rest[1: 12]
                if DEBUG: print(C.RED + length_binary + C.END, end="")
                counter = int(length_binary, 2)
                left = rest[12:]
                if DEBUG: print(left, end="")
                todo.append((left, Counter(counter)))

    print(result.count("["), result.count("]"))

    print(result)
    return eval(result)[0]


def mock(lines):
    return run(lines)


def parse_data(data):
    return data.strip().splitlines()


if __name__ == "__main__":
    for test_input, test_answer in zip(TEST_INPUTS, TEST_ANSWERS):
        print()
        print(test_input)
        print("".join(to_binary(test_input)))
        version_sum = 0
        mock_answer = mock(parse_data(test_input))
        print()
        print(f"[TEST] Expected answer: {test_answer}")
        print(f"[TEST] Actual answer: {mock_answer}")
        print(f"[TEST] {'PASSED' if mock_answer == test_answer else 'FAILED'}")
        assert mock_answer == test_answer, f"{mock_answer}, {test_answer}"

    answer = run(parse_data(Path("input.txt").read_text()))
    print(f"[RUN] answer: {answer}")
