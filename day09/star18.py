from dataclasses import dataclass


@dataclass
class Location:
    size: int
    location: int
    block_num: int = -1

    def value(self):
        return self.block_num * (
            self.location * self.size + self.size * (self.size - 1) // 2
        )


files: list[Location] = []
blanks: list[Location] = []

with open("input.txt", "r") as f:
    data = f.read().strip()
    mem_location: int = 0
    for i, c in enumerate(data):
        c = int(c)
        if i % 2 == 0:
            files.append(Location(size=c, location=mem_location, block_num=i // 2))
        else:
            blanks.append(Location(size=c, location=mem_location))
        mem_location += c

files_reordered: list[Location] = []
while files:
    file = files.pop()
    for i, blank in enumerate(blanks):
        if file.location < blank.location:
            break
        if file.size <= blank.size:
            file.location = blank.location
            if file.size < blank.size:
                blanks[i] = Location(
                    size=blank.size - file.size, location=blank.location + file.size
                )
            else:
                del blanks[i]
            break
    files_reordered.append(file)

print(sum(file.value() for file in files_reordered))
