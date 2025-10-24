from entity.group_type import GroupType
from entity.reader import Reader
from entity.request import Request
from entity.sort_type import SortType
from entity.sorting import Sorting
from entity.where_type import WhereType

# Демо работы написанных entity
# --------------------------------------------------------------------
# Получаем распарсенные репозитории в лист.
repositories = Reader.read_file()
print([repository.name for repository in repositories[:10]])
# Создаем экземпляр запроса с несколькими полями для сортировки и полем для группировки
request = Request([SortType.NAME, SortType.NAME, SortType.SIZE], {GroupType.HAS_PROJECTS},
                  {WhereType.NAME: "awesome", WhereType.LICENSE: "CC0-1.0"})

count = 0
for key in Sorting.execute_request(request, repositories):
    print(f"The {count}th repositories bag!")
    for repository in key:
        print(repository)
    count += 1
    print()
