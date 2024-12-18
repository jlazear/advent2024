from functools import cache
import math

type Registers = tuple[int, int, int]
type Instructions = tuple[int, ...]
type State = tuple[Registers, int, int | None]  # ((A, B, C), pointer, output)


opcodes = ["adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv"]
opcode_dict = dict(enumerate(opcodes))
combos = ["0", "1", "2", "3", "A", "B", "C", "R"]
combos_dict = dict(enumerate(combos))


@cache
def step(registers: Registers, pointer: int, instructions: Instructions) -> State:
    opcode = instructions[pointer]
    operand = instructions[pointer + 1]
    A, B, C = registers
    output = None
    match opcode:
        case 0:  # adv
            A = A // 2 ** combo(registers, operand)
            pointer += 2
        case 1:  # bxl
            B = B ^ operand
            pointer += 2
        case 2:  # bst
            B = combo(registers, operand) % 8
            pointer += 2
        case 3:  # jnz
            if A:
                pointer = operand
            else:
                pointer += 2
        case 4:  # bxc
            B = B ^ C
            pointer += 2
        case 5:  # out
            output = combo(registers, operand) % 8
            pointer += 2
        case 6:  # bdv
            B = A // 2 ** combo(registers, operand)
            pointer += 2
        case 7:  # cdv
            C = A // 2 ** combo(registers, operand)
            pointer += 2
        case _:  # invalid
            raise ValueError("invalid opcode!")
    new_registers = (A, B, C)
    return (new_registers, pointer, output)


@cache
def combo(registers: Registers, operand: int) -> int:
    A, B, C = registers
    match operand:
        case 0 | 1 | 2 | 3 as i:
            return i
        case 4:
            return A
        case 5:
            return B
        case 6:
            return C
        case 7:
            raise ValueError("combo(7) is reserved!")
        case _:
            raise ValueError(f"operand ({operand}) must be in range 0-7")


def run(
    registers: Registers, instructions: Instructions, pointer: int = 0
) -> list[int]:
    output_list: list[int] = []
    # print("--------")  # DELME
    while 0 <= pointer < len(instructions):
        registers, pointer, output = step(registers, pointer, instructions)
        if output is not None:
            output_list.append(output)
    return output_list


with open("input.txt", "r") as f:
    a_str, b_str, c_str, _, program_str = f.readlines()
A = int(a_str.removeprefix("Register A: "))
B = int(b_str.removeprefix("Register B: "))
C = int(c_str.removeprefix("Register C: "))
instructions = tuple(
    [int(x) for x in program_str.strip().removeprefix("Program: ").split(",")]
)


def a_from_digits(digits: list[int]) -> int:
    return sum(8 ** (len(digits) - i - 1) * d for i, d in enumerate(digits))


target = instructions
digits = [0] * len(target)


def op(
    digits: list[int], B: int = B, C: int = C, instructions: Instructions = instructions
) -> Instructions:
    a = a_from_digits(digits)
    return tuple(run((a, B, C), instructions))


i = 0
output = op(digits)
while output != instructions:
    # print(f"\n{i = } {digits = }\n{output = }\ninstru = {instructions}")  # DELME
    if digits[i] >= 7:
        digits[i] = 0
        digits[i - 1] += 1
        if i == 0:
            print("failed")
            break
        i -= 1
    else:
        digits[i] += 1
    output = op(digits)
    if output[-i - 1] == instructions[-i - 1]:
        # print(f"last digit match {output[-i - 1] = },  {instructions[-i - 1] = }")
        i += 1


print(digits)
a = a_from_digits(digits)
# print(f"{a = }")
# print(run((a, B, C), instructions))
# print(instructions)

best_a = a
for delta in range(8**6):
    new_a = a - delta
    new_output = run((new_a, B, C), instructions)
    if tuple(new_output) == instructions:
        # print(f"{tuple(new_output) == instructions}")
        # print(f"{new_output}")
        # print(f"{instructions}")
        # print(new_a)
        best_a = min(best_a, new_a)
print(best_a)


# for a in range(64):
#     print(a, run((a, B, C), instructions))


def find_bounds(B, C, instructions, offset: int = 0):
    op = lambda a: len(run((a, B, C), instructions))
    left: int = 1
    right: int = 1
    output_len: int = 0
    while output_len < len(instructions) + offset:
        right *= 2
        print(f"{right = }")  # DELME
        output_len = op(right)

    while right - left >= 2:
        print(f"{left = } {right = }")  # DELME
        mid = (left + right) // 2
        output_len = op(mid)
        if output_len < len(instructions) + offset:
            left = mid
        else:
            right = mid
    return left, right


# _, bottom = find_bounds(B, C, instructions)
# top, _ = find_bounds(B, C, instructions, 1)
#
# print(run((bottom, B, C), instructions))
# print(run((top, B, C), instructions))
# print(len(instructions))
# print(top, bottom)
# print(top - bottom)
# print(math.log10(bottom), math.log2(bottom), math.log2(bottom) / math.log2(8))
# print(math.log10(top), math.log2(top), math.log2(top) / math.log2(8))


# for delta in range(0, (top - bottom), (top - bottom) // 256):
#     a = bottom + delta
#     print(f"{a = }")
#     print(run((a, B, C), instructions))
# # for i in range(128):
# #     firsts = []
# #     for delta in range(0, 9):
# #         a = bottom + delta + 8 * i
# #         firsts.append(run((a, B, C), instructions)[0])
# #     print(firsts)

# for a in range(bottom, top):
#     if (a - bottom) % ((top - bottom) // 1_000_000) == 0:
#         print(f"{a = } ({(a - bottom) / (top - bottom)})")
#     registers = (a, B, C)
#     output_list = run(registers, instructions)
#     if tuple(output_list) == instructions:
#         print(f"{a = }")
#         break
# a = 1
# max_iter = 1000000
# for i in range(max_iter):  # infinite loops bad
#     registers = (a, B, C)
#     output_list = run(registers, instructions, 0)
#     if (i % (max_iter // 10)) == 0:
#         print(f"{i = } / {max_iter}")
#         print(f"{len(output_list) = }\n{output_list}")
#     if tuple(output_list) == instructions:
#         print(i)
#         break
#     if len(output_list) < len(instructions):
#         a *= 10
#         print(f"10x! new {a = }")
#     a += 1
# else:
#     raise Exception("Infinite loop!")
