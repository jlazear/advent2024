type Position = tuple[int, int]
type PositionSet = set[Position]
type Direction = int
type PosDirSet = set[tuple[Position, Direction]]

barriers: PositionSet = set()
start_pos: Position = (-1, -1)

start_direction: Direction = 0  # 0 = UP, 1 = RIGHT, 2 = DOWN, 3 = LEFT
maxrow: int = 0
maxcol: int = 0
with open("input.txt", "r") as f:
    for i, row in enumerate(f.readlines()):
        maxrow = max(maxrow, i)
        for j, c in enumerate(row.strip()):
            maxcol = max(maxcol, j)
            if c == "^":
                start_pos = (i, j)
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


def make_candidates(
    barriers: PositionSet,
    current: Position = start_pos,
    direction: Direction = start_direction,
) -> PositionSet:
    n_iter = 0
    seen: PositionSet = set()
    while n_iter < 10000:
        n_iter += 1
        current, direction = get_next(barriers, current, direction)
        if (
            current[0] < 0
            or current[0] > maxrow
            or current[1] < 0
            or current[1] > maxcol
        ):
            break
        seen.add(current)
    if n_iter == 10000:
        raise Exception("max iterations exceeded")
    return seen


def check(
    barriers: PositionSet,
    current: Position = start_pos,
    direction: Direction = start_direction,
) -> bool:
    n_iter = 0
    seen: PosDirSet = set()
    while n_iter < 10000:
        n_iter += 1
        seen.add((current, direction))
        current, direction = get_next(barriers, current, direction)
        if (current, direction) in seen:
            return True
        elif (
            current[0] < 0
            or current[0] > maxrow
            or current[1] < 0
            or current[1] > maxcol
        ):
            return False
    if n_iter == 10000:
        raise Exception("max iterations exceeded")

    return False


def test_candidate(
    barriers: PositionSet,
    new_barrier: Position,
) -> bool:
    new_barriers = barriers.copy()
    new_barriers.add(new_barrier)
    return check(new_barriers)


candidates = make_candidates(barriers)

obstructions = set(
    new_barrier for new_barrier in candidates if test_candidate(barriers, new_barrier)
)
print(len(obstructions))
