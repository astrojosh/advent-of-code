from dataclasses import dataclass
from typing import Callable
import operator


@dataclass
class Item:
    worry_level: int


@dataclass
class Monkey:
    id: int
    items: list[Item]
    operation: Callable[[int], int]
    test_condition: Callable[[int], bool]
    test_success_id: int
    test_failure_id: int
    inspect_count: int = 0

    def __post_init__(self) -> None:
        self.test_success: Monkey
        self.test_failure: Monkey

    def process_item(self, item: Item, worry_function: Callable[[int], int]):
        item.worry_level = worry_function(self.operation(item.worry_level))

        if self.test_condition(item.worry_level):
            self.test_success.items.append(item)
        else:
            self.test_failure.items.append(item)

        self.inspect_count += 1

    def process_items(self, worry_function: Callable[[int], int]):
        for item in self.items:
            self.process_item(item, worry_function)

        self.items = []


class Simulation:
    def __init__(
        self,
        input_data: str,
        num_rounds: int,
        worry_function: Callable[[int], int],
    ) -> None:
        self.num_rounds = num_rounds
        self.worry_function = worry_function

        self.process_instructions(input_data)
        self.run_simulation()

    def process_operation(self, operation_str: str) -> Callable[[int], int]:
        _, operator_str, operation_value = operation_str.split(" ")

        if operator_str == "+":
            operation_operator = operator.add
        elif operator_str == "-":
            operation_operator = operator.sub
        elif operator_str == "*":
            operation_operator = operator.mul
        elif operator_str == "/":
            operation_operator = operator.floordiv

        general_operation: Callable[[int, int], int]
        general_operation = lambda a, b: operation_operator(a, b) % self.lcm

        monkey_operation: Callable[[int], int]

        if operation_value == "old":
            monkey_operation = lambda old: general_operation(old, old)
        else:
            operation_value_int = int(operation_value)
            monkey_operation = lambda old: general_operation(old, operation_value_int)

        return monkey_operation

    def process_instruction(
        self,
        id_line: str,
        items_line: str,
        operation_line: str,
        test_line: str,
        test_success_line: str,
        test_failure_line: str,
    ) -> Monkey:
        monkey_id = int(id_line.split(" ")[1][:-1])
        worry_levels = map(int, items_line.split(": ")[1].split(", "))
        operation_str = operation_line.split("= ")[1]
        test_divisor = int(test_line.split(" ")[-1])
        test_success_id = int(test_success_line.split(" ")[-1])
        test_failure_id = int(test_failure_line.split(" ")[-1])

        monkey_items = [Item(worry_level) for worry_level in worry_levels]

        monkey_operation = self.process_operation(operation_str)

        monkey_test_condition: Callable[[int], int]
        monkey_test_condition = lambda worry_level: worry_level % test_divisor == 0

        return Monkey(
            monkey_id,
            monkey_items,
            monkey_operation,
            monkey_test_condition,
            test_success_id,
            test_failure_id,
        )

    def process_instructions(self, input_data: str):
        monkey_chunks = input_data.split("\n\n")
        monkey_lines = [monkey_chunk.splitlines() for monkey_chunk in monkey_chunks]

        self.lcm = 1
        for _, _, _, test_line, _, _ in monkey_lines:
            test_divisor = int(test_line.split(" ")[-1])
            self.lcm *= test_divisor

        self.monkeys = [
            self.process_instruction(*monkey_line) for monkey_line in monkey_lines
        ]

        for monkey in self.monkeys:
            monkey.test_success = self.monkeys[monkey.test_success_id]
            monkey.test_failure = self.monkeys[monkey.test_failure_id]

    def run_simulation(self):
        for _ in range(self.num_rounds):
            for monkey in self.monkeys:
                monkey.process_items(self.worry_function)

    @property
    def monkey_business(self):
        sorted_inspect_counts = sorted(monkey.inspect_count for monkey in self.monkeys)
        return sorted_inspect_counts[-1] * sorted_inspect_counts[-2]


def main(input_data: str) -> tuple[int, int]:
    part_1_simulation = Simulation(
        input_data,
        num_rounds=20,
        worry_function=lambda x: x // 3,
    )
    part_1_answer = part_1_simulation.monkey_business

    part_2_simulation = Simulation(
        input_data,
        num_rounds=10_000,
        worry_function=lambda x: x,
    )
    part_2_answer = part_2_simulation.monkey_business

    return part_1_answer, part_2_answer
