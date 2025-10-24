from entity.group_type import GroupType
from file_manager import FileManager
from entity.sort_type import SortType
from sorting import Sorting
from entity.where_type import WhereType
from user import User

# Демо работы
# --------------------------------------------------------------------
# Получаем распарсенные репозитории в лист.
repositories = FileManager.read_file()
print([repository.name for repository in repositories[:10]])

# Демонстрация работы User'а
user = User('Artem')
# Создаем экземпляр запроса с несколькими полями для сортировки и полем для группировки
request = user.create_request([SortType.NAME, SortType.NAME, SortType.SIZE], {GroupType.HAS_PROJECTS},
                              {WhereType.NAME: "awesome", WhereType.LICENSE: "CC0-1.0"})

# Сортируем репозитории по запросу
count = 0
for key in Sorting.execute_request(request, repositories):
    print(f"The {count}th repositories bag!")
    for repository in key:
        print(repository)
    count += 1
    print()

# Получаем статистику
stats = user.process_request(request, repositories)
print(stats)
# Получаем историю запросов
history = user.get_request_history()
print(history)
# Получаем конкретный запрос из истории
print(user.get_request(0))

# Пишем статистику в файл
FileManager.write_statistic(stats)
