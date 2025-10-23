from homework_oop.csv_reader import CSVReader
from homework_oop.data_handler import DataHandler
from homework_oop.data_statistics import DataStatistics
from homework_oop.user import User


def main():
    try:
        print("=== Тестируем Reader ===")
        reader = CSVReader('repositories.csv').get()
        print(f"Загружено записей: {len(reader.reader)}")
        print(f"Поля: {reader.fieldnames[:5]}...")

        print("\n=== Тестируем State ===")
        state = DataHandler(reader)

        result1 = state.select(['Name', 'Language', 'Stars']) \
            .filter('Language', 'Python') \
            .sort('Stars', reverse=True) \
            .execute()

        print(f"Найдено Python репозиториев: {len(result1)}")
        print("Топ-3 Python репо:")
        for i, repo in enumerate(result1[:3], 1):
            print(f"  {i}. {repo['Name']} - {repo['Stars']} звёзд")

        print("\n=== Тестируем User ===")
        user = User()
        user.save_query('top_python', state)

        result2 = user.execute_saved_query('top_python', reader)
        print(f"Сохранённый запрос вернул: {len(result2)} записей")

        print("\n=== Тестируем Statistics ===")
        stats = DataStatistics(reader.reader)

        print(f"Медианный размер: {stats.get_median()}")

        most_liked = stats.get_most_liked()
        print(f"Самый популярный: {most_liked['Name']} ({most_liked['Stars']} звёзд)")

        without_lang = stats.get_repos_without_language()
        print(f"Репозиториев без языка: {len(without_lang)}")

        top_commited = stats.get_top10_most_commited()
        print(f"Топ-10 по форкам: {[repo['Name'] for repo in top_commited]}")

        print("\n=== Тестируем сохранение ===")
        stats.save_to_csv('test_output.csv', result1[:5])
        stats.save_to_json('test_output.json', result1[:5])
        print("Файлы сохранены: test_output.csv, test_output.json")

        print("\n=== Тестируем обработку ошибок ===")
        try:
            state.filter('WrongField', 'value').execute()
        except ValueError as e:
            print(f"Ошибка поймана: {e}")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()