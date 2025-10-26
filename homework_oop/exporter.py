import json

from homework_oop.logger import log_operation


class StatisticsExporter:
    @staticmethod
    @log_operation
    def to_csv(data, filename):
        if not data:
            return

        fieldnames = ['name', 'description', 'url', 'size', 'stars', 'forks', 'issues', 'language', 'license']

        with open(filename, 'w', encoding='utf-8') as file:
            header = ','.join(fieldnames) + '\n'
            file.write(header)

            for repo in data:
                row = []
                for field in fieldnames:
                    value = getattr(repo, field, '')
                    if value is None:
                        value = ''
                    row.append(str(value))
                line = ','.join(row) + '\n'
                file.write(line)

    @staticmethod
    @log_operation
    def to_json(data, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False, default=str)
