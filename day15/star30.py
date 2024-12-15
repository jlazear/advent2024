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


def unsafe_move(pos: Position, direction: Direction, m: list[list[str]]) -> None:
    new_char = m[pos[0]][pos[1]]
    new_pos = pos_add(pos, direction.direction)
    match new_char:
        case "@":
            m[new_pos[0]][new_pos[1]] = "@"
            m[pos[0]][pos[1]] = "."
        case "[":
            paired = pos_add(pos, Direction.RIGHT.direction)
            new_paired = pos_add(new_pos, Direction.RIGHT.direction)
            # unset old
            m[pos[0]][pos[1]] = "."
            m[paired[0]][paired[1]] = "."
            # set new
            m[new_pos[0]][new_pos[1]] = "["
            m[new_paired[0]][new_paired[1]] = "]"
        case _:
            raise ValueError(f"Can only move '@' and '['! m[{pos}] = {new_char}")


def unpack(
    positions: list[Position], direction: Direction, m: list[list[str]]
) -> list[Position]:
    unpacked: list[Position] = []
    for pos in positions:
        c = m[pos[0]][pos[1]]
        match c, direction:
            case "@", _:
                unpacked.append(pos)
            case "[", Direction.UP | Direction.DOWN:
                unpacked.extend([pos, pos_add(pos, Direction.RIGHT.direction)])
            case "[", Direction.LEFT:
                unpacked.append(pos)
            case "[", Direction.RIGHT:
                unpacked.append(pos_add(pos, Direction.RIGHT.direction))
            case "]", Direction.UP | Direction.DOWN:
                unpacked.extend([pos, pos_add(pos, Direction.LEFT.direction)])
            case "]", Direction.LEFT:
                unpacked.append(pos_add(pos, Direction.LEFT.direction))
            case "]", Direction.RIGHT:
                unpacked.append(pos)
            case _:
                raise ValueError("Invalid positions list")
    return unpacked


def resolve_targets(
    positions: list[Position], direction: Direction, m: list[list[str]]
) -> list[Position]:
    d = direction.direction
    push_targets: list[Position] = []
    for pos in positions:
        next_pos = pos_add(pos, d)
        c = m[next_pos[0]][next_pos[1]]
        if c == "]":
            push_targets.append(pos_add(next_pos, Direction.LEFT.direction))
        else:
            push_targets.append(next_pos)
    return push_targets


def push(pos: Position, direction: Direction, m: list[list[str]]) -> Position:
    stack: list[list[Position]] = [[pos]]  # only add @ or ['s
    d = direction.direction
    for _ in range(10000):  # infinite loops bad
        positions = stack[-1]
        unpacked = unpack(positions, direction, m)
        push_targets = resolve_targets(unpacked, direction, m)
        next_chars = [m[p[0]][p[1]] for p in push_targets]
        if "#" in next_chars:
            return pos
        elif all(next_char == "." for next_char in next_chars):
            break
        else:
            new_positions = [p for p in set(push_targets) if m[p[0]][p[1]] != "."]
            stack.append(new_positions)
    else:
        raise Exception(f"infinite loop at {pos = } {direction = }")
    while stack:
        head = stack.pop()
        for p in head:
            unsafe_move(p, direction, m)
    return pos_add(pos, d)


def score(m: list[list[str]]) -> int:
    s: int = 0
    for i, row in enumerate(m):
        for j, c in enumerate(row):
            if c == "[":
                s += 100 * i + j
    return s


with open("input.txt", "r") as f:
    m_str, instructions = f.read().split("\n\n")
m: list[list[str]] = []
for row in m_str.split("\n"):
    m_row: list[str] = []
    for c in row:
        match c:
            case ".":
                m_row.extend([".", "."])
            case "#":
                m_row.extend(["#", "#"])
            case "O":
                m_row.extend(["[", "]"])
            case "@":
                m_row.extend(["@", "."])
            case _:
                raise Exception("invalid input")
    m.append(m_row)

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
