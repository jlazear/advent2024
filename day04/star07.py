def check_direction(i: int, j: int, characters: dict, dx: int, dy: int):
    if dx == 0 and dy == 0:
        return False
    xloc = (i, j)
    mloc = (i + dx, j+dy)
    aloc = (i + 2*dx, j + 2*dy)
    sloc = (i + 3*dx, j + 3*dy)
    
    Xs = characters['X']
    Ms = characters['M']
    As = characters['A']
    Ss = characters['S']

    return (xloc in Xs) and (mloc in Ms) and (aloc in As) and (sloc in Ss)

def check(i: int, j: int, characters: dict):
    n = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if check_direction(i, j, characters, dx, dy):
                n += 1
    return n


characters = {'X': set(), 'M': set(), 'A': set(), 'S': set()}

with open("input.txt", 'r') as f:
    for i, row in enumerate(f.readlines()):
        for j, c in enumerate(row):
            characters.get(c, set()).add((i, j))

print(sum(check(i, j, characters) for i, j in characters['X']))
