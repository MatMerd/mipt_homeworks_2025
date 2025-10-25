import csv
import numpy as np
from typing import Sequence, Any, Callable, overload
from numpy.typing import NDArray
import copy as _copy
import ast
import sys
from typing import TextIO
import random
import datetime


class Vector:
    def __init__(self, elements: Sequence[Any] | None = None, dtype_=object):
        self.__dtype = dtype_
        if self.__dtype is None:
            self.__dtype = object

        self.size: int = 0
        self.capacity: int = 0
        self.data: NDArray[Any] = np.empty(0, dtype=dtype_)
        if elements is None:
            return

        self.data = np.empty(len(elements), dtype=dtype_)
        self.capacity = len(elements)
        for element in elements:
            self.data[self.size] = element
            self.size += 1

    def __len__(self) -> int:
        return self.size

    @overload
    def __getitem__(self, index: int) -> Any:
        ...

    @overload
    def __getitem__(self, index: slice) -> Any:
        ...

    @overload
    def __getitem__(self, index: tuple) -> Any:
        ...

    def __getitem__(self, position: int | slice | tuple):
        if isinstance(position, tuple):
            rows, col = position
            if isinstance(rows, slice) and rows == slice(None) and isinstance(col, int):
                return np.array([self.data[i][col] for i in range(self.size)], dtype=self.__dtype)
            return self._as_matrix()[position]
        return self.data[position]

    def __setitem__(self, position: int, value: Any):
        self.data[position] = value

    def __iter__(self):
        for position in range(self.size):
            yield self.data[position]

    def __str__(self) -> str:
        return "[" + ", ".join(str(self.data[position]) for position in range(self.size)) + "]"

    def _as_matrix(self) -> np.ndarray:
        if self.size == 0:
            return np.empty((0, 0), dtype=self.__dtype)
        return np.stack(self.data[:self.size], axis=0)

    def copy(self) -> "Vector":
        new_vector = Vector()
        new_vector.size = self.size
        new_vector.capacity = self.capacity
        new_vector.data = self.data.copy()
        return new_vector

    def deepcopy(self) -> "Vector":
        new_vector = Vector()
        new_vector.size = self.size
        new_vector.capacity = self.capacity
        if getattr(self.data, "dtype", None) is not None and self.data.dtype == object:
            new_vector.data = np.empty(self.data.shape, dtype=self.__dtype)
            for position, element in enumerate(self.data):
                new_vector.data[position] = _copy.deepcopy(element)
        else:
            new_vector.data = self.data.copy()
        return new_vector

    def append(self, new_element: Any):
        self.reallocate()
        self.data[self.size] = new_element
        self.size += 1

    def reallocate(self):
        if self.size < self.capacity:
            return
        self.capacity = 2 * self.capacity + 1
        new_data = np.full(self.capacity, dtype=self.__dtype)
        for position in range(self.size):
            new_data[position] = self.data[position]
        self.data = new_data

    def array(self):
        return self.data[:self.size]

    def empty(self) -> bool:
        return self.size == 0

    def length(self):
        return self.size


