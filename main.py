from typing import Dict, Any, List

from homework_oop.reader import ReaderCSV
from homework_oop.repository.query import Query
from homework_oop.repository.repomodel import repository_model
from homework_oop.repository.reposprocessor import ReposProcessor


def read_repos() -> List[Dict[str, Any]]:
    with ReaderCSV('./homework_oop/repositories.csv', repository_model) as repos:
        return repos


def main():
    repos: List[Dict[str, Any]] = read_repos()
    query: Query = Query(sort_by='Size', filters= {'Language': 'TypeScript'})
    reposProcessor = ReposProcessor(repos, 1, query)
    res: Dict[Any, List[Dict[str, Any]]] = reposProcessor.execute()
    print("Hello from mipt-homeworks-2025!")


if __name__ == "__main__":
    main()
