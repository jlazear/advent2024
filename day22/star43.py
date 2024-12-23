def mix(value: int, into: int) -> int:
    return value ^ into


def prune(a: int) -> int:
    return a % 16777216


def evolve(secret: int) -> int:
    result = secret * 64
    secret = mix(result, secret)
    secret = prune(secret)

    result = secret // 32
    secret = mix(result, secret)
    secret = prune(secret)

    result = secret * 2048
    secret = mix(result, secret)
    secret = prune(secret)
    return secret


def evolveN(secret: int, n: int) -> int:
    for _ in range(n):
        secret = evolve(secret)
    return secret


numbers = [int(line) for line in open("input.txt")]

print(sum(evolveN(number, 2000) for number in numbers))
