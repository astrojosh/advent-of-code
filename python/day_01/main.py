import operator


class Elf:
    def __init__(self, raw_data: str) -> None:
        self.parse_data(raw_data)
        self.calculate_total_calories()

    def parse_data(self, raw_data: str) -> None:
        # Split on line breaks to seperate each elf calorie amount
        self.calories_list = map(int, raw_data.splitlines())

    def calculate_total_calories(self) -> None:
        self.total_calories = sum(self.calories_list)


class Elves:
    def __init__(self, input_data: str) -> None:
        self.create_elves(input_data)
        self.order_elves()

    def create_elves(self, input_data: str) -> None:
        # Split on blank lines to seperate each elf
        self.elves = map(Elf, input_data.split("\n\n"))

    def order_elves(self) -> None:
        order_key = operator.attrgetter("total_calories")
        self.ordered_elves = sorted(self.elves, key=order_key, reverse=True)

    def get_top_elf_calories(self) -> int:
        return self.ordered_elves[0].total_calories

    def get_top_n_elves_calories_sum(self, num_elves: int) -> int:
        top_n_elves = self.ordered_elves[:num_elves]
        return sum(elf.total_calories for elf in top_n_elves)


def main(input_data: str) -> tuple[int, int]:

    elves = Elves(input_data)

    part_1_answer = elves.get_top_elf_calories()
    part_2_answer = elves.get_top_n_elves_calories_sum(num_elves=3)

    return part_1_answer, part_2_answer