class ReadCSV:  # Vector(np.array(object))
    def __init__(self, filename: str | None = None):
        if filename is None:
            return

        self.translate: dict[str, int] = {}
        self.table: Vector = Vector()  # TODO: менять размер в open и setCSVFILE.
        self.re_translate: Vector = Vector()

        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for line_index, row in enumerate(csv_reader):
                if line_index == 0:
                    for i, el in enumerate(row):
                        self.translate[el] = i
                        self.re_translate.append(el)
                    continue
                massive: NDArray[Any] = np.array(row, dtype=object)
                for i, el in enumerate(row):
                    massive[i] = el
                self.table.append(massive)

        self._cast_columns_inplace()

    def setCSVFile(self, filename: str) -> None:
        self.translate = {}
        self.table = Vector()
        self.re_translate = Vector()

        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for line_index, row in enumerate(csv_reader):
                if line_index == 0:
                    for i, el in enumerate(row):
                        self.translate[el] = i
                        self.re_translate.append(el)
                    continue
                massive: NDArray[Any] = np.array(row, dtype=object)
                for i, el in enumerate(row):
                    massive[i] = el
                self.table.append(massive)
        self._cast_columns_inplace()

    def head(self, number_of_lines: int):
        if self.table.empty() or number_of_lines < 0:
            return None

        number_of_lines = min(number_of_lines, self.table.size)
        return self.table[:number_of_lines].copy()

    def tail(self, number_of_lines: int):
        if self.table.empty() or number_of_lines < 0:
            return None

        number_of_lines = min(number_of_lines, self.table.size)
        return self.table[-number_of_lines:].copy()

    def getColumnNames(self):
        if not self.translate:
            return None
        return list(self.translate.keys())

    def getColumnByName(self, column_name: str | None = None):
        if column_name is None or column_name not in self.translate:
            return None
        position = self.translate[column_name]
        return Vector([row[position] for row in self.table.array()])

    @staticmethod
    def convert_to_common_type(data: Sequence[str]) -> list[Any]:
        if len(data) == 0:
            return []

        def try_cast(seq: Sequence[str], caster: Callable[[str], Any]) -> list[Any]:
            out: list[Any] = []
            for s in seq:
                out.append(caster(s.strip()))
            return out

        def to_int(s: str) -> int:
            return int(s)

        def to_float(s: str) -> float:
            return float(s)

        def to_bool(s: str) -> bool:
            possible_values = {"true": True, "false": False}
            s = s.lower()
            if s not in possible_values:
                raise ValueError("Not a bool literal!!!")
            return possible_values[s]

        def to_list(s: str) -> list:
            try:
                val = ast.literal_eval(s)
                if isinstance(val, (list, tuple)):
                    return list(val)
            except Exception:
                raise ValueError("Not a list literal")

        for caster in (to_int, to_float, to_bool, to_list):
            try:
                return try_cast(data, caster)
            except:
                pass

        return data

    def _cast_columns_inplace(self) -> None:
        if self.table.empty():
            return

        num_rows = len(self.table)
        num_cols = len(self.table[0])

        for col in range(num_cols):
            raw_col: list[str] = [self.table[row][col] for row in range(num_rows)]
            casted_col: list[Any] = ReadCSV.convert_to_common_type(raw_col)
            for row in range(num_rows):
                self.table[row][col] = casted_col[row]

def python_sort_column(csv: ReadCSV, column_number_: int | str | None) -> ReadCSV | None:
    new_csv: ReadCSV = ReadCSV()
    if column_number_ is None:
        new_csv.translate = csv.translate
        all_columns: list[list] = list()
        for row_number in range(len(csv.table)):
            for column_number in range(len(csv.table[row_number])):
                if row_number == 0:
                    all_columns.append([[] for _ in range(len(csv.table))])
                all_columns[column_number][row_number] = csv.table[row_number][column_number]
        for column_number in range(len(all_columns)):
            all_columns[column_number] = list(sorted(all_columns[column_number]))
        for row_number in range(len(csv.table)):
            new_row: NDArray[Any] = np.empty(len(csv.table[row_number]), dtype=object)
            for column_number in range(len(csv.table[row_number])):
                new_row[column_number] = all_columns[column_number][row_number]
            new_csv.table.append(new_row)
    else:
        if type(column_number_) is str:
            if column_number_ not in csv.translate:
                return None
            column_number_ = csv.translate[column_number_]
        if column_number_ >= len(csv.translate):
            return None
        name_column: str = csv.re_translate[column_number_]
        new_csv.translate[name_column] = 0
        new_csv.re_translate.append(name_column)
        column: list = list()
        for row_number in range(len(csv.table)):
            column.append(csv.table[row_number][column_number_])
        column = list(sorted(column))
        for row_number in range(len(csv.table)):
            new_row: NDArray[Any] = np.empty(1, dtype=object)
            new_row[0] = column[row_number]
            new_csv.table.append(new_row)
    return new_csv


