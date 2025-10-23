class CSVReader:

    def read(self, file_name: str) -> list[list[str]]:
        result = []
        with open(file_name, "r", encoding='utf-8') as f:
            f.readline()
            for line in f.readlines():
                result.append(line.strip().split(','))
        return result
