from homework_oop.CSVReader import CSVReader
from homework_oop.DataProcessor import DataProcessor
from homework_oop.User import User

DATA_PATH = "homework_oop/repositories.csv"

def main():
    repositories = CSVReader(DATA_PATH).read()
    processor = DataProcessor(repositories)
    
    user = User("Nick")
    
    user.save_sort("Top by stars", ('Stars', True))
    user.save_group("Group by Language", 'Language')

    top_sorted = user.execute_sort("Top by stars", processor)
    print("Top by stars")
    for repo in top_sorted[:3]:
        print(f"{repo['Name']} — {repo['Stars']}")
        
    grouped = user.execute_group("Group by Language", processor, clean_execution=True)
    print("\nGroup by Language")
    for lang, repos in grouped.items():
        print(f"{lang}: {len(repos)}")

if __name__ == "__main__":
    main()
