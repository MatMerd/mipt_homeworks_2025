from homework_oop.CSVReader import CSVReader
from homework_oop.DataProcessor import DataProcessor

DATA_PATH = "homework_oop/repositories.csv"

def main():
    repositories = CSVReader(DATA_PATH)
    repositories.read()
    
    processor = DataProcessor(repositories)
    result = (processor.select('Name', 'Language', 'Stars').sort_by('Stars', reverse=True).execute())
    
    for repo in result[:10]:
        print(f"{repo['Name']} ({repo['Language']}): {repo['Stars']}")

if __name__ == "__main__":
    main()
