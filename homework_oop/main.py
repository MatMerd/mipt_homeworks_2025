from pathlib import Path
from homework_oop import CsvRepositoryReader

def Run():
    CsvPath = Path(__file__).parent / "homework_oop" / "repositories.csv"
    Rows = CsvRepositoryReader(CsvPath).read()
    return Rows

if __name__ == "__main__":
    Run()
