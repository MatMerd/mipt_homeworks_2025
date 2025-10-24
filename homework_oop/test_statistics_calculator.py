# С Пашей соглашусь, как можно жить без хоть каких-то тестов
import csv

from homework_oop.statistics_calculator import StatisticsCalculator

if __name__ == '__main__':
    with open('repositories.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        sample_data = list(reader)

    calc = StatisticsCalculator(sample_data)

    print("Медиана по размеру:", calc.median_size())
    print("Максимальное количество звёзд:", calc.max_stars_count())
    print("Репозитории без языка:", calc.repositories_without_language())
    print("Топ-3 репозитория по звёздам:")
    for repo in calc.most_starred_repositories(3):
        print(f"  - {repo['Name']}: {repo['Stars']} звёзд")

    total_stars = calc.custom_statistics('Stars', sum)
    print("Общее количество звёзд:", total_stars)

    print("\nСводная статистика:", calc.comprehensive_stats())
