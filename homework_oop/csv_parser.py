import os

from homework_oop.logger import log_operation


class CustomCSVParser:
    def __init__(self, delimiter=',', quotechar='"'):
        self.delimiter = delimiter
        self.quotechar = quotechar

    @log_operation
    def read_file(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл {filename} не найден")

        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        return [self.parse_line(line.strip()) for line in lines if line.strip()]

    @log_operation
    def parse_line(self, line):
        fields = []
        current_field = []
        in_quotes = False
        i = 0

        while i < len(line):
            char = line[i]

            if char == self.quotechar:
                if in_quotes and i + 1 < len(line) and line[i + 1] == self.quotechar:
                    current_field.append(self.quotechar)
                    i += 1
                else:
                    in_quotes = not in_quotes
            elif char == self.delimiter and not in_quotes:
                fields.append(''.join(current_field))
                current_field = []
            else:
                current_field.append(char)

            i += 1

        fields.append(''.join(current_field))
        return fields

    @log_operation
    def read_with_headers(self, filename):
        data = self.read_file(filename)
        if not data:
            return []

        headers = [header.strip() for header in data[0]]
        result = []

        for row in data[1:]:
            if len(row) == len(headers):
                result.append(dict(zip(headers, [field.strip() for field in row])))

        return result
