import Query
import Reader
import User
import Stats

def main():
    reader = Reader.Reader()
    reader.read("./homework_oop/repositories.csv")
    print(reader.data[0])

    user = User.User(reader.data)
    user.save_query("sort", "Name", "Issues")
    user.save_query("select", "Name", "Issues", "Language", "Stars", "Size")
    user.save_query("group", "Name", "Stars")

    data = user.data

    statistics = Stats.Stats(data)

    print(statistics.median())
    print(statistics.most_starred())
    print(statistics.top_committed())
    print(statistics.without_language())
    statistics.save_json("./homework_oop/statistics.json")



if __name__ == "__main__":
    main()
