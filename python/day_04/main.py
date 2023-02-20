from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Range:
    lower_bound: int
    upper_bound: int

    def contains(self, range: Range) -> int:
        condition_1 = self.lower_bound <= range.lower_bound
        condition_2 = range.upper_bound <= self.upper_bound
        return condition_1 and condition_2

    def overlaps(self, range: Range) -> int:
        condition_1 = self.lower_bound <= range.upper_bound
        condition_2 = range.lower_bound <= self.upper_bound
        return condition_1 and condition_2


def line_to_ranges(input_line: str) -> tuple[Range, Range]:

    raw_range_1, raw_range_2 = input_line.split(",")

    lower_bound_1, upper_bound_1 = raw_range_1.split("-")
    lower_bound_2, upper_bound_2 = raw_range_2.split("-")

    range_1 = Range(int(lower_bound_1), int(upper_bound_1))
    range_2 = Range(int(lower_bound_2), int(upper_bound_2))

    return range_1, range_2


def contained(range_1: Range, range_2: Range) -> int:
    return range_1.contains(range_2) or range_2.contains(range_1)


def main(input_data: str) -> tuple[int, int]:

    range_pairs = [line_to_ranges(input_line) for input_line in input_data.splitlines()]

    part_1_answer = sum(contained(range_1, range_2) for range_1, range_2 in range_pairs)
    part_2_answer = sum(range_1.overlaps(range_2) for range_1, range_2 in range_pairs)

    return part_1_answer, part_2_answer
