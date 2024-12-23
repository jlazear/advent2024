from collections import defaultdict


def find_triplets(
    connections: defaultdict[str, set[str]],
) -> set[frozenset[str]]:
    triplets: set[frozenset[str]] = set()
    for c1, neighbors1 in connections.items():
        for c2 in neighbors1:
            if c1 == c2:
                continue
            neighbors2 = connections[c2]
            for c3 in neighbors2:
                if (
                    c2 != c3
                    and c3 in neighbors1
                    and (c1.startswith("t") or c2.startswith("t") or c3.startswith("t"))
                ):
                    triplets.add(frozenset([c1, c2, c3]))
    return triplets


connections: defaultdict[str, set[str]] = defaultdict(set)
with open("input.txt", "r") as f:
    for line in f:
        first, second = line.strip().split("-")
        connections[first].add(second)
        connections[second].add(first)

triplets = find_triplets(connections)
print(len(triplets))
