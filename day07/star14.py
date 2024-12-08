from enum import auto, Enum


class Operator(Enum):
    ADD = auto()
    MULTIPLY = auto()
    CONCATENATE = auto()
    NONE = auto()


def dfs(
    target: int,
    numbers: list[int],
    partial: int = 0,
    operator: Operator = Operator.NONE,
) -> bool:
    if partial > target:
        return False
    match operator:
        case Operator.ADD:
            partial += numbers.pop()
        case Operator.MULTIPLY:
            partial *= numbers.pop()
        case Operator.CONCATENATE:
            number = numbers.pop()
            partial = int(f"{partial}{number}")
        case Operator.NONE:
            pass
    if not numbers:
        return partial == target
    return (
        dfs(target, numbers.copy(), partial, Operator.ADD)
        or dfs(target, numbers.copy(), partial, Operator.MULTIPLY)
        or dfs(target, numbers.copy(), partial, Operator.CONCATENATE)
    )


inputs: list[tuple[int, list[int]]] = []
with open("input.txt", "r") as f:
    for line in f:
        result, numbers_str = line.split(":")
        result = int(result)
        numbers = list(int(x) for x in numbers_str.split()[::-1])
        inputs.append((result, numbers))

s = sum(target for target, numbers in inputs if dfs(target, numbers))
print(s)
