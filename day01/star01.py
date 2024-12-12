first: list[int] = []
second: list[int] = []

with open("input.txt") as f:
    for line in f:
        left, right = line.split()
        first.append(int(left))
        second.append(int(right))

sorted_first = sorted(first)
sorted_second = sorted(second)

s = sum([abs(sorted_first[i] - sorted_second[i]) for i in range(len(first))])
print(s)
