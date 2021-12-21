from pathlib import Path


TEST_INPUT = """Player 1 starting position: 4
Player 2 starting position: 8"""
TEST_ANSWER = 739785


class Player:
    def __init__(self, pid, pos):
        self.pid = pid
        self.pos = pos
        self.score = 0

    def move(self, steps):
        next_pos = self.pos + steps
        if next_pos > 10:
            next_pos = next_pos % 10
            if next_pos == 0:
                next_pos = 10
        assert 0 < next_pos < 11, f"{self.pos=}, {steps=}, {next_pos=}"
        self.pos = next_pos

    @classmethod
    def from_str(cls, string):
        parts = string.split(" ")
        return cls(parts[1], int(parts[-1]))


class DeterministicDie:
    def __init__(self):
        self.rolls = 0

        def iterator():
            while True:
                for i in range(1, 101):
                    yield i

        self.iter = iterator()

    def roll(self):
        self.rolls += 1
        roll = next(self.iter)
        assert 0 < roll < 101
        return roll


def play(players, debug):
    die = DeterministicDie()
    while True:
        for player in players:
            rolls = [die.roll() for _ in range(3)]
            player.move(sum(rolls))
            player.score += player.pos
            if debug: print(f"Player {player.pid} rolls {'+'.join([str(r) for r in rolls])} and moves to space {player.pos} for a total score of {player.score}.")
            if player.score >= 1000:
                return players, die


def run(lines, debug=False):
    players = list(map(Player.from_str, lines))

    players, die = play(players, debug)

    loser = min(players, key=lambda p: p.score)
    return loser.score * die.rolls


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
