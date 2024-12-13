type Position = tuple[int, int]

with open("input.txt", "r") as f:
    m = {
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


def bfs(start: Position, m: dict[Position, str]) -> set[Position]:
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


def score(group: set[Position]) -> int:
    plant_type = m[next(iter(group))]
    num_fences: int = 0
    for pos in group:
        num_neighbors = len(
            [neighbor for neighbor in neighbors(pos) if m[neighbor] == plant_type]
        )
        num_fences += 4 - num_neighbors
    return len(group) * num_fences


seen: set[Position] = set()
groups: list[set[Position]] = []
for pos in valids:
    if pos not in seen:
        group = bfs(pos, m)
        if group:
            seen.update(group)
            groups.append(group)

print(sum(score(group) for group in groups))
