from __future__ import annotations


class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: Move):
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Position):
        return PositionDifference(self.x - other.x, self.y - other.y)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class Vector:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Move(Vector):
    pass


class PositionDifference(Vector):
    def to_move(self) -> Move:

        abs_x = abs(self.x)
        abs_y = abs(self.y)
        is_adjacent = abs_x <= 1 and abs_y <= 1

        if is_adjacent:
            return Move(0, 0)

        sign_x = self.x // max(abs_x, 1)
        sign_y = self.y // max(abs_y, 1)

        return Move(sign_x, sign_y)


class Knot:
    def __init__(self, starting_position: Position) -> None:
        self.current_position = starting_position
        self.positions_visited: set[Position] = set([self.current_position])

    def get_closest_move_to(self, knot: Knot) -> Move:
        return (knot.current_position - self.current_position).to_move()

    def update_knot_position(self, move: Move, record_positions: bool = True) -> None:
        self.current_position += move
        if record_positions:
            self.positions_visited.add(self.current_position)

    def count_unique_positions_visited(self) -> int:
        return len(self.positions_visited)


class HeadKnot(Knot):
    def __init__(
        self,
        starting_position: Position,
        record_positions: bool,
    ) -> None:
        super().__init__(starting_position)
        self.record_positions = record_positions

    def update_position(self, move: Move) -> None:
        self.update_knot_position(move, self.record_positions)


class TailKnot(Knot):
    def __init__(
        self,
        starting_position: Position,
        head_knot: Knot,
        record_positions: bool,
    ) -> None:
        super().__init__(starting_position)
        self.head_knot = head_knot
        self.record_positions = record_positions

    def update_position(self) -> None:
        move = self.get_closest_move_to(self.head_knot)
        if move != Move(0, 0):
            self.update_knot_position(move, self.record_positions)


class Rope:
    def __init__(self, num_knots: int, record_positions: list[int]) -> None:

        assert num_knots > 1

        starting_position = Position(0, 0)
        self.head_knot = HeadKnot(starting_position, 1 in record_positions)

        self.tail_knots: list[TailKnot] = [
            TailKnot(starting_position, self.head_knot, 2 in record_positions)
        ]

        for i in range(3, num_knots + 1):
            self.tail_knots.append(
                TailKnot(starting_position, self.tail_knots[-1], i in record_positions)
            )

    def update_position(self, move: Move) -> None:
        self.head_knot.update_position(move)

        for tail_knot in self.tail_knots:
            tail_knot.update_position()

    def get_knot(self, knot_num: int) -> Knot:
        if knot_num == 1:
            return self.head_knot
        else:
            return self.tail_knots[knot_num - 2]


def main(input_data: str) -> tuple[int, int]:

    rope = Rope(num_knots=10, record_positions=[2, 10])

    instructions = input_data.splitlines()

    moves = {
        "L": Move(-1, 0),
        "R": Move(1, 0),
        "U": Move(0, 1),
        "D": Move(0, -1),
    }

    for instruction in instructions:

        direction, steps = instruction.split(" ")
        move = moves[direction]

        for _ in range(int(steps)):
            rope.update_position(move)

    part_1_answer = rope.get_knot(2).count_unique_positions_visited()
    part_2_answer = rope.get_knot(10).count_unique_positions_visited()

    return part_1_answer, part_2_answer
