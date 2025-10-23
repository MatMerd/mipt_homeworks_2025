import csv
import typing as tp

class CSVReader:
    def __init__(self, filepath: str, delimetr: str = ",", encoding: str = "utf_8"):
        """
        :param filepath: путь к файлу
        :param delimiter: разделитель колонок (по умолчанию ',')
        :param encoding: кодировка файла
        """
        self.filepath = filepath
        self.delimetr = delimetr
        self.encoding = encoding
    
    def read_all(self) -> tp.List[tp.Dict[str, str]]:
        """
        Читает весь csv файл, возврващает список словарей, где ключи -
        заголовки колонок
        :return: список словарей, содержащие информацию из файла
        """
        with open(self.filepath, "r", encoding=self.encoding) as f:
            reader = csv.DictReader(f)
            data = list(reader)
        
        return data
