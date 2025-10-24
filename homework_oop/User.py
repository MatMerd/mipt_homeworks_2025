from homework_oop.DataProcessor import DataProcessor


class User:
    def __init__(self):
        self.saved_queries = {}

    def validate_processor(self, processor):
        if not hasattr(processor, 'operations'):
            raise TypeError("Переданный объект должен иметь атрибут 'operations'")

    def save_query(self, name, processor):
        self.validate_processor(processor)

        self.saved_queries[name] = processor.operations.copy()

    def execute_query(self, name, data, headers):
        if name not in self.saved_queries:
            raise ValueError(f"Запрос '{name}' не найден")
        processor = DataProcessor(data, headers)
        processor.operations = self.saved_queries[name]
        return processor.execute()
