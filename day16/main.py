from pathlib import Path


TEST_INPUTS = [
    "D2FE28",
    "38006F45291200",
    "EE00D40C823060",
    "8A004A801A8002F478",

    "620080001611562C8802118E34",
    "C0015000016115A2E0802F182340",
    "A0016C880162017C3686B18A3D4780"
]
TEST_ANSWERS = [
    6,
    9,
    14,
    16,
    12,
    23,
    31
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


def run(lines):
    binary = to_binary(lines[0])

    result = 0
    todo = [(binary, 99999)]
    while todo:
        binary, counter = todo.pop()
        if "1" not in binary:
            continue
        if counter <= 0:
            todo.append((binary, 999999))
            continue

        print()
        print()
        print(binary)
        version, type_id, rest = read_header(binary)
        if DEBUG: print(C.CYAN + version + C.END, end="")
        if DEBUG: print(C.BLUE + type_id + C.END, end="")

        result += int(version, 2)

        if type_id == "100":  # 4
            # Parse Literal (append one)
            literal, rest = read_literal(rest)
            todo.append((rest, counter - 1))

        else:
            # Parse operator (append two)
            mode = rest[0]
            if DEBUG: print(C.YELLOW + mode + C.END, end="")
            if mode == "0":
                length_binary = rest[1: 16]
                if DEBUG: print(C.RED + length_binary + C.END, end="")
                length = int(length_binary, 2)
                end = 16 + length
                left = rest[16: end]
                if DEBUG: print(left, end="")
                todo.append((left, counter - 1))
                todo.append((rest[end:], counter - 1))

            else:
                length_binary = rest[1: 12]
                if DEBUG: print(C.RED + length_binary + C.END, end="")
                counter = int(length_binary, 2) + 1
                left = rest[12: ]
                if DEBUG: print(left, end="")
                todo.append((left, counter))

    return result


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

    answer = run(parse_data(Path("input.txt").read_text()))
    print(f"[RUN] answer: {answer}")
