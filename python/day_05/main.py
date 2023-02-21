from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Crate:
    label: str


@dataclass
class Stack:
    crates: list[Crate]

    @classmethod
    def from_labels(cls, labels: tuple[str]) -> Stack:
        return cls([Crate(label) for label in labels if label != " "])

    def move_crates(self, num_crates: int, stack: Stack) -> None:
        stack.receive_crates(self.crates[-num_crates:])
        del self.crates[-num_crates:]

    def receive_crates(self, received_crates: list[Crate]) -> None:
        self.crates += received_crates

    @property
    def top_crate_label(self) -> str:
        return self.crates[-1].label


@dataclass
class Move:
    num_crates: int
    from_stack: Stack
    to_stack: Stack

    def move_crates(self, num_moves: int) -> None:
        self.from_stack.move_crates(num_moves, self.to_stack)

    def move_one_by_one(self) -> None:
        for _ in range(self.num_crates):
            self.move_crates(1)

    def move_all(self) -> None:
        self.move_crates(self.num_crates)


class Simulation:
    def __init__(self, input_data: str, can_move_multiple: bool) -> None:
        self.input_data = input_data
        self.can_move_multiple = can_move_multiple

        self.process_input_data()
        self.process_stacks()
        self.process_instructions()

        self.run_simulation()

    def process_input_data(self) -> None:
        crate_data, instruction_data = self.input_data.split("\n\n")

        stack_lines = crate_data.splitlines()[:-1]
        self.crate_labels = [stack_line[1::4] for stack_line in stack_lines[::-1]]

        self.instruction_lines = instruction_data.splitlines()

    def process_stacks(self) -> None:
        stack_labels = zip(*self.crate_labels)
        self.stacks = [Stack.from_labels(label) for label in stack_labels]

    def process_instruction(self, instruction: str) -> Move:
        instruction_numbers = map(int, instruction.split(" ")[1::2])
        num_crates, from_stack_label, to_stack_label = instruction_numbers

        from_stack = self.stacks[from_stack_label - 1]
        to_stack = self.stacks[to_stack_label - 1]

        return Move(num_crates, from_stack, to_stack)

    def process_instructions(self) -> None:
        self.instructions_list = map(self.process_instruction, self.instruction_lines)

    def run_simulation(self) -> None:
        for instruction in self.instructions_list:
            instruction.move_all() if self.can_move_multiple else instruction.move_one_by_one()

    @property
    def top_crate_labels(self) -> str:
        return "".join(stack.top_crate_label for stack in self.stacks)


def main(input_data: str) -> tuple[str, str]:

    part_1_sim = Simulation(input_data, can_move_multiple=False)
    part_2_sim = Simulation(input_data, can_move_multiple=True)

    part_1_answer = part_1_sim.top_crate_labels
    part_2_answer = part_2_sim.top_crate_labels

    return part_1_answer, part_2_answer
