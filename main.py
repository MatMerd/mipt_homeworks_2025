from typing import Dict, Any, List

from homework_oop.reader import ReaderCSV
from homework_oop.repository.query import Query
from homework_oop.repository.repomodel import repository_model, Repository
from homework_oop.repository.reposprocessor import ReposProcessor


def read_repos() -> List[Repository]:
    repos = []
    with ReaderCSV('./homework_oop/repositories.csv', repository_model) as rows:
        for row in rows:
            repo = Repository(
                name=row['Name'],
                description=row['Description'],
                url=row['URL'],
                created_at=row['Created At'],
                updated_at=row['Updated At'],
                homepage=row['Homepage'],
                size=row['Size'],
                stars=row['Stars'],
                forks=row['Forks'],
                issues=row['Issues'],
                watchers=row['Watchers'],
                language=row['Language'],
                license=row['License'],
                topics=row['Topics'],
                has_issues=row['Has Issues'],
                has_projects=row['Has Projects'],
                has_downloads=row['Has Downloads'],
                has_wiki=row['Has Wiki'],
                has_pages=row['Has Pages'],
                has_discussions=row['Has Discussions'],
                is_fork=row['Is Fork'],
                is_archived=row['Is Archived'],
                is_template=row['Is Template'],
                default_branch=row['Default Branch']
            )
            repos.append(repo)
    return repos



def main():
    repos: List[Repository] = read_repos()
    query: Query = Query(sort_by='Size', filters= {'Language': 'TypeScript'})
    res: Dict[Any, List[Repository]] = ReposProcessor.execute(repos, 1, query)
    print(res)
    print("Hello from mipt-homeworks-2025!")


if __name__ == "__main__":
    main()
