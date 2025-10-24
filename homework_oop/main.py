from dataclasses import asdict
from datacls import OperationType, Operation, Query
from user import User
from csv_reader import RepositoryCSVReader
from data_processor import DataProcessor
from executor import Executor
from csv_writer import stats_to_csv

def main():
    reader = RepositoryCSVReader('repositories.csv')
    data = reader.read_all()

    processor = DataProcessor(data)
        
    user = User("Gassy")
    
    operations = [
        Operation(OperationType.SELECT, ["Name", "Stars"]),
        Operation(OperationType.SORT, ["Stars", True])
    ]
    
    user.add_query(Query(operations=operations, result=None))
    
    operations = [
        Operation(OperationType.SORT, ["Name", True]),
        Operation(OperationType.SELECT, ["Name", "Stars", "Size", "Language"]),
        Operation(OperationType.SORT, ["Stars", "Size", True])
    ]
    
    user.add_query(Query(operations=operations, result=None))
    
    operations = [
        Operation(OperationType.GROUP_BY, ["Is Fork", True])
    ]
    
    user.add_query(Query(operations=operations, result=None))
    
    executor = Executor(processor)
    for query_name in user.get_queries().keys():
        executor.execute_query_and_compute_stats(user, query_name)
    
    stats_to_csv(executor.get_all_queries_stats(), "csv_results.csv")

if __name__ == "__main__":
    main()
