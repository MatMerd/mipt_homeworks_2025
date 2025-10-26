from homework_oop.reader import RepositoryReader
from homework_oop.query_executor import QueryExecutor
from homework_oop.user import User
from homework_oop.statistics import RepositoryStatistics
from homework_oop.exporter import StatisticsExporter


def main():
    try:
        print("Запуск анализа репозиториев")

        reader = RepositoryReader('repositories.csv')
        repositories = reader.read()

        print(f"Загружено {len(repositories)} репозиториев")

        if not repositories:
            print("Не удалось загрузить репозитории. Проверьте формат CSV файла.")
            return

        executor = QueryExecutor(repositories)

        result = (executor
                  .filter(lambda repo: repo.stars > 1000)
                  .sort('stars', reverse=True)
                  .execute())

        print(f"Найдено {len(result)} популярных репозиториев")

        stats = RepositoryStatistics(repositories)

        print(f"\nСтатистика:")
        print(f"  Медианный размер: {stats.median_size}")
        print(f"  Самый популярный: {stats.most_starred.name if stats.most_starred else 'N/A'}")
        print(f"  Репозиториев без языка: {len(stats.repos_without_language)}")
        print(f"  Общее количество звезд: {stats.total_stars}")
        print(f"  Средние звезды: {stats.avg_stars:.2f}")

        exporter = StatisticsExporter()
        exporter.to_json(stats.language_distribution, 'language_distribution.json')

        top_repos = stats.top_repos_by_stars(3)
        exporter.to_csv(top_repos, 'top_repositories.csv')

        print("\nРабота с пользовательскими запросами...")
        user = User("test_user")

        favorite_query = (QueryExecutor(repositories)
                          .filter(lambda repo: repo.stars > 5000)
                          .sort('updated_at', reverse=True))

        user.save_query("popular_recent", favorite_query)

        saved_result = user.execute_saved_query("popular_recent", repositories)
        print(f"Результат сохраненного запроса: {len(saved_result)} репозиториев")

        print("\nАнализ завершен")
        print("Созданные файлы: language_distribution.json, top_repositories.csv")

    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
