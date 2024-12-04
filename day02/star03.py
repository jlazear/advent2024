def evaluate_line(line: str):
    sequence = [int(x) for x in line.split()]
    if sequence[0] == sequence[1]:
        return False
    sign = (sequence[1] - sequence[0])/abs(sequence[1] - sequence[0])
    for i in range(len(sequence) - 1):
        delta = (sequence[i+1] - sequence[i]) * sign
        if delta < 1 or delta > 3:
            return False
    return True

with open("input.txt", 'r') as f:
    print(sum(evaluate_line(line) for line in f))
