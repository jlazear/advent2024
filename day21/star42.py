from collections import Counter
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
type Transition = tuple[str, str]


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


scores_dict: dict[Direction, int] = {
    Direction.LEFT: 1,
    Direction.UP: 2,
    Direction.DOWN: 3,
    Direction.RIGHT: 4,
}


@cache
def dijkstra(start: Position, end: Position, m: HashableDict) -> str:
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
        score = scores[state] * 10  # value cheaper steps sooner
        new_states = [go_forward(state), turn_left(state), turn_right(state)]
        new_scores = [score + scores_dict[state[1]], score + 10, score + 10]
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

    return "".join([direction_to_str[d] for d in directions[::-1][:-1]])


chars = "^>v<A"
transitions = ["".join([c1, c2]) for c1 in chars for c2 in chars]
chars2 = "A0123456789"
transitions2 = ["".join([c1, c2]) for c1 in chars2 for c2 in chars2]


def to_next(transition: str, numeric: bool = False, prepend: bool = False) -> str:
    start = transition[0]
    end = transition[1]
    w = w_numeric if numeric else w_directional
    m = m_numeric if numeric else m_directional
    p_start: Position = w[start]
    p_end: Position = w[end]
    directions = dijkstra(p_start, p_end, m)
    if prepend:
        directions = f"A{directions}A"
    else:
        directions = f"{directions}A"
    return directions


def generate_descent(transition: str, numeric: bool = False) -> Counter[str]:
    sequence = to_next(transition, numeric=numeric, prepend=True)
    if sequence == "A":
        return Counter({"AA": 1})
    else:
        return Counter(sequence[i : i + 2] for i in range(len(sequence) - 1))


descents = {t: generate_descent(t, numeric=False) for t in transitions}
descents.update({t: generate_descent(t, numeric=True) for t in transitions2})
costs = {t: c.total() for t, c in descents.items()}


def cmul[T](a: int, c: Counter[T]) -> Counter[T]:
    newc: Counter[T] = Counter()
    for key, count in c.items():
        newc[key] = count * a
    return newc


def descend(c: Counter[str]) -> Counter[str]:
    new_counter: Counter[str] = Counter()
    for transition, count in c.items():
        new_counter += cmul(count, descents[transition])
    return new_counter


def solve(sequence: str, depth: int = 2) -> int:
    sequence = f"A{sequence}"
    c = Counter(sequence[i : i + 2] for i in range(len(sequence) - 1))
    for i in range(depth):
        c = descend(c)
    return c.total()


with open("input.txt", "r") as f:
    codes = [line.strip() for line in f]
print(sum(int(code.removesuffix("A")) * solve(code, depth=26) for code in codes))
