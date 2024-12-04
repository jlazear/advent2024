def check(i: int, j: int, characters: dict):
    Ms = characters['M']
    Ss = characters['S']

    topleft = (i+1, j+1)
    bottomright = (i-1, j-1)
    topright = (i-1, j+1)
    bottomleft = (i+1, j-1)

    return (((topleft in Ms and bottomright in Ss) or (topleft in Ss and bottomright in Ms)) and
            ((topright in Ms and bottomleft in Ss) or (topright in Ss and bottomleft in Ms)))


characters = {'M': set(), 'A': set(), 'S': set()}

with open("input.txt", 'r') as f:
    for i, row in enumerate(f.readlines()):
        for j, c in enumerate(row):
            characters.get(c, set()).add((i, j))

print(sum(check(i, j, characters) for i, j in characters['A']))
