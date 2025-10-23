from entity.group_type import GroupType
from entity.file_manager import FileManager
from entity.request import Request
from entity.sort_type import SortType


# Демо работы написанных entity
# --------------------------------------------------------------------
# Получаем распарсенные репозитории в лист.
repositories = FileManager.read_file()
print([repository.name for repository in repositories[:10]])

# Создаем экземпляр запроса с несколькими полями для сортировки и полем для группировки
request = Request([SortType.NAME, SortType.SIZE], {GroupType.LICENSE})

# Записываем статистику в csv
statistics = {"the biggest stars number": "12222", "size median": "3200", "number of repositories without language": "1000", "top-10 repositories by commit number": "repository.toString()"}
FileManager.write_statistic(statistics)
