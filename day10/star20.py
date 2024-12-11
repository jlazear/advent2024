type Position = tuple[int, int]
with open("input.txt", "r") as f:
    m = [list(map(int, row.strip())) for row in f.readlines()]

trailheads: list[Position] = [
    (i, j) for i, row in enumerate(m) for j, c in enumerate(row) if c == 0
]
valids: list[Position] = [(i, j) for i in range(len(m)) for j in range(len(m[0]))]


def neighbors(pos: Position, m: list[list[int]]):
    i, j = pos
    c = m[i][j]
    neighbors: list[Position] = []
    neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    neighbors = [
        (row, col)
        for (row, col) in neighbors
        if (row, col) in valids and m[row][col] == c + 1
    ]
    return neighbors


def dfs(start: Position, m: list[list[int]]):
    seen: set[tuple[Position, ...]] = set()
    trails: set[tuple[Position, ...]] = set()
    stack: list[tuple[Position, ...]] = [(start,)]
    while stack:
        trail = stack.pop()
        seen.add(trail)
        pos = trail[-1]
        c = m[pos[0]][pos[1]]
        if c == 9:
            trails.add(trail)
        new_positions = neighbors(pos, m)
        for new_pos in new_positions:
            new_trail = trail + (new_pos,)
            if new_trail not in seen:
                stack.append(new_trail)
    return len(trails)


print(sum(dfs(trailhead, m) for trailhead in trailheads))
