from datetime import datetime


class Repository:
    def __init__(
            self,
            name: str,
            description: str,
            url: str,
            created_at: str,
            updated_at: str,
            homepage: str,
            size: int,
            stars: int,
            forks: int,
            issues: int,
            watchers: int,
            language: str,
            license: str,
            topics: list[str],
            has_issues: bool,
            has_projects: bool,
            has_downloads: bool,
            has_wiki: bool,
            has_pages: bool,
            has_discussions: bool,
            is_fork: bool,
            is_archived: bool,
            is_template: bool,
            default_branch: str
    ):
        self.name = name
        self.description = description
        self.url = url
        self.created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        self.updated_at = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
        self.homepage = homepage
        self.size = size
        self.stars = stars
        self.forks = forks
        self.issues = issues
        self.watchers = watchers
        self.language = language
        self.license = license
        self.topics = topics
        self.has_issues = has_issues
        self.has_projects = has_projects
        self.has_downloads = has_downloads
        self.has_wiki = has_wiki
        self.has_pages = has_pages
        self.has_discussions = has_discussions
        self.is_fork = is_fork
        self.is_archived = is_archived
        self.is_template = is_template
        self.default_branch = default_branch

    def __repr__(self):
        return (f'{self.name}, {self.description}, {self.url}, {self.created_at}, '
                f'{self.updated_at}, {self.homepage}, {self.size}, {self.stars}, '
                f'{self.forks}, {self.issues}, {self.watchers}, {self.language}')
