from collections import defaultdict

type Sequence = tuple[int, int, int, int]


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


def get_prices(secret: int, n: int) -> list[int]:
    prices: list[int] = [secret % 10]
    for _ in range(n):
        secret = evolve(secret)
        prices.append(secret % 10)
    return prices


def generate_sequences(prices: list[int]) -> dict[Sequence, int]:
    d: dict[Sequence, int] = {}
    for i in range(len(prices) - 5):
        sequence: Sequence = (
            prices[i + 1] - prices[i],
            prices[i + 2] - prices[i + 1],
            prices[i + 3] - prices[i + 2],
            prices[i + 4] - prices[i + 3],
        )
        if sequence not in d:
            d[sequence] = prices[i + 4]
    return d


numbers = [int(line) for line in open("input.txt")]
all_prices: defaultdict[Sequence, int] = defaultdict(int)
for number in numbers:
    prices = get_prices(number, 2000)
    d = generate_sequences(prices)
    for sequence, price in d.items():
        all_prices[sequence] += price

print(max(all_prices.values()))
