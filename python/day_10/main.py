from abc import ABC, abstractmethod
from dataclasses import dataclass


class Cycle(ABC):
    @abstractmethod
    def update_register(self, current_register: int) -> int:
        ...


class DoNothing(Cycle):
    def update_register(self, current_register: int) -> int:
        return current_register


@dataclass
class UpdateRegister(Cycle):
    add_x: int

    def update_register(self, current_register: int) -> int:
        return current_register + self.add_x


class Instruction(ABC):
    @abstractmethod
    def to_cycles(self) -> list[Cycle]:
        ...


@dataclass
class AddX(Instruction):
    add_x: int

    def to_cycles(self) -> list[Cycle]:
        return [DoNothing(), UpdateRegister(self.add_x)]


class NoOp(Instruction):
    def to_cycles(self) -> list[Cycle]:
        return [DoNothing()]


class Program:
    def __init__(self, raw_instructions: str) -> None:
        self.raw_instructions = raw_instructions
        self.parse_instructions()
        self.convert_instructions_to_cycles()
        self.execute_cycles()

    @staticmethod
    def parse_instruction(instruction: str) -> Instruction:
        if instruction == "noop":
            return NoOp()
        else:
            add_x = int(instruction.split(" ")[1])
            return AddX(add_x)

    def parse_instructions(self) -> None:
        raw_instructions_list = self.raw_instructions.splitlines()
        self.instructions = map(self.parse_instruction, raw_instructions_list)

    def convert_instructions_to_cycles(self) -> None:
        self.cycles = [
            cycle
            for instruction in self.instructions
            for cycle in instruction.to_cycles()
        ]

    def execute_cycles(self) -> None:

        current_register = 1
        self.register = [current_register]

        self.screen = ""
        num_pixels_in_row = 40

        for i, cycle in enumerate(self.cycles):

            pixel = i % num_pixels_in_row

            if pixel == 0:
                self.screen += "\n"

            if current_register in [pixel - 1, pixel, pixel + 1]:
                self.screen += "#"
            else:
                self.screen += "."

            current_register = cycle.update_register(current_register)
            self.register.append(current_register)

    @property
    def signal_strength(self) -> int:

        start = 20
        step = 40
        positions = range(start, len(self.register), step)
        components = [self.register[position - 1] for position in positions]

        signal_strength = sum(x * y for x, y in zip(positions, components))

        return signal_strength


def main(input_data: str) -> tuple[int, str]:

    program = Program(input_data)

    part_1_answer = program.signal_strength
    part_2_answer = program.screen

    return part_1_answer, part_2_answer
