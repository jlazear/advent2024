import re

pattern = re.compile(r"mul\((\d+),(\d+)\)")

with open('input.txt', 'r') as f:
    instructions = f.read()

s = 0
for match in pattern.finditer(instructions):
    a, b = match.groups()
    s += int(a)*int(b)
print(s)
