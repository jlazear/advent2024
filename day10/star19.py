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
    seen: set[Position] = set()
    trails: set[Position] = set()
    stack: list[Position] = [start]
    while stack:
        pos = stack.pop()
        seen.add(pos)
        c = m[pos[0]][pos[1]]
        if c == 9:
            trails.add(pos)
        new_positions = neighbors(pos, m)
        for new_pos in new_positions:
            if new_pos not in seen:
                stack.append(new_pos)
    return len(trails)


print(sum(dfs(trailhead, m) for trailhead in trailheads))
