from functools import cache


@cache
def count_design(design: str, patterns: tuple[str, ...]) -> int:
    counts: int = 0
    if design in patterns:
        counts += 1
    for i in range(1, len(design)):
        sub_pattern = design[:i]
        if sub_pattern in patterns:
            sub_design = design[i:]
            if c := count_design(sub_design, patterns):
                counts += c
    return counts


with open("input.txt", "r") as f:
    patterns_str, designs_str = f.read().split("\n\n")
patterns: tuple[str, ...] = tuple(patterns_str.split(", "))
designs: list[str] = designs_str.split()

print(sum(count_design(design, patterns) for design in designs))
