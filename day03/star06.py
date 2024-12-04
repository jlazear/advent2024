import re

pattern = re.compile(r"(do\(\))|(don't\(\))|mul\((\d+),(\d+)\)")

with open('input.txt', 'r') as f:
    instructions = f.read()

s = 0
flag = True
for match in pattern.finditer(instructions):
    do, dont, a, b = match.groups() 
    if do:
        flag = True
    elif dont:
        flag = False
    elif flag:
        s += int(a)*int(b)

print(s)
