from collections import Counter


def update_stone(value: int) -> list[int]:
    if value == 0:
        return [1]

    if len(s_value := str(value)) % 2 == 0:
        return [int(s_value[: len(s_value) // 2]), int(s_value[len(s_value) // 2 :])]

    return [value * 2024]


def update(c: Counter[int]):
    new_c: Counter[int] = Counter()
    for value, n in c.items():
        for new_value in update_stone(value):
            new_c[new_value] += n
    return new_c


with open("input.txt", "r") as f:
    c = Counter([int(x) for x in f.read().strip().split()])

for n in range(25):
    c = update(c)
print(c.total())
