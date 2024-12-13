from enum import Enum, auto
from typing import NamedTuple


type Position = tuple[int, int]


class Direction(Enum):
    TOPLEFT = auto()
    TOPRIGHT = auto()
    BOTTOMLEFT = auto()
    BOTTOMRIGHT = auto()


class Quadrant(NamedTuple):
    pos: Position
    pos_adjacent1: Position
    pos_adjacent2: Position
    pos_diagonal: Position


with open("input.txt", "r") as f:
    m: dict[Position, str] = {
        (i, j): c
        for i, row in enumerate(f.readlines())
        for j, c in enumerate(row.strip())
    }
valids = set(m)


def neighbors(pos: Position) -> list[Position]:
    i, j = pos
    neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
    neighbors = [neighbor for neighbor in neighbors if neighbor in valids]
    return neighbors


def bfs(start: Position, m: dict[Position, str] = m) -> set[Position]:
    stack = [start]
    group: set[Position] = set()
    plant_type = m[start]
    while stack:
        pos = stack.pop()
        group.add(pos)
        new_neighbors = neighbors(pos)
        for neighbor in new_neighbors:
            if neighbor not in group and m[neighbor] == plant_type:
                stack.append(neighbor)
    return group


def quadrant(pos: Position, direction: Direction) -> Quadrant:
    i, j = pos
    match direction:
        case Direction.TOPLEFT:
            coords = ((i, j), (i, j - 1), (i - 1, j), (i - 1, j - 1))
        case Direction.TOPRIGHT:
            coords = ((i, j), (i - 1, j), (i, j + 1), (i - 1, j + 1))
        case Direction.BOTTOMLEFT:
            coords = ((i, j), (i, j - 1), (i + 1, j), (i + 1, j - 1))
        case Direction.BOTTOMRIGHT:
            coords = ((i, j), (i, j + 1), (i + 1, j), (i + 1, j + 1))
    return Quadrant(*coords)


def is_corner(quadrant: Quadrant, m: dict[Position, str] = m) -> bool:
    plant_type = m[quadrant.pos]
    n_adjacent_match = 2
    if (quadrant.pos_adjacent1 not in m) or (m[quadrant.pos_adjacent1] != plant_type):
        n_adjacent_match -= 1
    if (quadrant.pos_adjacent2 not in m) or (m[quadrant.pos_adjacent2] != plant_type):
        n_adjacent_match -= 1
    diag_match = (quadrant.pos_diagonal not in m) or (
        m[quadrant.pos_diagonal] == plant_type
    )
    return (n_adjacent_match == 2 and not diag_match) or n_adjacent_match == 0


def n_corners(pos: Position, m: dict[Position, str] = m) -> int:
    return sum(is_corner(quadrant(pos, direction), m) for direction in Direction)


def score(group: set[Position]) -> int:
    n = sum(n_corners(pos) for pos in group)
    return len(group) * n


seen: set[Position] = set()
groups: list[set[Position]] = []
for pos in valids:
    if pos not in seen:
        group = bfs(pos, m)
        if group:
            seen.update(group)
            groups.append(group)

print(sum(score(group) for group in groups))
