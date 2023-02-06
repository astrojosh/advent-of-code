from typing import Generator


class Grid:
    def __init__(self, input_data: str) -> None:

        self.num_visible = 0
        self.highest_scenic_score = 0

        self.create_grid(input_data)
        self.update_visibility()

    def create_grid(self, input_data: str) -> None:

        raw_row_list = input_data.splitlines()
        self.max_rows = len(raw_row_list)
        self.max_cols = len(raw_row_list[0])

        self.grid = [[int(tree_height) for tree_height in row] for row in raw_row_list]

    @staticmethod
    def check_visibility_along_direction(
        current_tree_height: int,
        trees_in_direction: Generator[int, None, None],
    ) -> tuple[bool, int]:

        scenic_score = 0
        for tree_height in trees_in_direction:
            scenic_score += 1
            if tree_height >= current_tree_height:
                is_visible = False
                return is_visible, scenic_score

        is_visible = True
        return is_visible, scenic_score

    def check_visibility_in_all_directions(
        self, tree_height: int, row_num: int, col_num: int
    ) -> tuple[bool, int]:

        trees_to_left = (self.grid[row_num][x] for x in range(col_num - 1, -1, -1))
        trees_to_right = (
            self.grid[row_num][x] for x in range(col_num + 1, self.max_cols)
        )
        trees_above = (self.grid[x][col_num] for x in range(row_num - 1, -1, -1))
        trees_below = (self.grid[x][col_num] for x in range(row_num + 1, self.max_rows))

        visible_from_left, left_scenic_score = self.check_visibility_along_direction(
            tree_height, trees_to_left
        )

        visible_from_right, right_scenic_score = self.check_visibility_along_direction(
            tree_height, trees_to_right
        )

        visible_from_above, up_scenic_score = self.check_visibility_along_direction(
            tree_height, trees_above
        )

        visible_from_below, down_scenic_score = self.check_visibility_along_direction(
            tree_height, trees_below
        )

        is_visible = (
            visible_from_left
            or visible_from_right
            or visible_from_above
            or visible_from_below
        )

        scenic_score = (
            left_scenic_score * right_scenic_score * up_scenic_score * down_scenic_score
        )

        return is_visible, scenic_score

    def update_visibility(self) -> None:
        for row_num, row in enumerate(self.grid):
            for col_num, tree_height in enumerate(row):

                on_edge_of_grid = (
                    row_num == 0
                    or row_num == self.max_rows
                    or col_num == 0
                    or col_num == self.max_cols
                )

                if on_edge_of_grid:
                    is_visible = True
                    scenic_score = 0
                else:
                    is_visible, scenic_score = self.check_visibility_in_all_directions(
                        tree_height, row_num, col_num
                    )

                if is_visible:
                    self.num_visible += 1

                if scenic_score > self.highest_scenic_score:
                    self.highest_scenic_score = scenic_score


def main(input_data: str) -> tuple[int, int]:

    grid = Grid(input_data)

    part_1_answer = grid.num_visible
    part_2_answer = grid.highest_scenic_score

    return part_1_answer, part_2_answer
