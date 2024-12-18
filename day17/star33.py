from typing import override


class ThreeBit:
    def __init__(self, A: int, B: int, C: int, instructions: list[int]):
        self.A: int = A
        self.B: int = B
        self.C: int = C
        self.instructions: list[int] = instructions
        self.pointer: int = 0
        self.output: list[int] = []

    @override
    def __str__(self) -> str:
        return f"ThreeBit(A = {self.A}, B = {self.B}, C = {self.C}, ^={self.pointer})"

    def step(self):
        if self.pointer >= len(self.instructions):
            raise ValueError(
                f"pointer ({self.pointer}) must be between 0 and {len(self.instructions)}"
            )
        opcode = self.instructions[self.pointer]
        operand = self.instructions[self.pointer + 1]
        match opcode:
            case 0:  # adv
                self.A = self.A // 2 ** self.combo(operand)
                self.pointer += 2
            case 1:  # bxl
                self.B = self.B ^ operand
                self.pointer += 2
            case 2:  # bst
                self.B = self.combo(operand) % 8
                self.pointer += 2
            case 3:  # jnz
                if self.A:
                    self.pointer = operand
                else:
                    self.pointer += 2
            case 4:  # bxc
                self.B = self.B ^ self.C
                self.pointer += 2
            case 5:  # out
                self.output.append(self.combo(operand) % 8)
                self.pointer += 2
            case 6:  # bdv
                self.B = self.A // 2 ** self.combo(operand)
                self.pointer += 2
            case 7:  # cdv
                self.C = self.A // 2 ** self.combo(operand)
                self.pointer += 2
            case _:  # invalid
                raise ValueError("invalid opcode!")

    def combo(self, operand: int):
        match operand:
            case 0 | 1 | 2 | 3 as i:
                return i
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C
            case 7:
                raise ValueError("combo(7) is reserved!")
            case _:
                raise ValueError(f"operand ({operand}) must be in range 0-7")

    def run(self):
        while 0 <= self.pointer < len(self.instructions):
            self.step()


with open("input.txt", "r") as f:
    a_str, b_str, c_str, _, program_str = f.readlines()
A = int(a_str.removeprefix("Register A: "))
B = int(b_str.removeprefix("Register B: "))
C = int(c_str.removeprefix("Register C: "))
instructions = [
    int(x) for x in program_str.strip().removeprefix("Program: ").split(",")
]

threebit = ThreeBit(A, B, C, instructions)
threebit.run()
print(",".join([str(x) for x in threebit.output]))
