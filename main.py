from homework_oop.csv_writer.writer import DataExporter
from homework_oop.data_processor.data_processor import DataProcessor
from homework_oop.stat_analyzer.stat_analyzer import StatisticsCalculator
from homework_oop.user.user import User
from homework_oop.csv_reader.reader import CSVReader
from pathlib import Path

def main():
    print("\n[Чтение данных]")
    reader = CSVReader(Path(__file__).parent / 'homework_oop/repositories_short.csv')
    reader.read()
    repo_data = reader.get_data()
    print(f"Успешно прочитано {len(repo_data)} записей.")

    print("\n[Обработка данных]")
    processor = DataProcessor(repo_data)
    top_python_repos = processor.select('Name', 'Stars') \
        .sort_by('Stars', reverse=True) \
        .execute()

    print("Топ-3 Python репозитория по звездам:")
    for repo in top_python_repos[:3]:
        print(f"  - {repo['Name']}: {repo['Stars']} звезд")

    print("\n[Работа с пользователем]")
    app_user = User("Alex")

    grouping_query = DataProcessor(repo_data).group_by('Language')
    app_user.save_query("group_by_language", grouping_query)

    print("\nВыполнение сохраненного запроса 'group_by_language'...")
    grouped_result = app_user.execute_saved_query("group_by_language")
    for lang, repos in grouped_result.items():
        print(f"  - Язык: {lang or 'Undefined'}, репозиториев: {len(repos)}")

    print("\n[Расчет статистики]")
    stats_calculator = StatisticsCalculator(repo_data)
    all_stats = stats_calculator.calculate_all()
    print("Статистика успешно рассчитана. Медианный размер репозитория:", all_stats['median_repo_size'])

    print("\n[Экспорт результатов]")
    exporter = DataExporter(all_stats)
    exporter.export('repo_statistics', export_format='json')
    exporter.export('repo_statistics', export_format='csv')


if __name__ == "__main__":
    main()
