from enum import Enum
from typing import NamedTuple
import heapq
from functools import total_ordering
import sys

BIG_NUMBER = sys.maxsize

type Position = tuple[int, int]


class Direction(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

    def __init__(self, row: int, col: int):
        self.n: int = -1
        match row, col:
            case 0, 1:
                self.n = 0
            case -1, 0:
                self.n = 1
            case 0, -1:
                self.n = 2
            case 1, 0:
                self.n = 3
            case _:
                raise ValueError(f"invalid {row=}, {col=}")


class State(NamedTuple):
    pos: Position
    dir: Direction


@total_ordering
class QueueItem:
    def __init__(self, state: State, score: int):
        self.state: State = state
        self.score: int = score

    def __eq__(self, other):
        if isinstance(other, State):
            return self.state == other
        else:
            return self.state == other.state

    def __lt__(self, other):
        return self.score < other.score


def turn_left(state: State) -> State:
    pos, dir = state
    match dir:
        case Direction.NORTH:
            return State(pos, Direction.WEST)
        case Direction.EAST:
            return State(pos, Direction.NORTH)
        case Direction.SOUTH:
            return State(pos, Direction.EAST)
        case Direction.WEST:
            return State(pos, Direction.SOUTH)


def turn_right(state: State) -> State:
    pos, dir = state
    match dir:
        case Direction.NORTH:
            return State(pos, Direction.EAST)
        case Direction.EAST:
            return State(pos, Direction.SOUTH)
        case Direction.SOUTH:
            return State(pos, Direction.WEST)
        case Direction.WEST:
            return State(pos, Direction.NORTH)


def go_forward(state: State) -> State:
    pos, dir = state
    delta = dir.value
    return State((pos[0] + delta[0], pos[1] + delta[1]), dir)


def go_back(state: State) -> State:
    pos, dir = state
    delta = dir.value
    return State((pos[0] - delta[0], pos[1] - delta[1]), dir)


def dijkstra(start: Position, m: dict[Position, str]) -> dict[State, int]:
    init_state = State(start, Direction.EAST)
    scores: dict[State, int] = {}
    for node, c in m.items():
        if c != "#":
            for d in Direction:
                scores[State(node, d)] = BIG_NUMBER
    scores[init_state] = 0

    seen: set[State] = set()
    init_item = QueueItem(init_state, 0)
    queue: list[QueueItem] = [init_item]
    while queue:
        item = heapq.heappop(queue)
        score = item.score
        state = item.state

        if state in seen:
            continue
        seen.add(state)

        next_states = [go_forward(state), turn_left(state), turn_right(state)]
        next_scores = [score + 1, score + 1000, score + 1000]
        if m[next_states[0].pos] == "#":
            del next_states[0]
            del next_scores[0]
        for new_state, new_score in zip(next_states, next_scores):
            if new_state not in seen and new_state not in queue:
                heapq.heappush(queue, QueueItem(new_state, new_score))
                scores[new_state] = new_score
            elif new_state in queue:
                i_old_state = queue.index(new_state)
                if new_score < queue[i_old_state].score:
                    queue[i_old_state].score = new_score
                    heapq.heapify(queue)
                    scores[new_state] = new_score
    return scores


def trace_back(
    end: Position, scores: dict[State, int], m: dict[Position, str]
) -> set[State]:
    end_states = [State(end, d) for d in Direction]
    min_end = min(scores[end_state] for end_state in end_states)
    end_states = [end_state for end_state in end_states if scores[end_state] == min_end]

    seen: set[State] = set()
    stack: list[QueueItem] = [QueueItem(state, min_end) for state in end_states]
    while stack:
        item = stack.pop()
        state = item.state
        score = item.score

        seen.add(state)

        next_states = [go_back(state), turn_left(state), turn_right(state)]
        next_scores = [score - 1, score - 1000, score - 1000]

        if m[next_states[0].pos] == "#":
            del next_states[0]
            del next_scores[0]

        for new_state, new_score in zip(next_states, next_scores):
            if scores[new_state] == new_score:
                stack.append(QueueItem(new_state, new_score))
    return seen


m: dict[Position, str] = {}
start: Position = (-1, -1)  # to appease mypy
end: Position = (-1, -1)  # to appease mypy
with open("input.txt", "r") as f:
    for i, row in enumerate(f.readlines()):
        for j, c in enumerate(row.strip()):
            m[(i, j)] = c
            if c == "S":
                start = (i, j)
            elif c == "E":
                end = (i, j)


scores = dijkstra(start, m)
seen = trace_back(end, scores, m)
seen_pos = set(state.pos for state in seen)
print(len(seen_pos))
