from enum import Enum
from functools import cache
import sys
from typing import override


class Direction(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


direction_to_str: dict[Direction, str] = {
    Direction.UP: "^",
    Direction.RIGHT: ">",
    Direction.DOWN: "v",
    Direction.LEFT: "<",
}


type Position = tuple[int, int]
type State = tuple[Position, Direction]


def get_direction(start: Position, end: Position) -> Direction:
    delta = (end[0] - start[0], end[1] - start[1])
    return Direction(delta)


def turn_left(state: State) -> State:
    pos, direction = state
    match direction:
        case Direction.UP:
            return (pos, Direction.LEFT)
        case Direction.RIGHT:
            return (pos, Direction.UP)
        case Direction.DOWN:
            return (pos, Direction.RIGHT)
        case Direction.LEFT:
            return (pos, Direction.DOWN)


def turn_right(state: State) -> State:
    pos, direction = state
    match direction:
        case Direction.UP:
            return (pos, Direction.RIGHT)
        case Direction.RIGHT:
            return (pos, Direction.DOWN)
        case Direction.DOWN:
            return (pos, Direction.LEFT)
        case Direction.LEFT:
            return (pos, Direction.UP)


def go_forward(state: State) -> State:
    pos, direction = state
    new_pos = pos_add(pos, direction.value)
    return (new_pos, direction)


BIG_NUMBER = sys.maxsize


class HashableDict(dict[Position, str]):
    @override
    def __hash__(self) -> int:
        return hash(frozenset(self))


m_directional: HashableDict = HashableDict(
    {
        (0, 1): "^",
        (0, 2): "A",
        (1, 0): "<",
        (1, 1): "v",
        (1, 2): ">",
    }
)
w_directional: dict[str, Position] = {
    value: key for key, value in m_directional.items()
}

m_numeric: HashableDict = HashableDict(
    {
        (0, 0): "7",
        (0, 1): "8",
        (0, 2): "9",
        (1, 0): "4",
        (1, 1): "5",
        (1, 2): "6",
        (2, 0): "1",
        (2, 1): "2",
        (2, 2): "3",
        (3, 1): "0",
        (3, 2): "A",
    }
)
w_numeric: dict[str, Position] = {value: key for key, value in m_numeric.items()}


def pos_add(p1: Position, p2: Position) -> Position:
    return (p1[0] + p2[0], p1[1] + p2[1])


@cache
def dijkstra(start: Position, end: Position, m: HashableDict) -> list[str]:
    queue: list[State] = [(start, d) for d in Direction]
    scores: dict[State, int] = {(p, d): BIG_NUMBER for p in m for d in Direction}
    seen: set[State] = set()
    prevs: dict[State, State] = {}
    for state in queue:
        scores[state] = 0

    while queue:
        queue.sort(key=lambda x: scores[x], reverse=True)
        state = queue.pop()
        seen.add(state)
        score = scores[state]
        new_states = [go_forward(state), turn_left(state), turn_right(state)]
        new_scores = [score + 1, score + 10, score + 10]
        if new_states[0][0] not in m:
            del new_states[0]
            del new_scores[0]
        for new_state, new_score in zip(new_states, new_scores):
            new_pos = new_state[0]
            if (new_pos in m) and (new_state not in seen) and (new_state not in queue):
                queue.append(new_state)
                if new_score < scores[new_state]:
                    scores[new_state] = new_score
                    prevs[new_state] = state

    final_score = BIG_NUMBER
    final_state: State | None = None
    for d in Direction:
        candidate = (end, d)
        candidate_score = scores[candidate]
        if candidate_score < final_score:
            final_state = candidate
            final_score = candidate_score

    state = final_state
    assert state is not None
    path: list[Position] = [state[0]]
    directions: list[Direction] = [state[1]]
    while state[0] != start:
        state = prevs[state]
        if state[0] != path[-1]:
            path.append(state[0])
            directions.append(state[1])

    return [direction_to_str[d] for d in directions[::-1][:-1]]


def generate_full_sequence(code: str, depth: int = 1) -> list[str]:
    sequence = generate_code_sequence(code, numeric=True)
    for _ in range(depth):
        sequence = generate_code_sequence(sequence, numeric=False)
    return sequence


def generate_code_sequence(code: str | list[str], numeric: bool = False) -> list[str]:
    start: str = "A"
    sequence: list[str] = []
    for end in code:
        sequence.extend(to_next(start, end, numeric))
        start = end
    return sequence


def to_next(start: str, end: str, numeric: bool = False) -> list[str]:
    w = w_numeric if numeric else w_directional
    m = m_numeric if numeric else m_directional
    p_start: Position = w[start]
    p_end: Position = w[end]
    directions = dijkstra(p_start, p_end, m).copy()
    directions.append("A")
    return directions


with open("input.txt", "r") as f:
    codes = [line.strip() for line in f]

score = 0
for code in codes:
    value = int(code.removesuffix("A"))
    sequence = generate_full_sequence(code, depth=2)
    score += len(sequence) * value
print(score)
