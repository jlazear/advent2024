from typing import NamedTuple
import numpy as np
import numpy.typing as npt

type NDArrayFloat = npt.NDArray[np.float_]


class Block(NamedTuple):
    A: NDArrayFloat
    prize: NDArrayFloat


def parse_button_line(line: str) -> NDArrayFloat:
    _, right = line.split(":")
    x_str, y_str = right.split(",")
    x = int(x_str.strip().removeprefix("X+"))
    y = int(y_str.strip().removeprefix("Y+"))
    return np.array([x, y], dtype=float)


def parse_prize_line(line: str) -> NDArrayFloat:
    _, right = line.split(":")
    x_str, y_str = right.split(",")
    x = int(x_str.strip().removeprefix("X="))
    y = int(y_str.strip().removeprefix("Y="))
    return np.array([[x, y]], dtype=float).T


def parse_block(block: str):
    a_str, b_str, prize_str = block.strip().split("\n")
    a = parse_button_line(a_str)
    b = parse_button_line(b_str)
    prize = parse_prize_line(prize_str)
    A = np.vstack([a, b]).T
    return Block(A, prize)


blocks: list[Block] = []
with open("input.txt", "r") as f:
    s = f.read()
    for block_str in s.split("\n\n"):
        blocks.append(parse_block(block_str))

s = 0
score_vec = np.array([[3.0, 1.0]], dtype=int)
for block in blocks:
    rho = np.linalg.inv(block.A) @ block.prize
    rho_int = rho.round(0)
    valid = np.allclose(rho, rho_int)
    if valid:
        score = score_vec @ rho_int
        s += int(score[0, 0])

print(s)
