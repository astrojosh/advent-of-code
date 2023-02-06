import sys
import importlib
from types import ModuleType
import os


def read_data(path: str) -> str:

    with open(f"../data/{path}") as f:
        data = f.read()

    # Remove trailing newline
    cleaned_data = data.rstrip()

    return cleaned_data


def run_tests(day: str, module: ModuleType, test_output: bool = True) -> None:
    print("Running code on test data")
    if os.path.isfile(f"../data/example_input/{day}_part_1.txt"):
        example_input = read_data(f"example_input/{day}_part_1.txt")
        example_output = read_data(f"example_output/{day}_part_1.txt")
        expected_part_1_answer = example_output
        part_1_answer, _ = module.main(example_input)

        if test_output and str(part_1_answer) != expected_part_1_answer:
            raise ValueError(
                f"Part 1 failed tests, got {part_1_answer} when expecting {expected_part_1_answer}"
            )

        if test_output:
            example_input = read_data(f"example_input/{day}_part_2.txt")
            example_output = read_data(f"example_output/{day}_part_2.txt")
            expected_part_2_answer = example_output
            _, part_2_answer = module.main(example_input)

    else:
        example_input = read_data(f"example_input/{day}.txt")
        example_output = read_data(f"example_output/{day}.txt")
        expected_part_1_answer, expected_part_2_answer = example_output.split(",")
        part_1_answer, part_2_answer = module.main(example_input)

        if test_output and str(part_1_answer) != expected_part_1_answer:
            raise ValueError(
                f"Part 1 failed tests, got {part_1_answer} when expecting {expected_part_1_answer}"
            )

    if test_output and str(part_2_answer) != expected_part_2_answer:
        raise ValueError(
            f"Part 2 failed tests, got {part_2_answer} when expecting {expected_part_2_answer}"
        )

    if test_output:
        print("Tests passed successfully\n")


def run(day: str, module: ModuleType) -> None:
    print("Running code on input data")

    input_data = read_data(f"input/{day}.txt")
    part_1_answer, part_2_answer = module.main(input_data)

    print(f"Part 1 Answer = {part_1_answer}")
    print(f"Part 2 Answer = {part_2_answer}")


def main() -> None:

    cmd_args = sys.argv[1:]
    day = cmd_args[0]

    module = importlib.import_module(f"{day}.main")

    if len(cmd_args) == 2:
        run_tests(day, module, test_output=False)
    else:
        run_tests(day, module)
        run(day, module)


if __name__ == "__main__":

    main()
