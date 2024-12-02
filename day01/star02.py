from collections import Counter

first = [] 
second = []

with open('input.txt') as f:
    for i, line in enumerate(f):
        left, right = line.split()
        first.append(int(left))
        second.append(int(right))

c = Counter(second)

s = sum(v * c[v] for v in first)
print(s)
