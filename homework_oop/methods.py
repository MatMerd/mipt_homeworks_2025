from repository import Repository


class Methods:

    def filter(self, repositories: list[Repository]) -> list[Repository]:
        pass

    def sort(self, repositories: list[Repository]) -> list[Repository]:
        pass

    def group_by(self, repositories: list[Repository]) -> list[Repository]:
        pass

'''
    Синтаксис возможных команд.
    Всего 4 типа команд, у каждой свой синтаксис, 
    если команда не соотвествует синтаксису, то она не будет выполнена:
    I) filter
    1) filter <название_поля_целочисленного_типа> <оператор_сравнения> <число>
        Пример: filter 
    filter <название_поля_строкового_типа> <оператор_сравнения> <строка>
    filter <название_поля_строкового_типа> <оператор_сравнения> <строка>
    IV) execute
    Выполняет все написанные ранее команды типов 1-3, очищает набор команд
    V) delete_last
    Удаляет последнюю команду (filter, sort, group_by). 
    Выполняется сразу.
    Невозможно отменить execute и delete_last.
    
    
    filter size <= 1024
    sort name decrease
    
    
    
    filter stars > 100
    
    group_by language
    execute 
'''