from collections import deque
from typing import override, final

with open("input.txt", "r") as f:
    data = deque(map(int, f.read().strip()))


@final
class Runner:
    data: deque[int] = data

    def __init__(self, ascending: bool, block_num: int, size: int):
        self.ascending: bool = ascending
        self.block_num = block_num if ascending else block_num // 2
        self.size = size
        self.blank = False

    @override
    def __eq__(self, other: object, /) -> bool:
        try:
            return self.block_num == other.block_num and self.size == other.size
        except:
            raise NotImplementedError

    def next(self) -> int:
        toret = self.block_num
        self.size -= 1
        while not self.size:
            if self.ascending:
                if self.blank:
                    self.block_num += 1
                self.size = self.data.popleft()
                self.blank = not self.blank
            else:
                self.block_num -= 1
                _ = self.data.pop()
                self.size = self.data.pop()
        return toret


right = Runner(False, len(data), data.pop())
left = Runner(True, 0, data.popleft())

s: int = 0
memory_location: int = 0
while data:
    if left.blank:
        s += memory_location * right.next()
        _ = left.next()
    else:
        s += memory_location * left.next()
    memory_location += 1

while right.size:
    s += memory_location * right.block_num
    memory_location += 1
    right.size -= 1


print(s)
