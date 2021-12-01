import argparse
from pathlib import Path
import time

import requests


URL_FORMAT = "https://adventofcode.com/2021/day/{day}/input"
BOILER_PLATE = '''from pathlib import Path


TEST_INPUT = """"""
TEST_ANSWER = None


def run(lines):
    # lines = [int(i) for i in lines]
    for line in lines:
        # TODO: Implement me
        pass
    return


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
'''


def main(day: int):
    url = URL_FORMAT.format(day=day)
    cookie = Path(".env").read_text()
    day_directory = Path(f"day{day}")
    day_directory.mkdir(exist_ok=True)
    day_input_path = day_directory / Path("input.txt")
    day_main_path = day_directory / Path("main.py")
    if not day_main_path.exists():
        day_main_path.write_text(BOILER_PLATE)

    print(f"Downloading input for day {day}")
    print(f"URL: {url}")

    while True:
        response = requests.get(url, headers={"cookie": cookie})
        try:
            response.raise_for_status()
            break
        except:
            print("...")
            time.sleep(1)

    data = response.text
    for line in data.split("\n")[:10]:
        print(line)

    day_input_path.write_text(data)
    print("GOGO!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int)
    args = parser.parse_args()
    main(args.day)
