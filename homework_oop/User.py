from homework_oop.DataProcessor import DataProcessor
from typing import List, Dict

class User():
    def __init__(self, name: str):
        self.name = name
        self.saved_sorts: Dict[str, tuple] = {}
        self.saved_groups: Dict[str, str] = {}
        
    def save_sort(self, name: str, operation_params: tuple) -> None:
        self.saved_sorts[name] = operation_params
        
    def save_group(self, name: str, column: str) -> None:
        self.saved_groups[name] = column
        
    def execute_sort(self, name: str, processor: DataProcessor, clean_execution: bool = False) -> List[Dict[str, str]]:
        if name not in self.saved_sorts:
            raise KeyError(f"Сортировка '{name}' не найдена")
        column, reverse = self.saved_sorts[name]
        if clean_execution:
            return processor.reset().sort_by(column, reverse).execute()
        return processor.sort_by(column, reverse).execute()
        
    def execute_group(self, name: str, processor: DataProcessor, clean_execution: bool = False) -> Dict[str, List[Dict[str, str]]]:
        if name not in self.saved_groups:
            raise KeyError(f"Группировка '{name}' не найдена")
        column = self.saved_groups[name]
        if clean_execution:
            return processor.reset().group_by(column).execute()
        return processor.group_by(column).execute()