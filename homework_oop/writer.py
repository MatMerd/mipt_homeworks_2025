import json

from repository import Repository


class Writer:
    def write(
        self, repositories: list[Repository], file_format: str, file_name: str
    ) -> None:
        separator: str = ""
        if file_format == "txt":
            separator = " "
        elif file_format == "csv":
            separator = ","
        if file_format == "txt" or file_format == "csv":
            output_file = open(
                "saved/" + file_name + "." + file_format, "w", encoding="utf-8"
            )
            for repository in repositories:
                output_file.write(repository.to_string(separator) + "\n")
            output_file.close()
        else:
            data: list[dict[str, str]] = []
            for repository in repositories:
                map_repository: dict[str, str] = repository.to_map()
                data.append(map_repository)
            output_file = open(
                "saved/" + file_name + "." + file_format, "w", encoding="utf-8"
            )
            json.dump(data, output_file, indent=2, ensure_ascii=False)
            output_file.close()

    def write_number(
        self, statistics_name: str, number: float, file_format: str, file_name: str
    ) -> None:
        output_file = open(
            "saved/" + file_name + "." + file_format, "w", encoding="utf-8"
        )
        if file_format == "txt" or file_format == "csv":
            output_file.write(str(number) + "\n")
        else:
            output_file.write("{\n\t" + statistics_name + ": " + str(number) + "\n}")
        output_file.close()
