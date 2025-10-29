from typing import List, Dict, Any, Union
from datacls import OperationType, QueryStats
from user import User
from data_processor import DataProcessor

class Executor:
    '''
    Класс для исполнения запросов и сохранения их статистик
    
    Fields:
    queries_stats - Статистики запросов.
    processor - дата процессор, исполняющий запросы.
    '''
    def __init__(self, processor: DataProcessor):
        self.queries_stats: list[Union[QueryStats, list[QueryStats]]] = []
        self.processor = processor
        
    def __getitem__(self, key) -> Union[QueryStats, list[QueryStats]]:
        return self.queries_stats[key]
    
    def get_all_queries_stats(self) -> list[Union[QueryStats, list[QueryStats]]]:
        return self.queries_stats
    
    def _get_size_median(self, repos: List[Dict[str, Any]]) -> int:
        if "Size" not in repos[0].keys():
            return None
        sorted_repos = sorted(repos, key=lambda arg: arg["Size"])
        median_index = (len(sorted_repos) + 1) // 2
        return sorted_repos[median_index]["Size"]
    
    def _get_most_liked_repo(self, repos: List[Dict[str, Any]]) -> dict[str, Any]:
        if "Stars" not in repos[0].keys():
            return None
        most_liked = max(repos, key=lambda arg: arg["Stars"])
        return most_liked
    
    def _get_longest_name_repo(self, repos: List[Dict[str, Any]]) -> dict[str, Any]:
        if "Name" not in repos[0].keys():
            return None
        most_liked = max(repos, key=lambda arg: len(arg["Name"]))
        return most_liked
    
    def _get_no_lang_repos(self, repos: List[Dict[str, Any]]) -> list[dict[str, Any]]:
        if "Language" not in repos[0].keys():
            return None
        no_lang_repos = [item for item in repos if item["Language"] == ""]
        return no_lang_repos
    
    def _get_top_no_commits_repos(self, repos: List[Dict[str, Any]]) -> list[dict[str, Any]]:
        if "Size" not in repos[0].keys():
            return None
        sorted_repos = sorted(repos, key=lambda arg: arg["Size"]) # placeholder
        return sorted_repos[:10]
        
    def execute_query_and_compute_stats(self, user: User, user_query_name: str):
        '''
        Выполняет запрос, сохраняя результат в юзера. Также считает статистики результата запроса и сохраняет в себя.
        Args:
            user - Пользователь, имеющий запросы.
            user_query_name - Имя запроса.
        '''
        query = user.get_query(user_query_name)
        
        for operation in query.operations:
            if operation.operation_type == OperationType.SORT:
                sort_type = operation.args[-1]
                for arg in operation.args[:-1]:
                    self.processor = self.processor.sort_by(arg, sort_type)
            elif operation.operation_type == OperationType.SELECT:
                self.processor = self.processor.select(operation.args)
            elif operation.operation_type == OperationType.GROUP_BY:
                self.processor = self.processor.group_by(operation.args[0])
            elif operation.operation_type == OperationType.WHERE:
                self.processor = self.processor.where(operation.args[0])
            elif operation.operation_type == OperationType.LIMIT:
                self.processor = self.processor.limit(operation.args[0])
                
        query_result = self.processor.execute()
        self.processor = self.processor.reset()
        user.set_query_result(user_query_name, query_result)
        query_stats: Union[QueryStats, list[QueryStats]]
        
        if (isinstance(query_result, list)):
            query_stats = QueryStats(
                median=self._get_size_median(query_result),
                most_liked_repo=self._get_most_liked_repo(query_result),
                longest_name_repo=self._get_longest_name_repo(query_result),
                no_lang_repos=self._get_no_lang_repos(query_result),
                top_no_commits_repos=self._get_top_no_commits_repos(query_result)
                )
        elif (isinstance(query_result, dict)):
            query_stats = []
            for repo_list in query_result.values():
                query_stats.append(QueryStats(
                median=self._get_size_median(repo_list),
                most_liked_repo=self._get_most_liked_repo(repo_list),
                longest_name_repo=self._get_longest_name_repo(repo_list),
                no_lang_repos=self._get_no_lang_repos(repo_list),
                top_no_commits_repos=self._get_top_no_commits_repos(repo_list)
                ))
                
        self.queries_stats.append(query_stats)
