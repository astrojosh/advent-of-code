import sys
import importlib
from types import ModuleType
import os


def read_data(path: str) -> str:

    with open(f"../data/{path}") as f:
        data = f.read()

    return data.rstrip()


def test_section(path: str, module: ModuleType, section: int, debug: bool = False):

    example_input = read_data(f"example_input/{path}.txt")

    if section == 1:
        answer, _ = module.main(example_input)
    else:
        _, answer = module.main(example_input)

    example_output = read_data(f"example_output/{path}.txt")

    if section == 1:
        expected_answer, _ = example_output.split(",")
    else:
        _, expected_answer = example_output.split(",")

    if not debug and str(answer) != expected_answer:
        raise ValueError(
            f"Part {section} failed tests, got {answer} when expecting {expected_answer}"
        )


def run_tests(day: str, module: ModuleType, debug: bool = False) -> None:

    print("Running code on test data")

    if os.path.isfile(f"../data/example_input/{day}_part_1.txt"):
        part_1_path = f"{day}_part_1"
        part_2_path = f"{day}_part_2"
    else:
        part_1_path, part_2_path = day, day

    test_section(part_1_path, module, section=1, debug=debug)

    if not debug:
        test_section(part_2_path, module, section=2)
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

    if len(cmd_args) == 2 and cmd_args[1] == "debug":
        run_tests(day, module, debug=True)
    else:
        run_tests(day, module)
        run(day, module)


if __name__ == "__main__":
    main()
