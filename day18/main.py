from copy import copy
import math
from pathlib import Path

import colorama

colorama.init()

TEST_INPUT = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]"""
TEST_ANSWER_P1 = "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]"
TEST_ANSWER = 4140


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


def colour(string, c):
    if c is None:
        return string
    return c + str(string) + C.END


def recursive_apply(root, fn):
    todo = [root.left, root.right]
    while todo:
        node = todo.pop()
        if node is None:
            continue
        fn(node)
        if node.has_left:
            todo.append(node.left)
        if node.has_left:
            todo.append(node.right)


def add_to_depth(node):
    if isinstance(node, Node):
        node.depth += 1


def get_left_digit(node):
    left = node.parent.left
    while not isinstance(left, int) and not isinstance(left.right, int):
        left = left.right
    return left


def get_right_digit(node):
    right = node.parent.right
    while not isinstance(right, int) and not isinstance(right.left, int):
        right = right.left
    return right


def explode(node):
    todo = [node]
    while todo:
        node = todo.pop()
        if node is None:
            continue
        if node.should_explode:
            print("node to explode: ", node)
            right = get_right_digit(node)
            print("number on right: ", right.left)
            right.left += node.right
            left = get_left_digit(node)
            print("number on left: ", left.right)
            left.right += node.left
            print(node)
            if right.left > 10:
                split(right, "left")
            if left.right > 10:
                split(left, "right")
            break

        if not isinstance(node.left, int):
            todo.append(node.left)
        if not isinstance(node.right, int):
            todo.append(node.right)


def split(node, left_or_right):
    """
    To split a regular number, replace it with a pair; the left element of the pair should be
    the regular number divided by two and rounded down, while the right element of the pair
    should be the regular number divided by two and rounded up. For example, 10 becomes [5,5],
    11 becomes [5,6], 12 becomes [6,6], and so on.
    """
    if left_or_right == "left":
        digit = node.left
        assert isinstance(digit, int), "Tried to split a node that was not a regular number"
        node.left = Node(
            [math.floor(digit // 2), math.ceil(digit // 2)],
            node,
            node.depth + 1
        )
        node.left.expand()
    elif left_or_right == "right":
        digit = node.right
        assert isinstance(digit, int), "Tried to split a node that was not a regular number"
        node.right = Node(
            [math.floor(digit // 2), math.ceil(digit // 2)],
            node,
            node.depth + 1
        )
        node.right.expand()
    else:
        raise ValueError("You passed" + left_or_right)


class Node:
    def __init__(self, data, parent, depth):
        self._data = [copy(data[0]), copy(data[1])]
        self.left = None
        self.right = None
        self.parent = parent
        self.depth = depth

    @property
    def is_leaf(self):
        return isinstance(self.left, int) and isinstance(self.right, int)

    @property
    def has_left(self):
        return not isinstance(self.left, int)

    @property
    def has_right(self):
        return not isinstance(self.right, int)

    @property
    def should_explode(self):
        return self.depth == 4

    @property
    def should_split(self):
        return (isinstance(self.left, int) and isinstance(self.right, int)) and (self.right > 10 or self.left > 10)

    def expand(self):
        if not isinstance(self._data[0], int):
            self.left = Node(
                self._data[0],
                self,
                self.depth + 1
            )
        else:
            self.left = self._data[0]

        if not isinstance(self._data[1], int):
            self.right = Node(
                self._data[1],
                self,
                self.depth + 1
            )
        else:
            self.right = self._data[1]

    def __repr__(self):
        colours = {
            # should split, should explode: colour
            (True, True): C.PINK,
            (True, False): C.RED,
            (False, True): C.BLUE,
            (False, False): None
        }
        left_string = colour(str(self.left), colours[(self.should_split, self.should_explode)] if isinstance(self.left, int) else None)
        right_string = colour(str(self.right), colours[(self.should_split, self.should_explode)] if isinstance(self.right, int) else None)
        return f"[{left_string}, {right_string}]"


class SnailFishNumber:
    def __init__(self, root):
        self.root = root

    @classmethod
    def from_data(cls, data):
        root = Node(
            data,
            None,
            0
        )
        todo = [root]
        while todo:
            node = todo.pop()
            if node is None:
                continue
            if not isinstance(node, int):
                node.expand()
            if not isinstance(node.left, int):
                todo.append(node.left)
            if not isinstance(node.right, int):
                todo.append(node.right)
        return cls(root)

    def __add__(self, other):
        result = SnailFishNumber.from_data([self.root._data, other.root._data])
        print("--", result)
        explode(result.root)
        return result

    @classmethod
    def from_str(cls, string):
        return cls.from_data(eval(string))

    def __repr__(self):
        return f"[{self.root}]"


def run(lines):
    result = SnailFishNumber.from_str(lines[0])
    for other in [SnailFishNumber.from_str(line) for line in lines[1:]]:
        print("  ", result)
        print("+ ", other)
        result = result + other
        print("= ", result)
        break
    return result


def mock(lines):
    return run(lines)


def parse_data(data):
    return data.strip().splitlines()


if __name__ == "__main__":
    mock_answer = mock(parse_data(TEST_INPUT))
    print(f"[TEST] Expected answer: {TEST_ANSWER}")
    print(f"[TEST] Actual answer: {mock_answer}")
    print(f"[TEST] {'PASSED' if mock_answer == TEST_ANSWER else 'FAILED'}")

    # answer = run(parse_data(Path("input.txt").read_text()))
    # print(f"[RUN] answer: {answer}")
