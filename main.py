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
from collections.abc import Iterable
from pathlib import Path
import json
import shutil
import re

SAFE_BUILTINS: dict[str, Any] = {
    "abs": abs, "len": len, "int": int, "float": float, "str": str,
    "round": round, "min": min, "max": max, "sum": sum,
}

_TYPE_MAP: dict[str, Callable[[Any], Any]] = {
    "int": int,
    "float": float,
    "str": str,
}

class Vector:
    def __init__(self, elements: Sequence[Any] | None = None, dtype_=object):
        self.__dtype = dtype_
        self.size: int = 0
        self.capacity: int = 0
        self.data: NDArray[Any] = np.empty(0, dtype=dtype_)
        if self.__dtype is None:
            self.__dtype = object
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
        if isinstance(position, slice):
            return self.data[:self.size][position]
        if isinstance(position, tuple):
            rows, col = position
            if isinstance(rows, slice) and rows == slice(None) and isinstance(col, int):
                return np.array([self.data[i][col] for i in range(self.size)], dtype=self.__dtype)
            return self._as_matrix()[position]
        return self.data[(self.size + position) % self.size]

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
        new_data = np.empty(self.capacity, dtype=self.__dtype)
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
        self.translate: dict[str, int] = {}
        self.table: Vector = Vector()
        self.re_translate: Vector = Vector()
        if filename is None:
            return
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
        new_csv: ReadCSV = ReadCSV()
        new_csv.table = Vector(self.table[:number_of_lines].copy())
        new_csv.translate = self.translate.copy()
        new_csv.re_translate = self.re_translate.copy()
        return new_csv

    def tail(self, number_of_lines: int):
        if self.table.empty() or number_of_lines < 0:
            return None
        number_of_lines = min(number_of_lines, self.table.size)
        new_csv: ReadCSV = ReadCSV()
        new_csv.table = Vector(self.table[-number_of_lines:].copy())
        new_csv.translate = self.translate
        new_csv.re_translate = self.re_translate
        return new_csv

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


def python_sort_column(csv: ReadCSV, column_number: int | str, needed_type: int | float | str | None = None,
                       key: Callable[[Any], Any] | None = None) -> ReadCSV | None:
    new_csv: ReadCSV = ReadCSV()
    
    new_csv.translate = csv.translate.copy()
    new_csv.re_translate = csv.re_translate.copy()

    if isinstance(column_number, int): 
        needed_column_index = column_number
    else:
        needed_column_index = csv.translate[column_number]
    
    def our_key(idx: int):
        value = csv.table[idx][needed_column_index]
        if needed_type is not None:
            value = needed_type(value)
        return key(value) if key is not None else value

    indices = list(range(len(csv.table)))
    indices.sort(key=our_key)

    for idx in indices:
        cur_row = csv.table[idx].copy()
        new_csv.table.append(cur_row)
    
    return new_csv


