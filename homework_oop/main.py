import csv
import json
from enum import IntEnum
import statistics
from typing import Self, TypedDict, Generator, Iterable, Callable, Literal
from datetime import datetime
from dataclasses import dataclass, field
from functools import cmp_to_key
from copy import deepcopy


RepositoryField = Literal[
    "name",
    "description",
    "url",
    "created_at",
    "updated_at",
    "homepage",
    "size",
    "stars",
    "forks",
    "issues",
    "watchers",
    "language",
    "topics",
    "has_issues",
    "has_projects",
    "has_downloads",
    "has_wiki",
    "has_pages",
    "has_discussions",
    "is_fork",
    "is_archived",
    "is_template",
    "default_branch",
]


class RawRepository(TypedDict):
    name: str
    description: str
    url: str
    created_at: str
    updated_at: str
    homepage: str
    size: str
    stars: str
    forks: str
    issues: str
    watchers: str
    language: str
    license: str
    topics: list[str]
    has_issues: str
    has_projects: str
    has_downloads: str
    has_wiki: str
    has_pages: str
    has_discussions: str
    is_fork: str
    is_archived: str
    is_template: str
    default_branch: str


class Repository(TypedDict):
    name: str
    description: str
    url: str
    created_at: datetime
    updated_at: datetime
    homepage: str
    size: int
    stars: int
    forks: int
    issues: int
    watchers: int
    language: str
    license: str
    topics: list[str]
    has_issues: bool
    has_projects: bool
    has_downloads: bool
    has_wiki: bool
    has_pages: bool
    has_discussions: bool
    is_fork: bool
    is_archived: bool
    is_template: bool
    default_branch: str

    @classmethod
    def new(cls, raw: RawRepository) -> Self:
        return {
            **raw,
            **{key: datetime.fromisoformat(raw[key]) for key in ["created_at", "updated_at"]},
            **{key: int(raw[key]) for key in ["size", "stars", "forks", "issues", "watchers"]},
            **{
                key: bool(raw[key])
                for key in [
                    "has_issues",
                    "has_projects",
                    "has_downloads",
                    "has_wiki",
                    "has_pages",
                    "has_discussions",
                    "is_fork",
                    "is_archived",
                    "is_template",
                ]
            },
        }


@dataclass
class Reader:
    filename: str
    delimiter: str = ","

    def iter(self) -> Generator[Repository]:
        fieldnames = list(RawRepository.__annotations__.keys())
        with open(self.filename, "r", encoding="utf-8") as file:
            file.readline()  # skip CSV header as we provide our own
            reader = csv.DictReader(file, delimiter=self.delimiter, fieldnames=fieldnames)
            for repo in reader:
                yield Repository.new(repo)


class Ordering(IntEnum):
    ASC = 0
    DESC = 1


