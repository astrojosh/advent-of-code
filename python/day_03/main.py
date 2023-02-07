from dataclasses import dataclass
from collections.abc import Iterator


@dataclass
class Item:
    character: str

    @property
    def priority(self) -> int:
        if self.character.isupper():
            return ord(self.character) - ord("A") + 27
        else:
            return ord(self.character) - ord("a") + 1


class Rucksack:
    def __init__(self, contents: str) -> None:
        self.contents = contents
        self.split_contents_into_compartments()

    def split_contents_into_compartments(self) -> None:
        num_contents = len(self.contents)
        midpoint = num_contents // 2
        self.compartment_1 = self.contents[:midpoint]
        self.compartment_2 = self.contents[midpoint:]

    def get_common_item(self) -> Item:
        return get_common_item([self.compartment_1, self.compartment_2])


@dataclass
class Group:
    rucksacks: list[Rucksack]

    def get_common_item(self) -> Item:
        return get_common_item([rucksack.contents for rucksack in self.rucksacks])


def get_common_items(item_strings: list[str]) -> list[Item]:
    item_sets = (set(item_string) for item_string in item_strings)
    common_items: set[str] = set.intersection(*item_sets)
    return [Item(item) for item in common_items]


def get_common_item(item_strings: list[str]) -> Item:
    common_items = get_common_items(item_strings)
    assert len(common_items) == 1
    return common_items[0]


def split_elves_into_groups(
    rucksacks: list[Rucksack], num_elves_per_group: int
) -> Iterator[Group]:
    for i in range(0, len(rucksacks), num_elves_per_group):
        yield Group(rucksacks[i : i + num_elves_per_group])


def main(input_data: str) -> tuple[int, int]:

    rucksacks = [Rucksack(contents) for contents in input_data.splitlines()]

    part_1_answer = sum(rucksack.get_common_item().priority for rucksack in rucksacks)

    groups = split_elves_into_groups(rucksacks, num_elves_per_group=3)

    part_2_answer = sum(group.get_common_item().priority for group in groups)

    return part_1_answer, part_2_answer