def medianByColumn(csv: ReadCSV, column: str | int) -> float:
    our_column = python_sort_column(csv, column)
    ans = 0.0
    if isinstance(column, int):
        needed_column = column
    else:
        needed_column = csv.translate[column]

    if len(our_column.table) % 2 != 0:
        ans = our_column.table[len(our_column.table) // 2][needed_column]
    else:
        ans = (our_column.table[len(our_column.table) // 2 - 1][needed_column] + our_column.table[len(our_column.table) // 2][
            needed_column]) / 2
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
RANDOM_NAMES = ["Patrick Star", "SpongeBob SquarePants", "Squidward Tentacles", "Eugene H. Krabs",
                "Sheldon J. Plankton",
                "Karen Plankton", "Sandy Cheeks", "Mrs. Puff", "Pearl Krabs", "Gary the Snail", "Patchy the Pirate",
                "Potty the Parrot", "Mermaid Man", "Barnacle Boy", "The Flying Dutchman", "Larry the Lobster"]

class User:
    def __init__(self, new_username: str = ""):
        self.username = new_username
        self.all_csv: dict[str, ReadCSV] = {}
        self.sort_keys: dict[str, Callable[[Any], Any]] = {}
        self.key_name_to_source: dict[str, str] = {}

    def add_csv(self, csv_path: str | None = None, csv_name: str | None = None) -> str | None:
        if csv_path is None:
            return None
        if csv_name is None or csv_name == "":
            csv_name = f"default_{len(self.all_csv) + 1}"
        if csv_name in self.all_csv:
            return NAME_EXISTS
        self.all_csv[csv_name] = ReadCSV(csv_path)
        return csv_name

    def all_csv_names(self) -> list[str] | None:
        if self.all_csv is None:
            return None
        return list(self.all_csv.keys())
    
    def get_csv(self, csv_name: str | None = None) -> ReadCSV | None:
        if csv_name is None or csv_name not in self.all_csv:
            return None
        return self.all_csv[csv_name]

    def csv_file_exists(self, csv_name: str | None = None) -> bool:
        if csv_name is None or csv_name not in self.all_csv:
            return False
        return True
    
    def del_csv(self, csv_name: str | None = None) -> None:
        if csv_name is None or csv_name not in self.all_csv:
            return
        del self.all_csv[csv_name]

    @staticmethod
    def compileNamedKey(name: str, expression: str) -> Callable[[Any], Any]:
        if not re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$").match(name):
            raise ValueError("Invalid name of the key >:(")
        src = f"def {name}(x):\n    return {expression}\n"
        local_names: dict[str, Any] = {}
        exec(src, {"__builtins__": SAFE_BUILTINS}, local_names)
        return local_names[name]

class Root:
    def __init__(self, all_names: Iterable[str] | None = None) -> None:
        self.names: dict[str, User] = {}
        if all_names is None:
            return
        for name in all_names:
            self.names[name] = User(name)

    def add_user(self, new_user: str | None = None) -> str:
        if new_user is None or new_user == "":
            new_user = RANDOM_NAMES[random.randint(0, len(RANDOM_NAMES) - 1)] + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.names[new_user] = User(new_user)
        return new_user

    def all_user_names(self) -> list[str]:
        return list(self.names.keys())

    def get_user(self, name: str) -> User:
        return self.names[name]

    def name_exists(self, name: str) -> bool:
        return name in self.names
    
    def clear(self) -> None:
        self.names.clear()

documentation_path = "./documentation.txt"

PROMPT = ">>> "

GREETINGS = """Hello! What would you like to do?\n(You can try command \"documentation\")"""

USER_NAME_NOT_EXISTS = "A user with that name does not exist."

INCORRECT_PATH = "Incorrect path provided."

INCORRECT_TRANSITION = "Incorrect transition."

UNKNOWN_COMMAND = "I'm sorry, I couldn't understand the command."

INCORRECT_DIRECTORY = "Incorrect directory for creating a new user."

INVALID_PREFIX = "I'm sorry, but the username cannot begin with the characters . or /"

CSV_IN_ROOT = "I'm sorry, but add csv cannot be used in the root directory"

ROOT_PATH = "./root"

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

def save_as_csv(read_csv: ReadCSV, path: str, delimiter: str = ",", write_header: bool = True) -> None:
    real_path: Path = Path(path)
    real_path.parent.mkdir(parents=True, exist_ok=True)
    with open(real_path, "w", encoding="utf-8") as f:
        out = csv.writer(f, delimiter=delimiter)
        if write_header and not read_csv.re_translate.empty():
            out.writerow(list(read_csv.re_translate.array()))
        out.writerows(read_csv.table.array())

def _pyify(x):
    if isinstance(x, np.generic):
        return x.item()
    if isinstance(x, np.ndarray):
        return x.tolist()
    return x

def save_as_json(read_csv: ReadCSV, path: str, orient: str = "records", ensure_ascii: bool = False, indent: int | None = 2) -> None:
    real_path: Path = Path(path)
    real_path.parent.mkdir(parents=True, exist_ok=True)
    rows = read_csv.table.array()
    header = list(read_csv.re_translate.array()) if not read_csv.re_translate.empty() else []
    amount_of_columns: int = len(rows[0]) if len(rows) else 0
    if not header:
        header = [str(i) for i in range(amount_of_columns)]
    if orient == "records":
        payload = [{header[i]: _pyify(row[i]) for i in range(min(amount_of_columns, len(row)))} for row in rows]
        with open(real_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=ensure_ascii, indent=indent)
    elif orient == "split":
        payload = { "columns": header, "data": [[_pyify(v) for v in row] for row in rows] }
        with open(real_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=ensure_ascii, indent=indent)
    elif orient == "jsonl":
        with open(real_path, "w", encoding="utf-8") as f:
            for row in rows:
                rec = {header[i]: _pyify(row[i]) for i in range(min(amount_of_columns, len(row)))}
                f.write(json.dumps(rec, ensure_ascii=ensure_ascii) + "\n")


def get_all_names(position: int, all_commands: list[str], all_csv_names: list[str], current_user: User) -> tuple[str, int]:
    last_csv_name: str = ""
    flag: bool = False
    while position < len(all_commands) and all_commands[position][:9] != "--format=":
        if all_commands[position][:8] == "--names=":
            if last_csv_name != "" or flag:
                return (UNKNOWN_COMMAND, position)
            last_csv_name += all_commands[position][8:]
            flag = True
        else:
            last_csv_name += all_commands[position]
        if len(last_csv_name) > 0 and last_csv_name[-1] == ",":
            add_csv_name: str = last_csv_name[:-1]
            if not current_user.csv_file_exists(add_csv_name):
                return (f"Name {add_csv_name} doesn't exist", position)
            all_csv_names.append(add_csv_name)
            last_csv_name = ""
        position += 1
    if last_csv_name != "" and last_csv_name != ".":
        if not flag:
            return (UNKNOWN_COMMAND, position)
        if not current_user.csv_file_exists(last_csv_name):
            return (f"Name {last_csv_name} doesn't exist", position)
        all_csv_names.append(last_csv_name)
    if last_csv_name == "" or last_csv_name == ".":
        for user_name in current_user.all_csv_names():
            all_csv_names.append(user_name)
    return ("", position)

def get_format(position: int, all_commands: list[str]) -> str:
    current_format: str = ".csv"
    if position < len(all_commands) and all_commands[position][:9] == "--format=":
        current_format = all_commands[position][9:]
        if current_format == "" or current_format == ".":
            return ".csv"
        if len(current_format) > 0 and current_format[0] != ".":
            current_format = "." + current_format
        if current_format != ".csv" and current_format != ".json":
            return f"I\'m sorry, but I cannot work with the {current_format} format"
    return current_format

def save_current_user(root: Root, user_name: str, all_commands: list[str]) -> str:
    current_user: User = root.get_user(user_name)
    all_user_path: str = ROOT_PATH + "/" + user_name
    all_csv_names: list[str] = []
    position: int = 1
    err, position = get_all_names(position, all_commands, all_csv_names, current_user)
    if err != "":
        return err
    current_format: str = get_format(position, all_commands)
    if current_format != ".csv" and current_format != ".json":
        return current_format
    for csv_name in all_csv_names:
        all_csv_path: str = all_user_path + "/" + csv_name + current_format
        if current_format == ".csv":
            save_as_csv(current_user.get_csv(csv_name), all_csv_path)
        else:
            save_as_json(current_user.get_csv(csv_name), all_csv_path)
    return ""

def delete_current_user(root: Root, user_name: str, all_commands: list[str], real_del: bool = False) -> str:
    current_user: User = root.get_user(user_name)
    all_user_path: str = ROOT_PATH + "/" + user_name
    all_csv_names: list[str] = []
    position: int = 1
    err, position = get_all_names(position, all_commands, all_csv_names, current_user)
    if err != "":
        return err
    current_format: str = get_format(position, all_commands)
    if current_format != ".csv" and current_format != ".json":
        return current_format
    if not real_del:
        for csv_name in all_csv_names:
            current_user.del_csv(csv_name)
    else:
        for csv_name in all_csv_names:
            csv_path = all_user_path + "/" + csv_name + current_format
            Path(csv_path).unlink(missing_ok=True)
    return ""


def parse_sort_args(argline: str) -> dict[str, Any]:
    """
    Поддерживаем:
      --column <name|index>   (обязательно)
      --using  <key_name>     (опционально)
      --type   <int|float|str>  (опционально)
      --out    <new_csv_name> (обязательно)
    Возвращает словарь параметров для python_sort_column
    """
    tokens = argline.split()
    i = 0
    result: dict[str, Any] = {}

    def need_value(flag: str):
        nonlocal i
        if i + 1 >= len(tokens):
            raise ValueError(f"Flag {flag} requires a value")
        v = tokens[i + 1]
        i += 2
        return v

    while i < len(tokens):
        t = tokens[i]
        if t == "--column":
            v = need_value("--column")
            try:
                result["column_number"] = int(v)
            except ValueError:
                result["column_number"] = v
        elif t == "--using":
            result["--using"] = need_value("--using")
        elif t == "--type":
            v = need_value("--type").lower()
            if v not in _TYPE_MAP:
                raise ValueError(f"Unknown type: {v}")
            result["needed_type"] = _TYPE_MAP[v]
        elif t == "--out":
            result["--out"] = need_value("--out")
        else:
            raise ValueError(f"Unknown argument: {t}")

    if "column_number" not in result:
        raise ValueError("Missing required --column")
    if "--out" not in result or not result["--out"]:
        raise ValueError("Missing required --out <new_csv_name>")
    if "needed_type" not in result:
        result["needed_type"] = None
    return result

def terminal(inp: TextIO = sys.stdin, output: TextIO = sys.stdout) -> None:
    root: Root = Root()
    user_now: str = "sudo"
    root.add_user(user_now)
    write_into(output, user_now, GREETINGS)
    all_commands: list = inp.readline().rstrip("\r\n").split() or ["" for _ in range(1)]
    exit_words: set[str] = set()
    exit_words.add("quit")
    exit_words.add("q")
    while all_commands[0].lower() not in exit_words:
        prefix = ""
        if all_commands[0].lower() == "save":
            if user_now != "":
                prefix = save_current_user(root, user_now, all_commands)
                if prefix == "":
                    prefix = "Successful preservation"
            elif len(all_commands) > 1 and all_commands[1] == "all":
                new_all_commands: list[str] = ["save", "--format=.csv"]
                current_format: str = ".csv"
                if len(all_commands) > 2 and all_commands[2][:9] == "--format=":
                    current_format = all_commands[2][9:]
                    if len(current_format) > 0 and current_format[0] != ".":
                        current_format = "." + current_format
                    if current_format == "" or current_format == ".":
                        current_format = ".csv"
                    if current_format != ".csv" and current_format != ".json":
                        prefix = f"I\'m sorry, but I cannot work with the {current_format} format"
                if prefix == "":
                    new_all_commands[1] = "--format=" + current_format
                    for user_name in root.all_user_names():
                        prefix = save_current_user(root, user_name, new_all_commands)
                    if prefix == "":
                        prefix = "Successful preservation"
            else:
                prefix = UNKNOWN_COMMAND
        elif all_commands[0].lower() == "delete":
            if user_now != "":
                prefix = delete_current_user(root, user_now, all_commands)
                if prefix == "":
                    prefix = "Successful deletion"
            elif len(all_commands) > 1 and all_commands[1].lower() == "all":
                new_all_commands: list[str] = ["delete"]
                for user_name in root.all_user_names():
                    prefix = delete_current_user(root, user_name, new_all_commands)
                root.clear()
                prefix = "Successful deletion"
            else:
                prefix = UNKNOWN_COMMAND
        elif all_commands[0].lower() == "rdelete":
            if user_now != "":
                prefix = delete_current_user(root, user_now, all_commands, True)
                if prefix == "":
                    prefix = "Successful rdeletion"
            elif len(all_commands) > 1 and all_commands[1].lower() == "all":
                root_path: Path = Path(ROOT_PATH)
                if root_path.exists():
                    shutil.rmtree(str(root_path))
                prefix = "Successful rdeletion"
            else:
                prefix = UNKNOWN_COMMAND
        elif len(all_commands) == 1:
            if all_commands[0].lower() == "ls":
                if user_now == "":
                    prefix = "\n".join(root.all_user_names())
                else:
                    prefix = "\n".join(root.get_user(user_now).all_csv_names())
            elif all_commands[0] == "documentation":
                print_txt(documentation_path, output)
            elif all_commands[0] != "":
                prefix = UNKNOWN_COMMAND
        elif all_commands[0].lower() == "cd":
            norm_path: str = normalize_path(all_commands[1])
            flag: bool = True
            position: int = 0
            while position < len(norm_path) and norm_path[position] in {".", "/"}:
                if position >= 2 and norm_path[position - 2] == "." and norm_path[position - 1] == "." and norm_path[
                    position] == ".":
                    flag = False
                    break
                position += 1
            all_user_name: str = norm_path[position:]
            if all_user_name == "":
                all_user_name += " ".join(all_commands[2:])
            elif len(all_commands) > 2:
                all_user_name += " " + " ".join(all_commands[2:])
            if not flag:
                prefix = INCORRECT_PATH
            elif norm_path[:position] == "/":
                if all_user_name == "":
                    user_now = ""
                elif not root.name_exists(all_user_name):
                    prefix = USER_NAME_NOT_EXISTS
                else:
                    user_now = all_user_name
            elif len(norm_path[:position]) >= 2 and norm_path[:position] != "./":
                if all_user_name == "":
                    user_now = ""
                elif not root.name_exists(all_user_name):
                    prefix = USER_NAME_NOT_EXISTS
                else:
                    user_now = all_user_name
            elif position == 0 or (len(norm_path) > 2 and norm_path[:position] == "./"):
                if user_now != "":
                    prefix = INCORRECT_TRANSITION
                elif not root.name_exists(all_user_name):
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
                elif root.name_exists(all_user_name):
                    prefix = NAME_EXISTS
                else:
                    if len(all_user_name) >= 1 and (all_user_name[0] == "." or all_user_name[0] == "/"):
                        prefix = INVALID_PREFIX
                    else:
                        all_user_name = root.add_user(all_user_name)
                        prefix = f"Add new user {all_user_name}"
            elif all_commands[1].lower() == "csv":
                position: int = 2
                all_path: str = ""
                all_csv_name: str = ""
                while position < len(all_commands) and all_commands[position][:7] != "--name=":
                    all_path += all_commands[position]
                    position += 1
                if position < len(all_commands):
                    all_csv_name = all_commands[position][7:]
                    if all_csv_name == "":
                        all_csv_name += " ".join(all_commands[position + 1:])
                    elif position + 1 < len(all_commands):
                        all_csv_name += " " + " ".join(all_commands[position + 1:])
                norm_path: str = normalize_path(all_path)
                if all_path == "":
                    norm_path = "./homework_oop/repositories.csv"
                path = Path(norm_path).expanduser()
                if not path.is_file():
                    prefix = INCORRECT_PATH
                elif user_now == "":
                    prefix = CSV_IN_ROOT
                else:
                    all_csv_name = root.get_user(user_now).add_csv(norm_path, all_csv_name)
                    if all_csv_name == NAME_EXISTS:
                        prefix = NAME_EXISTS
                    else:
                        prefix = f"Add new csv file {all_csv_name} to the user {user_now}"
        elif all_commands[0].lower() == "key":
            sub = all_commands[1] if len(all_commands) > 1 else ""
            if user_now:
                current_user = root.get_user(user_now)
                if sub == "create":
                    if len(all_commands) != 3:
                        prefix = "Usage: key create <key_name>"
                    else:
                        try:
                            key_name = all_commands[2]
                            output.write(f"def {key_name}(x):\n    return ")
                            output.flush()
                            expression = inp.readline().rstrip("\r\n")
                            new_key_function = User.compileNamedKey(key_name, expression)
                            src = f"def {key_name}(x):\n    return {expression}"
                            current_user.sort_keys[key_name] = new_key_function
                            current_user.key_name_to_source[key_name] = src
                        except Exception as exception:
                            prefix = f"Key compile error: {exception}"
                elif sub == "list":
                    if len(all_commands) != 2:
                        prefix = "Usage: key list"
                    else:
                        to_output = []
                        for name in sorted(current_user.sort_keys):
                            to_output.append(current_user.key_name_to_source[name])
                        prefix = "\n".join(to_output)
            else:
                prefix = "Incorrect directory for such a command!"
        elif all_commands[0].lower() == "sort":
            rest = " ".join(all_commands)[len("sort"):].strip()
            if "|" not in rest:
                prefix = "Usage: sort <csv_name> | --column <name|index> [--using <key>] [--type <int|float|str>] --out <new_csv_name>"
            else:
                left, right = rest.split("|", 1)
                csv_name = left.strip()
                args_str = right.strip()

                if user_now == "":
                    prefix = CSV_IN_ROOT
                elif not csv_name:
                    prefix = "CSV name is empty."
                elif csv_name not in root.get_user(user_now).all_csv:
                    prefix = f"CSV '{csv_name}' not found."
                else:
                    try:
                        params = parse_sort_args(args_str)
                        current_user = root.get_user(user_now)
                        
                        new_name = params["--out"]
                        if new_name in current_user.all_csv:
                            raise ValueError(f"CSV '{new_name}' already exists")

                        kwargs = {
                            "column_number": params["column_number"],
                            "needed_type": params.get("needed_type"),
                            "key": None
                        }
                        
                        if "--using" in params:
                            key_name = params["--using"]
                            key_func = current_user.sort_keys.get(key_name)
                            if key_func is None:
                                raise ValueError(f"No such key: {key_name}")
                            kwargs["key"] = key_func

                        res = python_sort_column(current_user.all_csv[csv_name], **kwargs)
                        if res is None:
                            prefix = "Sort failed."
                        else:
                            current_user.all_csv[new_name] = res
                            prefix = f"Created CSV '{new_name}'"
                    except Exception as e:
                        prefix = f"Sort error: {e}"

        else:
            prefix = UNKNOWN_COMMAND
        write_into(output, user_now, prefix)
        all_commands = inp.readline().rstrip("\r\n").split() or ["" for _ in range(1)]


def main():
    terminal()

if __name__ == "__main__":
    main()

