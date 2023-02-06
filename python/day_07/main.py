from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class StorageObject(ABC):
    name: str

    @abstractmethod
    def size(self) -> int:
        pass


@dataclass
class Directory(StorageObject):
    name: str
    path: str
    storage_objects: list[StorageObject] = field(default_factory=list)

    def size(self) -> int:
        self.object_size = sum(object.size() for object in self.storage_objects)
        return self.object_size


@dataclass
class File(StorageObject):
    name: str
    file_size: int

    def size(self) -> int:
        return self.file_size


class Command(ABC):
    output: list[StorageObject] = field(default_factory=list)


@dataclass
class CommandCD(Command):
    input: Directory
    output: list[StorageObject] = field(default_factory=list)


@dataclass
class CommandLS(Command):
    output: list[StorageObject] = field(default_factory=list)


class Data:
    def __init__(self, input_data: str) -> None:
        self.data = self.clean_data(input_data)

    @staticmethod
    def clean_data(data: str) -> list[str]:
        return data.splitlines()

    def parse_data(self) -> Data:

        current_path: list[str] = []
        self.commands: list[Command] = []
        self.directories: list[Directory] = [Directory("/", "")]

        for line in self.data:

            path = "/".join(current_path)

            if line == "$ ls":
                self.commands.append(CommandLS())

            elif line.startswith("$ cd "):

                arg = line[5:]

                if arg == "..":
                    directory = Directory(arg, path)
                    current_path.pop()

                elif arg == "/":
                    directory = self.directories[0]
                    current_path = []

                else:
                    directory = [
                        x for x in self.directories if x.path == path and x.name == arg
                    ][0]
                    current_path.append(arg)

                self.commands.append(CommandCD(directory))

            elif line.startswith("dir "):

                directory_name = line[4:]
                directory = Directory(directory_name, path)

                self.commands[-1].output.append(directory)
                self.directories.append(directory)

            else:
                file_size_str, file_name = line.split(" ")
                file_size = int(file_size_str)

                self.commands[-1].output.append(File(file_name, file_size))

        return self

    def build_tree(self) -> Data:

        self.tree = self.directories[0]
        current_directory = [self.tree]

        for command in self.commands:

            if type(command) is CommandCD:

                directory = command.input.name

                if directory == "..":
                    current_directory.pop()

                elif directory == "/":
                    current_directory = [self.tree]

                else:
                    current_directory.append(command.input)

            if type(command) is CommandLS:
                current_directory[-1].storage_objects = command.output

        # Recursively calculate the size of all directories in the tree
        self.tree.size()

        return self

    def display_tree(self) -> Data:

        self.display_general_tree(self.tree)

        return self

    @classmethod
    def display_general_tree(cls, tree: Directory, prefix: str = "-") -> None:

        print(f"{prefix} Directory(name={tree.name}, object_size={tree.object_size})")

        for file in tree.storage_objects:

            if type(file) is File:
                print(f"{prefix}- {file}")

            if type(file) is Directory:
                cls.display_general_tree(file, prefix + "-")


def main(input_data: str) -> tuple[int, int]:

    data = Data(input_data).parse_data().build_tree()

    # data.display_tree()

    sum_size_less_than_100k = sum(
        x.object_size for x in data.directories if x.object_size <= 100_000
    )

    min_size_to_leave_30k = min(
        x.object_size
        for x in data.directories
        if x.object_size >= 30_000_000 - (70_000_000 - data.tree.object_size)
    )

    # 1367870 549173
    return sum_size_less_than_100k, min_size_to_leave_30k
