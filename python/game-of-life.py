import argparse
import copy
import json
import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import Union

import pytest

"""
A recreation of game of life written in python, fully unit tested. I wanted
to check how long it would take me to write this in python after creating it as 
part of my c++ learning process (see ttibsi/game-of-life). See the 
gol-config.json file in the same directory for the config file

This took just over 3 hours to recreate, test, and pass all pre-commit hooks.
This was originally written in it's own repo and moved here as this makes more
sense. 

Usage
-----
```bash
$ python3 -m virtualenv venv 
$ . venv/bin/activate
$ pip install pytest
$ python3 game-of-life.py
```

usage: game-of-life.py [-h] [-j JSON] [-s SIZE] [-i ITER]

options:
  -h, --help            show this help message and exit
  -j JSON, --json JSON  Pass program a json config file
  -s SIZE, --size SIZE  Specify board size
  -i ITER, --iter ITER  Specify number of iterations

Or to run unit tests:
```bash
pytest game-of-life.py 
```
"""

# LIVE_SYMBOL = "#"
# DEAD_SYMBOL = "."
LIVE_SYMBOL = "⬛"
DEAD_SYMBOL = "🟦"


@dataclass
class Point:
    x_cord: int
    y_cord: int
    live: bool


def check_neighbors(board: list[Point], loc: Point) -> int:
    living_relatives = 0
    relatives = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, +1),
        (+1, -1),
        (+1, 0),
        (+1, +1),
    ]

    for rel in relatives:
        x_val = rel[0] + loc.x_cord
        y_val = rel[1] + loc.y_cord

        found = [i for i in board if i.x_cord == x_val and i.y_cord == y_val]
        if found and found[0].live:
            living_relatives += 1

    return living_relatives


def increment_board_state(board: list[Point]) -> list[Point]:
    temp: list[Point] = construct_board(int(math.sqrt(len(board))))

    for idx, point in enumerate(board):
        live_adj = check_neighbors(board, point)

        if point.live:
            if not (live_adj == 2 or live_adj == 3):
                temp[idx].live = False
            else:
                temp[idx].live = True

        else:
            if live_adj == 3:
                temp[idx].live = True
            else:
                temp[idx].live = False

    return temp


def print_board(b: list[Point], size: int) -> None:
    for elem in b:
        if elem.live:
            print(LIVE_SYMBOL, end=" ")
        else:
            print(DEAD_SYMBOL, end=" ")

        if elem.y_cord == (size - 1):
            print("\n")


def populate_board(board: list[Point], pop_list: list[int]) -> list[Point]:
    for val in pop_list:
        board[val].live = True
        print(f"{board[val].x_cord} {board[val].y_cord}")

    return board


def construct_board(size: int) -> list[Point]:
    ret: list[Point] = []

    for i in range(size):
        for j in range(size):
            val = Point(i, j, False)
            ret.append(val)

    return ret


def get_populate_list(size: int, coords: list[Dict[str, int]]) -> list[int]:
    ret: list[int] = []

    for elem in coords:
        val = (size * int(elem["x_cord"])) + int(elem["y_cord"])
        ret.append(val)

    return ret


def game_loop(size: int, iter: int, config: Dict[str, Any]) -> None:
    populate_list: list[int] = get_populate_list(size, config["coords"])
    my_board: list[Point] = populate_board(construct_board(size), populate_list)

    print("Iter 0 (Starting layout)")
    print_board(my_board, size)

    for i in range(size):
        print(f"Iter {i} (Starting layout)")
        my_board = increment_board_state(my_board)
        print_board(my_board, size)


def main(argv: Union[Sequence[str], None] = None) -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-j", "--json", help="Pass program a json config file", default=""
    )
    parser.add_argument("-s", "--size", help="Specify board size", default=0)
    parser.add_argument("-i", "--iter", help="Specify number of iterations", default=0)

    args: argparse.Namespace = parser.parse_args(argv)

    if args.json:
        with open(args.json) as f:
            config = json.load(f)

        size = config["size"]
        iter = config["iter"]
    else:
        config = {"coords": []}
        size = int(args.size)
        iter = int(args.iter)

    game_loop(size, iter, config)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# --------------------------------------
# Tests

empty_board = [
    Point(0, 0, False),
    Point(0, 1, False),
    Point(0, 2, False),
    Point(1, 0, False),
    Point(1, 1, False),
    Point(1, 2, False),
    Point(2, 0, False),
    Point(2, 1, False),
    Point(2, 2, False),
]

inp_board = [
    Point(0, 0, False),
    Point(0, 1, True),
    Point(0, 2, False),
    Point(1, 0, True),
    Point(1, 1, False),
    Point(1, 2, True),
    Point(2, 0, False),
    Point(2, 1, False),
    Point(2, 2, False),
]

incremented_board = [
    Point(0, 0, False),
    Point(0, 1, True),
    Point(0, 2, False),
    Point(1, 0, False),
    Point(1, 1, True),
    Point(1, 2, False),
    Point(2, 0, False),
    Point(2, 1, False),
    Point(2, 2, False),
]

test_coords = [
    {"x_cord": 0, "y_cord": 1},
    {"x_cord": 1, "y_cord": 0},
    {"x_cord": 1, "y_cord": 2},
]

glider_coords = [
    {"x_cord": 0, "y_cord": 2},
    {"x_cord": 1, "y_cord": 3},
    {"x_cord": 2, "y_cord": 1},
    {"x_cord": 2, "y_cord": 2},
    {"x_cord": 2, "y_cord": 3},
]


@pytest.mark.parametrize(
    ("inp1", "inp2", "expected"),
    [
        (inp_board, Point(1, 1, False), 3),
        (inp_board, Point(1, 0, True), 1),
    ],
)
def test_check_neighbors(inp1, inp2, expected):
    assert check_neighbors(inp1, inp2) == expected


@pytest.mark.parametrize(
    ("inp", "expected"),
    [
        (inp_board, incremented_board),
    ],
)
def test_increment_board_state(inp, expected):
    assert increment_board_state(inp) == expected


@pytest.mark.parametrize(
    ("inp1", "inp2", "expected"),
    [
        # Hilariously - this is a flaky test... that's why we have to pass in
        # a deepcopy of the board - whichever test runs first modifies empty_board
        (copy.deepcopy(empty_board), [1, 3, 5], inp_board),
        (copy.deepcopy(empty_board), [1, 4], incremented_board),
    ],
)
def test_populate_board(inp1, inp2, expected):
    assert populate_board(inp1, inp2) == expected


@pytest.mark.parametrize(
    ("inp", "expected"),
    [(3, empty_board)],
)
def test_construct_board(inp, expected):
    assert construct_board(inp) == expected


@pytest.mark.parametrize(
    ("inp1", "inp2", "expected"),
    [
        (3, test_coords, [1, 3, 5]),
        (7, glider_coords, [2, 10, 15, 16, 17]),
    ],
)
def test_get_populate_list(inp1, inp2, expected):
    assert get_populate_list(inp1, inp2) == expected