def medianByColumn(csv: ReadCSV, column: str | int) -> float:
    our_column = python_sort_column(csv, column)
    ans = 0.0
    if len(our_column.table) % 2 != 0:
        ans = our_column.table[len(our_column.table) // 2]
    else:
        ans = (our_column.table[len(len(our_column.table) // 2) - 1] + our_column.table[
            len(len(our_column.table) // 2)]) / 2
    return ans


def getNBestByColumn(csv: ReadCSV, column: str | int, number: int) -> ReadCSV:
    return python_sort_column(csv, column).tail(number)


class GroupingAndSorting:
    def __init__(self):
        self.operations: list[Callable[[ReadCSV], ReadCSV]] = []

    def addOperation(self, operation: Callable[[ReadCSV], ReadCSV]) -> None:
        self.operations.append(operation)

    def clear(self) -> None:
        self.operations.clear()

    def execute(self, read_csv: ReadCSV) -> ReadCSV:
        for operation in self.operations:
            read_csv = operation(read_csv)
        return read_csv

NAME_EXISTS = "This name is already exists"
RANDOM_NAMES = ["Patrick Star", "SpongeBob SquarePants", "Squidward Tentacles", "Eugene H. Krabs", "Sheldon J. Plankton",
                "Karen Plankton", "Sandy Cheeks", "Mrs. Puff", "Pearl Krabs", "Gary the Snail", "Patchy the Pirate",
                "Potty the Parrot", "Mermaid Man", "Barnacle Boy", "The Flying Dutchman", "Larry the Lobster"]

class User:
    def __init__(self, new_username: str | None = None, new_csv: ReadCSV | None = None,  csv_name: str | None = None):
        if new_username is None:
            new_username = ""
        self.username = new_username
        self.all_csv: dict[str, ReadCSV] = {}
        if new_csv is None:
            return
        if csv_name is None:
            csv_name = "default_1"
        self.all_csv[csv_name] = new_csv

    def add(self, new_csv: ReadCSV | None = None,  csv_name: str | None = None) -> str | None:
        if new_csv is None:
            return None
        if csv_name is None:
            csv_name = f"default_{len(self.all_csv) + 1}"
        if csv_name in self.all_csv:
            return NAME_EXISTS
        self.all_csv[csv_name] = new_csv
        return None

    def all_csv_names(self) -> list[str] | None:
        if self.all_csv is None:
            return None
        return list(self.all_csv.keys())

documentation_path = "./documentation.txt"

PROMPT = ">>> "

GREETINGS = """Hello! What would you like to do?\n(You can try command \"documentation\")"""

USER_NAME_NOT_EXISTS = "A user with that name does not exist."

INCORRECT_PATH = "Incorrect path provided."

INCORRECT_TRANSITION = "Incorrect transition."

UNKNOWN_COMMAND = "I'm sorry, I couldn't understand the command."

INCORRECT_DIRECTORY = "Incorrect directory for creating a new user."

INVALID_PREFIX = "I'm sorry, but the username cannot begin with the characters . or /"

def write_into(output: TextIO | None = sys.stdout, user_name: str | None = "sudo", prefix: str | None = "") -> None:
    if output is None:
        output = sys.stdout
    if user_name is None:
        user_name = "sudo"
    if prefix is None:
        prefix = ""
    all_output: str = prefix
    if all_output != "":
        all_output += "\n"
    all_output += f"(./{user_name}) " + PROMPT
    output.write(all_output)
    output.flush()

def print_txt(path: str, output: TextIO = sys.stdout, encoding: str = "utf-8") -> None:
    chunk_size: int = 1 << 16
    with open(path, "r", encoding=encoding) as f:
        chunk = f.read(chunk_size)
        while chunk:
            output.write(chunk)
            chunk = f.read(chunk_size)
    output.write("\n")
    output.flush()

def normalize_path(path: str) -> str:
    norm_path: list[str] = []
    point_or_clear_elements: int = 0
    position: int = 0
    first_element: str = "/" if len(path) > 0 and path[0] == "/" else ""
    not_none_and_not_point: int = 0
    if first_element != "":
        not_none_and_not_point += 1
    for prefix in path.split("/"):
        if position == 0:
            if first_element == "":
                first_element = prefix
        if prefix == "" or prefix == ".":
            point_or_clear_elements += 1
            continue
        if prefix == "..":
            if len(norm_path) > 0 and norm_path[-1] != "..":
                norm_path.pop()
                not_none_and_not_point -= 1
            else:
                if first_element == "." or first_element == ".." or path[0] != "/":
                    norm_path.append(prefix)
                    not_none_and_not_point += 1
            continue
        not_none_and_not_point += 1
        norm_path.append(prefix)
        position += 1
    if not_none_and_not_point == 0:
        return "."
    if first_element == "/":
        return "/" + "/".join(norm_path)
    return "/".join(norm_path)


def terminal(inp: TextIO = sys.stdin, output: TextIO = sys.stdout) -> None:
    all_users: dict[str, User] = {"sudo": User()}
    user_now: str = "sudo"
    write_into(output, user_now, GREETINGS)
    all_commands: list = inp.readline().rstrip("\r\n").split() or ["" for _ in range(1)]
    exit_words: set[str] = set()
    exit_words.add("quit")
    exit_words.add("q")
    while all_commands[0].lower() not in exit_words:
        prefix = ""
        if len(all_commands) == 1:
            if all_commands[0].lower() == "ls":
                if user_now == "":
                   prefix = "\n".join(all_users.keys())
                else:
                    prefix = "\n".join(all_users[user_now].all_csv_names())
            elif all_commands[0] == "documentation":
                print_txt(documentation_path, output)
            elif all_commands[0] != "":
                prefix = "I'm sorry, I didn't understand the command."
        elif all_commands[0].lower() == "cd":
            norm_path: str = normalize_path(all_commands[1])
            flag: bool = True
            position: int = 0
            while position < len(norm_path) and norm_path[position] in {".", "/"}:
                if position >= 2 and norm_path[position - 2] == "." and norm_path[position - 1] == "." and norm_path[position] == ".":
                    flag = False
                    break
                position += 1
            if not flag:
                prefix = INCORRECT_PATH
            elif norm_path[:position] == "/":
                all_user_name: str = norm_path[position:]
                if len(all_commands) > 2:
                    all_user_name += " " + " ".join(all_commands[2:])
                if all_user_name == "":
                    user_now = ""
                elif all_user_name not in all_users:
                    prefix = USER_NAME_NOT_EXISTS
                else:
                    user_now = all_user_name
            elif len(norm_path[:position]) >= 2 and norm_path[:position] != "./":
                all_user_name: str = norm_path[position:]
                if len(all_commands) > 2:
                    all_user_name += " " + " ".join(all_commands[2:])
                if all_user_name == "":
                    user_now = ""
                elif all_user_name == "" or all_user_name not in all_users:
                    prefix = USER_NAME_NOT_EXISTS
                else:
                    user_now = all_user_name
            elif position == 0 or (norm_path[:position] == "./" and len(norm_path) > 2):
                all_user_name: str = norm_path
                if len(all_commands) > 2:
                    all_user_name += " " + " ".join(all_commands[2:])
                if user_now != "":
                    prefix = INCORRECT_TRANSITION
                elif all_user_name not in all_users:
                    prefix = USER_NAME_NOT_EXISTS
                else:
                    user_now = all_user_name
            elif norm_path != "." and norm_path != "./":
                prefix = UNKNOWN_COMMAND
        elif all_commands[0].lower() == "add":
            if all_commands[1].lower() == "user":
                all_user_name: str = " ".join(all_commands[2:])
                if user_now != "":
                    prefix = INCORRECT_DIRECTORY
                elif all_user_name in all_users:
                    prefix = NAME_EXISTS
                else:
                    if all_user_name == "":
                        all_user_name = RANDOM_NAMES[random.randint(0, len(RANDOM_NAMES) - 1)] + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
                    if all_user_name[0] == "." or all_user_name[0] == "/":
                        prefix = INVALID_PREFIX
                    else:
                        all_users[all_user_name] = User()
                        prefix = f"Add new user {all_user_name}"
            elif all_commands[1].lower() == "csv":
                pass









        write_into(output, user_now, prefix)
        all_commands = inp.readline().rstrip("\r\n").split() or ["" for _ in range(1)]


def main():
    """
    our_csv = ReadCSV("./homework_oop/repositories.csv")
    print(our_csv.getColumnNames())
    """
    with open("log.txt", "w") as log:
        log.write("")
    #wow = ReadCSV("./homework_oop/repositories.csv")
    #print(wow.getColumnByName("Forks"))
    terminal()


if __name__ == "__main__":
    main()
