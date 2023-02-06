from dataclasses import dataclass


@dataclass
class Range:
    lower_bound: int
    upper_bound: int


def contains():
    pass


def overlaps():
    pass


def main(input_data: str) -> tuple[int, int]:

    data = input_data.splitlines()

    split_data = [map(int, x.replace(",", "-").split("-")) for x in data]

    output = sum(
        complex((c <= a <= b <= d) | (a <= c <= d <= b), (c <= b) & (a <= d))
        for a, b, c, d in split_data
    )

    return int(output.real), int(output.imag)
