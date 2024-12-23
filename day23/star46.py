from collections import defaultdict
from itertools import combinations


def test(computers: set[str], connections: defaultdict[str, set[str]]) -> bool:
    for c1 in computers:
        for c2 in computers:
            if c1 == c2:
                continue
            if c1 not in connections[c2]:
                return False
    return True


def find_interconnected(connections: defaultdict[str, set[str]]) -> set[str]:
    longest: set[str] = set()
    for c, neighbors in connections.items():
        for i in range(2, len(neighbors)):
            for combo in combinations(neighbors, i):
                candidate = set(combo)
                candidate.add(c)
                if test(candidate, connections) and len(candidate) > len(longest):
                    longest = candidate
    return longest


connections: defaultdict[str, set[str]] = defaultdict(set)
with open("input.txt", "r") as f:
    for line in f:
        first, second = line.strip().split("-")
        connections[first].add(second)
        connections[second].add(first)

longest = find_interconnected(connections)
print(",".join(sorted(longest)))
