from user import User
from statistics_writer import StatWriter
from statistics_collector import StatCollector
from csv_reader import CSVReader

reader = CSVReader("repositories.csv")
data = reader.read_as_dict()
user = User(data)

user.update_user_settings(
    group_field="Language",
    aggregation={"Issues": lambda x: sum(x)},
)
user.apply_saved_settings()

default_result_one = user.get_default_query()
for row in default_result_one:
    print(row)

user.update_user_settings(
    sort_field="Name", sort_descending=True, group_field=None, aggregation=None
)
user.apply_saved_settings()

default_result_two = user.get_default_query()
for row in default_result_two:
    print(row)

query_id = user.create_and_save_query(
    "Популярные python репозитории",
    [
        ("where", {"condition": lambda x: x["Language"] == "Python"}),
        ("where", {"condition": lambda x: int(x["Stars"]) > 100000}),
        ("select", {"fields": ["Name", "URL", "Stars", "Issues", "Size", "Language"]}),
        ("order_by", {"field": "Size", "descending": True}),
    ],
)

result = user.execute_saved_query(query_id)
for row in result:
    print(row)


collector = StatCollector(result)
writer = StatWriter(collector.get_all_statistics())
writer.export_to_csv()
