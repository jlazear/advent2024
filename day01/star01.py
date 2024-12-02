first = [] 
second = []

with open('input.txt') as f:
    for i, line in enumerate(f):
        left, right = line.split()
        first.append(int(left))
        second.append((right))

sorted_first = sorted(first)
sorted_second = sorted(second)

s = sum([abs(sorted_first[i] - sorted_second[i]) for i in range(len(first))])
print(s)
