from collections import defaultdict

type Position = tuple[int, int]

antennas: dict[str, list[Position]] = defaultdict(list)
maxrow: int = 0
maxcol: int = 0
with open("input.txt", "r") as f:
    for i, line in enumerate(f.readlines()):
        maxrow = max(i, maxrow)
        for j, c in enumerate(line.strip()):
            maxcol = max(i, maxcol)
            if c != ".":
                antennas[c].append((i, j))


def pos_diff(a: Position, b: Position) -> Position:
    return (a[0] - b[0], a[1] - b[1])


def pos_sum(a: Position, b: Position) -> Position:
    return (a[0] + b[0], a[1] + b[1])


def valid(a: Position, maxrow: int = maxrow, maxcol: int = maxcol) -> bool:
    return (0 <= a[0] <= maxrow) and (0 <= a[1] <= maxcol)


def find_nodes(positions: list[Position], maxrow: int = maxrow, maxcol: int = maxcol):
    nodes: set[Position] = set()
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            pos1 = positions[i]
            pos2 = positions[j]
            delta = pos_diff(pos1, pos2)
            if valid(node1 := pos_sum(pos1, delta), maxrow=maxrow, maxcol=maxcol):
                nodes.add(node1)
            if valid(node2 := pos_diff(pos2, delta), maxrow=maxrow, maxcol=maxcol):
                nodes.add(node2)
    return nodes


nodes: set[Position] = set()
for frequency, positions in antennas.items():
    new_nodes = find_nodes(positions)
    nodes.update(new_nodes)
print(len(nodes))
