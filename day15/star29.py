from enum import Enum


type Position = tuple[int, int]


class Direction(Enum):
    UP = "^"
    RIGHT = ">"
    DOWN = "v"
    LEFT = "<"

    def __init__(self, d: str):
        match d:
            case "^":
                self.direction = (-1, 0)
            case ">":
                self.direction = (0, 1)
            case "v":
                self.direction = (1, 0)
            case "<":
                self.direction = (0, -1)
            case _:
                raise ValueError(f"Invalid direction {d=}")


def pos_add(a: Position, b: Position) -> Position:
    return (a[0] + b[0], a[1] + b[1])


def print_m(m: list[list[str]]) -> None:
    for row in m:
        print("".join(row))


def move(pos: Position, direction: Direction, m: list[list[str]]) -> None:
    new_char = m[pos[0]][pos[1]]
    new_pos = pos_add(pos, direction.direction)
    m[new_pos[0]][new_pos[1]] = new_char
    m[pos[0]][pos[1]] = "."


def push(pos: Position, direction: Direction, m: list[list[str]]) -> Position:
    stack = [pos]
    d = direction.direction
    next_pos = pos_add(pos, d)
    while m[next_pos[0]][next_pos[1]] not in (".", "#"):
        stack.append(next_pos)
        next_pos = pos_add(next_pos, d)
    if m[next_pos[0]][next_pos[1]] == "#":
        return pos
    while stack:
        head = stack.pop()
        move(head, direction, m)
    return pos_add(pos, d)


def score(m: list[list[str]]) -> int:
    s: int = 0
    for i, row in enumerate(m):
        for j, c in enumerate(row):
            if c == "O":
                s += 100 * i + j
    return s


with open("input.txt", "r") as f:
    m_str, instructions = f.read().split("\n\n")
m = [[c for c in row] for row in m_str.split("\n")]
instructions = instructions.replace("\n", "")
pos: Position = (-1, -1)  # to appease the mypy gods
for i, row in enumerate(m):
    for j, c in enumerate(row):
        if c == "@":
            pos = (i, j)

for c in instructions:
    pos = push(pos, Direction(c), m)

# print_m(m)
print(score(m))
