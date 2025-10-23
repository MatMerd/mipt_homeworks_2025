import typing as tp
from collections import defaultdict
import difflib

DataRow: tp.TypeAlias = tp.Dict[str, str]
DataRowList: tp.TypeAlias = tp.List[tp.Dict[str, str]]

class DataHandler:
    def __init__(self, data: DataRowList):
        """
        :param data: список словарей, содержащие информацию из файла
        """
        self.data = data
        self.temp_data = data
        self.operations: tp.List[tp.Tuple[str, tp.Any]] = []
    
    def filter(self, *, condition: tp.Callable[[DataRow], bool]) -> "DataHandler":
        """
        Добавление фильтра данных в список операций
        :param condition: функция, принимающая строку данных и возвращающая True, если строку нужно оставить
        :return: self для цепочки вызовов
        """
        self.operations.append(("filter", condition))
        return self

    def sort(self, *, column: str, reverse: bool = False) -> "DataHandler":
        """
        Добавление сортировки в список операций
        :param column: название колонки для сортировки
        :param reverse: если True, сортировка будет по убыванию
        :return: self для цепочки вызовов
        """
        self.operations.append(("sort", (column, reverse)))
        return self

    def group_by(self, *, column: str, agg: tp.Optional[tp.Dict[str, str]] = None) -> "DataHandler":
        """
        Добавление операции группировки по указанной колонке с возможной агрегацией
        :param column: название колонки для сортировки, по которой будет проводиться группировка
        :param agg: словарь вида {название_колонки: агрегатная_функция}, где функция одна из ['sum', 'mean', 'max', 'min', 'count']
        :return: self для цепочки вызовов
        """
        self.operations.append(("group", (column, agg)))
        return self
    
    def select(self, columns: tp.List[str]) -> "DataHandler":
        """
        Добавление операции выбора определенных колонок.
        :param columns: cписок колонок, которые нужно оставить
        :return: self для цепочки вызовов
        """
        self.operations.append(("select", columns))
        return self
    
    def execute(self) -> DataRowList:
        """
        Выполнение всех накопленных операции (filter, sort, group, select) над данными.
        :return: список словарей с результатом обработки
        """
        pointer = 0

        while pointer < len(self.operations):
            operation, param = self.operations[pointer]

            if operation == "filter":
                filters = []
                while pointer < len(self.operations) and self.operations[pointer][0] == "filter":
                    filters.append(self.operations[pointer][1])
                    pointer += 1
                self.temp_data = [row for row in self.temp_data if all(f(row) for f in filters)]
            
            if operation == "sort":
                column, reverse = param
                self._check_column(column)
                self.temp_data = sorted(self.temp_data, key=lambda r: int(r[column]), reverse=reverse)
                pointer += 1
            
            if operation == "group":
                column, agg = param
                self._check_column(column)

                grouped = defaultdict(list)
                for row in self.temp_data:
                    grouped[row[column]].append(row)
                
                new_data = []
                for group_value, rows in grouped.items():
                    base_row: tp.Dict[str, tp.Any] = {column: group_value}
                    if agg:
                        for field, func_name in agg.items():
                            self._check_column(field)
                            
                            values = [r[field] for r in rows if r[field] is not None]

                            if func_name == "sum":
                                base_row[field + "_sum"] = sum([int(v) for v in values])
                            elif func_name == "mean":
                                base_row[field + "_mean"] = sum([int(v) for v in values]) / len(values)
                            elif func_name == "max":
                                base_row[field + "_max"] = max(values)
                            elif func_name == "min":
                                base_row[field + "_min"] = min(values)
                            elif func_name == "count":
                                base_row[field + "_count"] = len(values)
                            else:
                                raise ValueError(f"Неизвестная агрегатная функция: {func_name}")
                        
                    new_data.append(base_row)
                pointer += 1
                self.temp_data = new_data
            
            if operation == "select":
                columns = set(param)
                pointer += 1

                while pointer < len(self.operations) and self.operations[pointer][0] == "select":
                    next_columns = set(self.operations[pointer][1])
                    if not next_columns.issubset(columns):
                        raise ValueError(f"Columns '{next_columns - columns}' does not exist.")
                    columns &= next_columns
                    pointer += 1
                self.temp_data = [{k : v for k, v in row.items() if k in columns} for row in self.temp_data]
    
        self.operations = []
        return_data = self.temp_data
        self.temp_data = self.data
        return return_data
    
    def _check_column(self, column: str) -> None:
        """
        Проверка существования указанной колонки в данных.
        :param column: название колонки
        :raises ValueError: если колонка не найдена, с подсказкой близких по имени колонок
        """
        available_columns = self.temp_data[0].keys()
        if column not in available_columns:
            close_matches = difflib.get_close_matches(column, available_columns)
            raise ValueError(
                f"Column '{column}' does not exist. Did you mean one of the following columns: {close_matches} ?"             
            )
