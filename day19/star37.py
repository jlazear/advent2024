def test_design(design: str, patterns: list[str]) -> bool:
    if design in patterns:
        return True
    for i in range(len(design)):
        sub_pattern = design[:i]
        if sub_pattern in patterns:
            sub_design = design[i:]
            if test_design(sub_design, patterns):
                return True
    return False


with open("input.txt", "r") as f:
    patterns_str, designs_str = f.read().split("\n\n")
patterns: list[str] = patterns_str.split(", ")
designs: list[str] = designs_str.split()

print(sum(test_design(design, patterns) for design in designs))
