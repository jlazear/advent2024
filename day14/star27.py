import math
from dataclasses import dataclass
from enum import Enum, auto
from collections import Counter

type Position = list[int]
type Velocity = tuple[int, int]


class Quadrant(Enum):
    TOPLEFT = auto()
    TOPRIGHT = auto()
    BOTTOMLEFT = auto()
    BOTTOMRIGHT = auto()
    MIDDLE = auto()


@dataclass
class Bot:
    pos: Position
    vel: Velocity

    def advance(self, n_rows: int, n_cols: int) -> None:
        row, col = self.pos
        drow, dcol = self.vel
        new_row = (row + drow) % n_rows
        new_col = (col + dcol) % n_cols
        self.pos = [new_row, new_col]

    def quadrant(self, n_rows: int, n_cols: int) -> Quadrant:
        row, col = self.pos
        top_flag = row < (n_rows // 2)
        left_flag = col < (n_cols // 2)
        middle_flag = (row == n_rows // 2) or (col == n_cols // 2)
        match (middle_flag, top_flag, left_flag):
            case True, _, _:
                return Quadrant.MIDDLE
            case False, True, True:
                return Quadrant.TOPLEFT
            case False, True, False:
                return Quadrant.TOPRIGHT
            case False, False, True:
                return Quadrant.BOTTOMLEFT
            case False, False, False:
                return Quadrant.BOTTOMRIGHT


fname = "input.txt"
if fname in ("test.txt", "test2.txt"):
    n_rows = 7
    n_cols = 11
else:
    n_rows = 103
    n_cols = 101

bots: list[Bot] = []
with open(fname, "r") as f:
    for line in f:
        pos_str, vel_str = line.split()
        pos_vec = pos_str.strip().removeprefix("p=").split(",")
        pos = [int(pos_vec[1]), int(pos_vec[0])]
        vel_vec = vel_str.strip().removeprefix("v=").split(",")
        vel = int(vel_vec[1]), int(vel_vec[0])
        bots.append(Bot(pos, vel))

for i in range(100):
    for bot in bots:
        bot.advance(n_rows, n_cols)

quadrants = Counter(bot.quadrant(n_rows, n_cols) for bot in bots)
del quadrants[Quadrant.MIDDLE]
print(math.prod(count for count in quadrants.values()))