class Transform:
    filters: list[Callable[[Repository], bool]]
    group_keys: set[RepositoryField]
    sort_keys: dict[RepositoryField, Ordering]

    def __init__(self) -> None:
        self.filters = []
        self.group_keys = set()
        self.sort_keys = {}

    def filter(self, fn: Callable[[Repository], bool]) -> Self:
        self.filters.append(fn)
        return self

    def group_by(self, *fields: RepositoryField) -> Self:
        for field in fields:  # noqa: F402
            if field not in RepositoryField.__args__:
                raise ValueError(f"Field `{field}` does not exist")
            if field in self.sort_keys:
                raise ValueError(f"Field `{field}` can't act as both grouping and sorting key")
            if field in self.group_keys:
                raise ValueError(f"Field `{field}` is already used as grouping key")
            self.group_keys.add(field)
        return self

    def sort(self, *fields: tuple[RepositoryField, Ordering]) -> Self:
        for field, ordering in fields:  # noqa: F402
            if field not in RepositoryField.__args__:
                raise ValueError(f"Field `{field}` does not exist")
            if field in self.group_keys:
                raise ValueError(f"Field `{field}` can't act as both grouping and sorting key")
            if field in self.sort_keys:
                raise ValueError(f"Field `{field}` is already used as a sorting key")
            self.sort_keys[field] = ordering
        return self

    def execute(
        self,
        repos: Iterable[Repository],
        limit: int = -1,
    ) -> list[Repository] | dict[tuple, list[Repository]]:
        def get_group_key(repo: Repository) -> tuple:
            return tuple(repo[key] for key in self.group_keys)

        def compare_repos(first: Repository, second: Repository) -> int:
            for key, ordering in self.sort_keys.items():
                if first[key] == second[key]:
                    continue
                cmp = -1 if first[key] < second[key] else 1
                if ordering == Ordering.DESC:
                    return -cmp
                return cmp
            return 0

        inserted = 0
        result: list[Repository] | dict[tuple, list[Repository]] = (
            [] if len(self.group_keys) == 0 else {}
        )
        for repo in repos:
            if not all(filter(repo) for filter in self.filters):
                continue
            if isinstance(result, list):
                result.append(repo)
            else:
                key = get_group_key(repo)
                if key not in result:
                    result[key] = []
                result[key].append(repo)
            inserted += 1
            if limit != -1 and inserted >= limit:
                break
        if isinstance(result, list):
            result.sort(key=cmp_to_key(compare_repos))
        else:
            for group in result.values():
                group.sort(key=cmp_to_key(compare_repos))
        return result


@dataclass
class User:
    transforms: dict[str, Transform]

    def __init__(self) -> None:
        self.transforms = {}

    def save_transform(self, name: str, transform: Transform) -> Self:
        if name in self.transforms:
            raise ValueError(f"Transform with name `{name}` already exists")
        self.transforms[name] = deepcopy(transform)
        return self

    def get_transform(self, name: str) -> Transform | None:
        return self.transforms.get(name)


@dataclass
class Stats:
    sizes: list[int] = field(default_factory=list)
    most_popular: Repository | None = None
    without_language: list[Repository] = field(default_factory=list)
    without_language_limit: int = 10
    most_forks: list[Repository] = field(default_factory=list)
    most_forks_limit: int = 10

    def process(self, repo: Repository) -> Self:
        self.sizes.append(repo["size"])
        if self.most_popular is None or self.most_popular["stars"] < repo["stars"]:
            self.most_popular = repo
        if not repo["language"] and len(self.without_language) < self.without_language_limit:
            self.without_language.append(repo)
        self.most_forks.append(repo)
        self.most_forks.sort(key=lambda repo: repo["forks"], reverse=True)
        if len(self.most_forks) > self.most_forks_limit:
            self.most_forks.pop()
        return self

    def process_many(self, iter: Iterable[Repository]) -> Self:
        for repo in iter:
            self.process(repo)
        return self

    def dump_json(self, filename: str) -> Self:
        stats = {
            "median_size": statistics.median_high(self.sizes),
            "most_popular_repo": {
                "name": self.most_popular["name"],
                "url": self.most_popular["url"],
                "stars": self.most_popular["stars"],
            },
            "repos_without_language": [
                {"name": repo["name"], "url": repo["url"]} for repo in self.without_language
            ],
            "repos_with_most_forks": [
                {"name": repo["name"], "url": repo["url"], "forks": repo["forks"]}
                for repo in self.most_forks
            ],
        }
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(stats, file)
        return self

    def dump_csv(self, filename: str) -> Self:
        stats = {
            "Median size": statistics.median_high(self.sizes),
            "Most popular repo": f"{self.most_popular['name']}={self.most_popular['stars']}",
            "Repos without language": ";".join(repo["name"] for repo in self.without_language),
            "Repos with most forks": ";".join(
                f"{repo['name']}={repo['forks']}" for repo in self.most_forks
            ),
        }
        with open(filename, "w", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=list(stats.keys()))
            writer.writeheader()
            writer.writerow(stats)
        return self