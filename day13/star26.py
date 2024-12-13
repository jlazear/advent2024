from typing import NamedTuple
import numpy as np
import numpy.typing as npt

type NDArrayInt = npt.NDArray[np.int_]


class Block(NamedTuple):
    A: NDArrayInt
    prize: NDArrayInt


def parse_button_line(line: str) -> NDArrayInt:
    _, right = line.split(":")
    x_str, y_str = right.split(",")
    x = int(x_str.strip().removeprefix("X+"))
    y = int(y_str.strip().removeprefix("Y+"))
    return np.array([x, y], dtype="int64")


def parse_prize_line(line: str, offset: int = 10000000000000) -> NDArrayInt:
    _, right = line.split(":")
    x_str, y_str = right.split(",")
    x = int(x_str.strip().removeprefix("X="))
    y = int(y_str.strip().removeprefix("Y="))
    return offset + np.array([[x, y]], dtype="int64").T


def parse_block(block: str):
    a_str, b_str, prize_str = block.strip().split("\n")
    a = parse_button_line(a_str)
    b = parse_button_line(b_str)
    prize = parse_prize_line(prize_str)
    A = np.vstack([a, b]).T
    return Block(A, prize)


def score(block: Block):
    x, y = block.prize.T[0]

    (a, b), (c, d) = block.A
    det = a * d - b * c
    num_x = d * x - b * y
    num_y = a * y - c * x
    if (num_x % det) != 0 or (num_y % det) != 0:
        return 0
    rho_x = num_x // det
    rho_y = num_y // det
    return rho_x * 3 + rho_y


blocks: list[Block] = []
with open("input.txt", "r") as f:
    s = f.read()
    for block_str in s.split("\n\n"):
        blocks.append(parse_block(block_str))

s = sum(score(block) for block in blocks)
print(s)
