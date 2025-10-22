import typing

from DataProcessor import DataProcessor, CsvTable, ProcessingResult


class User:
    _processors: dict[str, DataProcessor]

    def __init__(self):
        self._processors = {}

    def add_processor(self, name: str, processor: DataProcessor) -> None:
        self._processors[name] = processor.copy()

    def available_processors(self) -> set[str]:
        return set(self._processors.keys())

    def process_using(self, data: CsvTable, processor_name: str) -> ProcessingResult:
        return self._processors[processor_name].process(data)
