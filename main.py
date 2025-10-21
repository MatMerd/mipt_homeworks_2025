from entity.group_type import GroupType
from entity.reader import Reader
from entity.request import Request
from entity.sort_type import SortType


# Демо работы написанных entity
# --------------------------------------------------------------------
# Получаем распарсенные репозитории в лист.
repositories = Reader.read_file()
print([repository.name for repository in repositories[:10]])

# Создаем экземпляр запроса с несколькими полями для сортировки и полем для группировки
request = Request({SortType.NAME, SortType.SIZE}, {GroupType.LICENSE})
