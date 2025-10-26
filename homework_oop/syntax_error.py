class SyntaxError:
    def raise_command_not_found_exception(self) -> None:
        print("SyntaxError: ", end="")
        print("Введена несуществующая команда.")

    def raise_empty_field_exception(self, command: str) -> None:
        print("SyntaxError: ", end="")
        print("Для команды " + command + " не введено поле")

    def raise_uncorrect_condition_exception(self, command: str) -> None:
        print("SyntaxError: ", end="")
        print("Для команды " + command + " введено неверное условие")

    def raise_more_than_one_group_by_exception(self) -> None:
        print("SyntaxError: ", end="")
        print("Нельзя вводить больше одной команды group_by")

    def raise_cannot_use_save_query(self) -> None:
        print("SyntaxError: ", end="")
        print(
            "Невозможно использовать save_query, так как нет новых запросов вида filter, sort или group_by"
        )

    def raise_query_not_found_exception(self) -> None:
        print("SyntaxError: ", end="")
        print("Невозможно использовать call, потому что запроса с таким именем нет")
