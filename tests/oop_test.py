import os
from typing import List
from homework_oop.repository import Repository
from homework_oop.reader import CSVRepositoryReader
from homework_oop.stats import Statistics
from homework_oop.user import User
from homework_oop.utils import DATA_PATH, save_to_csv, save_to_json

def stats_test(repositories: List[Repository]):
    print("="*10, " stats test ", "="*10)

    stats = Statistics(repositories)

    print(f"максимальная медиана размера репозиториев: {stats.median_size()}")
    print(f"максимальное количество звезд: {stats.max_stars()}")
    print(f"количество репозиториев без языка: {stats.repos_without_language()}")
    print(f"топ 10 репозиториев по количеству форков: {stats.top_10_forks()}")
    print(f"топ 10 языков по количеству звезд: {stats.top_10_popular_languages()}")
    os.makedirs("tests/temp_obj", exist_ok=True)
    save_to_csv("tests/temp_obj/stats.csv", stats.top_10_popular_languages())
    save_to_json("tests/temp_obj/stats.json", stats.top_10_popular_languages())

def user_test(repositories: List[Repository]):
    print("="*10, " user test ", "="*10)

    user = User("user")
    user.create_query("top_languages", select=["Language"], group_by=["Language"])
    print(f"результат запроса: {[result[0] for result in user.execute_saved_query("top_languages", repositories).keys()]}")
    print(user.get_query_details("top_languages"))

if __name__ == "__main__":
    reader = CSVRepositoryReader(DATA_PATH)
    reader.read()
    repositories = reader.get_data()

    stats_test(repositories)

    user_test(repositories)