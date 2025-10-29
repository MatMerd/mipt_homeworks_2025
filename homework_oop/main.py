from datacls import OperationType, Operation, Query
from user import User
from csv_reader import RepositoryCSVReader
from data_processor import DataProcessor
from executor import Executor
from csv_writer import to_csv

def main():
    reader = RepositoryCSVReader('repositories.csv')
    data = reader.read_all()

    processor = DataProcessor(data)
        
    user = User("Gassy")
    
    # Query 1
    
    operations = [
        Operation(OperationType.SELECT, ["Name", "Stars"]),
        Operation(OperationType.SORT, ["Stars", True])
    ]
    
    user.add_query(Query(operations=operations, result=None))
    
    # Query 2
    
    operations = [
        Operation(OperationType.WHERE, [(lambda x: int(x["Stars"]) > 1000)]),
        Operation(OperationType.SELECT, ["Name", "Stars", "Size", "Language"]),
        Operation(OperationType.SORT, ["Stars", "Size", True]), 
        Operation(OperationType.LIMIT, [10])
    ]
    
    user.add_query(Query(operations=operations, result=None))
    
    # Query 3
    
    operations = [
        Operation(OperationType.WHERE, [(lambda x: int(x["Stars"]) > 10000)]),
        Operation(OperationType.SELECT, ["Name", "Stars", "Size", "Language"]),
        Operation(OperationType.SORT, ["Size", True]), 
        Operation(OperationType.LIMIT, [100])
    ]
    
    user.add_query(Query(operations=operations, result=None))
    
    # Query 4
    
    operations = [
        Operation(OperationType.GROUP_BY, ["Is Archived", True]),
    ]
    
    user.add_query(Query(operations=operations, result=None))
    
    executor = Executor(processor)
    for query_name in user.get_queries().keys():
        executor.execute_query_and_compute_stats(user, query_name)
    
    to_csv(executor.get_all_queries_stats(), "all_stats.csv")
    
    
if __name__ == "__main__":
    main()