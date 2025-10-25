from homework_oop.CSVReader import CSVReader 

DATA_PATH = "homework_oop/repositories.csv"

def main():
    repositories = CSVReader(DATA_PATH)
    repositories.read()
    print(repositories.get_column_names())

if __name__ == "__main__":
    main()
