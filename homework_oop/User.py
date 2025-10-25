from DataProcessor import DataProcessor, CsvTable, ProcessingResult
from dataclasses import dataclass, field


@dataclass
class User:
    _processors: dict[str, DataProcessor] = field(default_factory=dict)

    def add_processor(self, name: str, processor: DataProcessor) -> None:
        self._processors[name] = processor.copy()

    def available_processors(self) -> set[str]:
        return set(self._processors.keys())

    def process_using(self, data: CsvTable, processor_name: str) -> ProcessingResult:
        return self._processors[processor_name].process(data)
