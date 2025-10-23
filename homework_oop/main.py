import csv_reader
import data_handler
import data_statistics
import data_exporter
import user

def main() -> None:
    reader = csv_reader.CSVReader("repositories.csv")
    handler = data_handler.DataHandler(reader.read_all())
    user1 = user.User("Bob")

    (
    handler
        .group_by(column="Language", agg={"Stars": "sum", "Forks": "max"})
        .filter(condition=lambda r: int(r["Stars_sum"]) > 100_000)
        .sort(column="Forks_max", reverse=True)
        .select(columns=["Language", "Stars_sum"])
    )

    user1.save_query("query1", handler.operations)

    data_exporter.DataExporter.export_to_json(user1.run_query("query1", handler)[:5], filename="temp")
    print(len(data_statistics.DataStatistics.repos_without_language(reader.read_all())))
    

if __name__ == "__main__":
    main()
