from homework_oop.CSVReader import CSVReader
from homework_oop.DataProcessor import DataProcessor
from homework_oop.StatisticProcessor import StatisticsProcessor


DATA_PATH = "homework_oop/repositories.csv"

def main():
    repositories = CSVReader(DATA_PATH).read()
    processor = DataProcessor(repositories)

    stats = StatisticsProcessor(processor)

    print("Медиана по размеру:", stats.median_repository_size())
    print("Самый залайканный:", stats.most_starred_repository().get('Name'))
    print("Репозиториев без языка:", len(stats.repositories_without_language()))
    processor.reset()
    print("Топ-10 по форкам:", [r['Name'] for r in stats.top_repositories_by_forks()])
    processor.reset()
    print("Средние звёзды по языкам:", stats.average_stars_by_language())
    
if __name__ == "__main__":
    main()
