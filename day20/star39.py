import sys

type Position = tuple[int, int]

BIG_NUMBER = sys.maxsize


def dijkstra(start: Position, m: dict[Position, str]) -> dict[Position, int]:
    queue: list[Position] = [start]
    scores: dict[Position, int] = {p: BIG_NUMBER for p in m}
    seen: set[Position] = set()
    scores[start] = 0

    while queue:
        queue.sort(key=lambda x: scores[x], reverse=True)
        pos = queue.pop()
        seen.add(pos)
        score = scores[pos]
        if m[pos] == "E":
            continue
        i, j = pos
        neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        neighbors = [
            neighbor
            for neighbor in neighbors
            if (
                neighbor in m
                and m[neighbor] != "#"
                and neighbor not in seen
                and neighbor not in queue
            )
        ]
        queue.extend(neighbors)
        for neighbor in neighbors:
            new_score = score + 1
            scores[neighbor] = min(scores[neighbor], new_score)
    return scores


def find_cheats(pos: Position, scores: dict[Position, int]) -> list[int]:
    score = scores[pos]
    i, j = pos
    neighbors = [(i - 2, j), (i + 2, j), (i, j - 2), (i, j + 2)]
    neighbors = [
        neighbor
        for neighbor in neighbors
        if neighbor in scores and scores[neighbor] < BIG_NUMBER
    ]
    deltas = [
        delta for neighbor in neighbors if (delta := scores[neighbor] - score - 2) > 0
    ]
    return deltas


def find_all_cheats(scores: dict[Position, int]):
    cheats: list[int] = []
    for pos in scores:
        cheats.extend(find_cheats(pos, scores))
    return cheats


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
cheats = find_all_cheats(scores)
print(sum(cheat >= 100 for cheat in cheats))
