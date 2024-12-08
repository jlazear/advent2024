type Position = tuple[int, int]
type PositionSet = set[Position]
type Direction = int
type StateSet = set[tuple[Position, Direction, Position]]

barriers: PositionSet = set()
current: Position = (-1, -1)

direction: Direction = 0  # 0 = UP, 1 = RIGHT, 2 = DOWN, 3 = LEFT
maxrow: int = 0
maxcol: int = 0
with open("input.txt", "r") as f:
    for i, row in enumerate(f.readlines()):
        maxrow = max(maxrow, i)
        for j, c in enumerate(row.strip()):
            maxcol = max(maxcol, j)
            if c == "^":
                current = (i, j)
            elif c == "#":
                barriers.add((i, j))


def tuple_sum(a: Position, b: Position) -> Position:
    return (a[0] + b[0], a[1] + b[1])


def get_next(
    barriers: PositionSet, current: Position, direction: Direction
) -> tuple[Position, Direction]:
    delta_dict = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
    while (next_pos := tuple_sum(current, delta_dict[direction])) in barriers:
        direction = (direction + 1) % 4
    return next_pos, direction


def is_valid_position(
    pos: Position, maxrow: int, maxcol: int, minrow: int = 0, mincol: int = 0
):
    row, col = pos
    return row < minrow or row > maxrow or col < mincol or col > maxcol


# make candidates
n_iter = 0
seen: StateSet = set()
while n_iter < 10000:
    n_iter += 1
    old = current
    current, direction = get_next(barriers, current, direction)
    if current[0] < 0 or current[0] > maxrow or current[1] < 0 or current[1] > maxcol:
        break
    seen.add((old, direction, current))

print(len(seen))
print(list(seen)[:5])
